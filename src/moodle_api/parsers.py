import re


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


def parse_radio_button_answers(soup):
    correct_answers = {}
    for all_ans_tag in soup.find_all('div', {'class': 'answer'}):
        # Правильный ответ идет прямо в следующем теге
        if not all_ans_tag.nextSibling:
            continue
        for ans_candidate in all_ans_tag.nextSibling.contents:
            if _contains_answer(ans_candidate):
                correct_answer = ans_candidate.split(': ')[1]
                # Теперь надо найти тег, который соответствует этому ответу. Боже, дай мне силы
                for label in all_ans_tag.find_all('label'):
                    if label.text == correct_answer:
                        correct_answer = label.parent.next['value']
                        break
                correct_answers.update({
                    all_ans_tag.next.find('input')['name'].split(':')[1]: correct_answer})
    return correct_answers


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


def parse_answers(soup):
    result = dict()
    handlers = [parse_plain_text_answers, parse_radio_button_answers, parse_picker_answers]
    while handlers:
        result.update(handlers.pop()(soup))
    return result
