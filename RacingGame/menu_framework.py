from __future__ import annotations
import customtkinter
import tkinter
from tkinter import *


def initialize_custom_tkinter():
    # base appeareance of the menu
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")


class TkinterFramework:
    '''Class that creates the framework of the menu outside of the game,
    used in the facade menu class (created with Tkinter library)'''

    def __init__(self):
        initialize_custom_tkinter()
        self.root = customtkinter.CTk()
        self.game_function = None
        self.usernameEntry = None

    def set_geometry(self, geometry) -> str:
        '''Set the Window size of the main menu'''
        self.root.geometry(geometry)

    def set_images(self, background_image_path, icon_image_path) -> PhotoImage:
        '''Set the background image of the main menu '''
        self.bg = PhotoImage(file=background_image_path)
        self.bg_label = Label(master=self.root, image=self.bg)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.root.iconbitmap(icon_image_path)

    def create_frame(self, border_width) -> customtkinter.CTkFrame:
        '''Create a frame to locate all the widgets of the menu'''
        self.frame = customtkinter.CTkFrame(
            master=self.root, border_width=border_width)
        self.frame.pack(pady=20, padx=60, expand=True)

    def create_label(self, text, font) -> customtkinter.CTkLabel:
        '''Create a label to insert in the frame of the menu '''
        self.label = customtkinter.CTkLabel(
            master=self.frame, text=text, font=font)
        self.label.pack(pady=15, padx=12)

    def create_Username_entry(self, placeholder_text, font) -> customtkinter.CTkEntry:
        '''Create an entry to insert in the frame of the menu '''
        self.entry = customtkinter.CTkEntry(
            master=self.frame, placeholder_text=placeholder_text, font=font)
        self.entry.pack(pady=12, padx=10)
        self.usernameEntry = self.entry

    def get_username(self) -> str:
        '''Get the username of the player to display it in game'''
        return self.usernameEntry.get()

    def create_radio_button(self, text, variable, value, font) -> customtkinter.CTkRadioButton:
        '''Create a radio button to insert in the frame of the menu '''
        self.radio = customtkinter.CTkRadioButton(
            master=self.frame, text=text, variable=variable, value=value, font=font)
        self.radio.pack(pady=12, padx=10)

    def create_separator(self) -> tkinter.ttk.Separator:
        '''Create a separator to insert in the frame of the menu '''
        self.separator = tkinter.ttk.Separator(
            master=self.frame, orient="horizontal")
        self.separator.pack(pady=12, padx=10, fill="x")

    def create_button(self, text, font, command) -> customtkinter.CTkButton:
        '''Create a button to insert in the frame of the menu '''
        self.button = customtkinter.CTkButton(
            master=self.frame, text=text, font=font, command=command)
        self.button.pack(pady=12, padx=10)

    def create_quit_button(self, text, font) -> customtkinter.CTkButton:
        '''Create a button to quit the menu '''
        self.button = customtkinter.CTkButton(
            master=self.frame, text=text, font=font, command=quit, fg_color="red", text_color="white", hover_color="red4")
        self.button.pack(pady=16, padx=10)

    def set_game_function(self, game_function) -> str:
        '''Set the game function to run the game'''
        self.game_function = game_function

    def run_game_wrapper(self) -> tkinter.Tk.destroy:
        '''Wrap the game function to run'''
        if self.game_function:
            self.game_function()
            self.root.destroy()

    def run(self) -> mainloop:
        '''Run the menu'''
        self.root.mainloop()
