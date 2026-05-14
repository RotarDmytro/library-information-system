# Основи програмування. Курсовий проєкт за 2 курс. Інформаційна система бібліотеки

import json
import hashlib
import os

data = {}

current_user = None
reader_name = None

issue_date = ""
return_date = ""
day = 0
month = 0
year = 0

book_library = []

choice = ['librarian', 'reader']

my_book = []

dictionary_my = {}


# Блок №1. База даних бібліотеки
def function_reader_quick_search(request_answer_book):
    if request_answer_book in data["dictionary_book"]:
        return "Книга знайдена!\nАвтор: " + str(data["dictionary_book"][request_answer_book])
    else:
        return 'Не відповідає заданим даним'


def function_reader_by_genre(request_5, request_8):
    if request_5 in data["dictionary_author"]:
        request_name = data["dictionary_author"][request_5]
        if isinstance(request_name, list):
            request_name = request_name[0] if request_name else ''
        dictionary_my.update({'name': request_name})

        available_years = list(data["dictionary_library"][request_name]["editions"]["default"].keys())

        if request_8 in data["dictionary_library"][request_name]["editions"]["default"]:
            edition = data["dictionary_library"][request_name]["editions"]["default"][request_8]
            dictionary_my.update({'year': request_8})
            dictionary_my.update({
                'language': edition["language"],
                'binding': edition["binding"],
                'price': edition["price"]
            })
            return dictionary_my
        else:
            return 'Не відповідає заданим даним'
    else:
        return 'Не відповідає заданим даним'


def function_reader_get_genre_years(request_5):
    if request_5 in data["dictionary_author"]:
        request_name = data["dictionary_author"][request_5]
        return list(data["dictionary_library"][request_name]["editions"]["default"].keys())
    return []


def function_reader_by_type(etype, request_book, request_year):
    if request_book in data["dictionary_library"] and etype in data["dictionary_library"][request_book]["editions"]:
        if request_year in data["dictionary_library"][request_book]["editions"][etype]:
            edition = data["dictionary_library"][request_book]["editions"][etype][request_year]
            dictionary_my.update({
                'book': request_book,
                'year': request_year,
                'language': edition["language"],
                'binding': edition["binding"],
                'price': edition["price"]
            })
            return dictionary_my
        else:
            return "Не відповідає заданим даним"
    else:
        return "Не відповідає заданим даним"


def function_reader_get_books_by_type(etype):
    result = {}
    for book in data["dictionary_library"]:
        if etype in data["dictionary_library"][book]["editions"]:
            years = list(data["dictionary_library"][book]["editions"][etype].keys())
            if years:
                result[book] = years
    return result


def function_reader_accessories(request_accessories):
    found = False
    for book in data["dictionary_library"]:
        if "accessories" in data["dictionary_library"][book]["editions"]:
            if request_accessories in data["dictionary_library"][book]["editions"]["accessories"]:
                dictionary_my.update({'book': request_accessories})
                found = True
                break
    if not found:
        return "Не відповідає заданим даним"
    return dictionary_my


def function_reader_get_accessories():
    result = {}
    for book in data["dictionary_library"]:
        if "accessories" in data["dictionary_library"][book]["editions"]:
            items = list(data["dictionary_library"][book]["editions"]["accessories"].keys())
            result[book] = items
    return result


def function_reader_by_index(request_index):
    found = False
    for book in data["dictionary_library"]:
        if "editions" in data["dictionary_library"][book]:
            for edition_type in data["dictionary_library"][book]["editions"]:
                if edition_type != "accessories":
                    for year in data["dictionary_library"][book]["editions"][edition_type]:
                        if "index" in data["dictionary_library"][book]["editions"][edition_type][year]:
                            if str(data["dictionary_library"][book]["editions"][edition_type][year]["index"]) == request_index:
                                dictionary_my.update({'book': book})
                                found = True
                                break
    if not found:
        return 'Не відповідає заданим даним'
    return dictionary_my


