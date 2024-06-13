# import tkinter as tk
# from random import randint
# from memory_profiler import profile

# def x_y_dict(list1 ,box_size) -> dict:
#     dict1 = {}
#     for x , y  in list1:
#         x //= box_size
#         y //= box_size
        
#         if x in dict1:
#             dict1[x].add(y)
#         else:
#             dict1[x] = {y}
#     return dict1

# def get_new_cords(dict1 ,width_box ,height_box ,box_size):
#     y = randint(0 , width_box)
#     x = randint(0 , height_box)
    
#     orignal_x = x
#     while (x in dict1) and (len(dict1[x]) == width_box+1):
#         x = (x+1) if x < width_box else 0
#         if orignal_x == x:
#             return None
        
#     orignal_y = y
#     while (x in dict1) and (y in dict1[x]):
#         y = (y+1) if y < height_box else 0
#         if orignal_y == y:
#             return None
    
#     return x * box_size , y * box_size

# game = 0
# width = 400
# height = 400
# box_size = 5

# list1 = []

# width_box = (width // box_size)-1
# height_box = (height // box_size)-1
# @profile
# def lololol():
#     def draw_coordinates(canvas, list1, box_size):
#         for x, y in list1:
#             canvas.create_rectangle(x, y, x + box_size, y + box_size, fill="red")
            
#     def lololol(canvas, list1, box_size, width_box, height_box):
#         global game
#         dict1 = x_y_dict(list1, box_size)
#         new_cords = get_new_cords(dict1, width_box, height_box, box_size)
        
#         if new_cords:
#             list1.append(new_cords)
#             draw_coordinates(canvas, [new_cords], box_size)
#             # Re-schedule the function to run again after 1ms
#             canvas.after(1, lololol, canvas, list1, box_size, width_box, height_box)
#             game += 1
#             print(game)
            
#     root = tk.Tk()
#     root.geometry(f"{width+100}x{height+100}")
#     root.title("Coordinate Visualization")

#     canvas = tk.Canvas(root, width=width, height=height)
#     canvas.pack()

#     canvas.after(100, lololol, canvas, list1, box_size, width_box, height_box)

#     draw_coordinates(canvas, list1, box_size)

#     root.mainloop()
    
# lololol()
# import tkinter as tk
# from tkinter import Canvas

# class Heart:
#     """
#     This class helps create hearts, remove hearts, and manipulate heart shapes on a canvas.
#     This class will not do anything to calculate coordinates.
#     """
#     def __init__(self, canvas: Canvas, box_size: int, color: str):
#         self.canvas = canvas
#         self.box_size = box_size
#         self.color = color
        
#         self.hearts = None
#         self.coords = None
            
#     def _create_heart_shape(self, coordinates: tuple[int, int]):
#         """
#         Draw a heart shape on the canvas.
        
#         Argument:
#             coordinates (int, int): Takes x and y coordinates for where to draw the heart.
            
#         Returns:
#             None
#         """
#         x1, y1 = coordinates
#         x2, y2 = x1 + self.box_size, y1 + self.box_size

#         new_y1 = (self.box_size / 2) + y1
#         new_x1 = (self.box_size / 2) + x1
#         radius = (new_y1 - y1) / 2
        
#         first = self.canvas.create_arc(x1, new_y1 - radius, new_x1, new_y1 + radius, fill=self.color, start=0, extent=180)
#         second = self.canvas.create_arc(new_x1, new_y1 - radius, x2, new_y1 + radius, fill=self.color, start=0, extent=180)
#         third = self.canvas.create_polygon(x1, new_y1, x2, new_y1, (x1 + x2) / 2, y2, fill=self.color)
#         self.hearts = (first, second, third)
#         self.coords = (x1, y1)
    
#     def _move_resize_heart_shape(self, coordinates):
#         x1, y1 = coordinates
#         x2, y2 = x1 + self.box_size, y1 + self.box_size

#         new_y1 = (self.box_size / 2) + y1
#         new_x1 = (self.box_size / 2) + x1
#         radius = (new_y1 - y1) / 2
        
#         self.canvas.coords(self.hearts[0],
#             x1, new_y1 - radius, new_x1, new_y1 + radius
#         )
#         self.canvas.coords(self.hearts[1],
#             new_x1, new_y1 - radius, x2, new_y1 + radius
#         )
#         self.canvas.coords(self.hearts[2],
#             x1, new_y1, x2, new_y1, (x1 + x2) / 2, y2
#         )
        
