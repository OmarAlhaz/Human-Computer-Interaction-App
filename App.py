import smtplib
from tkinter import MULTIPLE,DISABLED, END, NORMAL, W, WORD, Button, Entry
import customtkinter
from customtkinter import CTkSlider, CTkProgressBar
from CTkMessagebox import CTkMessagebox
import os
from PIL import Image
import requests
from tkcalendar import Calendar
import tkinter as tk
from tkcalendar import Calendar
import firebase_admin
from firebase_admin import credentials , firestore
from firebase_admin import db
from datetime import datetime
import warnings
import urllib.request
import pygame
from tkinter import Listbox
from tkinter import filedialog
from tkinter import ttk
import time
from PIL import Image
from tkintermapview import TkinterMapView
import wikipedia
from googlesearch import search

class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("520x300")

class ScrolledListbox(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent)
        self.listbox = tk.Listbox(self, *args, **kwargs)
        self.listbox_scrollbar = tk.Scrollbar(self, orient="vertical", command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=self.listbox_scrollbar.set)
        self.listbox_scrollbar.pack(side="right", fill="y")
        self.listbox.pack(side="left", fill="both", expand=True)
        self.listbox.bind('<Enter>', self.enter)
        self.listbox.bind('<Leave>', self.leave)
        self.listvariable(kwargs.get('listvariable',None))
        

    def configure(self, **kwargs):
        self.listvariable(kwargs.get('listvariable',None))
        self.setbackground(kwargs.get('bg',None))
        self.setforeground(kwargs.get('fg',None))
        self.sethighlight(kwargs.get('highlightcolor',None))
        self.setselectbackground(kwargs.get('selectbackground',None))
        self.setexportselection(kwargs.get('exportselection',1))
        

    def listvariable(self, item_list):
        if item_list != None:
            for item in item_list:
                self.listbox.insert(tk.END, item)

    def setexportselection(self, exportselection):
        self.listbox.configure(exportselection = exportselection)

    def setbackground(self, bg):
        if bg != None:
            self.listbox.configure(bg = bg)
        
    def setforeground(self, fg):
        if fg != None:
            self.listbox.configure(fg = fg)
            
    def sethighlight(self, highlightcolor):
        if highlightcolor != None:
            self.listbox.configure(highlightcolor = highlightcolor)

    def setselectbackground(self, selectbackground):
        if selectbackground != None:
            self.listbox.configure(selectbackground = selectbackground)

    def enter(self, event):
        self.listbox.config(cursor="hand2")

    def leave(self, event):
        self.listbox.config(cursor="")

    def insert(self, location, item):
        self.listbox.insert(location, item)

    def curselection(self):
        return self.listbox.curselection()
        
    def delete(self, first, last=None):
        self.listbox.delete(first, last)

    def delete_selected(self):
        selected_item = self.listbox.curselection()
        idx_count = 0
        for item in selected_item:
            self.listbox.delete(item - idx_count)
            idx_count += 1

    def delete_unselected(self):
        selected_item = self.listbox.curselection()
        idx_count = 0
        for i, listbox_entry in enumerate(self.listbox.get(0, tk.END)):
            if not listbox_entry in selected_item:
                self.listbox.delete(i - idx_count)
                idx_count += 1

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Virtual Personal Assistant")
        self.geometry("820x450")
        self.resizable(0, 0)
        
        # Fetch the service account key JSON file contents
        cred = credentials.Certificate('serviceAccountKey.json')

        # Initialize the app with a service account, granting admin privileges
        try:
            firebase_admin.get_app()
        except ValueError:  # in case the app hasn't been initialized yet
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://course-51653-default-rtdb.firebaseio.com/'
            })
        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "User_Interface_Icons")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "Uniwa_logo.png")), size=(36, 36))
        self.large_personal_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "virtual_personal_image.png")), size=(600, 150))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))
        self.calendar_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "calendar_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "calendar_light.png")), size=(20, 20))
        self.mail_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "mail_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "mail_light.png")), size=(20, 20))
        self.reminder_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "reminder_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "reminder_light.png")), size=(20, 20))
        self.weather_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "weather_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "weather_light.png")), size=(20, 20))
        self.music_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "music_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "music_light.png")), size=(20, 20))
        self.device_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "device_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "device_light.png")), size=(20, 20))
        self.basket_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "basket_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "basket_light.png")), size=(20, 20))
        self.map_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "map_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "map_light.png")), size=(20, 20))
        self.search_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "search_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "search_light.png")), size=(20, 20))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkScrollableFrame(self, corner_radius=16,border_width=16,border_color="#179dff",scrollbar_fg_color="#179dff",scrollbar_button_color="#0061b0")
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(13, weight=1)

        # center the window on the screen
        self.update_idletasks()
        width = 820
        height = 450
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))


        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Mail",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.mail_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Reminders",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.reminder_image, anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.frame_4_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Appointments",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.calendar_image, anchor="w", command=self.frame_4_button_event)
        self.frame_4_button.grid(row=4, column=0, sticky="ew")

        self.frame_5_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="SMS",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w", command=self.frame_5_button_event)
        self.frame_5_button.grid(row=5, column=0, sticky="ew")

        self.frame_6_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Weather",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.weather_image, anchor="w", command=self.frame_6_button_event)
        self.frame_6_button.grid(row=6, column=0, sticky="ew")

        self.frame_7_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Contacts",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w", command=self.frame_7_button_event)
        self.frame_7_button.grid(row=7, column=0, sticky="ew")

        self.frame_8_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Music",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.music_image, anchor="w", command=self.frame_8_button_event)
        self.frame_8_button.grid(row=8, column=0, sticky="ew")

        self.frame_9_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Devices",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.device_image, anchor="w", command=self.frame_9_button_event)
        self.frame_9_button.grid(row=9, column=0, sticky="ew")

        self.frame_10_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Shop",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.basket_image, anchor="w", command=self.frame_10_button_event)
        self.frame_10_button.grid(row=10, column=0, sticky="ew")

        self.frame_11_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Map",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.map_image, anchor="w", command=self.frame_11_button_event)
        self.frame_11_button.grid(row=11, column=0, sticky="ew")

        self.frame_12_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Search",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.search_image, anchor="w", command=self.frame_12_button_event)
        self.frame_12_button.grid(row=12, column=0, sticky="ew")



        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame,fg_color="#179dff",button_color="#0061b0", values=[ "Light", "Dark", "System"]
                                                                ,command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=13, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="", image=self.large_personal_image)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        # create textbox
        self.textbox = customtkinter.CTkTextbox(master=self.home_frame, width=10,height=275 ,wrap=WORD,fg_color=("#f0ecec","#282424"),text_color=("#3D3D3D","#FAFAFA"), font=("Franklin Gothic Book", 18))
        self.textbox.grid(row=1, sticky="nsew")

        filename = "On-line_help.txt"
        with open(filename, "r", encoding="utf-8") as file:
            text = file.read()

        self.textbox.insert("0.0", text)

        # create second frame
        self.second_frame = customtkinter.CTkFrame(self,corner_radius=0, fg_color="transparent")

        def send(): 
            try:
                username = usernameEntry.get() 
                password = passwordEntry.get() 
                to = receiverEntry.get()
                subject = subjectEntry.get() 
                body = bodyEntry.get('1.0', tk.END)
                if username=="" or password=="" or to=="" or subject=="" or body=="": 
                    notif.configure(text='All fields required!', text_color="orange")
                    return
                else:
                    finalMessage = 'Subject: {}\n\n{}'.format (subject, body)
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(username, password)
                    server.sendmail(username, to, finalMessage)
                    notif.configure(text='Email has been sent', text_color="Green")
            except Exception as e:
                notif.configure(text="Error sending email", text_color="red")
        def reset():
            try:
                usernameEntry.delete(0, 'end')
                passwordEntry.delete(0, 'end')
                receiverEntry.delete(0, 'end')
                subjectEntry.delete(0, 'end')
                bodyEntry.delete(0, 'end')
            except:
                pass

        notif = customtkinter.CTkLabel(self.second_frame, text="", font=customtkinter.CTkFont(size=20, weight="bold"))
        notif.grid(row=10, column=3, columnspan=8, padx=10, sticky="nsew")

        label = customtkinter.CTkLabel(self.second_frame, text="Use the form below to send an email", font=("Roboto", 24))
        label.grid(row=1, column=3, columnspan=8, padx=100, pady=10, sticky="nsew")

        usernameEntry = customtkinter.CTkEntry(self.second_frame, placeholder_text="Email")
        usernameEntry.grid(row=2, column=4, columnspan=6,  padx=50, pady=10, sticky="nsew")

        passwordEntry = customtkinter.CTkEntry(self.second_frame, placeholder_text="Password", show="*")
        passwordEntry.grid(row=3, column=4, columnspan=6,  padx=50, pady=10, sticky="nsew")

        receiverEntry = customtkinter.CTkEntry(self.second_frame, placeholder_text="To")
        receiverEntry.grid(row=4, column=4, columnspan=6,  padx=50, pady=10, sticky="nsew")

        subjectEntry = customtkinter.CTkEntry(self.second_frame, placeholder_text="Subject")
        subjectEntry.grid(row=5, column=2, columnspan=10,  padx=50, pady=10, sticky="nsew")

        bodyEntry = customtkinter.CTkTextbox(self.second_frame, width=200, height=70)
        bodyEntry.grid(row=6, column=2, columnspan=10,  padx=50, pady=10, sticky="nsew")
        bodyEntry.insert("0.0", "Entry\n\n\n\n")

        SendButton = customtkinter.CTkButton(self.second_frame, text="Send", width=200, command=send)
        SendButton.grid(row=7, column=4, columnspan=3, padx=(10, 0), pady=10, sticky="nsew")

        ResetButton = customtkinter.CTkButton(self.second_frame, text="Reset", width=200, command=reset)
        ResetButton.grid(row=7, column=7, columnspan=3, padx=(10, 0), pady=10, sticky="nsew")


        # create third frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        def set_reminder():
            reminder_msg = self.reminder_entry.get()
            reminder_time = self.time_entry.get()

            # validate user input
            if not reminder_msg:
                CTkMessagebox(title="Error", message="Please enter a reminder message.", icon="cancel")
                return
            if not reminder_time or not reminder_time.count(":") == 1:
                CTkMessagebox(title="Error", message="Please enter a valid time in format HH:MM AM/PM.", icon="cancel")
                return
            
            # check if the entered time is valid
            try:
                datetime.strptime(reminder_time, '%I:%M %p')
            except ValueError:
                CTkMessagebox(title="Error", message="Please enter a valid time in format HH:MM AM/PM.", icon="cancel")
                return

            # add code to set the reminder/alarm
            db = firestore.client()
            doc_ref = db.collection('reminders')
            doc_data ={
                'message': reminder_msg,
                'time': reminder_time
            }
            doc_ref.add(doc_data)
            CTkMessagebox(title="Success", message=f"Reminder/Alarm set for {reminder_time} Message: {reminder_msg}",icon="check", option_1="Thanks")
            show_reminders()


        self.reminder_label = customtkinter.CTkLabel(self.third_frame, text="Reminder:")
        self.reminder_label.grid(row=0,columnspan=1,padx=50, pady=10, sticky="w")

        self.reminder_entry = customtkinter.CTkEntry(self.third_frame, placeholder_text="Message")
        self.reminder_entry.grid(row=0,columnspan=8, padx=120, pady=10, sticky="nsew")

        self.time_label = customtkinter.CTkLabel(self.third_frame, text="Time:")
        self.time_label.grid(row=1,columnspan=1, padx=50, pady=10, sticky="w")

        self.time_entry = customtkinter.CTkEntry(self.third_frame, placeholder_text="HH:MM AM/PM")
        self.time_entry.grid(row=1,columnspan=10,  padx=150, pady=10, sticky="nsew")

        self.set_button = customtkinter.CTkButton(self.third_frame, text="Set", command=set_reminder)
        self.set_button.grid(row=2, columnspan=10,  padx=50, pady=10, sticky="nsew")

        self.reminders_window = ScrolledListbox(self.third_frame, selectmode=MULTIPLE, height=10, width=90)
        db = firestore.client()
        reminders_ref = db.collection('reminders')
        self.reminders_window.configure(bg='#5454FF', fg='white')
        self.reminders_window.configure(selectbackground='#2E2E8B')
        self.reminders_window.grid(row=3, column=0, padx=10, pady=10)


        def show_reminders():
            listbox = self.reminders_window.listbox
            listbox.delete(0, tk.END)  # Delete all existing items
            
            for reminder in reminders_ref.stream():
                reminder_data = reminder.to_dict()
                self.reminders_window.insert(tk.END, f"Time: {reminder_data['time']} - Message: {reminder_data['message']}")

        self.show_button = customtkinter.CTkButton(self.third_frame, text="Show Reminders", command=show_reminders)
        self.show_button.grid(row=4, columnspan=10, padx=50, pady=10, sticky="nsew")

        def delete_selected_reminders():
            selected_indices = self.reminders_window.listbox.curselection()
            selected_reminders = []

            for index in selected_indices:
                reminder = self.reminders_window.listbox.get(index)
                selected_reminders.append(reminder)

            # Delete the selected reminders from the database
            db = firestore.client()
            reminders_ref = db.collection('reminders')

            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                
                for reminder in selected_reminders:
                    # Find the reminder document in the database based on the reminder details
                    time, message = parse_reminder_details(reminder)
                    query = reminders_ref.where('time', '==', time).where('message', '==', message)

                    # Delete the reminder document
                    for doc in query.stream():
                        doc.reference.delete()

            # Remove the selected reminders from the listbox
            for index in reversed(selected_indices):
                self.reminders_window.delete(index)

        # Helper function to parse reminder details from the listbox entry
        def parse_reminder_details(reminder):
            # Assuming the reminder entry has the format: "Time: {time} - Message: {message}"
            time = reminder.split(' - ')[0].split(': ')[1]
            message = reminder.split(' - ')[1].split(': ')[1]
            return time, message

        self.delete_button = customtkinter.CTkButton(self.third_frame, text="Delete Reminders", command=delete_selected_reminders)
        self.delete_button.grid(row=5, columnspan=10, padx=50, pady=10, sticky="nsew")


        # create fourth frame
        self.fourth_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")  

        # start date title
        self.start_date_title = customtkinter.CTkLabel(self.fourth_frame, text="Select Start Date", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.start_date_title.grid(row=0, column=0, columnspan=1, padx=20, pady=10)

        # end date title
        self.end_date_title = customtkinter.CTkLabel(self.fourth_frame, text="Select End Date", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.end_date_title.grid(row=0, column=1, columnspan=1, padx=20, pady=10)

       # start date calander
        self.start_cal = Calendar(self.fourth_frame, selectmode='day',
                                showweeknumbers=False, cursor="hand2", date_pattern='y-mm-dd',
                                borderwidth=0, bordercolor='white')
        self.start_cal.grid(row=1, column=0, padx=30, pady=10, sticky='w')

        # bind function to update placeholder text for start date entry
        def update_start_date_placeholder(event):
            selected_date = self.start_cal.get_date()
            self.start_date_entry.delete(0, "end")  # Clear the current text in the entry field
            self.start_date_entry.insert(0, selected_date)  # Insert the selected date

        self.start_cal.bind("<<CalendarSelected>>", update_start_date_placeholder)

        # end date calander
        self.end_cal = Calendar(self.fourth_frame, selectmode='day',
                                showweeknumbers=False, cursor="hand2", date_pattern='y-mm-dd',
                                borderwidth=0, bordercolor='white')
        self.end_cal.grid(row=1, column=1, padx=30, pady=10, sticky='e')

        # bind function to update placeholder text for end date entry
        def update_end_date_placeholder(event):
            selected_date = self.end_cal.get_date()
            self.end_date_entry.delete(0, "end")  # Clear the current text in the entry field
            self.end_date_entry.insert(0, selected_date)  # Insert the selected date

        self.end_cal.bind("<<CalendarSelected>>", update_end_date_placeholder)

        def confirm_dates():
            start_date = self.start_date_entry.get()
            end_date = self.end_date_entry.get()
            comment = self.comment_entry.get()

            # Validate user input
            if not start_date or not end_date:
                CTkMessagebox(title="Error", message="Please select both start and end dates.", icon="cancel")
                return

            # Add code to save the selected dates to the Firebase database
            db = firestore.client()
            doc_ref = db.collection('appointments')
            doc_data = {
                'start_date': start_date,
                'end_date': end_date,
                'comment':comment
            }
            doc_ref.add(doc_data)
            CTkMessagebox(title="Success!", message="Dates confirmed and saved to database.",
                  icon="check", option_1="Thanks")

            # Clear the input fields
            self.start_date_entry.delete(0, "end")
            self.end_date_entry.delete(0, "end")
            self.comment_entry.delete(0,"end")

        def show_appointments():
            # Retrieve the appointments from the Firebase database
            db = firestore.client()
            appointments = db.collection('Appointments').get()

            # Create a new window to display the appointments
            self.appointments_window = ToplevelWindow(self.fourth_frame)
            self.appointments_window.title("Appointments")
            self.appointments_window_label = customtkinter.CTkLabel(self.appointments_window, text="Your Appointments:", font=customtkinter.CTkFont(size=20, weight="bold"))
            self.appointments_window_label.grid(row=0, column=0, columnspan=1, padx=20, pady=10)

            # Create a listbox to display the appointments
            self.appointment_listbox = ScrolledListbox(self.appointments_window, selectmode=MULTIPLE,height=10,width=70)
            #self.appointment_listbox = tk.Listbox(self.appointments_window)

            # fetch the appointments from Firestore and add them to the listbox
            db = firestore.client()
            appointments_ref = db.collection('appointments')
            for appointment in appointments_ref.stream():
                appt_data = appointment.to_dict()
                self.appointment_listbox.insert(tk.END, f"Start Date: {appt_data['start_date']} | End Date: {appt_data['end_date']} | Comment: {appt_data['comment']}")
            self.appointment_listbox.configure(bg='#5454FF', fg='white')
            self.appointment_listbox.configure(selectbackground='#2E2E8B')
            self.appointment_listbox.grid(row=1, column=0, padx=10, pady=10)

            # Create a button to dismiss the appointments window
            self.dismiss_button = customtkinter.CTkButton(self.appointments_window, text="Close",command=self.appointments_window.destroy)
            #dismiss_button.grid(row=4, column=0, columnspan=1, padx=10, pady=30)
            self.dismiss_button.grid(row=2,columnspan=3, padx=120, pady=10, sticky="w")

            # Create a button to delete the selected appointments
            self.delete_button = customtkinter.CTkButton(self.appointments_window, text="Delete", command=delete_selected_appointments)
            self.delete_button.grid(row=2, columnspan=3, padx=280, pady=10, sticky="w")


        def delete_selected_appointments():
            selected_indices = self.appointment_listbox.listbox.curselection()
            selected_appointments = []

            for index in selected_indices:
                appointment = self.appointment_listbox.listbox.get(index)
                selected_appointments.append(appointment)

            # Delete the selected appointments from the database
            db = firestore.client()
            appointments_ref = db.collection('appointments')
            
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                for appointment in selected_appointments:
                    # Find the appointment document in the database based on the appointment details
                    start_date, end_date, comment = parse_appointment_details(appointment)
                    query = appointments_ref.where('start_date', '==', start_date).where('end_date', '==', end_date).where('comment', '==', comment)


                # Delete the appointment document
                for doc in query.stream():
                    doc.reference.delete()

            # Remove the selected appointments from the listbox
            for index in reversed(selected_indices):
                self.appointment_listbox.delete(index)

        # Helper function to parse appointment details from the listbox entry
        def parse_appointment_details(appointment):
            # Assuming the appointment entry has the format: "Start Date: {start_date} | End Date: {end_date} | Comment: {comment}"
            start_date = appointment.split(' | ')[0].split(': ')[1]
            end_date = appointment.split(' | ')[1].split(': ')[1]
            comment = appointment.split(' | ')[2].split(': ')[1]
            return start_date, end_date, comment



            # Modify the show_appointments button
        self.show_appointments = customtkinter.CTkButton(self.fourth_frame, text="Show Appointments", hover=True, command=show_appointments)
        self.show_appointments.grid(row=4, column=1, columnspan=2, padx=10, pady=30)




        # date confirm button
        self.confirm_date = customtkinter.CTkButton(self.fourth_frame, text="Confirm Dates", hover=True, command=confirm_dates)
        self.confirm_date.grid(row=4, column=0, columnspan=1, padx=10, pady=30)

        # show appointments button
        self.show_appointments = customtkinter.CTkButton(self.fourth_frame, text="Show Appointments", hover=True, command=show_appointments)
        self.show_appointments.grid(row=4, column=1, columnspan=2, padx=10, pady=30)
        
        # start date entry
        self.start_date_entry = customtkinter.CTkEntry(self.fourth_frame, placeholder_text="Start Date")
        self.start_date_entry.grid(row=2, column=0, padx=10, pady=10)

        # end date entry
        self.end_date_entry = customtkinter.CTkEntry(self.fourth_frame, placeholder_text="End Date")
        self.end_date_entry.grid(row=2, column=1, padx=10, pady=10)

        # create main entry and button
        self.comment_entry = customtkinter.CTkEntry(self.fourth_frame, placeholder_text="Add Comment")
        self.comment_entry.grid(row=3,columnspan=8, padx=120, pady=10, sticky="nsew")


        # create fifth frame
        self.fifth_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent") 

        def send_text():
            phone_number = self.phone_entry.get()
            message = self.message_entry.get()

            # validate user input
            if not phone_number:
                CTkMessagebox(title="Error", message="Please enter a phone number.", icon="cancel")
                return
            if not message:
                CTkMessagebox(title="Error", message="Please enter a message.", icon="cancel")
                return

            # Save the phone number and message to Firebase Firestore
            db = firestore.client()
            doc_ref = db.collection('text_messages').document()
            doc_data = {
                'phone_number': phone_number,
                'message': message
            }
            doc_ref.set(doc_data)

            CTkMessagebox(title="Success", message=f"Text message sent to {phone_number}: {message}", icon="check", option_1="Thanks")
            show_text_messages()

        self.phone_label = customtkinter.CTkLabel(self.fifth_frame, text="Phone Number:")
        self.phone_label.grid(row=0, columnspan=1, padx=50, pady=10, sticky="w")

        self.phone_entry = customtkinter.CTkEntry(self.fifth_frame, placeholder_text="Number")
        #self.phone_entry.grid(row=0, columnspan=8, padx=120, pady=10, sticky="nsew")
        self.phone_entry.grid(row=0,columnspan=10,  padx=150, pady=10, sticky="nsew")

        self.message_label = customtkinter.CTkLabel(self.fifth_frame, text="Message:")
        self.message_label.grid(row=1, columnspan=1, padx=50, pady=10, sticky="w")

        self.message_entry = customtkinter.CTkEntry(self.fifth_frame, placeholder_text="Message")
        self.message_entry.grid(row=1, columnspan=8, padx=120, pady=10, sticky="nsew")

        self.send_button = customtkinter.CTkButton(self.fifth_frame, text="Send", command=send_text)
        self.send_button.grid(row=2, columnspan=10, padx=50, pady=10, sticky="nsew")

        self.text_messages_window = ScrolledListbox(self.fifth_frame, selectmode=tk.MULTIPLE, height=10, width=90)
        self.text_messages_window.configure(bg='#5454FF', fg='white')
        self.text_messages_window.configure(selectbackground='#2E2E8B')
        self.text_messages_window.grid(row=3, column=0, padx=10, pady=10)

        def show_text_messages():
            listbox = self.text_messages_window.listbox
            listbox.delete(0, tk.END)  # Delete all existing items

            db = firestore.client()
            text_messages_ref = db.collection('text_messages')

            for message in text_messages_ref.stream():
                message_data = message.to_dict()
                listbox.insert(tk.END, f"Phone Number: {message_data['phone_number']} - Message: {message_data['message']}")

        self.show_button = customtkinter.CTkButton(self.fifth_frame, text="Show Text Messages", command=show_text_messages)
        self.show_button.grid(row=4, columnspan=10, padx=50, pady=10, sticky="nsew")

        def delete_selected_text_messages():
            selected_indices = self.text_messages_window.listbox.curselection()
            selected_messages = []

            db = firestore.client()
            text_messages_ref = db.collection('text_messages')

            for index in selected_indices:
                message = self.text_messages_window.listbox.get(index)
                selected_messages.append(message)

            with warnings.catch_warnings():
                warnings.simplefilter("ignore")

                for message in selected_messages:
                    # Find the message document in the database based on the message details
                    phone_number, message_text = parse_message_details(message)
                    query = text_messages_ref.where('phone_number', '==', phone_number).where('message', '==', message_text)

                    # Delete the message document
                    for doc in query.stream():
                        doc.reference.delete()

            # Remove the selected messages from the listbox
            for index in reversed(selected_indices):
                self.text_messages_window.delete(index)

        # Helper function to parse message details from the listbox entry
        def parse_message_details(message):
            # Assuming the message entry has the format: "Phone Number: {phone_number} - Message: {message}"
            phone_number = message.split(' - ')[0].split(': ')[1]
            message_text = message.split(' - ')[1].split(': ')[1]
            return phone_number, message_text

        self.delete_button = customtkinter.CTkButton(self.fifth_frame, text="Delete Text Messages", command=delete_selected_text_messages)
        self.delete_button.grid(row=5, columnspan=10, padx=50, pady=10, sticky="nsew")

        # create sixth frame
        self.sixth_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        self.location_label = customtkinter.CTkLabel(self.sixth_frame, text="Enter your location:", font=("Roboto", 24))
        self.location_label.grid(row=1, columnspan=1, padx=200, pady=10)

        self.location_entry = customtkinter.CTkEntry(self.sixth_frame, placeholder_text="Location")
        self.location_entry.grid(row=2, columnspan=5, padx=150, pady=10)
        self.update_button = customtkinter.CTkButton(self.sixth_frame, text="Get Updates", width=200,
                                                command=lambda: display_weather(self.location_entry.get()))
        self.update_button.grid(row=3, columnspan=6, padx=100, pady=10)

        self.radiobutton_var = customtkinter.IntVar(value=2)
        self.weather_label_1 = None
        self.weather_label_2 = None

        # Create the labels with initial properties
        weather_label_1 = customtkinter.CTkLabel(self.sixth_frame, text="", image=None,
                                                    compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        weather_label_2 = customtkinter.CTkLabel(self.sixth_frame, text="",
                                                    font=customtkinter.CTkFont(size=15, weight="bold"))
        # Grid the labels
        weather_label_1.grid(row=4, padx=100, pady=10)
        weather_label_2.grid(row=5, padx=100, pady=10)

        # Grid the labels
        self.radiobutton_1 = customtkinter.CTkRadioButton(master=self.sixth_frame, variable=self.radiobutton_var, text="Fahrenheit" , value=1,command=lambda: display_weather(self.location_entry.get()))
        self.radiobutton_1.grid(row=7, columnspan=1, padx=100, pady=10)
        self.radiobutton_1.configure(state="disabled")

        self.radiobutton_2 = customtkinter.CTkRadioButton(master=self.sixth_frame, variable=self.radiobutton_var, text="Celcius" ,value=2,command=lambda: display_weather(self.location_entry.get()))
        self.radiobutton_2.grid(row=6,columnspan=1, padx=100, pady=10)
        self.radiobutton_2.configure(state="disabled")

        def display_weather(location):
            #print(location)
            # use an API to get weather updates
            # replace 'YOUR_API_KEY' with your actual API key
            weather_url = f"https://api.weatherapi.com/v1/current.json?key=6c1025c12b0a43fa9e4144151230204&q={location}&aqi=no"

            try:
                response = requests.get(weather_url)
                data = response.json()

                #print(data)  # Print the response data to check its structure

                # get the temperature and condition from the API response
                temperature_c = data['current']['temp_c']
                condition = data['current']['condition']['text']
                temperature_f = data['current']['temp_f']
                current_weather_icon = data['current']['condition']['icon']
                country = data['location']['tz_id']
                wind_speed_mph = data['current']['wind_mph']
                wind_speed_kph = data['current']['wind_kph']
                wind_direction = data['current']['wind_dir']
                feels_like_c = data['current']['feelslike_c']
                feels_like_f = data['current']['feelslike_f']


                urllib.request.urlretrieve('https:' + current_weather_icon, "User_Interface_Icons\weather_icon.png")
                weather_icon = customtkinter.CTkImage(Image.open("User_Interface_Icons\weather_icon.png"), size=(100, 100))

                if self.location_entry.get() !="":
                    self.radiobutton_1.configure(state="normal")
                    self.radiobutton_2.configure(state="normal")


                radio_var = self.radiobutton_var.get()
                if radio_var == 2:
                    # Create new labels
                    weather_label_1 = customtkinter.CTkLabel(self.sixth_frame, text=f"{temperature_c}°C\n{country}\n", image=weather_icon,
                                                                compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
                    weather_label_2 = customtkinter.CTkLabel(self.sixth_frame, text=f"Current Condition:    {condition}\nFeels Like:    {feels_like_c}°C\nWind Speed:    {wind_speed_kph}\nWind Direction:    {wind_direction}",
                                                                font=customtkinter.CTkFont(size=15, weight="bold"))
                elif radio_var== 1:
                    # Create new labels
                    weather_label_1 = customtkinter.CTkLabel(self.sixth_frame, text=f"{temperature_f}°F\n{country}\n", image=weather_icon,
                                                                compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
                    weather_label_2 = customtkinter.CTkLabel(self.sixth_frame, text=f"Current Condition:    {condition}\nFeels Like:    {feels_like_f}°F\nWind Speed:    {wind_speed_mph}\nWind Direction:    {wind_direction}",
                                                                font=customtkinter.CTkFont(size=15, weight="bold"))
                else:
                    pass
                # Grid the labels
                weather_label_1.grid(row=4, padx=100, pady=10)
                weather_label_2.grid(row=5, padx=100, pady=10)

                # Destroy the labels if they already exist
                if self.weather_label_1:
                    self.weather_label_1.destroy()
                if self.weather_label_2:
                    self.weather_label_2.destroy()

                # Assign the new labels to instance variables
                self.weather_label_1 = weather_label_1
                self.weather_label_2 = weather_label_2

            except Exception as e:
                CTkMessagebox(title="Error", message=f"{str(e)}", icon="cancel")
                print(f"{str(e)}")
        
        # Call the display_weather function with default value
        display_weather("Athens")
        
        # create seventh frame
        self.seventh_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        self.message_label = customtkinter.CTkLabel(self.seventh_frame, text="Name:")
        self.message_label.grid(row=0, columnspan=1, padx=50, pady=10, sticky="w")

        self.name_entry = customtkinter.CTkEntry(self.seventh_frame, placeholder_text="First and Last Name")
        self.name_entry.grid(row=0, columnspan=8, padx=120, pady=10, sticky="nsew")

        self.phone_label = customtkinter.CTkLabel(self.seventh_frame, text="Phone Number:")
        self.phone_label.grid(row=1, columnspan=1, padx=50, pady=10, sticky="w")

        self.phon_entry = customtkinter.CTkEntry(self.seventh_frame, placeholder_text="Number")
        self.phon_entry.grid(row=1,columnspan=10,  padx=150, pady=10, sticky="nsew")

        def add_contact():
            name = self.name_entry.get()
            phone = self.phon_entry.get()

            # validate user input
            if not name:
                CTkMessagebox(title="Error", message="Please enter a name.", icon="cancel")
                return
            if not phone:
                CTkMessagebox(title="Error", message="Please enter a phone number.", icon="cancel")
                return
            
            # Save the phone number and message to Firebase Firestore
            db = firestore.client()
            doc_ref = db.collection('contacts').document(name)
            doc_data = {
                'name': name,
                'number': phone
            }
            doc_ref.set(doc_data)
            CTkMessagebox(title="Success", message=f"Contact added!\n{name}: {phone}", icon="check", option_1="Thanks")
            show_contacts()

        self.send_button = customtkinter.CTkButton(self.seventh_frame, text="Add Contact", command=add_contact)
        self.send_button.grid(row=2, columnspan=10, padx=50, pady=10, sticky="nsew")

        self.contacts_window = ScrolledListbox(self.seventh_frame, selectmode=tk.MULTIPLE, height=10, width=90)
        self.contacts_window.configure(bg='#5454FF', fg='white')
        self.contacts_window.configure(selectbackground='#2E2E8B')
        self.contacts_window.grid(row=3, column=0, padx=10, pady=10)

        def show_contacts():
                    listbox = self.contacts_window.listbox
                    listbox.delete(0, tk.END)  # Delete all existing items

                    db = firestore.client()
                    contacts_ref = db.collection('contacts')

                    for contact in contacts_ref.stream():
                        contact_data = contact.to_dict()
                        name = contact_data.get('name', '')
                        number = contact_data.get('number', '')
                        listbox.insert(tk.END, f"Name: {name} - Number: {number}")
    

        self.show_button = customtkinter.CTkButton(self.seventh_frame, text="Show Contacts", command=show_contacts)
        self.show_button.grid(row=4, columnspan=10, padx=50, pady=10, sticky="nsew")


        def delete_contacts():
            selected_indices = self.contacts_window.listbox.curselection()
            selected_contacts = []

            db = firestore.client()
            contacts_ref = db.collection('contacts')

            for index in selected_indices:
                contact = self.contacts_window.listbox.get(index)
                selected_contacts.append(contact)

            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                for contact in selected_contacts:
                    name, number = parse_contact_details(contact)
                    query = contacts_ref.where('number', '==', number).where('name', '==', name)
                    #.document(name)

                    # Delete the contact document
                    for doc in query.stream():
                        doc.reference.delete()

            # Remove the selected contacts from the listbox
            for index in reversed(selected_indices):
                self.contacts_window.listbox.delete(index)


        # Helper function to parse contact details from the listbox entry
        def parse_contact_details(contact):
            # Assuming the message entry has the format: "Name: {name} - Number: {number}"
            name = contact.split(' - ')[1].split(': ')[1]
            number = contact.split(' - ')[0].split(': ')[1]
            return name, number        

        self.delete_button = customtkinter.CTkButton(self.seventh_frame, text="Delete Contacts", command=delete_contacts)
        self.delete_button.grid(row=5, columnspan=10, padx=50, pady=10, sticky="nsew")

        # create eighth frame
        self.eighth_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        pygame.mixer.init()


        

        def volume(value):
            pygame.mixer.music.set_volume(value)


        songs = []
        global current_song, paused, current_song_loop,seek_time
        current_song = ""
        paused = False
        current_song_loop = ""
        seek_time = ""
            



        def play_music():
            global current_song, paused
                
            if paused == False:

                pygame.mixer.music.load(os.path.join(self.eighth_frame.directory, current_song))
                pygame.mixer.music.play()
            else:
                pygame.mixer.music.unpause() 
                paused = False


        def pause_music():
            global paused
            pygame.mixer.music.pause() 
            paused = True

        def next_music():
            global current_song, paused
            try:
                songlist.selection_clear(0, tk.END)
                songlist.selection_set(songs.index (current_song) + 1) 
                current_song = songs[songlist.curselection()[0]] 
                play_music()
            except:
                pass

        def prev_music():
            global current_song, paused
            try:
                songlist.selection_clear(0, tk.END)
                songlist.selection_set(songs.index (current_song) - 1) 
                current_song = songs[songlist.curselection()[0]] 
                play_music()
            except:
                pass

        def on_progressbar_click(event):
            global music_duration,seek_time

            x = event.x
            progress = x / progressbar.winfo_width()
            seek_time = int(music_duration * progress)
            print(seek_time)
            pygame.mixer.music.set_pos(seek_time)
            

            # Update the progress bar and current time
            update_progress()

        def update_progress():
            global current_song, music_duration, current_song_loop,seek_time
            try:
                if not (current_song_loop == current_song):
                    current_song = songs[songlist.curselection()[0]]
                    music = pygame.mixer.Sound(os.path.join(self.eighth_frame.directory, current_song))
                    music_duration = music.get_length()
                    current_song_loop = current_song

                if seek_time != "":
                    current_time = seek_time
                else:
                    current_time = pygame.mixer.music.get_pos() / 1000


                progressbar.set((current_time / music_duration))
                progressbar.update()

                current_time_str = time.strftime('%M:%S', time.gmtime(current_time))
                duration_str = time.strftime('%M:%S', time.gmtime(music_duration))
                if current_time_str != "59:59":
                    song_label.configure(
                        text=f"Now Playing: {current_song.split('/')[-1].split('.mp3')[0]} - {current_time_str}/{duration_str}")
                self.eighth_frame.after(100, update_progress)  # Schedule the next update after 100 milliseconds
            except:
                pass

        def load_music():
            global current_song, music_duration, current_song_loop

            # open a file dialog to select a music file
            if current_song == "":
                self.eighth_frame.directory = filedialog.askdirectory()
                try:
                    for song in os.listdir(self.eighth_frame.directory):
                        name, ext = os.path.splitext(song)
                        if ext == '.mp3':
                            songs.append(song)

                    for song in songs:
                        songlist.insert("end", song)
                    songlist.selection_set(0)
                    current_song = songs[songlist.curselection()[0]]
                    current_song_loop = current_song
                    music = pygame.mixer.Sound(os.path.join(self.eighth_frame.directory, current_song))
                    music_duration = music.get_length()
                except:
                    pass

                # start updating the progress bar and song label
                update_progress()

            
        def on_song_select(event):
            global current_song, paused
            try:
                current_song = songs[songlist.curselection()[0]]
                if not paused:
                    play_music()
                else:
                    pygame.mixer.music.load(os.path.join(self.eighth_frame.directory, current_song))
                update_progress()  # Call the update_progress function here
            except IndexError:
                pass
            
        def on_song_double_click(event):
            global current_song, paused
            try:
                current_song = songs[songlist.curselection()[0]]
                if not paused:
                    play_music()
            except IndexError:
                pass

        play_btn_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "play_button.png")),
                                                    dark_image=Image.open(os.path.join(image_path, "play_button.png")), size=(50, 50))
        next_btn_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "next_button.png")),
                                                    dark_image=Image.open(os.path.join(image_path, "next_button.png")), size=(50, 50))
        prev_btn_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "previous_button.png")),
                                                    dark_image=Image.open(os.path.join(image_path, "previous_button.png")), size=(50, 50))
        pause_btn_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "pause_button.png")),
                                                    dark_image=Image.open(os.path.join(image_path, "pause_button.png")), size=(50, 50))



        self.navigation_frame_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, anchor="w", border_spacing=10, text="Uni.W.A ICE", image=self.logo_image,
            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),compound="left", font=customtkinter.CTkFont(size=15, weight="bold"), command=load_music)
        self.navigation_frame_button.grid(row=0, column=0, sticky="ew")



        # Create the song list
        songlist = Listbox(master=self.eighth_frame, fg='white', bg='#7676EE', width=92, height=15)
        songlist.configure(selectbackground='#7F7FFF')
        songlist.grid(row=0, padx=10, pady=10)
        songlist.bind("<<ListboxSelect>>", on_song_select)
        songlist.bind("<Double-Button-1>", on_song_double_click)

        # Create the play button
        play_button = customtkinter.CTkButton(master=self.eighth_frame, corner_radius=0, text="", width=2,
                                            fg_color="transparent", hover_color=("gray70", "gray30"),
                                            image=play_btn_image, command=play_music)
        play_button.grid(row=1, column=0, padx=(230, 0), pady=10, sticky='w')

        # Create the next button
        next_button = customtkinter.CTkButton(master=self.eighth_frame, corner_radius=0, text="", width=2,
                                            fg_color="transparent", hover_color=("gray70", "gray30"),
                                            image=next_btn_image, command=next_music)
        next_button.grid(row=1, column=0, padx=(350, 0), pady=10, sticky='w')

        # Create the previous button
        prev_button = customtkinter.CTkButton(master=self.eighth_frame, corner_radius=0, text="", width=2,
                                            fg_color="transparent", hover_color=("gray70", "gray30"),
                                            image=prev_btn_image, command=prev_music)
        prev_button.grid(row=1, column=0, padx=(170, 0), pady=10, sticky='w')

        # Create the pause button
        pause_button = customtkinter.CTkButton(master=self.eighth_frame, corner_radius=0, text="", width=2,
                                            fg_color="transparent", hover_color=("gray70", "gray30"),
                                            image=pause_btn_image, command=pause_music)
        pause_button.grid(row=1, column=0, padx=(290, 0), pady=10, sticky='w')

        # Create the slider
        slider = CTkSlider(master=self.eighth_frame, from_=0, to=1, progress_color='#7676EE',button_color='#45458B', command=volume, width=210)
        slider.grid(row=2, padx=10, pady=10)

        # Create the progress bar
        progressbar = CTkProgressBar(master=self.eighth_frame, progress_color='#7676EE', width=450)
        progressbar.grid(row=3, padx=10, pady=10)
        progressbar.bind("<Button-1>", on_progressbar_click)

        # Create the song label
        song_label = customtkinter.CTkLabel(master=self.eighth_frame, text="Press the Uni.W.A ICE button to load music", font=customtkinter.CTkFont(size=12, weight="bold"))
        song_label.grid(row=4, padx=10, pady=10)

        # create ninth frame
        self.ninth_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # Fetch the service account key JSON file contents
        cred = credentials.Certificate('serviceAccountKey.json')

        # Initialize the app with a service account, granting admin privileges
        try:
            firebase_admin.get_app()
        except ValueError:  # in case the app hasn't been initialized yet
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://course-51653-default-rtdb.firebaseio.com/'
            })



        self.device_label = customtkinter.CTkLabel(self.ninth_frame, text="Device Name:")
        self.device_label.grid(row=0, columnspan=1, padx=50, pady=10, sticky="w")

        self.device_entry = customtkinter.CTkEntry(self.ninth_frame, placeholder_text="Name")
        self.device_entry.grid(row=0, columnspan=10, padx=150, pady=10, sticky="nsew")

        self.location_label = customtkinter.CTkLabel(self.ninth_frame, text="Location:")
        self.location_label.grid(row=1, columnspan=1, padx=50, pady=10, sticky="w")

        self.device_location_entry = customtkinter.CTkEntry(self.ninth_frame, placeholder_text="example: Athens")
        self.device_location_entry.grid(row=1,columnspan=8,  padx=120, pady=10, sticky="nsew")

        self.threshold_label = customtkinter.CTkLabel(self.ninth_frame, text="Threshold:")
        self.threshold_label.grid(row=2, columnspan=1, padx=50, pady=10, sticky="w")

        self.threshold_entry = customtkinter.CTkEntry(self.ninth_frame, placeholder_text="in Mbps")
        self.threshold_entry.grid(row=2,columnspan=12,  padx=180, pady=10, sticky="nsew")    

        def add_device():
            device = self.device_entry.get()
            location = self.device_location_entry.get()
            threshold = self.threshold_entry.get()

            # validate user input
            if not device:
                CTkMessagebox(title="Error", message="Please enter a Device name.", icon="cancel")
                return
            if not location:
                CTkMessagebox(title="Error", message="Please enter a location.", icon="cancel")
                return
            if not threshold:
                CTkMessagebox(title="Error", message="Please enter a threshold.", icon="cancel")
                return
            
            # Save the phone number and message to Firebase Firestore
            db = firestore.client()
            doc_ref = db.collection('devices').document(device)
            doc_data = {
                'device_name': device,
                'location': location,
                'threshold': threshold
            }

            doc_ref.set(doc_data)
            CTkMessagebox(title="Success", message=f"Device added!\n{device}:{threshold} Mbps, {location} ", icon="check", option_1="Thanks")
            show_devices()

        self.send_button = customtkinter.CTkButton(self.ninth_frame, text="Add Device", command=add_device)
        self.send_button.grid(row=3, columnspan=10, padx=50, pady=10, sticky="nsew")

        self.devices_window = ScrolledListbox(self.ninth_frame, selectmode=tk.MULTIPLE, height=8, width=90)
        self.devices_window.configure(bg='#5454FF', fg='white')
        self.devices_window.configure(selectbackground='#2E2E8B')
        self.devices_window.grid(row=4, column=0, padx=10, pady=10)

        def show_devices():
                    listbox = self.devices_window.listbox
                    listbox.delete(0, tk.END)  # Delete all existing items

                    db = firestore.client()
                    devices_ref = db.collection('devices')

                    for device in devices_ref.stream():
                        device_data = device.to_dict()
                        dev = device_data.get('device_name', '')
                        location = device_data.get('location', '')
                        threshold = device_data.get('threshold', '')

                        listbox.insert(tk.END, f"Device: {dev} - Threshold: {threshold} - Location: {location}")
    

        self.show_button = customtkinter.CTkButton(self.ninth_frame, text="Show Devices", command=show_devices)
        self.show_button.grid(row=5, columnspan=10, padx=50, pady=10, sticky="nsew")


        def delete_devices():
            selected_indices = self.devices_window.listbox.curselection()
            selected_devices = []

            db = firestore.client()
            devices_ref = db.collection('devices')

            for index in selected_indices:
                device = self.devices_window.listbox.get(index)
                selected_devices.append(device)

            with warnings.catch_warnings():
                warnings.simplefilter("ignore")

                for device in selected_devices:
                    device_name, location, threshold = parse_device_details(device)
                    query = devices_ref.where('device_name', '==', device_name).where('location', '==', location).where('threshold', '==', threshold)

                    # Delete the devices document
                    for doc in query.stream():
                        doc.reference.delete()

            # Remove the selected devices from the listbox
            for index in reversed(selected_indices):
                self.devices_window.listbox.delete(index)


        # Helper function to parse device details from the listbox entry
        def parse_device_details(device):
            # Assuming the message entry has the format: "Name: {name} - Number: {number}"
            #"Device: {dev} - Threshold: {threshold} - Location: {location}"
            device_name = device.split(' - ')[1].split(': ')[1]
            threshold = device.split(' - ')[0].split(': ')[1]
            location = device.split(' - ')[0].split(': ')[1]
            return device_name, threshold, location   

        self.delete_button = customtkinter.CTkButton(self.ninth_frame, text="Delete Devices", command=delete_devices)
        self.delete_button.grid(row=6, columnspan=10, padx=50, pady=10, sticky="nsew")


        # Create the tenth frame
        self.tenth_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # Add a label to the shopping window
        self.shopping_label = customtkinter.CTkLabel(self.tenth_frame, text="Welcome to the shopping list!", font=customtkinter.CTkFont(size=22, weight="bold"))
        self.shopping_label.pack(pady=10)

        # Add a listbox to display the selected items
        items_listbox = tk.Listbox(self.tenth_frame, bg ='#5C5C5C')
        items_listbox.config(selectbackground='#383838')
        items_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Add the shopping items to the listbox
        shopping_items = [
            {"name": "Milk", "price": 1.99, "image": "milk.png"},
            {"name": "Eggs", "price": 2.99, "image": "eggs.png"},
            {"name": "Bread", "price": 0.99, "image": "bread.png"},
            {"name": "Cheese", "price": 3.99, "image": "cheese.png"},
            {"name": "Apples", "price": 0.50, "image": "apples.png"},
            {"name": "Oranges", "price": 0.75, "image": "oranges.png"},
            {"name": "Bananas", "price": 0.25, "image": "bananas.png"},
            {"name": "Tomatoes", "price": 1.49, "image": "tomatoes.png"},
            {"name": "Lettuce", "price": 1.99, "image": "lettuce.png"},
            {"name": "Carrots", "price": 0.99, "image": "carrots.png"},
            {"name": "Potatoes", "price": 0.75, "image": "potatoes.png"},
            {"name": "Onions", "price": 0.50, "image": "onions.png"},
            {"name": "Garlic", "price": 1.99, "image": "garlic.png"},
            {"name": "Chicken", "price": 6.99, "image": "chicken.png"},
            {"name": "Beef", "price": 9.99, "image": "beef.png"},
            {"name": "Fish", "price": 7.99, "image": "fish.png"},
            {"name": "Pasta", "price": 2.99, "image": "pasta.png"},
            {"name": "Rice", "price": 1.99, "image": "rice.png"},
            {"name": "Cereal", "price": 3.49, "image": "cereal.png"},
            {"name": "Yogurt", "price": 1.25, "image": "yogurt.png"}
        ]
        for item in shopping_items:
            items_listbox.insert(tk.END, f"{item['name']} (${item['price']})")

        # Add a listbox to display the selected items for the shopping list
        shopping_listbox = tk.Listbox(self.tenth_frame, bg='#5C5C5C')
        shopping_listbox.config(selectbackground='#383838')
        shopping_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Add a scrollbar for the shopping list listbox
        shopping_scrollbar = tk.Scrollbar(self.tenth_frame)
        shopping_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        

        shopping_listbox.config(yscrollcommand=shopping_scrollbar.set)
        shopping_scrollbar.config(command=shopping_listbox.yview)
        # Add a label to display the total price of selected items in the shopping list
        self.total_price_label = customtkinter.CTkLabel(self.tenth_frame, text="Total Price: $0.00   ")
        self.total_price_label.pack(pady=10)

        def update_total_price():
            total_price = 0.0
            for idx in range(shopping_listbox.size()):
                item_price = float(shopping_listbox.get(idx).split("$")[1].split(")")[0])
                total_price += item_price
            self.total_price_label.configure(text=f"Total Price: ${total_price:.2f}")

        # Add a button to add selected items to the shopping list
        def add_item():
            selected_items = items_listbox.curselection()
            if len(selected_items) > 0:
                for item_index in selected_items:
                    item = shopping_items[item_index]
                    shopping_listbox.insert(tk.END, f"{item['name']} (${item['price']})")
                    update_total_price()

        # Add a button to checkout and place an online order
        def checkout():
            selected_items = shopping_listbox.get(0, tk.END)
            if len(selected_items) > 0:
                message = f"You are about to place an order for the following items:\n\n"
                for item in selected_items:
                    message += f"- {item}\n"
                total_price = 0.0
                for idx in range(shopping_listbox.size()):
                    item_price = float(shopping_listbox.get(idx).split("$")[1].split(")")[0])
                    total_price += item_price
                message += f"Total Price: ${total_price:.2f}\n"
                message += "\nDo you want to proceed with the order?"
                # get yes/no answers
                msg = CTkMessagebox(title="Confirm order", message=message,
                                    icon="question",  option_1="No", option_2="Yes")
                response = msg.get()
                
                if response=="Yes":
                    CTkMessagebox(title="Order placed", message="Your order has been placed. Thank you for shopping with us!")
                    clear_list()       
                else:
                    print("Click 'Yes' to exit!")

        # Add a button to clear the shopping list
        def clear_list():
            shopping_listbox.delete(0, tk.END)
            update_total_price()

        # Call the update_total_price function initially to display the correct total price
        update_total_price()

        checkout_button = customtkinter.CTkButton(self.tenth_frame, text="Checkout and place order",fg_color ='#5C5C5C',hover_color='#383838', command=checkout)
        checkout_button.pack(pady=10)

        add_button = customtkinter.CTkButton(self.tenth_frame, text="Add Item",fg_color ='#5C5C5C',hover_color='#383838', command=add_item)
        add_button.pack(pady=10)

        clear_button = customtkinter.CTkButton(self.tenth_frame, text="Clear List",fg_color ='#5C5C5C',hover_color='#383838', command=clear_list)
        clear_button.pack(pady=5)

        item_image = customtkinter.CTkLabel(self.tenth_frame, compound="center", text="")
        item_image.pack(pady=10)

        def on_item_select(event):
            try:
                selected_item = items_listbox.get(items_listbox.curselection())
                item_name = selected_item.split(" ")[0]
                if item_name in item_images:
                    item_image.configure(image=item_images[item_name])
                    item_image.image = item_images[item_name]  # Keep a reference to prevent garbage collection
                else:
                    item_image.config(image=None)
            except Exception:
                pass

        items_listbox.bind("<<ListboxSelect>>", on_item_select)

        image_path2 = os.path.join(os.path.dirname(os.path.realpath(__file__)), "shopping_items")

        # Load and store the images
        item_images = {}
        for item in shopping_items:
            self.photo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path2,(item['image']))), size=(225, 225))
            item_images[item['name']] = self.photo_image


        # Start with the first item selected (if any)
        if items_listbox.size() > 0:
            items_listbox.selection_set(0)
            on_item_select(None)


        # Create the eleventh frame
        self.eleventh_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        self.marker_list = []

        def search_event(event=None):
            self.map_widget.set_address(self.entry.get())

        def set_marker_event():
            current_position = self.map_widget.get_position()
            self.marker_list.append(self.map_widget.set_marker(current_position[0], current_position[1]))

        def clear_marker_event():
            for marker in self.marker_list:
                marker.delete()


        def change_map(new_map: str):
            if new_map == "OpenStreetMap":
                self.map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
            elif new_map == "Google normal":
                self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
            elif new_map == "Google satellite":
                self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)


        self.eleventh_frame.grid_columnconfigure(0, weight=0)
        self.eleventh_frame.grid_columnconfigure(1, weight=1)
        self.eleventh_frame.grid_rowconfigure(0, weight=1)

        self.frame_right = customtkinter.CTkFrame(master=self.eleventh_frame, corner_radius=0)
        self.frame_right.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")

        self.frame_right.grid_rowconfigure(1, weight=1)
        self.frame_right.grid_rowconfigure(0, weight=0)
        self.frame_right.grid_columnconfigure(0, weight=1)
        self.frame_right.grid_columnconfigure(1, weight=0)
        self.frame_right.grid_columnconfigure(2, weight=1)

        self.map_widget = TkinterMapView(self.frame_right, corner_radius=0)
        self.map_widget.grid(row=1, rowspan=1, column=0, columnspan=3, sticky="nswe", padx=(0, 0), pady=(0, 0))

        self.entry = customtkinter.CTkEntry(master=self.frame_right,
                                            placeholder_text="type address")
        self.entry.grid(row=0, column=0, sticky="we", padx=(12, 0), pady=12)
        self.entry.bind("<Return>", search_event)

        self.search = customtkinter.CTkButton(master=self.frame_right,
                                                text="Search",
                                                width=90,
                                                command=search_event,fg_color ='#5C5C5C',hover_color='#383838')
        self.search.grid(row=0, column=1, sticky="wesn", padx=(12, 0), pady=12)


        self.set_marker = customtkinter.CTkButton(master=self.frame_right,
                                                text="Set Marker",
                                                command=set_marker_event,fg_color ='medium sea green',hover_color='sea green')
        self.set_marker.grid(row=4, column=0, sticky="w", padx=(12, 0), pady=12)

        self.clear_marker = customtkinter.CTkButton(master=self.frame_right,
                                                text="Clear Markers",
                                                command=clear_marker_event,fg_color ='indian red',hover_color='orange red')
        self.clear_marker.grid(pady=12, padx=(140, 0), row=4, column=0)

        self.map_option_menu = customtkinter.CTkOptionMenu(self.frame_right, values=["OpenStreetMap", "Google normal", "Google satellite"],
                                                                       command=change_map,fg_color ='#5C5C5C',button_color='#383838',button_hover_color='#383838')
        self.map_option_menu.grid(row=4, column=1, padx=(60, 0), pady=(5, 0))


        self.map_widget.set_address("Berlin")
        self.map_option_menu.set("OpenStreetMap")


        # create twelfth frame
        self.twelfth_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "User_Interface_Icons")
        self.browser_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "browser.png")), size=(60, 60))

        labelWeb = customtkinter.CTkLabel(self.twelfth_frame, text="Wiki Web Search", image=self.browser_image,
                                                             compound="left", font=customtkinter.CTkFont(size=25, weight="bold"))
        labelWeb.grid(row=0, sticky=W)

        labelSearch = customtkinter.CTkLabel(self.twelfth_frame, text="Search", text_color=("#8B8B00","yellow") , font=customtkinter.CTkFont(size=20, weight="bold"))
        labelSearch.grid(row=1, sticky=W)

        def perform_search():
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                topic = textentry.get()
                try:
                    data = wikipedia.summary(topic, sentences=10, chars=500, auto_suggest=False, redirect=True)
                    insert_text(data)
                except wikipedia.exceptions.DisambiguationError as e:
                    search_results = wikipedia.search(topic)
                    result = f"Multiple options found for '{topic}'. Please be more specific.\n" + '\n'.join(search_results)
                    insert_text(result)
                except wikipedia.exceptions.PageError:
                    insert_text(f"No results found for '{topic}' on Wikipedia.")
                
        def perform_google_search():
            topic = textentry.get()
            links_list = list(search(topic, tld="com", lang='en', num=50, stop=50, pause=2))
            links_text = '\n'.join(links_list[:50])  # Concatenate links with newline separator
            insert_text(links_text)

        def clear_text():
            output.configure(state=NORMAL)
            output.delete(1.0, END)
            textentry.delete(0, END)
            output.configure(state=DISABLED)

        def insert_text(text):
            output.configure(state=NORMAL)
            output.delete(1.0, END)
            output.insert(END, text)
            output.configure(state=DISABLED)
            
        def random_text():
            topic = wikipedia.random(pages=1)
            data = wikipedia.summary(topic, sentences=10, chars=500, auto_suggest=True, redirect=True)
            insert_text(data)
        # Create a text entry box
        textentry = Entry(self.twelfth_frame, width=92, bg="white", highlightcolor='red', bd=3)
        textentry.grid(row=4, sticky=W, columnspan=8, padx=3, pady=10)


        # create textbox
        output = customtkinter.CTkTextbox(master=self.twelfth_frame, width=550,height=285 ,wrap=WORD,fg_color=("#FFFFFA","#424242"),text_color=("black","#FAFAFA"), font=("Roboto", 12))
        output.grid(row=6, padx=10, sticky=W)
        output.configure(state=DISABLED)

        EnterButton = Button(self.twelfth_frame, text="Enter", width=10, fg="#FFFFFF", bg="#3E48DA", activeforeground='red', activebackground='blue', command=perform_search)
        EnterButton.grid(row=5,padx=125, sticky=W)

        ClearButton = Button(self.twelfth_frame, text="Clear", width=10, fg="#FFFFFF", bg="#3E48DA", activeforeground='red', activebackground='blue', command=clear_text)
        ClearButton.grid(row=5,padx=205, sticky=W)

        LinksButton = Button(self.twelfth_frame, text="Google", width=10, fg="#FFFFFF", bg="#3E48DA", activeforeground='red', activebackground='blue', command=perform_google_search)
        LinksButton.grid(row=5,padx=285, sticky=W)

        RandomButton = Button(self.twelfth_frame, text="Random", width=10, fg="#FFFFFF", bg="#3E48DA", activeforeground='red', activebackground='blue', command=random_text)
        RandomButton.grid(row=5,padx=365, sticky=W)


       
        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "Mail" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "Reminders" else "transparent")
        self.frame_4_button.configure(fg_color=("gray75", "gray25") if name == "Appointments" else "transparent")
        self.frame_5_button.configure(fg_color=("gray75", "gray25") if name == "SMS" else "transparent")
        self.frame_6_button.configure(fg_color=("gray75", "gray25") if name == "Weather" else "transparent")
        self.frame_7_button.configure(fg_color=("gray75", "gray25") if name == "Contacts" else "transparent")
        self.frame_8_button.configure(fg_color=("gray75", "gray25") if name == "Music" else "transparent")
        self.frame_9_button.configure(fg_color=("gray75", "gray25") if name == "Devices" else "transparent")
        self.frame_10_button.configure(fg_color=("gray75", "gray25") if name == "Shop" else "transparent")
        self.frame_11_button.configure(fg_color=("gray75", "gray25") if name == "Map" else "transparent")
        self.frame_12_button.configure(fg_color=("gray75", "gray25") if name == "Search" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "Mail":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "Reminders":
            self.third_frame.grid(row=0, column=1, sticky="nsew")    
        else:
            self.third_frame.grid_forget()
        if name == "Appointments":
            self.fourth_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.fourth_frame.grid_forget()
        if name == "SMS":
            self.fifth_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.fifth_frame.grid_forget()
        if name == "Weather":
            self.sixth_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.sixth_frame.grid_forget()
        if name == "Contacts":
            self.seventh_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.seventh_frame.grid_forget()
        if name == "Music":
            self.eighth_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.eighth_frame.grid_forget()
        if name == "Devices":
            self.ninth_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.ninth_frame.grid_forget()
        if name == "Shop":
            self.tenth_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.tenth_frame.grid_forget()
        if name == "Map":
            self.eleventh_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.eleventh_frame.grid_forget()
        if name == "Search":
            self.twelfth_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.twelfth_frame.grid_forget()



    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("Mail")

    def frame_3_button_event(self):
        self.select_frame_by_name("Reminders")

    def frame_4_button_event(self):
        self.select_frame_by_name("Appointments")
    
    def frame_5_button_event(self):
        self.select_frame_by_name("SMS")

    def frame_6_button_event(self):
        self.select_frame_by_name("Weather")       

    def frame_7_button_event(self):
        self.select_frame_by_name("Contacts")

    def frame_8_button_event(self):
        self.select_frame_by_name("Music")

    def frame_9_button_event(self):
        self.select_frame_by_name("Devices")

    def frame_10_button_event(self):
        self.select_frame_by_name("Shop")

    def frame_11_button_event(self):
        self.select_frame_by_name("Map")

    def frame_12_button_event(self):
        self.select_frame_by_name("Search")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()

