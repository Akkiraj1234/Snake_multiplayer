from tkinter import Canvas, Frame, Button, Label, Entry, Toplevel, Tk
from random import choice
from game_idles import Food,goofy_Snakes


class inisial_screens:
    """A class representing an initial screen setup for a game.

    This class provides methods for setting up the initial screen of a game, including adding snakes, food items, starting animations, and managing animations.

    Attributes:
        master: The master widget where the initial screen will be placed.
        background_color (str): The background color of the game screen.
        game_width (int): The width of the game screen.
        box_size (int): The size of each box or unit in the game grid.
        game_height (int): The height of the game screen.
        speed (int): The speed of animations in milliseconds.
        child_window (tkinter.Canvas): The canvas widget representing the game screen.
        food (Food): The food item on the game screen.
        snakes (list): A list containing snake objects on the game screen.
        animation_after_ids: A reference to the animation after method IDs for managing animation loops.

    Methods:
        __init__: Initializes the initial screen with provided parameters.
        add_snakes: Adds a snake to the game screen.
        add_food: Adds a food item to the game screen.
        start_animation: Starts the animation loop for moving snakes and updating the game state.
        stop_animation: Stops the animation loop.
        add_button: Adds a button widget to the game screen.

    Example:
        # Initialize the initial screen
        initial_screen = inisial_screens(master, background_color='black', game_width=800, box_size=20, game_height=600, speed=100)

        # Add a snake to the initial screen
        initial_screen.add_snakes(color='green', coordinates=(5, 5), length=3, direction='right')

        # Add food to the initial screen
        initial_screen.add_food(color='red', food_type='oval', random_color=True)

        # Start the animation loop
        initial_screen.start_animation()

        # Stop the animation loop
        initial_screen.stop_animation()

        # Add a button to the game screen
        initial_screen.add_button(button1, button2, button3)
    """
    
    def __init__(self,master,background_color:str,game_width:int,box_size:int, game_height:int,speed:int,pack=True) -> None:
        """Initialize the initial screen of the game.

        Args:
            master: The master widget where the initial screen will be placed.
            background_color (str): The background color of the game screen.
            game_width (int): The width of the game screen.
            box_size (int): The size of each box or unit in the game grid.
            game_height (int): The height of the game screen.
            speed (int): The speed of animations in milliseconds.
            pack (bool): Whether to automatically pack the canvas widget (default is True).
        """
        self.master = master
        self.background_color = background_color
        self.game_width = game_width
        self.game_height = game_height
        self.box_size = box_size
        self.speed=speed
        
        self.child_window = Canvas(self.master,bg=self.background_color,height=self.game_height,width=self.game_width)
        if pack: self.child_window.pack()
        self.food = None
        self.snakes = []
        self.Windows_list = []
        self.animation_after_ids=None
    
    def add_snakes(self, color:str ,coordinates:tuple, lenght:int, direction:str)-> None:
        """Add a snake to the game screen.

        Args:
            color (str): The color of the snake.
            coordinates (tuple): The initial coordinates of the snake.
            length (int): The length of the snake.
            direction (str): The initial direction of the snake ('up', 'down', 'left', 'right').
        """
        coordinates = [i * self.box_size for i in coordinates]
        self.snakes.append(
            goofy_Snakes(self.child_window,color,coordinates,lenght,direction,self.box_size)
        )
    
    def add_food(self, color:str, food_type="oval",randome_color=False):
        """Add a food item to the game screen.

        Args:
            color (str): The color of the food item.
            food_type (str): The type of food item ('oval' or 'rectangle', default is 'oval').
            random_color (bool): Whether to randomize the color of the food item (default is False).
        """
        self.food_type=food_type
        self.random_color=randome_color
        self.food=Food(self.child_window, self.box_size, color, self.game_width, self.game_height, food_type)
        
    def add_button(self,*args):
        """Add button widgets to the game screen.

        Args:
            *buttons: Button widgets to be added to the game screen.
        """
        self.Windows_list = args
        
        num = self.box_size-(self.box_size*2)
        for button in args:
            self.child_window.create_window(self.game_width//2,self.game_height//2+num,window=button)
            num += self.box_size
        
    def start_animation(self):
        """Start the animation loop for moving snakes and updating the game state."""
        for snake in self.snakes:
            snake.move_the_snakes()
            x,y= snake.coordinates
            foodx,foody=self.food.x,self.food.y
            if x == foodx and y == foody:
                if self.random_color:
                    self.food.color = choice(("blue","yellow","red","pink"))
                self.food.new_food(self.food_type)
        self.animation_after_ids=self.child_window.after(self.speed,self.start_animation)
    
    def stop_animation(self):
        """Stop the animation loop."""
        if self.animation_after_ids:
            self.child_window.after_cancel(self.animation_after_ids)
        
    def add_to_master(self):
        '''add to the master'''
        self.child_window.pack()
        
    def remove_from_master(self):
        '''remove window from master'''
        self.stop_animation()
        self.child_window.pack_forget()
        


class WindowGenerator:
    """
    A class for managing window settings and operations.

    Attributes:
        root (Tk): The main Tkinter root window.
        master (Frame): The master frame to contain the windows.
        height (int): The height of the windows.
        width (int): The width of the windows.
        theme (tuple[str,str]): A tuple containing theme colors.
        font_size (int): The font size for texts.
        __value (list): A private list to capture values from entry widgets.
    """
    def __init__(self,root:Tk ,theme:tuple[str,str] ,font_size:int, height:int, width:int) -> None:
        """
        Initialize the setting window screen with specified parameters.

        Args:
            root (Tk): The main Tkinter root window.
            theme (tuple[str,str]): A tuple containing theme colors.
            font_size (int): The font size for texts.
        """
        self.root = root
        self.theme1 = theme[0]
        self.theme2 = theme[1]
        self.font_s = font_size
        self.height = height
        self.width = width
        self.__value = None
        self.font = "Myanmar Text"

    def Inisial_screen(self, master:Frame, text:str = "demo texxt") -> Canvas:
        """
        Create an initial screen canvas with specified parameters.

        Args:
            master (tkinter.Widget): The master widget to contain the canvas.
            height (int): The height of the canvas.
            widths (int): The width of the canvas.
            text (str, optional): The text to display on the canvas. Defaults to "demo texxt".

        Returns:
            Canvas: The canvas containing the initial screen with the specified text.
        """
        inisial_screen = Canvas(
            master = master,
            height = self.height,
            width = self.width,
            bg = self.theme1
        )
        inisial_screen.create_text(
            self.width // 2 , self.height // 2,
            font = (self.font, self.font_s, 'bold'),
            text = text,
            fill = self.theme2,
        )
        return inisial_screen
    
    def creating_form_on_canvas(self, height:int, width:int, canvas:Canvas,*args:tuple) -> Canvas:
        '''
        this method create a form on a canvas and return it
        
        Argument:
            - width and height of the window
            - a canvas type obj by tk
            - takes tupple as an argument containing 2 obj
            - 1st obj => the left side of window
            - 2nd obj => the ryt side of window
        
        Return:
            - the canvas containg a form
        
        Note:
            - if u wanna add a window in middle horigentally so just 
                add one window in a tuple or add other artibute as none
                ex :- (window , None) or (None , window)
        
        Example:
            >>> tuple_obj = (window1 ,window2) or (window1 , None)
            >>> canvas = creating_form_on_canvas(
                canvas = canvas , 300 , 600,
                (widget , widget1) , (lable1 , entry1 ),
                (widget2 , None ) , (window5 , canvas1)
            )
        '''
        #calculation of diameters :0
        middle1 = width // 4
        middle2 = middle1 *3
        distance = height // len(args)-1
        start = distance * 2 // 3
        
        # adding to the window :0
        for left , right in args:
            
            if not (left and right):
                canvas.create_window(middle1 *2 ,start ,window =left or right)
                start += distance
                continue
            #addig_both_window_left and ryt
            canvas.create_window(middle1 , start , window = left)
            canvas.create_window(middle2 , start , window = right)
            start += distance
        
        #returning the canvas         
        return canvas
    
    def create_top_level_screen(self, title:str, color:str, width:int, height:int) -> Toplevel:
        """
        Create a temporary top-level window and return it.

        This method creates a top-level window with the specified title, background color, width, and height.
        The main window (root) is disabled while the top-level window is open, and re-enabled when it is closed.

        Parameters:
        title (str): The window title.
        color (str): The background color.
        width (int): The window width.
        height (int): The window height.

        Returns:
            Toplevel: The created top-level window.
        
        """
        window = Toplevel(self.root, bg = color)
        window.title(title)
        window.geometry(f"{width}x{height}")
        self.root.attributes('-disabled', True)
        
        def on_close():
            self.root.attributes('-disabled', False)
            window.destroy()
        
        window.protocol("WM_DELETE_WINDOW", on_close)
        window.grab_set()
        window.focus_set()
        
        return window

    def taking_password_for_verification_window(self) -> str:
        """
        Create a temp window for taking password input from the user and return the entered password.

        This method displays a top-level window titled 'Verify Password' with a password entry field.
        After the user enters the password and clicks the 'continue' button, the window closes, and the entered password is returned.

        Returns:
            str: The password entered by the user.

        Note:
            The password entry field is masked for security, displaying asterisks instead of the actual characters.
        """
        self.__value == None
        
        window = self.create_top_level_screen(
            title = "Verify Password",
            width = 200,
            height = 90,
            color = "#e6f2ff"
        )
        
        frame1 = Frame(window , bg = "#e6f2ff" , padx= 5 ,pady=5)
        
        lable1 = Label(
            master = frame1, 
            relief="flat", 
            text="password :",
            font = (self.font ,8,"bold"),
            bg="#e6f2ff",fg= "black" 
        )
        password1 = Entry(
            master = frame1,
            width = 15,bd = 1,
            relief="solid",
            justify="center",
            show = "*",
            font=(self.font ,8,"bold")
        )
        button = Button(
            master = frame1,
            relief="solid",
            text= "continue",
            bg= "#e6f2ff" ,fg="black",
            font = (self.font ,8,"bold"),
            command= lambda : self.__capture_and_close(password1 , window = window ,root_enable = True)
        )
        
        lable1.grid(row=0, column=0 , padx= 5, pady= 5)
        password1.grid(row=0 , column=1 , padx=5, pady=5)
        button.grid(row=1,column=0,columnspan=2,sticky='ew', padx=5)
        frame1.pack()
        window.wait_window(window)
        
        return self.__value[0]

    def change_password_window(self):
        """
        Create a window for changing the password.

        This method creates a temp top-level window titled 'Update Password' with fields to enter and verify a new password.
        After entering the new passwords and clicking the 'continue' button, the window closes.

        Returns:
            list: A list containing the new passwords entered by the user.

        Note:
            Passwords entered are masked for security, displaying asterisks instead of the actual characters.
        """
        self.__value = (None , None)
        
        window = self.create_top_level_screen(
            title = "Update Password",
            width = 260,
            height = 130,
            color = "#e6f2ff"
        )
        frame1 = Frame(window ,bg = "#e6f2ff")
        
        label1 = Label(
            master = frame1,
            text = "Enter New Password",
            relief = "flat",
            bg ="#e6f2ff",fg ="black",
            font = (self.font ,8,"bold")
        )
        label2 = Label(
            master = frame1,
            text = "Verify New Password",
            relief = "flat",
            bg ="#e6f2ff",fg ="black",
            font = (self.font ,8,"bold")
        )
        password1 = Entry(
            master = frame1,
            width = 15,bd = 1,
            relief="solid",
            justify="center",
            show = "*",
            font=(self.font ,8,"bold")
        )
        password2 = Entry(
            master = frame1,
            width = 15,bd = 1,
            relief="solid",
            justify="center",
            show = "*",
            font=(self.font ,8,"bold")
        )
        button = Button(
            master = frame1,
            relief="solid",
            text= "continue",
            bg= "#e6f2ff" ,fg="black",
            font = (self.font ,8,"bold"),
            command= lambda : self.__capture_and_close(password1 , password2 , window = window , root_enable = True)
        )
        label1.grid(row=0,column=0,padx=5,pady=5)
        label2.grid(row=1,column=0,padx=5,pady=5)
        password1.grid(row=0,column=1,padx=5,pady=5)
        password2.grid(row=1,column=1,padx=5,pady=5)
        button.grid(row=2,column=0,columnspan=2,sticky='ew', padx=5, pady=5)
        
        frame1.pack()
        window.wait_window(window)
        
        return self.__value
    
    def create_new_account_window(self):
        print("will come soon")
        
    def change_account_window(self):
        print("will come soon")
               
    def __capture_and_close(self, *entry_widget, window ,root_enable:bool):
        """
        Capture the entry value from the entry widget, close the window, and optionally enable the root window.

        Args:
            entry_widget (tk.Entry): The entry widget from which to capture the value.
            window (tk.Toplevel): The window to be closed.
            root (tk.Tk): The root window to be enabled if root_enable is True.
            root_enable (bool): A flag indicating whether to enable the root window.
        """
        self.__value = [widget.get()  for widget in entry_widget]
        window.destroy()
        
        if root_enable:
            self.root.attributes('-disabled', False)
            self.root.grab_set()
            self.root.focus_set()