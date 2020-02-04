from Tkinter import *
import database
import time

class Main:

    def __init__(self):

#main window         
        self.main_window = Tk()
        self.main_window.title('DejaVu')
        self.main_window.wm_attributes('-topmost', True)
        #self.main_window.overrideredirect(True)
        x = self.main_window.winfo_screenwidth() - 250
        #self.main_window.minsize(200, 200)
        #self.main_window.maxsize(200, 300)
        self.main_window.geometry('200x200') 
        self.main_window.geometry('+%d+200'% (x))        
        self.main_window.resizable( width = False, height = False)
        self.main_window.config(bd = 0)
	self.note_color = "white"

#present application name
        self.status_bar = Frame(self.main_window)
        self.status_bar.pack(fill = X, side = BOTTOM)

        self.present_application_name = Label(self.status_bar)
        self.present_application_name.pack()

#menubar
        self.panel = Frame(self.main_window)
        self.panel.pack(side = TOP, fill = X,pady = 5, padx = 5)
        
        self.photo_new=PhotoImage(file="new.png")
        self.new_button = Button(self.panel)
        self.new_button.config(bd = 0, image = self.photo_new)
        self.new_button.pack(side  = LEFT,expand = 1,pady = 5, padx = 5)
        
        self.photo_list=PhotoImage(file="list.png")
	self.list_button = Button(self.panel)
        self.list_button.config(bd = 0, image = self.photo_list, command = self.list_button_clicked)
        self.list_button.pack(side = LEFT,expand = 1,pady = 5, padx = 5)

        self.photo_close=PhotoImage(file="close.png")
        self.quit_button = Button(self.panel)
        self.quit_button.config(bd = 0, image = self.photo_close)
        #self.quit_button.pack(side = RIGHT,pady = 5, padx = 5)

#settings_button
        self.setting_menu_button = Menubutton(self.panel)
        self.photo_settings=PhotoImage(file="settings.png")
        self.setting_menu_button.config(bd = 0, image = self.photo_settings)
        self.setting_menu = Menu(self.setting_menu_button)
        self.setting_menu.config( tearoff = 0) 
        self.setting_menu_button["menu"] = self.setting_menu
        self.setting_menu.add_command(label = 'Change Appearance', command = self.change_appearance)
        self.setting_menu.add_command(label = 'Help', command = self.help)
        self.setting_menu_button.pack(side = LEFT,expand = 1,pady = 5, padx = 5)
        
