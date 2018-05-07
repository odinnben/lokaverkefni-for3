'''-----------------------------------------------

                    PlaceDB
            Óðinn B og Matthías Ólafur

-----------------------------------------------'''
from tkinter import *
from tkinter import ttk
from tkinter import font as tkfont
from notendur import *
from iceconnect import *

class place:

    def __init__(self,container,font_titill,notandinn):
        self.container = container
        self.font_titill = font_titill
        self.notandinn = notandinn

    def skiptaPlace(self,til,fra):
        if til == "valmynd":
            from valmynd import val
            val(self.container,self.font_titill,self.notandinn).valmynd()
        elif til == "placedb":
            self.placedb()
        elif til == "placedb_add":
            self.placedb_add()
        elif til == "placedb_update":
            self.placedb_update()
        fra.grid_remove()

    def placedb(self):
        self.place = Frame(self.container)
        self.place.grid(row=0,column=0,pady=50,sticky="nsew")
        Label(self.place, text="PlaceDB  Staðir", font=self.font_titill).grid(row=0,column=0,sticky="w",pady=17)
        texti = "| Notandi | "+self.notandinn[0]+" | "
        if self.notandinn[2]:
            texti += " Admin Réttindi |"
        else:
            texti += " Venjuleg Réttindi |"
        Label(self.place, text=texti, font="Arial 13").grid(row=0,column=3,sticky="e",pady=17)

        self.tree = ttk.Treeview(self.place, columns=('Borg','Svæði','Vefsíða'),height=20)
        self.tree.heading('#0', text='PlaceID')
        self.tree.heading('#1', text='Borg')
        self.tree.heading('#2', text='Svæði')
        self.tree.heading('#3', text='Vefsíða')
        pd = PlaceDB()
        stadir = pd.get_place_list()
        stadir.sort()
        for x in range(len(stadir)):
            self.tree.insert("", x, stadir[x][0], text=stadir[x][0],values=(stadir[x][1],stadir[x][2],stadir[x][3]))
            nanar = pd.get_place(stadir[x][0])
            if nanar[4] != None and nanar[5] != None:
                self.tree.insert(stadir[x][0], 1, text='- Nánari -',values=("Íbúafjöldi","Latitude","Longitude"))
                self.tree.insert(stadir[x][0], 2, text='- Íbúafjöldi -',values=(nanar[2]))
                self.tree.insert(stadir[x][0], 3, text='- Latitude -',values=(nanar[4]))
                self.tree.insert(stadir[x][0], 4, text='- Longitude -',values=(nanar[5]))
                seinast = 4
            else:
                self.tree.insert(stadir[x][0], 1, text='- Íbúafjöldi -',values=(nanar[2]))
                seinast = 1
            self.tree.insert(stadir[x][0], 0, text='')
            self.tree.insert(stadir[x][0], seinast+1, text='')
            seinast+=1
            if self.notandinn[2]:
                upp = "upp"+str(stadir[x][0])
                self.tree.insert(stadir[x][0],seinast+1, text='Uppfæra', tags=(upp,stadir[x][0]))
                self.tree.tag_configure(upp, background='cyan')
                self.tree.tag_bind(upp, '<Double-1>', self.uppfaeraPl)
                eyda = "eyda"+str(stadir[x][0])
                self.tree.insert(stadir[x][0], seinast+2, text='Eyða', tags=(eyda,stadir[x][0]))
                self.tree.tag_configure(eyda, background='#ff6464')
                self.tree.tag_bind(eyda, '<Double-1>', self.eydaPlace)
        self.tree.grid(row=1, columnspan=4, sticky='nsew')
        if self.notandinn[2]:
            baeta = ttk.Button(self.place, text="Bæta Við Nýjum Stað",command=lambda: self.skiptaPlace("placedb_add",self.place))
            baeta.grid(row=3, column=0, pady=6,sticky=NW)
        tilbaka = ttk.Button(self.place, text="Til Baka",
                             command=lambda: self.skiptaPlace("valmynd", self.place))
        tilbaka.grid(row=3, column=3, pady=6,sticky=E)

    def placedb_add(self):
        self.place_add = Frame(self.container)
        self.place_add.grid(row=0,column=0,pady=50,sticky="nsew")
        Label(self.place_add, text="  Bæta Við Nýjum Stað\t", font=self.font_titill).grid(row=0, column=1, sticky="nsew",pady=17)
        Label(self.place_add, text="Borg", font=self.font_titill).grid(row=1, column=0, sticky="e")
        self.borg = Entry(self.place_add, font=("Arial", 12), width=15)
        self.borg.grid(row=1, column=1, pady=6)
        Label(self.place_add, text="Svæði", font=self.font_titill).grid(row=2, column=0, sticky="e")
        self.svaedi = Entry(self.place_add, font=("Arial", 12), width=15)
        self.svaedi.grid(row=2, column=1, pady=6)
        Label(self.place_add, text="Íbúafjöldi", font=self.font_titill).grid(row=3, column=0, sticky="e")
        self.ibuafjoldi = Entry(self.place_add, font=("Arial", 12), width=15)
        self.ibuafjoldi.grid(row=3, column=1, pady=6)
        Label(self.place_add, text="Vefsíða", font=self.font_titill).grid(row=4, column=0, sticky="e")
        self.vefsida = Entry(self.place_add, font=("Arial", 12), width=15)
        self.vefsida.grid(row=4, column=1, pady=6)
        self.valid = IntVar(value=0)
        coord = Checkbutton(self.place_add, text="Skrá coordinates fyrir stað", variable=self.valid, onvalue=1, offvalue=0, width=20, command=lambda:self.synaCoord())
        coord.grid(row=5, column=1, pady=6)
        self.latitudeL = Label(self.place_add, text="Latitude", font=self.font_titill)
        self.latitudeL.grid(row=6, column=0, sticky="e")
        self.latitudeL.grid_remove()
        self.latitude = Entry(self.place_add, font=("Arial", 12), width=15)
        self.latitude.grid(row=6, column=1, pady=6)
        self.latitude.grid_remove()
        self.longitudeL = Label(self.place_add, text="Longitude", font=self.font_titill)
        self.longitudeL.grid(row=7, column=0, sticky="e")
        self.longitudeL.grid_remove()
        self.longitude = Entry(self.place_add, font=("Arial", 12), width=15)
        self.longitude.grid(row=7, column=1, pady=6)
        self.longitude.grid_remove()
        tilbaka = ttk.Button(self.place_add, text="Bæta Við",
                             command=lambda: self.baetaVidPlace())
        tilbaka.grid(row=8, column=1, pady=6, sticky="S")
        tilbaka = ttk.Button(self.place_add, text="Til Baka",
                             command=lambda: self.skiptaPlace("placedb", self.place_add))
        tilbaka.grid(row=8, column=2, pady=6, sticky=N)
        self.þarf = Label(self.place_add, text="", font="arial 10",fg="red")
        self.þarf.grid(row=9, column=1)

    def placedb_update(self):
        self.place_update = Frame(self.container)
        self.place_update.grid(row=0, column=0, pady=50, sticky="nsew")
        Label(self.place_update, text="    Uppfæra Stað\t", font=self.font_titill).grid(row=0, column=1,
                                                                                             sticky="nsew", pady=17)
        Label(self.place_update, text="Borg", font=self.font_titill).grid(row=1, column=0, sticky="e")
        self.borg = Entry(self.place_update, font=("Arial", 12), width=15)
        self.borg.insert(0,self.placeInfo[0])
        self.borg.grid(row=1, column=1, pady=6)
        Label(self.place_update, text="Svæði", font=self.font_titill).grid(row=2, column=0, sticky="e")
        self.svaedi = Entry(self.place_update, font=("Arial", 12), width=15)
        self.svaedi.grid(row=2, column=1, pady=6)
        self.svaedi.insert(0,self.placeInfo[1])
        Label(self.place_update, text="Íbúafjöldi", font=self.font_titill).grid(row=3, column=0, sticky="e")
        self.ibuafjoldi = Entry(self.place_update, font=("Arial", 12), width=15)
        self.ibuafjoldi.grid(row=3, column=1, pady=6)
        self.ibuafjoldi.insert(0,self.placeInfo[2])
        Label(self.place_update, text="Vefsíða", font=self.font_titill).grid(row=4, column=0, sticky="e")
        self.vefsida = Entry(self.place_update, font=("Arial", 12), width=15)
        self.vefsida.grid(row=4, column=1, pady=6)
        self.vefsida.insert(0,self.placeInfo[3])
        self.valid2 = IntVar(value=0)
        coord = Checkbutton(self.place_update, text="Uppfæra coordinatesID", variable=self.valid2, onvalue=1,
                            offvalue=0, width=20, command=lambda: self.synaCoordID())
        coord.grid(row=5, column=1, pady=6)
        self.coordIDL = Label(self.place_update, text="CoordID", font=self.font_titill)
        self.coordIDL.grid(row=6, column=0, sticky="e")
        self.coordIDL.grid_remove()
        self.coordID = Entry(self.place_update, font=("Arial", 12), width=15)
        self.coordID.grid(row=6, column=1, pady=6)
        self.coordID.grid_remove()
        tilbaka = ttk.Button(self.place_update, text="Uppfæra",
                             command=lambda: self.uppfaeraPlace())
        tilbaka.grid(row=8, column=1, pady=6, sticky="S")
        tilbaka = ttk.Button(self.place_update, text="Til Baka",
                             command=lambda: self.skiptaPlace("placedb", self.place_update))
        tilbaka.grid(row=8, column=2, pady=6, sticky=N)
        self.þarf = Label(self.place_update, text="", font="arial 10", fg="red")
        self.þarf.grid(row=9, column=1)

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

    def baetaVidPlace(self):
        pd = PlaceDB()
        borg = self.borg.get()
        svaedi = self.svaedi.get()
        ibuafjoldi = self.ibuafjoldi.get()
        vefsida = self.vefsida.get()
        valid = self.valid.get()
        lat = self.latitude.get()
        long = self.longitude.get()
        if borg == "" or svaedi == "":
            self.þarf.config(text="Fylltu inn í Borg og Svæði")
        else:
            if valid and (lat != "" or long != ""):
                pd.add_place(borg,svaedi,ibuafjoldi,vefsida,lat,long)
            else:
                pd.add_place(borg,svaedi,ibuafjoldi,vefsida)
            self.þarf.config(text="")
            self.borg.delete(0, END)
            self.svaedi.delete(0, END)
            self.ibuafjoldi.delete(0, END)
            self.vefsida.delete(0, END)
            self.latitude.delete(0, END)
            self.longitude.delete(0, END)
            self.valid.set(1)
            self.synaCoord()
            self.skiptaPlace("placedb",self.place_add)

    def uppfaeraPlace(self):
        pd = PlaceDB()
        borg = self.borg.get()
        svaedi = self.svaedi.get()
        ibuafjoldi = self.ibuafjoldi.get()
        vefsida = self.vefsida.get()
        valid2 = self.valid2.get()
        coordID = self.coordID.get()
        if borg == "" or svaedi == "":
            self.þarf.config(text="Fylltu inn í Borg og Svæði")
        else:
            if valid2 and coordID != "":
                pd.update_place(self.placeID,borg, svaedi, ibuafjoldi, vefsida, coordID)
            else:
                pd.update_place(self.placeID,borg,svaedi,ibuafjoldi,vefsida)
            self.þarf.config(text="")
            self.valid2.set(1)
            self.synaCoordID()
            self.skiptaPlace("placedb",self.place_update)

    def uppfaeraPl(self,event):
        pd = PlaceDB()
        focus = self.tree.focus()
        item = self.tree.item(focus)
        self.placeID = item['tags'][1]
        self.placeInfo = pd.get_place(self.placeID)
        self.skiptaPlace("placedb_update",self.place)

    def eydaPlace(self,event):
        focus = self.tree.focus()
        item = self.tree.item(focus)
        pd = PlaceDB()
        pd.delete_place(item['tags'][1])
        self.place.grid_remove()
        self.placedb()
