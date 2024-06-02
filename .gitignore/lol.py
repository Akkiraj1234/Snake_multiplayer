import tkinter as tk

class CanvasApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x400")
        
        # Frame for canvas
        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Canvas
        self.canvas = tk.Canvas(self.canvas_frame, width=400, height=400, bg='white')
        self.canvas.pack()
        
        # Frame for options
        self.options_frame = None
        
        # Draw initial items
        self.draw_initial()
        
    def draw_initial(self):
        self.rect = self.canvas.create_rectangle(50, 50, 150, 150, fill='blue', tags="item")
        self.oval = self.canvas.create_oval(200, 200, 300, 300, fill='red', tags="item")
        
        # Bind click event to items
        self.canvas.tag_bind("item", "<Button-1>", self.on_item_click)

    def on_item_click(self, event):
        # Get the clicked item
        item = self.canvas.find_withtag(tk.CURRENT)
        
        # Show options for the selected item
        self.show_options(item)
        
    def show_options(self, item):
        # Destroy previous options frame
        if self.options_frame:
            self.options_frame.destroy()
        
        # Create a new options frame
        self.options_frame = tk.Frame(self.root)
        self.options_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Example options for the selected item
        tk.Label(self.options_frame, text="Options for selected item:").pack()
        
        # Color change option
        tk.Button(self.options_frame, text="Change to Green", command=lambda: self.change_color(item, 'green')).pack()
        tk.Button(self.options_frame, text="Change to Yellow", command=lambda: self.change_color(item, 'yellow')).pack()
    
    def change_color(self, item, color):
        self.canvas.itemconfig(item, fill=color)

root = tk.Tk()
app = CanvasApp(root)
root.mainloop()
