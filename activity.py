'''-----------------------------------------------

                    ActivityDB
            Óðinn B og Matthías Ólafur

-----------------------------------------------'''
from tkinter import *
from tkinter import ttk
from tkinter import font as tkfont
from notendur import *
from iceconnect import *

class activity:

    def __init__(self,container,font_titill,notandinn):
        self.container = container
        self.font_titill = font_titill
        self.notandinn = notandinn

    def skipta(self,til,fra):
        if til == "valmynd":
            from valmynd import val
            val(self.container,self.font_titill,self.notandinn).valmynd()
        elif til == "actdb":
            self.actdb()
        elif til == "actdb_add":
            self.actdb_add()
        elif til == "actdb_social_add":
            self.actdb_social_add()
        elif til == "actdb_social_eyda":
            self.actdb_social_eyda()
        elif til == "actdb_update":
            self.actdb_update()
        fra.grid_remove()

    def actdb(self):
        self.act = Frame(self.container)
        self.act.grid(row=0,column=0,pady=50,sticky="nsew")
        Label(self.act, text="ActivityDB  Activity", font=self.font_titill).grid(row=0,column=0,sticky="w",pady=17)
        texti = "| Notandi | "+self.notandinn[0]+" | "
        if self.notandinn[2]:
            texti += " Admin Réttindi |"
        else:
            texti += " Venjuleg Réttindi |"
        Label(self.act, text=texti, font="Arial 13").grid(row=0,column=3,sticky="e",pady=17)

        self.tree = ttk.Treeview(self.act, columns=('Nafn Activity','Fyrirtaeki','Vefsida','Postnumer'),height=20)
        self.tree.heading('#0', text='ActivityID')
        self.tree.heading('#1', text='Nafn Activity')
        self.tree.heading('#2', text='Fyrirtæki')
        self.tree.heading('#3', text='Vefsíða')
        self.tree.heading('#4', text='Póstnúmer')
        self.tree.column("#0",width=160)
        self.tree.column("#1",width=300)
        self.tree.column("#2",width=200)
        self.tree.column("#3",width=200)
        self.tree.column("#4",width=100)
        at = ActivityDB()
        act = at.activity_list()
        act.sort()
        for x in range(len(act)):
            self.tree.insert("", x, act[x][0], text=act[x][0],
                             values=(act[x][1], act[x][2], act[x][3], act[x][4]))
            nanar = at.get_activity(act[x][0])
            self.tree.insert(act[x][0], 1, text='- Hverfi -', values=str(nanar[3]))
            seinast = 3
            social = at.get_activity_media_list(act[x][0])
            if len(social) > 0:
                for i in range(len(social)):
                    self.tree.insert(act[x][0], seinast + i + 1, text='- ' + social[i][1] + ' -', values=(social[i][2]))
                self.tree.insert(act[x][0], seinast + 1, text='')
                seinast = len(social) + 2 + seinast
            else:
                self.tree.insert(act[x][0], seinast + 1, text='')
                seinast += 1
            self.tree.insert(act[x][0], 0, text='')
            seinast += 1
            if self.notandinn[2]:
                upp = "upp" + str(act[x][0])
                self.tree.insert(act[x][0], seinast + 1, text='Uppfæra', tags=(upp, act[x][0]))
                self.tree.tag_configure(upp, background='cyan')
                self.tree.tag_bind(upp, '<Double-1>', self.uppfaeraht)
                baetasocial = "social" + str(act[x][0])
                self.tree.insert(act[x][0], seinast + 2, text='Bæta Við Socialmedia', tags=(baetasocial, act[x][0]))
                self.tree.tag_configure(baetasocial, background='orange')
                self.tree.tag_bind(baetasocial, '<Double-1>', self.baetaSocial)
                seinast += 2
                if len(at.get_activity_media_list(act[x][0])) > 0:
                    eydamedia = "eydamedia" + str(act[x][0])
                    self.tree.insert(act[x][0], seinast + 1, text='Eyða Socialmedia', tags=(eydamedia, act[x][0]))
                    self.tree.tag_configure(eydamedia, background='#ff6464')
                    self.tree.tag_bind(eydamedia, '<Double-1>', self.eydaMedia)
                    seinast += 1
                eyda = "eyda" + str(act[x][0])
                self.tree.insert(act[x][0], seinast + 1, text='Eyða', tags=(eyda, act[x][0]))
                self.tree.tag_configure(eyda, background='#ff6464')
                self.tree.tag_bind(eyda, '<Double-1>', self.eydarest)
        self.tree.grid(row=1, columnspan=4, sticky='nsew')
        if self.notandinn[2]:
            baeta = ttk.Button(self.act, text="Bæta Við Nýju Activity",command=lambda: self.skipta("actdb_add",self.act))
            baeta.grid(row=3, column=0, pady=6,sticky=NW)
        tilbaka = ttk.Button(self.act, text="Til Baka",
                             command=lambda: self.skipta("valmynd", self.act))
        tilbaka.grid(row=3, column=3, pady=6,sticky=E)

    def actdb_add(self):
        self.act_add = Frame(self.container)
        self.act_add.grid(row=0,column=0,pady=50,sticky="nsew")
        Label(self.act_add, text="Bæta Við Nýju Activity", font=self.font_titill).grid(row=0, column=1, sticky="nsew",pady=17)
        Label(self.act_add, text="Activity Nafn", font=self.font_titill).grid(row=1, column=0, sticky="e")
        self.actnafn = Entry(self.act_add, font=("Arial", 12), width=15)
        self.actnafn.grid(row=1, column=1, pady=6)
        Label(self.act_add, text="Fyrirtæki", font=self.font_titill).grid(row=2, column=0, sticky="e")
        self.fyrir = Entry(self.act_add, font=("Arial", 12), width=15)
        self.fyrir.grid(row=2, column=1, pady=6)
        Label(self.act_add, text="Vefsíða", font=self.font_titill).grid(row=3, column=0, sticky="e")
        self.vefsida = Entry(self.act_add, font=("Arial", 12), width=15)
        self.vefsida.grid(row=3, column=1, pady=6)
        Label(self.act_add, text="Póstnúmer", font=self.font_titill).grid(row=4, column=0, sticky="e")
        self.postnumer = Entry(self.act_add, font=("Arial", 12), width=15)
        self.postnumer.grid(row=4, column=1, pady=6)
        tilbaka = ttk.Button(self.act_add, text="Bæta Við",
                             command=lambda: self.baetaVidrest())
        tilbaka.grid(row=5, column=1, pady=6, sticky="S")
        tilbaka = ttk.Button(self.act_add, text="Til Baka",
                             command=lambda: self.skipta("actdb", self.act_add))
        tilbaka.grid(row=5, column=2, pady=6, sticky=N)
        self.þarf = Label(self.act_add, text="", font="arial 10",fg="red")
        self.þarf.grid(row=6, column=1)

    def actdb_social_add(self):
        at = ActivityDB()
        socialmedia = at.get_activity_social_list()
        self.act_social_add = Frame(self.container)
        self.act_social_add.grid(row=0,column=0,pady=50,sticky="nsew")
        Label(self.act_social_add, text="Bæta Við SocialMedia Fyrir Activity", font=self.font_titill).grid(row=0, column=1, sticky="nsew",pady=17)
        Label(self.act_social_add, text="Veldu Media", font=self.font_titill).grid(row=1, column=0, sticky="e")
        self.social = StringVar()
        values = []
        for x in socialmedia:
            values.append(x[1])
        self.dropdown = ttk.Combobox(self.act_social_add, textvariable=self.social, values=values, state="readonly")
        self.dropdown.grid(row=1, column=1, pady=6)
        Label(self.act_social_add, text="Media URL", font=self.font_titill).grid(row=2, column=0, sticky="e")
        self.socialurl = Entry(self.act_social_add, font=("Arial", 12), width=15)
        self.socialurl.grid(row=2, column=1, pady=6)
        tilbaka = ttk.Button(self.act_social_add, text="Bæta Við",
                             command=lambda: self.baetaVidSocial())
        tilbaka.grid(row=3, column=1, pady=6, sticky="S")
        tilbaka = ttk.Button(self.act_social_add, text="Til Baka",
                             command=lambda: self.skipta("actdb", self.act_social_add))
        tilbaka.grid(row=3, column=2, pady=6, sticky=N)
        self.þarf = Label(self.act_social_add, text="", font="arial 10",fg="red")
        self.þarf.grid(row=4, column=1)

    def actdb_social_eyda(self):
        at = ActivityDB()
        socialmedia = at.get_activity_media_list(self.actID)
        self.act_social_eyda = Frame(self.container)
        self.act_social_eyda.grid(row=0,column=0,pady=50,sticky="nsew")
        Label(self.act_social_eyda, text="Eyða SocialMedia Hjá Veitingastaði", font=self.font_titill).grid(row=0, column=1, sticky="nsew",pady=17)
        Label(self.act_social_eyda, text="Veldu Media", font=self.font_titill).grid(row=1, column=0, sticky="e")
        self.social = StringVar()
        values = []
        for x in socialmedia:
            values.append(x[1]+": "+x[2])
        self.dropdown = ttk.Combobox(self.act_social_eyda, textvariable=self.social, values=values, state="readonly", width=50)
        self.dropdown.grid(row=1, column=1, pady=10)
        tilbaka = ttk.Button(self.act_social_eyda, text="Eyða",
                             command=lambda: self.eydaSocial())
        tilbaka.grid(row=2, column=1, pady=6, sticky="S")
        tilbaka = ttk.Button(self.act_social_eyda, text="Til Baka",
                             command=lambda: self.skipta("actdb", self.act_social_eyda))
        tilbaka.grid(row=2, column=2, pady=6, sticky=N)
        self.þarf = Label(self.act_social_eyda, text="", font="arial 10",fg="red")
        self.þarf.grid(row=3, column=1)

    def actdb_update(self):
        self.act_update = Frame(self.container)
        self.act_update.grid(row=0, column=0, pady=50, sticky="nsew")
        Label(self.act_update, text="Uppfæra Acitivity", font=self.font_titill).grid(row=0, column=1,
                                                                                        sticky="nsew", pady=17)
        Label(self.act_update, text="Activity Nafn", font=self.font_titill).grid(row=1, column=0, sticky="e")
        self.actnafn = Entry(self.act_update, font=("Arial", 12), width=15)
        self.actnafn.grid(row=1, column=1, pady=6)
        self.actnafn.insert(0, str(self.actInfo[1]))
        Label(self.act_update, text="Fyrirtæki", font=self.font_titill).grid(row=2, column=0, sticky="e")
        self.fyrir = Entry(self.act_update, font=("Arial", 12), width=15)
        self.fyrir.grid(row=2, column=1, pady=6)
        self.fyrir.insert(0, str(self.actInfo[2]))
        Label(self.act_update, text="Vefsíða", font=self.font_titill).grid(row=3, column=0, sticky="e")
        self.vefsida = Entry(self.act_update, font=("Arial", 12), width=15)
        self.vefsida.grid(row=3, column=1, pady=6)
        self.vefsida.insert(0, str(self.actInfo[4]))
        Label(self.act_update, text="Póstnúmer", font=self.font_titill).grid(row=4, column=0, sticky="e")
        self.postnumer = Entry(self.act_update, font=("Arial", 12), width=15)
        self.postnumer.grid(row=4, column=1, pady=6)
        self.postnumer.insert(0, str(self.actInfo[5]))
        tilbaka = ttk.Button(self.act_update, text="Uppfæra",
                             command=lambda: self.uppfaerarest())
        tilbaka.grid(row=5, column=1, pady=6, sticky="S")
        tilbaka = ttk.Button(self.act_update, text="Til Baka",
                             command=lambda: self.skipta("actdb", self.act_update))
        tilbaka.grid(row=5, column=2, pady=6, sticky=N)
        self.þarf = Label(self.act_update, text="", font="arial 10", fg="red")
        self.þarf.grid(row=6, column=1)

    def baetaVidrest(self):
        at = ActivityDB()
        actnafn = self.actnafn.get()
        fyrir = self.fyrir.get()
        vefsida = self.vefsida.get()
        postnumer = self.postnumer.get()
        if actnafn == "" or postnumer == "":
            self.þarf.config(text="Fylltu inn í Activity Nafn og Póstnúmer")
        else:
            at.add_activity(actnafn,fyrir,vefsida,postnumer)
            self.þarf.config(text="")
            self.actnafn.delete(0, END)
            self.fyrir.delete(0, END)
            self.vefsida.delete(0, END)
            self.postnumer.delete(0, END)
            self.skipta("actdb",self.act_add)

    def uppfaerarest(self):
        at = ActivityDB()
        actnafn = self.actnafn.get()
        fyrir = self.fyrir.get()
        vefsida = self.vefsida.get()
        postnumer = self.postnumer.get()
        if actnafn == "" or postnumer == "":
            self.þarf.config(text="Fylltu inn í Activity Nafn og Póstnúmer")
        else:
            at.update_activity(self.actID,actnafn,fyrir,vefsida,postnumer)
            self.þarf.config(text="")
            self.skipta("actdb",self.act_update)

    def uppfaeraht(self,event):
        at = ActivityDB()
        focus = self.tree.focus()
        item = self.tree.item(focus)
        self.actID = item['tags'][1]
        self.actInfo = at.get_activity(self.actID)
        self.skipta("actdb_update",self.act)

    def baetaSocial(self,event):
        focus = self.tree.focus()
        item = self.tree.item(focus)
        self.actID = item['tags'][1]
        self.skipta("actdb_social_add",self.act)

    def baetaVidSocial(self):
        media = self.social.get()
        mediaurl = self.socialurl.get()
        if mediaurl == "" or media == "":
            self.þarf.config(text="Veldu Media og fylltu inn í Media URL")
        else:
            at = ActivityDB()
            socialmedia = at.get_activity_social_list()
            mediaID = ""
            for x in socialmedia:
                if x[1] == media:
                    mediaID = x[0]
            at.add_activity_media(self.actID,mediaID,mediaurl)
            self.þarf.config(text="")
            self.dropdown.delete(0, END)
            self.socialurl.delete(0, END)
            self.skipta("actdb",self.act_social_add)

    def eydarest(self,event):
        focus = self.tree.focus()
        item = self.tree.item(focus)
        at = ActivityDB()
        at.delete_activity(item['tags'][1])
        self.act.grid_remove()
        self.actdb()

    def eydaMedia(self,event):
        focus = self.tree.focus()
        item = self.tree.item(focus)
        self.actID = item['tags'][1]
        self.skipta("actdb_social_eyda",self.act)

    def eydaSocial(self):
        media = self.social.get()
        if media == "":
            self.þarf.config(text="Veldu Media til að eyða")
        else:
            at = ActivityDB()
            socialmedia = at.get_activity_media_list(self.actID)
            mediaID = ""
            for x in socialmedia:
                texti = x[1]+": "+x[2]
                if texti == media:
                    mediaID = x[3]
            at.remove_activity_media(self.actID,mediaID)
            self.þarf.config(text="")
            self.dropdown.delete(0, END)
            self.skipta("actdb",self.act_social_eyda)
