"""
Readme.md
---------
If you are interested in this project and want to make one like this then follow this script.

For this project, you need to download database like `mysql`, `sqlite`, etc... for storing the data into the database.

And also a `GUI(Graphical User Interface)` for display the app and to use it easily, Recommanded `tkinter` because its in-built in Python.


Required modules*
>>> import mysql.connector as sql #database

The below line imports all classes and methods which makes the program slower and not recommonded 
>>> from tkinter import * # All GUI's

The below line imports classes and methods which are required and makes the program faster and recommonded
>>> from tkinter import Label, Frame, Button, Entry, Tk, StringVar, Scrollbar, OptionMenu, END

The below lines of code(imports) are optional because you can use different methods to display messeges
>>> from tkinter import ttk 
>>> from tkinter import simpledialog as sd
>>> from tkinter import messagebox as mb

Optional modules*
>>> from env import MysqlData # This module is created customly 
>>> import csv

This App contains important commands like:-
1. `Add Record`
2. `Delete Record`
3. `Update Record`
4. `Change Status` (Optional)
5. `Download Data` (Optional)

You can also modify any command or change interface as you like
Visit : https://adcode14.vercel.app/project for more projects
"""

import mysql.connector as sql #database
# from tkinter import *
from tkinter import Label, Frame, Button, Entry, Tk, StringVar, Scrollbar, OptionMenu, END
from tkinter import ttk 
from tkinter import simpledialog as sd
from tkinter import messagebox as mb
from env import MysqlData
import csv

MD = MysqlData()
database = sql.connect(host=MD.HOST,user=MD.USER,password=MD.PASSWORD,database=MD.DATABASE)
cursor = database.cursor()

table = "create table if not exists library_management (book_id varchar(20) primary key not null , book_name varchar(250), book_author varchar(250), book_price varchar(20), book_status varchar(200), user_id varchar(20) DEFAULT NULL, user_name varchar(250));"

cursor.execute(table)
database.commit()

# default variables
backgroundtheme = "#252525"
globalfont = "Courier"
title = "Library Management System"
left_frame_font_color = "cyan"
left_frame_bg_color = "#303030"
delete_font_color = "red"
dark_color = "black"
download_font_color = "cyan"

win = Tk()

# aspect screen ratio => 16:9 (width:height)
height = 720
width = 1280

win.title(title)
win.minsize(width=width, height=height)
win.config(background=backgroundtheme)
Label(win, text=title, font=(globalfont, 18, "bold"), bg = dark_color, fg = "#00ff00").pack(side="top", fill="x")


# functions
def display_records():
    global database, cursor, tree
    tree.delete(*tree.get_children())
    query = "select * from library_management;"
    cursor.execute(query)
    data : list = cursor.fetchall()
    for row in data:
        tree.insert('', END, values=row)


def clear_fields():
    global book_id,book_name,book_author,book_price,book_status,user_id,user_name

    book_status.set('Available')
    for i in ["book_id","book_name","book_author","book_price","user_id","user_name"]:
        exec(f"{i}.set('')")

    try:
        tree.selection_remove(tree.selection()[0])
    except:
        pass

def clear_and_display():
    clear_fields()
    display_records()
    toggle_option("Available")


def user_card():
    ask_id = sd.askstring('User ID', 'What is the User Card ID?',)
    if not ask_id:
        mb.showerror('User ID cannot be empty!', 'Can\'t keep User ID empty, it must have a value!')
    else:
        ask_name = sd.askstring('User Name', 'What is the Username?')
        if not ask_name:
            mb.showerror('User Name cannot be empty!', 'Can\'t keep User Name empty, it must have a value!')
        else:
            return [ask_id, ask_name]
    


def toggle_option(value):
    global book_userid_entry, book_username_entry, user_id, user_name
    if value=="Available":
        book_userid_entry.config(state="disabled",disabledbackground="#AAAAAA", cursor="x_cursor ")
        book_username_entry.config(state="disabled", disabledbackground="#AAAAAA", cursor="x_cursor ")

        user_name.set("")
        user_id.set("")
    else:
        book_userid_entry.config(state="normal", cursor="xterm")
        book_username_entry.config(state="normal", cursor="xterm")

