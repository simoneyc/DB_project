import tkinter as tk
from tkinter import ttk
import mysql.connector
import pandas as pd
from tabulate import tabulate
from tkcalendar import Calendar, DateEntry
from datetime import date, datetime


movie_list = []

# Connect DB
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="4110056030",
    database="movie"
)

# cursor object
cursor = db.cursor()

# select 功能
def get_selected_data():
    selected_option_1 = option_var_1.get()
    selected_option_2 = option_var_2.get()

    # query
    query = f"SELECT * FROM {selected_option_2} WHERE title = \"{selected_option_1}\";"
    cursor.execute(query)
    data = cursor.fetchall()

    for i in range(len(data)):
        print(data[i])

    # Display data
    display_text.delete(1.0, tk.END)  # Clear previous content

    if selected_option_2 == 'movieinfo':
        headers = ["title", "genre","duration","releasetime"]
    if selected_option_2 == 'boxoffice':
        headers = ["title", "budget", "box_office"]
    if selected_option_2 == 'award':
        headers = ["title", "oscar", "total"]
    if selected_option_2 == 'crew':
        headers = ["title", "director", "writer","producer"]
    if selected_option_2 == 'cast':
        headers = ["name", "gender", "birthdate","height","title"]

    if selected_option_2 == "cast":
        data_list = [list(row[:-1]) for row in data]
    else:
        data_list = [list(row) for row in data]

    
    table = tabulate(data_list, headers)
    display_text.insert(tk.END, f"{table}\n")

# delete 功能
def get_delete_data():
    delete_option_1 = del_op_var_1.get()
    delete_option_2 = del_op_var_2.get()

    # query
    query = f"DELETE FROM {delete_option_2} WHERE title = \"{delete_option_1}\";"
    cursor.execute(query)
    db.commit()

    # Display data
    display_text.delete(1.0, tk.END)  # Clear previous content
    display_text.insert(tk.END, f"deletion title = {delete_option_1} from {delete_option_2} complete!\n")

# insert 創造 query (暫不insert)
query_list = [] # 儲存還沒按下insert的所有query
def insert_tool(t_name, col_list, value_str):
    global query_list
    sql_DB = """INSERT INTO `%s` (%s) VALUES %s"""
    # column name
    ins_col_str = "%s" % ", ".join(col_list)

    # sql
    sql_DB = sql_DB % (t_name, ins_col_str, value_str)
    query_list.append(sql_DB)

    # 結果視窗提示
    display_text.delete(1.0, tk.END)  # Clear previous content
    display_text.insert(tk.END, f"Input {value_str} to {t_name} Ready!\n")

# 按下"新增"才用
def insert_confirm():
    
    cursor = db.cursor()

    for q in query_list:
        cursor.execute(q)
        db.commit()

    cursor.close()
    # Display data
    display_text.delete(1.0, tk.END)  # Clear previous content
    display_text.insert(tk.END, f"insertion complete!\n")

# 日期global (movieinfo-releasetime)
releasetime_entry = ''

