from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from ingredient import Ingredient
import numpy as np
import pandas as pd
import gspread
import time

gc = gspread.oauth()

def add_ingredient():
    ingredientWindow = Tk()
    ingredientWindow.geometry('800x600')
    ingredientWindow.title("Tilføj ingrediens")
    Label(ingredientWindow, text='Navn').pack()
    name = Entry(ingredientWindow).pack()
    Label(ingredientWindow, text='Pris').pack()
    price = Entry(ingredientWindow).pack()
    Label(ingredientWindow, text='Kcal').pack()
    kcal = Entry(ingredientWindow).pack()
    Label(ingredientWindow, text='Fedt').pack()
    fat = Entry(ingredientWindow).pack()
    Label(ingredientWindow, text='Kulhydrater').pack()
    carbs = Entry(ingredientWindow).pack()
    Label(ingredientWindow, text='Protein').pack()
    protein = Entry(ingredientWindow).pack()
    ingredient = Ingredient("Kartofler", 10, 99, 99, 99, 99)
    print(ingredient.name)
    ingredient.pushToDatabase()


def import_subscription_csv():
    sh = gc.open('Mad')
    worksheet = sh.worksheet("Uge")
    csv_file_path = askopenfilename()
    a_file = open(csv_file_path, "r")
    lines = a_file.readlines()
    a_file.close()
    new_file = open(csv_file_path, "w+")
    string = "order_items"
    for line in lines:
        if string in line:
            print('Found string')
            lines.remove(line)
        else:
            new_file.write(line.replace('"', ''))

    new_file.close()

    csv = pd.read_table(csv_file_path, header=None,
                        sep=",", names=list(range(40)))
    df = pd.DataFrame(columns=['Ret', 'Antal'])
    for column in csv:
        if(column > 1):
            if (column % 2) == 0:
                xtra = pd.DataFrame(data=csv.iloc[:, [column, column+1]])
                xtra.columns = ['Ret', 'Antal']
                df = df.append(xtra, ignore_index=True)
            else:
                print('Append 1')
    df = df.dropna()
    # Eliminate invalid data from dataframe (see Example below for more context)

    num_df = (df.drop(['Antal'], axis=1)
              .join(df['Antal'].apply(pd.to_numeric, errors='coerce')))
    num_df = num_df.dropna()
    num_df["Antal"] = pd.to_numeric(num_df["Antal"])
    sales = num_df.groupby('Ret').sum()
    sales = sales.reset_index()
    for row in sales.itertuples():
        try:
            cell = worksheet.find(row.Ret)
            time.sleep(1)
            worksheet.update_cell(cell.row, cell.col+4, row.Antal)
        except gspread.exceptions.CellNotFound:  # or except gspread.CellNotFound:
            print('Not found')


def import_sales_csv():
    sh = gc.open('Mad')
    worksheet = sh.worksheet("Uge")
    csv_file_path = askopenfilename()
    df = pd.read_csv(csv_file_path)
    for index, row in df.iterrows():
        print(row[0])
        try:
            cell = worksheet.find(row[0])
            print(cell)
            time.sleep(1)
            worksheet.update_cell(cell.row, cell.col+1, row[1])
        except gspread.exceptions.CellNotFound:  # or except gspread.CellNotFound:
            print('Not found')


def get_product_sales():
    sh = gc.open('Mad')
    val = sh.values_get("Uge!A2:B76")
    rows = val.get('values', [])
    df = pd.DataFrame(rows)
    popup = Tk()
    for index, row in df.iterrows():
        Label(popup, text=row[0]).grid(row=index, column=0)
        Label(popup, text=row[1]).grid(row=index, column=1)


root = Tk()
root.geometry('')
root.call('wm', 'iconphoto', root._w, PhotoImage(file='./assets/icon.png'))
root.title("Gaia's Awesome Backend Software")

canvas = Canvas(root)
canvas.pack()

notebook = ttk.Notebook(canvas)
notebook.pack(pady=10, expand=True)

tab1 = ttk.Frame(notebook, width=800, height=580)
tab2 = ttk.Frame(notebook, width=800, height=580)
tab3 = ttk.Frame(notebook, width=800, height=580)

tab1.pack(fill='both', expand=True)
tab2.pack(fill='both', expand=True)
tab3.pack(fill='both', expand=True)

notebook.add(tab1, text='Dashboard')
notebook.add(tab2, text='Ingredienser')
notebook.add(tab3, text='Retter')

    # Tab 1 - Dashboard

welcomeText = "Velkommen til Gaia's awesome backend software. Her kan du importere csv filer, og se salgstal."
myLabel1 = Label(tab1, text=welcomeText).place(relx=0, rely=0, relheight=0.1, relwidth=1.0)
Button(tab1, text='Importer Salgsrapport', command=import_sales_csv).place(relx=0.2, rely=0.1, relheight=0.2, relwidth=0.2)
Button(tab1, text="Importer Abonnentstal", command=import_subscription_csv).place(relx=0.2, rely=0.3, relheight=0.2, relwidth=0.2)
Button(tab1, text="Tryk her for at se salgstal",command=get_product_sales).place(relx=0.6, rely=0.1, relheight=0.2, relwidth=0.2)

    # Tab2 - Ingredienser

Button(tab2, text="Tilføj Ingrediens",command=add_ingredient).place(relx=0.1, rely=0.1, relheight=0.2, relwidth=0.2)
sample = {"File Name":[f"file_{i}" for i in range(5)],
          'Sheet Name': [f"sheet_{i}" for i in range(5)],
          'Number Of Rows': [f"row_{i}" for i in range(5)],
          'Number Of Columns': [f"col_{i}" for i in range(5)]
          }
df = pd.DataFrame(sample)
cols = list(df.columns)

tree = ttk.Treeview(tab2)
tree.place(relx=0.0, rely=0.3, relheight=0.7, relwidth=1.0)
tree["columns"] = cols
for i in cols:
    tree.column(i, anchor="w")
    tree.heading(i, text=i, anchor='w')

for index, row in df.iterrows():
    tree.insert("",0,text=index,values=list(row))

root.mainloop()
