import tkinter as tk
from tkinter import simpledialog

class ResizeDialog(tk.simpledialog.Dialog):
    def __init__(self, parent, title,prev_size=(0,0)):
        self.width = prev_size[0]
        self.height = prev_size[1]
        self.prev_size=prev_size
        self.is_scale=True
        self.ratio=prev_size[1]/prev_size[0]
        self._scale_var=tk.BooleanVar()
        self._width_var=tk.StringVar()
        self._height_var=tk.StringVar()

        self._scale_var.set(True)

        super().__init__(parent, title)


    def on_scale_change(self):
        
        self.is_scale=self._scale_var.get()
        

    def on_change_width(self,event=None):
        
        if self.is_scale:
            r=self.height/self.width
            w=int(self._width_var.get())
            h=int(w*r)
            self._height_var.set(h)

    def on_change_height(self,event=None):
        
        if self.is_scale:
            r=self.width/self.height
            h=int(self._height_var.get())
            w=int(h*r)
            self._width_var.set(w)
            print(f"{r} : {w} : {h}")
        

    def body(self, frame):
        # print(type(frame)) # tkinter.Frame
        tk.Label(frame, width=25, text="Width").pack()
    
        self.entry_width = tk.Entry(frame, width=25,textvariable=self._width_var)
        self.entry_width.insert(tk.END,self.prev_size[0])
        self.entry_width.pack()
        self.entry_width.focus()
        self.entry_width.bind("<KeyRelease>",self.on_change_width)
        

        tk.Label(frame, width=25, text="Height").pack()
    
        self.entry_height = tk.Entry(frame, width=25,textvariable=self._height_var)
        self.entry_height.insert(tk.END,self.prev_size[1])
        self.entry_height.pack()
        self.entry_height.bind("<KeyRelease>",self.on_change_height)
        # self.entry_height['show'] = '*'

        tk.Checkbutton(frame,text="Scale proportionally",variable=self._scale_var, command=self.on_scale_change).pack()

        return frame

    def ok_pressed(self):
        # print("ok")
        self.width = int(self.entry_width.get())
        self.height = int(self.entry_height.get())
        self.destroy()

    def cancel_pressed(self):
        self.width=0
        self.height=0
        self.destroy()


    def buttonbox(self):
        self.ok_button = tk.Button(self, text='OK', width=5, command=self.ok_pressed)
        self.ok_button.pack(padx=10,pady=10,side="left")
        cancel_button = tk.Button(self, text='Cancel', width=5, command=self.cancel_pressed)
        cancel_button.pack(padx=10,pady=10,side="right")
        self.bind("<Return>", lambda event: self.ok_pressed())
        self.bind("<Escape>", lambda event: self.cancel_pressed())
