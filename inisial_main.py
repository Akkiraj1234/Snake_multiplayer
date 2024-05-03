from game_idles import Snake,Food,Heart
from game_screens import inisial_screens

from tkinter import Tk,Canvas,Button,Label,Frame
from random import choice , randint

import json
import time


class variable:
    """
    Class to store game-related variables and manage updates.

    This class handles initialization of game variables from JSON files,
    updates to game variables, game settings, and casual settings.
    """
    
    def getting_and_extracting_info(self) -> None:
        """
        Extracts information from JSON files:
        1. Game settings information
        2. Account details
        
        Requirements:
            - JSON objects must be initialized before calling this function.
        
        Return:
            - None 
            - but inisalize self.game_setting and self.player_acc_info
        """
        
        # Extracting game setting info
        with open("setting.json","r",encoding="utf-8") as Game_settings:
            self._game_setting = json.load(Game_settings)
            
        #gathering player account_name
        account_name = self._game_setting["game_info"]["Account"]
            
        # Extracting player information by id
        with open(f"player_info\\{account_name}.json","r",encoding="utf-8") as Account_details:
            self._player_acc_info = json.load(Account_details)
        
    
    def __init__(self):
        """Initialize game variables."""
        self.getting_and_extracting_info()
        
        self.background_color = self._game_setting["basic_info"]["background_color"]
        self.font_color = self._game_setting["basic_info"]["font_color"]
        self.game_width = self._game_setting["basic_info"]["game_width"]
        self.game_height = self._game_setting["basic_info"]["game_height"]
        self.box_size = self._game_setting["basic_info"]["box_size"]
        self.speed = self._game_setting["basic_info"]["speed"]
        
        self.game_box_size = self._game_setting["game_info"]["box_size"]
        self.game_speed = self._game_setting["game_info"]["game_speed"]
        
        self.snake_color = self._player_acc_info["snake_color"]
        self.food_color = self._player_acc_info["food_color"]
        self.nevigation_color = self._player_acc_info["nevigation_color"]
        self.nevigation_text_color = self._player_acc_info["navigation_text_color"]
        self.heart_color = self._player_acc_info["heart_color"]
        
        #fixed values :0
        self.SNAKE_LENGHT = 3
        self.SNAKE_CORDINATES = (0,0)
        self.SNAKE_LOSS_COUNTDOWN = 2
        self.FONT_STYLE = "Press Start 2P"
        self.INISIAL_HOME_TEXT = "Sneck suffarie :0"
        
        self.FOOD_TYPE = self._player_acc_info["food_type"]
        self.INISISAL_HEART = self._player_acc_info["INISISAL_HEART"]
        self.SNAKE_TYPE = self._player_acc_info["sneck_type"]
        
        #this is bla bla
        self.HIGHT_SCORE = self._player_acc_info["HIGH_SCORE"]
        self.POINTES = self._player_acc_info["points"]
        self.ACCOUNT_NAME = self._player_acc_info["name"]
        
            
    def update_game_settings(self):
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
        # self._player_acc_info["sneck_owned_id"] = self.sneck_owned_id
        # self._player_acc_info["food_owned_id"] = self.food_owned_id
        
        with open("player_info\\demo_player.json", "w", encoding="utf-8") as player_file:
            json.dump(self._player_acc_info, player_file,)
        
    def update_password(self):
        # self._player_acc_info["password"] = password
        pass
        
    def updaing_casul_setting(self):
        pass
    
    def update(self):
        self.update_game_settings()
        self.updaing_casul_setting()