def function_reader_return(extend):
    global reader_name

    # Шукаємо видану книгу поточного читача в JSON
    issued = data.get("issued_books", [])
    entry = None
    entry_idx = None
    for i, rec in enumerate(issued):
        if rec.get("reader") == reader_name:
            entry = rec
            entry_idx = i
            break

    if entry is None:
        return "Спочатку має бути видача книги"

    if extend:
        # Продовжуємо від поточної дати повернення
        parts = entry["return_date"].split(".")
        d, m, y = int(parts[0]), int(parts[1]), int(parts[2])
        m += 3
        while m > 12:
            m -= 12
            y += 1
        new_return = f"{d}.{m}.{y}"
        data["issued_books"][entry_idx]["return_date"] = new_return
        json_a_d_c_base()
        return f"Книга: {entry['book']}\nНовий термін повернення: {new_return}"
    else:
        # Повернення — видаляємо запис
        data["issued_books"].pop(entry_idx)
        json_a_d_c_base()
        return f"Книга '{entry['book']}' повернена. Дата видачі: {entry['issue_date']}"


# Блок №2. Вхід
def function_exit(login_exit, password_exit):
    global current_user, reader_name

    user = data["login_password"].get(login_exit)

    if not user:
        return None, "Помилка в логіні"

    if user.get('password') != fast_hash(password_exit):
        return None, "Помилка в паролі"

    current_user = user
    reader_name = user.get('reader_name')

    reader_data = None
    if reader_name:
        reader_data = data["dictionary_reader"].get(reader_name)

    regime = user.get('role')

    return regime, f"Вхід успішний ({regime})"


# Блок №3. Реєстрація
def function_registration(login, password, role):
    if role == "бібліотекар":
        role = "librarian"
    elif role == "читач":
        role = "reader"
    else:
        return "Невірна роль"

    if not (7 <= len(login) <= 15):
        return 'Не відповідає умові (логін від 7 до 15)'

    if not (6 <= len(password) <= 10):
        return 'Не відповідає умові (пароль від 6 до 10)'

    if login in data["login_password"]:
        return 'Такий аккаунт зареєстрований'

    if role == "librarian" or role == "reader":
        hashed = fast_hash(password)
        data["login_password"][login] = {
            "password": hashed,
            "role": role
        }
        return "Користувач доданий"


# Блок №4. Бібліотекар

# Блок №4.1. Бібліотекар "Знайти"
def function_librarian_find(name, author, genre, index, edition_type, year):
    if name in data["dictionary_library"]:
        book = data["dictionary_library"][name]

        if author == book['author']:
            if genre == book['genre']:
                if edition_type in book['editions']:

                    my_book.append(name)
                    my_book.append(author)
                    my_book.append(genre)
                    my_book.append(edition_type)

                    if edition_type == "accessories":
                        return "Знайдено аксесуари: " + str(book['editions'][edition_type])

                    else:
                        try:
                            year = int(year)

                            if year in book['editions'][edition_type]:
                                my_book.append(year)
                                return str(my_book) + "\n" + str(book['editions'][edition_type][year])

                            else:
                                return "Такого року видання немає"

                        except ValueError:
                            return "Рік повинен бути числом"

                else:
                    return "Такого типу видання немає"

            else:
                return "Жанр не співпадає"

        else:
            return "Автор не співпадає"
    else:
        return "Такої книги немає"


# Блок №4.2. Бібліотекар "Картка читача"
def function_librarian_card(reader_card):
    reader_card = reader_card.title().strip()
    reader_card = reader_card.split("-")
    reader_card = '-'.join(reader_card)

    if reader_card in data["dictionary_reader"]:
        return data["dictionary_reader"][reader_card]
    else:
        return 'Немає такого читача'


# Блок №4.3. Бібліотекар "Реєстрація читача"
def function_librarian_register_reader(name, surname, father, email, phone, birth, ticket, login, password, confirm_password):
    reader_key = f"{name}-{surname}-{father}".title()

    if reader_key in data["dictionary_reader"]:
        return "Такий читач вже існує!"

    if login in data["login_password"]:
        return "Такий логін вже використовується!"

    if password != confirm_password:
        return "Паролі не співпадають!"

    if not (7 <= len(login) <= 15):
        return "Логін має бути від 7 до 15 символів!"

    if not (6 <= len(password) <= 10):
        return "Пароль має бути від 6 до 10 символів!"

    data["dictionary_reader"][reader_key] = {
        "ticket_number": ticket,
        "mail": email,
        "tel": phone,
        "date_of_birth": birth,
        "limit": 3,
        "login": login
    }

    data["login_password"][login] = {
        "password": fast_hash(password),
        "role": "reader",
        "reader_name": reader_key
    }

    json_a_d_c_base()
    return "Успішна реєстрація"


