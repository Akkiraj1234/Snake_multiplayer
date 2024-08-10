import json
from os import listdir,name,path
from helper import get_nested_value

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
        self.__path_set_up()
    
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
    
    def _defult_player_data(self, name:str|None = None, password:str|None = None) -> None:
        """
        return defult data for player account
        takes name and password as artibute optional
        """
        
        return {
            "name": "demo_player" if not name else name,
            "password": "123" if not password else password,
            "HIGH_SCORE": 0,
            "points": 0,
            "inisial_heart": 1,
            "inisiak_snake": 1,
            "coin_value": 2,
            "text_info": {
                "selected_index": 0,
                "items": [
                        {"color": "#FFFFFF","selected": True,"purchased": True,"price": 0},
                        {"color": "#333333","selected": False,"purchased": False,"price": 100},
                        {"color": "#4B0082","selected": False,"purchased": False,"price": 120},
                        {"color": "#2F4F4F","selected": False,"purchased": False,"price": 150},
                        {"color": "#800000","selected": False,"purchased": False,"price": 250},
                        {"color": "#000000","selected": False,"purchased": False,"price": 100},
                        {"color": "#F8F8FF","selected": False,"purchased": False,"price": 150},
                        {"color": "#D3D3D3","selected": False,"purchased": False,"price": 200},
                        {"color": "#FFD700","selected": False,"purchased": False,"price": 300},
                        {"color": "#00FF00","selected": False,"purchased": False,"price": 500}
                    ],
                "upgradable": 0,
                "charge": 0
            },
            "nevigation_info": {
                "selected_index": 0,
                "items": [
                        {"color": "#000000","selected": True,"purchased": True,"price": 0},
                        {"color": "#32CD32","selected": False,"purchased": False,"price": 200},
                        {"color": "#1E90FF","selected": False,"purchased": False,"price": 380},
                        {"color": "#FF6347","selected": False,"purchased": False,"price": 230},
                        {"color": "#FF69B4","selected": False,"purchased": False,"price": 250},
                        {"color": "#8A2BE2","selected": False,"purchased": False,"price": 500},
                    ],
                "upgradable": 0,
                "charge": 0
            },
            "canvas_info": {
                "selected_index": 0,
                "items": [
                        {"color": "#050B2B","selected": True,"purchased" : True ,"price": 0},
                        {"color": "#228B22","selected": False,"purchased": False,"price": 380},
                        {"color": "#2E8B57","selected": False,"purchased": False,"price": 380},
                        {"color": "#006400","selected": False,"purchased": False,"price": 380},
                        {"color": "#556B2F","selected": False,"purchased": False,"price": 280},
                        {"color": "#8FBC8F","selected": False,"purchased": False,"price": 500},
                        {"color": "#9ACD32","selected": False,"purchased": False,"price": 380},
                        {"color": "#BDB76B","selected": False,"purchased": False,"price": 200},
                        {"color": "#808000","selected": False,"purchased": False,"price": 500},
                        {"color": "#3CB371","selected": False,"purchased": False,"price": 2000},
                        {"color": "#6B8E23","selected": False,"purchased": False,"price": 500}
                    ],
                "upgradable": 0,
                "charge": 0
            },
            "food_info": {
                "selected_index": 0,
                "items": [
                        {"color": "#ff0000","selected": True,"purchased" : True ,"price": 0},
                        {"color": "#FFFF00","selected": False,"purchased": False,"price": 380},
                        {"color": "#FFA500","selected": False,"purchased": False,"price": 380},
                        {"color": "#800080","selected": False,"purchased": False,"price": 380},
                        {"color": "#00FF00","selected": False,"purchased": False,"price": 200},
                        {"color": "#FFC0CB","selected": False,"purchased": False,"price": 500},
                        {"color": "#8B4513","selected": False,"purchased": False,"price": 380},
                        {"color": "#00FFFF","selected": False,"purchased": False,"price": 200},
                        {"color": "#FFD700","selected": False,"purchased": False,"price": 500},
                        {"color": "#FF6347","selected": False,"purchased": False,"price": 200},
                        {"color": "#4B0082","selected": False,"purchased": False,"price": 500},
                        {"color": "#ADFF2F","selected": False,"purchased": False,"price": 500}
                    ],
                "upgradable": 0,
                "charge": 0
            },
            "heart_info": {
                "selected_index": 0,
                "items": [
                        {"color": "#FF0000","selected": True,"purchased" : True ,"price": 0},
                        {"color": "#E60000","selected": False,"purchased": False,"price": 380},
                        {"color": "#FF69B4","selected": False,"purchased": False,"price": 380},
                        {"color": "#FF1493","selected": False,"purchased": False,"price": 380},
                        {"color": "#DB7093","selected": False,"purchased": False,"price": 200},
                        {"color": "#C71585","selected": False,"purchased": False,"price": 500},
                        {"color": "#FF4500","selected": False,"purchased": False,"price": 380},
                        {"color": "#FF6347","selected": False,"purchased": False,"price": 200},
                        {"color": "#CD5C5C","selected": False,"purchased": False,"price": 500}
                    ],
                "upgradable": 1,
                "charge": 500
            },
            "snake_info": {
                "selected_index": 0,
                "items": [
                        {"color": "#ffff00","selected": True,"purchased" : True ,"price": 0},
                        {"color": "#32CD32","selected": False,"purchased": False,"price": 380},
                        {"color": "#1E90FF","selected": False,"purchased": False,"price": 380},
                        {"color": "#FFD700","selected": False,"purchased": False,"price": 380},
                        {"color": "#FF1493","selected": False,"purchased": False,"price": 200},
                        {"color": "#8A2BE2","selected": False,"purchased": False,"price": 500},
                        {"color": "#FF6347","selected": False,"purchased": False,"price": 380},
                        {"color": "#00CED1","selected": False,"purchased": False,"price": 200},
                        {"color": "#ADFF2F","selected": False,"purchased": False,"price": 500},
                        {"color": "#FF69B4","selected": False,"purchased": False,"price": 200},
                        {"color": "#FF8C00","selected": False,"purchased": False,"price": 500},
                        {"color": "#7FFF00","selected": False,"purchased": False,"price": 500}
                    ],
                "upgradable": 1,
                "charge": 100
            },
            "coin_info": {
                "selected_index": 0,
                "items": [
                        {"color": "#ff0000","selected": True,"purchased" : True ,"price": 0},
                        {"color": "#FFFF00","selected": False,"purchased": False,"price": 380},
                        {"color": "#FFA500","selected": False,"purchased": False,"price": 380},
                        {"color": "#800080","selected": False,"purchased": False,"price": 380},
                        {"color": "#00FF00","selected": False,"purchased": False,"price": 220},
                        {"color": "#FFC0CB","selected": False,"purchased": False,"price": 500},
                        {"color": "#8B4513","selected": False,"purchased": False,"price": 380},
                        {"color": "#00FFFF","selected": False,"purchased": False,"price": 250},
                        {"color": "#FF6347","selected": False,"purchased": False,"price": 200},
                        {"color": "#4B0082","selected": False,"purchased": False,"price": 500},
                        {"color": "#ADFF2F","selected": False,"purchased": False,"price": 500},
                    ],
                "upgradable": 1,
                "charge": 1000
            }
        }

    def _defult_setting_data(self, account:str|None = None ) -> None:
        """
        return sefult setting data
        takes account as argumtnt
        """
        return {
            "basic_info": {
                "game_width": 720,
                "game_height": 360,
                "box_size": 40,
                "speed": 100,
                "text_size": 8,
                "volume_level": 80
            },
            "theme": {
                "theme1": "#e6f2ff",
                "theme2": "#111111",
                "theme3": "#ff6f61"
            },
            "game_info": {
                "Account": "demo_player" if not account else account,
                "verstion": "1.0",
                "box_size": 30,
                "game_speed": 100
            }
        }
    
    def __path_set_up(self):
        if name == 'nt':  # Check if the OS is Windows
            self.path = path.join('C:', 'Users', 'Public', 'snake_game')
        else:
            self.path = path.join('/home', 'public', 'snake_game')
        
        self.account_path = path.join(self.path,"player_info")
        self.setting_path = path.join(self.path,"Game_assest")
        
        if not path.exists(self.account_path):
            print("path didnt found run setup.exe")
            quit()
        if not path.exists(self.setting_path):
            print("path didnt found run setup.exe")
            quit()
         
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
    
    def _check_path_and_get_info(self,location:str,value_keys:list):
        """
        Checks if the specified file path exists and retrieves information from the file.

        This method checks whether the provided file path exists. If the file exists,
        it reads and loads the JSON data from the file, then retrieves the value
        specified by the list of keys using `get_nested_value`.

        Parameters:
        location (str): The file path to check and read from.
        value_keys (list): A list of keys representing the path to the desired value in the JSON data.

        Returns:
        any: The value retrieved from the JSON data, or an empty dictionary if the file 
            doesn't exist or the keys are not found.
        """
        if path.exists(location):
            pass
        with open(location,'r',encoding='utf-8') as data:
            try:
                data = json.load(data)
            except json.JSONDecodeError:
                pass
        return get_nested_value(data,value_keys)
            
            
        
        
    def create_fille(slef,obj,path):
        with open(path,'w',encoding='utf-8') as new_file:
            json.dump(obj,new_file)
        
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
        path_name = f"player_info\\{self._active_account}.json"
        
        if not path.exists(path_name):
            print('lol')
            quit()
        
        # Extracting player information by id
        with open(path_name,"r",encoding="utf-8") as Account_details:
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

    def change_account(self,path_,name) -> bool:
        return False
    
    def update_by_dict(self, info:dict) -> None:
        """
        update the variable class by dict

        Args:
            info (dict): a dict contain info regarding what u wanna update

        None:
            the dict key should be name similar to the artibute of this class to update
        """
        if info is None:
            return None
        
        for name , value in info.items():
            if hasattr(self,name):
                setattr(self, name, value)
        self.updaing_game_setting()
        
    def get_account_list(self) -> tuple[str,tuple[str]]:
        data = listdir(self.account_path)
        data = [name.split('.')[0] for name in data]
        return self.active_user_name, data
        
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