#         for heart in self.hearts:
#             self.canvas.itemconfig(heart, state='normal', fill=self.color)
        
#         self.coords = (x1, y1)
        
#     def delete_heart(self, hide: bool = True):
#         if self.hearts is None:
#             return None
        
#         if hide:
#             for heart in self.hearts:
#                 self.canvas.itemconfig(heart, state="hidden")
#             return None
        
#         for heart in self.hearts:
#             self.canvas.delete(heart)
#         self.hearts = None
        
    
#     def new_heart(self, coordinates):
#         if self.hearts == () or self.hearts is None:
#             self._create_heart_shape(coordinates)
#         else:
#             self._move_resize_heart_shape(coordinates)
             
#     def change_color(self, color: str):
#         self.color = color
        
#         if self.hearts is None:
#             return None
        
#         for heart in self.hearts:
#             self.canvas.itemconfig(heart, fill=self.color)
    
#     def change_size(self, box_size: int):
#         self.box_size = box_size
        
#         if self.hearts is None:
#             return None
        
#         self._move_resize_heart_shape(self.coords)

# def check_canvas_state():
#     """
#     Check the current state of the canvas and print details.
#     """
#     item_count = len(canvas.find_all())
#     heart_references = len(heart_item.hearts) if heart_item.hearts else 0
#     coords = heart_item.coords if heart_item.coords else "None"
#     list = canvas.find_all()
    
#     print(f"Total items on canvas: {item_count}")
#     print(f"Heart references: {heart_references}")
#     print(f"Heart coordinates: {coords}")
#     print(f"Items list: {list}")

# # Create the main window
# root = tk.Tk()
# root.title("Heart Shape Example")

# # Create a canvas
# canvas = tk.Canvas(root, width=400, height=400)
# canvas.pack()

# # Instantiate the Heart class
# heart_item = Heart(canvas, 50, "red")

# # Define functions to interact with the Heart object
# def create_heart():
#     heart_item.new_heart((100, 100))

# def change_color(selected_color):
#     heart_item.change_color(selected_color)

# def change_size(new_size):
#     heart_item.change_size(new_size)

# def hide_heart():
#     heart_item.delete_heart(hide=False)

# # Buttons to interact with the Heart object
# btn_create_heart = tk.Button(root, text="Create Heart", command=create_heart)
# btn_create_heart.pack()

# # Color options
# colors = ["red", "blue", "green", "yellow", "purple"]
# selected_color = tk.StringVar(root)
# selected_color.set(colors[0])  # default value
# color_menu = tk.OptionMenu(root, selected_color, *colors, command=change_color)
# color_menu.pack()

# # Size scale
# size_scale = tk.Scale(root, from_=10, to=200, orient="horizontal", label="Heart Size", command=lambda val: change_size(int(val)))
# size_scale.set(50)  # default value
# size_scale.pack()

# btn_hide_heart = tk.Button(root, text="Hide Heart", command=hide_heart)
# btn_hide_heart.pack()

# btn_check_canvas = tk.Button(root, text="Check Canvas State", command=check_canvas_state)
# btn_check_canvas.pack()

# # Start the Tkinter event loop
# root.mainloop()


# from tkinter import Tk , Canvas

# root = Tk()

# root.geometry("300x300")

# canvas = Canvas(root, background="pink",width=300 , height=300)

# def create_coin(canvas:Canvas, x1 , y1 , box_size , color):
#     #innerx1 and box_szie
#     innerx1 = (box_size // 10) + x1
#     innery1 = (box_size // 10) + y1
#     inner_boxsize = box_size - (box_size // 10)*2
#     #inner_smile_cords
#     middlex1 = innerx1+(inner_boxsize//2)
#     middley1 = innery1+(inner_boxsize//2)
#     #text_size = pixels * (72 / dpi(96))==0.75
#     text_size = inner_boxsize // 5
#     text_size = int(text_size * 7.5)//2
    
#     canvas.create_oval(x1, y1, x1+box_size, y1+box_size,fill = color, outline = "black")
#     canvas.create_oval(innerx1, innery1, innerx1+inner_boxsize, innerx1+inner_boxsize, outline="black", fill="#FFCC00")
#     canvas.create_text(middlex1 , middley1, text="!",justify="center",fill="black",font=("Arial",text_size,"bold"))

