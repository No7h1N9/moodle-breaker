import re
from urllib.parse import parse_qs, urlparse
import bs4
from src.utils import to_float, logger
from src.moodle_api.parsers import parse_answers


class Page:
    def __init__(self, page_content: bytes):
        self.soup = bs4.BeautifulSoup(page_content, features='lxml')
        self.content = page_content


class SummaryPage(Page):
    def best_attempt_id(self):
        soup = self.soup
        all_attempts = soup.find_all('tr')[1:]  # Первый - это хидер таблицы

        best_attempt, total_cols = None, None
        try:
            # Надо определить, где находится твоя оценка
            total_cols = all_attempts[0].find_all('td', {'class', 'lastcol'})[0]['class']
            ide = [item for i, item in enumerate(total_cols) if re.search(r'c\d', item)]
            if ide:
                total_cols = int(ide[0][1:])

            all_attempts.sort(key=lambda tag: to_float(
                # В 'c3' содержится твоя оценка
                tag.find('td', {'class': f'c{total_cols - 1}'}).text.replace(',', '.')
            ))
            best_attempt = all_attempts.pop()
            # BUG: best_attempt может указывать неоконченную попытку, если та единственна
        except IndexError:
            logger.info('could not parse best own attempt. Proceeding as the first run...')
        best_url = None
        if best_attempt:
            try:
                best_url = best_attempt.find('a', {'title': 'Просмотр своих ответов этой попытки'})['href']
            except TypeError:
                # Если есть незавершенная попытка, он не сможет найти 'href' у следующего тега
                # Поэтому мы просто пометим best_attempt в None
                logger.info('first own attempt and not finished. `best_url` is set to None')
        return parse_qs(urlparse(best_url).query).get('attempt', [None])[0]


class FinishedAttemptPage(Page):
    def parse_answers(self) -> dict:
        return parse_answers(self.soup)


class RunningAttemptPage(Page):
    def __init__(self, page_content: bytes):
        super().__init__(page_content)
        self._id, self._prefix, self._all_questions = None, None, None

    @property
    def prefix(self) -> str:
        if not self._prefix:
            try:
                self._prefix = re.findall(r'q\d+:', str(self.content))[0][:-1]
            except IndexError:
                self._prefix = None
        return self._prefix

    @property
    def id(self) -> str:
        if not self._id:
            try:
                self._id = re.findall(r'\d+', re.findall(r'attempt=\d+', str(self.content))[0])[0]
            except IndexError:
                self._id = None
        return self._id

    @property
    def all_questions(self) -> set:
        if not self._all_questions:
            try:
                self._all_questions = set([x[:-1] for x in re.findall(r'\d+_sub\d+_answer"', str(self.content))])
            except:
                self._all_questions = None
        return self._all_questions