# 以下5個show_****_table大致長一樣
def show_movieinfo_input():
    # 創建新視窗
    movieinfo_window = tk.Toplevel(window)
    movieinfo_window.title("Movie Information Input")

    def example1():
        def print_sel():
            global releasetime_entry

            # 轉換日期格式
            input_date_str = cal.selection_get()
            input_date = datetime.datetime.strptime(str(input_date_str), "%Y-%m-%d")
            releasetime_entry = input_date.strftime("%d-%b-%y")
            
            # 按下確認 顯示在旁邊
            input_label_5 = tk.Label(movieinfo_window, text=releasetime_entry)
            input_label_5.grid(row=3, column=2, padx=10, pady=10)

            print(cal.selection_get())
            cal.see(datetime.date(year=2016, month=2, day=5))

            # 關閉子視窗
            top.destroy()

        # 選日期的視窗
        top = tk.Toplevel(movieinfo_window)

        import datetime
        today = datetime.date.today()

        mindate = datetime.date(year=1700, month=1, day=21)
        maxdate = today 

        cal = Calendar(top, font="Arial 14", selectmode='day', locale='en_US',
                    mindate=mindate, maxdate=maxdate, disabledforeground='red',
                    cursor="hand1", year=2000, month=1, day=1)
        cal.grid()
        botton = ttk.Button(top, text="確認", command=print_sel)
        botton.grid()

    # 創建四個輸入框
    input_label_1 = tk.Label(movieinfo_window, text="Title:")
    input_label_1.grid(row=0, column=0, padx=10, pady=10)
    entry_1 = tk.Label(movieinfo_window, textvariable=movie_name)
    entry_1.grid(row=0, column=1, padx=10, pady=10)

    # 下拉式選單
    input_label_2 = tk.Label(movieinfo_window, text="Genre:")
    input_label_2.grid(row=1, column=0, padx=10, pady=10)
    genre_list = ["drama","crime","action","biography","adventure","comedy","animation","horror","western","mystery","film-noir","other"]
    genre_op_var_1 = tk.StringVar(movieinfo_window)
    genre_op_var_1.set(genre_list[0])  # default選項
    entry_2 = ttk.Combobox(movieinfo_window, textvariable=genre_op_var_1, values=genre_list,font=("Arial",8))
    entry_2.grid(row=1, column=1, padx=10, pady=10)

    # 時長(長這樣: 2h 2m)
    input_label_3 = tk.Label(movieinfo_window, text="Duration:")
    input_label_3.grid(row=2, column=0, padx=10, pady=10)
    #
    hour_list = ["0","1","2","3","4","5","6","7","8","9","10"]
    hour_op_var_1 = tk.StringVar(movieinfo_window)
    hour_op_var_1.set(hour_list[0])  # default選項
    entry_3 = ttk.Combobox(movieinfo_window, textvariable=hour_op_var_1, values=hour_list,font=("Arial",8))
    entry_3.grid(row=2, column=1, padx=5, pady=5)
    h_label = tk.Label(movieinfo_window, text="h")
    h_label.grid(row=2, column=2, padx=5, pady=5)
    #
    min_list = [str(i) for i in range(60)]
    min_op_var_1 = tk.StringVar(movieinfo_window)
    min_op_var_1.set(min_list[0])  # default選項
    entry_5 = ttk.Combobox(movieinfo_window, textvariable=min_op_var_1, values=min_list,font=("Arial",8))
    entry_5.grid(row=2, column=3, padx=5, pady=5)
    m_label = tk.Label(movieinfo_window, text="m")
    m_label.grid(row=2, column=4, padx=5, pady=5)

    # 選日期calendar
    input_label_4 = tk.Label(movieinfo_window, text="Releasetime:")
    input_label_4.grid(row=3, column=0, padx=10, pady=10)
    entry_4 = ttk.Button(movieinfo_window, text='點我', command=example1)
    entry_4.grid(row=3, column=1, padx=10, pady=10)

    col_list = ['title','genre','duration','releasetime']
    def get_movieinfo_input():
        global movie_name
        title = movie_name.get()

        
        genre = entry_2.get()
        duration_1 = entry_3.get()
        duration_2 = entry_5.get()
        releasetime = releasetime_entry

        value_str = f"('{title}','{genre}','{duration_1}h {duration_2}m','{releasetime}')"
        insert_tool("movieinfo",col_list,value_str)

        # print
        print("Title:", title)
        print("Genre:", genre)
        print("Duration:", duration_1+"h "+duration_2+"m")
        print("Releasetime:", releasetime)

        # 關閉子視窗
        movieinfo_window.destroy()

    # 創建確定按鈕
    confirm_button = tk.Button(movieinfo_window, text="確定", command=get_movieinfo_input)
    confirm_button.grid(row=4, column=0, columnspan=3, pady=20)
    # 重置
    global releasetime_entry
    releasetime_entry = ''
    