def is_fields_filled(which_type: bool) -> bool:
    global book_id_entry, book_name_entry, book_author_entry, book_price_entry, book_userid_entry, book_username_entry

    if which_type:
        items = [book_id_entry.get(), book_name_entry.get(), book_author_entry.get(), book_price_entry.get(), book_userid_entry.get(), book_username_entry.get()]
        for item in items:
            if item.isspace() or item.strip() == "":
                mb.showwarning("Field Warning!","Fill the required fields!")
                return False
        return True
    else:
        items = [book_id_entry.get(), book_name_entry.get(), book_author_entry.get(), book_price_entry.get()]
        for item in items:
            if item.isspace() or item.strip() == "":
                mb.showwarning("Field Warning!","Fill the required fields!")
                return False
        return True

def add_data():
    global database, cursor
    global book_id, book_author, book_name, book_price, book_status, user_id, user_name
    global book_userid_entry , book_username_entry

    flag = False
    if book_status.get() == "Issued":
        user_id.set(book_userid_entry.get())
        user_name.set(book_username_entry.get())
        flag = is_fields_filled(True)
    else:
        user_id.set("")
        user_name.set("")
        flag = is_fields_filled(False)
    
    if flag:
        try:
            insertquery = 'insert into library_management values ("%s","%s","%s","%s","%s","%s","%s");' % (book_id.get(), book_name.get(), book_author.get(), book_price.get(), book_status.get(), user_id.get(), user_name.get())
            cursor.execute(insertquery)
            database.commit()
            clear_and_display()
        except (sql.errors.IntegrityError, sql.errors.ProgrammingError):
            mb.showwarning("Duplicate Book ID's", "Please give unique Book ID")
    
    
def delete_all_records():
    global tree, cursor, database
    if mb.askyesno('Are you sure?', 'Are you sure you want to delete the entire data?\n\nThis command cannot be reversed'):
        tree.delete(*tree.get_children())
        cursor.execute("delete from library_management;")
        database.commit()
        clear_and_display()
    else:
        return

def delete_record():
    global tree, database, cursor

    if not tree.selection():
        mb.showwarning('Not-Selection Warning!', 'Please select an item from the Records')
        return

    current_item = tree.focus()
    values = tree.item(current_item)
    selection = values["values"]

    if mb.askyesno('Are you sure!', f'Are you sure you want to delete this data\n\nBook ID is {selection[0]}'):

        delete_item = 'delete from library_management where book_id = %s' % (selection[0])

        cursor.execute(delete_item)
        database.commit()
        clear_and_display()

def change_status():
    global cursor, database, tree, book_id

    if not tree.selection():
        mb.showwarning('Not-Selection Warning!', 'Please select an item from the Records')
        return
    
    current_item = tree.focus()
    values = tree.item(current_item)
    temp_book_id = values["values"][0]
    temp_book_status = values["values"][4]

    if temp_book_status == "Issued":
        query = 'update library_management set book_status = "%s", user_id = "%s", user_name = "%s" where book_id = "%s";' % ("Available", "", "", temp_book_id)
        cursor.execute(query)
        database.commit()

    else:
        data = user_card()
        if data:
            uid = data[0]
            uname = data[1]
            query = 'update library_management set book_status = "%s", user_id = "%s", user_name = "%s" where book_id = "%s";' % ("Issued", uid, uname, temp_book_id)
            cursor.execute(query)
            database.commit()
    
    clear_and_display()

def view_record():
    global book_id, book_name, book_author, book_price, book_status, user_id, user_name
    global tree, database, cursor

    current_item = tree.focus()
    values = tree.item(current_item)
    selected_item = values["values"]

    book_id.set(selected_item[0])
    book_name.set(selected_item[1])
    book_author.set(selected_item[2])
    book_price.set(selected_item[3])
    book_status.set(selected_item[4])
    user_id.set(selected_item[5])
    user_name.set(selected_item[6])

    toggle_option(selected_item[4])

