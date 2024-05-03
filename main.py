from game_idles import Snake,Food,Heart
from game_screens import inisial_screens

from tkinter import Tk,Canvas,Button,Label,Frame
from random import choice , randint

import json
import time


class variable:
    """
    A class for managing game-related variables and settings.

    This class serves the purpose of centralizing game variables, 
    preventing unnecessary copies, and providing control over variables
    in one place. It handles the following tasks:

    1. **Initialization**: Loads game variables from JSON files.
    2. **Updates**: Manages updates to game variables.
    3. **Settings**: Handles user settings and game settings.

    Use this class to streamline variable management and ensure
    consistency across your game.
    
    METHODS:
        - __init__(): this method inisalize the all game variables
        - getting_and_extracting_info(): this method gather all json data
        - update_user_settings(): this method update user_setting json
        - updaing_game_setting(): this method update game_setting json
        - update_password(): this method update user password
        - update(): this method update both user info and game info
    """
    
    def __init__(self) -> None:
        """
        Initialize the game and user variables by loading data from JSON files.
        """
        self.getting_and_extracting_info()
        #game basic info that stay same for every user by changing it change but for all user
        self.background_color = self._game_setting["basic_info"]["background_color"]
        self.font_color = self._game_setting["basic_info"]["font_color"]
        self.game_width = self._game_setting["basic_info"]["game_width"]
        self.game_height = self._game_setting["basic_info"]["game_height"]
        self.box_size = self._game_setting["basic_info"]["box_size"]
        self.speed = self._game_setting["basic_info"]["speed"]
        
        #user info that changes by every new_users
        self.game_box_size = self._game_setting["game_info"]["box_size"]
        self.game_speed = self._game_setting["game_info"]["game_speed"]
        self.snake_color = self._player_acc_info["snake_color"]
        self.food_color = self._player_acc_info["food_color"]
        self.nevigation_color = self._player_acc_info["nevigation_color"]
        self.nevigation_text_color = self._player_acc_info["navigation_text_color"]
        self.heart_color = self._player_acc_info["heart_color"]
        
        #fixed and constant variables
        self.SNAKE_LENGHT = 3
        self.SNAKE_CORDINATES = (0,0)
        self.SNAKE_LOSS_COUNTDOWN = 2
        self.FONT_STYLE = "Press Start 2P"
        self.INISIAL_HOME_TEXT = "Sneck suffarie :0"
        
        self.FOOD_TYPE = self._player_acc_info["food_type"]
        self.INISISAL_HEART = self._player_acc_info["INISISAL_HEART"]
        self.SNAKE_TYPE = self._player_acc_info["sneck_type"]
        
        #the variable constantally changing are (*change by users)
        self.HIGHT_SCORE = self._player_acc_info["HIGH_SCORE"]
        self.POINTES = self._player_acc_info["points"]
        self.ACCOUNT_NAME = self._player_acc_info["name"]
    
    def getting_and_extracting_info(self) -> None:
        """
        Extract information from JSON files.

        This method extracts game settings information from a 'setting.json' file
        and player account details from a file named after the player's account name.
        It initializes the class attributes '_game_setting' and '_player_acc_info'
        with the extracted data.
        """
        # Extracting game setting info
        with open("Game_assets\\setting.json","r",encoding="utf-8") as Game_settings:
            self._game_setting = json.load(Game_settings)
            
        #gathering player account_name
        self.account_name = self._game_setting["game_info"]["Account"]
            
        # Extracting player information by id
        with open(f"player_info\\{self.account_name}.json","r",encoding="utf-8") as Account_details:
            self._player_acc_info = json.load(Account_details)
        
    def update_user_settings(self) -> None:
        """
        Update user settings in the player account JSON file 
        by anything changes on the variable.
        """
        self._player_acc_info["name"] = self.ACCOUNT_NAME
        self._player_acc_info["snake_color"] = self.snake_color
        self._player_acc_info["food_color"] = self.food_color
        self._player_acc_info["nevigation_color"] = self.nevigation_color
        self._player_acc_info["navigation_text_color"] = self.nevigation_text_color
        self._player_acc_info["heart_color"] = self.heart_color
        self._player_acc_info["INISISAL_HEART"] = self.INISISAL_HEART
        self._player_acc_info["food_type"] = self.FOOD_TYPE
        self._player_acc_info["sneck_type"] = self.SNAKE_TYPE
        self._player_acc_info["HIGH_SCORE"] = self.HIGHT_SCORE
        self._player_acc_info["points"] = self.POINTES
        
        with open(f"player_info\\{self.account_name}.json", "w", encoding="utf-8") as player_file:
            json.dump(self._player_acc_info, player_file,)
        
    def updaing_game_setting(self) -> None:
        """
        Update game settings in the 'setting.json' file.
        by anything chnageed on the variable
        """
        self._game_setting["basic_info"]["background_color"] = self.background_color
        self._game_setting["basic_info"]["font_color"] = self.font_color
        self._game_setting["basic_info"]["game_width"] = self.game_width
        self._game_setting["basic_info"]["game_height"] = self.game_height
        self._game_setting["basic_info"]["box_size"] = self.box_size
        self._game_setting["basic_info"]["speed"] = self.speed
        self._game_setting["game_info"]["box_size"] = self.game_box_size
        self._game_setting["game_info"]["game_speed"] = self.game_speed
        self._game_setting["game_info"]["Account"] = self.ACCOUNT_NAME
        
        with open("Game_assets\\setting.json","w",encoding="utf-8") as game_setting:
            json.dump(self._game_setting,game_setting)
    
    def update_password(self) -> None:
        """
        Update the player's account password.

        This method updates the password associated with the player's account.
        However, it's currently implemented as a placeholder and does not perform
        any actual password update operation. Future implementation should include
        appropriate security measures for updating passwords.
        """
        # self._player_acc_info["password"] = password
        pass
    
    def update(self) -> None:
        """
        Update both user and game settings.
        """
        self.update_user_settings()
        self.updaing_game_setting()
        
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
   
    def __init__(self,Master:Tk,var:variable) -> None:
        """Initialize the game screen. 
        with main game canvas and nevigation panel
        and sneck ,  food in hevigation heart score board,
        and menu option

        Args:
            Master (Tk): The parent Tkinter window.
            var (variable): An object containing game variables.
        """
   
        self.var = var
        self.MASTER = Master
        
        self.NEVIGATION_CANVAS = None
        self.GAME_CANVAS = None
        self.SNAKE = None
        self.FOOD = None
        self.HEART = None
        self.MENU_OPTION = None
        self.SCORE_TEXT = None
        
        #game_variables
        self._game_bord_height = None
        self._nevigation_height = None
        
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
        nevigation_height = self.var.game_height // 8
        nevigation_height = nevigation_height // self.var.game_box_size
        
        if not nevigation_height:
            self._nevigation_height = self.var.game_box_size * nevigation_height
        else:
            self._nevigation_height = self.var.game_box_size
            
        self._game_bord_height = self.var.game_height - self._nevigation_height
    
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
            bg = self.var.nevigation_color,
            width = self.var.game_width,
            height = self._nevigation_height
            )
        self.HEART = Heart(
            canvas = self.NEVIGATION_CANVAS,
            cordnites = (self.var.game_width - Heart_size,pady),
            box_size = Heart_size,
            color = self.var.heart_color,
            inisial_heart = self.var.INISISAL_HEART
            )
        self.SCORE_TEXT = self.NEVIGATION_CANVAS.create_text(
            self.var.game_width // 2,
            braking_into_4 * 2,
            font = ("Arial",braking_into_4 * 2,"bold"),
            text = f"Score: 0",
            fill = self.var.nevigation_text_color
            )
        self.MENU_OPTION = self.NEVIGATION_CANVAS.create_text(
            30,
            braking_into_4 * 2,
            font = ("Arial", braking_into_4 * 2, "bold"),
            text = "Menu",
            fill = self.var.nevigation_text_color
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
            bg = self.var.background_color,
            width = self.var.game_width,
            height = self._game_bord_height
            )
        
        self.SNAKE = Snake(
            canvas = self.GAME_CANVAS,
            lenght = self.var.SNAKE_LENGHT,
            coordinates = self.var.SNAKE_CORDINATES,
            color = self.var.snake_color,
            box_size = self.var.game_box_size
            )
        
        self.FOOD = Food(
            canvas = self.GAME_CANVAS,
            box_size = self.var.game_box_size,
            color = self.var.food_color,
            game_width = self.var.game_width,
            game_height = self._game_bord_height,
            food_type = self.var.FOOD_TYPE
            )
    
    def update_things(self,**kwargs):
        """
        Update game elements based on provided keyword arguments.

        Args:
            **kwargs: Keyword arguments to update game elements. Available args:
                      - score: Score to be updated.
        """
        if "score" in kwargs:
            self.NEVIGATION_CANVAS.itemconfig(
                self.SCORE_TEXT,text=f"Score: {kwargs['score']}"
            )
    
    def add_to_Master(self)->None:
        """
        Pack the navigation and game canvases and add it to master
        """
        self.NEVIGATION_CANVAS.pack()
        self.GAME_CANVAS.pack()

    def remove_to_Master(self)-> None:
        """
        remove the navigation and game canvases. from master
        """
        self.NEVIGATION_CANVAS.pack_forget()
        self.GAME_CANVAS.pack_forget()