def show_boxoffice_input():
    
    # 創建新視窗
    boxoffice_window = tk.Toplevel(window)
    boxoffice_window.title("Box Office Input")

    # 創建三個輸入框
    input_label_1 = tk.Label(boxoffice_window, text="Title:")
    input_label_1.grid(row=0, column=0, padx=10, pady=10)
    entry_1 = tk.Label(boxoffice_window, textvariable=movie_name)
    entry_1.grid(row=0, column=1, padx=10, pady=10)

    input_label_2 = tk.Label(boxoffice_window, text="Budget:")
    input_label_2.grid(row=1, column=0, padx=10, pady=10)
    entry_2 = tk.Entry(boxoffice_window)
    entry_2.grid(row=1, column=1, padx=10, pady=10)

    input_label_3 = tk.Label(boxoffice_window, text="Box_office:")
    input_label_3.grid(row=2, column=0, padx=10, pady=10)
    entry_3 = tk.Entry(boxoffice_window)
    entry_3.grid(row=2, column=1, padx=10, pady=10)

    col_list = ['title','budget','box_office']

    def get_boxoffice_input():
        global movie_name
        title = movie_name.get()
        
        budget = entry_2.get()
        box_office = entry_3.get()

        value_str = f"('{title}','{budget}','{box_office}')"
        insert_tool("boxoffice",col_list,value_str)

        print("Title:", title)
        print("budget:", budget)
        print("Box_office:", box_office)

        # 關閉子視窗
        boxoffice_window.destroy()

    # 創建確定按鈕
    confirm_button = tk.Button(boxoffice_window, text="確定", command=get_boxoffice_input)
    confirm_button.grid(row=3, column=0, columnspan=2, pady=20)
 
def show_award_input():

    # 創建新視窗
    award_window = tk.Toplevel(window)
    award_window.title("Award Input")

    # 創建三個輸入框
    input_label_1 = tk.Label(award_window, text="Title:")
    input_label_1.grid(row=0, column=0, padx=10, pady=10)
    entry_1 = tk.Label(award_window, textvariable=movie_name)
    entry_1.grid(row=0, column=1, padx=10, pady=10)

    input_label_2 = tk.Label(award_window, text="Oscar:")
    input_label_2.grid(row=1, column=0, padx=10, pady=10)
    entry_2 = tk.Entry(award_window)
    entry_2.grid(row=1, column=1, padx=10, pady=10)

    input_label_3 = tk.Label(award_window, text="Total:")
    input_label_3.grid(row=2, column=0, padx=10, pady=10)
    entry_3 = tk.Entry(award_window)
    entry_3.grid(row=2, column=1, padx=10, pady=10)

    col_list = ['title','oscar','total']
    
    def get_award_input():
        global movie_name
        title = movie_name.get()
        
        oscar = entry_2.get()
        total = entry_3.get()

        value_str = f"('{title}','{oscar}','{total}')"
        insert_tool("award",col_list,value_str)

        print("Title:", title)
        print("Oscar:", oscar)
        print("Total:", total)

        # 關閉子視窗
        award_window.destroy()

    # 創建確定按鈕
    confirm_button = tk.Button(award_window, text="確定", command=get_award_input)
    confirm_button.grid(row=3, column=0, columnspan=2, pady=20)

def show_crew_input():
    # 創建新視窗
    crew_window = tk.Toplevel(window)
    crew_window.title("Crew Input")
   
    # 創建四個輸入框
    input_label_1 = tk.Label(crew_window, text="Title:")
    input_label_1.grid(row=0, column=0, padx=10, pady=10)
    entry_1 = tk.Label(crew_window, textvariable=movie_name)
    entry_1.grid(row=0, column=1, padx=10, pady=10)

    input_label_2 = tk.Label(crew_window, text="Director:")
    input_label_2.grid(row=1, column=0, padx=10, pady=10)
    entry_2 = tk.Entry(crew_window)
    entry_2.grid(row=1, column=1, padx=10, pady=10)

    input_label_3 = tk.Label(crew_window, text="Writer:")
    input_label_3.grid(row=2, column=0, padx=10, pady=10)
    entry_3 = tk.Entry(crew_window)
    entry_3.grid(row=2, column=1, padx=10, pady=10)

    input_label_4 = tk.Label(crew_window, text="Producer:")
    input_label_4.grid(row=3, column=0, padx=10, pady=10)
    entry_4 = tk.Entry(crew_window)
    entry_4.grid(row=3, column=1, padx=10, pady=10)

    col_list = ['title','director','writer','producer']

    def get_crew_input():

        global movie_name
        title = movie_name.get()

        director = entry_2.get()
        writer = entry_3.get()
        producer = entry_4.get()

        value_str = f"('{title}','{director}','{writer}','{producer}')"
        insert_tool("crew",col_list,value_str)

        print("Title:", title)
        print("Director:", director)
        print("Writer:", writer)
        print("Producer:", producer)

        # 關閉子視窗
        crew_window.destroy()

    # 創建確定按鈕
    confirm_button = tk.Button(crew_window, text="確定", command=get_crew_input)
    confirm_button.grid(row=4, column=0, columnspan=2, pady=20)

