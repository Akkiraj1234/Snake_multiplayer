from tkinter import *
from main import variable
from main import Game_screen
import time

class option_menu:
    
    def __init__(self , master , var , height , width , color:str):
        '''
        inisalize a option menu for the game
        '''
        self.master = master
        self.var = var
        self.height = height
        self.width = width
        self.color = color
        
        self.nevigation_height = None
        self.main_window_height = None
        self.creating_window()
        
    def calculate_area(self):
        pass
    
    def creating_window(self):
        # self.nevigation_canvas
        self.main_canvas = Canvas(
            master = self.master,
            width = self.width-5,
            height = self.height,
            bg = self.color
        )

class setting_up_the_option_menu:
    #anything changes in code shoude be modified inside of the class
    
    def __init__(self,root:Tk , var:variable , nevigation_height:int , height = 0 , width = 0) -> None:
        self.root = root
        self.var = var
        
        self.background_bg = "#f0f0f0"
        self.button1_color = "#e6f2ff"
        self.button2_color = "#111111"
        self.width = width
        self.height = height
        self.nevigation_height = nevigation_height
        
        #inisalizing
        self._calculate_windows_size()
        self.inisalizing_window()

    def _calculate_windows_size(self):
        self.main_canvas_height =self.height - self.nevigation_height
        self.text_pady = 20
    
    def inisalizing_window(self):
        self.master = Frame(
            master = self.root,
            width = self.width,
            height = self.height,
            bg = self.background_bg
        )
        
        self.button1 = Canvas(
            master = self.master,
            width = (self.width // 2) - 5,
            height = self.nevigation_height,
            bg = self.button1_color,
        )
        
        self.button2 = Canvas(
            master = self.master,
            width = (self.width // 2) - 5,
            height = self.nevigation_height,
            bg = self.button2_color,
        )
        
        self.button1_text = self.button1.create_text(
            self.width //4 , self.text_pady,
            font = ("Arial",15,'bold'),
            text = "Game",
            fill = self.button2_color
        )
        
        self.button2_text = self.button2.create_text(
            self.width // 4 , self.text_pady,
            font = ("Arial",15,'bold'),
            text = "Account",
            fill = self.button1_color
        )
        self.setting_up_the_account_option()
    
    def setting_up_the_account_option(self):
        self.main_canvas = Frame(
            master = self.master,
            pady=5,
            padx=15,
            bd=1,
            relief="groove"
        )
        
        
        form_frame1 = Frame(self.main_canvas,relief="groove",bd=1,bg="pink",padx=15)
        form_frame1.grid(row=2,column=1,columnspan=1)
        
        #adding_form_frame1_widget(game_setting):-
        Label(self.main_canvas,font=("Arial",10,'bold'),relief="flat",text="Game basic setting",pady=5).grid(row=1,column=1)
        Label(form_frame1,font=("Arial",10,'bold'),relief="flat",text="game width :",pady=5,bg="pink").grid(row=0,column=0)
        Label(form_frame1,font=("Arial",10,'bold'),relief="flat",text="game height :",pady=5,bg="pink").grid(row=1,column=0)
        Label(form_frame1,font=("Arial",10,'bold'),relief="flat",text="Obj Size(home) :",pady=10,bg="pink").grid(row=2,column=0)
        Label(form_frame1,font=("Arial",10,'bold'),relief="flat",text="Speed (ms):",pady=5,bg="pink").grid(row=3,column=0)
        
        self.__Game_width_get = Entry(form_frame1,font=("Arial",10,'bold'),relief="flat",width=10,justify="center")
        self.__Game_width_get.grid(row=0,column=1)
        self.__Game_height_get = Entry(form_frame1,font=("Arial",10,'bold'),relief="flat",width=10,justify="center")
        self.__Game_height_get.grid(row=1,column=1)
        self.__box_size_get = Entry(form_frame1,font=("Arial",10,'bold'),relief="flat",width=10,justify="center")
        self.__box_size_get.grid(row=2,column=1)
        self.__speed_get = Entry(form_frame1,font=("Arial",10,'bold'),relief="flat",width=10,justify="center")
        self.__speed_get.grid(row=3,column=1)
        
        #adding_form_frame2_widget(account_setting):-
        Label(self.main_canvas,font=("Arial",10,'bold'),relief="flat",text="Account setting",pady=5).grid(row=3,column=1)
        form_frame2 = Frame(self.main_canvas,relief="groove",bd=1,bg="pink",pady=5,padx=15)
        form_frame2.grid(row=4,column=1,columnspan=1)
        
        self.__account_status_info_provide = Label(form_frame2,font=("Arial",5,"bold" ),relief="flat",text="*please add your account name if u wanna login in not found will create new_one*",bg="pink",wraplength=200)
        self.__account_status_info_provide.grid(row=0,column=0,columnspan=2)
        
        Label(form_frame2,font=("Arial",10,'bold'),relief="flat",text="Name :",padx=10,pady=5,bg="pink").grid(row=1,column=0)
        Label(form_frame2,font=("Arial",10,'bold'),relief="flat",text="game height :",padx=10,pady=5,bg="pink").grid(row=2,column=0)
        
        self.__account_name_get = Entry(form_frame2,font=("Arial",10,'bold'),relief="flat",width=10,justify="center")
        self.__account_name_get.grid(row=1,column=1)
        self.__account_pasowrd_get = Entry(form_frame2,font=("Arial",10,'bold'),relief="flat",width=10,justify="center")
        self.__account_pasowrd_get.grid(row=2,column=1)
        
        
        save_button = Button(self.main_canvas,activebackground="black",activeforeground="white",relief="flat",text="Save!",font=("Arial",10,'bold'),padx=10,pady=5,command=self.save_the_info)
        save_button.grid(row=5,column=1,sticky='ew')
        
        self.updating_account_info()
        
        # print(self.__Game_width_get.cget("text"))
        # Game_width_get.insert(0,"100")
        # Game_width_get1.insert(0,"200")
        
        
        # self.account_canvas = self.main_canvas
    
    def save_the_info(self):
        self.var.game_width = int(self.__Game_width_get.get())
        self.var.game_height = int(self.__Game_height_get.get())
        self.var.box_size = int(self.__box_size_get.get())
        self.var.speed = int(self.__speed_get.get())
        self.var._game_setting["game_info"]["Account"] = str(self.__account_name_get.get())
        self.var.update_user_settings()
        self.var.updaing_game_setting()
        
        
    def updating_account_info(self):
        self.__Game_width_get.insert(0,self.var.game_width)
        self.__Game_height_get.insert(0,self.var.game_height)
        self.__box_size_get.insert(0,self.var.box_size)
        self.__speed_get.insert(0,self.var.speed)
        self.__account_name_get.insert(0,self.var._game_setting["game_info"]["Account"])
        # self.__account_pasowrd_get.insert()
        
    
    def _packing_up_account_option(self):
        self.main_canvas.grid(sticky=NSEW,row=2,column=0,columnspan=2)
        
        
    def __shift_button_button1(self,event):
        self.button1.config(bg = self.button2_color)
        self.button2.config(bg = self.button1_color)
        self.button1.itemconfig(self.button1_text, fill= self.button1_color)
        self.button2.itemconfig(self.button1_text, fill= self.button2_color)
        
    def _shift_button_button2(self,event):
        self.button2.config(bg = self.button2_color)
        self.button1.config(bg = self.button1_color)
        self.button2.itemconfig(self.button1_text, fill= self.button1_color)
        self.button1.itemconfig(self.button1_text, fill= self.button2_color)
        
    def bind_key(self):
        self.__bind_keys_id = [
            self.button1.bind("<Button-1>",self._shift_button_button2),
            self.button2.bind("<Button-1>",self.__shift_button_button1)
        ]

    def remove_bind_key(self):
        self.button1.bind("<Button-1>",self.__bind_keys_id[0])
        self.button2.bind("<Button-1>",self.__bind_keys_id[1])
    
    def add_to_window(self):
        self.button1.grid(row=1,column=0)
        self.button2.grid(row=1,column=1)
        self.main_canvas.grid(row=2,column=0,columnspan=2)
        self.master.pack(side = "left", anchor = "nw")
        self.bind_key()
        
    def remove_to_window(self):
        self.button1.grid_forget()
        self.button2.grid_forget()
        self.main_canvas.grid_forget()
        self.master.pack_forget()
        self.remove_bind_key()
    
class setting_screen:
    
    def __init__(self, master:Tk, var:variable) -> None:
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
        self.root = master
        self.var = var
        self.master = Frame(self.root,height=self.var.game_height,width=self.var.game_width,border=0)
        self.master.config(highlightthickness=1,relief="flat")
        
        #inisalizing_varibales_requird_for_creating_screen
        self.game_screen_height = None
        self.game_screen_width = None
        self.settingscre_height = None
        self.settingscre_width = None
        self._calculate_screen_dimensions()
        
        #settingn up screens_for_the_game
        self.game_screen = Game_screen(self.master , self.var)
        self.game_screen.game_height = self.game_screen_height
        self.game_screen.game_width  = self.game_screen_width
        self.game_screen.set_up()
        self.possision_snack_and_idels()
        
        #setting_up_option_menu
        self.Nevigation_Menu = setting_up_the_option_menu(
            root = self.master,
            var = var,
            nevigation_height = self.game_screen._nevigation_height,
            width = self.settingscre_width,
            height = self.settingscre_height
        )
        
    def binding_keys(self):
        '''
        this method bind keys for the screen
        '''
        self.__get_idels_cordinates()
        self.__binding_keys_id = [
            self.game_screen.NEVIGATION_CANVAS.bind("<Button-1>",self._checkNavigationOption),
            self.game_screen.GAME_CANVAS.bind("<Button-1>",self._checkGamecanvasOption)
        ]
    
    def remove_binding_keys(self):
        self.game_screen.NEVIGATION_CANVAS.bind("<Button-1>",self.__binding_keys_id[0])
        self.game_screen.GAME_CANVAS.bind("<Button-1>",self.__binding_keys_id[1])
        
    def _checkNavigationOption(self , event) -> None:
        '''
        Check which navigation option is clicked based on the mouse event coordinates.

        This method checks if the mouse click event falls within the ranges of various navigation elements such as menu options and hearts. 
        If the click is within the range of a menu option or score text, it prints a message indicating the intent to change home and text color. 
        If the click is within the range of a heart, it prints a message indicating the intent to change heart color. 
        If the click is not within the range of any navigation elements, it prints a message indicating the intent to change navigation color.

        Parameters:
        - event: The mouse event containing the coordinates of the click.

        Returns:
        None
        '''
        if self.__check_cords_in_range(self._cordinates_home_and_score, (event.x , event.y)):
            print("you wanna change home and text color")
            
        elif self.__check_cords_in_range(self._hearts_cordinates, (event.x , event.y)):
            print("you wanna change heart color")
        
        else:
            print("you wanna change nevigation color oki")
            
    # def change_window(self,color):
    #     self.Nevigation_Menu.main_canvas.grid_forget()
    #     self.Nevigation_Menu.main_canvas = option_menu(self.Nevigation_Menu.master,self.var, self.game_screen._nevigation_height,self.settingscre_width,color).main_canvas
    #     self.Nevigation_Menu.main_canvas.grid(row=2,column=0,columnspan=2)
    #     self.Nevigation_Menu._shift_button_button2("j")
        
    def _checkGamecanvasOption(self , event) -> None:
        '''
        Check which game canvas option is clicked based on the mouse event coordinates.

        This method checks if the mouse click event falls within the ranges of various game canvas elements such as snake segments and food. 
        If the click is within the range of a snake segment, it prints a message indicating the intent to change snake appearance. 
        If the click is within the range of the food, it prints a message indicating the intent to change the food. 
        If the click is not within the range of any game canvas elements, it prints a message indicating the intent to change the food.

        Parameters:
        - event: The mouse event containing the coordinates of the click.

        Returns:
        None
        '''
        if self.__check_cords_in_range(self._cordinates_sneck , (event.x , event.y)):
            print("you wanna change sneck oki")
            
        elif self.__check_cords_in_range(self._cordinates_food, (event.x , event.y)):
            print("you wanna change the food")
        
        else:
            print("you wanna chnge canvas oki")
            
    def __check_cords_in_range(self, list_cords:list[tuple,tuple], coordinates:tuple[int,int]) -> bool:
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
        self._cordinates_home_and_score = [
            self.game_screen.NEVIGATION_CANVAS.bbox(self.game_screen.MENU_OPTION),
            self.game_screen.NEVIGATION_CANVAS.bbox(self.game_screen.SCORE_TEXT)
        ]
        
        self._hearts_cordinates = [
            self.game_screen.NEVIGATION_CANVAS.bbox(body)
            for heart in self.game_screen.HEART.hearts_list
            for body in heart
        ]

        self._cordinates_food = [
            self.game_screen.GAME_CANVAS.bbox(self.game_screen.FOOD.food)
        ]
        
        self._cordinates_sneck = [
            self.game_screen.GAME_CANVAS.bbox(snack)
            for snack in self.game_screen.SNAKE.snake_body
        ]
        
        
    def _calculate_screen_dimensions(self) -> None:
        '''
        Calculate the screen dimensions for the game and settings screen.

        This method calculates the height and width of both the game screen and the settings screen.
        The game screen height is set to the same value as the game height stored in the class variable.
        The settings screen height is also set to the game height.
        The game screen width is calculated as half of the game width plus one eighth of the game width.
        The settings screen width is calculated as the difference between the game width and the game screen width.

        Parameters:
            None

        Returns:
            None
        '''
        self.game_screen_height = self.var.game_height
        self.settingscre_height = self.var.game_height
        self.game_screen_width = (self.var.game_width // 2) + (self.var.game_width // 8)
        self.settingscre_width = self.var.game_width - self.game_screen_width
    
    def possision_snack_and_idels(self):
        '''
        possison the sneck and idels like food and heart and stuff
        and postion etc........
        '''
        self.game_screen.SNAKE.delete_all_snake()
        center_boarderx = self.game_screen_width // 2
        center_boardery = self.game_screen._game_bord_height // 2
        box_size = self.var.game_box_size
        
        self.game_screen.SNAKE.snake_coordinates = [(center_boarderx,center_boardery-box_size)]
        self.game_screen.SNAKE.snake_body = [self.game_screen.SNAKE._create_body(
            center_boarderx,center_boardery - box_size)
        ]
        
        x = center_boarderx
        for _ in range(4):
            x += box_size
            self.game_screen.SNAKE.move_snake(x-box_size ,center_boardery-box_size ,False)
        
        x = center_boarderx
        for _ in range(4):
            x -= box_size
            self.game_screen.SNAKE.move_snake(x+box_size ,center_boardery ,False)
            
    def ADD_TO_MASTER(self) -> None:
        '''
        add it to windoow
        '''
        self.master.pack()
        self.game_screen.add_to_Master()
        self.binding_keys()
        self.Nevigation_Menu.add_to_window()
    
    def REMOVE_FROM_MASTR(self) -> None:
        '''
        remove it from window
        '''
        pass







root = Tk()
var = variable()
root.geometry(f"{var.game_width+5}x{var.game_height+10}")
root.config(bg="black")

lol  = setting_screen(root,var)
lol.ADD_TO_MASTER()

root.mainloop()