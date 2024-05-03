from tkinter import Canvas
from random import choice
from game_idles import Food,goofy_Snakes


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
        self.Windows_list = []
        self.animation_after_ids=None
    
    
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
        
    def add_button(self,*args):
        """Add button widgets to the game screen.

        Args:
            *buttons: Button widgets to be added to the game screen.
        """
        self.Windows_list = args
        
        num = self.box_size-(self.box_size*2)
        for button in args:
            self.child_window.create_window(self.game_width//2,self.game_height//2+num,window=button)
            num += self.box_size
        
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
        if self.animation_after_ids:
            self.child_window.after_cancel(self.animation_after_ids)
        
    def add_to_master(self):
        '''add to the master'''
        self.child_window.pack()
        
    def remove_from_master(self):
        self.stop_animation()
        self.child_window.pack_forget()