birthdate_entry = ''
def show_cast_input():
    global movie_name
    
    # 創建新視窗
    cast_window = tk.Toplevel(window)
    cast_window.title("Cast Input")
    default_msg = tk.StringVar(value="default") # 設定防呆忘填

    def example1():
        def print_sel():
            global birthdate_entry
            
            input_date_str = cal.selection_get()
            # 日期格式
            input_date = datetime.datetime.strptime(str(input_date_str), "%Y-%m-%d")
            birthdate_entry = input_date.strftime("%Y/%m/%d")
            
            input_label_5 = tk.Label(cast_window, text=birthdate_entry)
            input_label_5.grid(row=3, column=2, padx=10, pady=10)

            print(cal.selection_get())
            cal.see(datetime.date(year=2016, month=2, day=5))

            # 關閉子視窗
            top.destroy()

        top = tk.Toplevel(cast_window)

        import datetime
        today = datetime.date.today()

        mindate = datetime.date(year=1700, month=1, day=1)
        maxdate = today 

        cal = Calendar(top, font="Arial 14", selectmode='day', locale='en_US',
                    mindate=mindate, maxdate=maxdate, disabledforeground='red',
                    cursor="hand1", year=2000, month=1, day=1)
        cal.grid()
        botton = ttk.Button(top, text="確認", command=print_sel)
        botton.grid()

    # 創建五個輸入框
    input_label_1 = tk.Label(cast_window, text="Name:")
    input_label_1.grid(row=0, column=0, padx=10, pady=10)
    entry_1 = tk.Entry(cast_window, textvariable=default_msg)
    entry_1.grid(row=0, column=1, padx=10, pady=10)

    # 選單
    input_label_2 = tk.Label(cast_window, text="Gender:")
    input_label_2.grid(row=1, column=0, padx=10, pady=10)
    gender_list = ["male","female"]
    gender_op_var_1 = tk.StringVar(cast_window)
    gender_op_var_1.set(gender_list[0])  # default選項
    entry_2 = ttk.Combobox(cast_window, textvariable=gender_op_var_1, values=gender_list,font=("Arial",8))
    entry_2.grid(row=1, column=1, padx=10, pady=10)

    input_label_3 = tk.Label(cast_window, text="Height:")
    input_label_3.grid(row=2, column=0, padx=10, pady=10)
    entry_3 = tk.Entry(cast_window)
    entry_3.grid(row=2, column=1, padx=10, pady=10)

    input_label_4 = tk.Label(cast_window, text="Birthday:")
    input_label_4.grid(row=3, column=0, padx=10, pady=10)
    entry_4 = ttk.Button(cast_window, text='點我', command=example1)
    entry_4.grid(row=3, column=1, padx=10, pady=10)

    input_label_5 = tk.Label(cast_window, text="Title:")
    input_label_5.grid(row=4, column=0, padx=10, pady=10)
    entry_5 = tk.Label(cast_window, textvariable=movie_name)
    entry_5.grid(row=4, column=1, padx=10, pady=10)

    col_list = ['name','gender','height','birthdate','title']
    def get_cast_input():
        title = movie_name.get()

        name = entry_1.get()
        gender = entry_2.get()
        height = entry_3.get()
        birthdate = birthdate_entry
        
        value_str = f"('{name}','{gender}','{height}','{birthdate}','{title}')"
        insert_tool("cast",col_list,value_str)

        print("Name:", name)
        print("Gender:", gender)
        print("Height:", height)
        print("Birthday:", birthdate)
        print("Title:", title)

        # 關閉子視窗
        cast_window.destroy()

    # 創建確定按鈕
    confirm_button = tk.Button(cast_window, text="確定", command=get_cast_input)
    confirm_button.grid(row=5, column=0, columnspan=2, pady=20)
    # 重置
    global birthdate_entry
    birthdate_entry = ''

# 建視窗
window = tk.Tk()
window.title("Database Viewer")
window.geometry("1920x1080")

#########################################################################################
# 去DB撈name
# query
query = "SELECT title FROM movieinfo;"
cursor.execute(query)
data = cursor.fetchall()
options_1 = [item[0] for item in data]
#########################################################################################
# select選單1
option_var_1 = tk.StringVar(window)
option_var_1.set(options_1[0])  # default選項

table_label_1 = tk.Label(window, text="選擇movie:",font=("Arial",14),fg="#2894FF")
table_label_1.place(relx=0.05, rely=0.01)

