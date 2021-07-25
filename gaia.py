from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import numpy as np
import pandas as pd
import gspread
import time

gc = gspread.oauth()

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

    csv = pd.read_table(csv_file_path, header=None, sep=",", names=list(range(40)))
    df = pd.DataFrame(columns=['Ret', 'Antal'])
    for column in csv:
        if(column > 1):
            if (column % 2) == 0:
                xtra = pd.DataFrame(data=csv.iloc[:, [column, column+1]])
                xtra.columns = ['Ret', 'Antal']
                df = df.append(xtra, ignore_index= True)
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

root.call('wm', 'iconphoto', root._w, PhotoImage(file='./assets/icon.png'))
root.title("Gaia's Awesome Backend Software")
tabControl = ttk.Notebook(root)
  
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
  
tabControl.add(tab1, text ='Dashboard')
tabControl.add(tab2, text ='Opskrifter')
tabControl.add(tab3, text ='Ingredienser')
tabControl.grid(row = 0, column=0)

welcomeText = "Velkommen til Gaia's awesome backend software. Her kan du importere csv filer, og se salgstal."
myLabel1 = Label(tab1, text=welcomeText).grid(row=0, columnspan="2", sticky="N")
Button(tab1, text='Importer Sales Report',command=import_sales_csv).grid(row=1, column=1, ipady=12, ipadx=12)
buttonSalesNumbers = Button(tab1, text="Tryk her for at se salgstal", command=get_product_sales).grid(row=1, column=0, ipady=12, ipadx=12)
buttonDelete = Button(tab1, text="Importer Abonnentstal", command=import_subscription_csv).grid(row=2, column=1, ipady=12, ipadx=12)

root.mainloop()
