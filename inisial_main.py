from game_idles import Snake,Food,Heart
from game_screens import inisial_screens
from tkinter import Tk,Canvas,Button,Label,Frame
from random import choice , randint
import json
import time


class variable:
    """Class to store game-related variables."""
    
    def __init__(self):
        """Initialize game variables."""
        self.background_color = "#050B2B"
        self.font_color = "white"
        self.game_width = 740
        self.game_height = 360
        self.box_size = 40
        self.speed =120
        
        self.game_box_size = 30
        self.game_speed = 120
        self.snake_color = "yellow"
        self.food_color = "red"
        
        self.nevigation_color = "black"
        self.nevigation_text_color = "white"
        self.heart_color = "red"
        
        #fixed values :0
        self.SNAKE_LENGHT = 3
        self.SNAKE_CORDINATES = (0,0)
        self.SNAKE_LOSS_COUNTDOWN = 2
        self.FOOD_TYPE = "oval"
        self.INISISAL_HEART = 3
        self.FONT_STYLE = "Press Start 2P"
        self.INISIAL_HOME_TEXT = "Sneck suffarie :0"
        
        


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
        self.FRAME = Frame(self.MASTER)
        
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
            master = self.FRAME,
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
            master = self.FRAME,
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
        self.FRAME.pack()

    def remove_to_Master(self)-> None:
        """remove from master"""
        self.NEVIGATION_CANVAS.pack_forget()
        self.GAME_CANVAS.pack_forget()
        self.FRAME.pack_forget


class Game_engion:
    "this class server purpose of controlling the main_game :0"
    
    def __init__(self,Master:Tk,var:variable):
        
        self.MASTER = Master
        self.var = var
        
        #varibales needed
        self.SCORE = 0
        self.direction = "down"
        self.master_after_ids = None
        self.stop_game_animation = False
        self._old_time_ = time.time()
        
        #creating screen
        self.GAME_FRAME = Game_screen(self.MASTER,self.var)
        
    def _bild_key(self):
        '''
        binding keys for the main game 
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
        self.MASTER.bind("<p>",self.PAUSE_GAME),
        
        #binding home button for paush menu
        self.GAME_FRAME.GAME_CANVAS.bind("<Button-1>",self.PAUSE_GAME),
        
        #binding right click on canvas for stoping the game
        self.GAME_FRAME.NEVIGATION_CANVAS.tag_bind(self.GAME_FRAME.MENU_OPTION,"<Button-1>",self.PAUSE_GAME),
        ]
    
    def _remove_bind_key(self):
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
        print('llolll :)')
        if direction in ("down","up") and self.direction in ("down","up"):
            pass
        elif direction in ("right","left") and self.direction in ("right","left"):
            pass
        else: self.direction = direction
    
    def _check_collision(self,sneckx,snecky):
        if sneckx < 0 or sneckx >= self.var.game_width or snecky < 0 or snecky >= self.GAME_FRAME._game_bord_height:
            self._check_loss()
        
        for i in range(1,len(self.GAME_FRAME.SNAKE.snake_coordinates)-1):
            x,y = self.GAME_FRAME.SNAKE.snake_coordinates[i]
            if sneckx == x and snecky == y:
                self._check_loss()
    
    def _check_loss(self):
        current_time = time.time()
        if not (current_time - self._old_time_ > self.var.SNAKE_LOSS_COUNTDOWN):
            return None
        
        if len(self.GAME_FRAME.HEART.hearts_list) > 1:
            self.GAME_FRAME.HEART.remmove_heart()
        else:
            self.GAME_FRAME.HEART.remmove_heart()
            self.PAUSE_GAME("event")
        
        self._old_time_ = current_time      
    
    def PLAY_THE_GAME(self):
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
            
    def PAUSE_GAME(self,event):
        self.REMOVE_FROM_SCREEN()
    
    def RESTART_GAME(self):
        pass  
    
    def ADD_TO_SCREEN(self):
        self.GAME_FRAME.add_to_Master()
        self._bild_key()
        self.stop_game_animation = False
    
    def REMOVE_FROM_SCREEN(self):
        self.GAME_FRAME.remove_to_Master()
        self._remove_bind_key()
        self.stop_game_animation = True
    
    

def home_screen_inisalization(Master,var:variable) -> inisial_screens:
    Home_window = inisial_screens(
        master = Master,
        background_color = var.background_color,
        game_width = var.game_width,
        box_size = var.box_size,
        game_height = var.game_height,
        speed = var.speed,
        pack = True
        )
    
    Home_window.add_snakes("red", (0,0), 5, "down")
    Home_window.add_snakes("pink", (4,2), 8, "left")
    Home_window.add_snakes("grey", (1,3), 3, "right")
    Home_window.add_snakes("blue", (4,4), 4, "up")
    Home_window.add_snakes("yellow", (2,1), 3, "down")
    Home_window.add_food("red", "any", True)
    
    lable = Label(
        master = Home_window.child_window,
        text = var.INISIAL_HOME_TEXT,
        bg = var.background_color,
        fg = var.font_color,
        font = (var.FONT_STYLE,30),
        relief = "flat"
        )
    
    button = Button(
        master = Home_window.child_window,
        text = "Play",
        command = button_click,
        width = 10,
        bg = var.background_color,
        fg = var.font_color,
        font = (var.FONT_STYLE,10),
        relief="groove"
        )
    
    button1 = Button(
        Home_window.child_window,
        text = "Settings",
        command = button_click,
        width = 10,
        bg = var.background_color,
        fg = var.font_color,
        font = (var.FONT_STYLE,10),
        relief = "groove"
        )
    
    button2 = Button(
        master = Home_window.child_window,
        text = "about me",
        command = button_click,
        width = 10,
        bg = var.background_color,
        fg = var.font_color,
        font = (var.FONT_STYLE,10),
        relief = "groove"
        )
    
    Home_window.add_button(lable, button, button1, button2)
    return Home_window
        
    




#!!!!!!!!!!!!!!!!!!!!!!!!sneck_game!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# with open("settings.json","r",encoding="utf-8") as data:
#     vars = json.load(data)
    
def button_click():
    print("wow u did something :0")
    home_screen.remove_from_master()
    game.ADD_TO_SCREEN()
    game.PLAY_THE_GAME()
    

def main(): 
    root.geometry(f"{var.game_width}x{var.game_height}")
    root.title("title")
    

if __name__ == "__main__":
    root = Tk()
    var = variable()
    
    home_screen = home_screen_inisalization(root, var)
    home_screen.start_animation()
    
    game = Game_engion(
        Master=root, 
        var=var
        )
    main()
    
    root.mainloop()
