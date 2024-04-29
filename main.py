from game_idles import Snake , Food , Heart
from game_screens import inisial_screens
from tkinter import Tk , Canvas , Button , Label
from random import choice , randint
import json
import time
#!!!!!!!!!!!!!!!!!!!!!!!!sneck_game!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class Game_screen:
    """
    Class representing the game screen.

    This class manages the game screen, including the main canvas for gameplay,
    the navigation canvas for displaying score and other information,
    and the game logic such as snake movement and collision detection.

    Attributes:
        MASTER (Tk): The Tkinter master window.
        GAME_WIDTH (int): The width of the game screen.
        GAME_HEIGHT (int): The height of the game screen.
        BOX_SIZE (int): The size of each box in the game.
        ... (add other attributes with descriptions)
    
    Methods:
        __init__: Initialize the game screen.
        Update_score: Update the displayed score on the navigation canvas.
        add_to_window: Add the navigation canvas and child window to the master window.
        check_loss: Check if the game is lost due to collision or other conditions.
        new_commad: Handle a new command event.
        stop_game_animation: Stop the game animation.
        resume_game_animation: Resume the game animation.
        _adjust_window_size: Adjust the size of the game window.
        __navigation_set_up: Set up the navigation section of the game screen.
        _bind_key: Bind keys to corresponding functions for controlling the game.
        _check_collision: Check for collision between snake and walls or itself.
        change_direction: Change the direction of the snake.
        START: Start the game.
    """
    def __init__(self,Master:Tk,Game_width,Game_height,box_size)->None:
        """
        Initialize the game screen.

        Args:
            Master (Tk): The Tkinter master window.
            Game_width (int): The width of the game screen.
            Game_height (int): The height of the game screen.
            box_size (int): The size of each box in the game.
        """
        self.MASTER=Master
        self.GAME_WIDTH = Game_width
        self.GAME_HEIGHT = Game_height
        self.BACKGROUND_COLOR = "#050B2B"
        self.BOX_SIZE = box_size
        
        # sneck and food variables
        self.DIRECTION_sneck = "down"
        self.Lenght_sneck = 3
        self.FOOD_COLOR = "red"
        self.COLOR_sneck = "yellow"
        self.SPEED_game = 120
        self.CORDINATERS_sneck =  (0,0)
        
        # nevigation and its variable
        self.NAVIGATION_COLOR = "black"
        self.NAVIGATION_text_color = "white"
        self.HEART_color = "red"
        self.INISITIAL_heart = 3
        
        #option_screens screen
        self.optionscreen = inisial_screens(self.MASTER,self.BACKGROUND_COLOR,self.GAME_WIDTH,self.BOX_SIZE,self.GAME_HEIGHT,self.SPEED_game,pack=False)
        # lable =Label(optionscreen.child_window,text="Paused",bg=BACKGROUND_COLOR,fg="White",font=("Press Start 2P",30),relief="flat")
        button =Button(self.optionscreen.child_window, text="Resume", command=self.resume,width=10,bg=BACKGROUND_COLOR,fg='white',font=("Press Start 2P",10),relief="flat")
        button1 =Button(self.optionscreen.child_window, text="Restart", command=self.restart,width=10,bg=BACKGROUND_COLOR,fg='white',font=("Press Start 2P",10),relief="flat")
        button2 =Button(self.optionscreen.child_window, text="Home", command=button_click,width=10,bg=BACKGROUND_COLOR,fg='white',font=("Press Start 2P",10),relief="flat")
        self.optionscreen.add_button(button,button1,button2)
        
        #game system variables
        self.remove = True
        self.SCORE = 0
        self.sneckx = 0
        self.snecky = 0
        self.count_down = time.time()
        self.stop_game_animation = False
        
        # Game  settings  and  adjustment
        self._adjust_winodw_size()
        self.__nevigation_set_up()
        self.CHILD_WINDOW = Canvas(self.MASTER,bg=self.BACKGROUND_COLOR,width=self.GAME_WIDTH,height=self.GAME_HEIGHT)
        self.SNECK = Snake(self.CHILD_WINDOW,self.Lenght_sneck,self.CORDINATERS_sneck, self.COLOR_sneck,self.BOX_SIZE)
        self.food = Food(self.CHILD_WINDOW, self.BOX_SIZE,self.FOOD_COLOR,self.GAME_WIDTH,self.GAME_HEIGHT,"oval")
        self._bind_key()
    
    def check_loss(self):
        """
        Check if the game is lost due to collision or other conditions.
        """
        current_time=time.time()
        if not (current_time - self.count_down > 2):
            return None
        
        if len(self.HEART.hearts_list)>1:
            self.HEART.remmove_heart()
        else:
            self.HEART.remmove_heart()
            self.stop_game_animation = True
            self.Pause_menu("event")
            print("you loss losser")
        
        self.count_down = current_time
    
    def restart(self):
        self.SCORE=0
        self.food.new_food("oval")
        
        self.SNECK.coordinates = (0,0)
        self.DIRECTION_sneck = "down"
        for body in self.SNECK.snake_body:
            self.SNECK.canvas.delete(body)
        self.SNECK._create_snake()
        for _ in range(len(self.HEART.hearts_list)):
            self.HEART.remmove_heart()
        for _ in range(self.HEART.inisial_heart):
            self.HEART.add_one_heart()
        
        self.resume()
    
    def Pause_menu (self,event):
        print("oye :0 oni chan")
        self.stop_game_animation = True
        self.CHILD_WINDOW.pack_forget()
        self.NEVIGATION_CANVAS.pack_forget()
        self.optionscreen.add_to_window()
        pass
    
    def resume(self):
        self.optionscreen.child_window.pack_forget()
        self.NEVIGATION_CANVAS.pack()
        self.CHILD_WINDOW.pack()
        self.resume_game_animation()
        
    def _adjust_winodw_size(self):
        """
        Adjust the size of the game window.
        """
        Nevigation_height = self.GAME_HEIGHT // 8
        Nevigation_height = Nevigation_height // self.BOX_SIZE
        if not Nevigation_height:
            self._Nevigation_height = self.BOX_SIZE
        else:
            self._Nevigation_height = self.BOX_SIZE * Nevigation_height  
        self.GAME_HEIGHT = self.GAME_HEIGHT - self._Nevigation_height
        
    def __nevigation_set_up(self):
        """
        Set up the navigation section of the game screen.
        """
        self.NEVIGATION_CANVAS = Canvas(self.MASTER,bg=self.NAVIGATION_COLOR,width=self.GAME_WIDTH,height=self._Nevigation_height)
        division4 = self._Nevigation_height // 4 
        heart_size = division4 * 3
        pady = division4 // 2
        self.HEART = Heart(self.NEVIGATION_CANVAS,(self.GAME_WIDTH-heart_size,pady),heart_size,self.HEART_color,self.INISITIAL_heart)
        self.SCORE_TEXT = self.NEVIGATION_CANVAS.create_text(self.GAME_WIDTH//2,division4*2,font=("Arial",division4*2,"bold"),text=f"Score: {self.SCORE}",fill=self.NAVIGATION_text_color)
        self.menu_option = self.NEVIGATION_CANVAS.create_text(30,division4*2,font=("Arial",division4*2,"bold"),text="Menu",fill=self.NAVIGATION_text_color)
        
    def _bind_key(self):
        """
        Bind keys to corresponding functions for controlling the game.
        """
        self.MASTER.bind('<Left>', lambda event: self.change_direction('left'))
        self.MASTER.bind('<Right>', lambda event: self.change_direction('right'))
        self.MASTER.bind('<Up>', lambda event: self.change_direction('up'))
        self.MASTER.bind('<Down>', lambda event: self.change_direction('down'))
        self.MASTER.bind('<a>', lambda event: self.change_direction('left'))
        self.MASTER.bind('<d>', lambda event: self.change_direction('right'))
        self.MASTER.bind('<w>', lambda event: self.change_direction('up'))
        self.MASTER.bind('<s>', lambda event: self.change_direction('down'))
        # stop and resume menu binding
        self.NEVIGATION_CANVAS.tag_bind(self.menu_option,"<Button-1>",self.Pause_menu)
        self.MASTER.bind("<p>",self.Pause_menu)
        self.CHILD_WINDOW.bind("<Button-1>",self.Pause_menu)
        
    
    def _check_collision(self):
        """
        Check for collision between snake and walls or itself.
        """
        if self.sneckx < 0 or self.sneckx >= self.GAME_WIDTH or self.snecky < 0 or self.snecky >= self.GAME_HEIGHT:
            self.check_loss()
            
        for i in range(1,len(self.SNECK.snake_coordinates)-1):
            x,y = self.SNECK.snake_coordinates[i]
            if self.sneckx == x and self.snecky == y:
                self.check_loss()
                
    def change_direction(self,direction):
        """
        Change the direction of the snake.

        Args:
            direction (str): The new direction ('up', 'down', 'left', or 'right').
        """
        if direction in ("down","up") and self.DIRECTION_sneck in ("down","up"):
            pass
        elif direction in ("right","left") and self.DIRECTION_sneck in ("right","left"):
            pass
        else: self.DIRECTION_sneck =direction
    
    def START(self):
        """
        Start the game.
        """
        self.remove = True
        self.sneckx,self.snecky = self.SNECK.snake_coordinates[0]
        self.foodx,self.foody = self.food.x,self.food.y
        
        if self.DIRECTION_sneck == "up":
            self.snecky -= self.BOX_SIZE
        elif self.DIRECTION_sneck == "down":
            self.snecky += self.BOX_SIZE
        elif self.DIRECTION_sneck == "right":
            self.sneckx += self.BOX_SIZE
        elif self.DIRECTION_sneck == "left":
            self.sneckx -= self.BOX_SIZE
            
        if self.sneckx == self.foodx and self.snecky == self.foody:
            self.remove = False
            self.food.new_food("oval")
            self.SCORE +=1
            
        self.Update_score()
        self.SNECK.move_snake(self.sneckx,self.snecky,self.remove)
        self._check_collision()
        self.master_after_ids = self.MASTER.after(self.SPEED_game,self.START)
        
        if self.stop_game_animation :
            self.MASTER.after_cancel(self.master_after_ids)
            
    def add_to_window(self):
        """
        Add the navigation canvas and child window to the master window.
        """
        self.NEVIGATION_CANVAS.pack()
        self.CHILD_WINDOW.pack()

    def resume_game_animation(self):
        """
        Resume the game animation.
        """
        self.stop_game_animation = False
        self.MASTER.after(self.SPEED_game,self.START)
    
    def Update_score(self):
        """
        Update the displayed score on the navigation canvas.
        """
        self.NEVIGATION_CANVAS.itemconfig(self.SCORE_TEXT , text=f"Score: {self.SCORE}")


#functiones !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def button_click():
    Home_window.stop_animation()
    Home_window.child_window.pack_forget()
    game_window.add_to_window()
    game_window.START()
    print("anything")


#snake game inisial_info: !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
with open("settings.json","r",encoding="utf-8")as data:
    game_info_json = json.load(data)

GAME_WIDTH = game_info_json["basic_info"]["game_width"]
GAME_HEIGHT = game_info_json["basic_info"]["game_height"]
BACKGROUND_COLOR = game_info_json["basic_info"]["background_color"]
NEVIGATION_COLOR = game_info_json["basic_info"]["nevigation_color"]
NEV_TEXT_COLOR = game_info_json["basic_info"]["nev_text_color"]
HOME_SCREEN_SPEED = game_info_json["basic_info"]["home_screen_speed"]
HOME_SCREEN_BOX_SIZE = game_info_json["basic_info"]["home_screen_box_size"]
GAME_BOX_SIZE = game_info_json["basic_info"]["game_box_size"]
GAME_SPPED = game_info_json["basic_info"]["game_speed"]

title = "sneck_game"

# making root_window !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
root = Tk()
root.geometry(f"{GAME_WIDTH}x{GAME_HEIGHT}")
root.title(title)


#home_screen_window !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Home_window = inisial_screens(root,BACKGROUND_COLOR,GAME_WIDTH,HOME_SCREEN_BOX_SIZE,GAME_HEIGHT,HOME_SCREEN_SPEED,True)
Home_window.add_snakes("red",(0,0),5,"down")
Home_window.add_snakes("yellow",(2,1),3,"down")
Home_window.add_snakes("pink",(4,2),8,"left")
Home_window.add_snakes("grey",(1,3),3,"right")
Home_window.add_snakes("blue",(4,4),4,"up")
Home_window.add_food("red","any",True)
Home_window.start_animation()

lable = Label(Home_window.child_window,text="Sneck suffarie :0",bg=BACKGROUND_COLOR,fg="White",font=("Press Start 2P",30),relief="flat")
button = Button(Home_window.child_window, text="Play", command=button_click,width=10,bg=BACKGROUND_COLOR,fg='white',font=("Press Start 2P",10),relief="groove")
button1 = Button(Home_window.child_window, text="Settings", command=button_click,width=10,bg=BACKGROUND_COLOR,fg='white',font=("Press Start 2P",10),relief="groove")
button2 = Button(Home_window.child_window, text="about me", command=button_click,width=10,bg=BACKGROUND_COLOR,fg='white',font=("Press Start 2P",10),relief="groove")
Home_window.add_button(lable,button,button1,button2)

#Game_window !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! level5
game_window = Game_screen(root,GAME_WIDTH,GAME_HEIGHT,GAME_BOX_SIZE)
game_window._bind_key()

root.update()
root.mainloop()