table_menu_1 = ttk.Combobox(window, textvariable=option_var_1, values=options_1,font=("Arial",14))
table_menu_1.place(relx=0.05, rely=0.05)

# select選單2
options_2 = ["movieinfo", "boxoffice", "award", "crew", "cast"]  # Replace with your actual table names
option_var_2 = tk.StringVar(window)
option_var_2.set(options_2[0])  # default選項

table_label_2 = tk.Label(window, text="選擇table:",font=("Arial",14),fg="#2894FF")
table_label_2.place(relx=0.25, rely=0.01)

table_menu_2 = ttk.Combobox(window, textvariable=option_var_2, values=options_2,font=("Arial",14))
table_menu_2.place(relx=0.25, rely=0.05)

# select Button
fetch_button = tk.Button(window, text="查詢", command=get_selected_data,font=("Arial",12),bg="purple",fg="white")
fetch_button.place(relx=0.55, rely=0.048)
#########################################################################################
# insert 的電影名
movie_name = tk.StringVar()   # 建立文字變數
movie_name.set('')            # 一開始設定沒有內容

# insert 電影名提示
movie_name_label = tk.Label(window, text="movie name:",font=("Arial",14),fg="#2894FF")
movie_name_label.place(relx=0.05, rely=0.1)
tk.Entry(window, textvariable=movie_name).place(relx=0.05, rely=0.15)  # 使用者輸入的名稱存在movie_name

# insert 提示
insert_label = tk.Label(window, text="選擇要insert的table:",font=("Arial",14),fg="#2894FF")
insert_label.place(relx=0.15, rely=0.1)

# insert Button 1
confirm_button_1 = tk.Button(window, text="movieinfo", command=show_movieinfo_input,font=("Arial",12),bg="blue",fg="white",width=8)
confirm_button_1.place(relx=0.15, rely=0.15)

# insert Button 2
confirm_button_2 = tk.Button(window, text="boxoffice", command=show_boxoffice_input,font=("Arial",12),bg="blue",fg="white",width=8)
confirm_button_2.place(relx=0.22, rely=0.15)

# insert Button 3
confirm_button_3 = tk.Button(window, text="award", command=show_award_input,font=("Arial",12),bg="blue",fg="white",width=8)
confirm_button_3.place(relx=0.29, rely=0.15)

# insert Button 4
confirm_button_4 = tk.Button(window, text="crew", command=show_crew_input,font=("Arial",12),bg="blue",fg="white",width=8)
confirm_button_4.place(relx=0.36, rely=0.15)

# insert Button 5
confirm_button_5 = tk.Button(window, text="cast", command=show_cast_input,font=("Arial",12),bg="blue",fg="white",width=8)
confirm_button_5.place(relx=0.43, rely=0.15)

# insert 確定按鈕
confirm_button_5 = tk.Button(window, text="新增", command=insert_confirm,font=("Arial",12),bg="purple",fg="white")
confirm_button_5.place(relx=0.55, rely=0.15)
query_list = []
#########################################################################################
# delete 選單1
del_op_var_1 = tk.StringVar(window)
del_op_var_1.set(options_1[0])  # default選項

table_label_1 = tk.Label(window, text="選擇movie:",font=("Arial",14),fg="#2894FF")
table_label_1.place(relx=0.05,rely=0.2)

table_menu_1 = ttk.Combobox(window, textvariable=del_op_var_1, values=options_1,font=("Arial",14))
table_menu_1.place(relx=0.05,rely=0.25)

# delete 選單2
del_op_var_2 = tk.StringVar(window)
del_op_var_2.set(options_2[0])  # default選項

table_label_2 = tk.Label(window, text="選擇table:",font=("Arial",14),fg="#2894FF")
table_label_2.place(relx=0.25,rely=0.2)

table_menu_2 = ttk.Combobox(window, textvariable=del_op_var_2, values=options_2,font=("Arial",14))
table_menu_2.place(relx=0.25,rely=0.25)

# delete Button
delete_button = tk.Button(window, text="刪除", command=get_delete_data,font=("Arial",12),bg="purple",fg="white")
delete_button.place(relx=0.55,rely=0.25)
#########################################################################################
# size~
display_text = tk.Text(window, height=1920, width=1080)
display_text.place(relx=0, rely=0.7)
#########################################################################################

# 開啟視窗
window.mainloop()

db.close()
#########################################################################################