#space for notes        
        self.frame2 = Frame(self.main_window)
        self.frame2.pack(fill = X)

	self.canvas = Canvas(self.frame2, bd=0)

        self.vsb = Scrollbar(self.frame2, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left")

        self.framefornote = Frame(self.canvas)
	#self.framefornote.pack()
        self.canvas.create_window((0,0),window=self.framefornote)
        #self.framefornote.bind("<Configure>", self.onFrameConfigure)

    def refresh(self):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def display_notes(self, application_name):
        db = database.DatabaseQueries()
        notes = db.get_notes_by_application(application_name)
        self.display(notes)
        db.database_connection.close()

    def display(self, notes):
	for note in notes:
            id1 = str(note[0])
            time1 = note[1] 
            text1 = note[2]
            application_name = note[3]
            self.single_note_entry = Label(self.framefornote, justify=LEFT)
            self.single_note_entry.bind("<1>", lambda event, application = application_name, note_id = id1 : self.OnClick( event, application, note_id))
            self.single_note_entry.config(text = text1, wraplength = 170, background = self.note_color)
            self.single_note_entry.pack(side = TOP, fill = X, pady = 5, padx = 5,ipady = 3, ipadx = 3)
    	    
    def OnClick(self, event, application_name, note_id):
        
        db = database.DatabaseQueries()
        notes = self.edit_note(application_name, note_id)        

	
#####################################################################################################

    def list_button_clicked(self):

        self.open_window = Toplevel(self.main_window)
	self.open_window.wm_attributes('-topmost', True)
        self.open_window.minsize(200, 350)
        self.open_window.maxsize(200, 500) 

        self.list_menu_button = Menubutton(self.open_window)
        self.list_menu_button.config(bd = 0)
        self.list_menu = Menu(self.list_menu_button)
        self.list_menu.config( tearoff = 0) 
        self.list_menu_button["menu"] = self.list_menu
        self.list_menu_button.pack()        
        
        self.canvas2 = Canvas(self.open_window, borderwidth=0)        
        self.vsb2 = Scrollbar(self.open_window, orient="vertical", command=self.canvas2.yview)
        self.canvas2.configure(yscrollcommand=self.vsb2.set)

        self.vsb2.pack(side="right", fill="y")
        self.canvas2.pack(side="left", fill=X)

        self.list_area = Frame(self.canvas2)     
        self.canvas2.create_window((0,0), window=self.list_area, tags="self.list_area")
        self.list_area.bind("<Configure>", self.onFrameConfigure2)
        
        db = database.DatabaseQueries()
        apps = db.get_application_list()
        
        self.list_menu.add_command(label = "all", command = lambda all_apps = apps :self.list_all(all_apps))
        for app in apps:
            self.list_menu.add_command(label = app, command = lambda application = app : self.list_by_application(application))
        self.list_all(apps)
        
    def onFrameConfigure2(self, event):
        '''
	#Reset the scroll region to encompass the inner frame
	'''
        self.canvas2.configure(scrollregion=self.canvas2.bbox("all"))


    def list_all(self, apps):
        self.list_menu_button.config(text = "all")
        
        for child in self.canvas2.winfo_children():
            child.destroy()
        self.list_area = Frame(self.canvas2)
        #self.list_area.pack(fill = X, expand = 1)
        self.list_area.bind("<Configure>", self.onFrameConfigure2)
        self.canvas2.create_window((0,0), window=self.list_area, tags="self.list_area")       
        '''
        #self.vsb2 = Scrollbar(self.open_window, orient="vertical", command=self.canvas2.yview)
        #self.vsb2.pack(side="right", fill="y")
        #self.canvas2.configure(yscrollcommand=self.vsb2.set)
        #self.canvas2.pack(side="left", fill="both", expand=True)
        '''
        for app in apps:
            db = database.DatabaseQueries()
            notes = db.get_notes_by_application(app)
            for note in notes:
                note_id = str(note[0])
                note_text = note[2]
                application_name = note[3]
                self.single_note_entry = Label(self.list_area, anchor = W, justify = LEFT)
                self.single_note_entry.bind("<1>", lambda event, application = application_name, temp = note_id : self.OnClick( event, application, temp))
		self.single_note_entry.config(text = (note_text +" | "+ application_name), wraplength = 160, bg = "white")
                self.single_note_entry.pack(fill = X, expand = 1, padx = 5, pady = 5)
            
            db.database_connection.close()

    def list_by_application(self, app_name):
        self.list_menu_button.config(text = app_name)
        for child in self.canvas2.winfo_children():
            child.destroy()
        self.list_area = Frame(self.canvas2)
        #self.list_area.pack(fill = X, expand = 1) 
        self.canvas2.create_window((0,0), window=self.list_area, tags="self.list_area")
        self.list_area.bind("<Configure>", self.onFrameConfigure2)
        '''

        #self.vsb2 = Scrollbar(self.open_window, orient="vertical", command=self.canvas2.yview)
        #self.vsb2.pack(side="right", fill="y")
        #self.canvas2.configure(yscrollcommand=self.vsb2.set)
        #self.canvas2.pack(side="left", fill="both", expand=True)

        '''       
        db = database.DatabaseQueries()
        notes = db.get_notes_by_application(app_name)
        for note in notes:
            note_id = str(note[0])
            note_text = note[2]
            application_name = note[3]
            self.single_note_entry = Label(self.list_area, anchor = W, justify = LEFT)
            self.single_note_entry.bind("<1>", lambda event, application = application_name, temp = note_id : self.OnClick( event, application, temp))
            self.single_note_entry.config(text = note_text, wraplength = 160, bg = "white")
            self.single_note_entry.pack(fill = X, padx = 5, pady = 5)
            
        db.database_connection.close()

#######################################################################################

    def add_new(self, application_name):

        self.add_new_window = Toplevel(self.main_window);
        self.add_new_window.title('New Note')
	x = self.add_new_window.winfo_screenwidth() - 520
        self.add_new_window.geometry('200x100+%d+200'% (x))        
        self.add_new_window.resizable( width = False, height = False)
        self.add_new_window.config(bd = 0)

        self.frame3 = Frame(self.add_new_window)
	self.frame3.pack(fill = BOTH, expand = 1)

        self.label3 = Label(self.frame3)        
        self.label3.config(text = application_name)
        self.label3.pack(fill = X, expand = 1)

        self.text1 = Text(self.frame3)
        self.text1.config(wrap = WORD, height = 3)
        self.text1.pack(fill = BOTH, expand = 1)

        self.photo_save=PhotoImage(file="save.png")     
        self.save_button = Button(self.frame3)
        self.save_button.config(image=self.photo_save,bd = 0, command = lambda application = application_name : self.save_button_clicked(application))
        self.save_button.pack()
        
    def save_button_clicked(self, application_name):
        db = database.DatabaseQueries()
        db.save_note( time.strftime("%Y-%m-%d %H:%M"), self.text1.get("1.0",'end-1c'), application_name)
        self.add_new_window.destroy()
        for child in self.framefornote.winfo_children():
            child.destroy()
        self.display_notes(application_name)

###############################################################################################################

    def edit_note(self, application_name, note_id):
        self.edit_window = Toplevel(self.main_window);
        self.edit_window.title('Edit Note')
        x = self.edit_window.winfo_screenwidth() - 520
        self.edit_window.geometry('250x150+%d+100'% (x))        
        self.edit_window.resizable( width = False, height = False)
        self.edit_window.config(bd = 0)

	self.label4 = Label(self.edit_window)        
        self.label4.config(text = application_name)
        self.label4.pack(side =TOP, fill = X)

        self.text2 = Text(self.edit_window)
        db = database.DatabaseQueries()
        self.text2.insert(END, db.get_note_by_id(note_id))
        self.text2.config(wrap = WORD, height = 3)
        self.text2.pack(fill = BOTH, expand = 1)

	self.edit_panel = Frame(self.edit_window)
        self.edit_panel.pack(side = BOTTOM, fill = X)
	
        self.photo_save=PhotoImage(file="save.png")
        self.save_changes_button = Button(self.edit_panel)
        self.save_changes_button.config(image = self.photo_save, bd = 0, command = lambda temp = note_id, application = application_name : self.save_changes_button_clicked(temp, application))
        self.save_changes_button.pack(side = LEFT)

	self.photo_delete=PhotoImage(file="delete.png")
        self.delete_button = Button(self.edit_panel)
        self.delete_button.config(image = self.photo_delete, bd = 0, command = lambda temp = note_id, application = application_name : self.delete_button_clicked(temp, application))
        self.delete_button.pack(side = RIGHT)

    def save_changes_button_clicked(self, note_id, application_name):
        db = database.DatabaseQueries()
        db.edit_note(note_id, time.strftime("%Y-%m-%d %H:%M"), self.text2.get("1.0",'end-1c'))
        self.edit_window.destroy()
        for child in self.framefornote.winfo_children():
            child.destroy()
        self.display_notes(application_name)

    def delete_button_clicked(self, note_id, application_name):
        db = database.DatabaseQueries()
        db.delete_note(note_id)
        self.edit_window.destroy()
        for child in self.framefornote.winfo_children():
            child.destroy()
        self.display_notes(application_name)


############################################################################################

    def change_appearance(self):
	self.note_color = "white"

############################################################################################

    def help(self):

        self.help_window = Toplevel(self.main_window)
        self.help_window.title('help')
        self.text3 = Text(self.help_window)
        self.text3.insert(END, "Documentation goes here!")
        self.text3.pack()


