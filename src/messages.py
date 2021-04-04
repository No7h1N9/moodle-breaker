FIRST_ENTRY_MESSAGE = """
Кажется, я тебя раньше не видел. Добро пожаловать!
Мне понадобится твои логин и пароль от мудла, чтобы оперировать дальше.
Пожалуйста, введи их в следующем сообщении в формате:

login@mail.ru
password

Обязательно раздели их переносом строки. Я иначе читать пока не умею.
Эти данные никому не уйдут.
Если ты не хочешь делиться оттого, что используешь один и тот же \
пароль для мудла и остальных сервисов, то у меня для тебя плохие новости: мудл \
не использует шифрования в своем сайте и твои пароли может запросто прочитать \
любой человек в твоей сети. Рекомендую сменить пароль на мудле на уникальный \
и уже быть готовым воспользоваться нашим сервисом. 
"""

INCORRECT_LOGIN_INPUT = """
У меня не получилось прочитать логин и/или пароль :(
Пожалуйста, убедись, что вводишь их в формате:

login@mail.ru
password

Здесь перенос строки обязателен! Если ничего не работает, пиши админам в личку.
Сообщение с логином и паролем можешь удалить, чтобы его никто не увидел :)
"""

CORRECT_LOGIN_INPUT = """
У меня получилось считать твой логин и пароль. Сейчас попробую зайти под ним на мудл... 
Сообщение с логином и паролем можешь удалить, чтобы его никто не увидел :)
"""

MOODLE_ACCEPTED_LOGIN = """
Мудл принял логин. Мы готовы блистать!
Теперь ты можешь отправлять мне ссылку на задание, а я попробую его взломать.

Ссылки могут быть вида:
http://moodle.phystech.edu/mod/quiz/view.php?id=30805
http://moodle.phystech.edu/mod/quiz/review.php?attempt=528310&cmid=30805

Остальные пока не протестированы.
Взлом базируется на том, что мудл показывает ответы после первой попытки. \
Если этого не происходит, я пока ничего не смогу сделать :(
ВНИМАНИЕ! НЕ используй этот сервис для заданий с ограниченным числом попыток, а так же заданий с \
ограничением по времени. Они не были протестированы и могут не работать. Я буду благодарен, \
если ты отправишь мне пример такого задания.
"""

MOODLE_DECLINED_LOGIN = """
Мудл не принял логин :(
Проверь еще раз, пожалуйста.
"""

CORRECT_TASK_URL = """
Мне удалось считать ссылку на задание. Начинаю взлом...
"""

INCORRECT_TASK_URL = """
Мне не удалось прочитать строку с заданием. Убедись, что ввел её одном из форматов:

http://moodle.phystech.edu/mod/quiz/view.php?id=30805
http://moodle.phystech.edu/mod/quiz/review.php?attempt=528310&cmid=30805
"""

BREAKING_DONE = """
Взлом завершен. Проверяй мудл :)

Если что-то не сработало, сохрани страницу с заданием (ее скрины обычно в общий чат кидают) в формате .htm или .html \
и отправь админам группы. Это делается через Ctrl+S в Windows/Linux, Cmd+S в MacOS

Кстати, я умею сразу несколько раз делать одно и то же задание. Для этого надо писать число перед ссылкой, например,

3 http://moodle.phystech.edu/mod/quiz/review.php?attempt=832803&cmid=36258

Это может тебе пригодится в заданиях со средним баллом.
"""

FIELDS_ARE_MISSING = """
Я не смог определить ответы на некоторые задания. Обычно это случается по следующим причинам:

1) Мудл не показывает ответы в принципе. В этом случае я бессилен, к сожалению.
2) Этот тип задания еще не поддерживается. В таком случае сохрани страницу с заданием \
(ее скрины обычно в общий чат кидают) в формате .htm или .html \
и отправь админам группы. Это делается через Ctrl+S в Windows/Linux, Cmd+S в MacOS.
3) Мудл переклинило и он не показал ответы на лучшую попытку, хотя должен был. Такое тоже бывает и \
я не знаю, почему :) Вбей ссылку с заданием еще раз и мы сможем узнать наверняка.

Я не завершил попытку, чтобы не запороть тебе задание. 

Кстати, я умею сразу несколько раз делать одно и то же задание. Для этого надо писать число перед ссылкой, например,

3 http://moodle.phystech.edu/mod/quiz/review.php?attempt=832803&cmid=36258

Это может тебе пригодится в заданиях со средним баллом.
"""