def update_record():
    def update():
        global book_id, book_name, book_author, book_price, book_status, user_id, user_name, book_userid_entry,book_username_entry
        global tree, database, cursor
        if book_status.get() == "Issued":
            data = user_card()
            if data:
                user_id.set(data[0])
                user_name.set(data[1])
        else:
            user_id.set("")
            user_name.set("")

        query = 'update library_management set book_name = "%s", book_author = "%s", book_price= "%s", book_status = "%s", user_id = "%s", user_name = "%s" where book_id = "%s";' % (book_name.get(), book_author.get(), book_price.get(), book_status.get(), user_id.get(), user_name.get(), book_id.get())
        cursor.execute(query)
        database.commit()
        edit_btn.destroy()
        clear_and_display()
    
    global tree

    edit_btn = Button(left_frame, text="Update Record", font=(globalfont, "16", "bold"), command=update, cursor="hand2", bg=dark_color, fg="white" )
    
    if tree.focus():
        view_record()
        edit_btn.grid(row=8, columnspan=2, pady=20)
    else:
        mb.showwarning('Select a row!', 'To view a record, you must select it in the table. Please do so before continuing.')
        return

def download_database_as_csv():
    global cursor
    query = "select * from library_management;"
    cursor.execute(query)
    datas : list = cursor.fetchall()

    # using try-except statement will help us to run the program smoothly without getting any error while runtime
    try:
        with open("download.csv", "w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerows(datas)

        mb.showinfo("Download successful", "Successfully downloaded the Data from Database!")

    except (EOFError, Exception, NameError, FileExistsError, RuntimeError):
        mb.showinfo("Cannot download", "The database give error to write data to your CSV file!\n\nTry again later.")
    

# input strings
book_id = StringVar()
book_name = StringVar()
book_author = StringVar()
book_price = StringVar()
book_status = StringVar()
user_id = StringVar()
user_name = StringVar()

# frames
left_frame = Frame(win, background=left_frame_bg_color, relief="sunken" ,width= width//3, borderwidth= 2)
left_frame.pack(side="left", fill="both", )

right_frame = Frame(win, background=backgroundtheme, relief="sunken" ,borderwidth= 2)
right_frame.pack(side="right", fill="both", expand=True)

right_top_frame = Frame(right_frame )
right_top_frame.pack(side="top",fill="both", expand=1)

right_bottom_frame = Frame(right_frame,background=backgroundtheme , height=height//5)
right_bottom_frame.pack(side="bottom", fill="both", expand=1)

# In left frame
Label(left_frame, text="Book ID", background=left_frame_bg_color,font=(globalfont, 14, "bold"), fg=left_frame_font_color).grid(row=0, column=0, padx=(20,0), pady=20)
book_id_entry = Entry(left_frame, textvariable=book_id,font=(globalfont, 14), width=20)
book_id_entry.grid(row=0, column=1, padx=(0,20) ,pady=20)

Label(left_frame, text="Book Name", background=left_frame_bg_color,font=(globalfont, 14, "bold"), fg=left_frame_font_color).grid(row=1, column=0,padx=(20,0), pady=20)
book_name_entry = Entry(left_frame, textvariable=book_name,font=(globalfont, 14), width=20)
book_name_entry.grid(row=1, column=1,padx=(0,20), pady=20)

Label(left_frame, text="Author", background=left_frame_bg_color,font=(globalfont, 14, "bold"), fg=left_frame_font_color).grid(row=2, column=0, padx=(20,0),pady=20)
book_author_entry = Entry(left_frame, textvariable=book_author,font=(globalfont, 14), width=20)
book_author_entry.grid(row=2, column=1,padx=(0,20),pady=20)

Label(left_frame, text="Book Price", background=left_frame_bg_color,font=(globalfont, 14, "bold"), fg=left_frame_font_color).grid(row=3, column=0, padx=(20,0),pady=20)
book_price_entry = Entry(left_frame, textvariable=book_price,font=(globalfont, 14), width=20)
book_price_entry.grid(row=3, column=1,padx=(0,20), pady=20)

Label(left_frame, text="Book Status", background=left_frame_bg_color,font=(globalfont, 14, "bold"), fg=left_frame_font_color).grid(row=4, column=0,padx=(20,0), pady=20)
book_status_entry = OptionMenu(left_frame, book_status, *['Available', 'Issued'], command=toggle_option)
book_status_entry.config(font=("sanrif", 12, "bold"), width=20, cursor="hand2")
book_status_entry.grid(row=4, column=1,padx=(0,20), pady=20)


Label(left_frame, text="User ID", background=left_frame_bg_color,font=(globalfont, 14, "bold"), fg=left_frame_font_color).grid(row=5, column=0, padx=(20,0),pady=20)
book_userid_entry = Entry(left_frame, textvariable=user_id,font=(globalfont, 14), width=20)
book_userid_entry.grid(row=5, column=1,padx=(0,20), pady=20)

Label(left_frame, text="User Name", background=left_frame_bg_color,font=(globalfont, 14, "bold"), fg=left_frame_font_color).grid(row=6, column=0, padx=(20,0),pady=20)
book_username_entry = Entry(left_frame, textvariable=user_name,font=(globalfont, 14), width=20)
book_username_entry.grid(row=6, column=1,padx=(0,20), pady=20)

submit_btn = Button(left_frame, text="Add New Record",bg=dark_color, fg="white", font=(globalfont, 16, "bold"), width=20, cursor="hand2", relief="raised", command=add_data)
submit_btn.grid(row=7, columnspan=2, pady=20)


# In right frame:-

# In right frame -> top
columns = ("Book ID", "Book Name", "Author","Book Price", "Book Status" , "User ID", "User Name")
tree = ttk.Treeview(right_top_frame, selectmode="browse", columns=columns, show="headings")

XScrollbar = Scrollbar(tree, orient="horizontal", command=tree.xview)
YScrollbar = Scrollbar(tree, orient="vertical", command=tree.yview)
XScrollbar.pack(side="bottom", fill="x")
YScrollbar.pack(side="right", fill="y")
tree.config(xscrollcommand=XScrollbar.set, yscrollcommand=YScrollbar.set)

tree.heading("Book ID", text="Book ID".upper(), anchor="w")
tree.heading("Book Name", text="Book Name".upper(), anchor="w")
tree.heading("Author", text="Author".upper(), anchor="w")
tree.heading("Book Price", text="Book Price".upper(), anchor="w")
tree.heading("Book Status", text="Book Status".upper(), anchor="w")
tree.heading("User ID", text="User ID".upper(), anchor="w")
tree.heading("User Name", text="User Name".upper(), anchor="w")

tree.pack(fill="both", expand=True)


# In right frame -> bottom
clear_fields_btn = Button(right_bottom_frame, text="Clear Fields", font=(globalfont, "16", "bold"), command=clear_fields, cursor="hand2")
clear_fields_btn.grid(row=0, column=0, padx=10, pady=20,)


change_status_btn = Button(right_bottom_frame, text="Change Status", font=(globalfont, "16", "bold"), cursor="hand2", command=change_status)
change_status_btn.grid(row=0, column=1, padx=10, pady=20)

update_btn = Button(right_bottom_frame, text="Update", font=(globalfont, 16, "bold"), cursor="hand2", command=update_record)
update_btn.grid(row=0, column=2, padx=20, pady=10)

delete_record_btn = Button(right_bottom_frame, text="Delete", font=(globalfont, "16", "bold"), cursor="hand2", command=delete_record, fg= delete_font_color, bg=dark_color) 
delete_record_btn.grid(row=0, column=3, padx=10, pady=20)

delete_records = Button(right_bottom_frame, text="Delete All records", font=(globalfont, "16", "bold"), cursor="hand2", command=delete_all_records, fg= delete_font_color, bg=dark_color )
delete_records.grid(row=0, column=4, padx=10, pady=20)

download_records = Button(right_bottom_frame, text="Download records", font=(globalfont, "16", "bold"), cursor="hand2", command=download_database_as_csv , fg= download_font_color, bg=dark_color)
download_records.grid(row=0, column=5, padx=10, pady=20)

# mandatory lines
clear_and_display()
win.update()
win.mainloop()