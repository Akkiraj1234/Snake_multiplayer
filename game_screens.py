from tkinter import Canvas, Frame, Button, Label, Entry, Toplevel ,Tk, messagebox
from random import choice

from game_idles import Food, goofy_Snakes, Snake, Heart_NEV, Heart, Coin
from variable import Variable


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
        self.random_food_color = None
        self.random_heart_color = None
        self.random_coin_color = None
        self.speed = None
        self.animation_after_ids=None
        self._middel_windows = 0
        self.header_info = (0,0)
        self.footer_info = (0,0)
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
            color = color
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
            color = color
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
            color = color
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
            insalize = False,
        )
        
        home_coin.new_coin((x , y),False)
        
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
            x , y = snake.coordinates
            
            if bool(self.food) and x == self.food.x and y == self.food.y:
                if self.random_food_color:
                    color = choice(self.color_list)
                    self.food.update_color(color)
                self.food.new_food()
            
            if bool(self.food) and bool(self.heart) and (x , y) == self.heart.coords:
                if self.random_heart_color:
                    color = choice(self.color_list)
                    self.heart.change_color(color)
                self.heart.new_heart(self.food.new_coordinates())
            
            if bool(self.food) and bool(self.coin) and (x , y) == self.coin.coords:
                if self.random_coin_color:
                    color = choice(self.color_list)
                    self.coin.change_color(color)
                self.coin.new_coin(self.food.new_coordinates())
                
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
        """
   
        self.var = var
        self.master = Master
        self.MASTER = Frame(self.master)
        
        self.NEVIGATION_CANVAS = None
        self.GAME_CANVAS = None
        self.SNAKE = None
        self.FOOD = None
        self.HEART = None
        self.MENU_OPTION = None
        self.SCORE_TEXT = None
        
        #game_variables
        self.game_height = self.var.game_height
        self.game_width = self.var.game_width
        self._game_bord_height = None
        self._nevigation_height = None
    
    def update(self):
        '''
        update the things
        '''
        #updating the color
        self.NEVIGATION_CANVAS.config(bg=self.var.NEV_COLOR)
        self.GAME_CANVAS.config(bg=self.var.CANVAS_COLOR)
        self.SNAKE.update_color(self.var.SNAKE_COLOR)
        self.FOOD.update_color(self.var.FOOD_COLOR)
        self.HEART.update_color(self.var.HEART_COLOR)
        self.NEVIGATION_CANVAS.itemconfig(self.MENU_OPTION,fill = self.var.TEXT_COLOR)
        self.NEVIGATION_CANVAS.itemconfig(self.SCORE_TEXT,fill = self.var.TEXT_COLOR)
        
        #updating height and rest
        pass
        
        
    def set_up(self) -> None:
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
        nevigation_height = self.game_height // 8
        nevigation_height = nevigation_height // self.var.game_box_size
        
        if not nevigation_height:
            self._nevigation_height = self.var.game_box_size * nevigation_height
        else:
            self._nevigation_height = self.var.game_box_size
            
        self._game_bord_height = self.game_height - self._nevigation_height
    
    def nevigation_setup(self) -> None:
        """
        This method sets up the navigation canvas with essential elements such as a heart icon
        representing the player's remaining lives, a score text displaying the current score,
        and a menu option for accessing game options or pausing the game.
        """
        braking_into_4 =  self._nevigation_height // 4
        Heart_size = braking_into_4 * 3
        pady = braking_into_4 // 4
        
        self.NEVIGATION_CANVAS = Canvas(
            master = self.MASTER,
            bg = self.var.NEV_COLOR,
            width = self.game_width,
            height = self._nevigation_height
            )
        
        self.HEART = Heart_NEV(
            canvas = self.NEVIGATION_CANVAS,
            color = self.var.HEART_COLOR,
            inisial_heart = self.var.INISISAL_HEART
            )
        
        self.SCORE_TEXT = self.NEVIGATION_CANVAS.create_text(
            self.game_width // 2,
            braking_into_4 * 2,
            font = ("Arial",braking_into_4 * 2,"bold"),
            text = f"Score: 0",
            fill = self.var.TEXT_COLOR
            )
        
        self.MENU_OPTION = self.NEVIGATION_CANVAS.create_text(
            30,
            braking_into_4 * 2,
            font = ("Arial", braking_into_4 * 2, "bold"),
            text = "Menu",
            fill = self.var.TEXT_COLOR
            )
    
    def game_canvas_setup(self) -> None:
        """
        This method sets up the game canvas with the snake and food objects.
        It creates a canvas widget with the specified background color, width,
        and height. Then, it initializes the snake and food objects on the canvas
        using the provided game variables.
        """
        self.GAME_CANVAS = Canvas(
            master = self.MASTER,
            bg = self.var.CANVAS_COLOR,
            width = self.game_width,
            height = self._game_bord_height
            )
        
        self.SNAKE = Snake(
            canvas = self.GAME_CANVAS,
            lenght = self.var.SNAKE_LENGHT,
            coordinates = self.var.SNAKE_CORDINATES,
            color = self.var.SNAKE_COLOR,
            box_size = self.var.game_box_size
            )
        
        self.FOOD = Food(
            canvas = self.GAME_CANVAS,
            box_size = self.var.game_box_size,
            color = self.var.FOOD_COLOR
            )
    
    def update_things(self,**kwargs):
        """
        Update game elements based on provided keyword arguments.

        Args:
            **kwargs: Keyword arguments to update game elements. Available args:
                      - score: Score to be updated.
        """
        if kwargs.get('score',None):
            self.NEVIGATION_CANVAS.itemconfig(
                self.SCORE_TEXT,text=f"Score: {kwargs['score']}"
            )
    
    def add_to_Master(self,side = "left",side_status = True)->None:
        """
        Pack the navigation and game canvases and add it to master
        """
        if side_status:
            self.MASTER.pack()
        else:
            self.MASTER.pack(side=side)
            
        self.NEVIGATION_CANVAS.pack()
        self.GAME_CANVAS.pack()

    def remove_to_Master(self)-> None:
        """
        remove the navigation and game canvases. from master
        """
        self.NEVIGATION_CANVAS.pack_forget()
        self.GAME_CANVAS.pack_forget()
        self.MASTER.pack_forget()


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



class setting_option_menu:
    '''
    this class will inisalize option menu for the setting where they can change settings
    '''
    
    def __init__(self,master:Frame,var:Variable,canvas_height:int, canvas_width:int, nevigation_height:int, button_height:int , root) -> None:
        self._master = master
        self.var = var
        self.root = root
        self._canvas_height = canvas_height
        self._canvas_width  = canvas_width
        self._nevigation_height  = nevigation_height
        self._game_button_height = button_height
        
        self.height_main_canvs = (self._canvas_height - self._nevigation_height) - self._game_button_height
        self.width_main_canvs  = self._canvas_width - 14
        
        self.curent_screen = None
        
        #creating_instance
        self.windows = WindowGenerator(
            root = self.root,
            theme = (self.var.theme1 , self.var.theme2),
            font_size = self.var.home_text_size,
            height = self.height_main_canvs,
            width = self.width_main_canvs
        )
        
        self.INISALIZING_SETTING_SCREEN()
        self.inisalizing_windows()
        
    def inisalizing_windows(self) -> None:
        basic_setting_screen = Canvas(
            master = self._master,
            height = self.height_main_canvs,
            width = self.width_main_canvs,
            bg = self.var.theme1
        )
        
        args = self.var.basic_setting_screen_var(
            basic_setting_screen,
            self.__acoount_setting_calling_func
        )
        
        self.basic_setting_screen = self.windows.creating_form_on_canvas(
            self.height_main_canvs,
            self.width_main_canvs,
            basic_setting_screen,
            *args
        )
        account_setting_screen = Canvas(
            master = self._master,
            height = self.height_main_canvs,
            width = self.width_main_canvs,
            bg = self.var.theme1
        )
        
        args = self.var.setting_option_menu_var(
            account_setting_screen,
            self.__change_password_func,
            self.__create_new_account,
            self.__change_account,
            self.__go_back
        )
        
        #setting_widget_in Canvas
        self.account_setting_screen = self.windows.creating_form_on_canvas(
            self.height_main_canvs,
            self.width_main_canvs,
            account_setting_screen,
            *args
        )
        
    def INISALIZING_SETTING_SCREEN(self) -> None:
        '''
        inisalize the setting screen with all obj requird in screen
        like nevigation nuttons-2, save button-1
        inclue :-
            - nevigation_button1 : game button canvs
            - nevigation_button2 : account button canvs
            - _text_nev_button1  : game_button_text_id
            - _text_nev_button2  : account_button_text_id
            - save_button        : save button canvas
            - _save_button_text_itemid : save button_text id

        return :
            None
        '''
        #nevigation button1 game option
        self.nevigation_button1 = Canvas(
            master = self._master,
            height = self._nevigation_height,
            width= self._canvas_width // 2 -7 , #7 is the width of white border for adjusing width
            bg = self.var.theme1
        )
        #nevigation button2 account option
        self.nevigation_button2 = Canvas(
            master = self._master,
            height = self._nevigation_height,
            width= self._canvas_width // 2 -7 ,
            bg = self.var.theme2
        )
        #nevigation button1 game option text and itemid
        self._text_nev_button1 = self.nevigation_button1.create_text(
            self._canvas_width // 4 , self._nevigation_height //2,
            font = ("Arial",self.var.home_text_size,'bold'),
            text = "Shop",
            fill = self.var.theme2
        )
        #nevigation button2 account option text and itemid
        self._text_nev_button2 = self.nevigation_button2.create_text(
            self._canvas_width // 4 , self._nevigation_height //2,
            font = ("Arial",self.var.home_text_size,'bold'),
            text = "Setting",
            fill = self.var.theme1
        )
        
        #adding save buttone
        self.save_button = Canvas(
            master = self._master,
            height = self._game_button_height,
            width = self._canvas_width -14,
            bg = self.var.theme2
        )
        #save_button_text_id
        self._save_button_text_itemid = self.save_button.create_text(
            self._canvas_width // 2,self._game_button_height // 2,
            font = ("Arial",self.var.home_text_size,'bold'),
            text = "Save",
            fill = self.var.theme1
        )
        
    def __acoount_setting_calling_func(self) ->None:
        '''
        this function helps to confirm user password and also if password
        ryt then take them to account setting canvas:0
        '''
        get_pass = self.windows.taking_password_for_verification_window()
        if get_pass == self.var._player_acc_info["password"]:
            messagebox.showinfo("password matched","password matched now u can modify you account")
            self.basic_setting_screen.grid_forget()
            self.account_setting_screen.grid(row = 1 , column = 0,columnspan = 2)
        else:
            messagebox.showinfo("wrong password","wrong password u cant modify your account")
    
    def __change_password_func(self):
        value1 , value2 = self.windows.change_password_window()
        
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
        self.windows.create_new_account_window()
    
    def __change_account(self):
        self.windows.change_account_window()
    
    def __go_back(self):
        self.account_setting_screen.grid_forget()
        self.basic_setting_screen.grid(row = 1 , column = 0,columnspan = 2)
        
    def save_fucn(self,event):#need to fix
        # getting_value
        width = self.__width_get.get()
        height = self.__Height_get.get()
        speed = self.__Speed_get.get()
        size = self.__Size_get.get()
        text = self.__Text_get.get()
        volume = self.__Volume_get.get()
        
        #checking_if_value_is_ryt_or_not
        if not (width.isdigit() and 360 <= int(width) <= 1440):
            messagebox.showerror("Error", "Width shoude be number and under and equal to 360 and 1440!")
            return None
        if not (height.isdigit() and 180 <= int(height) <= 720):
            messagebox.showerror("Error", "Height shoude be number and under and equal to 180 and 720!")
            return None
        speed = 100 if speed == 'Extreme' else 150 if speed == 'Fast' else 200 if speed ==  'Normal' else 300
        size = 15 if size == 'Small' else 30 if size == "Medium" else 45 if size == 'Large' else 50
        
        #saving_things :0
        self.var.game_width = int(width)
        self.var.game_height = int(height)
        self.var.home_speed = speed
        self.var.home_boxsize = size
        self.var.home_text_size = text
        self.var.volume_level = volume
        
        
        self.var.update()
        
        #amm just for check u know
        print("=========================")
        print(width)
        print(height)
        print(speed)
        print(size)
        
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
        self.__shift_button_button1(None)
        self.curent_screen.grid_forget()
        self.curent_screen = canvas
        self.curent_screen.grid(row = 1 , column = 0,columnspan = 2)    
    
    def __shift_button_button1(self,event):
        """
        Handle the event when navigation button 1 is clicked.

        This method updates the background colors and text colors of two navigation buttons to reflect
        the active state of button 1. It also switches the visible screen by hiding the basic setting 
        and account setting screens, and displaying the current screen.

        Args:
            event: The event that triggered this method.
        """
        self.nevigation_button1.config(bg = self.var.theme1)
        self.nevigation_button1.itemconfig(self._text_nev_button2, fill = self.var.theme2)
        self.nevigation_button2.config(bg = self.var.theme2)
        self.nevigation_button2.itemconfig(self._text_nev_button1, fill = self.var.theme1)
        #button1 acction code 
        self.basic_setting_screen.grid_forget()#even if its not grid already its simply pass so needa worry
        self.account_setting_screen.grid_forget()
        self.curent_screen.grid(row = 1 , column = 0,columnspan = 2)
    
    def __shift_button_button2(self,event):
        """
        Handle the event when navigation button 2 is clicked.

        This method updates the background colors and text colors of two navigation buttons to reflect
        the active state of button 2. It also switches the visible screen by hiding the current screen 
        and account setting screens, and displaying the basic setting screen.

        Args:
            event: The event that triggered this method.
        """
        self.nevigation_button1.config(bg = self.var.theme2)
        self.nevigation_button1.itemconfig(self._text_nev_button1, fill = self.var.theme1)
        self.nevigation_button2.config(bg = self.var.theme1)
        self.nevigation_button2.itemconfig(self._text_nev_button2, fill = self.var.theme2)
        #button2 acction code 
        self.curent_screen.grid_forget()
        self.account_setting_screen.grid_forget()
        self.basic_setting_screen.grid(row = 1 , column = 0,columnspan = 2)
        
    def BIND_KEYS(self) -> None:
        '''
        bind the keys for setting screen
            - nevigation_button1 -game
            - nevigation_button2 -account
            - save_button
        '''
        self.nevigation_button1.bind("<Button-1>",self.__shift_button_button1)
        self.nevigation_button2.bind("<Button-1>",self.__shift_button_button2)
        self.save_button.bind("<Button-1>",self.save_fucn)
    
    def REMOVE_BIND_KEYS(self) -> None:
        '''
        undbin all the setting keys at once
        '''
        self.nevigation_button1.unbind_all("<Button-1>")
        self.nevigation_button2.unbind_all("<Button-1>")
        self.save_button.unbind_all("<Button-1>")
        
    def PACK_CURRENT_SCREEN(self) -> None:
        """
        Packs the current screen and associated navigation and save
        buttons into the grid layout and add binding of keys.
        
        If current_screen is None, the method returns None.
        """
        if self.curent_screen is None:
            return None
        
        self.nevigation_button1.grid(row = 0, column = 0)
        self.nevigation_button2.grid(row = 0, column = 1)
        self.curent_screen.grid(row = 1 , column = 0,columnspan = 2)
        self.save_button.grid(row = 2 , column = 0 , columnspan = 2)
        
        self.BIND_KEYS()
    
    def REMOVE_CURRENT_SCREEN(self) -> None:
        """
        Removes the current screen and associated navigation and 
        save buttons from the grid layout and remove all binded keys.
        
        If current_screen is None, the method returns None.
        """
        if self.curent_screen is None:
            return None
        self.REMOVE_BIND_KEYS()
        
        self.nevigation_button1.grid_forget()
        self.nevigation_button2.grid_forget()
        self.curent_screen.grid_forget()
        self.save_button.grid_forget()




