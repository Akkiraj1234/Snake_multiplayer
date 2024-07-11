from variable import Variable
from game_screens import inisial_screens, Game_screen , WindowGenerator, setting_screen_gui
from tkinter import Tk,Frame,Button,Label,Canvas
from random import choice
import time


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
    
    def __init__(self, Master:Tk, var:Variable, pause_screen:inisial_screens) -> None:
        """
        Initializes the Game_engion object.

        Parameters:
        - Master (Tk): The master Tkinter window.
        - var (variable): An object containing variables/settings for the game.
        """
        self.MASTER = Master
        self.var = var
        self.GAME_FRAME = Game_screen(self.MASTER, self.var)
        self.pause_screen = pause_screen
        
        #varibales needed
        self.SCORE = 0
        self._old_time_ = 0
        self.direction = "down"
        self.master_after_ids = None
        self.stop_game_animation = False
        self.chance_of_drop = self.var.CHANCE_OF_DROP
        self.increase_speed_after = self.var.INCREASE_SPEED_AFTER
        self.game_speed =  self.var.game_speed
        
    def bild_key(self) -> None:
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
    
    def remove_bind_key(self) -> None:
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
        if len(self.GAME_FRAME.HEART_NEW.heart_list) > 1:
            self.GAME_FRAME.HEART_NEW.remove_one_heart()
        else:
            self.GAME_FRAME.HEART_NEW.remove_one_heart()
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
        snake_cords = self.GAME_FRAME.SNAKE.snake_coordinates
        
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
        if self.GAME_FRAME.FOOD.coords == (sneckx,snecky):
            remove = False
            self.GAME_FRAME.FOOD.new_food(snake_cords)
            self.SCORE +=1
        
        #checking if any 
        heart_avl = self.GAME_FRAME.HEART.avialable
        coin_avl  = self.GAME_FRAME.COIN.avialable
        
        if heart_avl or coin_avl:
            if heart_avl and self.GAME_FRAME.HEART.coords == (sneckx,snecky):
                self.GAME_FRAME.HEART.delete_all(hide=True)
                self.GAME_FRAME.HEART_NEW.add_one_heart()
                self.SCORE += 2
            if coin_avl and self.GAME_FRAME.COIN.coords == (sneckx,snecky):
                self.GAME_FRAME.COIN.delete_all(hide=True)
                self.var.PLAYERP_COINE += 10
                self.SCORE += 1
        else:
            # if they not exist creating new
            if self.SCORE and self.SCORE % self.chance_of_drop == 0:
                item = choice((self.GAME_FRAME.HEART.new_heart,self.GAME_FRAME.COIN.new_coin))
                item(snake_cords)
        
        #updaing things and collection after id
        self.GAME_FRAME.SNAKE.move_snake(sneckx,snecky,remove)
        self.GAME_FRAME.update_things(score = self.SCORE)
        self._check_collision(sneckx,snecky)
                
        #work on speed increcsing
        if self.SCORE and not self.SCORE % self.increase_speed_after:
            self.game_speed -= 10 
            self.SCORE += 1
            print(self.SCORE,"cool",self.game_speed)
            
        self.master_after_ids = self.MASTER.after(
            self.game_speed,
            self.PLAY_THE_GAME
            )
        
        #checking if game pause is called or not
        if self.stop_game_animation:
            self.MASTER.after_cancel(self.master_after_ids)
            
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
        
        if self.pause_screen: #if i inisalize the pause screen or its not None then
            #Windows_list[0] becouse while creating pause screen we added text lable in index 0
            id = self.pause_screen.Windows_list[0]
            id.config(text=text)
            self.pause_screen.update_nessassaery(update = True)
            
            if deacive_resume:
                #Windows_list[1] becouse while creating pause screen we added resume button in index 1
                resume = self.pause_screen.Windows_list[1]
                resume.config(state='disabled')
                
            self.pause_screen.add_to_master()
        
        #removeing canvas binded keys and stoping game animation
        self.GAME_FRAME.remove_to_Master()
        self.remove_bind_key()
        self.stop_game_animation = True
    
    def UPDATION_AFTER_GAME_OVER(self) -> None:
        """
        Handles post-game update actions.

        Updates the high score if the current score surpasses it,
        then triggers user settings update.

        Parameters:
        - status (str): Game outcome ('loss' or 'high_score').
        """
        self.set_everrything_to_default()
        status = 'loss'
        
        if self.SCORE > self.var.HIGHT_SCORE:
            self.var.HIGHT_SCORE = self.SCORE
            status = 'high_score'
            
        # self.var.update()
        self.var.update_user_settings()
        self.PAUSE_GAME(status)
    
    def update_everything(self):
        self.GAME_FRAME.update_everything()
        
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
        self.GAME_FRAME.HEART_NEW.delete_all()
        self.GAME_FRAME.HEART_NEW.add_heart_in_range(self.var.INISISAL_HEART)
        
        #removeing heart and coin
        self.GAME_FRAME.HEART.delete_all()
        self.GAME_FRAME.COIN.delete_all()
        
        #setting sneck lenght to inisial lenght and directiong to 
        #down and cordinates to (0,0) all done by the method get_to_inisial_posision
        self.direction = "down"
        self.GAME_FRAME.SNAKE.initial_posision()
        
        #food to new loaction
        self.GAME_FRAME.FOOD.new_food()
        
        if self.pause_screen:
            #if pause_screen inisalize then making resume button 
            # to normal again as an default
            resume = self.pause_screen.Windows_list[1]
            resume.config(state= 'normal')
        
        self.game_speed = self.var.game_speed       
            
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
        self.bild_key()
        self.stop_game_animation = False