class Game_engion:
    """
    This class controls the main game.

    Attributes:
    - MASTER (Tk): The master Tkinter window.
    - var (variable): An object containing game variables/settings.
    - SCORE (int): The player's score.
    - direction (str): The current direction of the snake.
    - master_after_ids: ID returned by `Tk.after()` for animation control.
    - stop_game_animation (bool): Flag to control game animation.
    - _old_time_ (float): Timestamp for tracking time.

    Methods:
    - __init__(Master: Tk, var: variable): Initializes the game engine.
    - _bild_key(): Binds keys for game control.
    - _remove_bind_key(): Unbinds keys.
    - _change_direction(direction: str): Changes the snake's direction.
    - _check_collision(sneckx, snecky): Checks for collisions.
    - _check_loss(): Checks if the game is lost.
    - PLAY_THE_GAME(): Controls the game loop.
    - PAUSE_GAME(status: str): Pauses or ends the game.
    - RESTART_GAME(): Restarts the game.
    - ADD_TO_SCREEN(): Adds the game screen to the master window.
    """
    
    def __init__(self, Master:Tk, var:variable) -> None:
        """
        Initializes the Game_engion object.

        Parameters:
        - Master (Tk): The master Tkinter window.
        - var (variable): An object containing variables/settings for the game.
        """
        self.MASTER = Master
        self.var = var
        
        #varibales needed
        self.SCORE = 0
        self.direction = "down"
        self.master_after_ids = None
        self.stop_game_animation = False
        self._old_time_ = 0
        
        #creating screen
        self.GAME_FRAME = Game_screen(self.MASTER,self.var)
        self.pause_screen = None
        
    def _bild_key(self) -> None:
        '''
        Binds keys for controlling the game.
        - binding
            - left , right , down , up key for movment 
            - a , d , w , s key for movemnt 
            - p , menu button and right click for pausing the game
        
        this menthod only purpose is to bind keys  
        '''
        self.button_binds_id_game_bord =[
        self.MASTER.bind('<Left>', lambda event: self._change_direction('left')),
        self.MASTER.bind('<Right>', lambda event: self._change_direction('right')),
        self.MASTER.bind('<Up>', lambda event: self._change_direction('up')),
        self.MASTER.bind('<Down>', lambda event: self._change_direction('down')),
        self.MASTER.bind('<a>', lambda event: self._change_direction('left')),
        self.MASTER.bind('<d>', lambda event: self._change_direction('right')),
        self.MASTER.bind('<w>', lambda event: self._change_direction('up')),
        self.MASTER.bind('<s>', lambda event: self._change_direction('down')),
        # stop and resume menu binding by p 
        self.MASTER.bind("<p>",lambda event: self.PAUSE_GAME("pause")),
        
        #binding home button for paush menu
        self.GAME_FRAME.GAME_CANVAS.bind("<Button-1>",lambda event: self.PAUSE_GAME("pause")),
        
        #binding right click on canvas for stoping the game
        self.GAME_FRAME.NEVIGATION_CANVAS.tag_bind(self.GAME_FRAME.MENU_OPTION,"<Button-1>",lambda event: self.PAUSE_GAME("pause")),
        ]
    
    def _remove_bind_key(self) -> None:
        """
        remove all the binding of the key used in game screen
        """
        self.MASTER.unbind('<Left>', self.button_binds_id_game_bord[0])
        self.MASTER.unbind('<Right>', self.button_binds_id_game_bord[1])
        self.MASTER.unbind('<Up>', self.button_binds_id_game_bord[2])
        self.MASTER.unbind('<Down>', self.button_binds_id_game_bord[3])
        self.MASTER.unbind('<a>', self.button_binds_id_game_bord[4])
        self.MASTER.unbind('<d>', self.button_binds_id_game_bord[5])
        self.MASTER.unbind('<w>', self.button_binds_id_game_bord[6])
        self.MASTER.unbind('<s>', self.button_binds_id_game_bord[7])
        self.MASTER.unbind("<p>", self.button_binds_id_game_bord[8])
        self.GAME_FRAME.GAME_CANVAS.unbind("<Button-1>",self.button_binds_id_game_bord[9])
        
        self.GAME_FRAME.NEVIGATION_CANVAS.tag_unbind(
            self.GAME_FRAME.MENU_OPTION,"<Button-1>",self.button_binds_id_game_bord[10])
        
    def _change_direction(self,direction) -> None:
        """
        Changes the direction of the snake.

        Parameters:
        - direction (str): The direction to change to.
        """
        if direction in ("down","up") and self.direction in ("down","up"):
            pass
        elif direction in ("right","left") and self.direction in ("right","left"):
            pass
        else: self.direction = direction
    
    def _check_collision(self, sneckx:int , snecky:int )-> None:
        """
        Checks for collisions with walls or itself.

        Parameters:
        - sneckx (int): X-coordinate of the snake's head.
        - snecky (int): Y-coordinate of the snake's head.
        """
        # checking collision with walls
        if sneckx < 0 or sneckx >= self.var.game_width or \
            snecky < 0 or snecky >= self.GAME_FRAME._game_bord_height:
                self._check_loss()
        
        #checking collision with it's self
        for i in range(1,len(self.GAME_FRAME.SNAKE.snake_coordinates)-1):
            x,y = self.GAME_FRAME.SNAKE.snake_coordinates[i]
            if sneckx == x and snecky == y:
                self._check_loss()
    
    def _check_loss(self) -> None:
        """
        Checks if the game is over by monitoring the number of hearts left and a countdown
        for each heart loss.

        If the time since the last heart loss exceeds the specified countdown duration,
        and there is only one heart left, the game is considered over, and the
        `UPDATION_AFTER_GAME_OVER()` method is called.

        Returns:
        - None: If the game is not over.

        Notes:
        - This method relies on the `GAME_FRAME.HEART` attribute to access heart-related
        functionality.
        - The `SNAKE_LOSS_COUNTDOWN` variable from the `var` attribute is used to determine
        the time interval between each heart loss.
        """
        current_time = time.time()
        #checking if the collision happens between the countdown of heart loss if not pass
        if not (current_time - self._old_time_ > self.var.SNAKE_LOSS_COUNTDOWN):
            return None
        
        # if all heart is not gone yet call remove one heart else game over 
        # and call the UPDATION_AFTER_GAME_OVER method
        if len(self.GAME_FRAME.HEART.hearts_list) > 1:
            self.GAME_FRAME.HEART.remmove_heart()
        else:
            self.GAME_FRAME.HEART.remmove_heart()
            self.UPDATION_AFTER_GAME_OVER()
        
        self._old_time_ = current_time      
    
    def PLAY_THE_GAME(self) -> None:
        """
        Controls the main gameplay loop.

        This method updates the snake's position, checks for collisions,
        updates the score, and schedules the next iteration of the game loop.

        If the game animation is stopped, it cancels the scheduled updates.

        Note:
        - This method is intended to be called recursively to create the game loop.

        """
        #insializing variables
        remove = True
        sneckx , snecky = self.GAME_FRAME.SNAKE.snake_coordinates[0]
        foodx , foody = self.GAME_FRAME.FOOD.x , self.GAME_FRAME.FOOD.y
        
        #moving the snack by direction
        if self.direction == "up":
            snecky -= self.var.game_box_size
        elif self.direction == "down":
            snecky += self.var.game_box_size
        elif self.direction == "right":
            sneckx += self.var.game_box_size
        elif self.direction == "left":
            sneckx -= self.var.game_box_size
        
        #checking if snack collision with food or not if yes 
        # create new food and add up score
        if sneckx == foodx and snecky == foody:
            remove = False
            self.GAME_FRAME.FOOD.new_food("oval")#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! food styles modification
            self.SCORE +=1
        
        #updaing things and collection after id
        self.GAME_FRAME.SNAKE.move_snake(sneckx,snecky,remove)
        self.GAME_FRAME.update_things(score = self.SCORE)
        self._check_collision(sneckx,snecky)
        self.master_after_ids = self.MASTER.after(
            self.var.game_speed,
            self.PLAY_THE_GAME
            )
        
        #checking if game pause is called or not
        if self.stop_game_animation:
            self.MASTER.after_cancel(self.master_after_ids)
            
    def UPDATION_AFTER_GAME_OVER(self) -> None:
        """
        Handles post-game update actions.

        Updates the high score if the current score surpasses it,
        then triggers user settings update.

        Parameters:
        - status (str): Game outcome ('loss' or 'high_score').
        """
        status = 'loss'
        
        if self.SCORE > self.var.HIGHT_SCORE:
            self.var.HIGHT_SCORE = self.SCORE
            status = 'high_score'
            
        # self.var.update()
        self.var.update_user_settings()
        self.PAUSE_GAME(status)
            
            
    def PAUSE_GAME(self,status:str) -> None:
        """
        Pauses the game and displays relevant information based on the game status.

        Parameters:
        - status (str): The current game status. It can be one of the following:
            - 'pause': Indicates that the game is paused.
            - 'loss': Indicates that the player has lost the game.
            - 'high_score': Indicates that the player has achieved a new high score.

        Behavior:
        - If the status is 'pause', the method pauses the game and displays a message indicating that the game is paused.
        - If the status is 'loss', the method displays a message indicating that the player has lost the game, along with the current score.
        - If the status is 'high_score', the method displays a message indicating that the player has achieved a new high score, along with the score itself.

        The method also removes the game canvases from the master window, unbinds keys, sets the stop_game_animation flag to True, and updates the pause screen accordingly.
        """
        
        #the remove_resume variable idicating weather to remove
        #deactive resume button from pause screen or not
        deacive_resume = False
        #checking weater game is pause lost or new high score based on that making text
        if status == "pause":
            text = 'Game is Paused'
        if status == "loss":
            text = f'You lose :(  score: {self.SCORE}'
            deacive_resume = True
        if status == "high_score":
            text = f'New High Score:0   {self.SCORE}'
            deacive_resume = True
        
        #removeing canvas binded keys and stoping game animation
        self.GAME_FRAME.remove_to_Master()
        self._remove_bind_key()
        self.stop_game_animation = True
        
        
        if self.pause_screen: #if i inisalize the pause screen or its not None then
            #Windows_list[0] becouse while creating pause screen we added text lable in index 0
            id = self.pause_screen.Windows_list[0]
            id.config(text=text)
            
            if deacive_resume:
                #Windows_list[1] becouse while creating pause screen we added resume button in index 1
                resume = self.pause_screen.Windows_list[1]
                resume.config(state='disabled')
                
            self.pause_screen.add_to_master()
                
                
    def set_everrything_to_default(self) -> None:
        """
        Resets all game-related variables and components to their default states.

        Behavior:
        - Sets the stop_game_animation flag to False, allowing the game animation to resume.
        - Resets the player's score to 0 and updates the score display on the game frame.
        - Removes all hearts from the heart display and adds the default number of hearts back.
        - Resets the snake's length to the initial length.
        - Resets the snake's direction to 'down'.
        - Moves the snake's position to the initial coordinates.
        - Resets the food's position to a new location.
        - If a pause screen exists, enables the resume button.

        Note:
        - This method is typically called when restarting the game.
        """
        #set stop_game_animation to false
        self.stop_game_animation = False
        
        #setting score to 0 and updating the text
        self.SCORE = 0
        self.GAME_FRAME.update_things(score = self.SCORE)
        
        #setting heart to therre inisisal value
        self.GAME_FRAME.HEART.remove_all_heart()
        self.GAME_FRAME.HEART.add_heart_in_range(self.var.INISISAL_HEART)
        
        #setting sneck lenght to inisial lenght and directiong to 
        #down and cordinates to (0,0) all done by the method get_to_inisial_posision
        self.direction = "down"
        self.GAME_FRAME.SNAKE.get_to_inisial_posision()
        
        #food to new loaction
        self.GAME_FRAME.FOOD.new_food()
        
        if self.pause_screen:
            #if pause_screen inisalize then making resume button 
            # to normal again as an default
            resume = self.pause_screen.Windows_list[1]
            resume.config(state= 'normal')
    
    def ADD_TO_SCREEN(self) -> None:
        """
        Adds the game frame to the master window and sets up key bindings for game controls.

        Behavior:
        - Packs the game frame onto the master window for display.
        - Binds keys for controlling the snake's movement and pausing the game.
        - Sets the stop_game_animation flag to False, allowing the game animation to start.

        Note:
        - This method should be called when starting or resuming the game.
        """
        self.GAME_FRAME.add_to_Master()
        self._bild_key()
        self.stop_game_animation = False
    
    

