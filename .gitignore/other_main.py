from tkinter import * 
from main import Variable
from main import Game_screen
from tkinter import messagebox
from game_screens import WindowGenerator

        
class setting_option_menu:
    '''
    this class will inisalize option menu for the setting where they can change settings
    '''
    
    def __init__(self,master:Frame,var:Variable,canvas_height:int, canvas_width:int, nevigation_height:int, button_height:int) -> None:
        self._master = master
        self.var = var
        self._canvas_height = canvas_height
        self._canvas_width  = canvas_width
        self._nevigation_height  = nevigation_height
        self._game_button_height = button_height
        
        self.height_main_canvs = (self._canvas_height - self._nevigation_height) - self._game_button_height
        self.width_main_canvs  = self._canvas_width - 14
        
        self.curent_screen = None
        
        #creating_instance
        self.windows = WindowGenerator(
            root = root,
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
    
    

class setting_screen:
    '''
    this classs help us inisalizing gui game screen 
    that can use to modify code
    
    return:
        None
    '''
    def __init__(self , master:Tk , var:Variable ) -> None:
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
        #creating frames
        self.child_frame = Frame(master= self.master, relief= "flat", bg= "black")
        self.gane_screen_frame = Frame(self.child_frame)
        self.setting_screen_frame = Frame(self.child_frame)
        
        #setting up screen for the game and resulatiion
        self._gameexit_button_height = None
        self._game_screen_height = None
        self._game_screen_width = None
        self._settingscreen_height = None
        self._settingscreen_width = None
        self._calculate_screen_dimensions()
        
        #setting up screens for the game
        self.game_screen = Game_screen(Master=self.gane_screen_frame, var=self.var)
        self.game_screen.game_height = self._game_screen_height
        self.game_screen.game_width = self._game_screen_width
        self.game_screen.set_up()
        self.possision_snack_and_idels()
        self._add_back_button()

        #adding setting screen for the game
        self.window_screen = setting_option_menu(
            master = self.setting_screen_frame,
            var = var,
            canvas_height = self._settingscreen_height,
            canvas_width = self._settingscreen_width,
            nevigation_height = self.game_screen._nevigation_height,
            button_height = self._gameexit_button_height
        )
        
        self.windows = self.window_screen.windows
        #adding inisial shop screen
        self.window_screen.curent_screen = self.windows.Inisial_screen(self.setting_screen_frame,"please click on anything in game canvas to start with")
        
    def _add_back_button(self) -> None:
        '''
        set up the back button for the game
        '''
        #add back button for the game 
        self.back_button = Canvas(
            master = self.gane_screen_frame,
            height = self._gameexit_button_height,
            width = self._game_screen_width,
            bg = self.var.theme2
        )
        
        self.back_button_text_id = self.back_button.create_text(
            self._game_screen_width // 2,self._gameexit_button_height // 2,
            font = ("Arial",self.var.home_text_size,'bold'),
            text = "Back",
            fill = self.var.theme1
        )
        
    def back_button_func(self,event) -> None:
        '''
        the function for going back the function
        '''
        print("hola amigos")
        self.back_button.config(bg = self.var.theme1)
        self.back_button.itemconfig(self.back_button_text_id, fill = self.var.theme2)
        self.REMOVE_TO_MASTER()
        
    def binding_keys(self) -> None:
        '''
        this method bind keys for the screen
        '''
        self.__get_idels_cordinates()
        self.__binding_keys_id = [
            self.game_screen.NEVIGATION_CANVAS.bind(
                "<Button-1>",lambda event: self._check_bind_event_on_game_screen(event , 1)
                ),
            self.game_screen.GAME_CANVAS.bind(
                "<Button-1>",lambda event: self._check_bind_event_on_game_screen(event , 2)
                )
        ]
        self.back_button.bind("<Button-1>",self.back_button_func)
    
    def remove_binding_keys(self) -> None:
        '''
        this method removes binds keys for the screen
        '''
        self.game_screen.NEVIGATION_CANVAS.unbind("<Button-1>",self.__binding_keys_id[0])
        self.game_screen.GAME_CANVAS.unbind("<Button-1>",self.__binding_keys_id[1])
        self.back_button.unbind_all("<Button-1>")
    
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
        
    def _check_bind_event_on_game_screen(self, event , screen:int) -> None:#fix things here too !!!!!!!!!!!!!!!!!!!!!!
        """Check and handle events based on the current game screen and event coordinates.

        Args:
            event: The event object containing information about the event.
            screen (int): The current game screen (1 or 2).

        Prints:
            A message indicating the type of action based on the event coordinates and the game screen.
        """
        if screen == 1:
            if self.__check_cords_in_range(self._cordinates_home_and_score, (event.x, event.y)):
                window = self.windows.Inisial_screen(self.setting_screen_frame,"text1")
                
            elif self.__check_cords_in_range(self._hearts_cordinates, (event.x, event.y)):
                window = self.windows.Inisial_screen(self.setting_screen_frame,"text2")
                
            else:
                window = self.windows.Inisial_screen(self.setting_screen_frame,"text3")
                
        elif screen == 2:
            if self.__check_cords_in_range(self._cordinates_sneck, (event.x, event.y)):
                window = self.windows.Inisial_screen(self.setting_screen_frame,"text4")
                
            elif self.__check_cords_in_range(self._cordinates_food, (event.x, event.y)):
                window = self.windows.Inisial_screen(self.setting_screen_frame,"text5")
                
            else:
                window = self.windows.Inisial_screen(self.setting_screen_frame,"text6")
        
        #setting up the window acording to window they selected
        self.window_screen.change_screen(window)
                
    
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
    
    def _calculate_screen_dimensions(self) -> None:#FIX IT THE EXIT BUTTON HEIGHT
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
        self._gameexit_button_height = 30
        self._game_screen_height = self.var.game_height - self._gameexit_button_height - 14
        self._settingscreen_height = self.var.game_height -14
        self._game_screen_width = (self.var.game_width // 2) + (self.var.game_width // 8)
        self._settingscreen_width = self.var.game_width - self._game_screen_width
    
    def possision_snack_and_idels(self) -> None:
        '''
        possison the sneck and idels like food and heart and stuff
        and postion etc........
        '''
        self.game_screen.SNAKE.delete_all_snake()
        center_borderx = self._game_screen_width // 2
        center_bordery = self.game_screen._game_bord_height // 2
        box_size = self.var.game_box_size
        
        self.game_screen.SNAKE.snake_coordinates = [(center_borderx,center_bordery-box_size)]
        self.game_screen.SNAKE.snake_body = [self.game_screen.SNAKE._create_body(
            center_borderx,center_bordery - box_size)
        ]
        # adding snacke body to left
        x = center_borderx
        for _ in range(4):
            x += box_size
            self.game_screen.SNAKE.move_snake(x - box_size , center_bordery - box_size,False)
        
        #adding snacke body to right
        x = center_borderx
        for _ in range(4):
            x -= box_size
            self.game_screen.SNAKE.move_snake(x+box_size , center_bordery,False)

        #adding food:
        snake_cords = self.game_screen.SNAKE.snake_coordinates
        self.game_screen.FOOD.new_food(cordinates = snake_cords)
        
    def ADD_TO_MASTER(self) -> None:
        '''
        add the setting screen to master
        '''
        self.child_frame.grid()
        self.gane_screen_frame.grid(row = 0,column=0)
        self.setting_screen_frame.grid(row = 0,column = 1)
        
        self.game_screen.add_to_Master()
        self.back_button.pack()
        self.window_screen.PACK_CURRENT_SCREEN()
        self.binding_keys()
    
    def REMOVE_TO_MASTER(self):
        '''
        remove the setting screen from the master
        '''
        self.remove_binding_keys()
        self.game_screen.remove_to_Master()
        self.window_screen.REMOVE_CURRENT_SCREEN()
        self.gane_screen_frame.grid_forget()
        self.setting_screen_frame.grid_forget()
        self.child_frame.grid_forget()




root = Tk()
var = Variable()
root.geometry(f"{var.game_width}x{var.game_height}")
# root.config(bg = "black")

setting = setting_screen(root , var)
setting.ADD_TO_MASTER()

root.mainloop()


# def _get_coords(self) -> None:
#         """
#         The way its contains coordinates are :
#         _button_coords = index-[0,1,2,3,4,5,6,7,8,9]
#         From 0 to 5 its shop canvas button coordinates.
#         From 6 to 9 its conatins coordinates in this squence:
#         upgradable_id[1](button), footer_shape_id[0-2](back,save,next)
#         """
#         self._button_coords = [
#             self.main_canvas.bbox(self.shop_button_id[num]) for num in range(6)
#         ]
#         self._button_coords.append(
#             self.main_canvas.bbox(self.upgradable_id[1])
#         )
#         for id in self.footer_shape_id:
#             self._button_coords.append(self.main_canvas.bbox(id))
#         print('something')
#         print(i for i in self._button_coords)
