import json
from tkinter import Label,Entry,OptionMenu,Button,StringVar,Scale

class Variable:
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
        self.get_the_info()
        
        #fixed and constant variables
        self.SNAKE_LENGHT = 3
        self.SNAKE_CORDINATES = (0,0)
        self.FONT_STYLE =  "Press Start 2P" 
        self.Form_font = "Myanmar Text"
        self.INISIAL_HOME_TEXT = "Sneck suffarie :0"
        
        self.game_speed = 120
        self.game_box_size = 30
    
    def get_the_info(self):
        """
        Initialize the game and user variables by loading data from JSON files.
        """
        self.getting_and_extracting_info()
        
        #game basic info that stay same for every user by changing it change but for all user
        self.game_width     = self._game_setting["basic_info"]["game_width"]
        self.game_height    = self._game_setting["basic_info"]["game_height"]
        self.home_boxsize   = self._game_setting["basic_info"]["box_size"]
        self.home_speed     = self._game_setting["basic_info"]["speed"]
        self.home_text_size = self._game_setting["basic_info"]["text_size"]
        self.volume_level   = self._game_setting["basic_info"]["volume_level"]
        self.theme1         = self._game_setting["theme"]["theme1"]
        self.theme2         = self._game_setting["theme"]["theme2"]
        self.version        = self._game_setting["game_info"]["verstion"]
        
        #user info that changes by every new_users
        self.active_user_name     = self._player_acc_info["name"]
        self.PLAYERP_COINE  = self._player_acc_info["points"]
        self.HIGHT_SCORE    = self._player_acc_info["HIGH_SCORE"]
        self.NEV_COLOR      = self._player_acc_info["Cur_nev_color"]
        self.TEXT_COLOR     = self._player_acc_info["cur_text_color"]
        self.HEART_COLOR    = self._player_acc_info["cur_heart_color"]
        self.CANVAS_COLOR   = self._player_acc_info["cur_canvas_color"]
        self.FOOD_COLOR     = self._player_acc_info["cur_food_color"]
        self.SNAKE_COLOR    = self._player_acc_info["cur_snake_color"]
        self.INISISAL_HEART = self._player_acc_info["inisial_heart"]
        self.SNAKE_LOSS_COUNTDOWN = self._player_acc_info["countdown_time_s"]
        
        self.owned_heart_color  = self._player_acc_info["owned_heart_color"]
        self.owned_nev_color    = self._player_acc_info["inisial_heart"]
        self.owned_food_color   = self._player_acc_info["owned_food_color"]
        self.owned_snake_color  = self._player_acc_info["owned_snake_color"]
        self.owned_canvas_color = self._player_acc_info["owned_canvas_color"]
        
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
        self._active_account = self._game_setting["game_info"]["Account"]
            
        # Extracting player information by id
        with open(f"player_info\\{self._active_account}.json","r",encoding="utf-8") as Account_details:
            self._player_acc_info = json.load(Account_details)
    
    def update_user_settings(self) -> None:
        """
        Update user settings in the player account JSON file 
        by anything changes on the variable.
        """
        self._player_acc_info["name"]              = self.active_user_name
        self._player_acc_info["HIGH_SCORE"]        = self.HIGHT_SCORE
        self._player_acc_info["points"]            = self.PLAYERP_COINE
        self._player_acc_info["Cur_nev_color"]     = self.NEV_COLOR
        self._player_acc_info["cur_text_color"]    = self.TEXT_COLOR
        self._player_acc_info["cur_heart_color"]   = self.HEART_COLOR
        self._player_acc_info["cur_canvas_color"]  = self.CANVAS_COLOR
        self._player_acc_info["cur_food_color"]    = self.FOOD_COLOR
        self._player_acc_info["cur_snake_color"]   = self.SNAKE_COLOR
        self._player_acc_info["inisial_heart"]     = self.INISISAL_HEART
        self._player_acc_info["countdown_time_s"]  = self.SNAKE_LOSS_COUNTDOWN
        
        self._player_acc_info["owned_nev_color"]   = self.owned_nev_color
        self._player_acc_info["owned_heart_color"] = self.owned_heart_color
        self._player_acc_info["owned_canvas_color"]= self.owned_canvas_color
        self._player_acc_info["owned_food_color"]  = self.owned_food_color
        self._player_acc_info["owned_snake_color"] = self.owned_snake_color
        
        with open(f"player_info\\{self._active_account}.json", "w", encoding="utf-8") as player_file:
            json.dump(self._player_acc_info, player_file,)
            
    def updaing_game_setting(self) -> None:
        """
        Update game settings in the 'setting.json' file.
        by anything chnageed on the variable
        """
        self._game_setting["basic_info"]["game_width"]  = self.game_width
        self._game_setting["basic_info"]["game_height"] = self.game_height
        self._game_setting["basic_info"]["box_size"]    = self.home_boxsize
        self._game_setting["basic_info"]["speed"]       = self.home_speed
        self._game_setting["basic_info"]["text_size"]   = self.home_text_size
        self._game_setting["basic_info"]["volume_level"]= self.volume_level
        self._game_setting["theme"]["theme1"]           = self.theme1
        self._game_setting["theme"]["theme2"]           = self.theme2
        self._game_setting["game_info"]["Account"]      = self._active_account
        
        with open("Game_assets\\setting.json","w",encoding="utf-8") as game_setting:
            json.dump(self._game_setting,game_setting)
            
    def updaing_game_setting(self) -> None:
        """
        Update game settings in the 'setting.json' file.
        by anything chnageed on the variable
        """
        self._game_setting["basic_info"]["game_width"] = self.game_width
        self._game_setting["basic_info"]["game_height"] = self.game_height
        self._game_setting["basic_info"]["box_size"] = self.home_boxsize
        self._game_setting["basic_info"]["speed"] = self.home_speed
        self._game_setting["basic_info"]["text_size"] = self.home_text_size
        self._game_setting["basic_info"]["volume_level"] = self.volume_level
        self._game_setting["theme"]["theme1"] = self.theme1
        self._game_setting["theme"]["theme2"] = self.theme2
        self._game_setting["game_info"]["box_size"] = self.game_box_size
        self._game_setting["game_info"]["game_speed"] = self.game_speed
        self._game_setting["game_info"]["Account"] = self._active_account
        
        with open("Game_assets\\setting.json","w",encoding="utf-8") as game_setting:
            json.dump(self._game_setting,game_setting)
    
    def basic_setting_screen_var(self,canvas , button_method):
        '''
        inisalize variable and widgets required to show in basic 
        setting screen canvs
        '''
        option1 = ("Slow", "Normal", "Fast", "Extreme")
        option2 = ("Small", "Medium", "Large", "Extra Large")
        
        lable1 = Label(canvas ,text="Game Width  :", font=('Arial',self.home_text_size,'bold'))
        lable2 = Label(canvas ,text="Game Height :", font=('Arial',self.home_text_size,'bold'))
        lable3 = Label(canvas ,text="Speed (Home):", font=('Arial',self.home_text_size,'bold'))
        lable4 = Label(canvas ,text="Size (Home)  :",font=('Arial',self.home_text_size,'bold'))
        lable5 = Label(canvas ,text="text size   :", font=('Arial',self.home_text_size,'bold'))
        lable6 = Label(canvas ,text="Volume level:", font=('Arial',self.home_text_size,'bold'))
        
        self.bssv_back_button = Button(
            canvas ,text="Account Setting",font=('Arial',self.home_text_size,'bold'),
            relief="groove", width=30 , command=button_method
        )
        self.bssv_width_entry = Entry(canvas, width=15, font=('Arial',self.home_text_size,'bold'))
        self.bssv_height_entry = Entry(canvas ,width=15, font=('Arial',self.home_text_size,'bold'))
        
        self.bssv_speed_get = StringVar(canvas)
        self.bssv_size_get = StringVar(canvas)
        
        self.bssv_text_get = Scale(
            canvas, from_= 5 , to = 20 , length = 107, orient="horizontal",
            relief="groove",sliderlength=10, sliderrelief="flat",font=('Arial',self.home_text_size,'bold'))
        self.bssv_volume_get = Scale(
            canvas ,from_= 0 , to = 100 , length = 107, orient="horizontal",
            relief="groove",sliderlength=10, sliderrelief="flat",font=('Arial',self.home_text_size,'bold'))
        
        Speed_get = OptionMenu(canvas, self.bssv_speed_get,*option1)
        size_get = OptionMenu(canvas , self.bssv_size_get, *option2)
        
        #insializing values in widgets :
        self.bssv_width_entry.insert(0,self.game_width)
        self.bssv_height_entry.insert(0,self.game_height)
        size = self.home_boxsize
        self.bssv_speed_get.set('Small'if size == 15 else "Medium" if size == 30 else 'Large' if size == 45 else 'Extra Large')
        speed = self.home_speed
        self.bssv_size_get.set('Extreme' if speed == 100 else 'Fast' if speed == 150 else 'Normal' if speed == 200 else 'Slow')
        self.bssv_text_get.set(self.home_text_size)
        self.bssv_volume_get.set(self.volume_level)
        
        #retuning the values :
        return (
            (lable1 , lable2),
            (self.bssv_width_entry , self.bssv_height_entry),
            (lable3 , Speed_get),
            (lable4 , size_get),
            (lable5 , self.bssv_text_get),
            (lable6 , self.bssv_volume_get),
            (self.bssv_back_button , None)
        )
    
    def setting_option_menu_var(self,canvas, changepass_method,createnewacc_method,changeaccount_method,goback_method):
        '''
        inisalize variable and widgets required to show in 
        account setting screen
        '''
        #adding_windows:==========================================================
        lable1 = Label(canvas, text="Name  :",font=('Arial',self.home_text_size,'bold'))
        lable2 = Label(canvas, text="Heigh Score",font=('Arial',self.home_text_size,'bold'))
        lable3 = Label(canvas, text="Money",font=('Arial',self.home_text_size,'bold'))
        
        self.somv_name_get = Entry(canvas, width=15,font=('Arial',self.home_text_size,'bold'))
        self.somv_heightscore_lable = Label(canvas, text="",font=('Arial',self.home_text_size,'bold'))
        self.somv_coin_lable = Label(canvas, text="",font=('Arial',self.home_text_size,'bold'))
        
        change_password = Button(
            canvas, text="Change password", font=('Arial',self.home_text_size,'bold'),
            relief="groove",width=30,command=changepass_method)
        create_new_account = Button(
            canvas, text="new account", font=('Arial',self.home_text_size,'bold'),
            relief="groove",width=14,command=createnewacc_method)
        change_account = Button(
            canvas, text="change account", font=('Arial',self.home_text_size,'bold'),
            relief="groove",width=14,command=changeaccount_method)
        go_back = Button(
            canvas, text="<- go back", font=('Arial',self.home_text_size,'bold'),
            relief="groove",width=30,command=goback_method)
        
        #adding_value;0
        self.somv_name_get.insert(0,self.active_user_name)
        self.somv_heightscore_lable.config(text=self.HIGHT_SCORE)
        self.somv_coin_lable.config(text=self.PLAYERP_COINE)
        
        #returning the value 
        return (
            (lable1 , self.somv_name_get),
            (lable2 , self.somv_heightscore_lable),
            (lable3 , self.somv_coin_lable),
            (change_password , None),
            (create_new_account , change_account),
            (go_back , None)
        )
        
        
    
    def update_password(self,password) -> None:
        """
        Update the player's account password.

        This method updates the password associated with the player's account.
        However, it's currently implemented as a placeholder and does not perform
        any actual password update operation. Future implementation should include
        appropriate security measures for updating passwords.
        """
        self._player_acc_info["password"] = password
        
        with open(f"player_info\\{self._active_account}.json", "w", encoding="utf-8") as player_file:
            json.dump(self._player_acc_info, player_file)
        
    
    def update(self) -> None:
        """
        Update both user and game settings.
        """
        self.update_user_settings()
        self.updaing_game_setting()