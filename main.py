import tkinter as tk
import sqlite3
from tkinter import ttk

# класс главного окна
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):

        # верхняя панель программы
        toolbar = tk.Frame(bg='#d7d7d7', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_image = tk.PhotoImage(file='./image/add.png')

        btn_open_dialog = tk.Button(toolbar, bg='#d7d7d7', bd=0, image=self.add_image, command=self.open_dialog)
        btn_open_dialog.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file='./image/delete.png')
        btn_delete = tk.Button(toolbar, bg='#d7d7d7', bd=0, image=self.delete_img, command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        # кнопка поиска
        self.search_img = tk.PhotoImage(file='./image/search.png')
        btn_search = tk.Button(toolbar, bg='#d7d7d7', bd=0, image=self.search_img, command=self.open_search_dialog)
        btn_search.pack(side=tk.RIGHT, padx=14)

    
        # создание Treeview (таблицы контактов)
        self.tree = ttk.Treeview(self,
                                 columns=['ID', 'name', 'phone', 'email', 'salary'],
                                 height=45,
                                 show='headings')

        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('name', width=300, anchor=tk.CENTER)
        self.tree.column('phone', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)
        self.tree.column('salary', width=150, anchor=tk.CENTER)

        # подпси колонок 
        self.tree.heading('ID', text='id')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('phone', text='Телефон')
        self.tree.heading('email', text='E-mail')
        self.tree.heading('salary', text='Зарплата')

        # упаковка
        self.tree.pack(side=tk.LEFT)
        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

        # редактирование
        self.update_img = tk.PhotoImage(file='./image/update.png')
        btn_edit_dialog = tk.Button(toolbar, bg='#d7d7d7', bd=0, image=self.update_img, command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        self.refresh_img = tk.PhotoImage(file='./image/refresh.png')
        btn_refresh = tk.Button(toolbar, bg='#d7d7d7', bd=0, 
                                image=self.refresh_img, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

    # метод для вызова записи новых данных в бд
    def records(self, name, phone, email, salary):
        self.db.insert_data(name, phone, email, salary)
        self.view_records()

    def update_record(self, name, phone, email, salary):
        self.db.c.execute('''UPDATE users SET name=?, phone=?, email=?, salary WHERE ID=?''',
                          (name, phone, email, salary, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    # метод отображения данных
    def view_records(self):
        self.db.c.execute('''SELECT * FROM users''')
        r = self.db.c.fetchall()
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=i) for i in r]

    # метод вызова дочернего окна
    def open_dialog(self):
        Child()

    def open_update_dialog(self):
        Update()
    
    def open_search_dialog(self):
        Search()
    
    def update_record(self, name, phone, email, salary):
        self.db.c.execute('''UPDATE users SET name = ?, phone = ?, email = ?, salary = ?
        WHERE ID = ?''', (name, phone, email, salary,
        self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()    

    # удаление
    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM users WHERE id = ?''',
            (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_records()

    # поиск записи
    def search_records(self, name):
        name = ('%' + name + '%',)
        self.db.c.execute('''SELECT * FROM users WHERE name LIKE ?''', name)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row)
        for row in self.db.c.fetchall()]


# класс дочерних окон
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добавление сотрудника')
        self.geometry('370x215+680+350')
        self.resizable(False, False)

        # перехват всех событий
        self.grab_set()

        # захват фокуса
        self.focus_set()

        label_name = tk.Label(self, text='ФИО:')
        label_name.place(x=50, y=30)
        label_phone = tk.Label(self, text='Телефон:')
        label_phone.place(x=50, y=60)
        label_email = tk.Label(self, text='E-mail:')
        label_email.place(x=50, y=90)
        label_salary = tk.Label(self, text='Зарплата:')
        label_salary.place(x=50, y=120)
        
        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=160, y=30)
        self.entry_phone = tk.Entry(self)
        self.entry_phone.place(x=160, y=60)
        self.entry_email = tk.Entry(self)
        self.entry_email.place(x=160, y=90)
        self.entry_salary = tk.Entry(self)
        self.entry_salary.place(x=160, y=120)

        self.btn_cancel = tk.Button(self, text='Закрыть', command=self.destroy, bg='red', fg='white', font=('Arial', 10, 'bold'))
        # self.btn_cancel.place(x=148, y=180, height=30)
        # self.btn_cancel.place(x=215, y=180, height=30)
        self.btn_cancel.place(x=1, y=189, height=25)
        self.btn_ok = tk.Button(self, text='Добавить', bg='green', fg='white', font=('Arial', 10, 'bold'))
        self.btn_ok.bind('<Button-1>', lambda ev: self.view.records(self.entry_name.get(), self.entry_phone.get(), self.entry_email.get(), self.entry_salary.get()))
        # self.btn_ok.place(x=233, y=180, height=30)
        self.btn_ok.place(x=160, y=150, height=25, width=125)


class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        self.title('Редактировать позицию')
        self.btn_edit = ttk.Button(self, text='Редактировать')
        self.btn_edit.configure(style='r.TButton')
        self.style = ttk.Style()
        self.style.configure('r.TButton', background='blue', foreground='blue', font=('Arial', 10, 'bold'))
        self.btn_edit.place(x=160, y=150, height=25, width=125)
        self.btn_edit.bind('<Button-1>', lambda event:
                      self.view.update_record(self.entry_name.get(),
                                              self.entry_phone.get(),
                                              self.entry_email.get(),
                                              self.entry_salary.get()))
        self.btn_edit.bind('<Button-1>', lambda event:
                      self.destroy(), add = '+')
        self.btn_ok.destroy()
    
    def default_data(self):
        self.db.c.execute('''SELECT * FROM users WHERE id=?''',
        (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        row = self.db.c.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_phone.insert(0, row[2])
        self.entry_email.insert(0, row[3])
        self.entry_salary.insert(0, row[4])

class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app
    
    def init_search(self):
        self.title('Поиск')
        self.geometry('300x100+800+400')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Введите ФИО')
        label_search.place(x=20, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=104, y=50, width=72)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=184, y=50, width=72)
        
        btn_search.bind('<Button-1>', lambda event:
                        self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event:
                        self.destroy(), add = '+')

# класс БД
class Db:
    def __init__(self):
        self.conn = sqlite3.connect('contacts.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY,
                                name TEXT,
                                phone TEXT,
                                email TEXT,
                                salary INT)''')
        self.conn.commit()

    # добавление в бд
    def insert_data(self, name, phone, email, salary):
        self.c.execute('''INSERT INTO users (name, phone, email, salary)
                        VALUES (?, ?, ?, ?)''', (name, phone, email, salary))
        self.conn.commit()

if __name__ == '__main__':
    root = tk.Tk()
    db = Db()
    app = Main(root)
    app.pack()
    root.title('Cписок сотрудников')
    root.geometry('800x450+600+200')
    root.resizable(False, False)
    root.mainloop()