# #coin can use 1,2,3,!

# create_coin(canvas, 50, 50 , 60 , "yellow")


# canvas.pack()

# root.mainloop()

# import tkinter as tk
# from tkinter import colorchooser

# def lighten_hex_color(hex_color, lighten_factor=0.1):
#     if hex_color.startswith('#'):
#         hex_color = hex_color[1:]
#     r = int(hex_color[:2], 16)
#     g = int(hex_color[2:4], 16)
#     b = int(hex_color[4:], 16)
#     r = int(r + (255 - r) * lighten_factor)
#     g = int(g + (255 - g) * lighten_factor)
#     b = int(b + (255 - b) * lighten_factor)
#     r = min(255, max(0, r))
#     g = min(255, max(0, g))
#     b = min(255, max(0, b))
#     lightened_hex_color = f'#{r:02X}{g:02X}{b:02X}'
#     return lightened_hex_color

# def darken_hex_color(hex_color, darken_factor=0.1):
#     if hex_color.startswith('#'):
#         hex_color = hex_color[1:]
#     r = int(hex_color[:2], 16)
#     g = int(hex_color[2:4], 16)
#     b = int(hex_color[4:], 16)
#     r = int(r * (1 - darken_factor))
#     g = int(g * (1 - darken_factor))
#     b = int(b * (1 - darken_factor))
#     r = min(255, max(0, r))
#     g = min(255, max(0, g))
#     b = min(255, max(0, b))
#     darkened_hex_color = f'#{r:02X}{g:02X}{b:02X}'
#     return darkened_hex_color

# def choose_color():
#     color_code = colorchooser.askcolor(title="Choose color")[1]
#     if color_code:
#         color_entry.delete(0, tk.END)
#         color_entry.insert(0, color_code)

# def update_color(action):
#     hex_color = color_entry.get()
#     try:
#         factor = float(factor_entry.get())
#         if not (0 <= factor <= 1):
#             raise ValueError
#     except ValueError:
#         result_label.config(text="Please enter a valid factor between 0 and 1.")
#         return
    
#     if action == "lighten":
#         new_color = lighten_hex_color(hex_color, factor)
#     elif action == "darken":
#         new_color = darken_hex_color(hex_color, factor)

#     original_color_label.config(bg=hex_color)
#     new_color_label.config(bg=new_color)
#     result_label.config(text=f'Original: {hex_color}, New Color: {new_color}')

# root = tk.Tk()
# root.title("Hex Color Modifier")

# tk.Label(root, text="Hex Color:").grid(row=0, column=0, padx=10, pady=10)
# color_entry = tk.Entry(root)
# color_entry.grid(row=0, column=1, padx=10, pady=10)
# tk.Button(root, text="Choose Color", command=choose_color).grid(row=0, column=2, padx=10, pady=10)

# tk.Label(root, text="Factor (0-1):").grid(row=1, column=0, padx=10, pady=10)
# factor_entry = tk.Entry(root)
# factor_entry.grid(row=1, column=1, padx=10, pady=10)

# tk.Button(root, text="Lighten Color", command=lambda: update_color("lighten")).grid(row=2, column=0, pady=10)
# tk.Button(root, text="Darken Color", command=lambda: update_color("darken")).grid(row=2, column=1, pady=10)

# original_color_label = tk.Label(root, text="Original Color", width=20, height=2)
# original_color_label.grid(row=3, column=0, padx=10, pady=10)
# new_color_label = tk.Label(root, text="New Color", width=20, height=2)
# new_color_label.grid(row=3, column=1, padx=10, pady=10)
# result_label = tk.Label(root, text="")
# result_label.grid(row=4, columnspan=3, pady=10)

# root.mainloop()
import tkinter as tk
from tkinter import Canvas
from tkinter.colorchooser import askcolor

def darken_hex_color(hex_color, darken_factor=0.1):
    if hex_color.startswith('#'):
        hex_color = hex_color[1:]
    r = int(hex_color[:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:], 16)
    r = int(r * (1 - darken_factor))
    g = int(g * (1 - darken_factor))
    b = int(b * (1 - darken_factor))
    r = min(255, max(0, r))
    g = min(255, max(0, g))
    b = min(255, max(0, b))
    darkened_hex_color = f'#{r:02X}{g:02X}{b:02X}'
    return darkened_hex_color

