'''-----------------------------------------------

                    Keyrsla
            Óðinn B og Matthías Ólafur

-----------------------------------------------'''
from tkinter import *
from tkinter import ttk
from tkinter import font as tkfont
from valmynd import *

root = Tk()
root.title("IceConnect")
root.minsize(1200, 700)
font_titill = tkfont.Font(family='Arial', size=15, weight="bold")
container = Frame(root)
container.pack()
style = ttk.Style(root)
style.theme_use("clam")
style.configure("TButton", background="black",
                fieldbackground="black", foreground="white", borderwidth=6)
style.configure("Treeview.Insert", padding=10)
style.configure("Treeview.Heading", background="black", foreground='white', borderwidth=8)
val(container,font_titill,["Matti","",1]).valmynd()
root.mainloop()
