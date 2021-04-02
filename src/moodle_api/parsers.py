import re
from typing import Dict, List
import bs4
from bs4 import NavigableString
from bs4 import BeautifulSoup


def _contains_answer(string):
    if not string:
        return False
    return 'Правильный' in string or 'правильный' in string


def parse_cmid(url: str) -> str:
    try:
        return re.findall(r'id=\d+$', url)[0][len('id='):]
    except IndexError:
        raise ValueError('Incorrect task URL')


class TaskMetadata:
    def __init__(self, content: bytes):
        self._content = content
        self._task_metadata = None

    @property
    def task_metadata(self):
        if not self._task_metadata:
            cmid = re.findall(r'cmid-\d+', str(self._content))
            if cmid:
                cmid = cmid[0][len('cmid-'):]
            else:
                cmid = None
            sesskey = re.findall(r'sesskey=\w+', str(self._content))
            if sesskey:
                sesskey = sesskey[0][len('sesskey='):]
            else:
                sesskey = None
            self._task_metadata = {'cmid': cmid, 'sesskey': sesskey}
        return self._task_metadata

    @property
    def cmid(self):
        return self.task_metadata['cmid']

    @property
    def sesskey(self):
        return self.task_metadata['sesskey']


def parse_plain_text_answers(soup) -> dict:
    correct_answers = {}
    for tag in soup.find_all('input'):
        if 'sub' not in tag.get('name', ''):
            continue
        to_iterate = tag.parent.find_all('span', {'class': 'feedbackspan'})
        if not to_iterate:
            continue
        for i in to_iterate[0].contents:
            if _contains_answer(i):
                correct_ans = i.split(': ')[1]
                correct_answers.update({
                    tag['name'].split(':')[1]: correct_ans})
    return correct_answers


def remove_duplicates(l):
    prev = None
    res = []
    for elem in l:
        if elem != prev:
            res.append(elem)
        prev = elem
    return res


def remove_last_digit(string):
    return re.search(r'(.*)[^\d]', string).group(0)


def remove_prefix(string):
    return string.split(':')[1]


def parse_radio_button_answers(soup):
    correct_answers = []
    radio_tags = soup.find_all('input', {'type': 'radio', 'id': re.compile(r'q\d+:\d.*')})
    if not radio_tags:
        return {}
    questions = [remove_last_digit(x['id']) for x in radio_tags]
    # remove duplicates
    questions = remove_duplicates(questions)
    i = 0
    for tags in soup.find_all('div', {'class': 'outcome'}):
        for ans_candidate in tags.contents:
            if _contains_answer(ans_candidate):
                correct_answer = ans_candidate.split(': ')[1]
                correct_answers.append([questions[i].split(':')[1], correct_answer])
                i += 1
    if not correct_answers:
        return {}
    # Build mapper
    i = 0
    for tag in radio_tags:
        if tag.next.text == correct_answers[i][1] and remove_prefix(remove_last_digit(tag['id'])) == correct_answers[i][0]:
            correct_answers[i][1] = tag['value']
            i += 1
        if i == len(correct_answers):
            # no need for further processing
            break
    return dict(correct_answers)


def parse_picker_answers(soup):
    correct_answers = {}
    task_fields = set()
    for tmp in soup.find_all('select'):
        if 'sub' in tmp.get('name', ''):
            task_fields.add(tmp['name'])
    for field in task_fields:
        tag = soup.find_all('select', {'name': field})
        if len(tag) == 0:
            continue
        for i in tag[0].parent.find_all():
            for content in i.contents:
                if _contains_answer(content):
                    correct_ans = content.split(': ')[1]
                    # Ищем номер позиции пикера, соответствующий ответу. Опять тяжко
                    for option in soup.find_all('select', {'name': field})[0].find_all('option'):
                        if option.text == correct_ans:
                            correct_ans = option['value']
                    correct_answers.update({
                        field.split(':')[1]: correct_ans})
    return correct_answers


def parse_checkbox_answers(soup):
    task_fields = set()
    prefix = None
    for possible_tag in soup.find_all('input', {'type': 'checkbox'}):
        prefix_and_field = re.findall(r'.*:\d+_choice\d+', possible_tag.get('id', ''))
        if not prefix_and_field:
            continue
        prefix, field = prefix_and_field[0].split(':')
        task_fields.add(field)
    result = dict(zip(task_fields, ['0']*len(task_fields)))
    tmp = soup.find_all('div', {'class': 'rightanswer'})
    right_answers = []
    for i in tmp:
        right_answers.append([x.strip() for x in i.contents[0].split(':')[1].split(',')])
    for field in task_fields:
        for label_tag in soup.find_all('label', {'for': f'{prefix}:{field}'}):
            for string in label_tag.contents:
                if not isinstance(string, NavigableString):
                    continue
                for i, arr in enumerate(right_answers[int(field.split('_')[0])-1]):
                    if string in arr:
                        result[field] = '1'
    return result


def parse_one_string_answers(soup: BeautifulSoup) -> Dict[str, str]:
    """
    Парсит страницы с ответом в тегах
    <div class="rightanswer" id="yui_3_17_2_1_1597047509273_134">Правильный ответ: make a living</div>

    :param soup: Суп из страницы
    :return: словарь правильных ответов
    """
    result = {}     # type: Dict[str, str]
    answer_tags = soup.find_all(attrs={'class': 'rightanswer'}) # type: List[bs4.Tag]
    for tag in answer_tags:
        # Ищем ответ
        # После split() будет ['', <содержательно>], поэтому [1:] + join() (если в ответе есть ':')
        ans = ''.join(re.split(r'Правильный ответ: ', tag.get_text())[1:])
        # Если ответа нет, сразу выходим - парсер не работает
        if not ans:
            break
        # Ищем соответствующий 1sub_ans...
        # Для этого идем вверх по дереву и на каждом уровне по соседям запускаем поиск в глубину (shit!)
        # пока не найдем тег по регулярке 'q\d+:.*'
        current_tag = tag
        found_name = ''
        while not found_name:
            candidate = ''  # type: str
            for child in current_tag.findChildren(recursive=True):    # type: bs4.Tag
                if 'id' in child.attrs:
                    candidate = re.findall(r'q\d+:.*', child.attrs['id'])   # type: List[str]
                    if len(candidate) != 1:
                        candidate = ''
                        continue
                    candidate = candidate[0].split(':')[1]   # type: str
                    break
            found_name = candidate
            current_tag = current_tag.parent
        result.update({found_name: ans})
    return result


def parse_answers(soup):
    result = dict()
    handlers = [parse_plain_text_answers, parse_radio_button_answers, parse_picker_answers,
                parse_checkbox_answers, parse_one_string_answers]
    while handlers:
        result.update(handlers.pop()(soup))
    return result
