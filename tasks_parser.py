import bs4

def _contains_answer(string):
    return 'Правильный' in string or 'правильный' in string


def parse_plain_text_task(soup, task_fields):
    task_fields = set([x.get('name')
                       for x in soup.find_all('input', {'class': 'form-control'})])
    if None in task_fields:
        task_fields.remove(None)
    return task_fields


def parse_radio_button_task(soup, task_fields):
    task_fields = set([x.get('name') for x in soup.find_all('input', {'type': 'radio'})])
    # Clean rubbish
    result = set()
    for item in task_fields:
        if 'sub' in item:
            result.add(item)
    return result


def parse_plain_text_answers(soup, task_fields):
    correct_answers = {}
    for field in task_fields:
        tag = soup.find_all('input', {'name': field})
        for i in tag[0].parent.find_all('span', {'class': 'feedbackspan'})[0].contents:
            if _contains_answer(i):
                correct_ans = i.split(': ')[1]
                correct_answers.update({field: correct_ans})
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


def parser_factory(parsers):
    def parser(response, task_fields: set = frozenset()):
        soup = bs4.BeautifulSoup(response.content)
        result = None
        handlers = parsers.copy()
        while not result:
            try:
                result = handlers.pop()(soup, task_fields)
            except IndexError:
                raise NotImplementedError(f'Cannot process task with URL {response.url}')
        return result
    return parser


parse_task_fields = parser_factory([parse_plain_text_task, parse_radio_button_task])
parse_answers = parser_factory([parse_plain_text_answers, parse_radio_button_answers])