class Game_screen:
    """
    Class to manage the game screen, including navigation setup,
    game canvas setup, updating game elements, and adding/removing
    from the master widget.
    """
   
    def __init__(self,Master:Tk,var:variable):
        """Initialize the game screen.

        Args:
            Master (Tk): The parent Tkinter window.
            var (variable): An object containing game variables.
        """
   
        self.var = var
        self.MASTER = Master
        # self.FRAME = Frame(self.MASTER)
        
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
        
    
    def adjust_window_size(self):
        """
        Adjust the window size based on game and navigation heights.
        """
        nevigation_height = self.var.game_height // 8
        nevigation_height = nevigation_height // self.var.game_box_size
        
        if not nevigation_height:
            self._nevigation_height = self.var.game_box_size * nevigation_height
        else:
            self._nevigation_height = self.var.game_box_size
            
        self._game_bord_height = self.var.game_height - self._nevigation_height
    
    def nevigation_setup(self):
        """
        Setup the navigation canvas with heart, score text, and menu option.
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
    
    def game_canvas_setup(self):
        """
        Setup the game canvas with snake and food.
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
        # for key, value in kwargs.items():
    
    def add_to_Master(self)->None:
        """
        Pack the navigation and game canvases.
        """
        self.NEVIGATION_CANVAS.pack()
        self.GAME_CANVAS.pack()
        # self.FRAME.pack()

    def remove_to_Master(self)-> None:
        """remove from master"""
        self.NEVIGATION_CANVAS.pack_forget()
        self.GAME_CANVAS.pack_forget()
        # self.FRAME.pack_forget