def home_screen_inisalization(Master:Tk, var:variable) -> inisial_screens:
    """
    Initialize the home screen with specified parameters and widgets.

    Parameters:
    - Master (Tk): The master Tkinter window.
    - var (variable): An object containing variables/settings for the home screen.

    Returns:
    - inisial_screens: An instance of the initialized home screen.
    """
    
    # Initialize the home screen with specified parameters 
    # using var obj pack is true
    Home_window = inisial_screens(
        master = Master,
        background_color = var.background_color,
        game_width = var.game_width,
        box_size = var.box_size,
        game_height = var.game_height,
        speed = var.speed,
        pack = True
        )
    
    # Add snakes and food to the home screen
    Home_window.add_snakes("red", (0,0), 5, "down")
    Home_window.add_snakes("pink", (4,2), 8, "left")
    Home_window.add_snakes("grey", (1,3), 3, "right")
    Home_window.add_snakes("blue", (4,4), 4, "up")
    Home_window.add_snakes("yellow", (2,1), 3, "down")
    Home_window.add_food("red", "any", True)
    
    # Create and configure label widget
    lable = Label(
        master = Home_window.child_window,
        text = var.INISIAL_HOME_TEXT,
        bg = var.background_color,
        fg = var.font_color,
        font = (var.FONT_STYLE,30),
        relief = "flat"
        )
    
    # Create and configure 'Play' button widget
    button = Button(
        master = Home_window.child_window,
        text = "Play",
        command = play_home,
        width = 10,
        bg = var.background_color,
        fg = var.font_color,
        font = (var.FONT_STYLE,10),
        relief="groove"
        )
    
    # Create and configure 'Settings' button widget
    button1 = Button(
        Home_window.child_window,
        text = "Settings",
        command = setting_home,
        width = 10,
        bg = var.background_color,
        fg = var.font_color,
        font = (var.FONT_STYLE,10),
        relief = "groove"
        )
    
    # Create and configure 'shop' button widget
    button2 = Button(
        master = Home_window.child_window,
        text = "Shop",
        command = shop_home,
        width = 10,
        bg = var.background_color,
        fg = var.font_color,
        font = (var.FONT_STYLE,10),
        relief = "groove"
        )
    
    # Create and configure 'about me' button widget
    button3 = Button(
        master = Home_window.child_window,
        text = "about me",
        command = about_me_home,
        width = 10,
        bg = var.background_color,
        fg = var.font_color,
        font = (var.FONT_STYLE,10),
        relief = "groove"
        )
    
    # adding buttons to the home_window canvas and then
    # returning the instance of the home_window
    Home_window.add_button(lable, button, button1, button2 ,button3)
    return Home_window


