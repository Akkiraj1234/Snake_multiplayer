from tkinter import Canvas, Frame, Button, Label, Entry, Toplevel ,Tk, messagebox
from random import choice

from game_idles import Food, Snake, Heart, Coin, Heart_NEV, goofy_Snakes, validate_coordinates
from variable import Variable, demo_variable


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
   
    def __init__(self,Master:Tk, var:Variable, initialize:bool = True) -> None:
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
        
        if initialize:
            self.SET_UP()
    
    def SET_UP(self) -> None:
        """
        genrate the game canvas by adjusting 
        window_size and nevigation_size create the
        game_canvas with all things set up
        """
        self.adjust_window_size()
        self.nevigation_setup()
        self.game_canvas_setup()
        
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
    
    def nevigation_setup(self) -> None:
        """
        This method sets up the navigation canvas with essential elements such as a heart icon
        representing the player's remaining lives, a score text displaying the current score,
        and a menu option for accessing game options or pausing the game.
        """
        var = self.var if not self.demo else self.var1
        
        braking_into_4 =  self._nevigation_height // 4
        
        self.NEVIGATION_CANVAS = Canvas(
            master = self.MASTER,
            bg = var.NEV_COLOR,
            width = self.game_width,
            height = self._nevigation_height
            )
        
        self.HEART_NEW = Heart_NEV(
            canvas = self.NEVIGATION_CANVAS,
            color = var.HEART_COLOR,
            initial_heart = var.INISISAL_HEART,
            limit = var.HEART_LIMIT
            )
        
        self.SCORE_TEXT = self.NEVIGATION_CANVAS.create_text(
            self.game_width // 2,
            braking_into_4 * 2,
            font = ("Arial",braking_into_4 * 2,"bold"),
            text = f"Score: 0",
            fill = var.TEXT_COLOR
            )
        
        self.MENU_OPTION = self.NEVIGATION_CANVAS.create_text(
            braking_into_4 * 4,
            braking_into_4 * 2,
            font = ("Arial", braking_into_4 * 2, "bold"),
            text = "Menu",
            fill = var.TEXT_COLOR
            )
    
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
            bg = var.CANVAS_COLOR,
            width = self.game_width,
            height = self._game_bord_height
            )
        
        self.SNAKE = Snake(
            canvas = self.GAME_CANVAS,
            lenght = var.SNAKE_LENGHT,
            coordinates = var.SNAKE_CORDINATES,
            color = var.SNAKE_COLOR,
            box_size = var.game_box_size
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
        
    def update_everything(self) -> None:
        """
        this method update all elemets posstion and color acording to new one
        """
        var = self.var if not self.demo else self.var1
        self.adjust_window_size()
        
        #updating nevigation and its itemes================
        braking_into_4 =  self._nevigation_height // 4
        
        if self.NEVIGATION_CANVAS: self.NEVIGATION_CANVAS.config(
            bg = var.NEV_COLOR,
            width = self.game_width,
            height = self._nevigation_height
            )
        
        if self.HEART:
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
                    text_id[0],
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
            
        if self.FOOD: 
            self.FOOD.update_color(var.FOOD_COLOR)
            self.FOOD._calculate_dimension()
            
        if self.HEART: 
            self.HEART.update_color(var.HEART_COLOR)
            self.HEART._calculate_dimension()
            
        if self.COIN: 
            self.COIN.update_color(var.COIN_COLOR)
            self.COIN._calculate_dimension()

    def demo_screen_var_update(self, initialize:bool = False,**kwargs) -> demo_variable:
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
        
        if initialize:
            self.SET_UP()
        else:
            self.adjust_window_size()
            self.update_everything()
            
        return var
        
    def add_to_Master(self) -> None:
        """
        Pack the navigation and game canvases and add it to master
        """
        self.MASTER.pack()    
        self.NEVIGATION_CANVAS.pack()
        self.GAME_CANVAS.pack()

    def remove_to_Master(self)-> None:
        """
        remove the navigation and game canvases. from master
        """
        self.NEVIGATION_CANVAS.pack_forget()
        self.GAME_CANVAS.pack_forget()
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
            
    def update_everything(self,var) -> None:
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


class setting_screen_gui:
    """_summary_

    Returns:
        _type_: _description_
    """
    def __init__(self, master:Tk|Frame, var:Variable) -> None:
        self.master = master
        self.var = var
        
        self.game_screen_frame = Frame(self.master)
        self.setting_screen_frame = Frame(self.master)
        
        self._calculate_dimension()
        self.Initialize_First_Screen()
        self.Initialize_second_Screen()
        self.current_screen = self.demo_screen
    
    def _calculate_dimension(self):
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
        '''
        possison the sneck and idels like food and heart and stuff
        and postion etc........
        '''
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
        inisalize the second_screen with all obj requird in screen
        like nevigation buttons-2, save button-1
        inclue :-
            - nevigation_button1  : game button canvs
            - nevigation_button2  : account button canvs
            - _text_nev_button_id : (tuple)button1 and button2 text id
            - _text_nev_button2   : account_button_text_id
            - save_button         : save button canvas
            - save_button_text_id : save button_text id
            - demo_screen         : demo screen for setting
            - main_screen_height  : the main screen_height

        return :
            None
        """
        nev_button_height = self.GAME_SCREEN._nevigation_height
        #adding account and shop button and writing text on it :0
        self.nevigation_button1 = Canvas(
            master = self.setting_screen_frame,
            height = nev_button_height,
            width = (self._settingscreen_width // 2 ) - 7,
            bg = self.var.theme1
        )
        self.nevigation_button2 = Canvas(
            master = self.setting_screen_frame,
            height = nev_button_height,
            width = (self._settingscreen_width // 2 ) - 7,
            bg = self.var.theme2
        )
        button_text_id1 = self.nevigation_button1.create_text(
            self._settingscreen_width // 4,
            nev_button_height // 2,
            font = ("Arial",self.var.home_text_size,'bold'),
            text = "shop",
            fill = self.var.theme2,
            anchor = "center"
        )
        button_text_id2 = self.nevigation_button2.create_text(
            self._settingscreen_width // 4,
            nev_button_height // 2,
            font = ("Arial",self.var.home_text_size,'bold'),
            text = "setting",
            fill = self.var.theme1,
            anchor = "center"
        )
        self._text_nev_button_id = (button_text_id1,button_text_id2)
        
        #adding down save button and its text 
        self.save_button = Canvas(
            master = self.setting_screen_frame,
            height = self._gameexit_button_height,
            width = self._settingscreen_width ,
            bg = self.var.theme2
        )
        self.save_button_text_id = self.save_button.create_text(
            self._settingscreen_width // 2,
            self._gameexit_button_height // 2,
            font = ("Arial",self.var.home_text_size,'bold'),
            text = "Save",
            fill = self.var.theme1,
            anchor = "center"
        )
        # calculating main screen_ height and creating demo screen :0
        self.main_screen_height = self._settingscreen_height - self._gameexit_button_height - nev_button_height
        self.demo_screen = Canvas(
            master = self.setting_screen_frame,
            height = self.main_screen_height,
            width = self._settingscreen_width,
            bg = self.var.theme2
        )
    
    def Initialize_First_Screen(self):
        self.GAME_SCREEN = Game_screen(self.game_screen_frame,self.var,False)
        self.GAME_SCREEN.demo_screen_var_update(
            initialize=True,
            game_height = self._game_screen_height,
            game_width = self._game_screen_width
        )
        self.back_button = Canvas(
            master = self.game_screen_frame,
            height = self._gameexit_button_height,
            width = self._game_screen_width,
            bg = self.var.theme2
        )
        self.back_button_text_id = self.back_button.create_text(
            self._game_screen_width //2 , self._gameexit_button_height // 2,
            font = ("Arial", self.var.home_text_size, "bold"),
            text = "back",
            fill = self.var.theme1
        )
        self._possision_snack_and_idels()
        self.GAME_SCREEN.add_to_Master()
        self.back_button.pack()

    def Initialize_second_Screen(self):
        self._adding_second_screen_element()
        self.nevigation_button1.grid(row = 0, column = 0)
        self.nevigation_button2.grid(row = 0, column = 1)
        self.demo_screen.grid(row = 1, column = 0, columnspan = 2)
        self.save_button.grid(row = 2, column = 0, columnspan = 2)
    
    def change_screen(self,canvas:Canvas):
        """
        Change the current screen to a new canvas in the application.

        This method performs the following actions:
        1. Invokes the `__shift_button_button1` method with `None` as the argument.
        2. Removes the currently displayed screen (stored in `self.curent_screen`) from the grid.
        3. Updates `self.curent_screen` to the provided `canvas`.
        4. Displays the new canvas by placing it in the grid at row 1, column 0, spanning two columns.

        Args:
            canvas (Canvas): The new canvas to be displayed on the screen.
        """
        # self.__shift_button_button1(None)
        self.curent_screen.grid_forget()
        self.curent_screen = canvas
        self.curent_screen.grid(row = 1 , column = 0,columnspan = 2)    
        
    def _something(self):
        self.game_screen_frame.grid(row = 0, column = 0)
        self.setting_screen_frame.grid(row = 0, column = 1)
    
    def save_fucn(self,event):#need to fix
        pass
        # # getting_value
        # width = self.__width_get.get()
        # height = self.__Height_get.get()
        # speed = self.__Speed_get.get()
        # size = self.__Size_get.get()
        # text = self.__Text_get.get()
        # volume = self.__Volume_get.get()
        
        # #checking_if_value_is_ryt_or_not
        # if not (width.isdigit() and 360 <= int(width) <= 1440):
        #     messagebox.showerror("Error", "Width shoude be number and under and equal to 360 and 1440!")
        #     return None
        # if not (height.isdigit() and 180 <= int(height) <= 720):
        #     messagebox.showerror("Error", "Height shoude be number and under and equal to 180 and 720!")
        #     return None
        # speed = 100 if speed == 'Extreme' else 150 if speed == 'Fast' else 200 if speed ==  'Normal' else 300
        # size = 15 if size == 'Small' else 30 if size == "Medium" else 45 if size == 'Large' else 50
        
        # #saving_things :0
        # self.var.game_width = int(width)
        # self.var.game_height = int(height)
        # self.var.home_speed = speed
        # self.var.home_boxsize = size
        # self.var.home_text_size = text
        # self.var.volume_level = volume
        
        
        # self.var.update()
        
        # #amm just for check u know
        # print("=========================")
        # print(width)
        # print(height)
        # print(speed)
        # print(size)

    def _remove(self):
        self.GAME_SCREEN.remove_to_Master()
        self.back_button.pack_forget()
        self.game_screen_frame.grid_forget()
        self.nevigation_button1.grid_forget()
        self.nevigation_button2.grid_forget()
        self.demo_screen.grid_forget()
        self.save_button.grid_forget()
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
    def __init__(self,root:Tk ,var:Variable, setting_gui:setting_screen_gui) -> None:
        """
        Initialize the setting window screen with specified parameters.

        Args:
            root (Tk): The main Tkinter root window.
            theme (tuple[str,str]): A tuple containing theme colors.
            font_size (int): The font size for texts.
        """
        self.root = root
        self.var = var
        self.setting_gui = setting_gui
    
    def __account_setting_calling_func(self) -> None:
        """
        this function helps to confirm user password and also if password
        ryt then take them to account setting canvas:0
        """
        get_pass = self.taking_password_for_verification_window()
        if get_pass == self.var._player_acc_info["password"]:
            messagebox.showinfo("password matched","password matched now u can modify you account")
            self.setting_gui.current_screen.grid_forget()
            # self.
        else:
            messagebox.showinfo("wrong password","wrong password u cant modify your account")
    
    def __change_password_func(self) -> None:
        value1, value2 = self.change_password_window()
        
        if value1 is None:
            return None
        
        if not (value1 == value2):
            messagebox.showwarning("Password Mismatch", "The new password and confirmation do not match.")
            return None
        
        self.var.update_password(value1)
        
        if value1 == self.var._player_acc_info["password"]:
            messagebox.showinfo("Password Changed Successfully", "Your password has been updated successfully.")
        else:
            messagebox.showerror("Password Change Failed", "There was an error updating your password. Please try again.")
    
    def __create_new_account(self):
        self.create_new_account_window()
    
    def __change_account(self):
        self.change_account_window()
    
    def __go_back(self):
        self.account_setting_screen.grid_forget()
        self.basic_setting_screen.grid(row = 1 , column = 0,columnspan = 2)
        
    def create_shop_window(self,width:int, height:int, canvas:Canvas, info:tuple[tuple]) -> None:
        pass
    
    def create_account_window_or_update(self,master, width:int, height:int, grid_info:dict) -> tuple[Canvas,Canvas]:
        
        
        #1. creating canvas for account option beasic account setting
        self.basic_setting_screen = Canvas(
            master = master,
            height = height,
            width = width,
            bg = self.var.theme1
        )
        #collecing its var and all widgets in tuple[tuple[any, any]]
        args = self.var.basic_setting_screen_var(
            canvas = self.basic_setting_screen,
            sec_account_calling_method = self.__account_setting_calling_func
        )
        #adding widget list (args) to the basic_setting_screen
        self.creating_form_on_canvas(
            height = height,
            width = width,
            canvas = self.basic_setting_screen,
            *args
        )
        
        #2. creating canvas for account option account main setting
        self.account_setting_screen = Canvas(
            master = master,
            height = height,
            width = width,
            bg = self.var.theme1
        )
        #collecing its var and all widgets in tuple[tuple[any, any]]
        args = self.var.setting_option_menu_var(
            canvas = self.account_setting_screen,
            changepass_method = self.__change_password_func,
            createnewacc_method = self.__create_new_account,
            changeaccount_method = self.__create_new_account,
            goback_method = self.__go_back
        )
        #adding widget list (args) to the account_setting_screen
        self.creating_form_on_canvas(
            height = height,
            width = width,
            canvas = self.account_setting_screen,
            *args
        )
        
        
        
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