class setting_screen:
    '''
    this classs help us inisalizing gui game screen 
    that can use to modify settings :0
    
    return:
        None
    '''
    def __init__(self , master:Tk , var:Variable, home_screen:inisial_screens ) -> None:
        '''
        Initialize the Game GUI.

        This method initializes the game GUI by creating the main frame, calculating screen dimensions,
        setting up screens for the game, and positioning the snake and other elements.

        Parameters:
        - master (Tk): The Tkinter root window.
        - var (variable): An instance of the variable class containing game variables.

        Returns:
        None
        '''
        #inisalizing frame and important variables
        self.master = master
        self.var = var
        self.home_screen = home_screen
        self.main_frame = Frame(master = self.master, relief="flat", bg="black")
        
        self.setting_screen = setting_screen_gui(self.main_frame, self.var)
        self.windows = WindowGenerator(root = self.master, var = var, setting_gui = self.setting_screen)
        
        self.set_up()
        
    def __check_cords_in_range(self, list_cords:list[tuple], coordinates:tuple[int]) -> bool:
        """
        Check if the given coordinates fall within any of the ranges specified in the list of coordinates.

        Parameters:
        - list_cords (list[tuple, tuple]): A list of tuples representing coordinate ranges. Each tuple contains
            four integers (x1, y1, x2, y2), defining a rectangular area.
        - coordinates (tuple[int, int]): A tuple representing the coordinates to be checked.

        Returns:
        - bool: True if the coordinates fall within any of the specified ranges, False otherwise.
        """
        x , y = coordinates
        for group in list_cords:
            x1 , y1 , x2 , y2 = group
            if x1 < x < x2 and y1 < y < y2:
                return True
        return False
    
    def __get_idels_cordinates(self) -> None:
        '''
        Get the coordinates of various elements on the game screen.

        This method retrieves the coordinates of different elements on the game screen, such as menu options, score text, hearts, food, and snake body segments.

        Returns:
        - None
        '''
        nevigation_canvas = self.setting_screen.GAME_SCREEN.NEVIGATION_CANVAS
        game_canvas = self.setting_screen.GAME_SCREEN.GAME_CANVAS
        self._cordinates_home_and_score = [
            nevigation_canvas.bbox(self.setting_screen.GAME_SCREEN.MENU_OPTION),
            nevigation_canvas.bbox(self.setting_screen.GAME_SCREEN.SCORE_TEXT)
        ]
        
        self._hearts_cordinates = [
            nevigation_canvas.bbox(body)
            for heart in self.setting_screen.GAME_SCREEN.HEART_NEW.heart_list
            for body in heart
        ]
        
        self._cordinates_food = [
            game_canvas.bbox(self.setting_screen.GAME_SCREEN.FOOD.food)
        ]
        
        self._cordinates_sneck = [
            game_canvas.bbox(snack)
            for snack in self.setting_screen.GAME_SCREEN.SNAKE.snake_body
        ]
        
        self._cordinates_canvas_heart = [
            game_canvas.bbox(heart)
            for heart in self.setting_screen.GAME_SCREEN.HEART.hearts
        ]
        
        self._cordinates_coin = [
            game_canvas.bbox(coin)
            for coin in self.setting_screen.GAME_SCREEN.COIN.coins
        ]

    def __shift_button_button1(self, event) -> None:
        """
        Handle the event when navigation button 1 is clicked.

        This method updates the background colors and text colors of two navigation buttons to reflect
        the active state of button 1. It also switches the visible screen by hiding the basic setting 
        and account setting screens, and displaying the current screen.

        Args:
            event: The event that triggered this method.
        """
        self.setting_screen.nevigation_button1.config(bg = self.var.theme1)
        self.setting_screen.nevigation_button1.itemconfig(self.setting_screen._text_nev_button_id[0], fill = self.var.theme2)
        self.setting_screen.nevigation_button2.config(bg = self.var.theme2)
        self.setting_screen.nevigation_button2.itemconfig(self.setting_screen._text_nev_button_id[1], fill = self.var.theme1)
    
    def __shift_button_button2(self, event) -> None:
        """
        Handle the event when navigation button 2 is clicked.

        This method updates the background colors and text colors of two navigation buttons to reflect
        the active state of button 2. It also switches the visible screen by hiding the current screen 
        and account setting screens, and displaying the basic setting screen.

        Args:
            event: The event that triggered this method.
        """
        self.setting_screen.nevigation_button1.config(bg = self.var.theme2)
        self.setting_screen.nevigation_button1.itemconfig(self.setting_screen._text_nev_button_id[0], fill = self.var.theme1)
        self.setting_screen.nevigation_button2.config(bg = self.var.theme1)
        self.setting_screen.nevigation_button2.itemconfig(self.setting_screen._text_nev_button_id[1], fill = self.var.theme2)   
    
    def __save_button_method(self, event) -> None:
        print(event.x)
    
    def __back_button_method(self, event) -> None:
        self.REMOVE_TO_MASTER()
        self.home_screen.add_to_master()
        self.home_screen.start_animation(self.var.home_speed)
        self.home_screen.update_nessassaery(update=True)
    
    def _check_bind_event_on_game_screen(self, event , screen:int) -> None:
        """Check and handle events based on the current game screen and event coordinates.

        Args:
            event: The event object containing information about the event.
            screen (int): The current game screen (1 or 2).

        Prints:
            A message indicating the type of action based on the event coordinates and the game screen.
        """
        if screen == 1:
            if self.__check_cords_in_range(self._cordinates_home_and_score, (event.x, event.y)):
                # window = self.windows.Inisial_screen(self.setting_screen_frame,"text1")
                print("you touched text")
                
            elif self.__check_cords_in_range(self._hearts_cordinates, (event.x, event.y)):
                # window = self.windows.Inisial_screen(self.setting_screen_frame,"text2")
                print("you rouched heart")
                
            else:
                # window = self.windows.Inisial_screen(self.setting_screen_frame,"text3")
                print("you touched background")
                
        elif screen == 2:
            if self.__check_cords_in_range(self._cordinates_sneck, (event.x, event.y)):
                # window = self.windows.Inisial_screen(self.setting_screen_frame,"text4")
                print("woops you touched snake")
                
            elif self.__check_cords_in_range(self._cordinates_food, (event.x, event.y)):
                # window = self.windows.Inisial_screen(self.setting_screen_frame,"text5")
                print("you touched food")
                
            elif self.__check_cords_in_range(self._cordinates_coin, (event.x , event.y)):
                # window = self.windows.Inisial_screen(self.setting_screen_frame,"coin window")
                print("you touched coin")
            
            elif self.__check_cords_in_range(self._cordinates_canvas_heart, (event.x , event.y)):
                # window = self.windows.Inisial_screen(self.setting_screen_frame,"heart window")
                print("you touched another heart")
                
            else:
                # window = self.windows.Inisial_screen(self.setting_screen_frame,"text6")
                print("you touched background")
     
    def set_up(self):
        self.setting_screen._something()
        self.__get_idels_cordinates()
    
    def bind_keys(self) -> None:
        self._bind_keys_id = [
            self.setting_screen.back_button.bind("<Button-1>",self.__back_button_method),
            self.setting_screen.save_button.bind("<Button-1>",self.__save_button_method),
            
            self.setting_screen.GAME_SCREEN.NEVIGATION_CANVAS.bind(
                "<Button-1>", lambda event: self._check_bind_event_on_game_screen(event, 1)
            ),
            self.setting_screen.GAME_SCREEN.GAME_CANVAS.bind(
                "<Button-1>", lambda event: self._check_bind_event_on_game_screen(event , 2)
            ),
            
            self.setting_screen.nevigation_button1.bind("<Button-1>",self.__shift_button_button1),
            self.setting_screen.nevigation_button2.bind("<Button-1>",self.__shift_button_button2)
        ]
    
    def remove_bind_keys(self) -> None:
        '''
        this method removes binds keys for the screen
        '''
        self.setting_screen.back_button.unbind("<Button-1>", self._bind_keys_id[0])
        self.setting_screen.save_button.unbind("<Button-1>", self._bind_keys_id[1])
        self.setting_screen.GAME_SCREEN.NEVIGATION_CANVAS.unbind("<Button-1>",self._bind_keys_id[2])
        self.setting_screen.GAME_SCREEN.GAME_CANVAS.unbind("<Button-1>",self._bind_keys_id[3])
        self.setting_screen.nevigation_button1.unbind("<Button-1>", self._bind_keys_id[4])
        self.setting_screen.nevigation_button2.unbind("<Button-1>", self._bind_keys_id[5])
    
    def ADD_TO_MASTER(self) -> None:
        '''
        add the setting screen to master
        '''
        self.main_frame.grid()
        self.bind_keys()
        # self.gane_screen_frame.grid(row = 0,column=0)
        # self.setting_screen_frame.grid(row = 0,column = 1)
        
        # self.game_screen.add_to_Master()
        # self.back_button.pack()
        # self.window_screen.PACK_CURRENT_SCREEN()
        # self.binding_keys()
    
    def REMOVE_TO_MASTER(self):
        '''
        remove the setting screen from the master
        '''
        self.setting_screen._remove()
        self.remove_bind_keys()
        self.main_frame.grid_forget()
        print(root.children.values())
        
        # self.remove_binding_keys()
        # self.game_screen.remove_to_Master()
        # self.window_screen.REMOVE_CURRENT_SCREEN()
        # self.gane_screen_frame.grid_forget()
        # self.back_button.pack_forget()
        # self.setting_screen_frame.grid_forget()



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
    print(root.children.values())

