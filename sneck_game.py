from tkinter import Tk, Canvas, Frame, Button, Label
from random import choice , randint
import time

class Snake:
    """Represents a snake in the game.

    Attributes:
        canvas (Canvas): The canvas on which the snake will be drawn.
        length (int): The initial length of the snake.
        coordinates (tuple): The initial coordinates of the snake.
        color (str): The color of the snake.
        box_size (int): The size of each box representing a segment of the snake.

    Methods:
        __init__(canvas, length, coordinates, color, box_size): Initialize a new Snake object.
        _create_snake(): Create the snake on the canvas.
        move_snake(x, y, remove): Move the snake to the new coordinates.
        _create_body(x, y): Create a segment of the snake.
    """
    
    def __init__(self,canvas:Canvas,lenght:int,coordinates:tuple,color:str,box_size:int) -> None :
        """Initialize the Snake object on the canvas.

        Args:
            canvas (Canvas): The canvas on which the snake will be drawn.
            length (int): The initial length of the snake.
            coordinates (tuple): The initial coordinates of the snake.
            color (str): The color of the snake.
            box_size (int): The size of each box representing a segment of the snake.
        """
        self.box_size = box_size
        self.color = color
        self.canvas = canvas
        self.lenght=lenght
        self.coordinates = coordinates
        self._create_snake()
        
    def _create_snake(self)-> None:
        """Create the snake on the canvas."""
        self.snake_coordinates=[self.coordinates]*self.lenght
        self.snake_body=[self._create_body(x,y) for x,y in self.snake_coordinates]
        
    def move_snake(self,x:int,y:int,remove:bool)-> None:
        """Move the snake to the new coordinates.

        Args:
            x (int): The x-coordinate of the new position.
            y (int): The y-coordinate of the new position.
            remove (bool): Whether to remove the last segment of the snake.
        """
        self.snake_coordinates.insert(0,(x,y))
        self.snake_body.insert(0,self._create_body(x,y))
        
        if remove:
            self.snake_coordinates.pop()
            self.canvas.delete(self.snake_body.pop())
    
    def _create_body(self,x:int,y:int)-> None:
        """Create a segment of the snake.

        Args:
            x (int): The x-coordinate of the segment.
            y (int): The y-coordinate of the segment.

        Returns:
            int: The id of the created segment on the canvas.
        """
        square= self.canvas.create_rectangle(x,y,x+self.box_size,y+self.box_size,fill=self.color)
        return square
    
