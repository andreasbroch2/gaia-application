from tkinter import *
from tkinter import ttk

root = Tk()


root.call('wm', 'iconphoto', root._w, PhotoImage(file='./assets/icon.png'))
root.title("Gaia's Awesome Backend Software")

mainframe = ttk.Frame(root, padding="12 12 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

welcomeText = "Velkommen til Gaia's awesome backend software. Her kan du importere csv filer, og se salgstal."
myLabel1 = Label(mainframe, text=welcomeText).grid(row=0, columnspan="2", sticky="N")

buttonCSV = Button(mainframe, text="Tryk her for at importere en csv fil").grid(row=1, column=0)
buttonSalesNumbers = Button(mainframe, text="Tryk her for at se salgstal").grid(row=2, column=0)
buttonDelete = Button(mainframe, text="Tryk her for at nulstille").grid(row=3, column=0)

root.mainloop()