def shop_home():
    """
    Display shopping options.

    Behavior:
    - Prints a message indicating the user's intent to access shopping.
    """
    home_screen.remove_from_master()
    shop.ADD_TO_MASTER()
    print(root.children.values())
    
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

def restart_pause_menu():
    """
    Restart the game from the pause menu.

    Behavior:
    - Removes the pause menu from the master window.
    - Resets game settings to default and starts the game.
    - Prints a message indicating the action taken.
    """
    game.set_everrything_to_default()
    pause_menu.remove_from_master()
    game.ADD_TO_SCREEN()
    game.PLAY_THE_GAME()

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
    home_screen.start_animation(var.game_speed)
    home_screen.update_nessassaery(update=True)

def update_everything():
    pause_menu.update_everything()
    home_screen.update_everything()
    game.update_everything()

def home_screen_inisalization(Master:Tk, var:Variable) -> inisial_screens:
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
        background_color = var.CANVAS_COLOR,
        game_width = var.game_width,
        game_height = var.game_height,
        box_size = var.home_boxsize
        )
    
    # Add snakes and food to the home screen
    Home_window.add_snakes("red", [0,0], 5, "down")
    Home_window.add_snakes("pink", [8,4], 8, "left")
    Home_window.add_snakes("grey", [9,3], 3, "right")
    Home_window.add_snakes("blue", [10,4], 4, "up")
    Home_window.add_snakes("yellow", [6,1], 3, "down")
    Home_window.add_food("red", True)
    Home_window.add_heart("red", False)
    Home_window.add_coin("#ffff00",False)
    #adding header and footer
    Home_window.HomeScreen_HeaderFooter_modle1_inisalization(var = var)
    
    
    # Create and configure label widget
    lable = Label(
        master = Home_window.child_window,
        text = var.INISIAL_HOME_TEXT,
        bg = var.CANVAS_COLOR,
        fg = var.TEXT_COLOR,
        font = (var.FONT_STYLE,30),
        relief = "flat"
        )
    
    # Create and configure 'Play' button widget
    button = Button(
        master = Home_window.child_window,
        text = "Play",
        command = play_home,
        width = 10,
        bg = var.CANVAS_COLOR,
        fg = var.TEXT_COLOR,
        font = (var.FONT_STYLE,10),
        relief="groove"
        )
    
    # Create and configure 'Settings' button widget
    button1 = Button(
        Home_window.child_window,
        text = "Shop",
        command = shop_home,
        width = 10,
        bg = var.CANVAS_COLOR,
        fg = var.TEXT_COLOR,
        font = (var.FONT_STYLE,10),
        relief = "groove"
        )
    
    # Create and configure 'about me' button widget
    button2 = Button(
        master = Home_window.child_window,
        text = "about me",
        command = about_me_home,
        width = 10,
        bg = var.CANVAS_COLOR,
        fg = var.TEXT_COLOR,
        font = (var.FONT_STYLE,10),
        relief = "groove"
        )
    
    # adding buttons to the home_window canvas and then
    # returning the instance of the home_window
    Home_window.add_windows(lable, button, button1, button2, middle=1)
    return Home_window