def pause_menu_stabalization(master:Tk, var:variable) -> inisial_screens:
    """
    Creates a pause menu screen for the game.

    Args:
    - master (Tk): The master Tkinter window.
    - var (variable): An object containing variables/settings for the game.

    Returns:
    - inisial_screens: An instance of the pause menu screen.

    Behavior:
    - Creates a pause menu screen with a label displaying "Game is Paused" and buttons for "Resume",
      "Restart", and "Home".
    - Sets appropriate attributes and styling for the label and buttons based on the provided variables.
    - Adds the label and buttons to the pause menu screen.
    - Returns the pause menu screen instance.

    Note:
    - This function is intended to be called when pausing the game to display the pause menu.
    """
    pause_game_screen = inisial_screens(
        master = master,
        background_color = var.background_color,
        game_width = var.game_width,
        game_height = var.game_height,
        box_size = var.box_size,
        speed = var.game_speed,
        pack = False
    )
    # adding buttones
    
    Label1 = Label(
        master = pause_game_screen.child_window,
        text = "Game is Paused",
        bg = var.background_color,
        fg = var.font_color,
        font = (var.FONT_STYLE,15),
        relief = "flat"
    )
    Button1 = Button(
        master = pause_game_screen.child_window,
        text = "Resume",
        command = resume_pause_menu,
        width = 10,
        bg = var.background_color,
        fg = var.font_color,
        font = (var.FONT_STYLE, 10),
        relief = "groove"
    )
    
    Button2 = Button(
        master = pause_game_screen.child_window,
        text = "Restart",
        command = restart_pause_menu,
        width = 10,
        bg = var.background_color,
        fg = var.font_color,
        font = (var.FONT_STYLE, 10),
        relief = "groove"
    )
    
    Button3 = Button(
        master = pause_game_screen.child_window,
        text = "Home",
        command = home_pause_menu,
        width = 10,
        bg = var.background_color,
        fg = var.font_color,
        font = (var.FONT_STYLE, 10),
        relief = "groove"
    )
    
    #adding button to pause_game_screen and returning its instanse
    pause_game_screen.add_button(Label1,Button1,Button2,Button3)
    return pause_game_screen


