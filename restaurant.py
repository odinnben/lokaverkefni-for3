'''-----------------------------------------------

                    RestaurantDB
            Óðinn B og Matthías Ólafur

-----------------------------------------------'''
from tkinter import *
from tkinter import ttk
from tkinter import font as tkfont
from notendur import *
from iceconnect import *

class rest:

    def __init__(self,container,font_titill,notandinn):
        self.container = container
        self.font_titill = font_titill
        self.notandinn = notandinn

    def skipta(self,til,fra):
        if til == "valmynd":
            from valmynd import val
            val(self.container,self.font_titill,self.notandinn).valmynd()
        elif til == "restdb":
            self.restdb()
        elif til == "restdb_add":
            self.restdb_add()
        elif til == "restdb_social_add":
            self.restdb_social_add()
        elif til == "restdb_social_eyda":
            self.restdb_social_eyda()
        elif til == "restdb_update":
            self.restdb_update()
        fra.grid_remove()

    def restdb(self):
        self.rest = Frame(self.container)
        self.rest.grid(row=0,column=0,pady=50,sticky="nsew")
        Label(self.rest, text="RestaurantDB  Veitingarstaðir", font=self.font_titill).grid(row=0,column=0,sticky="w",pady=17)
        texti = "| Notandi | "+self.notandinn[0]+" | "
        if self.notandinn[2]:
            texti += " Admin Réttindi |"
        else:
            texti += " Venjuleg Réttindi |"
        Label(self.rest, text=texti, font="Arial 13").grid(row=0,column=3,sticky="e",pady=17)

        self.tree = ttk.Treeview(self.rest, columns=('Veitingastadur','Stadsetning','Postnumer','Hverfi','Simanumer'),height=20)
        self.tree.heading('#0', text='RestaurantID')
        self.tree.heading('#1', text='Veitingastaður')
        self.tree.heading('#2', text='Staðsetning')
        self.tree.heading('#3', text='Póstnúmer')
        self.tree.heading('#4', text='Hverfi')
        self.tree.heading('#5', text='Símanúmer')
        self.tree.column("#0",width=160)
        self.tree.column("#1",width=300)
        self.tree.column("#2",width=200)
        self.tree.column("#3",width=100)
        self.tree.column("#4",width=100)
        self.tree.column("#5",width=150)
        rt = RestaurantDB()
        rest = rt.get_restaurant_list()
        rest.sort()
        for x in range(len(rest)):
            self.tree.insert("", x, rest[x][0], text=rest[x][0],values=(rest[x][1],rest[x][2],rest[x][3],rest[x][4],rest[x][5]))
            nanar = rt.get_restaurant(rest[x][0])
            if nanar[9] != None and nanar[10] != None:
                self.tree.insert(rest[x][0], 1, text='- Gerð Veitingastaðs -',values=str(nanar[4]))
                self.tree.insert(rest[x][0], 3, text='- Fjöldi sæta -',values=str(nanar[5]))
                self.tree.insert(rest[x][0], 4, text='- Vefsíða -',values=str(nanar[7]))
                self.tree.insert(rest[x][0], 5, text='- Framkvæmdastjóri -',values=str(nanar[8]))
                self.tree.insert(rest[x][0], 6, text='- Latitude -',values=str(nanar[9]))
                self.tree.insert(rest[x][0], 6, text='- Longitude -',values=str(nanar[10]))
                seinast = 5
            else:
                self.tree.insert(rest[x][0], 1, text='- Gerð Veitingastaðs -',values=str(nanar[4]))
                self.tree.insert(rest[x][0], 3, text='- Fjöldi sæta -',values=str(nanar[5]))
                self.tree.insert(rest[x][0], 4, text='- Vefsíða -',values=str(nanar[7]))
                self.tree.insert(rest[x][0], 5, text='- Framkvæmdastjóri -',values=str(nanar[8]))
                seinast = 3
            social = rt.get_restaurant_media_list(rest[x][0])
            if len(social) > 0:
                for i in range(len(social)):
                    self.tree.insert(rest[x][0],seinast+i+1, text='- '+social[i][1]+' -',values=(social[i][2]))
                seinast = len(social)+1+seinast
            else:
                self.tree.insert(rest[x][0], seinast+1, text='')
                seinast += 1
            self.tree.insert(rest[x][0], 0, text='')
            self.tree.insert(rest[x][0], seinast+1, text='')
            seinast+=1
            if self.notandinn[2]:
                upp = "upp"+str(rest[x][0])
                self.tree.insert(rest[x][0], seinast+1, text='Uppfæra', tags=(upp,rest[x][0]))
                self.tree.tag_configure(upp, background='cyan')
                self.tree.tag_bind(upp, '<Double-1>', self.uppfaeraht)
                baetasocial = "social"+str(rest[x][0])
                self.tree.insert(rest[x][0], seinast+2, text='Bæta Við Socialmedia', tags=(baetasocial,rest[x][0]))
                self.tree.tag_configure(baetasocial, background='orange')
                self.tree.tag_bind(baetasocial, '<Double-1>', self.baetaSocial)
                seinast += 2
                if len(rt.get_restaurant_media_list(rest[x][0])) > 0:
                    eydamedia = "eydamedia"+str(rest[x][0])
                    self.tree.insert(rest[x][0], seinast+1, text='Eyða Socialmedia', tags=(eydamedia,rest[x][0]))
                    self.tree.tag_configure(eydamedia, background='#ff6464')
                    self.tree.tag_bind(eydamedia, '<Double-1>', self.eydaMedia)
                    seinast+=1
                eyda = "eyda"+str(rest[x][0])
                self.tree.insert(rest[x][0], seinast+1, text='Eyða', tags=(eyda,rest[x][0]))
                self.tree.tag_configure(eyda, background='#ff6464')
                self.tree.tag_bind(eyda, '<Double-1>', self.eydarest)
        self.tree.grid(row=1, columnspan=4, sticky='nsew')
        if self.notandinn[2]:
            baeta = ttk.Button(self.rest, text="Bæta Við Nýju Hóteli",command=lambda: self.skipta("restdb_add",self.rest))
            baeta.grid(row=3, column=0, pady=6,sticky=NW)
        tilbaka = ttk.Button(self.rest, text="Til Baka",
                             command=lambda: self.skipta("valmynd", self.rest))
        tilbaka.grid(row=3, column=3, pady=6,sticky=E)

    def restdb_add(self):
        self.rest_add = Frame(self.container)
        self.rest_add.grid(row=0,column=0,pady=50,sticky="nsew")
        Label(self.rest_add, text="Bæta Við Nýjum Veitingastaði", font=self.font_titill).grid(row=0, column=1, sticky="nsew",pady=17)
        Label(self.rest_add, text="Nafn Veitingastaðs", font=self.font_titill).grid(row=1, column=0, sticky="e")
        self.restnafn = Entry(self.rest_add, font=("Arial", 12), width=15)
        self.restnafn.grid(row=1, column=1, pady=6)
        Label(self.rest_add, text="Gerð Veitingastaðs", font=self.font_titill).grid(row=2, column=0, sticky="e")
        self.restgerd = Entry(self.rest_add, font=("Arial", 12), width=15)
        self.restgerd.grid(row=2, column=1, pady=6)
        Label(self.rest_add, text="Fjöldi Sæta", font=self.font_titill).grid(row=3, column=0, sticky="e")
        self.fjoldi = Entry(self.rest_add, font=("Arial", 12), width=15)
        self.fjoldi.grid(row=3, column=1, pady=6)
        Label(self.rest_add, text="Staðsetning", font=self.font_titill).grid(row=4, column=0, sticky="e")
        self.stad = Entry(self.rest_add, font=("Arial", 12), width=15)
        self.stad.grid(row=4, column=1, pady=6)
        Label(self.rest_add, text="Framkvæmdastjóri", font=self.font_titill).grid(row=5, column=0, sticky="e")
        self.framk = Entry(self.rest_add, font=("Arial", 12), width=15)
        self.framk.grid(row=5, column=1, pady=6)
        Label(self.rest_add, text="Vefsíða", font=self.font_titill).grid(row=6, column=0, sticky="e")
        self.vefsida = Entry(self.rest_add, font=("Arial", 12), width=15)
        self.vefsida.grid(row=6, column=1, pady=6)
        Label(self.rest_add, text="Símanúmer", font=self.font_titill).grid(row=7, column=0, sticky="e")
        self.simanumer = Entry(self.rest_add, font=("Arial", 12), width=15)
        self.simanumer.grid(row=7, column=1, pady=6)
        Label(self.rest_add, text="Póstnúmer", font=self.font_titill).grid(row=8, column=0, sticky="e")
        self.postnumer = Entry(self.rest_add, font=("Arial", 12), width=15)
        self.postnumer.grid(row=8, column=1, pady=6)
        self.valid = IntVar(value=0)
        coord = Checkbutton(self.rest_add, text="Skrá coordinates fyrir veitingastaðinn", variable=self.valid, onvalue=1, offvalue=0, width=30, command=lambda:self.synaCoord())
        coord.grid(row=9, column=1, pady=6)
        self.latitudeL = Label(self.rest_add, text="Latitude", font=self.font_titill)
        self.latitudeL.grid(row=10, column=0, sticky="e")
        self.latitudeL.grid_remove()
        self.latitude = Entry(self.rest_add, font=("Arial", 12), width=15)
        self.latitude.grid(row=10, column=1, pady=6)
        self.latitude.grid_remove()
        self.longitudeL = Label(self.rest_add, text="Longitude", font=self.font_titill)
        self.longitudeL.grid(row=11, column=0, sticky="e")
        self.longitudeL.grid_remove()
        self.longitude = Entry(self.rest_add, font=("Arial", 12), width=15)
        self.longitude.grid(row=11, column=1, pady=6)
        self.longitude.grid_remove()
        tilbaka = ttk.Button(self.rest_add, text="Bæta Við",
                             command=lambda: self.baetaVidrest())
        tilbaka.grid(row=12, column=1, pady=6, sticky="S")
        tilbaka = ttk.Button(self.rest_add, text="Til Baka",
                             command=lambda: self.skipta("restdb", self.rest_add))
        tilbaka.grid(row=12, column=2, pady=6, sticky=N)
        self.þarf = Label(self.rest_add, text="", font="arial 10",fg="red")
        self.þarf.grid(row=13, column=1)

    def restdb_social_add(self):
        rt = RestaurantDB()
        socialmedia = rt.get_restaurant_social_list()
        self.rest_social_add = Frame(self.container)
        self.rest_social_add.grid(row=0,column=0,pady=50,sticky="nsew")
        Label(self.rest_social_add, text="Bæta Við SocialMedia Fyrir Veitingastað", font=self.font_titill).grid(row=0, column=1, sticky="nsew",pady=17)
        Label(self.rest_social_add, text="Veldu Media", font=self.font_titill).grid(row=1, column=0, sticky="e")
        self.social = StringVar()
        values = []
        for x in socialmedia:
            values.append(x[1])
        self.dropdown = ttk.Combobox(self.rest_social_add, textvariable=self.social, values=values, state="readonly")
        self.dropdown.grid(row=1, column=1, pady=6)
        Label(self.rest_social_add, text="Media URL", font=self.font_titill).grid(row=2, column=0, sticky="e")
        self.socialurl = Entry(self.rest_social_add, font=("Arial", 12), width=15)
        self.socialurl.grid(row=2, column=1, pady=6)
        tilbaka = ttk.Button(self.rest_social_add, text="Bæta Við",
                             command=lambda: self.baetaVidSocial())
        tilbaka.grid(row=3, column=1, pady=6, sticky="S")
        tilbaka = ttk.Button(self.rest_social_add, text="Til Baka",
                             command=lambda: self.skipta("restdb", self.rest_social_add))
        tilbaka.grid(row=3, column=2, pady=6, sticky=N)
        self.þarf = Label(self.rest_social_add, text="", font="arial 10",fg="red")
        self.þarf.grid(row=4, column=1)

    def restdb_social_eyda(self):
        rt = RestaurantDB()
        socialmedia = rt.get_restaurant_media_list(self.restID)
        self.rest_social_eyda = Frame(self.container)
        self.rest_social_eyda.grid(row=0,column=0,pady=50,sticky="nsew")
        Label(self.rest_social_eyda, text="Eyða SocialMedia Hjá Veitingastaði", font=self.font_titill).grid(row=0, column=1, sticky="nsew",pady=17)
        Label(self.rest_social_eyda, text="Veldu Media", font=self.font_titill).grid(row=1, column=0, sticky="e")
        self.social = StringVar()
        values = []
        for x in socialmedia:
            values.append(x[1]+": "+x[2])
        self.dropdown = ttk.Combobox(self.rest_social_eyda, textvariable=self.social, values=values, state="readonly", width=50)
        self.dropdown.grid(row=1, column=1, pady=10)
        tilbaka = ttk.Button(self.rest_social_eyda, text="Eyða",
                             command=lambda: self.eydaSocial())
        tilbaka.grid(row=2, column=1, pady=6, sticky="S")
        tilbaka = ttk.Button(self.rest_social_eyda, text="Til Baka",
                             command=lambda: self.skipta("restdb", self.rest_social_eyda))
        tilbaka.grid(row=2, column=2, pady=6, sticky=N)
        self.þarf = Label(self.rest_social_eyda, text="", font="arial 10",fg="red")
        self.þarf.grid(row=3, column=1)

    def restdb_update(self):
        self.rest_update = Frame(self.container)
        self.rest_update.grid(row=0, column=0, pady=50, sticky="nsew")
        Label(self.rest_update, text="Uppfæra Veitingastað", font=self.font_titill).grid(row=0, column=1,
                                                                                        sticky="nsew", pady=17)
        Label(self.rest_update, text="Nafn Veitingastaðs", font=self.font_titill).grid(row=1, column=0, sticky="e")
        self.restnafn = Entry(self.rest_update, font=("Arial", 12), width=15)
        self.restnafn.grid(row=1, column=1, pady=6)
        self.restnafn.insert(0, str(self.restInfo[0]))
        Label(self.rest_update, text="Gerð Veitingastaðs", font=self.font_titill).grid(row=2, column=0, sticky="e")
        self.restgerd = Entry(self.rest_update, font=("Arial", 12), width=15)
        self.restgerd.grid(row=2, column=1, pady=6)
        self.restgerd.insert(0, str(self.restInfo[4]))
        Label(self.rest_update, text="Fjöldi Sæta", font=self.font_titill).grid(row=3, column=0, sticky="e")
        self.fjoldi = Entry(self.rest_update, font=("Arial", 12), width=15)
        self.fjoldi.grid(row=3, column=1, pady=6)
        self.fjoldi.insert(0, str(self.restInfo[5]))
        Label(self.rest_update, text="Staðsetning", font=self.font_titill).grid(row=4, column=0, sticky="e")
        self.stad = Entry(self.rest_update, font=("Arial", 12), width=15)
        self.stad.grid(row=4, column=1, pady=6)
        self.stad.insert(0, str(self.restInfo[1]))
        Label(self.rest_update, text="Framkvæmdastjóri", font=self.font_titill).grid(row=5, column=0, sticky="e")
        self.framk = Entry(self.rest_update, font=("Arial", 12), width=15)
        self.framk.grid(row=5, column=1, pady=6)
        self.framk.insert(0, str(self.restInfo[8]))
        Label(self.rest_update, text="Vefsíða", font=self.font_titill).grid(row=6, column=0, sticky="e")
        self.vefsida = Entry(self.rest_update, font=("Arial", 12), width=15)
        self.vefsida.grid(row=6, column=1, pady=6)
        self.vefsida.insert(0, str(self.restInfo[7]))
        Label(self.rest_update, text="Símanúmer", font=self.font_titill).grid(row=7, column=0, sticky="e")
        self.simanumer = Entry(self.rest_update, font=("Arial", 12), width=15)
        self.simanumer.grid(row=7, column=1, pady=6)
        self.simanumer.insert(0, str(self.restInfo[6]))
        Label(self.rest_update, text="Póstnúmer", font=self.font_titill).grid(row=8, column=0, sticky="e")
        self.postnumer = Entry(self.rest_update, font=("Arial", 12), width=15)
        self.postnumer.grid(row=8, column=1, pady=6)
        self.postnumer.insert(0, str(self.restInfo[2]))
        self.valid2 = IntVar(value=0)
        coord = Checkbutton(self.rest_update, text="Uppfæra coordinatesID", variable=self.valid2, onvalue=1,
                            offvalue=0, width=20, command=lambda: self.synaCoordID())
        coord.grid(row=9, column=1, pady=6)
        self.coordIDL = Label(self.rest_update, text="CoordID", font=self.font_titill)
        self.coordIDL.grid(row=10, column=0, sticky="e")
        self.coordIDL.grid_remove()
        self.coordID = Entry(self.rest_update, font=("Arial", 12), width=15)
        self.coordID.grid(row=10, column=1, pady=6)
        self.coordID.grid_remove()
        tilbaka = ttk.Button(self.rest_update, text="Uppfæra",
                             command=lambda: self.uppfaerarest())
        tilbaka.grid(row=11, column=1, pady=6, sticky="S")
        tilbaka = ttk.Button(self.rest_update, text="Til Baka",
                             command=lambda: self.skipta("restdb", self.rest_update))
        tilbaka.grid(row=11, column=2, pady=6, sticky=N)
        self.þarf = Label(self.rest_update, text="", font="arial 10", fg="red")
        self.þarf.grid(row=12, column=1)

    def synaCoord(self):
        if self.valid.get():
            self.latitudeL.grid()
            self.latitude.grid()
            self.longitudeL.grid()
            self.longitude.grid()
        else:
            self.latitudeL.grid_remove()
            self.latitude.grid_remove()
            self.longitudeL.grid_remove()
            self.longitude.grid_remove()

    def synaCoordID(self):
        if self.valid2.get():
            self.coordIDL.grid()
            self.coordID.grid()
        else:
            self.coordIDL.grid_remove()
            self.coordID.grid_remove()

    def baetaVidrest(self):
        rt = RestaurantDB()
        restnafn = self.restnafn.get()
        gerd = self.restgerd.get()
        fjoldi = self.fjoldi.get()
        stad = self.stad.get()
        framk = self.framk.get()
        vefsida = self.vefsida.get()
        simanumer = self.simanumer.get()
        postnumer = self.postnumer.get()
        valid = self.valid.get()
        lat = self.latitude.get()
        long = self.longitude.get()
        if restnafn == "" or postnumer == "":
            self.þarf.config(text="Fylltu inn í Nafn Veitingastaðs og Póstnúmer")
        else:
            if valid and (lat != "" or long != ""):
                rt.add_restaurant(restnafn,gerd,fjoldi,stad,framk,vefsida,simanumer,postnumer,lat,long)
            else:
                rt.add_restaurant(restnafn,gerd,fjoldi,stad,framk,vefsida,simanumer,postnumer)
            self.þarf.config(text="")
            self.restnafn.delete(0, END)
            self.restgerd.delete(0, END)
            self.fjoldi.delete(0, END)
            self.stad.delete(0, END)
            self.framk.delete(0, END)
            self.vefsida.delete(0, END)
            self.simanumer.delete(0, END)
            self.postnumer.delete(0, END)
            self.latitude.delete(0, END)
            self.longitude.delete(0, END)
            self.valid.set(1)
            self.synaCoord()
            self.skipta("restdb",self.rest_add)

    def uppfaerarest(self):
        rt = RestaurantDB()
        restnafn = self.restnafn.get()
        gerd = self.restgerd.get()
        fjoldi = self.fjoldi.get()
        stad = self.stad.get()
        framk = self.framk.get()
        vefsida = self.vefsida.get()
        simanumer = self.simanumer.get()
        postnumer = self.postnumer.get()
        valid2 = self.valid2.get()
        coordID = self.coordID.get()
        if restnafn == "" or postnumer == "":
            self.þarf.config(text="Fylltu inn í Nafn Veitingastaðs og Póstnúmer")
        else:
            if valid2 and coordID != "":
                rt.update_restaurant(self.restID,restnafn,gerd,fjoldi,stad,framk,vefsida,simanumer,postnumer,coordID)
            else:
                rt.update_restaurant(self.restID,restnafn,gerd,fjoldi,stad,framk,vefsida,simanumer,postnumer)
            self.þarf.config(text="")
            self.valid2.set(1)
            self.synaCoordID()
            self.skipta("restdb",self.rest_update)

    def uppfaeraht(self,event):
        rt = RestaurantDB()
        focus = self.tree.focus()
        item = self.tree.item(focus)
        self.restID = item['tags'][1]
        self.restInfo = rt.get_restaurant(self.restID)
        self.skipta("restdb_update",self.rest)

    def baetaSocial(self,event):
        focus = self.tree.focus()
        item = self.tree.item(focus)
        self.restID = item['tags'][1]
        self.skipta("restdb_social_add",self.rest)

    def baetaVidSocial(self):
        media = self.social.get()
        mediaurl = self.socialurl.get()
        if mediaurl == "" or media == "":
            self.þarf.config(text="Veldu Media og fylltu inn í Media URL")
        else:
            rt = RestaurantDB()
            socialmedia = rt.get_restaurant_social_list()
            mediaID = ""
            for x in socialmedia:
                if x[1] == media:
                    mediaID = x[0]
            rt.add_restaurant_media(self.restID,mediaID,mediaurl)
            self.þarf.config(text="")
            self.dropdown.delete(0, END)
            self.socialurl.delete(0, END)
            self.skipta("restdb",self.rest_social_add)

    def eydarest(self,event):
        focus = self.tree.focus()
        item = self.tree.item(focus)
        rt = RestaurantDB()
        rt.delete_restaurant(item['tags'][1])
        self.rest.grid_remove()
        self.restdb()

    def eydaMedia(self,event):
        focus = self.tree.focus()
        item = self.tree.item(focus)
        self.restID = item['tags'][1]
        self.skipta("restdb_social_eyda",self.rest)

    def eydaSocial(self):
        media = self.social.get()
        if media == "":
            self.þarf.config(text="Veldu Media til að eyða")
        else:
            rt = RestaurantDB()
            socialmedia = rt.get_restaurant_media_list(self.restID)
            mediaID = ""
            for x in socialmedia:
                texti = x[1]+": "+x[2]
                if texti == media:
                    mediaID = x[3]
            rt.remove_restaurant_media(self.restID,mediaID)
            self.þarf.config(text="")
            self.dropdown.delete(0, END)
            self.skipta("restdb",self.rest_social_eyda)
