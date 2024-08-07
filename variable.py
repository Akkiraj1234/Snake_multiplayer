import json

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
        self.SNAKE_CORDINATES = (0,0)
        self.SNAKE_LOSS_COUNTDOWN = 2
        self.HEART_LIMIT = 5
        self.FONT_STYLE =  "Press Start 2P" 
        self.Form_font = "Myanmar Text"
        self.INISIAL_HOME_TEXT = "Sneck suffarie :0"
        self.CHANCE_OF_DROP = 17
        self.INCREASE_SPEED_AFTER = 20
        
        self.game_speed = 100
        self.game_box_size = 30
    
    @property
    def CANVAS_COLOR(self) -> str:
        return self._player_acc_info["canvas_info"]["items"][self._player_acc_info["canvas_info"]["selected_index"]]["color"]
    
    @property
    def NEV_COLOR(self) -> str:
        return self._player_acc_info["nevigation_info"]["items"][self._player_acc_info["nevigation_info"]["selected_index"]]["color"]
    
    @property
    def TEXT_COLOR(self) -> str:
        return self._player_acc_info["text_info"]["items"][self._player_acc_info["text_info"]["selected_index"]]["color"]
    
    @property
    def FOOD_COLOR(self) -> str:
        return self._player_acc_info["food_info"]["items"][self._player_acc_info["food_info"]["selected_index"]]["color"]
    
    @property
    def HEART_COLOR(self) -> str:
        return self._player_acc_info["heart_info"]["items"][self._player_acc_info["heart_info"]["selected_index"]]["color"]
    
    @property
    def COIN_COLOR(self) -> str:
        return self._player_acc_info["coin_info"]["items"][self._player_acc_info["coin_info"]["selected_index"]]["color"]
    
    @property
    def SNAKE_COLOR(self) -> str:
        return self._player_acc_info["snake_info"]["items"][self._player_acc_info["snake_info"]["selected_index"]]["color"]
    
    @property
    def SNAKE_LENGHT(self) -> int:
        return self._player_acc_info["snake_info"]["upgradable"] * self._player_acc_info["inisiak_snake"]
    
    @property
    def INISISAL_HEART(self) -> int:
        return self._player_acc_info["heart_info"]["upgradable"] * self._player_acc_info["inisial_heart"]

    @property
    def COIN_VALUE(self) -> int:
        return self._player_acc_info["coin_info"]["upgradable"] * self._player_acc_info["coin_value"]
        
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
        self.theme3         = self._game_setting["theme"]["theme3"]
        self.version        = self._game_setting["game_info"]["verstion"]
        
        #user info that changes by every new_users
        self.active_user_name     = self._player_acc_info["name"]
        self.PLAYERP_COINE  = self._player_acc_info["points"]
        self.HIGHT_SCORE    = self._player_acc_info["HIGH_SCORE"]
        
        self.canvas_info = self._player_acc_info["canvas_info"]
        self.nevigation_info    = self._player_acc_info["nevigation_info"]
        self.text_info = self._player_acc_info["text_info"]
        self.food_info   = self._player_acc_info["food_info"]
        self.snake_info  = self._player_acc_info["snake_info"]
        self.heart_info  = self._player_acc_info["heart_info"]
        self.coin_info = self._player_acc_info["coin_info"]
        
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
        
        self._player_acc_info["canvas_info"] = self.canvas_info
        self._player_acc_info["nevigation_info"] = self.nevigation_info
        self._player_acc_info["text_info"] = self.text_info
        self._player_acc_info["food_info"] = self.food_info 
        self._player_acc_info["snake_info"] = self.snake_info 
        self._player_acc_info["heart_info"] = self.heart_info
        self._player_acc_info["coin_info"] = self.coin_info
        
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

    def update_by_dict(self, info) -> None:
        print(info)
        
    def get_account_list(self) -> tuple[str,tuple[str]]:
        return self.active_user_name, ("hello world", "test subject", "lol")
        
class demo_variable:
    
    def __init__(self, dict1:dict) -> None:
        """
        inisialize game arttibutes
        """
        self.add_new_element(dict1)
        
    
    def update_with_dict(self, dict1:dict) -> None:
        """
        Update the attributes of the instance with the values from the provided dictionary.
        """
        for key, value in dict1.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def add_new_element(self, dict1:dict) -> None:
        """
        add new elemnt to class by dict
        """
        for key, value in dict1.items():
            setattr(self, key, value)