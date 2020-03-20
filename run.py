import requests
import bs4
from urllib.parse import urlparse, parse_qs
from settings import LOGIN, PASSWORD, HOMEWORK_URLS, MEAN_URLS


def get_login_token(session):
    """
    Нужен токен, без него не авторизует
    """
    soup = bs4.BeautifulSoup(session.get('http://moodle.phystech.edu/my/').content)
    return soup.find('input', {'name': 'logintoken'})['value']


def authorize(session, login, password):
    # 2. Авторизация
    token = get_login_token(session)
    response = session.post('http://moodle.phystech.edu/login/index.php',
          {'username': login, 'password': password, 'anchor': '', 'logintoken': token}
         )
    return response


def is_authorized(session):
    # 1. Проверка авторизации
    response = session.get('http://moodle.phystech.edu/my/')
    parsed = bs4.BeautifulSoup(response.content)
    return 'Вход' not in str(parsed.title)


def start_task(session, task_metadata):
    # 4. Стартуем задание
    # Note: `task_id` === `cmid`
    response = session.post(
        'http://moodle.phystech.edu/mod/quiz/startattempt.php',
        task_metadata
    )
    task_fields = set([x.get('name')
                   for x in bs4.BeautifulSoup(response.content).find_all('input', {'class': 'form-control'})])
    if None in task_fields:
        task_fields.remove(None)
    task_url = response.url
    return task_fields, task_url, response


def load_task(session, task_url):
    # 3. Метаданные задания
    soup = bs4.BeautifulSoup(session.get(task_url).content)
    cmid = soup.find('div', {'class': 'quizstartbuttondiv'}).input.find('input', {'name': 'cmid'})['value']
    sess_key = soup.find('input', {'name': 'sesskey'})['value']
    soup.find_all('input', {'class': 'form-control'})
    return {'cmid': cmid, 'sesskey': sess_key}


def upload_answers(session, answer_dict: dict, task_metadata, task_fields, attempt_number):
    data = {'sesskey': task_metadata['sesskey'], 'nextpage': -1, 'attempt': attempt_number,
            'next': 'Закончить попытку...', 'scrollpos': '', 'thispage': 0, 'timeup': 0, 'slots': 1}
    for elem in task_fields:
        # HACK: some strange field
        data.update({'{}:1_:flagged'.format(elem.split(':')[0]): 0})
        data.update({'{}:1_:sequencecheck'.format(elem.split(':')[0]): 1})
        break
    if len(answer_dict) == 0:
        # Пустые ответы
        for key in task_fields:
            data.update({key: ''})
    else:
        for key in task_fields:
            # Ищем подходящий ответ. Коварный мудл меняет ключи, но я тоже не дурак!
            # Короче, тут проблема такая: было "q50228:блабла1" - а становится "q50229:блабла1"
            # Ключевой момент: блабла1 остается тем же, на этом и сыграем!
            correct_key = None
            for key1 in answer_dict.keys():
                if key1.split(':')[1] == key.split(':')[1]:
                    correct_key = key1
                    break
            data.update({key: answer_dict[correct_key]})

    response = session.post(
        'http://moodle.phystech.edu/mod/quiz/processattempt.php?cmid={}'.format(task_metadata['cmid']),
        data
    )
    return response


def finish_attempt(session, attempt_number, task_metadata):
    response = session.post(
        'http://moodle.phystech.edu/mod/quiz/processattempt.php',
        {'attempt': attempt_number, 'finishattempt': 1,
         'cmid': task_metadata['cmid'], 'sesskey': task_metadata['sesskey']}
    )
    return response


def get_answers(session, task_fields, attempt_number, task_metadata):
    response = session.get(
        'http://moodle.phystech.edu/mod/quiz/review.php?attempt={}&cmid={}'
            .format(attempt_number, task_metadata['cmid'])
    )
    soup = bs4.BeautifulSoup(response.content)
    result = {}
    for field in task_fields:
        tag = soup.find_all('input', {'name': field})
        for i in tag[0].parent.find_all('span', {'class': 'feedbackspan'})[0].contents:
            if 'ильный' in i:
                correct_ans = i.split(': ')[1]
                result.update({field: correct_ans})
    return result


def cheat_on(s, url):
    task_metadata = load_task(s, url)
    task_fields, task_url, response = start_task(s, task_metadata)
    attempt_number = parse_qs(urlparse(task_url).query)['attempt'][0]
    upload_answers(s, answer_dict={}, task_metadata=task_metadata, task_fields=task_fields,
                   attempt_number=attempt_number)
    finish_attempt(s, attempt_number=attempt_number, task_metadata=task_metadata)
    answers = get_answers(s, task_fields=task_fields, attempt_number=attempt_number, task_metadata=task_metadata)
    # А теперь, девочки и мальчики, пора заполнять правильные ответы
    task_fields, task_url, response = start_task(s, task_metadata)
    attempt_number = parse_qs(urlparse(task_url).query)['attempt'][0]
    upload_answers(s, answer_dict=answers, task_metadata=task_metadata, task_fields=task_fields,
                   attempt_number=attempt_number)
    finish_attempt(s, attempt_number=attempt_number, task_metadata=task_metadata)


if __name__ == '__main__':
    s = requests.Session()
    if not is_authorized(s):
        authorize(s, login=LOGIN, password=PASSWORD)

    for url in HOMEWORK_URLS:
        cheat_on(s, url)
    for url in MEAN_URLS:
        for _ in range(40):
            cheat_on(s, url)