class Coin:
    def __init__(self, canvas: Canvas, box_size: int, color: str) -> None:
        self.canvas = canvas
        self.box_size = box_size
        self.color = color
        self.inner_color = darken_hex_color(self.color, 0.2)
        self.coin = None
        self.coords = None
        
    def _create_coin(self, coordinates: tuple[int, int]):
        x1, y1 = coordinates
        self.coords = coordinates
        innerx1 = (self.box_size // 10) + x1
        innery1 = (self.box_size // 10) + y1
        inner_boxsize = self.box_size - (self.box_size // 10) * 2
        middlex1 = innerx1 + (inner_boxsize // 2)
        middley1 = innery1 + (inner_boxsize // 2)
        text_size = inner_boxsize // 5
        text_size = int(text_size * 7.5) // 2
        
        first = self.canvas.create_oval(x1, y1, x1 + self.box_size, y1 + self.box_size, fill=self.color, outline="black")
        second = self.canvas.create_oval(innerx1, innery1, innerx1 + inner_boxsize, innery1 + inner_boxsize, outline="black", fill=self.inner_color)
        third = self.canvas.create_text(middlex1, middley1, text="!", justify="center", fill="black", font=("Arial", text_size, "bold"))
        self.coin = (first, second, third)
    
    def _move_resize_coin_shape(self, coordinates: tuple[int, int]) -> None:
        x1, y1 = coordinates
        self.coords = coordinates
        innerx1 = (self.box_size // 10) + x1
        innery1 = (self.box_size // 10) + y1
        inner_boxsize = self.box_size - (self.box_size // 10) * 2
        middlex1 = innerx1 + (inner_boxsize // 2)
        middley1 = innery1 + (inner_boxsize // 2)
        text_size = inner_boxsize // 5
        text_size = int(text_size * 7.5) // 2
        
        self.canvas.coords(self.coin[0], x1, y1, x1 + self.box_size, y1 + self.box_size)
        self.canvas.coords(self.coin[1], innerx1, innery1, innerx1 + inner_boxsize, innery1 + inner_boxsize)
        self.canvas.coords(self.coin[2], middlex1, middley1)
        
        self.canvas.itemconfig(self.coin[0], state='normal')
        self.canvas.itemconfig(self.coin[1], state='normal')
        self.canvas.itemconfig(self.coin[2], state='normal', font=("Arial", text_size, "bold"))
        
    def delete_heart(self, hide: bool = True) -> None:
        if self.coin is None:
            return None
        
        if hide:
            for coin in self.coin:
                self.canvas.itemconfig(coin, state="hidden")
            return None
        
        for coin in self.coin:
            self.canvas.delete(coin)
        self.coin = None
        
    def new_heart(self, coordinates):
        if self.coin is None:
            self._create_coin(coordinates)
        else:
            self._move_resize_coin_shape(coordinates)
            
    def change_color(self, color: str):
        self.color = color
        self.inner_color = darken_hex_color(self.color, 0.2)
        
        if self.coin is None:
            return None
        
        self.canvas.itemconfig(self.coin[0], fill=self.color)
        self.canvas.itemconfig(self.coin[1], fill=self.inner_color)
    
    def change_size(self, box_size: int):
        self.box_size = box_size
        
        if self.coin is None:
            return None
        self._move_resize_coin_shape(self.coords)

def choose_color():
    color = askcolor(title="Choose color")[1]
    if color:
        color_entry.delete(0, tk.END)
        color_entry.insert(0, color)

def update_coin():
    x = int(x_entry.get())
    y = int(y_entry.get())
    box_size = int(size_entry.get())
    color = color_entry.get()
    coin.change_color(color)
    coin.change_size(box_size)
    coin.new_heart((x, y))
    print(canvas.find_all())

def hide_coin():
    coin.delete_heart(hide=True)

def delete_coin():
    coin.delete_heart(hide=False)

# Create the main window
root = tk.Tk()
root.title("Coin Tester")

# Create the canvas
canvas = tk.Canvas(root, width=400, height=400, bg="white")
canvas.grid(row=0, columnspan=4)

# Create the Coin object
coin = Coin(canvas, 50, "#FFD700")

# Input fields
tk.Label(root, text="X:").grid(row=1, column=0)
x_entry = tk.Entry(root)
x_entry.grid(row=1, column=1)
x_entry.insert(0, "50")

tk.Label(root, text="Y:").grid(row=2, column=0)
y_entry = tk.Entry(root)
y_entry.grid(row=2, column=1)
y_entry.insert(0, "50")

tk.Label(root, text="Size:").grid(row=3, column=0)
size_entry = tk.Entry(root)
size_entry.grid(row=3, column=1)
size_entry.insert(0, "50")

tk.Label(root, text="Color:").grid(row=4, column=0)
color_entry = tk.Entry(root)
color_entry.grid(row=4, column=1)
color_entry.insert(0, "#FFD700")
tk.Button(root, text="Choose Color", command=choose_color).grid(row=4, column=2)

# Action buttons
tk.Button(root, text="Update Coin", command=update_coin).grid(row=5, column=0, columnspan=2)
tk.Button(root, text="Hide Coin", command=hide_coin).grid(row=5, column=2)
tk.Button(root, text="Delete Coin", command=delete_coin).grid(row=5, column=3)

# Run the application
root.mainloop()
# import tkinter as tk
# from tkinter import Canvas
# from tkinter.colorchooser import askcolor

# class Heart:
#     """
#     This class helps create hearts, remove hearts, and manipulate heart shapes on a canvas.
#     This class will not perform any calculations for coordinates.
    
#     Attributes:
#         canvas (Canvas): The canvas on which the heart shapes will be drawn.
#         box_size (int): The size of the heart shape.
#         color (str): The color of the heart shape.
#         hearts (tuple): A tuple containing the IDs of the components of the heart shape on the canvas.
#         coords (tuple): The coordinates of the heart shape.
#     """
#     def __init__(self, canvas: Canvas, box_size: int, color: str) -> None:
#         """
#         Initializes a Heart object with the given canvas, box size, and color.

#         Args:
#             canvas (Canvas): The canvas on which the heart shape will be drawn.
#             box_size (int): The size of the heart shape.
#             color (str): The color of the heart shape.

#         Returns:
#             None
#         """
#         self.canvas = canvas
#         self.box_size = box_size
#         self.color = color
        
#         self.hearts = None
#         self.coords = None
            
#     def _create_heart_shape(self, coordinates: tuple[int, int], return_: bool = False):
#         """
#         Draws a heart shape on the canvas.

#         Args:
#             coordinates (tuple[int, int]): The x and y coordinates where the heart will be drawn.
#             return_ (bool): Asking if the item it should be returned or not, default is False

#         Note:
#             This method can be a cause of data leakage, use it carefully.
#         """
#         x1, y1 = coordinates
#         x2, y2 = x1 + self.box_size, y1 + self.box_size
#         self.coords = (x1, y1)

#         new_y1 = (self.box_size / 2) + y1
#         new_x1 = (self.box_size / 2) + x1
#         radius = (new_y1 - y1) / 2
        
#         first = self.canvas.create_arc(x1, new_y1 - radius, new_x1, new_y1 + radius, fill=self.color, start=0, extent=180)
#         second = self.canvas.create_arc(new_x1, new_y1 - radius, x2, new_y1 + radius, fill=self.color, start=0, extent=180)
#         third = self.canvas.create_polygon(x1, new_y1, x2, new_y1, (x1 + x2) / 2, y2, fill=self.color)
        
#         if return_:
#             return (first, second, third)
#         self.hearts = (first, second, third)
    
#     def _move_resize_heart_shape(self, coordinates: tuple[int, int], heart: tuple = None):
#         """
#         Moves and resizes the heart shape on the canvas.

#         Args:
#             coordinates (tuple[int, int]): The new x and y coordinates for the heart shape.
#             heart (tuple): This method takes heart items tuple; should be the same canvas as this method's canvas holds. Default is None. If not given, takes self.hearts.

#         Returns:
#             None
#         """
#         if not heart:
#             heart = self.hearts
            
#         x1, y1 = coordinates
#         x2, y2 = x1 + self.box_size, y1 + self.box_size

#         new_y1 = (self.box_size / 2) + y1
#         new_x1 = (self.box_size / 2) + x1
#         radius = (new_y1 - y1) / 2
#         self.coords = (x1, y1)
        
#         self.canvas.coords(heart[0], x1, new_y1 - radius, new_x1, new_y1 + radius)
#         self.canvas.coords(heart[1], new_x1, new_y1 - radius, x2, new_y1 + radius)
#         self.canvas.coords(heart[2], x1, new_y1, x2, new_y1, (x1 + x2) / 2, y2)
        
#         for body in heart:
#             self.canvas.itemconfig(body, state='normal', fill=self.color)
        
#     def delete_heart(self, hide: bool = True) -> None:
#         """
#         Deletes or hides the heart shape from the canvas.

#         Args:
#             hide (bool): If True, hides the heart shape instead of deleting it.

#         Returns:
#             None
#         """
#         if self.hearts is None:
#             return None
        
#         if hide:
#             for heart in self.hearts:
#                 self.canvas.itemconfig(heart, state="hidden")
#             return None
        
#         for heart in self.hearts:
#             self.canvas.delete(heart)
#         self.hearts = None
        
#     def new_heart(self, coordinates):
#         """
#         Creates a new heart shape on the canvas.

#         Args:
#             coordinates (tuple[int, int]): The x and y coordinates where the heart will be drawn.

#         Returns:
#             None
#         """
#         if self.hearts is None:
#             self._create_heart_shape(coordinates)
#         else:
#             self._move_resize_heart_shape(coordinates)
            
#     def change_color(self, color: str):
#         """
#         Changes the color of the heart shape.

#         Args:
#             color (str): The new color of the heart shape.

#         Returns:
#             None
#         """
#         self.color = color
        
#         if self.hearts is None:
#             return None
        
#         for heart in self.hearts:
#             self.canvas.itemconfig(heart, fill=self.color)
    
#     def change_size(self, box_size: int):
#         """
#         Changes the size of the heart shape.

#         Args:
#             box_size (int): The new size of the heart shape.

#         Returns:
#             None
#         """
#         self.box_size = box_size
        
#         if self.hearts is None:
#             return None
#         self._move_resize_heart_shape(self.coords)

# def choose_color():
#     color = askcolor(title="Choose color")[1]
#     if color:
#         color_entry.delete(0, tk.END)
#         color_entry.insert(0, color)

# def update_heart():
#     x = int(x_entry.get())
#     y = int(y_entry.get())
#     box_size = int(size_entry.get())
#     color = color_entry.get()
#     heart.change_color(color)
#     heart.change_size(box_size)
#     heart.new_heart((x, y))
#     print(canvas.find_all())

# def hide_heart():
#     heart.delete_heart(hide=True)

# def delete_heart():
#     heart.delete_heart(hide=False)

# # Create the main window
# root = tk.Tk()
# root.title("Heart Tester")

# # Create the canvas
# canvas = tk.Canvas(root, width=400, height=400, bg="white")
# canvas.grid(row=0, columnspan=4)

# # Create the Heart object
# heart = Heart(canvas, 50, "#FF0000")

# # Input fields
# tk.Label(root, text="X:").grid(row=1, column=0)
# x_entry = tk.Entry(root)
# x_entry.grid(row=1, column=1)
# x_entry.insert(0, "50")

# tk.Label(root, text="Y:").grid(row=2, column=0)
# y_entry = tk.Entry(root)
# y_entry.grid(row=2, column=1)
# y_entry.insert(0, "50")

# tk.Label(root, text="Size:").grid(row=3, column=0)
# size_entry = tk.Entry(root)
# size_entry.grid(row=3, column=1)
# size_entry.insert(0, "50")

# tk.Label(root, text="Color:").grid(row=4, column=0)
# color_entry = tk.Entry(root)
# color_entry.grid(row=4, column=1)
# color_entry.insert(0, "#FF0000")
# tk.Button(root, text="Choose Color", command=choose_color).grid(row=4, column=2)

# # Action buttons
# tk.Button(root, text="Update Heart", command=update_heart).grid(row=5, column=0, columnspan=2)
# tk.Button(root, text="Hide Heart", command=hide_heart).grid(row=5, column=2)
# tk.Button(root, text="Delete Heart", command=delete_heart).grid(row=5, column=3)

# # Run the application
# root.mainloop()