def pause_menu_initialization(master:Tk, var:Variable) -> inisial_screens:
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
        background_color = var.CANVAS_COLOR,
        game_width = var.game_width,
        game_height = var.game_height,
        box_size = var.home_boxsize,
        pack = False
    )
    # adding buttones
    
    Label1 = Label(
        master = pause_game_screen.child_window,
        text = "Game is Paused",
        bg = var.CANVAS_COLOR,
        fg = var.TEXT_COLOR,
        font = (var.FONT_STYLE,15),
        relief = "flat"
    )
    Button1 = Button(
        master = pause_game_screen.child_window,
        text = "Resume",
        command = resume_pause_menu,
        width = 10,
        bg = var.CANVAS_COLOR,
        fg = var.TEXT_COLOR,
        font = (var.FONT_STYLE, 10),
        relief = "groove"
    )
    
    Button2 = Button(
        master = pause_game_screen.child_window,
        text = "Restart",
        command = restart_pause_menu,
        width = 10,
        bg = var.CANVAS_COLOR,
        fg = var.TEXT_COLOR,
        font = (var.FONT_STYLE, 10),
        relief = "groove"
    )
    
    Button3 = Button(
        master = pause_game_screen.child_window,
        text = "Home",
        command = home_pause_menu,
        width = 10,
        bg = var.CANVAS_COLOR,
        fg = var.TEXT_COLOR,
        font = (var.FONT_STYLE, 10),
        relief = "groove"
    )
    
    #adding button to pause_game_screen and returning its instanse
    pause_game_screen.add_windows(Label1,Button1,Button2,Button3)
    pause_game_screen.HomeScreen_HeaderFooter_modle1_inisalization(var = var)
    return pause_game_screen


def main(): 
    """
    Main function to initialize the game application.

    Behavior:
    - Sets the geometry and title of the root window.
    - Assigns the pause menu to the game object.
    - Starts the animation of the home screen.
    """
    root.geometry(f"{var.game_width+5}x{var.game_height+5}")
    # root.resizable(width=False,height=False)
    root.title(var.INISIAL_HOME_TEXT)
    home_screen.start_animation(var.game_speed)
    


if __name__ == "__main__":
    root = Tk()
    var = Variable()
    
    home_screen = home_screen_inisalization(root, var)
    pause_menu = pause_menu_initialization(root, var)
    game = Game_engion(Master=root, var=var, pause_screen=pause_menu)
    shop = setting_screen(root , var, home_screen = home_screen)
    
    main()
    print(root.children.values())
    root.update()
    root.mainloop()
    
        
        
        