def play_home():
    """
    Transition to the game screen from the home screen.

    Behavior:
    - Removes the home screen from the master window.
    - Adds the game screen to the master window and starts the game.
    - Prints a message indicating the transition.
    """
    home_screen.remove_from_master()
    game.ADD_TO_SCREEN()
    game.PLAY_THE_GAME()
    print("hmm lets play")

def setting_home():
    """
    Display settings options.

    Behavior:
    - Prints a message indicating the user's intent to access settings.
    """
    print("hmmm u wanna change something")

def shop_home():
    """
    Display shopping options.

    Behavior:
    - Prints a message indicating the user's intent to access shopping.
    """
    print("what u wanna shop :0")
    
def about_me_home():
    """
    Display information about the creator.

    Behavior:
    - Prints a message indicating the user's intent to learn about the creator.
    """
    print("hmmm u wanna know about me me crying :)")

def resume_pause_menu():
    """
    Resume the game from the pause menu.

    Behavior:
    - Removes the pause menu from the master window.
    - Adds the game screen to the master window and resumes the game.
    - Prints a message indicating the action taken.
    """
    pause_menu.remove_from_master()
    game.ADD_TO_SCREEN()
    game.PLAY_THE_GAME()
    print("wowow u clicked resume")

def restart_pause_menu():
    """
    Restart the game from the pause menu.

    Behavior:
    - Removes the pause menu from the master window.
    - Resets game settings to default and starts the game.
    - Prints a message indicating the action taken.
    """
    pause_menu.remove_from_master()
    game.set_everrything_to_default()
    game.ADD_TO_SCREEN()
    game.PLAY_THE_GAME()
    print("hmmm u wanna play again")

def home_pause_menu():
    """
    Return to the home screen from the pause menu.

    Behavior:
    - Removes the pause menu from the master window.
    - Resets game settings to default.
    - Adds the home screen to the master window and starts its animation.
    - Prints a message indicating the action taken.
    """
    pause_menu.remove_from_master()
    game.set_everrything_to_default()
    home_screen.add_to_master()
    home_screen.start_animation()
    print("hmm.... u wanna go home oki ! ")

def main(): 
    """
    Main function to initialize the game application.

    Behavior:
    - Sets the geometry and title of the root window.
    - Assigns the pause menu to the game object.
    - Starts the animation of the home screen.
    """
    root.geometry(f"{var.game_width}x{var.game_height}")
    root.title("title")
    game.pause_screen = pause_menu
    home_screen.start_animation()
    


if __name__ == "__main__":
    root = Tk()
    var = variable()
    
    home_screen = home_screen_inisalization(root, var)
    pause_menu = pause_menu_stabalization(root, var)
    game = Game_engion(Master=root, var=var)
    
    main()
    root.update()
    root.mainloop()