# Блок №4.4. Бібліотекар "Видача книги"
def function_librarian_issue(book_name, reader_name, issue_date_input):
    global issue_date, return_date, day, month, year

    book_finally = []

    if book_name in data["dictionary_library"]:
        book_finally.append(book_name)

        if reader_name in data["dictionary_reader"]:
            book_finally.append(reader_name)

            date_parts = issue_date_input.split(".")
            day = int(date_parts[0])
            month = int(date_parts[1])
            year = int(date_parts[2])

            ret_month = month + 3
            ret_year = year
            while ret_month > 12:
                ret_month -= 12
                ret_year += 1

            return_date = f"{day}.{ret_month}.{ret_year}"
            issue_date = issue_date_input

            book_finally.append(issue_date)
            book_finally.append(return_date)

            book_library.append(book_finally)

            # ПОЯСНЕННЯ. Зберігаємо у JSON щоб читач бачив видачу після перезапуску
            if "issued_books" not in data:
                data["issued_books"] = []
            data["issued_books"].append({
                "book": book_name,
                "reader": reader_name,
                "issue_date": issue_date,
                "return_date": return_date
            })
            json_a_d_c_base()

            return "Книга видана: " + str(book_finally)

        else:
            return "Немає такого читача"

    else:
        return "Немає такої книги"


# Блок №4.5. Бібліотекар "Видані екземпляри"
def function_librarian_issued():
    issued = data.get("issued_books", [])
    if issued:
        return [[r["book"], r["reader"], r["issue_date"], r["return_date"]] for r in issued]
    else:
        return "Немає виданих книг"


# Блок №4.6. Бібліотекар "Фільтр"
def function_librarian_filter(book_character):
    if book_character in data["dictionary_genre"]:
        return data["dictionary_genre"][book_character]
    else:
        return 'Немає жанру'


# Додання
def function_librarian_add(answer_where, *args):
    if answer_where == 'dictionary_library':
        name, author, genre, index, year, edition_type, language, binding, price = args

        year = int(year)

        if name not in data["dictionary_library"]:
            data["dictionary_library"][name] = {
                "author": author,
                "genre": genre,
                "editions": {}
            }

        if edition_type not in data["dictionary_library"][name]["editions"]:
            data["dictionary_library"][name]["editions"][edition_type] = {}

        data["dictionary_library"][name]["editions"][edition_type][year] = {
            "index": index,
            "language": language,
            "binding": binding,
            "price": price
        }

        json_a_d_c_base()
        return "Книгу додано успішно!"

    elif answer_where == 'dictionary_genre':
        genre, name = args

        if genre not in data["dictionary_genre"]:
            data["dictionary_genre"][genre] = []

        data["dictionary_genre"][genre].append(name)

        json_a_d_c_base()
        return "Додано успішно!"

    elif answer_where == 'login_password':
        login, password, role, reader_name = args

        login = login.strip()
        password = password.strip()
        role = role.strip().lower()
        reader_name = reader_name.strip()

        if not (7 <= len(login) <= 15):
            return "Логін має бути від 7 до 15 символів!"

        elif not (6 <= len(password) <= 10):
            return "Пароль має бути від 6 до 10 символів!"

        elif role not in ["reader", "librarian"]:
            return "Роль має бути тільки: reader або librarian!"

        else:
            if login not in data["login_password"]:
                data["login_password"][login] = {
                    "password": fast_hash(password),
                    "role": role,
                    "reader_name": reader_name
                }

                json_a_d_c_base()
                return "Додано успішно!"
            else:
                return "Такий логін вже існує!"

    elif answer_where == 'dictionary_reader':
        reader_name, limit, login, tel, ticket_number, date_of_birth, mail = args

        login = login.strip().lower()
        reader_name = reader_name.strip()
        mail = mail.strip().lower()
        tel = tel.strip()

        if not (7 <= len(login) <= 15):
            return "Логін має бути від 7 до 15 символів!"

        elif not (tel.startswith("+") and len(tel) == 13 and tel[1:].isdigit()):
            return "Не є телефоном! Формат: +380XXXXXXXXX"

        elif not ("@" in mail and "." in mail):
            return "Не є ел. поштою!"

        else:
            if reader_name not in data["dictionary_reader"]:
                data["dictionary_reader"][reader_name] = {
                    "limit": int(limit),
                    "login": login,
                    "tel": tel,
                    "ticket_number": ticket_number,
                    "date_of_birth": date_of_birth,
                    "mail": mail
                }

                json_a_d_c_base()
                return "Додано успішно!"
            else:
                return "Такий читач вже існує!"

    elif answer_where == 'dictionary_book':
        name, author = args

        name = name.strip().lower()
        author = author.strip().lower()

        if name not in data["dictionary_book"]:
            data["dictionary_book"][name] = author

            json_a_d_c_base()
            return "Додано успішно!"

        else:
            return "Вже є така книга!"

    elif answer_where == 'dictionary_author':
        author, name = args

        author = author.strip().lower()
        name = name.strip().lower()

        if author not in data["dictionary_author"]:
            data["dictionary_author"][author] = name
        else:
            pass  # автор вже є

        json_a_d_c_base()
        return "Додано успішно!"

    else:
        return 'Помилка введення!'


