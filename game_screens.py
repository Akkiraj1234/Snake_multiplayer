from tkinter import Canvas, Frame, Button, Label, Entry, Toplevel ,Tk, messagebox, StringVar, Scale, OptionMenu, END
from random import choice

from game_idles import *
from variable import Variable, demo_variable
from helper import deep_copy, darken_hex_color


class Game_screen:
    """
    Class to manage the game screen, including navigation setup,
    game canvas setup, updating game elements, and adding/removing
    from the master widget.

    Attributes:
        var (variable): An object containing game variables.
        MASTER (Tk): The parent Tkinter window.
        NEVIGATION_CANVAS (Canvas): The canvas for navigation elements.
        GAME_CANVAS (Canvas): The canvas for game elements.
        SNAKE (Snake): The snake object.
        FOOD (Food): The food object.
        HEART (Heart): The heart object.
        MENU_OPTION (Text): The menu option text.
        SCORE_TEXT (Text): The score text.
        _game_bord_height (int): Height of the game board.
        _nevigation_height (int): Height of the navigation canvas.

    Methods:
        __init__(Master, var): Initializes the game screen.
        adjust_window_size(): Adjusts window size based on game and navigation heights.
        nevigation_setup(): Sets up the navigation canvas with heart, score text, and menu option.
        game_canvas_setup(): Sets up the game canvas with snake and food.
        update_things(**kwargs): Updates game elements based on provided keyword arguments.
        add_to_Master(): Packs the navigation and game canvases.
        remove_to_Master(): Removes navigation and game canvases from master widget.
    """
   
    def __init__(self,Master:Tk, var:Variable) -> None:
        """
        Initialize the game screen. 
        with main game canvas and nevigation panel
        and sneck ,  food in hevigation heart score board,
        and menu option

        Args:
            Master (Tk): The parent Tkinter window.
            var (variable): An object containing game variables.
        
        Note: 
            1. this method directly interect with variable method
        """
   
        self.var = var
        self.root = Master
        self.MASTER = Frame(self.root)
        self.var1 = None
        self.demo = False
        
        self.NEVIGATION_CANVAS = None
        self.GAME_CANVAS = None
        self.SNAKE = None
        self.FOOD = None
        self.HEART = None
        self.COIN = None
        self.HEART_NEW = None
        self.MENU_OPTION = None
        self.SCORE_TEXT = None
        
        self.inisialize()
    
    def inisialize(self):
        self.nevigation_setup()
        self.game_canvas_setup()
    
    def nevigation_setup(self) -> None:
        """
        This method sets up the navigation canvas with essential elements such as a heart icon
        representing the player's remaining lives, a score text displaying the current score,
        and a menu option for accessing game options or pausing the game.
        """
        var = self.var if not self.demo else self.var1
        
        self.NEVIGATION_CANVAS = Canvas(
            master = self.MASTER
            )
        
        self.HEART_NEW = Heart_NEV(
            canvas = self.NEVIGATION_CANVAS,
            color = var.HEART_COLOR,
            initial_heart = var.INISISAL_HEART,
            limit = var.HEART_LIMIT
            )
        
        self.SCORE_TEXT = self.NEVIGATION_CANVAS.create_text(
            0 , 0 ,
            text = f"Score: 0",
            )
        
        self.MENU_OPTION = self.NEVIGATION_CANVAS.create_text(
            0 , 0 ,
            text = "Menu",
            )  
        self.NEVIGATION_CANVAS.pack()
    
    def game_canvas_setup(self) -> None:
        """
        This method sets up the game canvas with the snake and food objects.
        It creates a canvas widget with the specified background color, width,
        and height. Then, it initializes the snake and food objects on the canvas
        using the provided game variables.
        """
        var = self.var if not self.demo else self.var1
        
        self.GAME_CANVAS = Canvas(
            master = self.MASTER,
            bg = var.CANVAS_COLOR
            )
        
        self.SNAKE = Snake(
            canvas = self.GAME_CANVAS,
            coordinates = var.SNAKE_CORDINATES,
            box_size = var.game_box_size,
            lenght = var.SNAKE_LENGHT,
            color = var.SNAKE_COLOR
            )
        
        self.FOOD = Food(
            canvas = self.GAME_CANVAS,
            box_size = var.game_box_size,
            color = var.FOOD_COLOR,
            )
        
        self.HEART = Heart(
            canvas = self.GAME_CANVAS,
            box_size = var.game_box_size,
            color = var.HEART_COLOR
        )
        
        self.COIN = Coin(
            canvas = self.GAME_CANVAS,
            box_size = var.game_box_size,
            color = var.COIN_COLOR
        )
        self.HEART.delete_all()
        self.COIN.delete_all()
        
        self.GAME_CANVAS.pack()
        
    def adjust_window_size(self) -> None:
        """
        Adjust the window size based on game height and navigation heights.
        
        Note:
            The navigation height is calculated as one-eighth of the game height,
            but if the calculated height is less than or equal to the size of game
            boxes, it defaults to the size of game boxes.
        
        Attributes created:
            _nevigation_height (int): The height of the navigation canvas.
            _game_bord_height (int): The height of the game board canvas.
        """
        var = self.var if not self.demo else self.var1
        #game_variables
        self.game_height = var.game_height
        self.game_width = var.game_width
        self._game_bord_height = None
        self._nevigation_height = None
        
        nevigation_h = self.game_height // 8
        nevigation_height = nevigation_h // var.game_box_size
        
        if not bool(nevigation_height):
            self._nevigation_height = nevigation_h
        else:
            self._nevigation_height = var.game_box_size
            
        self._game_bord_height = self.game_height - self._nevigation_height
            
    def UPDATE(self) -> None:
        """
        this method update all elemets posstion and color acording to new one
        """
        self.adjust_window_size()
        
        var = self.var if not self.demo else self.var1
        
        #updating nevigation and its itemes================
        braking_into_4 =  self._nevigation_height // 4
        
        if self.NEVIGATION_CANVAS: self.NEVIGATION_CANVAS.config(
            bg = var.NEV_COLOR,
            width = self.game_width,
            height = self._nevigation_height
            )
        
        if self.HEART_NEW:
            self.HEART_NEW.update_color(var.HEART_COLOR)
            self.HEART_NEW.update_size()
            self.HEART_NEW.initial_heart = var.INISISAL_HEART
            self.HEART_NEW.limit = var.HEART_LIMIT
        
        if self.SCORE_TEXT and self.MENU_OPTION:
            #tuple1 contain text id and its x cords
            tuple1 = ((self.SCORE_TEXT,self.game_width // 2), (self.MENU_OPTION,braking_into_4 * 4))
            
            for text_id , xcords in tuple1:
                # updating color and size
                self.NEVIGATION_CANVAS.itemconfig(
                    text_id,
                    font = ("Arial",braking_into_4 * 2,"bold"),
                    fill = var.TEXT_COLOR
                )
                # updating postion.
                self.NEVIGATION_CANVAS.coords(
                    text_id,
                    xcords,#x
                    braking_into_4 * 2#y
                )
        #updating canvas and its itemes===================
        if self.GAME_CANVAS: self.GAME_CANVAS.config(
            bg = var.CANVAS_COLOR,
            width = self.game_width,
            height = self._game_bord_height
            )
        if self.SNAKE: 
            self.SNAKE.update_color(var.SNAKE_COLOR)
            self.SNAKE.lenght = var.SNAKE_LENGHT
            
        if self.FOOD: 
            self.FOOD.update_color(var.FOOD_COLOR)
            self.FOOD._calculate_dimension()
            
        if self.HEART: 
            self.HEART.update_color(var.HEART_COLOR)
            self.HEART._calculate_dimension()
            
        if self.COIN: 
            self.COIN.update_color(var.COIN_COLOR)
            self.COIN._calculate_dimension()
    
    def update_text(self, color:str) -> None:
        tuple1 = (self.SCORE_TEXT, self.MENU_OPTION)
        
        if self.SCORE_TEXT and self.MENU_OPTION:
            
            for text_id in tuple1:
                self.NEVIGATION_CANVAS.itemconfig(
                        text_id,
                        fill = color
                    )
                
    def update_things(self,**kwargs) -> None:
        """
        Update game elements based on provided keyword arguments.

        Args:
            **kwargs: Keyword arguments to update game elements. Available args:
                      - score: Score to be updated.
        """
        if kwargs.get('score',None) is not None:
            self.NEVIGATION_CANVAS.itemconfig(
                self.SCORE_TEXT,text=f"Score: {kwargs['score']}"
            )
            print("updated ",kwargs['score'])
        else:
            print("error : 0012, cant update text of score !") 

    def demo_screen_var_update(self, **kwargs) -> demo_variable:
        """
        Update screen variables with provided keyword arguments and optionally initialize the screen.
        
        Args:
            initialize (bool, optional): Whether to call the SET_UP method after updating variables. Defaults to False.
            
            **kwargs: Arbitrary keyword arguments for updating screen variables. Expected keys:\
                    game_height , game_width , game_box_size , HEART_LIMIT , INISISAL_HEART
                    HEART_COLOR,  NEV_COLOR , TEXT_COLOR , CANVAS_COLOR , COIN_COLOR
                    FOOD_COLOR , SNAKE_COLOR , SNAKE_CORDINATES , SNAKE_LENGHT
                
        Returns:
            tuple: _description_
        """        
        var = {
            "game_height" : self.var.game_height,
            "game_width" : self.var.game_width,
            "game_box_size": self.var.game_box_size,
            "HEART_LIMIT":self.var.HEART_LIMIT,
            "INISISAL_HEART":self.var.INISISAL_HEART,
            "HEART_COLOR":self.var.HEART_COLOR,
            "NEV_COLOR": self.var.NEV_COLOR,
            "TEXT_COLOR":self.var.TEXT_COLOR,
            "CANVAS_COLOR":self.var.CANVAS_COLOR,
            "FOOD_COLOR":self.var.FOOD_COLOR,
            "COIN_COLOR":self.var.COIN_COLOR,
            "SNAKE_COLOR":self.var.SNAKE_COLOR,
            "SNAKE_LENGHT":self.var.SNAKE_LENGHT,
            "SNAKE_CORDINATES":self.var.SNAKE_CORDINATES,
        }
        var.update(kwargs)
        self.demo = True
        
        if self.var1 is None:
            self.var1 = demo_variable(var)
        else:
            self.var1.update_with_dict(var)
        
        self.UPDATE()
        return var
        
    def add_to_Master(self) -> None:
        """
        Pack the navigation and game canvases and add it to master
        """
        self.MASTER.pack()  

    def remove_to_Master(self)-> None:
        """
        remove the navigation and game canvases. from master
        """
        self.MASTER.pack_forget()


class inisial_screens:
    
    """
    A class representing an initial screen setup for a game.

    This class provides methods for setting up the initial screen of a game, including adding snakes, food items, starting animations, and managing animations.

    Attributes:
        master (Tk | Frame): The master widget where the initial screen will be placed.
        background_color (str): The background color of the game screen.
        game_width (int): The width of the game screen.
        game_height (int): The height of the game screen.
        box_size (int): The size of each box or unit in the game grid.
        speed (int): The speed of animations in milliseconds.
        child_window (tkinter.Canvas): The canvas widget representing the game screen.
        food (Food): The food item on the game screen.
        heart (Heart): The heart item on the game screen.
        coin (Coin): The coin item on the game screen.
        snakes (list): A list containing snake objects on the game screen.
        Windows_list (list): A list of additional widgets (windows) added to the game screen.
        Header (list): A list containing header widgets placed at the top of the game screen.
        footer (list): A list containing footer widgets placed at the bottom of the game screen.
        methods (list): A list to store methods for deferred execution.
        color_list (list): A list of predefined colors for game elements.

    Methods:
        __init__: Initializes the initial screen with provided parameters.
        add_snakes: Adds a snake to the game screen.
        add_food: Adds a food item to the game screen.
        add_heart: Adds a heart item to the game screen.
        add_coin: Adds a coin item to the game screen.
        add_windows: Adds window widgets to the game screen.
        add_header: Adds header widgets to the game screen.
        add_footer: Adds footer widgets to the game screen.
        update_window_size: Updates the positions of all windows on the game screen.
        update_header: Updates the positions of header elements on the game screen.
        update_footer: Updates the positions of footer elements on the game screen.
        update_nessassaery: Appends methods to self.methods and optionally executes them.
        HomeScreen_HeaderFooter_modle1_inisalization: Initializes header and footer with labels and a coin widget.
        start_animation: Starts the animation loop for moving snakes and updating the game state.
        stop_animation: Stops the animation loop.
        update_everything: Updates various attributes, elements, and widgets based on provided variables.
        add_to_master: Adds the game screen to the master widget.
        remove_from_master: Removes the game screen from the master widget.
    
    Note: 
        Note: If you add any more elements to the canvas that are not part of the game_screens 
        method and their size and color can be updated, create a method to update them and append
        it to the self.methods list or through the self.update_message method.
    """
    
    def __init__(self, master:Tk|Frame, background_color:str, game_width:int, game_height:int, box_size:int, pack:bool = True ) -> None:
        """
        Initialize the initial screen of the game.

        Args:
            master (Tk | Frame): The master widget where the initial screen will be placed.
            background_color (str): The background color of the game screen.
            game_width (int): The width of the game screen.
            game_height (int): The height of the game screen.
            box_size (int): The size of each box or unit in the game grid.
            pack (bool): Whether to automatically pack the canvas widget (default is True).
        """
        self.master = master
        self.background_color = background_color
        self.game_width = game_width
        self.game_height = game_height
        self.box_size = box_size
        
        #inisalizing child window
        self.child_window = Canvas(
            master = self.master,
            bg = self.background_color,
            height = self.game_height,
            width = self.game_width
        )
        
        #elements of the game_screen :0
        self.food = None
        self.heart = None
        self.coin = None
        self.snakes = []
        self.Windows_list = []
        self.Header = []
        self.footer = []
        self.methods = []
        self.color_list = [
            "#FFA500", "#800080", "#00FFFF", "#FFD700", "#00FF00",
            "#0000FF", "#FFFF00", "#FF0000", "#FFC0CB"
        ]
        
        #arttibutes used for game_screen elements
        self.random_food_color = False
        self.random_heart_color = False
        self.random_coin_color = False
        #important regardin animation
        self.speed = None
        self.animation_after_ids = None
        #header footer and middele button posstion
        self._middel_windows = 0
        self.header_info = (0,0) #padding x and y
        self.footer_info = (0,0) ##padding x and y
        #windows ids created id on canvas
        self._Windows_ids = []
        self._header_ids = [None,None,None]
        self._footer_ids = [None,None,None]
        
        if pack: 
            self.child_window.pack()
        
    def add_food(self, color:str, randome_color=False) -> None:
        """
        Add a food item to the game screen.

        Args:
            color (str): The color of the food item.
            random_color (bool): Whether to randomize the color of the food item (default is False).
        """
        self.random_food_color = randome_color
        
        self.food=Food(
            canvas = self.child_window,
            box_size = self.box_size,
            color = color,
            initialize = True
        )
        
    def add_heart(self, color:str, randome_color=False) -> None:
        """
        add heart item to the game screen.

        Args:
            color (str): The color of the heart item.
            random_color (bool): Whether to randomize the color of the heart item (default is False).
        """
        self.random_heart_color = randome_color
        
        self.heart = Heart(
            canvas = self.child_window,
            box_size = self.box_size,
            color = color,
            initialize = True
        )
    
    def add_coin(self, color:str, randome_color=False) -> None:
        """
        add coin item to the game screen.

        Args:
            color (str): The color of the coin item
            random_color (bool): Whether to randomize the color of the coin item (default is False).
        """
        self.random_coin_color = randome_color
        
        self.coin = Coin(
            canvas = self.child_window,
            box_size = self.box_size,
            color = color,
            initialize = True
        )
    
    def add_snakes(self, color:str, coordinates:list, lenght:int, direction:str) -> None:
        """
        Add a snake to the game screen.

        Args:
            color (str): The color of the snake.
            coordinates (list): The initial coordinates of the snake. It should be a list of two integers [x, y], 
                                and both coordinates should be divisible by box_size.
            length (int): The length of the snake.
            direction (str): The initial direction of the snake ('up', 'down', 'left', 'right').

        Note:
            The coordinates should be divisible by box_size to ensure proper alignment on the game grid.
        """
        
        # getting the cords in the range not out of game width and height and not less then 0 then * it to get cords
        coordinates[0] = min((self.game_height // self.box_size),max(0,coordinates[0]))*self.box_size
        coordinates[1] = min((self.game_width // self.box_size),max(0,coordinates[1]))*self.box_size
             
        snake = goofy_Snakes(
            master = self.child_window,
            box_size = self.box_size,
            color = color,
            lenght = lenght,
            coordinates = coordinates,
            inisial_direction = direction
        )

        self.snakes.append(snake)
        
    def add_windows(self, *args, middle:int = 1 , destroy:bool = True) -> None:
        """
        Add window widgets to the game screen.

        This method places given widgets (e.g., buttons) on the game screen at a specific 
        position based on the `middle` parameter. It also handles the removal of previously 
        added widgets if called multiple times.

        Args:
            *args: Widgets to be added to the game screen.
            
            middle (int, optional): Determines the vertical offset of the widgets. Defaults to 1.
                The value represents how much the widgets should move upwards, with 1 
                representing one box size.
                
            destroy (bool, optional): Indicates whether to destroy the original widgets when 
                this method is called again. Defaults to True. If True, the original widget will 
                be destroyed; otherwise, only the canvas item will be deleted.

        Note:
            This method should ideally be used only once per object to avoid adding new 
            widgets and deleting old ones repeatedly.
        """
        #destroying all widget if its called again
        for _ in range(len(self._Windows_ids)):
            window = self._Windows_ids.pop()
            self.child_window.delete(window)
            if destroy: 
                window = self.Windows_list.pop()
                window.destroy()
            
        self.Windows_list = list(args)
        self._middel_windows = middle
        
        # getting the box size in negative or the inisal cords:0
        num = (self.box_size - (self.box_size * 2)) * middle
        
        for button in args:
            
            id = self.child_window.create_window(
                self.game_width//2, # x value
                self.game_height//2+num, # y value
                window=button
            )
            self._Windows_ids.append(id)
            num += self.box_size
        
    def add_header(self, header:tuple[int,int,int], pady:int = 10, padx:int = 10, destroy:bool = True) -> None:
        """
        Add header widgets to the header section of the game screen.

        This method positions up to three widgets in the header section: right side, center, and left side. 
        The `header` tuple should contain the widget IDs for these positions. If no widget is desired in 
        a particular position, `None` can be used.

        Args:
            header (tuple[int, int, int]): A tuple containing the widget IDs for the right side, center, and 
                left side of the header, respectively. Example: (right_side_id, center_id, left_side_id). 
                Use `None` for positions where no widget is needed.
            pady (int, optional): Padding on the y-axis. Defaults to 10.
            padx (int, optional): Padding on the x-axis. Defaults to 10.
            destroy (bool, optional): Indicates whether to destroy the original widgets when this method 
                is called again. Defaults to True. If True, the original widgets will be destroyed.

        Note:
            This method should ideally be used only once per object to avoid repeatedly adding new 
            headers and deleting old ones.
        """
        # Deleting existing header widgets if the method is called again
        for num in range(0,len(self._header_ids)):
            if not self._header_ids[num]:
                continue
            
            self.child_window.delete(self._header_ids[num])
            if destroy: 
                self.Header[num].destroy()
                
        # Reset header ids and store new header tuple
        self.Header = header
        self._header_ids = [None, None, None]    
        self.header_info = (padx,pady)
        
        # Adding widget
        if header[0]:# right-side header widget
            x = 0 + padx
            y = 0 + pady
            self._header_ids[0] = self.child_window.create_window(
                x, y, window=header[0], anchor="nw"
            )
            
        if header[1]: #center header widget
            x = (self.game_width // 2 )
            y = (header[1].winfo_reqheight() // 2) + pady
            self._header_ids[1] = self.child_window.create_window(
                x, y, window=header[1], anchor="center"
            )
        
        if header[2]: #left-side header widget
            x = self.game_width - padx
            y = 0 + pady
            self._header_ids[2] = self.child_window.create_window(
                x, y, window=header[2], anchor="ne"
            )
        
    def add_footer(self, footer:tuple, pady:int = 10, padx:int = 10, destroy:bool = True) -> None:
        """
        Add footer widgets to the footer section of the game screen.

        This method positions up to three widgets in the footer section: right side, center, and left side. 
        The `footer` tuple should contain the widget IDs for these positions. If no widget is desired in 
        a particular position, `None` can be used.

        Args:
            footer (tuple): A tuple containing the widget IDs for the right side, center, and 
                left side of the footer, respectively. Example: (right_side_id, center_id, left_side_id). 
                Use `None` for positions where no widget is needed.
            pady (int, optional): Padding on the y-axis. Defaults to 10.
            padx (int, optional): Padding on the x-axis. Defaults to 10.
            destroy (bool, optional): Indicates whether to destroy the original widgets when this method 
                is called again. Defaults to True. If True, the original widgets will be destroyed.

        Note:
            This method should ideally be used only once per object to avoid repeatedly adding new 
            footers and deleting old ones.
        """
        # Deleting existing footer widgets if the method is called again
        for num in range(0, len(self._footer_ids)):
            if not self._footer_ids[num]:
                continue
            
            self.child_window.delete(self._footer_ids[num])
            if destroy: 
                self.footer[num].destroy()
                
        # Reset footer ids and store new footer tuple
        self.footer = footer
        self._footer_ids = [None, None, None]    
        self.footer_info = (padx,pady)
        
        if footer[0]:
            x = 0 + padx
            y = self.game_height - pady
            self._footer_ids[0] = self.child_window.create_window(
                x, y, window=footer[0], anchor="sw"
            )
        
        if footer[1]:
            x = (self.game_width // 2 )
            y = self.game_height - (footer[1].winfo_reqheight() // 2) - pady
            self._footer_ids[1] = self.child_window.create_window(
                x, y, window=footer[1], anchor="center"
            )
        
        if footer[2]:
            x = self.game_width - padx
            y = self.game_height - pady
            self._footer_ids[2] = self.child_window.create_window(
                x, y, window=footer[2], anchor="se"
            )
    
    def update_window_size(self) -> None:
        """
        Update the positions of all windows in the game screen.

        This method adjusts the coordinates of each window stored in self._Windows_ids 
        to be centered horizontally and vertically stacked in the middle of the game screen.
        """
        if self._Windows_ids == []:
            return None
        
        num = (self.box_size - (self.box_size * 2)) * self._middel_windows
        
        for window in self._Windows_ids:
            x = self.game_width // 2
            y = self.game_height // 2 + num
            self.child_window.coords(window, x , y)
            num += self.box_size
            
    def update_header(self) -> None:
        """
        Update the positions of header elements on the game screen.

        This method adjusts the coordinates of each header element based on its stored ID and position info:
        - If self._header_ids[0] exists, it positions it at (0 + self.header_info[0], 0 + self.header_info[1]).
        - If self._header_ids[1] exists, it positions it horizontally centered and adjusted vertically based on its height.
        - If self._header_ids[2] exists, it positions it at (self.game_width - self.header_info[0], 0 + self.header_info[1]).
        """
        if self._header_ids[0]:
            x = 0 + self.header_info[0]
            y = 0 + self.header_info[1]
            self.child_window.coords(self._header_ids[0],x,y)
            
        if self._header_ids[1]:
            x = (self.game_width // 2 )
            y = (self.Header[1].winfo_reqheight() // 2) + self.header_info[1]
            self.child_window.coords(self._header_ids[1],x,y)
            
        if self._header_ids[2]:
            x = self.game_width - self.header_info[0]
            y = 0 + self.header_info[1]
            self.child_window.coords(self._header_ids[2],x,y)
    
    def update_footer(self) -> None:
        """
        Update the positions of footer elements on the game screen.

        This method adjusts the coordinates of each footer element based on its stored ID and position info:
        - If self._footer_ids[0] exists, it positions it at (0 + self.footer_info[0], self.game_height - self.footer_info[1]).
        - If self._footer_ids[1] exists, it positions it horizontally centered and adjusted vertically based on its height.
        - If self._footer_ids[2] exists, it positions it at (self.game_width - self.footer_info[0], self.game_height - self.footer_info[1]).
        """
        if self._footer_ids[0]:
            x = 0 + self.footer_info[0]
            y = self.game_height - self.footer_info[1]
            self.child_window.coords(self._footer_ids[0],x,y)
            
        if self._footer_ids[1]:
            x = (self.game_width // 2 )
            y = self.game_height - (self.footer[1].winfo_reqheight() // 2) - self.footer_info[1]
            self.child_window.coords(self._footer_ids[1],x,y)
            
        if self._header_ids[2]:
            x = self.game_width - self.footer_info[0]
            y = self.game_height - self.footer_info[1]
            self.child_window.coords(self._footer_ids[2],x,y)
            
    def update_nessassaery(self, *args_method, update:bool = False):
        """
        Append methods to self.methods and optionally execute them.

        Args:
            *args_method: Variable length argument list of methods to append to self.methods.
            update (bool): If True, execute all methods in self.methods after appending new methods.
        """
        for method in args_method:
            self.methods.append(method)
        
        if update:
            for method in self.methods: method()
        
    def HomeScreen_HeaderFooter_modle1_inisalization(self, var , padx:int = 10, pady:int = 10) -> None:
        """
        Initialize the header and footer for the home screen with specified labels and a coin widget.

        This method sets up the header with high score and player coin information, and the footer with the version info.
        It also initializes a coin widget in the specified position.

        Args:
            var (object): An object containing necessary attributes for initialization:
                - HIGHT_SCORE (int): The high score value to be displayed.
                - CANVAS_COLOR (str): Background color for the labels.
                - TEXT_COLOR (str): Text color for the labels.
                - FONT_STYLE (str): Font style for the labels.
                - PLAYERP_COINE (int): The player's coin count to be displayed.
                - version (str): The version of the game to be displayed.
                - Form_font (str): Font style for the version label.
            padx (int, optional): Padding on the x-axis for header and footer. Defaults to 10.
            pady (int, optional): Padding on the y-axis for header and footer. Defaults to 10.

        Note:
            This method utilizes the `add_header_or_footer` method to add widgets to the header and footer sections.
        """
        box_size = 20
        
        lable1 = Label(
            master = self.child_window,
            text = f"High score: {var.HIGHT_SCORE}",
            bg = var.CANVAS_COLOR,
            fg = var.TEXT_COLOR,
            font = (var.FONT_STYLE,int(box_size//1.66)),
            relief = "flat"
        )
        
        label2 = Label(
            master = self.child_window,
            text = f": {var.PLAYERP_COINE}",
            bg = var.CANVAS_COLOR,
            fg = var.TEXT_COLOR,
            font = (var.FONT_STYLE,int(box_size//1.66)),
            relief = "flat"
        )
        
        label3 = Label(
            master = self.child_window,
            text = f"Version: {var.version}v",
            bg = var.CANVAS_COLOR,
            fg = var.TEXT_COLOR,
            font = (var.Form_font,7),
            relief = "flat"
        )
        self.add_header(header = (lable1,None,label2), padx= padx, pady= pady)
        self.add_footer(footer = (None, None, label3), padx= padx, pady= pady)
        
        #cords for coin:
        x = self.game_width - label2.winfo_reqwidth() - padx - box_size
        y =  pady
        
        #inisalizing coin
        home_coin = Coin(
            canvas = self.child_window,
            box_size = box_size,
            color = "#ffff00",
            initialize = False
        )
        
        home_coin._create_coin_shape(coordinates = (x , y))
        
        def update(header1,header2,footer1,var, home_coin,gamewidth,box_size,padx,pady):
            header1.config(text = f"High score: {var.HIGHT_SCORE}")
            header2.config(text = f": {var.PLAYERP_COINE}")
            footer1.config(text = f"Version: {var.version}v")
            
            x = gamewidth - header2.winfo_reqwidth() - padx - box_size - 5
            y = 0 + pady 
            
            home_coin.update_color(var.COIN_COLOR)
            home_coin._move_resize_coin_shape((x,y))
            
        
        self.update_nessassaery(lambda : update(lable1,label2,label3,var,home_coin,self.game_width,box_size,padx,pady))
        
    def start_animation(self , speed:int) -> None:
        """
        Start the animation loop for moving snakes and updating the game state.

        This method moves each snake in the game, checks for collisions with
        food, heart, or coin, updates their colors if needed, and generates new 
        items as appropriate. It then schedules the next frame of the animation.

        Args:
            speed (int): The delay in milliseconds between each animation frame.
            
        Note:
            we need to inisalize atlest 1 snake to start the animation if not its return None :)
        """
        if len(self.snakes) == 0:
            return None
        
        for snake in self.snakes:
            
            snake.move_the_snakes()
            snake_cords = snake.snake.snake_coordinates
            x , y = snake.coordinates
            
            if bool(self.food) and (x, y )==  self.food.coords:
                if self.random_food_color:
                    color = choice(self.color_list)
                    self.food.update_color(color)
                self.food.new_food(snake_cords)
            
            if bool(self.heart) and (x , y) == self.heart.coords:
                if self.random_heart_color:
                    color = choice(self.color_list)
                    self.heart.update_color(color)
                self.heart.new_heart(snake_cords)
            
            if bool(self.coin) and (x , y) == self.coin.coords:
                if self.random_coin_color:
                    color = choice(self.color_list)
                    self.coin.update_color(color)
                self.coin.new_coin(snake_cords)
                
        self.animation_after_ids = self.child_window.after(speed,self.start_animation,speed)
        
    def stop_animation(self) -> None:
        """Stop the animation loop."""
        if self.animation_after_ids:
            self.child_window.after_cancel(self.animation_after_ids)
            
    def update_everything(self,var:Variable) -> None:
        """
        Update various attributes, elements, and widgets based on the provided `var` object.

        Args:
            var: An object containing variables to update the game screen attributes and elements.
        """
        if self.food: 
            self.food.update_color(var.FOOD_COLOR)
            self.food.update_size(var.home_boxsize)  
            
        if self.heart:
            self.heart.update_color(var.HEART_COLOR)
            self.heart.update_size(var.home_boxsize)
            
        if self.coin:
            self.coin.update_color(var.COIN_COLOR)
            self.coin.update_size(var.home_boxsize)
        
        #updating snake
        for snake in self.snakes:
            snake.update_size(var.home_boxsize)
        
        #updating canvas and mislanerious
        self.background_color = var.CANVAS_COLOR
        self.game_height = var.game_height
        self.game_width = var.game_width
        self.box_size = var.home_boxsize
        self.speed = var.home_speed
        
        self.child_window.config(
            bg = var.CANVAS_COLOR,
            width = var.game_width,
            height = var.game_height
        )
        
        #updating all window elements:0
        for windows in self.Windows_list:
            windows.config(bg=var.CANVAS_COLOR,fg=var.TEXT_COLOR)
        self.update_window_size()
        
        for window in self.Header:
            if window: window.config(bg=var.CANVAS_COLOR,fg=var.TEXT_COLOR)
        self.update_header()
        
        for window in self.footer:
            if window: window.config(bg=var.CANVAS_COLOR,fg=var.TEXT_COLOR)
        self.update_footer()
        
        self.update_nessassaery(update=True)
            
    def add_to_master(self) -> None:
        '''add to the master'''
        self.child_window.pack()
        
    def remove_from_master(self) -> None:
        '''remove window from master'''
        self.stop_animation()
        self.child_window.pack_forget()


class account_screen:
    #fix update_and_size_and_color method for better 
    #fixing with good calculation...
    
    def __init__(self,var:Variable, master:Frame, root:Tk, change_window:callable ) -> Canvas:
        self.master = master
        self.height = 0
        self.width = 0
        self.var = var
        self.window = WindowGenerator(root, var)
        self.change_method = change_window
        
        self._create_window1()
        self._create_window2()
    
    def __change_window_method(self) -> None:
        """
        this function helps to confirm user password and also if password
        ryt then take them to account setting canvas:0
        """
        get_pass = self.window.taking_password_for_verification_window()
        if get_pass == self.var._player_acc_info["password"]:
            messagebox.showinfo("password matched","password matched now u can modify you account")
            self.change_method(self.canvas2)
        else:
            messagebox.showinfo("wrong password","wrong password u cant modify your account")
    
    def __change_password(self) -> None:
        
        value1, value2 = self.window.change_password_window()
        
        if value1 is None:
            return None
        
        if not (value1 == value2):
            messagebox.showwarning("Password Mismatch", "The new password and confirmation do not match.")
            return None
        
        return_code = self.var.update_password(value1)
        
        if return_code:
            messagebox.showinfo("Password Changed Successfully", "Your password has been updated successfully.")
        else:
            messagebox.showerror("Password Change Failed", "There was an error updating your password. Please try again.")
    
    def __new_account(self) -> None:
        """
        Handles the creation of a new player account.

        This method gathers user input for account creation, verifies the input, 
        and creates a new account if all checks are passed. It displays appropriate 
        messages to the user based on the success or failure of the account creation process.
        """
        account_name, name, pass1, pass2 = self.window.create_new_account_window()
        account_list = self.var.get_account_list()
        
        if not (account_name and name and pass1 and pass2):
            return None
        
        if account_name in account_list[1]:
            messagebox.showerror("Account Name Error", "Account name already exists. Please create another account.")
            return None
        
        if not (pass1 == pass2):
            messagebox.showerror("Password Mismatch", "Passwords do not match. Please re-enter the passwords correctly.")
            return None
        
        data = self.var._defult_player_data(name,pass1)
        return_code = self.var.create_new_account(account_name, data)
        
        if return_code:
            messagebox.showinfo("Success", "Account created successfully!")
        else:
            messagebox.showerror("Failure", "Failed to create the account. Please try again.")
    
    def __change_account(self) -> None:
        name, password = self.window.change_account_window()
        
        if not( name and password):
            return None
        
        value_keys = ["password"]

        original_password = self.var._check_path_and_get_info(name, value_keys)
        
        if original_password == password:
            print(original_password , password)
            if not self.var.change_account(name):
                messagebox.showinfo("Login Failed", "some error happend try again or contact dev")
                return None
            
            messagebox.showinfo("Login Succeeded", "Login successful! If you encounter any issues, please try again or contact the developer.")
            
        elif original_password is None:
            messagebox.showinfo("Login Failed", "some error contact devlopers")
            
        else:
            messagebox.showinfo("Login Failed", "Wrong password")
        
        self.update_window1_info()
        self.update_window2_info()

    def __go_back(self) -> None:
        self.change_method(self.canvas)
    
    def _create_window1(self) -> None:
        """
        Create and configure window 1 with labels, entry fields, buttons, scales, and option menus.

        Initializes:
            - Canvas and labels for game settings (width, height, speed, size, text size, volume level).
            - Entry fields for width and height.
            - Scales for text size and volume level.
            - Option menus for speed and size.
            - Button for account settings.
            - Places elements on the canvas.
        """
        option1 = ("Slow", "Normal", "Fast", "Extreme")
        option2 = ("Small", "Medium", "Large", "Extra Large")
        
        self.canvas = Canvas(master = self.master)
        
        Label1 = Label(self.canvas ,text="Game Width  :", justify="center")
        Label2 = Label(self.canvas ,text="Game Height :", justify="center")
        Label3 = Label(self.canvas ,text="Speed (Home):", justify="left")
        Label4 = Label(self.canvas ,text="Size (Home) :", justify="left")
        Label5 = Label(self.canvas ,text="text size   :", justify="left")
        Label6 = Label(self.canvas ,text="Volume level:", justify="left")
        
        self._AS_button = Button(
            self.canvas, text="Account Setting",relief = "groove", 
            command = self.__change_window_method
        )
        self._AS_width_entry = Entry(self.canvas)  
        self._AS_height_entry = Entry(self.canvas)
        
        self._AS_speed_var = StringVar(self.canvas)
        self._AS_size_var = StringVar(self.canvas)
        
        self._AS_text_var = Scale(
            self.canvas, from_ = 5, to = 20, orient="horizontal",
            relief="groove", sliderlength = 10, sliderrelief = "flat"
        )
        self._AS_volume_var = Scale(
            self.canvas, from_ = 0, to = 100, orient="horizontal",
            relief="groove", sliderlength = 10, sliderrelief = "flat"
        )
        self._AS_speed_OP = OptionMenu(self.canvas, self._AS_speed_var, *option1)
        self._AS_size_OP = OptionMenu(self.canvas , self._AS_size_var,  *option2)
        
        self._AS_lable = (Label1,Label2,Label3,Label4,Label5,Label6)
        
        def add(item):
            return self.canvas.create_window(0,0,window=item)
        
        self.canvas_ids = (
            (add(Label1), add(Label2)),
            (add(self._AS_width_entry) , add(self._AS_height_entry)),
            (add(Label3) , add(self._AS_speed_OP)),
            (add(Label4) , add(self._AS_size_OP)),
            (add(Label5 ), add(self._AS_text_var)),
            (add(Label6) , add(self._AS_volume_var)),
            (add(self._AS_button) , None)
            
        )

    def _create_window2(self) -> None:
        """
        Create and configure window 2 with labels, entry fields, and buttons.
        
        Initializes:
            - Canvas and labels for Name, High Score, and Money.
            - Entry field for the name.
            - Labels for high score and coin count.
            - Buttons for changing password, creating new account, changing account, and going back.
            - Places elements on the canvas.
        """
        self.canvas2 = Canvas(master = self.master)
        
        Label1 = Label(self.canvas2, text = "Name")
        Label2 = Label(self.canvas2, text = "Heigh Score")
        Label3 = Label(self.canvas2, text = "Money")
        self._A_lable = (Label1, Label2, Label3)
        
        self._A_Name_var = Label(self.canvas2)
        self._A_heighscore_lable = Label(self.canvas2)
        self._A_coin_lable = Label(self.canvas2)
        
        self._A_changepassword_button = Button(
            self.canvas2, text="change password",relief = "groove",
            command = self.__change_password
        )
        self._A_newaccount_button = Button(
            self.canvas2, text="new account",relief="groove",
            command = self.__new_account
        )
        self._A_changeaccount_button = Button(
            self.canvas2, text="change account",relief="groove",
            command = self.__change_account
        )
        self._A_go_back_button = Button(
            self.canvas2, text= "<- go back", relief="groove",
            command = self.__go_back
        )
        
        def add(item):
            return self.canvas2.create_window(0,0,window=item)
        
        self.canvas2_ids = (
            (add(Label1) , add(self._A_Name_var)),
            (add(Label2) , add(self._A_heighscore_lable)),
            (add(Label3) , add(self._A_coin_lable)),
            (add(self._A_changepassword_button) , None),
            (add(self._A_newaccount_button) , add(self._A_changeaccount_button)),
            (add(self._A_go_back_button), None)
        )
    
    def update_size_color(self, width:int , height:int) -> None:
        #updating artibutes
        self.width = width
        self.height = height
        font = (self.var.INISIAL_HOME_TEXT,self.var.home_text_size,'bold')
        
        #updating window 1 items
        self.canvas.config(
            width = self.width,
            height = self.height,
            bg = self.var.theme1
        )
        for label in self._AS_lable:
            label.config(font = font )

        self._AS_button.config(width=30, font = font)
        self._AS_width_entry.config(width=15,font=font)
        self._AS_height_entry.config(width=15,font=font)
        self._AS_text_var.config(length=107, font = font)
        self._AS_volume_var.config(length=107, font = font)
        self._AS_speed_OP.config()
        self._AS_size_OP.config()
            
        #updating canvas2 items    
        self.canvas2.config(
            width = self.width,
            height = self.height,
            bg = self.var.theme1
        )
        for label in self._A_lable:
            label.config(font = font )
        
        self._A_Name_var.config(width=15, font = font)
        self._A_heighscore_lable.config(font = font)
        self._A_coin_lable.config(width=15, font = font)
        self._A_changepassword_button.config( width = 30, font = font)
        self._A_newaccount_button.config()
        self._A_changeaccount_button.config()
        self._A_go_back_button.config()
        
        #updating postion
        self.window.upating_form_on_canvas(self.height, self.width, self.canvas, *self.canvas_ids)
        self.window.upating_form_on_canvas(self.height, self.width, self.canvas2, *self.canvas2_ids)
    
    def update_window1_info(self) -> None:
        """
        Update window with current game settings.

        Updates the following:
            - Inserts game width and height.
            - Sets box size and speed options.
            - Sets text size and volume level.
            - Configures font for labels, buttons, and input fields.
        Note: update everything persent in update_window1
        """
        self._AS_width_entry.delete(0,END)
        self._AS_height_entry.delete(0, END)
        self._AS_width_entry.insert(0, self.var.game_width)
        self._AS_height_entry.insert(0, self.var.game_height)
        size = self.var.home_boxsize
        speed = self.var.home_speed
        self._AS_size_var.set('Small'if size == 15 else "Medium" if size == 30 else 'Large' if size == 45 else 'Extra Large')
        self._AS_speed_var.set('Extreme' if speed <= 100 else 'Fast' if speed <= 150 else 'Normal' if speed <= 200 else 'Slow')
        self._AS_text_var.set(self.var.home_text_size)
        self._AS_volume_var.set(self.var.volume_level)

    def update_window2_info(self) -> None:
        """
        Update window with current user information.

        Updates the following:
            - Inserts the active user's name.
            - Sets high score and coin labels.
            - Configures font for labels and buttons.
            
        Note: update everything persent in window2
        """
        self._A_Name_var.config(text = self.var.active_user_name)
        self._A_heighscore_lable.config(text = self.var.HIGHT_SCORE)
        self._A_coin_lable.config(text = self.var.PLAYERP_COINE)

    def update(self, width:int, height:int) -> None:
        """
        update the account setting windows and account window
        """
        self.update_size_color(width, height)
        self.update_window1_info()
        self.update_window2_info()

    def get_value(self) -> dict:
        """
        This method fetches the current values from various user input fields and 
        returns a dictionary containing these values
        """
        game_width = self._AS_width_entry.get()
        if game_width.isdigit():
            game_width = int(game_width)
        else:
            messagebox.showwarning("wrong input", "game width should in int not string")
            return None
        
        game_height = self._AS_height_entry.get()
        if game_height.isdigit():
            game_height = int(game_height)
        else:
            messagebox.showwarning("wrong input", "game height should in int not string")
            return None

        if not ( 500 <= game_width):
            messagebox.showwarning("size influeanse", "game width should not less then 500")
            return None

        if not ( 250 <= game_height):
            messagebox.showwarning("size influeanse", "game height should not less then 250")
            return None
        
        game_height = game_width // 2
        
        size = self._AS_size_var.get()
        speed = self._AS_speed_var.get()
        
        new_info = {
            "game_width" : game_width,
            "game_height" : game_height,
            "home_boxsize" : 15 if size == "Small" else 30 if size == 'Medium' else 45 if size == 'Large' else 60,
            "home_speed" : 100 if speed == 'Extreme' else 150 if speed == "Fast" else 200 if speed == 'Normal' else 300,
            "home_text_size" : self._AS_text_var.get(),
            "volume_level" : self._AS_volume_var.get()
        }
        return new_info


class shop_screen:
    """
    A class to create and manage a shopping interface window with multiple selectable and upgradable items.

    Attributes:
    master (Frame|Tk): The parent widget for the main canvas.
    var (Variable): An instance of the Variable class to hold theme and other settings.
    main_canvas (Canvas): The main canvas widget where all elements are drawn.
    shop_shape_id (list): List of canvas IDs for shop item shapes.
    shop_button_id (list): List of canvas IDs for shop item buttons.
    shape_text_id (list): List of canvas IDs for shop item text.
    button_text_id (list): List of canvas IDs for button text.
    footer_shape_id (list): List of canvas IDs for footer shapes.
    footer_text_id (list): List of canvas IDs for footer text.
    upgradable_id (list): List of canvas IDs for upgradable items.
    upgradable_text (int): Canvas ID for upgradable item text.
    current_data (dict): Current data dictionary for shop items and upgradables.
    current_Sindex (int): Index of the currently selected item.
    current_update_method (callable): Method to update the canvas when an item is selected or upgraded.
    current_save_method (callable): Method to save the current state of the window.
    
    """
    def __init__(self,master:Frame|Tk, var:Variable) -> None:
        """
        Initializes the WindowCreator with the parent widget and variable instance.

        Parameters:
        master (Frame|Tk): The parent widget for the main canvas.
        var (Variable): An instance of the Variable class to hold theme and other settings.
        width (int) : inisial width of the canvas
        height (int) : inisial height of the canvas
        """
        self.main_canvas = None
        self.shop_shape_id = []
        self.shop_button_id = []
        self.shape_text_id = []
        self.button_text_id = []
        self.upgradable_id = []
        self.upgradable_text = None
        
        self.footer_shape_id = []
        self.footer_text_id = []
        
        self.master = master
        self.var = var
        
        self.save = False
        self._current_value = 0
        self._orignal_index = None
        self.current_data = None
        self.current_Sindex = None
        self.current_update_method = None
        self.current_save_method = None
        
        self.set_up()
        self._bind_key()
    
    def __is_visible(self, id) -> bool:
        state = self.main_canvas.itemcget(id, 'state')
        return state != 'hidden'
    
    def _bind_key(self) -> None:
        """bind the canvas with button-1 click with a method _calling_func_method"""
        self.main_canvas.bind("<Button-1>",self._calling_func_method)
    
    def _unbind_keys(self) -> None:
        """unbind the canvas with button-1 click"""
        self.main_canvas.unbind_all("<Button-1>")
    
    def _one_time_styling(self) -> None:
        #hand 2 inisalizing
        def on_enter(event):
            self.main_canvas.config(cursor="hand2")
        
        def on_leave(event):
            self.main_canvas.config(cursor="")
            
        for id in self.shop_button_id:
            self.main_canvas.tag_bind(id, "<Enter>", on_enter)
            self.main_canvas.tag_bind(id, "<Leave>", on_leave)
        
        for id in self.footer_shape_id:
            self.main_canvas.tag_bind(id, "<Enter>", on_enter)
            self.main_canvas.tag_bind(id, "<Leave>", on_leave)
        
        id = self.upgradable_id[1]
        self.main_canvas.tag_bind(id, "<Enter>", on_enter)
        self.main_canvas.tag_bind(id, "<Leave>", on_leave)
        
    def _button_styling(self) -> None:
        #styling artibutes
        color = self.var.theme3
        darken = darken_hex_color(color, 0.2)
        Button_styling = {'fill': color, "activefill": darken, "activeoutline": darken,'outline': 'black',"activewidth":3}
        text_styling = {'fill': self.var.theme2, 'font': (self.var.FONT_STYLE, self.var.home_text_size, 'bold')}
        
        # for all buttons
        button_id = self.shop_button_id + self.footer_shape_id + [self.upgradable_id[1]]
        for id in button_id:
            self.main_canvas.itemconfig(id, **Button_styling)
        
        #this is for all text 
        text_id = self.footer_text_id + self.button_text_id + self.shape_text_id + [self.upgradable_text]
        for id in text_id: 
            self.main_canvas.itemconfig(id, **text_styling)
        
        #canvas updation
        self.main_canvas.config(
            bg = self.var.theme1
        )
    
    def _add_styling(self) -> None:
        #this is for shape id
        for id in self.shop_shape_id:
            color = self.main_canvas.itemcget(id, "fill")
            self.main_canvas.itemconfig(
                id, activeoutline=color,
                activewidth= 4,
            )
        #adding color to the upgradable button 
        self.main_canvas.itemconfig(self.upgradable_id[1],fill = self.var.theme3)
        
    def _add_upgrade(self) -> None:
        
        if self.current_data["upgradable"] >= 5:
            return 
        
        self.current_data["upgradable"] += 1
        
        self.main_canvas.itemconfig(
            self.upgradable_id[2 + self.current_data["upgradable"]-1],
            fill = "yellow",
        )
        
        power = self.current_data["upgradable"]
        charge = self.current_data["charge"]
        
        self.main_canvas.itemconfig(
            self.upgradable_text,
            text = (power * charge) if power < 5 else 'MAX',
            state = "normal"
        )
            
    def _add_info_shopitems(self , data:tuple[dict]) -> None:
        """
        add info in canvas and gui according to the data
        for 6 shapes (shapes, shape_text, button shape and text)

        Args:
            data (tuple[dict]): data for the updation should be a tuple
            containing 6 dict from 0 index to 5 index
        """
        for num in range(len(data)):
            dict_data = data[num]
            
            self.main_canvas.itemconfig(
                self.shop_shape_id[num],
                fill = dict_data["color"],
                state = "normal"
            )
            self.main_canvas.itemconfig(
                self.shop_button_id[num],
                state = "normal"
            )
            self.main_canvas.itemconfig(
                self.shape_text_id[num],
                text = "" if dict_data["purchased"]
                else dict_data["price"],
                state = "disabled"
            )
            self.main_canvas.itemconfig(
                self.button_text_id[num],
                text = "Buy" if not dict_data["purchased"]
                else "Selected" if dict_data["selected"] 
                else "Select",
                state = "disabled"
            )
        self._add_styling()
        
    def _add_info_upgradable(self) -> None:
        """
        Updates the canvas items for upgradable elements.

        Sets the fill color to yellow and makes upgradable items visible based on 
        current_data. Updates upgradable_text with the product of 'upgradable' and 
        'charge' values.

        Attributes:
            current_data (dict): Contains 'upgradable' and 'charge' keys.
        """
        #making upgradalble visible if self.current_data["upgradable"] else return
        if self.current_data["upgradable"]:
            for id in self.upgradable_id:
                self.main_canvas.itemconfig(id,state = "normal") 
            self.main_canvas.itemconfig(self.upgradable_text,state = "disabled") 
        else:
            return
        
        # coloring old upgradable... to yellow
        for num in range(self.current_data["upgradable"]):
            self.main_canvas.itemconfig(
            self.upgradable_id[2 + num],
            fill = "yellow"
            )
            
        #adding money text..
        power = self.current_data["upgradable"]
        charge = self.current_data["charge"]
        
        self.main_canvas.itemconfig(
            self.upgradable_text,
            text = (power * charge) if power < 5 else 'MAX'
        )
        self._add_styling()
        
    def _calling_func_method(self,event) -> None:
        """
        Internal method to update the canvas based on the current data.
        """
        def check_coords_in_range(list_coords,coords):
            x , y = coords
            x1 , y1 , x2 , y2 = list_coords
            
            if x1 < x < x2 and y1 < y < y2:
                return True
            return False
        
        coords = (event.x , event.y)
        
        if check_coords_in_range(self._button_coords[0],coords):
            if self.__is_visible(self.shop_button_id[0]): 
                self._button_method(0)
            
        elif check_coords_in_range(self._button_coords[1],coords):
            if self.__is_visible(self.shop_button_id[1]):
                self._button_method(1)
            
        elif check_coords_in_range(self._button_coords[2],coords):
            if self.__is_visible(self.shop_button_id[2]): 
                self._button_method(2)
            
        elif check_coords_in_range(self._button_coords[3],coords):
            if self.__is_visible(self.shop_button_id[3]): 
                self._button_method(3)
            
        elif check_coords_in_range(self._button_coords[4],coords):
            if self.__is_visible(self.shop_button_id[4]): 
                self._button_method(4)
            
        elif check_coords_in_range(self._button_coords[5],coords):
            if self.__is_visible(self.shop_button_id[5]): 
                self._button_method(5)
            
        elif check_coords_in_range(self._button_coords[6],coords):
            if self.__is_visible(self.upgradable_id[1]): 
                self._button2_method(1)
            
        elif check_coords_in_range(self._button_coords[7],coords):
            if self.__is_visible(self.footer_shape_id[0]): 
                self._button2_method(2)
            
        elif check_coords_in_range(self._button_coords[8],coords):
            if self.__is_visible(self.footer_shape_id[1]):
                self._button2_method(3)
            
        elif check_coords_in_range(self._button_coords[9],coords):
            if self.__is_visible(self.footer_shape_id[2]):
                self._button2_method(4)
    
    def _button_method(self,index_num) -> None:
        """
        handeling button event acording to button index
        """
        index = self.current_Sindex + index_num #for working with data
        data = self.current_data["items"]
        selected = self.current_data["selected_index"]
        
        #checking if purchasing or not if not purchase
        if not data[index]["purchased"]:
            # handelling buying
            if self._current_value >= data[index]["price"]:
                self._current_value -= data[index]["price"]
            else:
                messagebox.showwarning("buying info","purchase cant be made becouse of less money")
                return
            
            #updating dict data by actually index
            data[index]["purchased"] = True
            
            #upating canvas element by index_num..
            self.main_canvas.itemconfig(
                self.button_text_id[index_num],
                text = "select"
            )
            self.main_canvas.itemconfig(
                self.shape_text_id[index_num],
                text = ""
            )
        
        #checking if its already selected then pass
        elif data[index]["purchased"] and data[index]["selected"]:
            return 
        
        #checking if not selected then selecting
        elif data[index]["purchased"] and not data[index]["selected"]:
            
            #making selected dict data to true and old selcted to false
            data[index]["selected"] = True
            data[selected]["selected"] = False
            
            #updating canvas id by index_num
            self.main_canvas.itemconfig(
                self.button_text_id[index_num],
                text = "selected"
            )
            #update if selected come under current data else not
            #becouee it wont be visully appear so just needa change in dict
            if self.current_Sindex <= selected < (self.current_Sindex + 6):
                self.main_canvas.itemconfig(
                    self.button_text_id[(selected % 6)], #selcted % 6 for round up
                    text = "select"
                )
            
            #changing the current selected index
            self.current_data["selected_index"] = index
            self.current_update_method(data[index]["color"])
    
    def _button2_method(self,index_num) -> None:
        """
        handel button event for upgrade button save button
        back and next button
        """
        if index_num == 1:
            power = self.current_data["upgradable"]
            money = power * self.current_data["charge"]
            if not( power < 5 ):
                return
            
            if self._current_value >= money:
                self._add_upgrade()
                self._current_value -= money
            else:
                messagebox.showwarning("buying info","purchase cant be made becouse of less money")
            
        elif index_num == 2:
            if not self.current_Sindex <= 5:
                self.set_to_defult(upgradable = False)
                self.current_Sindex -= 6
                
                data = self.current_data["items"]\
                [self.current_Sindex:self.current_Sindex+6]
                
                self._add_info_shopitems(data)
                
        elif index_num == 3:
            self.var.PLAYERP_COINE = self._current_value
            self.current_save_method()
            self.var.update_user_settings()
            self.save = True
            
        elif index_num == 4:
            if self.current_Sindex + 6 < len(self.current_data["items"]):
                self.set_to_defult(upgradable = False)
                self.current_Sindex += 6
                
                data = self.current_data["items"]\
                [self.current_Sindex:self.current_Sindex+6]
                
                self._add_info_shopitems(data)
        
    def set_up(self) -> None:
        """
        Sets up the main canvas and initializes various graphical elements.

        Parameters:
        width (int): The width of the canvas.
        height (int): The height of the canvas.
        """
        # Create the main canvas if it does not already exist
        
        if not self.main_canvas : self.main_canvas = Canvas(
            master = self.master,
            bg = self.var.theme1
        )
        
        # Create hidden rectangles for shop shapes if they do not already exist
        if not self.shop_shape_id : self.shop_shape_id = [
            self.main_canvas.create_rectangle(
                0 , 0 , 0 , 0 ,
               state = "hidden"
            ) for _ in range(6)
        ]
        # Create hidden rectangles for shop buttons if they do not already exist
        if not self.shop_button_id : self.shop_button_id = [
            self.main_canvas.create_rectangle(
                0 , 0 , 0 , 0 ,
               state = "hidden",
            ) for _ in range(6)
        ]
        # Create hidden text elements for shape texts if they do not already exist
        if not self.shape_text_id : self.shape_text_id = [
            self.main_canvas.create_text(
                0 , 0 , state = "hidden" ,
                anchor = "center", text = "buy",
            ) for _ in range(6)
        ]
        # Create hidden text elements for button texts if they do not already exist
        if not self.button_text_id : self.button_text_id = [
            self.main_canvas.create_text(
                0 , 0 , state = "hidden" ,
                anchor = "center", text = "buy"
            ) for _ in range(6)
        ]
        if not self.upgradable_id : self.upgradable_id = [
            self.main_canvas.create_rectangle(
                0 , 0 , 0 , 0 , 
                state = "hidden",
            ) for _ in range(7)
        ]
        if not self.upgradable_text : 
            self.upgradable_text =  self.main_canvas.create_text(
                0 , 0 , state = "hidden" ,
                anchor = "center", text = "buy"
            )
            
        if not self.footer_shape_id : self.footer_shape_id = [
            self.main_canvas.create_rectangle(
                0 , 0 , 0 , 0 ,
                state = "normal"
            ) for _ in range(3)
        ]
        if not self.footer_text_id : self.footer_text_id = [
            self.main_canvas.create_text(
                0 , 0 , state = "disabled" ,
                anchor = "center", text = text
            ) for text in ('back', 'save', 'next')
        ]
        self._one_time_styling()
        self._button_styling()
        
    def resize_window(self, width:int , height:int) -> None:
        """
        Resizes the window and arranges shapes and buttons in a grid layout on the canvas.
        and gather new coords for _button_coords in this squeanse
        
        The way its contains coordinates are :
        _button_coords = index-[0,1,2,3,4,5,6,7,8,9]
        From 0 to 5 its shop canvas button coordinates.
        From 6 to 9 its conatins coordinates in this squence:
        upgradable_id[1](button), footer_shape_id[0-2](back,save,next)

        Parameters:
        width (int): The width of the window.
        height (int): The height of the window.
        """
        self._button_coords = []
        self.main_canvas.config(
            width=width,
            height=height
        )
        
        self.shape_width = (width / 1.4) // 3
        self.padx = (width / 3.25) // 4
        
        devision = height / 4
        self.mini_pady = (devision / 2) / 4
        self.pady = (devision / 2) / 3
        self.button_height = devision / 3
        self.shape_height = self.button_height * 2
        
        def configure_canvas_item(number, x, y):
            self.main_canvas.coords(
                self.shop_shape_id[number],
                x, y, 
                x + self.shape_width,
                y + self.shape_height
            )
            self.main_canvas.coords(
                self.shape_text_id[number],
                (x + x + self.shape_width) / 2,
                (y + y + self.shape_height) / 2
            )
            button_y = y + self.shape_height + self.mini_pady
            self.main_canvas.coords(
                self.shop_button_id[number],
                x, button_y,
                x + self.shape_width,
                button_y + self.button_height
            )
            self.main_canvas.coords(
                self.button_text_id[number],
                (x + x + self.shape_width) / 2,
                (button_y + button_y + self.button_height) / 2
            )
            #gathering coords of shop item buttons
            coords = tuple(map(int, [x, button_y, x + self.shape_width, button_y + self.button_height]))
            self._button_coords.append(coords)
            
        x, y = self.padx, self.pady
        number = 0
        for row in range(2):
            for col in range(3):
                configure_canvas_item(number, x, y)
                number += 1
                x += self.shape_width + self.padx
            x = self.padx
            y += self.shape_height + self.button_height + self.mini_pady + self.pady

        #calculation for creating upgradable :0
        x = self.padx
        remain_height = height / 3
        upgradable_width = (self.shape_width * 2 ) + self.padx
        upgradable_height = (remain_height - self.pady*2 ) // 2
        
        #setting up on canvas :0
        #main shape and button eastablization:0
        self.main_canvas.coords(
            self.upgradable_id[0],
            x , y ,
            x + upgradable_width, y + upgradable_height
        )
        
        x += upgradable_width + self.padx
        self.main_canvas.coords(
            self.upgradable_id[1],
            x , y ,
            x + self.shape_width, y + upgradable_height
        )
        self.main_canvas.coords(
            self.upgradable_text,
            (x + x + self.shape_width) // 2 ,
            (y + y + upgradable_height) // 2
        )
        #gathering coords of .. upgradable button
        coords = tuple(map(int,[x , y , x + self.shape_width, y + upgradable_height]))
        self._button_coords.append(coords)
        
        dividiablex = upgradable_width / 3
        dividiabley = upgradable_height / 3
        new_width = (dividiablex * 2 ) / 5
        new_height = dividiabley * 2
        new_padx = dividiablex / 6
        new_pady = dividiabley / 2
        new_x = self.padx + new_padx
        new_y = y + new_pady
        # setting up the widget items ":0"
        for id in self.upgradable_id[2:]:
            self.main_canvas.coords( id ,
                new_x , new_y,
                new_x + new_width, new_y + new_height
            )
            new_x += new_width + new_padx
        
        # setting up footer things ---------
        x = self.padx
        y += self.pady + upgradable_height
        for number in range(3):
            self.main_canvas.coords(
                self.footer_shape_id[number],
                x , y ,
                x + self.shape_width, y + upgradable_height
            )
            self.main_canvas.coords(
                self.footer_text_id[number],
                (x + x + self.shape_width) / 2,
                (y + y + upgradable_height) / 2
            )
            #collecting coords of.. back , next and save button
            coords = tuple(map(int,[x,y, x + self.shape_width, y + upgradable_height]))
            self._button_coords.append(coords)
            x += self.shape_width + self.padx
            
    def change_window(self, data:dict, update_method:callable, save_method:callable) -> None:
        """
        Changes the window's content based on the provided data, save method, and update method.

        Parameters:
        data (dict): The data to be displayed in the window.
        save_method (callable): Method to save the current state of the window.
        update_method (callable): Method to update the canvas when an item is selected or upgraded.
        """
        #if changing to new shop window changing current to orignal state
        if (not self.save) and self.current_update_method and self.current_data:
            self.current_update_method(self.current_data["items"][self._orignal_index]["color"])
        
        # adding new data :0
        self.current_data = deep_copy(data)
        self.current_save_method = save_method
        self.current_update_method = update_method
        self._current_value = self.var.PLAYERP_COINE
        self._orignal_index = data["selected_index"]
        self.current_Sindex = 0
        self.save = False
        
        self.set_to_defult()
        
        #adding data to items :0
        self._add_info_shopitems(self.current_data["items"][0:6])
        self._add_info_upgradable()
        # self.add_styling()
        
    def delete_window(self) -> None:
        """
        Deletes the current window and all its elements.
        """
        for id in self.shop_shape_id:
            self.main_canvas.delete(id)
        
        for id in self.shop_button_id:
            self.main_canvas.delete(id)
        
        for id in self.shape_text_id:
            self.main_canvas.delete(id)
        
        for id in self.button_text_id:
            self.main_canvas.delete(id)
        
        for id in self.upgradable_id:
            self.main_canvas.delete(id)
        
        self.main_canvas.delete(self.upgradable_text)
        
        # self._button_coords = None
    
    def set_to_defult(self, shop_item = True, upgradable = True) -> None:
        """
        Resets the window and all its elements to their default state.
        """
        if shop_item:
            
            for id in self.shop_shape_id:
                self.main_canvas.itemconfig(id, state = "hidden", fill = '')
        
            for id in self.shop_button_id:
                self.main_canvas.itemconfig(id, state = "hidden")
        
            for id in self.shape_text_id:
                self.main_canvas.itemconfig(id, state = "hidden", text = '')
        
            for id in self.button_text_id:
                self.main_canvas.itemconfig(id, state = "hidden",)
        
        if upgradable:
            
            for id in self.upgradable_id:
                self.main_canvas.itemconfig(id, state = "hidden", fill = '')
        
            self.main_canvas.itemconfig(self.upgradable_text,state = "hidden", text = '')
        
    def UPDATE(self, width, height) -> None:
        #resize withon method will resize the window
        #and all its artibute and then gather the coords..
        #acording to the new window size
        self.resize_window(width, height)
        #calling this method will add styling acording to
        #new info come under var for (theme1, theme2, theme3)
        self._button_styling()


class setting_screen_gui:
    """
    A class to represent the GUI for the setting screen in a game.

    Attributes:
        game_screen_frame (Frame): The frame for the game screen.
        setting_screen_frame (Frame): The frame for the setting screen.
        var (Variable): A variable to store various game settings.
        initialize (bool): A flag to initialize the GUI. Default is True.

    Methods:
        __init__(game_frame: Frame, setting_frame: Frame, var: Variable, initialize: bool = True) -> None:
            Initializes the setting screen GUI.
        _calculate_dimension() -> None:
            Calculates the dimensions for the game and setting screens.
        _possision_snack_and_idels() -> None:
            Positions the snake and other elements like food and heart on the game screen.
        _adding_second_screen_element() -> None:
            Initializes the second screen with required objects such as navigation buttons and save button.
        Initialize_First_Screen() -> None:
            Initializes the first screen (game screen).
        Initialize_second_Screen() -> None:
            Initializes the second screen (setting screen).
        change_screen(canvas: Canvas | None = None) -> None:
            Changes the current screen to a new canvas in the application.
        get_idels_coordinates() -> tuple[list]:
            Gets the coordinates of various elements on the game screen.
        update_size_and_color() -> None:
            Updates the size and color of various elements on the screen.
        add_to_master() -> None:
            Adds the frames to the master layout.
        remove_to_master() -> None:
            Removes the frames from the master layout.
    """
    def __init__(self, game_frame:Frame, setting_frame:Frame, var:Variable, initialize:bool = True) -> None:
        """
        Initializes the setting screen GUI.

        Args:
            game_frame (Frame): The frame for the game screen.
            setting_frame (Frame): The frame for the setting screen.
            var (Variable): A variable to store various game settings.
            initialize (bool): A flag to initialize the GUI. Default is True.
        """
        self.game_screen_frame = game_frame
        self.setting_screen_frame = setting_frame
        self.var = var
        
        self.Initialize_First_Screen()
        self.Initialize_second_Screen()
        self.current_screen = self.demo_screen
        
        if initialize:
            self.add_to_master()
    
    def _calculate_dimension(self) -> None:
        '''
        Calculate the screen dimensions for the game and settings screen.
        '''
        self._gameexit_button_height = 30
        self._game_screen_height = self.var.game_height - self._gameexit_button_height - 7
        self._game_screen_width = self.var.game_width // 1.6
        self._settingscreen_height = self.var.game_height - 7
        self._settingscreen_width = self.var.game_width - self._game_screen_width -7
        self.main_screen_height = None
        
    def _possision_snack_and_idels(self) -> None:
        """
        Position the snake and other elements like food and heart on the game screen.
        """
        center_borderx = self._game_screen_width // 2
        center_bordery = self.GAME_SCREEN._game_bord_height // 2
        box_size = self.var.game_box_size
        center_borderx, center_bordery = validate_coordinates((center_borderx,center_bordery), box_size)
        
        self.GAME_SCREEN.SNAKE.delete_all()
        self.GAME_SCREEN.SNAKE.snake_coordinates = [(center_borderx,center_bordery-box_size)]
        self.GAME_SCREEN.SNAKE.snake_body = [self.GAME_SCREEN.SNAKE._create_body(
            center_borderx,center_bordery - box_size)
        ]
        
        # adding snacke body to left
        x = center_borderx
        for _ in range(4):
            x += box_size
            self.GAME_SCREEN.SNAKE.move_snake(x - box_size , center_bordery - box_size,False)
        
        #adding snacke body to right
        x = center_borderx
        for _ in range(4):
            x -= box_size
            self.GAME_SCREEN.SNAKE.move_snake(x+box_size , center_bordery,False)
        
        #adding food:
        snake_cords = self.GAME_SCREEN.SNAKE.snake_coordinates
        self.GAME_SCREEN.FOOD.new_food(coordinates = snake_cords)
        snake_cords += [self.GAME_SCREEN.FOOD.coords]
        self.GAME_SCREEN.COIN.new_coin(coordinates = snake_cords)
        snake_cords += [self.GAME_SCREEN.COIN.coords]
        self.GAME_SCREEN.HEART.new_heart(coordinates = snake_cords)
        self.GAME_SCREEN.HEART_NEW.add_heart_in_range(range_int = 2)
    
    def _adding_second_screen_element(self) -> None:
        """
        Initialize the second screen with all objects required in the screen.

        Includes:
            - nevigation_button1: game button canvas
            - nevigation_button2: account button canvas
            - _text_nev_button_id: (tuple) button1 and button2 text id
            - _text_nev_button2: account_button_text_id
            - save_button: save button canvas
            - save_button_text_id: save button text id
            - demo_screen: demo screen for setting
            - main_screen_height: the main screen height
        """
        #adding account and shop button and writing text on it :0
        self.nevigation_button1 = Canvas(
            master = self.setting_screen_frame
        )
        self.nevigation_button2 = Canvas(
            master = self.setting_screen_frame
        )
        button_text_id1 = self.nevigation_button1.create_text(
            0 , 0 ,text = "shop", anchor = "center"
        )
        button_text_id2 = self.nevigation_button2.create_text(
            0 ,0 ,text = "setting", anchor = "center"
        )
        self._text_nev_button_id = (button_text_id1,button_text_id2)
        
        #adding down save button and its text 
        self.save_button = Canvas(
            master = self.setting_screen_frame
        )
        self.save_button_text_id = self.save_button.create_text(
            0 , 0 , text = "Save", anchor = "center"
        )
        
        self.demo_screen = Canvas(
            master = self.setting_screen_frame
        )
        self.demo_screen_text = self.demo_screen.create_text(
            0 , 0, text = "Please select an item from the left side to begin shopping." 
            +"\n\nImportant Reminders :\n1. After purchasing items, click the 'Save' button"
            + "located under the shop window."
            +"\n2. Once you have finished setting up, click the 'Save' button at the bottom to"
            + "save settings you made for your account.",
            anchor = "nw",justify='left',
        )

    def Initialize_First_Screen(self) -> None:
        """
        Initializes the first screen (game screen).
        """
        self.GAME_SCREEN = Game_screen(
            Master = self.game_screen_frame,
            var = self.var
        )
        self.back_button = Canvas(
            master = self.game_screen_frame
        )
        self.back_button_text_id = self.back_button.create_text(
            0 ,0 ,text = "back"
        )
        self.GAME_SCREEN.add_to_Master()
        self.back_button.pack()

    def Initialize_second_Screen(self) -> None:
        """
        Initializes the second screen (setting screen).
        """
        self._adding_second_screen_element()
        self.nevigation_button1.grid(row = 0, column = 0)
        self.nevigation_button2.grid(row = 0, column = 1)
        self.demo_screen.grid(row = 1, column = 0, columnspan = 2)
        self.save_button.grid(row = 2, column = 0, columnspan = 2)
    
    def change_screen(self,canvas:Canvas|None = None) -> None:
        """
        Change the current screen to a new canvas in the application.

        This method performs the following actions:
        1. Invokes the `__shift_button_button1` method with `None` as the argument.
        2. Removes the currently displayed screen (stored in `self.curent_screen`) from the grid.
        3. Updates `self.curent_screen` to the provided `canvas`.
        4. Displays the new canvas by placing it in the grid at row 1, column 0, spanning two columns.

        Args:
            canvas (Canvas | None): The new canvas to be displayed on the screen.
        """
        canvas = canvas if canvas is not None else self.demo_screen
        self.current_screen.grid_forget()
        self.current_screen = canvas
        self.current_screen.grid(row = 1 , column = 0,columnspan = 2)
    
    def get_idels_coordinates(self) -> tuple[list]:
        """
        Get the coordinates of various elements on the game screen.

        This method retrieves the coordinates of different elements on the game screen, such as menu options, score text, hearts, food, and snake body segments.

        Returns:
            tuple[list]: A tuple containing lists of coordinates for various game elements.
        """
        nevigation_canvas = self.GAME_SCREEN.NEVIGATION_CANVAS
        game_canvas = self.GAME_SCREEN.GAME_CANVAS
        
        coordinates_home_and_score = [
            nevigation_canvas.bbox(self.GAME_SCREEN.MENU_OPTION),
            nevigation_canvas.bbox(self.GAME_SCREEN.SCORE_TEXT)
        ]
        
        hearts_coordinates = [
            nevigation_canvas.bbox(body)
            for heart in self.GAME_SCREEN.HEART_NEW.heart_list
            for body in heart
        ]
        
        coordinates_food = [
            game_canvas.bbox(self.GAME_SCREEN.FOOD.food)
        ]
        
        coordinates_snake = [
            game_canvas.bbox(snake)
            for snake in self.GAME_SCREEN.SNAKE.snake_body
        ]
        
        coordinates_canvas_heart = [
            game_canvas.bbox(heart)
            for heart in self.GAME_SCREEN.HEART.hearts
        ]
        
        coordinates_coin = [
            game_canvas.bbox(coin)
            for coin in self.GAME_SCREEN.COIN.coins
        ]
        
        return (coordinates_home_and_score, hearts_coordinates, coordinates_food,
                coordinates_snake, coordinates_canvas_heart, coordinates_coin)
    
    def update_size_and_color(self) -> None:
        """
        Update the size and color of various elements on the screen.
        """
        self._calculate_dimension()
        font = (self.var.FONT_STYLE, self.var.home_text_size, "bold")
        
        self.GAME_SCREEN.demo_screen_var_update(
            initialize=True,
            game_height = self._game_screen_height,
            game_width = self._game_screen_width
        )
        self.back_button.config(
            height = self._gameexit_button_height,
            width = self._game_screen_width,
            bg = self.var.theme2
        )
        self.back_button.itemconfigure(
            self.back_button_text_id,
            font = font,
            fill = self.var.theme1
        )
        self.back_button.coords(
            self.back_button_text_id,
            self._game_screen_width //2 , self._gameexit_button_height // 2
        )
        
        self._possision_snack_and_idels()
        
        #updating secoend screen
        nev_button_height = self.GAME_SCREEN._nevigation_height
        
        self.nevigation_button1.config(
            height = nev_button_height,
            width = (self._settingscreen_width // 2 ) - 7,
            bg = self.var.theme1
        )
        self.nevigation_button2.config(
            height = nev_button_height,
            width = (self._settingscreen_width // 2 ) - 7,
            bg = self.var.theme2
        )
        self.nevigation_button1.itemconfig(
            self._text_nev_button_id[0],
            font = font,
            fill = self.var.theme2
        )
        self.nevigation_button1.coords(
            self._text_nev_button_id[0],
            self._settingscreen_width // 4,
            nev_button_height // 2,
        )
        self.nevigation_button2.itemconfig(
            self._text_nev_button_id[1],
            font = font,
            fill = self.var.theme1
        )
        self.nevigation_button2.coords(
            self._text_nev_button_id[1],
            self._settingscreen_width // 4,
            nev_button_height // 2,
        )
        
        #adding down save button and its text 
        self.save_button.config(
            height = self._gameexit_button_height,
            width = self._settingscreen_width ,
            bg = self.var.theme2
        )
        self.save_button.itemconfigure(
            self.save_button_text_id,
            font = font,
            fill = self.var.theme1
        )
        self.save_button.coords(
            self.save_button_text_id,
            self._settingscreen_width // 2,
            self._gameexit_button_height // 2,
        )
        # calculating main screen_ height and updating demo screen :0
        self.main_screen_height = self._settingscreen_height - self._gameexit_button_height - nev_button_height
        
        self.demo_screen.config(
            height = self.main_screen_height,
            width = self._settingscreen_width,
            bg = self.var.theme1
        )
        self._settingscreen_width
        divistion_x = self._settingscreen_width // 5
        divistion_y = self.main_screen_height // 7
        startx , starty = divistion_x , divistion_y
        wrapwidth = divistion_x * 3
        
        self.demo_screen.coords(
            self.demo_screen_text,
            startx, starty
        )
        self.demo_screen.itemconfigure(
            self.demo_screen_text,
            font = font,
            fill = self.var.theme2,
            width = wrapwidth
        )
        
    def add_to_master(self) -> None:
        """
        Add the frames to the master layout.
        """
        self.game_screen_frame.grid(row = 0, column = 0)
        self.setting_screen_frame.grid(row = 0, column = 1)
            
    def remove_to_master(self) -> None:
        """
        Remove the frames from the master layout.
        """
        self.game_screen_frame.grid_forget()
        self.setting_screen_frame.grid_forget()
        

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
    def __init__(self, root:Tk , var:Variable) -> None:
        """
        Initialize the WindowGenerator with the main Tkinter root window and a Variable instance.

        Args:
            root (Tk): The main Tkinter root window.
            var (Variable): An instance of Variable class used for getting account information.
        """
        self.root = root
        self.var = var
        self.__value = None
    
    @property
    def font(self):
        """
        Get the font style for text in the windows.

        Returns:
            tuple: A tuple containing the font style, size, and weight.
        """
        return (self.var.FONT_STYLE, self.var.home_text_size, "bold")
    
    def __method(self, func:callable, *args) -> None:
            for item in args:
                if not item.get():
                    item.focus_set()
                    return
            func()
            
    def upating_form_on_canvas(self, height:int, width:int, canvas:Canvas,*args:tuple) -> Canvas:
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
        for left_id , right_id in args:
            
            if not (left_id and right_id):
                canvas.coords(left_id or right_id, middle1 *2 , start)
                start += distance
                continue
            
            #addig_both_window_left and ryt
            canvas.coords(left_id , middle1 , start )
            canvas.coords(right_id , middle2 , start )
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
        self.__value = (None, None)
        
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
            font = self.font,
            bg="#e6f2ff",fg= "black" 
        )
        password1 = Entry(
            master = frame1,
            width = 15,bd = 1,
            relief="solid",
            justify="center",
            show = "*",
            font = self.font
        )
        func = lambda : self.__capture_and_close(password1 , window = window ,root_enable = True)
        
        button = Button(
            master = frame1,
            relief="solid",
            text= "continue",
            bg= "#e6f2ff" ,fg="black",
            font = self.font,
            command = func
        )
        
        lable1.grid(row=0, column=0 , padx= 5, pady= 5)
        password1.grid(row=0 , column=1 , padx=5, pady=5)
        button.grid(row=1,column=0,columnspan=2,sticky='ew', padx=5)
        frame1.pack()
        password1.focus_set()
        window.bind("<Return>",lambda event: self.__method(func,password1))
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
            font = self.font
        )
        label2 = Label(
            master = frame1,
            text = "Verify New Password",
            relief = "flat",
            bg ="#e6f2ff",fg ="black",
            font = self.font
        )
        password1 = Entry(
            master = frame1,
            width = 15,bd = 1,
            relief="solid",
            justify="center",
            show = "*",
            font = self.font
        )
        password2 = Entry(
            master = frame1,
            width = 15,bd = 1,
            relief="solid",
            justify="center",
            show = "*",
            font = self.font
        )
        
        func = lambda : self.__capture_and_close(password1 , password2 , window = window , root_enable = True)
        
        button = Button(
            master = frame1,
            relief="solid",
            text= "continue",
            bg= "#e6f2ff" ,fg="black",
            font = self.font,
            command= func
        )
        label1.grid(row=0,column=0,padx=5,pady=5)
        label2.grid(row=1,column=0,padx=5,pady=5)
        password1.grid(row=0,column=1,padx=5,pady=5)
        password2.grid(row=1,column=1,padx=5,pady=5)
        button.grid(row=2,column=0,columnspan=2,sticky='ew', padx=5, pady=5)
        password1.focus_set()
        frame1.pack()
        window.bind("<Return>",lambda event : self.__method(func,password1, password2))
        window.wait_window(window)
        
        return self.__value
    
    def create_new_account_window(self):
        """
        Create a window for creating a new account.

        Returns:
            list: A list containing the account name, player name, and password entered by the user.

        Notes:
            Passwords entered are masked for security, displaying asterisks instead of the actual characters.
        """
        self.__value = [None,None,None,None]
        window = self.create_top_level_screen(
            title = "create_new_account",
            width = 260,
            height = 160,
            color = "#e6f2ff"
        )
        frame1 = Frame(window ,bg = "#e6f2ff")
        
        label1 = Label(
            master = frame1,
            text = "Account Name",
            relief = "flat",
            bg ="#e6f2ff",fg ="black",
            font = self.font
        )
        label2 = Label(
            master = frame1,
            text = "Player Name",
            relief = "flat",
            bg ="#e6f2ff",fg ="black",
            font = self.font
        )
        label3 = Label(
            master = frame1,
            text = "Account Password",
            relief = "flat",
            bg ="#e6f2ff",fg ="black",
            font = self.font
        )
        label4 = Label(
            master = frame1,
            text = "Retype Password",
            relief = "flat",
            bg ="#e6f2ff",fg ="black",
            font = self.font
        )
        account_name = Entry(
            master = frame1,
            width = 15,bd = 1,
            relief="solid",
            justify="center",
            font = self.font
        )
        player_name = Entry(
            master = frame1,
            width = 15,bd = 1,
            relief="solid",
            justify="center",
            font = self.font
        )
        password1 = Entry(
            master = frame1,
            width = 15,bd = 1,
            relief="solid",
            justify="center",
            show = "*",
            font = self.font
        )
        password2 = Entry(
            master = frame1,
            width = 15,bd = 1,
            relief="solid",
            justify="center",
            show = "*",
            font = self.font
        )
        func = lambda : self.__capture_and_close(account_name, player_name, password1 , password2 , window = window , root_enable = True)
        button = Button(
            master = frame1,
            relief="solid",
            text= "create",
            bg= "#e6f2ff" ,fg="black",
            font = self.font,
            command = func
        )
        
        #adding to the window
        label1.grid(row=0,column=0,padx=5,pady=5)
        label2.grid(row=1,column=0,padx=5,pady=5)
        label3.grid(row=2,column=0,padx=5,pady=5)
        label4.grid(row=3,column=0,padx=5,pady=5)
        account_name.grid(row=0,column=1,padx=5,pady=5)
        player_name.grid(row=1,column=1,padx=5,pady=5)
        password1.grid(row=2,column=1,padx=5,pady=5)
        password2.grid(row=3,column=1,padx=5,pady=5)
        button.grid(row=4,column=0,columnspan=2,sticky='ew', padx=5, pady=5)
        account_name.focus_set()
        window.bind("<Return>",lambda event : self.__method(func,account_name,player_name,password1, password2))
        frame1.pack()
        window.wait_window(window)
        
        return self.__value
        
    def change_account_window(self):
        """
        Create a window for changing the account.

        This method displays a top-level window where the user can select an existing account from a dropdown menu and enter the password for the selected account. It facilitates switching accounts by verifying the entered password.

        Returns:
            list: A list containing two elements:
                - The first element is the name of the selected account.
                - The second element is the password entered for the selected account.

        Notes:
            - The account list is retrieved from the `self.var.get_account_list()` method.
            - The password field is masked to display asterisks instead of the actual characters.
            - The window is modal, meaning that it captures user input until it is closed.
        """
        self.__value = [None,None]
        window = self.create_top_level_screen(
            title = "change account",
            width = 260,
            height = 130,
            color = "#e6f2ff"
        )
        frame1 = Frame(window , bg = "#e6f2ff" , padx= 5 ,pady=5)
        name, account = self.var.get_account_list()
        string_var = StringVar(frame1, value=name)
        
        lable1 = Label(
            master = frame1, 
            relief="flat", 
            text="Select",
            font = self.font,
            bg="#e6f2ff",fg= "black" 
        )
        lable2 = Label(
            master = frame1, 
            relief="flat", 
            text="password :",
            font = self.font,
            bg="#e6f2ff",fg= "black" 
        )
        select = OptionMenu(
            frame1,
            string_var,
            *account
        )
        
        password1 = Entry(
            master = frame1,
            width = 15,bd = 1,
            relief="solid",
            justify="center",
            show = "*",
            font = self.font
        )
        func = lambda : self.__capture_and_close(string_var, password1 , window = window ,root_enable = True)
        button = Button(
            master = frame1,
            relief="solid",
            text= "continue",
            bg= "#e6f2ff" ,fg="black",
            font = self.font,
            command = func
        )
        
        lable1.grid(row=0, column=0 , padx= 5, pady= 5)
        lable2.grid(row=1, column=0 , padx= 5, pady= 5)
        select.grid(row=0 , column=1 , padx=5, pady=5)
        password1.grid(row=1 , column=1 , padx=5, pady=5)
        button.grid(row=2,column=0,columnspan=2,sticky='ew', padx=5)
        frame1.pack()
        password1.focus_set()
        window.bind("<Return>",lambda event : self.__method(func,password1))
        window.wait_window(window)
        
        return self.__value
               
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


