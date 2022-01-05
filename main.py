import tkinter as tk
from tkinter import ttk
import sqlite3


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):

        toolbar = tk.Frame(bg="#d7d8e0", bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        self.add_img = tk.PhotoImage(file="add.png")

        btn_open_dialog = tk.Button(
            toolbar,
            text="Добавить данные",
            command=self.open_dialog,
            bg="#d7d8e0",
            bd=2,
            compound=tk.TOP,
            image=self.add_img,
        )

        btn_open_dialog.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(
            self,
            columns=(
                "ID",
                "Description",
                "Type",
                "Activity",
                "Link",
                "Author",
                "Comments",
            ),
            height=15,
            show="headings",
        )

        self.tree.column("ID", width=70, anchor=tk.CENTER)
        self.tree.column("Description", width=300, anchor=tk.CENTER)
        self.tree.column("Type", width=270, anchor=tk.CENTER)
        self.tree.column("Activity", width=180, anchor=tk.CENTER)
        self.tree.column("Link", width=120, anchor=tk.CENTER)
        self.tree.column("Author", width=500, anchor=tk.CENTER)
        self.tree.column("Comments", width=250, anchor=tk.CENTER)

        self.tree.heading("ID", text="ID записи")
        self.tree.heading(
            "Description",
            text="Описание контента с признаками деструктивности",
        )
        self.tree.heading(
            "Type", text="Тип контента с признаками деструктивности"
        )
        self.tree.heading("Activity", text="Количество переходов к посту")
        self.tree.heading("Link", text="Ссылка на контент")
        self.tree.heading(
            "Author",
            text="Автор поста (для ресурсов с обязательной регистрацией для размещения постов)",
        )

        self.tree.heading(
            "Comments", text="Количество комментариев под постом"
        )

        self.tree.pack()

    def record(self, description, type, activity, link, author, comments):
        self.db.insert_data(
            description, type, activity, link, author, comments
        )
        self.view_records()

    def view_records(self):
        self.db.curs.execute("""SELECT * FROM destructive_content""")
        [self.tree.delete(i) for i in self.tree.get_children()]
        [
            self.tree.insert("", "end", values=row)
            for row in self.db.curs.fetchall()
        ]

    def open_dialog(self):
        Child_add()


class Child_add(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title("Добавить данные о контенте")
        self.geometry("800x400+400+300")
        self.resizable(True, True)
        ########################################################

        label_description = tk.Label(self, text="Наименование")
        label_description.place(x=120, y=110)

        label_type = tk.Label(self, text="Тип")
        label_type.place(x=120, y=140)

        label_activity = tk.Label(self, text="Количество переходов к посту")
        label_activity.place(x=120, y=170)

        label_link = tk.Label(self, text="Ссылка")
        label_link.place(x=120, y=200)

        label_author = tk.Label(self, text="Автор")
        label_author.place(x=120, y=230)

        label_type = tk.Label(self, text="Количество комментариев")
        label_type.place(x=120, y=260)
        ########################################################

        self.entry_description = ttk.Entry(self)
        self.entry_description.place(x=300, y=110)

        self.entry_type = self.combobox = ttk.Combobox(
            self,
            values=[u"Видео", u"Картинка", u"Текстовый пост", u"Ссылка"],
        )
        self.combobox.current(0)
        self.combobox.place(x=300, y=140)

        self.entry_activity = ttk.Entry(self)
        self.entry_activity.place(x=300, y=170)

        self.entry_link = ttk.Entry(self)
        self.entry_link.place(x=300, y=200)

        self.entry_author = ttk.Entry(self)
        self.entry_author.place(x=300, y=230)

        self.entry_comments = ttk.Entry(self)
        self.entry_comments.place(x=300, y=260)

        ###############################################################

        btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        btn_cancel.place(x=720, y=370)

        btn_ok = ttk.Button(self, text="Добавить")
        btn_ok.place(x=720, y=10)

        btn_ok.bind(
            "<Button-1>",
            lambda event: self.view.record(
                self.entry_description.get(),
                self.entry_type.get(),
                self.entry_activity.get(),
                self.entry_link.get(),
                self.entry_author.get(),
                self.entry_comments.get(),
            ),
        )

        self.grab_set()
        self.focus_set()


class DB:
    def __init__(self):
        self.conn = sqlite3.connect("destructive_content.db")
        self.curs = self.conn.cursor()
        self.curs.execute(
            """CREATE TABLE IF NOT EXISTS destructive_content 
           (id integer primary key, 
           description text, 
           type text, 
           activity integer, 
           link text, 
           author text, 
           comments integer)"""
        )
        self.conn.commit()

    def insert_data(self, description, type, activity, link, author, comments):
        self.curs.execute(
            """ INSERT INTO destructive_content (description, 
           type, 
           activity, 
           link, 
           author, 
           comments)
           
           VALUES(?, ?, ?, ?, ?, ?)""",
            (description, type, activity, link, author, comments),
        )

        self.conn.commit()


if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()

    root.title("База данных о контентах с признаками деструктивности")
    root.geometry("1900x600+0+200")
    root.resizable(False, False)
    root.mainloop()
