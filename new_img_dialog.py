import tkinter as tk
from tkinter import simpledialog,colorchooser

class NewImgDialog(tk.simpledialog.Dialog):
    def __init__(self, parent, title):
        self.width = 0
        self.height = 0

        # Initial color
        self.color = "#FF0000"


        
        super().__init__(parent, title)

    def show_color_picker(self,event=None):
        color = colorchooser.askcolor(title="Pick a Color", color=self.color)
        if color:
            self.color = color[1]
            self.color_box.config(bg=self.color)

    def body(self, frame):
        # print(type(frame)) # tkinter.Frame
        tk.Label(frame, width=25, text="Width").pack()
        self.entry_width = tk.Entry(frame, width=25)
        self.entry_width.pack()
        

        tk.Label(frame, width=25, text="Height").pack()
    
        self.entry_height = tk.Entry(frame, width=25)
        self.entry_height.pack()

        tk.Label(frame,width=25,text="Color").pack()
    

        # Create a colored box
        self.color_box = tk.Canvas(frame, width=60, height=60, bg=self.color)
        self.color_box.pack(padx=20, pady=20)
        self.color_box.bind("<Button-1>", self.show_color_picker)  # Bind left mouse click to show_color_picker

    

        return frame

    def ok_pressed(self):
        # print("ok")
        self.width = int(self.entry_width.get())
        self.height = int(self.entry_height.get())
        self.destroy()

    def cancel_pressed(self):
        # print("cancel")
        self.destroy()


    def buttonbox(self):
        self.ok_button = tk.Button(self, text='OK', width=5, command=self.ok_pressed)
        self.ok_button.pack(padx=10,pady=10,side="left")
        cancel_button = tk.Button(self, text='Cancel', width=5, command=self.cancel_pressed)
        cancel_button.pack(padx=10,pady=10,side="right")
        self.bind("<Return>", lambda event: self.ok_pressed())
        self.bind("<Escape>", lambda event: self.cancel_pressed())
