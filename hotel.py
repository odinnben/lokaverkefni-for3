'''-----------------------------------------------

                    HotelDB
            Óðinn B og Matthías Ólafur

-----------------------------------------------'''
from tkinter import *
from tkinter import ttk
from tkinter import font as tkfont
from notendur import *
from iceconnect import *

class hotel:

    def __init__(self,container,font_titill,notandinn):
        self.container = container
        self.font_titill = font_titill
        self.notandinn = notandinn

    def skipta(self,til,fra):
        if til == "valmynd":
            from valmynd import val
            val(self.container,self.font_titill,self.notandinn).valmynd()
        elif til == "hoteldb":
            self.hoteldb()
        elif til == "hoteldb_add":
            self.hoteldb_add()
        elif til == "hoteldb_social_add":
            self.hoteldb_social_add()
        elif til == "hoteldb_social_eyda":
            self.hoteldb_social_eyda()
        elif til == "hoteldb_update":
            self.hoteldb_update()
        fra.grid_remove()

    def hoteldb(self):
        self.hotel = Frame(self.container)
        self.hotel.grid(row=0,column=0,pady=50,sticky="nsew")
        Label(self.hotel, text="HótelDB  Hótel", font=self.font_titill).grid(row=0,column=0,sticky="w",pady=17)
        texti = "| Notandi | "+self.notandinn[0]+" | "
        if self.notandinn[2]:
            texti += " Admin Réttindi |"
        else:
            texti += " Venjuleg Réttindi |"
        Label(self.hotel, text=texti, font="Arial 13").grid(row=0,column=3,sticky="e",pady=17)

        self.tree = ttk.Treeview(self.hotel, columns=('Hotel','Staðsetning','Postnumer','Borg','Vefsida'),height=20)
        self.tree.heading('#0', text='HótelID')
        self.tree.heading('#1', text='Hótel')
        self.tree.heading('#2', text='Staðsetning')
        self.tree.heading('#3', text='Póstnúmer')
        self.tree.heading('#4', text='Borg')
        self.tree.heading('#5', text='Vefsíða')
        self.tree.column("#0",width=160)
        self.tree.column("#1",width=300)
        self.tree.column("#2",width=160)
        self.tree.column("#3",width=100)
        self.tree.column("#4",width=100)
        self.tree.column("#5",width=200)
        ht = HotelDB()
        hotel = ht.get_hotel_list()
        hotel.sort()
        for x in range(len(hotel)):
            self.tree.insert("", x, hotel[x][0], text=hotel[x][0],values=(hotel[x][1],hotel[x][2],hotel[x][3],hotel[x][4],hotel[x][5]))
            nanar = ht.get_hotel(hotel[x][0])
            if nanar[9] != None and nanar[10] != None:
                self.tree.insert(hotel[x][0], 1, text='- Hverfi -',values=str(nanar[2]))
                self.tree.insert(hotel[x][0], 2, text='- Framkvæmdastjóri -',values=(str(nanar[6]),"","","",""))
                self.tree.insert(hotel[x][0], 3, text='- Netfang -',values=str(nanar[7]))
                self.tree.insert(hotel[x][0], 4, text='- Símanúmer -',values=str(nanar[8]))
                self.tree.insert(hotel[x][0], 5, text='- Latitude -',values=str(nanar[9]))
                self.tree.insert(hotel[x][0], 6, text='- Longitude -',values=str(nanar[10]))
                seinast = 5
            else:
                self.tree.insert(hotel[x][0], 1, text='- Hverfi -',values=str(nanar[2]))
                self.tree.insert(hotel[x][0], 2, text='- Framkvæmdastjóri -',values=(str(nanar[6]),"","","",""))
                self.tree.insert(hotel[x][0], 3, text='- Netfang -',values=str(nanar[7]))
                self.tree.insert(hotel[x][0], 4, text='- Símanúmer -',values=str(nanar[8]))
                seinast = 3
            social = ht.get_hotel_media_list(hotel[x][0])
            if len(social) > 0:
                for i in range(len(social)):
                    self.tree.insert(hotel[x][0],seinast+i+1, text='- '+social[i][1]+' -',values=(social[i][2]))
                seinast = len(social)+1+seinast
            else:
                self.tree.insert(hotel[x][0], seinast+1, text='')
                seinast += 1
            self.tree.insert(hotel[x][0], 0, text='')
            self.tree.insert(hotel[x][0], seinast+1, text='')
            seinast+=1
            if self.notandinn[2]:
                upp = "upp"+str(hotel[x][0])
                self.tree.insert(hotel[x][0], seinast+1, text='Uppfæra', tags=(upp,hotel[x][0]))
                self.tree.tag_configure(upp, background='cyan')
                self.tree.tag_bind(upp, '<Double-1>', self.uppfaeraht)
                baetasocial = "social"+str(hotel[x][0])
                self.tree.insert(hotel[x][0], seinast+2, text='Bæta Við Socialmedia', tags=(baetasocial,hotel[x][0]))
                self.tree.tag_configure(baetasocial, background='orange')
                self.tree.tag_bind(baetasocial, '<Double-1>', self.baetaSocialhotel)
                seinast += 2
                if len(ht.get_hotel_media_list(hotel[x][0])) > 0:
                    eydaMedia = "eydaMedia"+str(hotel[x][0])
                    self.tree.insert(hotel[x][0], seinast+1, text='Eyða Socialmedia', tags=(eydaMedia,hotel[x][0]))
                    self.tree.tag_configure(eydaMedia, background='#ff6464')
                    self.tree.tag_bind(eydaMedia, '<Double-1>', self.eydaMedia)
                    seinast+=1
                eyda = "eyda"+str(hotel[x][0])
                self.tree.insert(hotel[x][0], seinast+1, text='Eyða', tags=(eyda,hotel[x][0]))
                self.tree.tag_configure(eyda, background='#ff6464')
                self.tree.tag_bind(eyda, '<Double-1>', self.eydahotel)
        self.tree.grid(row=1, columnspan=4, sticky='nsew')
        if self.notandinn[2]:
            baeta = ttk.Button(self.hotel, text="Bæta Við Nýju Hóteli",command=lambda: self.skipta("hoteldb_add",self.hotel))
            baeta.grid(row=3, column=0, pady=6,sticky=NW)
        tilbaka = ttk.Button(self.hotel, text="Til Baka",
                             command=lambda: self.skipta("valmynd", self.hotel))
        tilbaka.grid(row=3, column=3, pady=6,sticky=E)

    def hoteldb_add(self):
        self.hotel_add = Frame(self.container)
        self.hotel_add.grid(row=0,column=0,pady=50,sticky="nsew")
        Label(self.hotel_add, text="Bæta Við Nýju Hóteli", font=self.font_titill).grid(row=0, column=1, sticky="nsew",pady=17)
        Label(self.hotel_add, text="Hótel Nafn", font=self.font_titill).grid(row=1, column=0, sticky="e")
        self.hotelnafn = Entry(self.hotel_add, font=("Arial", 12), width=15)
        self.hotelnafn.grid(row=1, column=1, pady=6)
        Label(self.hotel_add, text="Staðsetning", font=self.font_titill).grid(row=2, column=0, sticky="e")
        self.stadsetning = Entry(self.hotel_add, font=("Arial", 12), width=15)
        self.stadsetning.grid(row=2, column=1, pady=6)
        Label(self.hotel_add, text="Framkvæmdastjóri", font=self.font_titill).grid(row=3, column=0, sticky="e")
        self.framk = Entry(self.hotel_add, font=("Arial", 12), width=15)
        self.framk.grid(row=3, column=1, pady=6)
        Label(self.hotel_add, text="Vefsíða", font=self.font_titill).grid(row=4, column=0, sticky="e")
        self.vefsida = Entry(self.hotel_add, font=("Arial", 12), width=15)
        self.vefsida.grid(row=4, column=1, pady=6)
        Label(self.hotel_add, text="Netfang", font=self.font_titill).grid(row=5, column=0, sticky="e")
        self.netfang = Entry(self.hotel_add, font=("Arial", 12), width=15)
        self.netfang.grid(row=5, column=1, pady=6)
        Label(self.hotel_add, text="Símanúmer", font=self.font_titill).grid(row=6, column=0, sticky="e")
        self.simanumer = Entry(self.hotel_add, font=("Arial", 12), width=15)
        self.simanumer.grid(row=6, column=1, pady=6)
        Label(self.hotel_add, text="Póstnúmer", font=self.font_titill).grid(row=7, column=0, sticky="e")
        self.postnumer = Entry(self.hotel_add, font=("Arial", 12), width=15)
        self.postnumer.grid(row=7, column=1, pady=6)
        self.valid = IntVar(value=0)
        coord = Checkbutton(self.hotel_add, text="Skrá coordinates fyrir hótelið", variable=self.valid, onvalue=1, offvalue=0, width=20, command=lambda:self.synaCoord())
        coord.grid(row=8, column=1, pady=6)
        self.latitudeL = Label(self.hotel_add, text="Latitude", font=self.font_titill)
        self.latitudeL.grid(row=9, column=0, sticky="e")
        self.latitudeL.grid_remove()
        self.latitude = Entry(self.hotel_add, font=("Arial", 12), width=15)
        self.latitude.grid(row=9, column=1, pady=6)
        self.latitude.grid_remove()
        self.longitudeL = Label(self.hotel_add, text="Longitude", font=self.font_titill)
        self.longitudeL.grid(row=10, column=0, sticky="e")
        self.longitudeL.grid_remove()
        self.longitude = Entry(self.hotel_add, font=("Arial", 12), width=15)
        self.longitude.grid(row=10, column=1, pady=6)
        self.longitude.grid_remove()
        tilbaka = ttk.Button(self.hotel_add, text="Bæta Við",
                             command=lambda: self.baetaVidhotel())
        tilbaka.grid(row=11, column=1, pady=6, sticky="S")
        tilbaka = ttk.Button(self.hotel_add, text="Til Baka",
                             command=lambda: self.skipta("hoteldb", self.hotel_add))
        tilbaka.grid(row=11, column=2, pady=6, sticky=N)
        self.þarf = Label(self.hotel_add, text="", font="arial 10",fg="red")
        self.þarf.grid(row=12, column=1)

    def hoteldb_social_add(self):
        ht = HotelDB()
        socialmedia = ht.get_hotel_social_list()
        self.hotel_social_add = Frame(self.container)
        self.hotel_social_add.grid(row=0,column=0,pady=50,sticky="nsew")
        Label(self.hotel_social_add, text="Bæta Við SocialMedia Fyrir Hótel", font=self.font_titill).grid(row=0, column=1, sticky="nsew",pady=17)
        Label(self.hotel_social_add, text="Veldu Media", font=self.font_titill).grid(row=1, column=0, sticky="e")
        self.social = StringVar()
        values = []
        for x in socialmedia:
            values.append(x[1])
        self.dropdown = ttk.Combobox(self.hotel_social_add, textvariable=self.social, values=values, state="readonly")
        self.dropdown.grid(row=1, column=1, pady=6)
        Label(self.hotel_social_add, text="Media URL", font=self.font_titill).grid(row=2, column=0, sticky="e")
        self.socialurl = Entry(self.hotel_social_add, font=("Arial", 12), width=15)
        self.socialurl.grid(row=2, column=1, pady=6)
        tilbaka = ttk.Button(self.hotel_social_add, text="Bæta Við",
                             command=lambda: self.baetaVidSocial())
        tilbaka.grid(row=3, column=1, pady=6, sticky="S")
        tilbaka = ttk.Button(self.hotel_social_add, text="Til Baka",
                             command=lambda: self.skipta("hoteldb", self.hotel_social_add))
        tilbaka.grid(row=3, column=2, pady=6, sticky=N)
        self.þarf = Label(self.hotel_social_add, text="", font="arial 10",fg="red")
        self.þarf.grid(row=4, column=1)

    def hoteldb_social_eyda(self):
        ht = HotelDB()
        socialmedia = ht.get_hotel_media_list(self.hotelID)
        self.hotel_social_eyda = Frame(self.container)
        self.hotel_social_eyda.grid(row=0,column=0,pady=50,sticky="nsew")
        Label(self.hotel_social_eyda, text="Eyða SocialMedia Hjá Hóteli", font=self.font_titill).grid(row=0, column=1, sticky="nsew",pady=17)
        Label(self.hotel_social_eyda, text="Veldu Media", font=self.font_titill).grid(row=1, column=0, sticky="e")
        self.social = StringVar()
        values = []
        for x in socialmedia:
            values.append(x[1]+": "+x[2])
        self.dropdown = ttk.Combobox(self.hotel_social_eyda, textvariable=self.social, values=values, state="readonly", width=50)
        self.dropdown.grid(row=1, column=1, pady=10)
        tilbaka = ttk.Button(self.hotel_social_eyda, text="Eyða",
                             command=lambda: self.eydaSoial())
        tilbaka.grid(row=2, column=1, pady=6, sticky="S")
        tilbaka = ttk.Button(self.hotel_social_eyda, text="Til Baka",
                             command=lambda: self.skipta("hoteldb", self.hotel_social_eyda))
        tilbaka.grid(row=2, column=2, pady=6, sticky=N)
        self.þarf = Label(self.hotel_social_eyda, text="", font="arial 10",fg="red")
        self.þarf.grid(row=3, column=1)

    def hoteldb_update(self):
        self.hotel_update = Frame(self.container)
        self.hotel_update.grid(row=0, column=0, pady=50, sticky="nsew")
        Label(self.hotel_update, text="Uppfæra Hótel", font=self.font_titill).grid(row=0, column=1,
                                                                                        sticky="nsew", pady=17)
        Label(self.hotel_update, text="Hótel Nafn", font=self.font_titill).grid(row=1, column=0, sticky="e")
        self.hotelnafn = Entry(self.hotel_update, font=("Arial", 12), width=15)
        self.hotelnafn.insert(0, str(self.hotelInfo[0]))
        self.hotelnafn.grid(row=1, column=1, pady=6)
        Label(self.hotel_update, text="Staðsetning", font=self.font_titill).grid(row=2, column=0, sticky="e")
        self.stadsetning = Entry(self.hotel_update, font=("Arial", 12), width=15)
        self.stadsetning.grid(row=2, column=1, pady=6)
        self.stadsetning.insert(0, str(self.hotelInfo[1]))
        Label(self.hotel_update, text="Framkvæmdastjóri", font=self.font_titill).grid(row=3, column=0, sticky="e")
        self.framk = Entry(self.hotel_update, font=("Arial", 12), width=15)
        self.framk.grid(row=3, column=1, pady=6)
        self.framk.insert(0, str(self.hotelInfo[6]))
        Label(self.hotel_update, text="Vefsíða", font=self.font_titill).grid(row=4, column=0, sticky="e")
        self.vefsida = Entry(self.hotel_update, font=("Arial", 12), width=15)
        self.vefsida.grid(row=4, column=1, pady=6)
        self.vefsida.insert(0, str(self.hotelInfo[5]))
        Label(self.hotel_update, text="Netfang", font=self.font_titill).grid(row=5, column=0, sticky="e")
        self.netfang = Entry(self.hotel_update, font=("Arial", 12), width=15)
        self.netfang.grid(row=5, column=1, pady=6)
        self.netfang.insert(0, str(self.hotelInfo[7]))
        Label(self.hotel_update, text="Símanúmer", font=self.font_titill).grid(row=6, column=0, sticky="e")
        self.simanumer = Entry(self.hotel_update, font=("Arial", 12), width=15)
        self.simanumer.grid(row=6, column=1, pady=6)
        self.simanumer.insert(0, str(self.hotelInfo[8]))
        Label(self.hotel_update, text="Póstnúmer", font=self.font_titill).grid(row=7, column=0, sticky="e")
        self.postnumer = Entry(self.hotel_update, font=("Arial", 12), width=15)
        self.postnumer.grid(row=7, column=1, pady=6)
        self.postnumer.insert(0, str(self.hotelInfo[3]))
        self.valid2 = IntVar(value=0)
        coord = Checkbutton(self.hotel_update, text="Uppfæra coordinatesID", variable=self.valid2, onvalue=1,
                            offvalue=0, width=20, command=lambda: self.synaCoordID())
        coord.grid(row=8, column=1, pady=6)
        self.coordIDL = Label(self.hotel_update, text="CoordID", font=self.font_titill)
        self.coordIDL.grid(row=9, column=0, sticky="e")
        self.coordIDL.grid_remove()
        self.coordID = Entry(self.hotel_update, font=("Arial", 12), width=15)
        self.coordID.grid(row=9, column=1, pady=6)
        self.coordID.grid_remove()
        tilbaka = ttk.Button(self.hotel_update, text="Uppfæra",
                             command=lambda: self.uppfaerahotel())
        tilbaka.grid(row=10, column=1, pady=6, sticky="S")
        tilbaka = ttk.Button(self.hotel_update, text="Til Baka",
                             command=lambda: self.skipta("hoteldb", self.hotel_update))
        tilbaka.grid(row=10, column=2, pady=6, sticky=N)
        self.þarf = Label(self.hotel_update, text="", font="arial 10", fg="red")
        self.þarf.grid(row=11, column=1)

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

    def baetaVidhotel(self):
        ht = HotelDB()
        hotelnafn = self.hotelnafn.get()
        stad = self.stadsetning.get()
        framk = self.framk.get()
        vefsida = self.vefsida.get()
        netfang = self.netfang.get()
        simanumer = self.simanumer.get()
        postnumer = self.postnumer.get()
        valid = self.valid.get()
        lat = self.latitude.get()
        long = self.longitude.get()
        if hotelnafn == "" or postnumer == "":
            self.þarf.config(text="Fylltu inn í Hótelnafn og Póstnúmer")
        else:
            if valid and (lat != "" or long != ""):
                ht.add_hotel(hotelnafn,stad,framk,vefsida,netfang,simanumer,postnumer,lat,long)
            else:
                ht.add_hotel(hotelnafn,stad,framk,vefsida,netfang,simanumer,postnumer)
            self.þarf.config(text="")
            self.hotelnafn.delete(0, END)
            self.stadsetning.delete(0, END)
            self.framk.delete(0, END)
            self.vefsida.delete(0, END)
            self.netfang.delete(0, END)
            self.simanumer.delete(0, END)
            self.postnumer.delete(0, END)
            self.latitude.delete(0, END)
            self.longitude.delete(0, END)
            self.valid.set(1)
            self.synaCoord()
            self.skipta("hoteldb",self.hotel_add)

    def uppfaerahotel(self):
        ht = HotelDB()
        hotelnafn = self.hotelnafn.get()
        stad = self.stadsetning.get()
        framk = self.framk.get()
        vefsida = self.vefsida.get()
        netfang = self.netfang.get()
        simanumer = self.simanumer.get()
        postnumer = self.postnumer.get()
        valid2 = self.valid2.get()
        coordID = self.coordID.get()
        if hotelnafn == "" or postnumer == "":
            self.þarf.config(text="Fylltu inn í Hótelnafn og Póstnúmer")
        else:
            if valid2 and coordID != "":
                ht.update_hotel(self.hotelID,hotelnafn,stad,framk,vefsida,netfang,simanumer,postnumer,coordID)
            else:
                ht.update_hotel(self.hotelID,hotelnafn,stad,framk,vefsida,netfang,simanumer,postnumer)
            self.þarf.config(text="")
            self.valid2.set(1)
            self.synaCoordID()
            self.skipta("hoteldb",self.hotel_update)

    def uppfaeraht(self,event):
        ht = HotelDB()
        focus = self.tree.focus()
        item = self.tree.item(focus)
        self.hotelID = item['tags'][1]
        self.hotelInfo = ht.get_hotel(self.hotelID)
        self.skipta("hoteldb_update",self.hotel)

    def baetaSocialhotel(self,event):
        focus = self.tree.focus()
        item = self.tree.item(focus)
        self.hotelID = item['tags'][1]
        self.skipta("hoteldb_social_add",self.hotel)

    def baetaVidSocial(self):
        media = self.social.get()
        mediaurl = self.socialurl.get()
        if mediaurl == "" or media == "":
            self.þarf.config(text="Veldu Media og fylltu inn í Media URL")
        else:
            ht = HotelDB()
            socialmedia = ht.get_hotel_social_list()
            mediaID = ""
            for x in socialmedia:
                if x[1] == media:
                    mediaID = x[0]
            ht.add_hotel_media(self.hotelID,mediaID,mediaurl)
            self.þarf.config(text="")
            self.dropdown.delete(0, END)
            self.socialurl.delete(0, END)
            self.skipta("hoteldb",self.hotel_social_add)

    def eydahotel(self,event):
        focus = self.tree.focus()
        item = self.tree.item(focus)
        ht = HotelDB()
        ht.delete_hotel(item['tags'][1])
        self.hotel.grid_remove()
        self.hoteldb()

    def eydaMedia(self,event):
        focus = self.tree.focus()
        item = self.tree.item(focus)
        self.hotelID = item['tags'][1]
        self.skipta("hoteldb_social_eyda",self.hotel)

    def eydaSoial(self):
        media = self.social.get()
        if media == "":
            self.þarf.config(text="Veldu Media til að eyða")
        else:
            ht = HotelDB()
            socialmedia = ht.get_hotel_media_list(self.hotelID)
            mediaID = ""
            for x in socialmedia:
                texti = x[1]+": "+x[2]
                if texti == media:
                    mediaID = x[3]
            ht.remove_hotel_media(self.hotelID,mediaID)
            self.þarf.config(text="")
            self.dropdown.delete(0, END)
            self.skipta("hoteldb",self.hotel_social_eyda)
