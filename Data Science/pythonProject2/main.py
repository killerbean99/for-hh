import tkinter as tk
from tkinter import filedialog
import pandas as pd


# Chose file function
def open_file():
    name = input_name.get().upper()
    app.filename = filedialog\
        .askopenfilename(filetypes=(("exel files", "*.xlsx"), ("all files", "*.*")))
    tk.Label(app, text=app.filename).pack()
    csv_file = str(name) + '.csv'
    data = pd.read_excel(app.filename)
    data.columns = ['Lname', 'Fname', 'Id', 'Format', 'Group', 'Course', \
                    'Kafedra', 'MT1', 'MT2', 'MTmid', 'Exam', 'Final']
    del data['Format']
    data.to_csv(csv_file, encoding='utf-8', index=False)
    data = data[data.Group == name]
    courses_file = str(name) + '_courses.xlsx'
    courses = data.Course
    courses = courses.drop_duplicates()
    courses.to_excel(courses_file)
    del data['Group']
    del data['Fname']

    lang_courses = data[data.Kafedra == 'Кафедра Языков']
    lang_courses.drop('Lname', axis='columns')
    lang_courses.drop('Kafedra', axis000='columns')
    lang_courses = lang_courses.dropna(axis=0, how='any', inplace=False)
    # 'азахский язык'

    data = data[data.Kafedra != 'Кафедра Языков']

    del data['Kafedra']

    data = pd.pivot_table(data, index=['Id'], columns='Course', values=['MT1', 'MT2', 'MTmid', 'Exam', 'Final'], fill_value=0)

    group_file = str(name) + '.xlsx'
    data.to_excel(group_file)
    global count
    count += 1
    btn_1['text'] = f'Files: {count}'
    
'''
def go():  # Settings function
    sts = tk.Tk()
    sts.title("Settings")
    sts.geometry("500x300")
    photo2 = tk.PhotoImage(file='sts.png')
    sts.iconphoto(True, photo2)
    sts.config(bg="pink")
    sts.minsize(500, 300)
    sts.maxsize(1500, 1000)
    btn_3 = tk.Button(sts, text='Start')
    btn_3.pack()
'''


count = 0
height = 500
width = 700
min_height = 300
min_width = 500
size = str(width) + 'x' + str(height)


# Window
app = tk.Tk()
app.title("Finder")
app.geometry(size)
#photo = tk.PhotoImage(file='my.png')
#app.iconphoto(True, photo)
app.config(bg="pink")
app.minsize(min_width, min_height)
app.grid_columnconfigure(0, minsize=100)
app.grid_columnconfigure(1, minsize=100)


# Chose file
btn_1 = tk.Button(app, text='Chose files', command=open_file, \
                  activebackground='green', state=tk.NORMAL)
mylabel = tk.Label(app, text = 'Enter group name')
mylabel.pack()


# btn_1.grid(row=1, column=1)
input_name = tk.Entry(app)
input_name.pack()

btn_1.pack()

app.mainloop()
