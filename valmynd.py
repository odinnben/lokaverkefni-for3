'''-----------------------------------------------

                    Valmynd
            Óðinn B og Matthías Ólafur

-----------------------------------------------'''
from tkinter import *
from tkinter import ttk
from tkinter import font as tkfont
from notendur import *
from iceconnect import *
from place import place
from hotel import hotel
from restaurant import rest
from activity import activity

class val:

    def __init__(self,container,font_titill,notandinn=None):
        self.container = container
        self.font_titill = font_titill
        self.notandinn = notandinn

    def skipta(self,til,fra):
        if til == "valmynd":
            self.valmynd()
        elif til == "placedb":
            place(self.container, self.font_titill, self.notandinn).placedb()
        elif til == "hoteldb":
            hotel(self.container, self.font_titill, self.notandinn).hoteldb()
        elif til == "restdb":
            rest(self.container, self.font_titill, self.notandinn).restdb()
        elif til == "actdb":
            activity(self.container, self.font_titill, self.notandinn).actdb()
        fra.grid_remove()

    def login(self):
        self.log = Frame(self.container)
        self.log.grid(row=0,column=0,pady=50,sticky="nsew")
        self.label = Label(self.log, text="Notendanafn", font=self.font_titill)
        self.label.grid(row=0,column=0)
        self.notendanafn = Entry(self.log, font=("Arial", 12), width=15)
        self.notendanafn.grid(row=1,column=0,pady=6)
        self.notendanafn.focus()
        label2 = Label(self.log, text="Lykilorð", font=self.font_titill)
        label2.grid(row=2,column=0)
        self.lykilord = Entry(self.log, font=("Arial", 12), width=15, show="*")
        self.lykilord.grid(row=3,column=0,pady=6)
        self.lykilord.bind("<Return>", self.skrainn)
        loginTakki = ttk.Button(self.log, text="Skrá Inn")
        loginTakki.grid(row=4, column=0, pady=20)
        loginTakki.bind("<Button-1>", self.skrainn)
        self.label3 = Label(self.log, text="",fg="red",font="arial 10",width="25")
        self.label3.grid(row=5,column=0)

    def skrainn(self, event):
        note = str(self.notendanafn.get())
        lykil = str(self.lykilord.get())
        if note != "" and lykil != "":
            notandinn = notendur().getUser(note)
            if len(notandinn) > 0:
                if lykil == notandinn[1]:
                    self.notandinn = notandinn
                    self.skipta("valmynd",self.log)
        self.label3.config(text="Rangt notandanafn eða lykilorð")
        self.lykilord.delete(0, END)

    def skraut(self,fra):
        self.login()
        fra.grid_remove()

    def valmynd(self):
        self.val = Frame(self.container)
        self.val.grid(row=0,column=0,pady=50,sticky="nsew")
        Label(self.val, text="  Veldu Database\t", font=self.font_titill).grid(row=0,column=1,sticky="nsew",pady=17)
        texti = "| Notandi | "+self.notandinn[0]+" | "
        if self.notandinn[2]:
            texti2 = "| Admin Réttindi |"
        else:
            texti2 = "| Venjuleg Réttindi |"
        Label(self.val, text=texti, font="Arial 13").grid(row=0,column=0,sticky="nsew",pady=17)
        Label(self.val, text=texti2, font="Arial 13").grid(row=0,column=2,sticky="nsew",pady=17)
        Label(self.val, text="PlaceDB", font=self.font_titill).grid(row=1,column=0,sticky="nsew")
        placedb = ttk.Button(self.val, text="Velja",command=lambda: self.skipta("placedb",self.val))
        placedb.grid(row=1, column=2, pady=6)
        Label(self.val, text="HotelDB", font=self.font_titill).grid(row=2,column=0,sticky="nsew")
        hoteldb = ttk.Button(self.val, text="Velja",command=lambda: self.skipta("hoteldb",self.val))
        hoteldb.grid(row=2, column=2, pady=6)
        Label(self.val, text="RestaurantDB", font=self.font_titill).grid(row=3,column=0,sticky="nsew")
        restdb = ttk.Button(self.val, text="Velja",command=lambda: self.skipta("restdb",self.val))
        restdb.grid(row=3, column=2, pady=6)
        Label(self.val, text="ActivityDB", font=self.font_titill).grid(row=4,column=0,sticky="nsew")
        activitydb = ttk.Button(self.val, text="Velja",command=lambda: self.skipta("actdb",self.val))
        activitydb.grid(row=4, column=2, pady=6)
        activitydb = ttk.Button(self.val, text="Skrá út",command=lambda: self.skraut(self.val))
        activitydb.grid(row=5, column=2, pady=6)