from tkinter import Canvas
from random import randint,choice

# notes: -
# 1. we are using canvas height or width to keep track of height and width 
#    we not taking it as argumrnt :0

def validate_cordinates(cords ,box_size:int) -> tuple[int:int]:
    """
    Snap coordinates to the nearest lower multiple of box size.

    Parameters:
    cords (tuple): A tuple (x, y) representing the coordinates.
    box_size (int): The size of the box grid.

    Returns:
    tuple: Adjusted coordinates (x, y) snapped to the nearest lower multiple of box_size.
    """
    x , y = cords
    
    x -= x % box_size
    y -= y % box_size
    
    return (x , y)


class Snake:
    """
    Represents a snake in the game.

    Attributes:
        canvas (Canvas): The canvas on which the snake will be drawn.
        length (int): The initial length of the snake.
        coordinates (tuple): The initial coordinates of the snake.
        color (str): The color of the snake.
        box_size (int): The size of each box representing a segment of the snake.
        snake_coordinates (list): List of tuples representing the coordinates of each segment.
        snake_body (list): List of segment IDs on the canvas.

    Methods:
        __init__(canvas, length, box_size, color, coordinates): Initialize a new Snake object.
        _create_inisial_snake(): Create the snake on the canvas.
        _create_body(x, y): Create a segment of the snake.
        delete_all_snake(): Delete all snake segments from the canvas.
        _update_snake_cords(snake_body, x, y): Update the coordinates of a snake segment.
        update_cords(new_box_size): Update the coordinates of the snake segments based on the new box size.
        move_snake(x, y, remove): Move the snake to the new coordinates.
        get_to_inisial_posision(): Reset the snake to its initial position.
        update_color(color): Update the color of the snake.
        update_size(box_size): Update the size of each box segment of the snake.
    """
    def __init__(self, canvas:Canvas, lenght:int, box_size:int, color:str, coordinates:tuple) -> None :
        """
        Initialize the Snake object on the canvas.

        Args:
            canvas (Canvas): The canvas on which the snake will be drawn.
            length (int): The initial length of the snake.
            box_size (int): The size of each box representing a segment of the snake.
            color (str): The color of the snake.
            coordinates (tuple): The initial coordinates of the snake.
        """
        self.box_size = box_size
        self.color = color
        self.canvas = canvas
        self.lenght=lenght
        self.coordinates = validate_cordinates(coordinates, self.box_size)
        self._create_inisial_snake()
        
    def _create_inisial_snake(self)-> None:
        """
        Create the snake on the canvas.
        """
        self.snake_coordinates=[self.coordinates] * self.lenght
        self.snake_body=[self._create_body(x , y) for x , y in self.snake_coordinates]
        
    def _create_body(self , x:int , y:int)-> int:
        """
        Create a segment of the snake.

        Args:
            x (int): The x-coordinate of the segment.
            y (int): The y-coordinate of the segment.

        Returns:
            int: The id of the created segment on the canvas.
        """
        square = self.canvas.create_rectangle(
            x , y , x + self.box_size , y + self.box_size, fill=self.color
        )
        return square

    def delete_all_snake(self) -> None:
        """
        Delete all snake segments from the canvas
        """
        for body in self.snake_body:
            self.canvas.delete(body)
            
        self.snake_coordinates = []
    
    def _update_snake_cords(self ,snake_body:int, x:int, y:int) -> None:
        """
        Update the coordinates of a snake segment.

        Args:
            snake_body (int): The id of the snake segment.
            x (int): The new x-coordinate.
            y (int): The new y-coordinate.
        """
        self.canvas.coords(snake_body, x, y, x + self.box_size, y + self.box_size)
    
    def update_cords(self, new_box_size:int) -> None:
        """
        Update the coordinates of the snake segments based on the new box size.

        This method adjusts the positions of the snake's segments to fit within the new box size while maintaining their
        relative positions. It calculates the increment (positive or negative) based on the difference between the new 
        and old box sizes and applies this increment to each segment's coordinates accordingly.

        Args:
            new_box_size (int): The new size of each box segment of the snake.
        """
        increment = new_box_size - self.box_size
        initial_coords = self.snake_coordinates[0] # Starting point of the snake
        x_increase = 0
        y_increase = 0
        
        for num in range(1, len(self.snake_coordinates)):
            
            oldx ,oldy = self.snake_coordinates[num-1]
            x , y = self.snake_coordinates[num]
            
            if x > initial_coords[0]:
                value = (x + (increment + x_increase) , oldy)
                x_increase += increment
            elif x < initial_coords[0]:
                value = (x - (increment - x_increase) , oldy)
                x_increase -= increment
            elif y > initial_coords[1]:
                value = (oldx , y + (increment + y_increase))
                y_increase += increment
            elif y < initial_coords[1]:
                value = (oldx , y - (increment - y_increase))
                y_increase -= increment
            
            self.snake_coordinates[num] = value
            initial_coords = (x , y)
        
        self.snake_coordinates = [validate_cordinates(cords , new_box_size) for cords in self.snake_coordinates]
        
    def move_snake(self , x:int , y:int, remove:bool)-> None:
        """
        Move the snake to the new coordinates.

        Args:
            x (int): The x-coordinate of the new position.
            y (int): The y-coordinate of the new position.
            remove (bool): Whether to remove the last segment of the snake.
        """
        self.snake_coordinates.insert(0, (x, y))
        
        if remove:
            self.snake_coordinates.pop()
            self._update_snake_cords(self.snake_body[-1], x, y)
            self.snake_body.insert(0, self.snake_body.pop())
        else:
            self.snake_body.insert(0, self._create_body(x , y))
        
    def get_to_inisial_posision(self) -> None:
        """
        Reset the snake to its initial position.
        """
        self.coordinates = (0 , 0)
        self.delete_all_snake()
        self._create_inisial_snake()
        
    def update_color(self, color:str) -> None:
        """Update the color of the snake.

        Args:
            color (str): The new color of the snake.
        """
        self.color = color
        for body in self.snake_body:
            self.canvas.itemconfig(body, fill = self.color)
            
    def update_size(self, box_size) -> None:
        """Update the size of the snake segments.

        Args:
            box_size (int): The new size of each box segment of the snake.
        """
        self.update_cords(box_size)
        self.box_size = box_size
        
        for num in range(len(self.snake_coordinates)):
            x, y = self.snake_coordinates[num]
            body = self.snake_body[num]
            self._update_snake_cords(body , x , y)
        
        
    
    
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
    def __init__(
        self,
        canvas : Canvas,
        color : str,
        box_size : int,
        game_width : int,
        game_height : int,
        )-> None:
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
        self.new_food()
        
    def _create_food_oval(self) -> None:
        """Create an oval-shaped food item."""
        
        iteme_id = self.canvas.create_oval(
            self.x , self.y, #x1 and y1
            self.x + self.box_size, #x2
            self.y + self.box_size, #y2
            fill=self.color #color
        )
        self.food = iteme_id
    
    def _delete_food(self) -> None:
        """Delete the current food item from the canvas."""
        self.canvas.delete(self.food)
        
    def new_coordinates(self) -> None:
        """Generate new random coordinates for the food item."""
        
        # The approach divides the screen into a grid of cells, where each cell represents a possible position for the food.
        # The grid is defined by the box_size, which determines the size of each cell.
        # To select a random cell, we choose a random integer index along the x-axis (vertical lines) and y-axis (horizontal lines).
        # We then multiply these indices by the box_size to obtain the exact coordinates within the canvas where the food can be placed.
        
        self.x = randint(0, (self.game_width // self.box_size)-1)* self.box_size
        self.y =  randint(0, (self.game_height // self.box_size)-1)* self.box_size
    
    def new_food(self, cordinates:list|tuple|None = None):
        """
        Create a new food item of the specified type and optionally at specified coordinates.

        Args:
            coordinates (list or tuple or None): Optional coordinates to place the food item.
                If provided, the food item will be placed at these coordinates.
        """
        print(self.food)
        if cordinates is not None:
            for x , y  in cordinates:
                if self.x != x and self.y != y:
                    self.new_coordinates()
                    break
        else:
            self.new_coordinates()
        
        if self.food:
            self.move_resize_food()
        else:
            self._create_food_oval()
        
    
    def move_resize_food(self) -> None:
        self.canvas.coords(
            self.food, self.x, self.y, self.x + self.box_size, self.y + self.box_size 
        )
        
    def update_color(self , color:str):
        """Update the color of the Food.

        Args:
            color (str): The new color of the Food.
        """
        self.color = color
        self.canvas.itemconfig(self.food, fill = self.color)
    
    def update_size(self , box_size:int) -> None:
        self.box_size = box_size
        
        self.x -= self.x % self.box_size
        self.y -= self.y % self.box_size
        
        self.canvas.coords(
            self.food, self.x, self.y, self.x + self.box_size, self.y + self.box_size 
        )
         
        
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
    def __init__(
        self,
        canvas : Canvas,
        cordnites : tuple,
        box_size : int,
        color : str,
        inisial_heart = 1
        ) -> None:
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
        self.limit = None
        self.inisial_heart = inisial_heart
        self.calulating_diameters()
        
        self.hearts_list = []
        for _ in range(self.inisial_heart):
            self.add_one_heart()
    
    def calulating_diameters(self):
        '''calculate the diameters'''
        self.distance = self.box_size // 4
    
    def add_one_heart(self):
        """
        Add one heart to the canvas.

        If the limit is set and the number of hearts exceeds the limit, no heart will be added.

        Returns:
            None
        """
        if self.limit and len(self.hearts_list)>= self.limit:
            return None
        self.heart()
        self.cordinates = (self.cordinates[0]-self.box_size-self.distance , self.cordinates[1])
        
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
        
    def remove_all_heart(self):
        """
        remove all the heart left on the canvas.
        
        returns:
            None
        """
        if self.hearts_list == []:
            return None
        
        for _ in range(len(self.hearts_list)):
            self.remmove_heart()
            
    def add_heart_in_range(self,num = 0):
        '''
        add hearts in a range given by num or the value of 
        num is by default set to be num = self.inisial_heart
        '''
        if not num:
            num = self.inisial_heart
        
        for _ in range(num):
            self.add_one_heart()
    
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
    
    def update_color(self,color:str):
        """Update the color of the Heart.

        Args:
            color (str): The new color of the Heart.
        """
        self.color = color
        
        for hearts in self.hearts_list:
            self.canvas.itemconfig(hearts[0],fill = self.color)
            self.canvas.itemconfig(hearts[1],fill = self.color)
            self.canvas.itemconfig(hearts[2],fill = self.color)
    
    def update_size(self , box_size:int) -> None:
        self.box_size = box_size
        
        self.calulating_diameters()
        
        heart = len(self.hearts_list)
        
        self.remove_all_heart()
        self.add_heart_in_range(heart)
        
        

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
    
    def __init__(
        self,
        master : Canvas,
        color : str,
        coordinates : tuple,
        lenght : int,
        inisial_direction : str,
        box_size : int
        ) -> None:
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
        
        self.snake = Snake(
            canvas = self.master,
            lenght = self.lenght,
            color  = self.color,
            box_size = self.box_size,
            coordinates = self.coordinates
        )

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
        y = canvas_width if y < 0 else 0 if y > canvas_height else y
        
        self.coordinates = (x,y)
    
    def move_the_snakes(self):
        """Move the snake to the new coordinates."""
        self.calculate_new_coordinates()
        x , y = self.coordinates
        self.snake.move_snake(x,y,True)
        
    def update_color(self , color):
        """Update the color of the goofy snake.

        Args:
            color (str): The new color of the goofy snake.
        """
        self.color = color
        self.snake.update_color(self.color)
        
    def update_size(self , box_size):
        self.box_size = box_size
        self.snake.update_size(self.box_size)