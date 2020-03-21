import bs4


def _contains_answer(string):
    if not string:
        return False
    return 'Правильный' in string or 'правильный' in string


def _clean_rubbish(task_fields):
    result = set()
    for item in task_fields:
        if item is not None and 'sub' in item:
            result.add(item)
    return result


def parse_plain_text_task(soup):
    task_fields = set([x.get('name')
                       for x in soup.find_all('input', {'class': 'form-control'})])
    return _clean_rubbish(task_fields)


def parse_radio_button_task(soup):
    task_fields = set([x.get('name') for x in soup.find_all('input', {'type': 'radio'})])
    # Clean rubbish
    return _clean_rubbish(task_fields)


def parse_picker_task(soup):
    result = set()
    for tag in soup.find_all('select'):
        if 'sub' in tag.get('id', []):
            result.add(tag['id'])
    return _clean_rubbish(result)


def parse_plain_text_answers(soup, task_fields):
    correct_answers = {}
    for tag in soup.find_all('input'):
        if 'sub' not in tag.get('name', ''):
            continue
        for i in tag.parent.find_all('span', {'class': 'feedbackspan'})[0].contents:
            if _contains_answer(i):
                correct_ans = i.split(': ')[1]
                correct_answers.update({tag['name']: correct_ans})
    return correct_answers


def parse_radio_button_answers(soup, task_fields):
    correct_answers = {}
    for all_ans_tag in soup.find_all('div', {'class': 'answer'}):
        # Правильный ответ идет прямо в следующем теге
        for ans_candidate in all_ans_tag.nextSibling.contents:
            if _contains_answer(ans_candidate):
                correct_answer = ans_candidate.split(': ')[1]
                # Теперь надо найти тег, который соответствует этому ответу. Боже, дай мне силы
                for label in all_ans_tag.find_all('label'):
                    if label.text == correct_answer:
                        correct_answer = label.parent.next['value']
                        break
                correct_answers.update({all_ans_tag.next.find('input')['name']: correct_answer})
    return correct_answers


def parse_picker_answers(soup, task_fields):
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
                    correct_answers.update({field: correct_ans})
    return correct_answers


def parse_task_fields(response):
    soup = bs4.BeautifulSoup(response.content)
    result = set()
    handlers = [parse_plain_text_task, parse_radio_button_task, parse_picker_task]
    handlers = handlers.copy()
    while handlers:
        result = result.union(handlers.pop()(soup))
    return result


def parse_answers(response, task_fields):
    soup = bs4.BeautifulSoup(response.content)
    result = dict()
    handlers = [parse_plain_text_answers, parse_radio_button_answers, parse_picker_answers]
    while handlers:
        result.update(handlers.pop()(soup, task_fields))
    return result
