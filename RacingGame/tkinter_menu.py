from __future__ import annotations
import customtkinter
import tkinter

def initialize_custom_tkinter():
    #Set image as background
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")

def runGame()->None:
    print("Game runned")

class TkinterMenu:
    def __init__(self):

        self.gameFunction = None


        initialize_custom_tkinter()
        self.root = customtkinter.CTk()
        self.root.geometry("1600x900")
        
        self.frame = customtkinter.CTkFrame(master=self.root )
        self.frame.pack(pady=20, padx=60,fill ="both", expand=True)

        self.label = customtkinter.CTkLabel(master=self.frame, text="Run Fast  & Fury")
        self.label.pack(pady=12,padx=10)

        self.entry1 = customtkinter.CTkEntry(master=self.frame, placeholder_text="Username")
        self.entry1.pack(pady=12,padx=10)



        self.label3 = customtkinter.CTkLabel(master=self.frame, text="Select your Track:")
        self.label3.pack(pady=12,padx=10)

        self.track = tkinter.IntVar(0)

        self.radio1 = customtkinter.CTkRadioButton(master=self.frame, text="Track 1", variable=self.track, value=1 )
        self.radio1.pack(pady=12,padx=10)

        self.car = tkinter.IntVar(0)

        self.seprator = tkinter.ttk.Separator(master=self.frame, orient="horizontal")
        self.seprator.pack(pady=12,padx=10, fill="x")

        self.label2 = customtkinter.CTkLabel(master=self.frame, text="Select your car: (speed changes...)")
        self.label2.pack(pady=12,padx=10)

        self.radio3 = customtkinter.CTkRadioButton(master=self.frame, text="Ferrari 458 Italia", variable=self.car, value=1 )
        self.radio3.pack(pady=12,padx=10)

        self.button = customtkinter.CTkButton(master=self.frame, text="Run Game", command=self.runGameWrapper)
        self.button.pack(pady=12,padx=10)

        self.quitButton = customtkinter.CTkButton(master=self.frame, text="Quit Game", command=quit,fg_color="red", text_color="white", hover_color="red4")
        self.quitButton.pack(pady=12,padx=10)

        self.root.title("Fast & Fury")
        #self.root.mainloop()


    def runMenu(self)->None:
        self.root.mainloop()

    def setGameFunction(self, gameFunction):
        self.gameFunction = gameFunction

    def runGameWrapper(self):
        if self.gameFunction:
            self.gameFunction()
            self.root.destroy() 

    