# Видалення
def function_librarian_delete(answer_where, *args):
    if answer_where == 'dictionary_library':
        answer_del = args[0].strip()
        if answer_del not in data["dictionary_library"]:
            return 'Такої книги немає!'
        else:
            del data["dictionary_library"][answer_del]
            json_a_d_c_base()
            return 'Книгу видалено!'

    elif answer_where == 'dictionary_genre':
        genre, name = args
        genre = genre.strip()
        name = name.strip()

        if genre not in data["dictionary_genre"]:
            return 'Такої жанру немає!'
        elif name not in data["dictionary_genre"][genre]:
            return 'Такої книги немає!'
        else:
            data["dictionary_genre"][genre].remove(name)
            if not data["dictionary_genre"][genre]:
                del data["dictionary_genre"][genre]
            json_a_d_c_base()
            return 'Книгу видалено!'

    elif answer_where == 'login_password':
        answer_del = args[0].strip().lower()
        if answer_del not in data["login_password"]:
            return 'Такого логіну немає!'
        else:
            del data["login_password"][answer_del]
            json_a_d_c_base()
            return 'Логін видалено!'

    elif answer_where == 'dictionary_reader':
        answer_del = args[0].strip()
        if answer_del not in data["dictionary_reader"]:
            return 'Такого читача немає!'
        else:
            del data["dictionary_reader"][answer_del]
            json_a_d_c_base()
            return 'Читача видалено!'

    elif answer_where == 'dictionary_book':
        answer_del = args[0].strip()
        if answer_del not in data["dictionary_book"]:
            return 'Такої книги немає!'
        else:
            del data["dictionary_book"][answer_del]
            json_a_d_c_base()
            return 'Книгу видалено!'

    elif answer_where == 'dictionary_author':
        answer_del = args[0].strip()
        if answer_del not in data["dictionary_author"]:
            return 'Такого автора немає!'
        else:
            del data["dictionary_author"][answer_del]
            json_a_d_c_base()
            return 'Автора видалено!'

    else:
        return 'Помилка введення!'

# Хеш-функція
def fast_hash(password):
    password = hashlib.sha256(password.encode()).hexdigest()
    return password

# Блок №8.1. Підключення json
def json_connect_base():
    global data, book_character_choose

    '''
        ПОЯСНЕННЯ. 
        Створення захищеної змінної, яка містить в собі логічний вираз:
        1. Отримання шляху до файлу, неважливо чи відносного, чи абсолютного
        2. Повернення абсолютного шляху, навіть якщо він є відносним
        3. Повернення папки, де знаходиться файл
        4. Об'єднання папки та бажаного файлу
    '''

    _path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'base.json')
    with open(_path, encoding='utf-8') as f:
        data = json.load(f)
    book_character_choose = list(data.get("dictionary_genre", {}).keys())

# Блок 8.2. Додавання у базу даних, видалення з неї та редагування
def json_a_d_c_base():
    _path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'base.json')
    with open(_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
