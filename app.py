
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw,ImageOps
from new_img_dialog import NewImgDialog

from resize_dialog import ResizeDialog
import remove_bg
import removebg_yolo




class ImageEditor:
    def __init__(self, root):
        self.root = root
    
        self.root.title("Photo Editor")
        # self.root.geometry("700x700")
        self.root.minsize(700,700)
        # self.root.attributes("-fullscreen",True)
        # Get screen width and height
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        # Set window width and height
        self.root.geometry(f"{self.screen_width}x{self.screen_height}")

        self.image_path = ""
        self.image = None
        self.orginal_image = None
        self.photo_image = None

        self.start_x = None
        self.start_y = None

        self.draw_shape = "box"

        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)
        
        
        self.canvas.bind("<Button-1>", self.on_button_press) # mouse left button pressed
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)  # mouse drag
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release) # mouse left button released

        
        # shortcut key
        self.root.bind("<Control-o>",self.open_image) # pressed Ctrl+O 
        self.root.bind("<Control-s>",self.save)       # pressed Ctrl+S
        self.root.bind("<Control-r>",self.resize)     # pressed Ctrl+R
        self.root.bind("<Control-z>",self.reset)      # pressed Ctrl+Z
        self.root.bind("<Control-c>",self.crop)       # pressed Ctrl+S
        self.root.bind("<Control-n>",self.new_img)    # pressed Ctrl+N

        

    def open_image(self,event=None):
        self.image_path = filedialog.askopenfilename(title="Select an image")
        if self.image_path:
            self.image = Image.open(self.image_path)
            self.orginal_image=self.image
            self.update_canvas()

    def new_img(self,event=None):

        dialog=NewImgDialog(parent=self.root,title="Choose width, hight and color")
        if dialog.width>0:
            self.image=Image.new("RGBA",(dialog.width,dialog.height),dialog.color)
            self.update_canvas()
        
        
    def on_button_press(self, event):
        # Record the starting point of the box
        self.start_x = event.x
        self.start_y = event.y

    def on_mouse_drag(self, event):
        # Draw a shape as the mouse is dragged
        self.draw(event)

    def on_button_release(self, event):
        # Draw a final shape when the mouse is released
        self.draw(event)
        
        
    def draw(self,event):
        if(self.draw_shape=="box"):
            self.draw_box(self.start_x, self.start_y, event.x, event.y)
        if(self.draw_shape=="circle"):     
            self.draw_circle(self.start_x, self.start_y, event.x, event.y)
    
    def enable_draw_box(self):
        self.draw_shape="box"

    def enable_draw_circle(self):
        self.draw_shape="circle"

    def draw_box(self, x1, y1, x2, y2):
        # Clear existing items on the canvas
        self.canvas.delete("shape")

        # Draw the box
        self.box_id=self.canvas.create_rectangle(x1, y1, x2, y2, outline="red", tags="shape")
        

    def draw_circle(self, x1, y1, x2, y2):
        # Clear existing items on the canvas
        self.canvas.delete("shape")

        # Draw the circle
        self.circle_id=self.canvas.create_oval(x1, y1, x2, y2, outline="red", tags="shape")

    def crop(self,event=None):
        if(self.draw_shape=="box"):
            self.crop_box()
        if(self.draw_shape=="circle"):
            self.crop_circle()

    def crop_box(self):
        x1, y1, x2, y2 = self.canvas.coords(self.box_id)
        
        wr=self.orginal_image.size[0]/self.image.size[0]
        hr=self.orginal_image.size[1]/self.image.size[1]
        x1=int(x1*wr)
        y1=int(y1*hr)
        x2=int(x2*wr)
        y2=int(y2*hr)
        
        self.image=self.orginal_image.crop((x1,y1,x2,y2))
        
        self.update_canvas()
        
    def crop_circle(self):
        # Get the coordinates of the drawn circle
        x1, y1, x2, y2 = self.canvas.coords(self.circle_id)

        wr=self.orginal_image.size[0]/self.image.size[0]
        hr=self.orginal_image.size[1]/self.image.size[1]
        x1=int(x1*wr)
        y1=int(y1*hr)
        x2=int(x2*wr)
        y2=int(y2*hr)

        
        # Create a circular mask
        mask = Image.new("L", self.orginal_image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((x1, y1, x2, y2), fill=255)

        # Apply the circular mask to the original image
        circular_image = Image.new("RGBA", self.orginal_image.size, (0, 0, 0, 0))
        circular_image.paste(self.orginal_image, mask=mask)

        # Crop the image to the bounding box of the ellipse
        bounding_box = mask.getbbox()
        cropped_image = circular_image.crop(bounding_box)

        # Update the image and canvas with the circular image
        self.image = cropped_image
        self.update_canvas()

    def resize(self,event=None):
    
        orginal_size=self.orginal_image.size
        dialog=ResizeDialog(parent=self.root,title="Input new size",prev_size=orginal_size)
        
        if(dialog.width>0):
            size=(dialog.width,dialog.height)
            if(size):
                self.image=self.orginal_image.resize(size)
                self.update_canvas()
    

    def rotate(self,event=None):
        self.image=self.image.rotate(angle=90)
        self.update_canvas()

    def grascale(self,event=None):
        self.image=ImageOps.grayscale(self.image)
        self.update_canvas()

    def invert(self,event=None):
        self.image=ImageOps.invert(self.image)
        self.update_canvas()

    def flip(self,event=None):
        self.image=ImageOps.flip(self.image)
        self.update_canvas()

    def remove_bg(self,event=None):
        self.image=remove_bg.removeBg(self.image)
        self.update_canvas()

    def remove_bg_yolo(self,event=None):
        self.image=removebg_yolo.remove(self.image)
        self.update_canvas()
        

    def update_canvas(self):
        rimg=self.image

        if rimg.width>self.screen_width:
            w=rimg.width
            h=rimg.height
            r=h/w
            w=int(self.screen_width*0.8)
            h=int(w*r)
            rimg=rimg.resize((w,h))
            self.image=rimg
            


        self.canvas.delete("all")
        pimg=ImageTk.PhotoImage(rimg)
        self.canvas.image=pimg
        self.canvas.config(width=rimg.width,height=rimg.height)
        self.canvas.create_image(0,0,image=pimg,anchor=tk.NW)
    
    

    def reset(self,event=None):
        self.image=self.orginal_image
        self.update_canvas()

    def save(self,event=None):
        path=filedialog.asksaveasfilename()
        if(path):
            self.image.save(path)


    

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditor(root)


    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    file_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Open (Ctrl+O)", command=app.open_image)
    file_menu.add_command(label="New (Ctrl+N)", command=app.new_img)
    file_menu.add_command(label="Resize (Ctrl+R)", command=app.resize)
    file_menu.add_command(label="Rotate", command=app.rotate)
    file_menu.add_command(label="Grayscale", command=app.grascale)
    file_menu.add_command(label="Invert", command=app.invert)
    file_menu.add_command(label="Flip", command=app.flip)
    file_menu.add_command(label="Draw Box", command=app.enable_draw_box)
    file_menu.add_command(label="Draw Circle", command=app.enable_draw_circle)
    file_menu.add_command(label="Crop (Ctrl+C)", command=app.crop)
    file_menu.add_command(label="Remove background", command=app.remove_bg)
    file_menu.add_command(label="Remove background (yolo)", command=app.remove_bg_yolo)

    file_menu.add_command(label="Reset (Ctrl+Z)", command=app.reset)
    file_menu.add_command(label="Save (Ctrl+S)", command=app.save)

    about_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="About", menu=about_menu)
    about_menu.add_command(label="Exit", command=app.reset)

    root.mainloop()