class Food:
    """Represents a food item in the game.

    Attributes:
        canvas (Canvas): The canvas on which the food item will be drawn.
        box_size (int): The size of each box representing the food item.
        color (str): The color of the food item.
        game_width (int): The width of the game area.
        game_height (int): The height of the game area.
        food (int): The ID of the current food item on the canvas.
        x (int): The x-coordinate of the food item.
        y (int): The y-coordinate of the food item.

    Methods:
        __init__(canvas, box_size, color, game_width, game_height, food_type="oval"): Initialize a new Food object.
        _create_food_oval(): Create an oval-shaped food item on the canvas.
        _create_food_square(): Create a square-shaped food item on the canvas.
        new_coordinates(): Generate new random coordinates for the food item.
        _delete_food(): Delete the current food item from the canvas.
        new_food(food_type): Create a new food item of the specified type.
    """
    def __init__(self, canvas:Canvas, box_size:int, color:str ,game_width:int ,game_height:int, food_type:str="oval")-> None:
        """Initialize the Food object.

        Args:
            canvas (Canvas): The canvas on which the food item will be drawn.
            box_size (int): The size of each box representing the food item.
            color (str): The color of the food item.
            game_width (int): The width of the game area.
            game_height (int): The height of the game area.
            food_type (str, optional): The type of the food item ("oval" or "square"). Defaults to "oval".
        """
        self.canvas = canvas
        self.box_size = box_size
        self.color = color
        self.game_width = game_width
        self.game_height = game_height
        self.food=None
        self.x=0
        self.y=0
        self.new_coordinates()
        self.new_food(food_type)
        
    def _create_food_oval(self):
        """Create an oval-shaped food item."""
        self.food=self.canvas.create_oval(self.x,self.y,self.x+self.box_size,self.y+self.box_size,fill=self.color)
    
    def _create_food_square(self):
        """Create a square-shaped food item."""
        # self.food=self.canvas.create_polygon(self.x,self.y,self.x+self.box_size,self.y+self.box_size,fill=self.color)
        self.food = self.canvas.create_polygon(self.x, self.y, self.x + self.box_size, self.y + self.box_size, fill=self.color)
        
    def new_coordinates(self):
        """Generate new random coordinates for the food item."""
        self.x = randint(0, (self.game_width // self.box_size)-1)* self.box_size
        self.y =  randint(0, (self.game_height // self.box_size)-1)* self.box_size
    
    def _delete_food(self):
        """Delete the current food item from the canvas."""
        self.canvas.delete(self.food)
    
    def new_food(self,food_type:str):
        """Create a new food item of the specified type.

        Args:
            food_type (str): The type of the food item ("oval" or "square" or "any" ).
        """
        if self.food:
            self._delete_food()
        self.new_coordinates()
        
        if food_type == "oval":
            self._create_food_oval()
        elif food_type == "square":
            self._create_food_square()
        else:
            self._create_food_oval()


class Heart:
    """
    Represents a heart shape drawn on a canvas.

    This class provides methods to add, remove, and manipulate heart shapes on a canvas.

    Attributes:
        canvas (Canvas): The canvas on which the hearts are drawn.
        coordinates (tuple): The initial coordinates (x, y) of the top-left corner of the heart.
        box_size (int): The size of the bounding box of the heart.
        color (str): The color of the heart.
        distance (int): The distance between each heart when added.
        hearts_list (list): A list to store the IDs of the heart shapes drawn on the canvas.
        limit (int or None): The maximum number of hearts allowed on the canvas. If set, adding more hearts will be limited.
    """
    def __init__(self,canvas:Canvas , cordnites:tuple , box_size:int , color:str , inisial_heart=1):
        """
        Initialize a Heart object.

        Args:
            canvas (Canvas): The canvas on which the heart will be drawn.
            coordinates (tuple): The initial coordinates (x, y) of the top-left corner of the heart.
            box_size (int): The size of the bounding box of the heart.
            color (str): The color of the heart.
            initial_heart (int, optional): The number of hearts to initialize. Defaults to 1.
        """
        self.canvas = canvas
        self.cordinates = cordnites
        self.box_size = box_size
        self.color = color
        self.distance = self.box_size // 4
        self.hearts_list = []
        self.limit = None
        self.heart()
        for _ in range(inisial_heart-1):
            self.add_one_heart()
    
    def add_one_heart(self):
        """
        Add one heart to the canvas.

        If the limit is set and the number of hearts exceeds the limit, no heart will be added.

        Returns:
            None
        """
        if self.limit and len(self.hearts_list)>= self.limit:
            return None
        self.cordinates = (self.cordinates[0]-self.box_size-self.distance , self.cordinates[1])
        self.heart()
        
    def remmove_heart(self):
        """
        Remove the last heart from the canvas.

        Returns:
            None
        """
        if self.hearts_list == []:
            return None
        for ids in self.hearts_list.pop():
            self.canvas.delete(ids)
        self.cordinates = (self.cordinates[0]+self.box_size+self.distance , self.cordinates[1])
        
    def heart(self):
        """
        Draw a heart shape on the canvas.

        This method calculates the coordinates and dimensions of the heart shape
        based on the given parameters and draws it on the canvas.

        Returns:
            None
        """
        x1 , y1 = self.cordinates
        x2 , y2 = x1 + self.box_size , y1 + self.box_size

        new_y1 = (self.box_size / 2) + y1
        new_x1 = (self.box_size / 2) + x1
        radious = (new_y1 - y1) / 2
        
        first = self.canvas.create_arc(x1,new_y1-radious,new_x1,new_y1+radious,fill=self.color,start=0,extent=180)
        secoend = self.canvas.create_arc(new_x1,new_y1-radious,x2,new_y1+radious,fill=self.color,start=0,extent=180)
        third = self.canvas.create_polygon(x1,new_y1,x2,new_y1,(x1+x2)/2,y2,fill=self.color)
        self.hearts_list.append((first,secoend,third))
            
            
class goofy_Snakes:
    """Represents a goofy snake in the game.

    Attributes:
        master (Canvas): The canvas on which the snake will be drawn.
        color (str): The color of the snake.
        coordinates (tuple): The initial coordinates of the snake.
        length (int): The initial length of the snake.
        initial_direction (str): The initial direction of the snake.
        box_size (int): The size of each box representing a segment of the snake.
        snake (Snake): The Snake object representing the snake on the canvas.
        coordinate (tuple): The current coordinates of the snake's head.

    Methods:
        __init__(master, color, coordinates, length, initial_direction, box_size): Initialize a new goofy_Snakes object.
        random_direction(): Randomly choose a new direction for the snake.
        calculate_new_coordinates(): Calculate new coordinates for the snake's head based on its current direction.
        move_the_snakes(): Move the snake to the new coordinates.
    """
    def __init__(self,master:Canvas, color:str ,coordinates:tuple, lenght:int ,inisial_direction:str, box_size:int)-> None:
        """Initialize a new goofy_Snakes object.

        Args:
            master (Canvas): The canvas on which the snake will be drawn.
            color (str): The color of the snake.
            coordinates (tuple): The initial coordinates of the snake.
            length (int): The initial length of the snake.
            initial_direction (str): The initial direction of the snake.
            box_size (int): The size of each box representing a segment of the snake.
        """
        self.master = master
        self.color = color
        self.coordinates = coordinates
        self.lenght = lenght
        self.direction = inisial_direction
        self.box_size = box_size
        self.snake = Snake(self.master, self.lenght, self.coordinates, self.color, self.box_size)
        
    def random_direction(self):
        """Randomly choose a new direction for the snake."""
        new_direction = choice(("down","right","down","right","down","left","up","down"))
        if new_direction in ("down","up") and self.direction in ("down","up"):
            pass
        elif new_direction in ("right","left") and self.direction in ("right","left"):
            pass
        else: self.direction = new_direction
    
    def calculate_new_coordinates(self):
        """Calculate new coordinates for the snake's head based on its current direction."""
        self.random_direction()
        x , y =self.snake.snake_coordinates[0]
        if self.direction == "up":
            y -= self.box_size
        elif self.direction == "down":
            y += self.box_size
        elif self.direction == "right":
            x += self.box_size
        elif self.direction == "left":
            x -= self.box_size
        
        #adjusting screen :0
        canvas_width = self.master.winfo_width()
        canvas_height = self.master.winfo_height()
        x = canvas_width if x < 0 else 0 if x > canvas_width else x
        y = canvas_height if y < 0 else 0 if y > canvas_height else y
        
        self.coordinates = (x,y)
    
    def move_the_snakes(self):
        """Move the snake to the new coordinates."""
        self.calculate_new_coordinates()
        x , y = self.coordinates
        self.snake.move_snake(x,y,True)

        
class inisial_screens:
    """A class representing an initial screen setup for a game.

    This class provides methods for setting up the initial screen of a game, including adding snakes, food items, starting animations, and managing animations.

    Attributes:
        master: The master widget where the initial screen will be placed.
        background_color (str): The background color of the game screen.
        game_width (int): The width of the game screen.
        box_size (int): The size of each box or unit in the game grid.
        game_height (int): The height of the game screen.
        speed (int): The speed of animations in milliseconds.
        child_window (tkinter.Canvas): The canvas widget representing the game screen.
        food (Food): The food item on the game screen.
        snakes (list): A list containing snake objects on the game screen.
        animation_after_ids: A reference to the animation after method IDs for managing animation loops.

    Methods:
        __init__: Initializes the initial screen with provided parameters.
        add_snakes: Adds a snake to the game screen.
        add_food: Adds a food item to the game screen.
        start_animation: Starts the animation loop for moving snakes and updating the game state.
        stop_animation: Stops the animation loop.
        add_button: Adds a button widget to the game screen.

    Example:
        # Initialize the initial screen
        initial_screen = inisial_screens(master, background_color='black', game_width=800, box_size=20, game_height=600, speed=100)

        # Add a snake to the initial screen
        initial_screen.add_snakes(color='green', coordinates=(5, 5), length=3, direction='right')

        # Add food to the initial screen
        initial_screen.add_food(color='red', food_type='oval', random_color=True)

        # Start the animation loop
        initial_screen.start_animation()

        # Stop the animation loop
        initial_screen.stop_animation()

        # Add a button to the game screen
        initial_screen.add_button(button1, button2, button3)
    """
    
    def __init__(self,master,background_color:str,game_width:int,box_size:int, game_height:int,speed:int,pack=True) -> None:
        """Initialize the initial screen of the game.

        Args:
            master: The master widget where the initial screen will be placed.
            background_color (str): The background color of the game screen.
            game_width (int): The width of the game screen.
            box_size (int): The size of each box or unit in the game grid.
            game_height (int): The height of the game screen.
            speed (int): The speed of animations in milliseconds.
            pack (bool): Whether to automatically pack the canvas widget (default is True).
        """
        self.master = master
        self.background_color = background_color
        self.game_width = game_width
        self.game_height = game_height
        self.box_size = box_size
        self.speed=speed
        
        self.child_window = Canvas(self.master,bg=self.background_color,height=self.game_height,width=self.game_width)
        if pack: self.child_window.pack()
        self.food = None
        self.snakes = []
        self.animation_after_ids=None
    
    def add_to_window(self):
        self.child_window.pack()
    
    def add_snakes(self, color:str ,coordinates:tuple, lenght:int, direction:str)-> None:
        """Add a snake to the game screen.

        Args:
            color (str): The color of the snake.
            coordinates (tuple): The initial coordinates of the snake.
            length (int): The length of the snake.
            direction (str): The initial direction of the snake ('up', 'down', 'left', 'right').
        """
        coordinates = [i * self.box_size for i in coordinates]
        self.snakes.append(
            goofy_Snakes(self.child_window,color,coordinates,lenght,direction,self.box_size)
        )
    
    def add_food(self, color:str, food_type="oval",randome_color=False):
        """Add a food item to the game screen.

        Args:
            color (str): The color of the food item.
            food_type (str): The type of food item ('oval' or 'rectangle', default is 'oval').
            random_color (bool): Whether to randomize the color of the food item (default is False).
        """
        self.food_type=food_type
        self.random_color=randome_color
        self.food=Food(self.child_window, self.box_size, color, self.game_width, self.game_height, food_type)
        
    def start_animation(self):
        """Start the animation loop for moving snakes and updating the game state."""
        for snake in self.snakes:
            snake.move_the_snakes()
            x,y= snake.coordinates
            foodx,foody=self.food.x,self.food.y
            if x == foodx and y == foody:
                if self.random_color:
                    self.food.color = choice(("blue","yellow","red","pink"))
                self.food.new_food(self.food_type)
        self.animation_after_ids=self.child_window.after(self.speed,self.start_animation)
    
    def stop_animation(self):
        """Stop the animation loop."""
        self.child_window.after_cancel(self.animation_after_ids)
    
    def add_button(self,*args):
        """Add button widgets to the game screen.

        Args:
            *buttons: Button widgets to be added to the game screen.
        """
        num = self.box_size-(self.box_size*2)
        for button in args:
            self.child_window.create_window(self.game_width//2,self.game_height//2+num,window=button)
            num += self.box_size
        
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
        button1 =Button(self.optionscreen.child_window, text="Restart", command=button_click,width=10,bg=BACKGROUND_COLOR,fg='white',font=("Press Start 2P",10),relief="flat")
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
#methodes and functiones :0 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! level1
def button_click():
    inisial_window.stop_animation()
    inisial_window.child_window.pack_forget()
    game_window.add_to_window()
    game_window.START()
    print("anything")


#Game_variables!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! level2
GAME_WIDTH = 720
GAME_HEIGHT = 360
title_of_game = "snack suffaries"
BACKGROUND_COLOR = "#050B2B"
nevigation_color = "white"
nev_text_color = "black"
home_screen_box_size = 40
home_screen_speed = 100
game_box_size = 30
game_speed = 120

#root windows!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! level3
root = Tk()
root.geometry(F"{GAME_WIDTH}x{GAME_HEIGHT}")
root.title(title_of_game)

#home_screen_window!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! levle4
inisial_window = inisial_screens(root,BACKGROUND_COLOR,GAME_WIDTH,home_screen_box_size,GAME_HEIGHT,home_screen_speed,True)
inisial_window.add_snakes("red",(0,0),5,"down")
inisial_window.add_snakes("yellow",(2,1),3,"down")
inisial_window.add_snakes("pink",(4,2),8,"left")
inisial_window.add_snakes("grey",(1,3),3,"right")
inisial_window.add_snakes("blue",(4,4),4,"up")
inisial_window.add_food("red","any",True)
inisial_window.start_animation()

lable =Label(inisial_window.child_window,text="Sneck suffarie :0",bg=BACKGROUND_COLOR,fg="White",font=("Press Start 2P",30),relief="flat")
button =Button(inisial_window.child_window, text="Play", command=button_click,width=10,bg=BACKGROUND_COLOR,fg='white',font=("Press Start 2P",10),relief="groove")
button1 =Button(inisial_window.child_window, text="Settings", command=button_click,width=10,bg=BACKGROUND_COLOR,fg='white',font=("Press Start 2P",10),relief="groove")
button2 =Button(inisial_window.child_window, text="about me", command=button_click,width=10,bg=BACKGROUND_COLOR,fg='white',font=("Press Start 2P",10),relief="groove")
inisial_window.add_button(lable,button,button1,button2)

#Game_window !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! level5
game_window = Game_screen(root,GAME_WIDTH,GAME_HEIGHT,game_box_size)
game_window._bind_key()




#packing_root!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! level2
root.update()
root.mainloop()