class Game_engion:
    """
    This class serves the purpose of controlling the main game.

    Attributes:
    - MASTER (Tk): The master Tkinter window.
    - var (variable): An object containing variables/settings for the game.
    - SCORE (int): The player's score.
    - direction (str): The current direction of movement for the snake.
    - master_after_ids: The ID returned by `Tk.after()` method for controlling animation.
    - stop_game_animation (bool): Flag to control game animation.
    - _old_time_ (float): Timestamp for tracking time.
    - GAME_FRAME (Game_screen): Instance of the game screen.

    Methods:
    - __init__(Master: Tk, var: variable): Initializes the game engine.
    - _bild_key(): Binds keys for controlling the game.
    - _remove_bind_key(): Unbinds keys.
    - _change_direction(direction: str): Changes the direction of the snake.
    - _check_collision(sneckx, snecky): Checks for collisions with walls or itself.
    - _check_loss(): Checks if the game is lost.
    - PLAY_THE_GAME(): Main method to control the game flow.
    - PAUSE_GAME(event): Pauses the game.
    - RESTART_GAME(): Restarts the game.
    - ADD_TO_SCREEN(): Adds the game screen to the master window and binds keys.
    """
    
    def __init__(self,Master:Tk,var:variable):
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
        
    def _bild_key(self):
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
    
    def _remove_bind_key(self):
        '''remove the bind keys'''
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
        
    def _change_direction(self,direction):
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
    
    def _check_collision(self,sneckx,snecky):
        """
        Checks for collisions with walls or itself.

        Parameters:
        - sneckx (int): X-coordinate of the snake's head.
        - snecky (int): Y-coordinate of the snake's head.
        """
        if sneckx < 0 or sneckx >= self.var.game_width or \
            snecky < 0 or snecky >= self.GAME_FRAME._game_bord_height:
                self._check_loss()
        
        for i in range(1,len(self.GAME_FRAME.SNAKE.snake_coordinates)-1):
            x,y = self.GAME_FRAME.SNAKE.snake_coordinates[i]
            if sneckx == x and snecky == y:
                self._check_loss()
    
    def _check_loss(self):
        """
        Checks if the game is lost.
        """
        current_time = time.time()
        if not (current_time - self._old_time_ > self.var.SNAKE_LOSS_COUNTDOWN):
            return None
        
        if len(self.GAME_FRAME.HEART.hearts_list) > 1:
            self.GAME_FRAME.HEART.remmove_heart()
        else:
            self.GAME_FRAME.HEART.remmove_heart()
            self.UPDATION_AFTER_GAME_OVER()
        
        self._old_time_ = current_time      
    
    def PLAY_THE_GAME(self):
        """
        Controls the main gameplay loop.

        This method updates the snake's position, checks for collisions,
        updates the score, and schedules the next iteration of the game loop.

        If the game animation is stopped, it cancels the scheduled updates.

        Note:
        - This method is intended to be called recursively to create the game loop.

        """
        remove = True
        sneckx , snecky = self.GAME_FRAME.SNAKE.snake_coordinates[0]
        foodx , foody = self.GAME_FRAME.FOOD.x , self.GAME_FRAME.FOOD.y
        
        if self.direction == "up":
            snecky -= self.var.game_box_size
        elif self.direction == "down":
            snecky += self.var.game_box_size
        elif self.direction == "right":
            sneckx += self.var.game_box_size
        elif self.direction == "left":
            sneckx -= self.var.game_box_size
            
        if sneckx == foodx and snecky == foody:
            remove = False
            self.GAME_FRAME.FOOD.new_food("oval")#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! food styles modification
            self.SCORE +=1
        
        self.GAME_FRAME.SNAKE.move_snake(sneckx,snecky,remove)
        self.GAME_FRAME.update_things(score = self.SCORE)
        self._check_collision(sneckx,snecky)
        self.master_after_ids = self.MASTER.after(
            self.var.game_speed,
            self.PLAY_THE_GAME
            )
        
        if self.stop_game_animation:
            self.MASTER.after_cancel(self.master_after_ids)
            
    def UPDATION_AFTER_GAME_OVER(self):
        status = 'loss'
        
        if self.SCORE > self.var.HIGHT_SCORE:
            self.var.HIGHT_SCORE = self.SCORE
            status = 'high_score'
            
        # self.var.update()
        self.var.update_game_settings()
        self.PAUSE_GAME(status)
            
            
    def PAUSE_GAME(self,status):
        remove_resume = False
        if status == "pause":
            text = 'Game is Paused'
        if status == "loss":
            text = f'YOu lose :(  score: {self.SCORE}'
            remove_resume = True
        if status == "high_score":
            text = f'New High Score:0   {self.SCORE}'
            remove_resume = True
            
        self.GAME_FRAME.remove_to_Master()
        self._remove_bind_key()
        self.stop_game_animation = True
        
        if self.pause_screen:
            # becouse whicle creating pause screen we added text lable in index 0
            id = self.pause_screen.Windows_list[0]
            id.config(text=text)
            
            # self.pause_screen.start_animation()
            if remove_resume:
                # becouse whicle creating pause screen we added resume button in index 1
                resume = self.pause_screen.Windows_list[1]
                resume.config(state='disabled')
                
            self.pause_screen.add_to_master()
                
                
    
    def set_everrything_to_default(self):
        #[x]set stop_game_animation to false
        self.stop_game_animation = False
        #[x]score = 0
        self.SCORE = 0
        self.GAME_FRAME.update_things(score = self.SCORE)
        #[x]heart = 3
        self.GAME_FRAME.HEART.remove_all_heart()
        self.GAME_FRAME.HEART.add_heart_in_range()
        #[x]sneck_lenght = 3
        #[x]sneck_direction = "down"
        #[x]sneck_cordination_to_= (0,0)
        self.direction = "down"
        self.GAME_FRAME.SNAKE.get_to_inisial_posision()
        #[x]food_to_new_loaction = 0
        self.GAME_FRAME.FOOD.new_food()
        
        if self.pause_screen:
            resume = self.pause_screen.Windows_list[1]
            resume.config(state= 'normal')
    
    def ADD_TO_SCREEN(self):
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
    
    # Create and configure 'about me' button widget
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
    
    pause_game_screen.add_button(Label1,Button1,Button2,Button3)
    return pause_game_screen






def play_home():
    home_screen.remove_from_master()
    game.ADD_TO_SCREEN()
    game.PLAY_THE_GAME()
    print("hmm lets play")

def setting_home():
    print("hmmm u wanna change something")

def shop_home():
    print("what u wanna shop :0")
    
def about_me_home():
    print("hmmm u wanna know about me me crying :)")

def resume_pause_menu():
    pause_menu.remove_from_master()
    game.ADD_TO_SCREEN()
    game.PLAY_THE_GAME()
    print("wowow u clicked resume")

def restart_pause_menu():
    pause_menu.remove_from_master()
    game.set_everrything_to_default()
    game.ADD_TO_SCREEN()
    game.PLAY_THE_GAME()
    print("hmmm u wanna play again")

def home_pause_menu():
    pause_menu.remove_from_master()
    game.set_everrything_to_default()
    home_screen.add_to_master()
    home_screen.start_animation()
    print("hmm.... u wanna go home oki ! ")


#!!!!!!!!!!!!!!!!!!!!!!!!sneck_game!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# with open("settings.json","r",encoding="utf-8") as data:
#     vars = json.load(data)


def main(): 
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
    
    root.mainloop()
