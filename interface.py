# ПРИМІТКА. Підключення сторонніх бібліотека і файлів

import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import ttk, messagebox
import tkinter as tk
import function as fn
from function import *

# УВАГА! Підключення функціоналу та умовної бази даних

def get_data():
    return fn.data
json_connect_base()
json_a_d_c_base()


# ПРИМІТКА. Створення інтерфейсу

class App:

    # ПРИМІТКА. Батьківський клас зі сталими параметрами

    class _BaseWindow:
        def __init__(self, root):
            self.root = root
            self.main_menu = tk.Menu(root)
            self.root.config(menu=self.main_menu)

            self.reader_menu = tk.Menu(self.main_menu, tearoff=0)
            self.main_menu.add_cascade(label="Читачі", menu=self.reader_menu)
            self.reader_menu.add_command(label="Реєстрація", command=self.open_card_reg)
            self.reader_menu.add_command(label="Картка читача", command=self.open_card_reader)

            self.book_menu = tk.Menu(self.main_menu, tearoff=0)
            self.main_menu.add_cascade(label="Книги", menu=self.book_menu)
            self.book_menu.add_command(label="Додати", command=self.open_book_add)
            self.book_menu.add_command(label="Видалити", command=self.open_book_del)
            self.book_menu.add_separator()
            self.book_menu.add_command(label="Видати", command=self.open_issue)
            self.book_menu.add_command(label="Видані екземпляри", command=self.open_issued)

        def open_card_reg(self):
            top = tk.Toplevel(self.root)
            App.Librarian_Card_reg(top)

        def open_card_reader(self):
            top = tk.Toplevel(self.root)
            App.Librarian_Card_reader(top)

        def open_book_add(self):
            top = tk.Toplevel(self.root)
            App.Librarian_Book_add(top)

        def open_book_del(self):
            top = tk.Toplevel(self.root)
            App.Librarian_Book_del(top)

        def open_issue(self):
            top = tk.Toplevel(self.root)
            App.Librarian_Issue(top)

        def open_issued(self):
            top = tk.Toplevel(self.root)
            App.Librarian_Issued(top)

    # ПРИМІТКА. Вхід в систему

    class Exit:
        def __init__(self, root):
            self.root = root
            self.root.title("Вхід в систему")
            self.root.geometry("400x270")
            self.root.resizable(False, False)

            ttk.Label(self.root, text="Логін:").place(relx=0.2, rely=0.1)
            ttk.Label(self.root, text="Пароль:").place(relx=0.2, rely=0.3)
            ttk.Label(self.root, text="Роль:").place(relx=0.2, rely=0.5)

            self.ent_login = ttk.Entry(self.root, width=20)
            self.ent_login.place(relx=0.43, rely=0.1)
            self.ent_password = ttk.Entry(self.root, width=20, show="*")
            self.ent_password.place(relx=0.43, rely=0.3)

            self.listbox = tk.Listbox(self.root, width=20, height=2, exportselection=False)
            self.listbox.insert(1, "Бібліотекар")
            self.listbox.insert(2, "Читач")
            self.listbox.place(relx=0.43, rely=0.5)

            self.btn_ok = ttk.Button(self.root, text="Вхід", width=6, command=self.do_login)
            self.btn_ok.place(relx=0.3, rely=0.8)
            self.btn_cancel = ttk.Button(self.root, text="Відміна", width=7, command=self.root.destroy)
            self.btn_cancel.place(relx=0.55, rely=0.8)

        # Функція для малювання дочірнього вікна згідно вибору ролі

        def do_login(self):
            login = self.ent_login.get().strip().lower()
            password = self.ent_password.get().strip()

            role, msg = function_exit(login, password)

            if role is None:
                messagebox.showerror("Помилка", msg)
                return

            self.root.withdraw()          
            new_root = tb.Toplevel()      
            if role == "librarian":
                App.Librarian(new_root)
            else:
                App.Reader(new_root)
                new_root.protocol("WM_DELETE_WINDOW", self.root.destroy)  

    # ПРИМІТКА. Головне меню бібліотекаря

    class Librarian(_BaseWindow):
        def __init__(self, root):
            self.root = root
            self.root.title("Головне меню бібліотекаря")
            self.root.geometry("770x400")
            self.root.resizable(False, False)
            super().__init__(root)

            self.frame_up = ttk.Frame(self.root, width=560, height=40)
            self.frame_up.place(x=100, y=2)
            ttk.Label(self.frame_up, text="Пошук:").place(x=10, y=8)
            self.entry_search = ttk.Entry(self.frame_up, width=60)
            self.entry_search.place(x=80, y=8)
            self.button_search = ttk.Button(self.frame_up, text="Знайти", width=10, command=self.do_search)
            self.button_search.place(x=460, y=6)

            self.frame_tree = ttk.Frame(self.root, width=560, height=330, relief='groove', borderwidth=2)
            self.frame_tree.place(x=14, y=50)
            self.column = ('№', 'Назва книги', 'Автор', 'Жанр', 'Індекс', 'За типом', 'Рік видання', 'Наявність')
            self.tree = ttk.Treeview(self.frame_tree, columns=self.column, show='headings', height=14)
            self.tree.column('№', width=30, anchor='center', stretch=False)
            self.tree.column('Назва книги', width=150, anchor='center', stretch=False)
            self.tree.column('Автор', width=100, anchor='center', stretch=False)
            self.tree.column('Жанр', width=100, anchor='center', stretch=False)
            self.tree.column('Індекс', width=80,  anchor='center', stretch=False)
            self.tree.column('За типом', width=80,  anchor='center', stretch=False)
            self.tree.column('Рік видання', width=80,  anchor='center', stretch=False)
            self.tree.column('Наявність', width=80,  anchor='center', stretch=False)

            for col in self.column:
                self.tree.heading(col, text=col)

            self.tree.pack(fill='both', expand=True)

            self.scroll_y = ttk.Scrollbar(self.frame_tree, orient="vertical", command=self.tree.yview)
            self.tree.configure(yscrollcommand=self.scroll_y.set)
            self.scroll_y.pack(side='right', fill='y')
            self.tree.pack(side='left', fill='both', expand=True)

            self.frame_down = ttk.Frame(self.root, width=707, height=27, relief='groove', borderwidth=2)
            self.frame_down.place(x=16, y=370)
            self.label_count = ttk.Label(self.frame_down, text="Всього книг: ")
            self.label_count.place(x=10, y=0)
            self.label_cor_count = ttk.Label(self.frame_down, text="0")
            self.label_cor_count.place(x=100, y=0)
            self.label_role = ttk.Label(self.frame_down, text="Роль: Бібліотекар")
            self.label_role.place(x=590, y=0)

            json_connect_base()
            self.load_tree()

        def load_tree(self, filter_text=""):
            for row in self.tree.get_children():
                self.tree.delete(row)
            i = 1
            for name, book in fn.data["dictionary_library"].items():
                if filter_text and filter_text.lower() not in name.lower() \
                        and filter_text.lower() not in book.get('author', '').lower():
                    continue
                for etype, editions in book["editions"].items():
                    if etype == "accessories":
                        continue
                    for yr, ed in editions.items():
                        self.tree.insert('', 'end', values=(
                            i, name, book.get('author', ''), book.get('genre', ''),
                            ed.get('index', ''), etype, yr, 'є'
                        ))
                        i += 1
            self.label_cor_count.config(text=str(i - 1))

        def do_search(self):
            self.load_tree(self.entry_search.get().strip())

    # ПРИМІТКА. Картка читача

    class Librarian_Card_reader(_BaseWindow):
        def __init__(self, root):
            self.root = root
            self.root.title("Картка читача")
            self.root.geometry("980x400")
            self.root.resizable(False, False)
            super().__init__(root)

            self.frame_up = ttk.Frame(self.root, width=560, height=40)
            self.frame_up.place(x=100, y=2)
            ttk.Label(self.frame_up, text="Пошук:").place(x=10, y=8)
            self.entry_search = ttk.Entry(self.frame_up, width=60)
            self.entry_search.place(x=80, y=8)
            self.button_search = ttk.Button(self.frame_up, text="Знайти", width=10, command=self.do_search)
            self.button_search.place(x=460, y=6)

            self.frame_tree = ttk.Frame(self.root, width=960, height=330, relief='groove', borderwidth=2)
            self.frame_tree.place(x=14, y=50)
            self.column = ('№', "Ім'я", 'Прізвище', 'Квиток', 'Телефон', 'Дата народження', 'Ел. пошта', 'Видано', 'Повернуто', 'Заборгованість')
            self.tree = ttk.Treeview(self.frame_tree, columns=self.column, show='headings', height=14)
            self.tree.column('№', width=30, anchor='center', stretch=False)
            self.tree.column("Ім'я", width=100, anchor='center', stretch=False)
            self.tree.column('Прізвище', width=100, anchor='center', stretch=False)
            self.tree.column('Квиток', width=80,  anchor='center', stretch=False)
            self.tree.column('Телефон', width=100, anchor='center', stretch=False)
            self.tree.column('Дата народження', width=110, anchor='center', stretch=False)
            self.tree.column('Ел. пошта', width=150, anchor='center', stretch=False)
            self.tree.column('Видано', width=80,  anchor='center', stretch=False)
            self.tree.column('Повернуто', width=80,  anchor='center', stretch=False)
            self.tree.column('Заборгованість', width=100, anchor='center', stretch=False)

            for col in self.column:
                self.tree.heading(col, text=col)
            self.tree.pack(fill='both', expand=True)

            self.scroll_y = ttk.Scrollbar(self.frame_tree, orient="vertical", command=self.tree.yview)
            self.tree.configure(yscrollcommand=self.scroll_y.set)
            self.scroll_y.pack(side='right', fill='y')
            self.tree.pack(side='left', fill='both', expand=True)

            self.frame_down = ttk.Frame(self.root, width=953, height=27, relief='groove', borderwidth=2)
            self.frame_down.place(x=14, y=370)
            self.label_count = ttk.Label(self.frame_down, text="Всього читачів: ")
            self.label_count.place(x=10, y=0)
            self.label_cor_count = ttk.Label(self.frame_down, text="0")
            self.label_cor_count.place(x=120, y=0)
            self.label_role = ttk.Label(self.frame_down, text="Роль: Бібліотекар")
            self.label_role.place(x=820, y=0)

            self.load_tree()

        def load_tree(self, filter_text=""):
            for row in self.tree.get_children():
                self.tree.delete(row)
            i = 1
            for pib, rd in fn.data["dictionary_reader"].items():
                parts = pib.split("-")
                name    = parts[0] if len(parts) > 0 else ""
                surname = parts[1] if len(parts) > 1 else ""
                if filter_text and filter_text.lower() not in pib.lower():
                    continue
                self.tree.insert('', 'end', values=(
                    i, name, surname,
                    rd.get('ticket_number', ''),
                    rd.get('tel', ''),
                    rd.get('date_of_birth', ''),
                    rd.get('mail', ''),
                    0, 0, 0
                ))
                i += 1
            self.label_cor_count.config(text=str(i - 1))

        def do_search(self):
            self.load_tree(self.entry_search.get().strip())

    # ПРИМІТКА. Реєстрація читача

    class Librarian_Card_reg(_BaseWindow):
        def __init__(self, root):
            self.root = root
            self.root.title("Реєстрація читача")
            self.root.geometry("700x500")
            self.root.resizable(False, False)
            super().__init__(root)

            ttk.Label(self.root, text="Номер:").place(x=70, y=30)
            ttk.Label(self.root, text="Квиток:").place(x=70, y=80)
            ttk.Label(self.root, text="Ім'я:").place(x=70, y=130)
            ttk.Label(self.root, text="Прізвище:").place(x=70, y=180)
            ttk.Label(self.root, text="Ел. пошта:").place(x=70, y=230)
            ttk.Label(self.root, text="Телефон:").place(x=70, y=280)
            ttk.Label(self.root, text="Дата народження:").place(x=70, y=330)
            ttk.Label(self.root, text="Логін:").place(x=400, y=30)
            ttk.Label(self.root, text="Пароль:").place(x=400, y=80)
            ttk.Label(self.root, text="Підтвердження:").place(x=400, y=130)

            self.frame_info = ttk.Frame(self.root, width=200, height=105, relief='groove', borderwidth=2)
            self.frame_info.place(x=400, y=200)
            ttk.Label(self.frame_info, text="Відомості").place(x=2, y=2)
            ttk.Label(self.frame_info, text="Видано:").place(x=25, y=25)
            self.label_cor_vydano = ttk.Label(self.frame_info, text="0")
            self.label_cor_vydano.place(x=80, y=25)
            ttk.Label(self.frame_info, text="Повернуто:").place(x=25, y=50)
            self.label_cor_pov = ttk.Label(self.frame_info, text="0")
            self.label_cor_pov.place(x=105, y=50)
            ttk.Label(self.frame_info, text="Заборгованість:").place(x=25, y=75)
            self.label_cor_zab = ttk.Label(self.frame_info, text="0")
            self.label_cor_zab.place(x=130, y=75)

            self.ent_number = ttk.Entry(self.root, width=20)
            self.ent_number.place(x=205, y=30)
            self.ent_ticket = ttk.Entry(self.root, width=20)
            self.ent_ticket.place(x=205, y=80)
            self.ent_name = ttk.Entry(self.root, width=20)
            self.ent_name.place(x=205, y=130)
            self.ent_surname = ttk.Entry(self.root, width=20)
            self.ent_surname.place(x=205, y=180)
            self.ent_post = ttk.Entry(self.root, width=20, foreground='grey')
            self.ent_post.place(x=205, y=230)
            self.ent_phone = ttk.Entry(self.root, width=20, foreground='grey')
            self.ent_phone.place(x=205, y=280)
            self.ent_birthdate = ttk.Entry(self.root, width=20, foreground='grey')
            self.ent_birthdate.place(x=205, y=330)
            self.ent_login = ttk.Entry(self.root, width=20)
            self.ent_login.place(x=520, y=30)
            self.ent_password = ttk.Entry(self.root, width=20, show="*")
            self.ent_password.place(x=520, y=80)
            self.ent_confirm_password = ttk.Entry(self.root, width=20, show="*")
            self.ent_confirm_password.place(x=520, y=130)

            self.btn_ok = ttk.Button(self.root, text="Зареєструвати", width=15, command=self.do_register)
            self.btn_ok.place(x=250, y=400)
            self.btn_cancel = ttk.Button(self.root, text="Відміна", width=10, command=self.root.destroy)
            self.btn_cancel.place(x=400, y=400)

            self.frame_down = ttk.Frame(self.root, width=670, height=27, relief='groove', borderwidth=2)
            self.frame_down.place(x=14, y=460)
            self.label_count = ttk.Label(self.frame_down, text="Всього читачів: ")
            self.label_count.place(x=10, y=0)
            self.label_cor_count = ttk.Label(self.frame_down, text=str(len(fn.data["dictionary_reader"])))
            self.label_cor_count.place(x=120, y=0)
            self.label_role = ttk.Label(self.frame_down, text="Роль: Бібліотекар")
            self.label_role.place(x=540, y=0)

            self.ent_post.bind('<FocusIn>',  self.on_entry_click_post)
            self.ent_post.bind('<FocusOut>', self.on_focusout_post)
            self.ent_post.insert(0, 'example@mail.com')

            self.ent_phone.bind('<FocusIn>',  self.on_entry_click_phone)
            self.ent_phone.bind('<FocusOut>', self.on_focusout_phone)
            self.ent_phone.insert(0, '+380XXXXXXXXX')

            self.ent_birthdate.bind('<FocusIn>',  self.on_entry_click_birthdate)
            self.ent_birthdate.bind('<FocusOut>', self.on_focusout_birthdate)
            self.ent_birthdate.insert(0, 'DD.MM.YYYY')

        def do_register(self):
            msg = function_librarian_register_reader(
                self.ent_name.get().strip(),
                self.ent_surname.get().strip(),
                self.ent_number.get().strip(),
                self.ent_post.get().strip(),
                self.ent_phone.get().strip(),
                self.ent_birthdate.get().strip(),
                self.ent_ticket.get().strip(),
                self.ent_login.get().strip().lower(),
                self.ent_password.get().strip(),
                self.ent_confirm_password.get().strip()
            )
            if "Успішна" in msg:
                messagebox.showinfo("Готово", msg)
                self.root.destroy()
            else:
                messagebox.showerror("Помилка", msg)

        def on_entry_click_post(self, event):
            if self.ent_post.get() == 'example@mail.com':
                self.ent_post.delete(0, "end")
                self.ent_post.insert(0, '')
                self.ent_post.config(foreground='black')

        def on_entry_click_phone(self, event):
            if self.ent_phone.get() == '+380XXXXXXXXX':
                self.ent_phone.delete(0, "end")
                self.ent_phone.insert(0, '')
                self.ent_phone.config(foreground='black')

        def on_entry_click_birthdate(self, event):
            if self.ent_birthdate.get() == 'DD.MM.YYYY':
                self.ent_birthdate.delete(0, "end")
                self.ent_birthdate.insert(0, '')
                self.ent_birthdate.config(foreground='black')

        def on_focusout_post(self, event):
            if self.ent_post.get() == '':
                self.ent_post.insert(0, 'example@mail.com')
                self.ent_post.config(foreground='grey')

        def on_focusout_phone(self, event):
            if self.ent_phone.get() == '':
                self.ent_phone.insert(0, '+380XXXXXXXXX')
                self.ent_phone.config(foreground='grey')

        def on_focusout_birthdate(self, event):
            if self.ent_birthdate.get() == '':
                self.ent_birthdate.insert(0, 'DD.MM.YYYY')
                self.ent_birthdate.config(foreground='grey')

    # ПРИМІТКА. Додавання книги

    class Librarian_Book_add(_BaseWindow):
        def __init__(self, root):
            self.root = root
            self.root.title("Додавання книги")
            self.root.geometry("760x400")
            self.root.resizable(False, False)
            super().__init__(root)

            self.frame_main = ttk.Frame(self.root, width=740, height=350, relief='groove', borderwidth=2)
            self.frame_main.place(x=10, y=10)

            ttk.Label(self.frame_main, text="За типом:").place(x=10, y=10)
            ttk.Label(self.frame_main, text="Назва книги:").place(x=10, y=40)
            ttk.Label(self.frame_main, text="Автор:").place(x=10, y=70)
            ttk.Label(self.frame_main, text="Жанр:").place(x=10, y=100)
            ttk.Label(self.frame_main, text="Індекс:").place(x=10, y=130)
            ttk.Label(self.frame_main, text="Рік видання:").place(x=10, y=160)
            ttk.Label(self.frame_main, text="Мова:").place(x=10, y=190)
            ttk.Label(self.frame_main, text="Палітурка:").place(x=10, y=220)
            ttk.Label(self.frame_main, text="Ціна:").place(x=10, y=250)

            types = ["default", "new", "hot", "action", "accessories"]
            self.combo_type = ttk.Combobox(self.frame_main, values=types, state="readonly", width=27)
            self.combo_type.current(0)
            self.combo_type.place(x=120, y=10)

            self.entry_name = ttk.Entry(self.frame_main, width=30)
            self.entry_name.place(x=120, y=40)
            self.entry_author = ttk.Entry(self.frame_main, width=30)
            self.entry_author.place(x=120, y=70)
            self.entry_genre = ttk.Entry(self.frame_main, width=30)
            self.entry_genre.place(x=120, y=100)
            self.entry_index = ttk.Entry(self.frame_main, width=30)
            self.entry_index.place(x=120, y=130)
            self.entry_year = ttk.Entry(self.frame_main, width=30)
            self.entry_year.place(x=120, y=160)
            self.entry_language = ttk.Entry(self.frame_main, width=30)
            self.entry_language.place(x=120, y=190)
            self.entry_binding = ttk.Entry(self.frame_main, width=30)
            self.entry_binding.place(x=120, y=220)
            self.entry_price = ttk.Entry(self.frame_main, width=30)
            self.entry_price.place(x=120, y=250)

            ttk.Button(self.frame_main, text="Додати",  width=12, command=self.do_add).place(x=120, y=290)
            ttk.Button(self.frame_main, text="Відміна", width=10, command=self.root.destroy).place(x=280, y=290)

            self.frame_down = ttk.Frame(self.root, width=740, height=27, relief='groove', borderwidth=2)
            self.frame_down.place(x=10, y=370)
            self.label_count = ttk.Label(self.frame_down, text="Всього книг: ")
            self.label_count.place(x=10, y=0)
            self.label_cor_count = ttk.Label(self.frame_down, text=str(len(fn.data["dictionary_library"])))
            self.label_cor_count.place(x=100, y=0)
            self.label_role = ttk.Label(self.frame_down, text="Роль: Бібліотекар")
            self.label_role.place(x=610, y=0)

        def do_add(self):
            msg = function_librarian_add(
                'dictionary_library',
                self.entry_name.get().strip(),
                self.entry_author.get().strip(),
                self.entry_genre.get().strip(),
                self.entry_index.get().strip(),
                self.entry_year.get().strip(),
                self.combo_type.get(),
                self.entry_language.get().strip(),
                self.entry_binding.get().strip(),
                self.entry_price.get().strip()
            )
            if "успішно" in msg:
                messagebox.showinfo("Готово", msg)
                self.root.destroy()
            else:
                messagebox.showerror("Помилка", msg)

    # ПРИМІТКА. Видалення книги

    class Librarian_Book_del(_BaseWindow):
        def __init__(self, root):
            self.root = root
            self.root.title("Видалення книги")
            self.root.geometry("760x200")
            self.root.resizable(False, False)
            super().__init__(root)

            self.frame_main = ttk.Frame(self.root, width=740, height=150, relief='groove', borderwidth=2)
            self.frame_main.place(x=10, y=10)

            ttk.Label(self.frame_main, text="Видалити з:").place(x=10, y=10)
            targets = ['dictionary_library', 'dictionary_genre', 'login_password',
                       'dictionary_reader', 'dictionary_book', 'dictionary_author']
            self.combo_target = ttk.Combobox(self.frame_main, values=targets, state="readonly", width=27)
            self.combo_target.current(0)
            self.combo_target.place(x=120, y=10)

            ttk.Label(self.frame_main, text="Значення 1:").place(x=10, y=45)
            self.entry_val1 = ttk.Entry(self.frame_main, width=30)
            self.entry_val1.place(x=120, y=45)

            ttk.Label(self.frame_main, text="Значення 2:").place(x=10, y=80)
            self.entry_val2 = ttk.Entry(self.frame_main, width=30)
            self.entry_val2.place(x=120, y=80)
            ttk.Label(self.frame_main, text="(тільки для dictionary_genre: жанр + назва книги)", foreground='grey').place(x=380, y=80)

            ttk.Button(self.frame_main, text="Видалити", width=12, command=self.do_delete).place(x=120, y=115)
            ttk.Button(self.frame_main, text="Відміна",  width=10, command=self.root.destroy).place(x=280, y=115)

            self.frame_down = ttk.Frame(self.root, width=740, height=27, relief='groove', borderwidth=2)
            self.frame_down.place(x=10, y=168)
            self.label_role = ttk.Label(self.frame_down, text="Роль: Бібліотекар")
            self.label_role.place(x=610, y=0)

        def do_delete(self):
            target = self.combo_target.get()
            val1 = self.entry_val1.get().strip()
            val2 = self.entry_val2.get().strip()

            if target == 'dictionary_genre':
                msg = function_librarian_delete(target, val1, val2)
            else:
                msg = function_librarian_delete(target, val1)

            if "видалено" in msg:
                messagebox.showinfo("Готово", msg)
                self.root.destroy()
            else:
                messagebox.showerror("Помилка", msg)

    # ПРИМІТКА. Видача книги

    class Librarian_Issue(_BaseWindow):
        def __init__(self, root):
            self.root = root
            self.root.title("Видача книги")
            self.root.geometry("760x250")
            self.root.resizable(False, False)
            super().__init__(root)

            self.frame_main = ttk.Frame(self.root, width=740, height=220, relief='groove', borderwidth=2)
            self.frame_main.place(x=10, y=10)

            ttk.Label(self.frame_main, text="Назва книги:").place(x=10, y=10)
            self.entry_book = ttk.Entry(self.frame_main, width=30)
            self.entry_book.place(x=150, y=10)

            ttk.Label(self.frame_main, text="Читач (ПІБ через дефіс):").place(x=10, y=65)
            self.entry_reader = ttk.Entry(self.frame_main, width=30)
            self.entry_reader.place(x=200, y=65)

            ttk.Label(self.frame_main, text="Дата видачі (d.m.y):").place(x=10, y=110)
            self.entry_date = ttk.Entry(self.frame_main, width=30)
            self.entry_date.place(x=170, y=110)

            ttk.Button(self.frame_main, text="Видати",  width=12, command=self.do_issue).place(x=150, y=165)
            ttk.Button(self.frame_main, text="Відміна", width=10, command=self.root.destroy).place(x=300, y=165)

            self.frame_down = ttk.Frame(self.root, width=740, height=27, relief='groove', borderwidth=2)
            self.frame_down.place(x=10, y=218)
            self.label_role = ttk.Label(self.frame_down, text="Роль: Бібліотекар")
            self.label_role.place(x=610, y=0)

        def do_issue(self):
            msg = function_librarian_issue(
                self.entry_book.get().strip(),
                self.entry_reader.get().strip(),
                self.entry_date.get().strip()
            )
            if "видана" in msg:
                messagebox.showinfo("Готово", msg)
                self.root.destroy()
            else:
                messagebox.showerror("Помилка", msg)

    # ПРИМІТКА. Видані екземпляри

    class Librarian_Issued(_BaseWindow):
        def __init__(self, root):
            self.root = root
            self.root.title("Видані екземпляри")
            self.root.geometry("660x400")
            self.root.resizable(False, False)
            super().__init__(root)

            self.frame_tree = ttk.Frame(self.root, width=740, height=350, relief='groove', borderwidth=2)
            self.frame_tree.place(x=10, y=10)

            self.column = ('№', 'Назва книги', 'Читач', 'Дата видачі', 'Повернути до')
            self.tree = ttk.Treeview(self.frame_tree, columns=self.column, show='headings', height=16)
            self.tree.column('№', width=30,  anchor='center', stretch=False)
            self.tree.column('Назва книги', width=170, anchor='center', stretch=False)
            self.tree.column('Читач', width=170, anchor='center', stretch=False)
            self.tree.column('Дата видачі', width=120, anchor='center', stretch=False)
            self.tree.column('Повернути до', width=120, anchor='center', stretch=False)

            for col in self.column:
                self.tree.heading(col, text=col)

            self.scroll_y = ttk.Scrollbar(self.frame_tree, orient="vertical", command=self.tree.yview)
            self.tree.configure(yscrollcommand=self.scroll_y.set)
            self.scroll_y.pack(side='right', fill='y')
            self.tree.pack(side='left', fill='both', expand=True)

            self.frame_down = ttk.Frame(self.root, width=740, height=27, relief='groove', borderwidth=2)
            self.frame_down.place(x=8, y=368)
            self.label_role = ttk.Label(self.frame_down, text="Роль: Бібліотекар")
            self.label_role.place(x=500, y=0)

            self.load_tree()

        def load_tree(self):
            result = function_librarian_issued()
            if isinstance(result, list):
                for i, item in enumerate(result, 1):
                    self.tree.insert('', 'end', values=(i, *item))
            else:
                self.tree.insert('', 'end', values=(1, result, '', '', ''))

    # ПРИМІТКА. Головне меню читача

    class Reader:
        def __init__(self, root):
            self.root = root
            self.root.title("Головне меню читача")
            self.root.geometry("760x400")
            self.root.resizable(False, False)

            self.main_menu = tk.Menu(root)
            self.root.config(menu=self.main_menu)

            search_menu = tk.Menu(self.main_menu, tearoff=0)
            self.main_menu.add_cascade(label="Пошук", menu=search_menu)
            search_menu.add_command(label="Швидкий пошук", command=self.open_quick_search)
            search_menu.add_command(label="За автором", command=self.open_by_author)
            search_menu.add_command(label="За типом", command=self.open_by_type)
            search_menu.add_command(label="За індексом", command=self.open_by_index)
            search_menu.add_command(label="Аксесуари", command=self.open_accessories)

            return_menu = tk.Menu(self.main_menu, tearoff=0)
            self.main_menu.add_cascade(label="Книга", menu=return_menu)
            return_menu.add_command(label="Повернення / Продовження", command=self.open_return)

            self.frame_tree = ttk.Frame(self.root, width=730, height=340, relief='groove', borderwidth=2)
            self.frame_tree.place(x=14, y=10)
            self.column = ('№', 'Назва книги', 'Автор', 'Жанр', 'Індекс', 'За типом', 'Рік видання')
            self.tree = ttk.Treeview(self.frame_tree, columns=self.column, show='headings', height=15)
            self.tree.column('№', width=30, anchor='center', stretch=False)
            self.tree.column('Назва книги', width=180, anchor='center', stretch=False)
            self.tree.column('Автор', width=120, anchor='center', stretch=False)
            self.tree.column('Жанр', width=100, anchor='center', stretch=False)
            self.tree.column('Індекс', width=80, anchor='center', stretch=False)
            self.tree.column('За типом', width=80, anchor='center', stretch=False)
            self.tree.column('Рік видання', width=80, anchor='center', stretch=False)
            for col in self.column:
                self.tree.heading(col, text=col)
            self.scroll_y = ttk.Scrollbar(self.frame_tree, orient="vertical", command=self.tree.yview)
            self.tree.configure(yscrollcommand=self.scroll_y.set)
            self.scroll_y.pack(side='right', fill='y')
            self.tree.pack(side='left', fill='both', expand=True)

            self.frame_down = ttk.Frame(self.root, width=730, height=26, relief='groove', borderwidth=2)
            self.frame_down.place(x=14, y=368)
            ttk.Label(self.frame_down, text="Роль: Читач").place(x=620, y=0)

            json_connect_base()
            self.load_tree()

        def load_tree(self):
            for row in self.tree.get_children():
                self.tree.delete(row)
            i = 1
            for name, book in fn.data["dictionary_library"].items():
                for etype, editions in book["editions"].items():
                    if etype == "accessories":
                        continue
                    for yr, ed in editions.items():
                        self.tree.insert('', 'end', values=(
                            i, name, book.get('author', ''), book.get('genre', ''),
                            ed.get('index', ''), etype, yr
                        ))
                        i += 1

        # ПРИМІТКА. Швидкий пошук

        def open_quick_search(self):
            top = tk.Toplevel(self.root)
            top.title("Швидкий пошук")
            top.geometry("400x150")
            top.resizable(False, False)
            ttk.Label(top, text="Назва книги:").place(x=20, y=20)
            entry = ttk.Entry(top, width=30)
            entry.place(x=130, y=20)
            result_label = ttk.Label(top, text="", wraplength=360)
            result_label.place(x=20, y=100)
            def do_search():
                res = function_reader_quick_search(entry.get().strip())
                result_label.config(text=res)
            ttk.Button(top, text="Знайти", command=do_search).place(x=130, y=70)

        # ПРИМІТКА. Пошук за автором

        def open_by_author(self):
            top = tk.Toplevel(self.root)
            top.title("Пошук за автором")
            top.geometry("400x200")
            top.resizable(False, False)
            ttk.Label(top, text="Автор:").place(x=20, y=20)
            entry_author = ttk.Entry(top, width=30)
            entry_author.place(x=130, y=20)
            ttk.Label(top, text="Рік видання:").place(x=20, y=75)
            entry_year = ttk.Entry(top, width=30)
            entry_year.place(x=130, y=75)
            result_label = ttk.Label(top, text="", wraplength=360)
            result_label.place(x=20, y=130)
            def do_search():
                res = function_reader_by_genre(entry_author.get().strip(), entry_year.get().strip())
                result_label.config(text=str(res))
            ttk.Button(top, text="Знайти", command=do_search).place(x=130, y=105)

        # ПРИМІТКА. Пошук за типом

        def open_by_type(self):
            top = tk.Toplevel(self.root)
            top.title("Пошук за типом")
            top.geometry("400x220")
            top.resizable(False, False)
            ttk.Label(top, text="Тип:").place(x=20, y=20)
            combo_type = ttk.Combobox(top, values=["default", "action", "new", "hot"], state="readonly", width=27)
            combo_type.current(0)
            combo_type.place(x=130, y=20)
            ttk.Label(top, text="Назва книги:").place(x=20, y=55)
            entry_book = ttk.Entry(top, width=30)
            entry_book.place(x=130, y=55)
            ttk.Label(top, text="Рік видання:").place(x=20, y=110)
            entry_year = ttk.Entry(top, width=30)
            entry_year.place(x=130, y=110)
            result_label = ttk.Label(top, text="", wraplength=360)
            result_label.place(x=20, y=145)
            def do_search():
                res = function_reader_by_type(combo_type.get(), entry_book.get().strip(), entry_year.get().strip())
                result_label.config(text=str(res))
            ttk.Button(top, text="Знайти", command=do_search).place(x=130, y=148)

        # ПРИМІТКА. Пошук за індексом

        def open_by_index(self):
            top = tk.Toplevel(self.root)
            top.title("Пошук за індексом")
            top.geometry("400x150")
            top.resizable(False, False)
            ttk.Label(top, text="Індекс:").place(x=20, y=30)
            entry = ttk.Entry(top, width=30)
            entry.place(x=130, y=30)
            result_label = ttk.Label(top, text="", wraplength=360)
            result_label.place(x=20, y=80)
            def do_search():
                res = function_reader_by_index(entry.get().strip())
                result_label.config(text=str(res))
            ttk.Button(top, text="Знайти", command=do_search).place(x=130, y=60)

        # ПРИМІТКА. Аксесуари

        def open_accessories(self):
            top = tk.Toplevel(self.root)
            top.title("Аксесуари")
            top.geometry("400x150")
            top.resizable(False, False)
            ttk.Label(top, text="Аксесуар:").place(x=20, y=30)
            entry = ttk.Entry(top, width=30)
            entry.place(x=130, y=30)
            result_label = ttk.Label(top, text="", wraplength=360)
            result_label.place(x=20, y=80)
            def do_search():
                res = function_reader_accessories(entry.get().strip())
                result_label.config(text=str(res))
            ttk.Button(top, text="Знайти", command=do_search).place(x=130, y=50)

        # ПРИМІТКА. Повернення книги

        def open_return(self):
            top = tk.Toplevel(self.root)
            top.title("Повернення книги")
            top.geometry("400x150")
            top.resizable(False, False)
            result_label = ttk.Label(top, text="", wraplength=360)
            result_label.place(x=20, y=70)
            def do_return():
                res = function_reader_return(False)
                result_label.config(text=str(res))
            def do_extend():
                res = function_reader_return(True)
                result_label.config(text=str(res))
            ttk.Button(top, text="Повернути", width=14, command=do_return).place(x=50, y=45)
            ttk.Button(top, text="Продовжити (+3 міс)", width=18, command=do_extend).place(x=200, y=45)

# Створення функції запуску
def start():
    root = tb.Window(themename="flatly")
    root.iconbitmap("book.ico")
    app = App.Exit(root)
    root.mainloop()

# Захист від випадкового імпорту і виклик 
if __name__ == '__main__':
    start()
