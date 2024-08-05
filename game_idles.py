from tkinter import Canvas
from random import randint,choice
from helper import *

# notes: -
# 1. Every game class contains an "initial_posision" initialize method, and in each
#    class, the __init__ method has an argument initialize: bool which is set to True. 
#    Setting it to False will not initialize the initial method.
#
# 2. We are using canvas height or width to keep track of height and width; 
#    we are not taking it as an argument.
#
# 3. Whenever taking coordinates as an argument, use the validate_coordinate 
#    method to validate the coordinates by providing the correct box_size.
#
# 4  Each method should contain update_color(color:str), update_size(box_size:int),
#    and delete_all(hide:bool = True) methods, and the names should also be the same.
#      a. update_color(color:str) : update item color takes new color as argument
#      b. update_size(box_size:int): update item size takes new box_size as argument
#      c. delete_all(hide:bool = True):if hide set to false then delete all shape drawn
#                                      by the method else hide all shape drawn by method.
# 
# 5. Each method should have "return_id()" method which don't take any arguemnt
#    return the main canvas drawn obj id which will be int
#
# 6. Each class have a avilable variable or arttibute that will say if item is currently
#    visible or not


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
        _create_initial_snake(): Create the inisial snake on the canvas.
        _create_body(x, y): Create a segment of the snake.
        _update_snake_coords(new_box_size): Update the coordinates of the snake segments based on the new box size.
        _update_coords(snake_body, x, y): Update the coordinates of a snake segment.
        delete_all(): Delete all snake segments from the canvas.
        move_snake(x, y, remove): Move the snake to the new coordinates.
        initial_posision(): Reset the snake to its initial position.
        update_color(color): Update the color of the snake.
        update_size(box_size): Update the size of each box segment of the snake.
    """
    def __init__(self, canvas:Canvas, lenght:int, box_size:int, color:str, coordinates:tuple, initialize:bool = True) -> None:
        """
        Initialize the Snake object on the canvas.

        Args:
            canvas (Canvas): The canvas on which the snake will be drawn.
            length (int): The initial length of the snake.
            box_size (int): The size of each box representing a segment of the snake.
            color (str): The color of the snake.
            coordinates (tuple): The initial coordinates of the snake.
            initialize (bool): weather to draw snake on canvas or not the initial snake
        """
        self.box_size = box_size
        self.color = color
        self.canvas = canvas
        self.lenght = lenght
        self.coordinates = validate_coordinates(coordinates, self.box_size)
        
        if initialize:
            self._create_initial_snake()
        
    def _create_initial_snake(self) -> None:
        """
        create the snake on the canvas.
        """
        self.snake_coordinates = [self.coordinates] * self.lenght
        self.snake_body = [self._create_body(x , y) for x , y in self.snake_coordinates]
    
    def _create_body(self, x:int , y:int) -> int:
        """
        create a segment of the snake

        Args:
            x (int): The x-coordinate of the segment.
            y (int): The y-coordinate of the segment.

        Returns:
            int: The id of the created segment.
        """
        return self.canvas.create_rectangle(
            x, y, x + self.box_size, y + self.box_size, fill = self.color
        )
    
    def _update_snake_coords(self, snake_body:int, x:int, y:int) -> None:
        """
        Update the coordinates of a snake segment.

        Args:
            snake_body (int): The id of the snake segment
            x (int): the new x-coordinate.
            y (int): the new y-coordinate.
        """
        self.canvas.coords(snake_body, x, y, x + self.box_size, y + self.box_size)
    
    def _update_coords(self, new_box_size:int) -> None:
        """
        Update the coordinates of the snake segments based on the new box size.

        This method adjusts the positions of the snake's segments to fit within the new box size while maintaining their
        relative positions. It calculates the increment (positive or negative) based on the difference between the new 
        and old box sizes and applies this increment to each segment's coordinates accordingly.

        Args:
            new_box_size (int): The new size of each box segment of the snake.
            
        Time Complexity: O(n), where n is the number of snake segments.
        Space Complexity: O(n), where n is the number of snake segments.
        """
        increment = new_box_size - self.box_size
        initial_coords = self.snake_coordinates[0] #starting point of the snake
        x_increase = 0
        y_increase = 0
        
        for num in range(1, len(self.snake_coordinates)):
            
            oldx , oldy = self.snake_coordinates[num-1]
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
            
            self.snake_coordinates[num] = validate_coordinates(value, new_box_size)
            initial_coords = (x , y)
        
    def move_snake(self, x:int, y:int, remove:bool = False) -> None:
        """
        move the snake to the new coordinates.

        Args:
            x (int): The x-coordinates of the new position.
            y (int): The y-coordinates of the new position.
            remove (bool): whether to remove the last segment of the snake. default False
        """
        # validate the x,y coords and insert new coords to 0 possition (x,y)
        x , y = validate_coordinates((x , y), self.box_size)
        self.snake_coordinates.insert(0 , (x , y))
        
        # if remove then last snake_coords will removed and last snake body modified 
        # to new possistion by given x,y coords and inserted to 0 possistion of snake_body
        # if not remove then snake body created and inserted it to 0 possition by given (x,y)
        if remove:
            self.snake_coordinates.pop()
            self._update_snake_coords(self.snake_body[-1], x , y)
            self.snake_body.insert(0, self.snake_body.pop())
        else:
            self.snake_body.insert(0, self._create_body(x , y))
    
    def return_id(self) -> list[int,int,int]:
        """
        Return the snake body as a list of tuples with coordinates.
        """
        return self.snake_body
        
    def delete_all(self) -> None:
        """
        Delete all snake segment from the canvas
        """
        for body in self.snake_body:
            self.canvas.delete(body)
            
        self.snake_coordinates = []
    
    def initial_posision(self) -> None:
        """
        Reset the snake to its initial position.
        """
        self.delete_all()
        self._create_initial_snake()
        
    def update_color(self, color:str) -> None:
        """
        update the color of the snake.

        Args:
            color (str): The new color of the snake
        """
        self.color = color
        
        #updating color for each segments.
        for body in self.snake_body:
            self.canvas.itemconfig(body, fill = self.color)
        
    def update_size(self, box_size:int) -> None:
        """
        update the size of the snake segments.

        Args:
            box_size (int): The new size of each box segment.
        """
        #updating the coordinates
        self._update_coords(box_size)
        self.box_size = box_size
        
        #updating body segment with new coords
        for num in range(len(self.snake_coordinates)):
            x , y = self.snake_coordinates[num]
            body = self.snake_body[num]
            self._update_snake_coords(body , x, y)

class Food:
    """
    A class to represent food items in a graphical canvas.

    Attributes:
        canvas (Canvas): The canvas on which to draw the food.
        box_size (int): The size of the food box.
        color (str): The color of the food.
        food (int): The ID of the food item on the canvas.
        coords (tuple[int, int]): The coordinates of the food item.
        canvas_width (int): The width of the canvas.
        canvas_height (int): The height of the canvas.
        avialable (bool): saying if the item is visually appeared in the canvas or not

    Methods:
        __init__(canvas, color, box_size): Initialize a new Food object.
        _calculate_dimension(): Calculate and store the width and height of the canvas.
        _create_food_oval(coords): Create an oval-shaped food item on the canvas.
        _move_resize_food(coords): Update the position and size of the food item on the canvas.
        new_food(coordinates): Create a new food item at optionally specified coordinates.
        delete_all(): Delete the current food item from the canvas.
        initial_posision(): Initialize the food position to the default.
        update_color(color): Update the color of the Food.
        update_size(box_size): Update the size of the Food.
        return_id(): return the current food item id
    """
    def __init__(self, canvas:Canvas, color:str, box_size:int, initialize:bool = True) -> None:
        """
        Initialize the Food class.

        Args:
            canvas (Canvas): The canvas on which to draw the food.
            color (str): The color of the food.
            box_size (int): The size of the food box.
            initialize (bool, optional): Whether to initialize the food position. Defaults to True.
        """
        self.canvas = canvas
        self.box_size = box_size
        self.color = color
        
        self.food = None
        self.coords = (0 , 0)
        self.avialable = False
        
        if initialize:
            self.initial_posision()
    
    def _calculate_dimension(self) -> None:
        """
        Calculate and store the width and height of the canvas.
        """
        self.canvas_width = int(self.canvas.cget("width"))
        self.canvas_height = int(self.canvas.cget("height"))
        #calculating grid
        self.__width_grid_size = (self.canvas_width // self.box_size) - 1
        self.__height_grid_size = (self.canvas_height // self.box_size) - 1
    
    def _create_food_oval(self, coords:tuple[int,int]) -> int:
        """
        Create an oval-shaped food item on the canvas.

        Args:
            coords (tuple[int, int]): The coordinates for the food item.
        """
        self.avialable = True
        x , y = self.coords
        
        iteme_id = self.canvas.create_oval(
            x , y, #x1 and y1-
            x + self.box_size, #x2
            y + self.box_size, #y2
            fill = self.color #color
        )
        self.food = iteme_id
        return self.food
    
    def _move_resize_food(self, coords:tuple[int,int], food:int|None = None) -> None:
        """
        Update the position and size of the food item on the canvas.

        Args:
            coords (tuple[int, int]): The coordinates to move the food item to.
        """
        self.avialable = True
        food = self.food if not food else food
        x , y = self.coords
        
        self.canvas.coords(
            food, x, y, x + self.box_size, y + self.box_size 
        )
        self.canvas.itemconfig(self.food, state = "normal")
    
    def delete_all(self, hide:bool = True) -> None:
        """
        Deletes or hide the food shape from the canvas.

        Args:
            hide (bool, optional): if True, hides the food shape or else delete it. Defaults to True.

        Returns:
            None
        """
        self.avialable = False
        
        if self.food is None:
            return None
        
        if hide:
            self.canvas.itemconfig(self.food, state = "hidden")
            return None
    
        self.canvas.delete(self.food)
        self.food = None
    
    def new_food(self, coordinates:list|tuple|None = None) -> None:
        """
        Create a new food item of the specified type and optionally at specified coordinates.

        Args:
            coordinates (list or tuple or None): Optional coordinates to place the food item.
                If provided, the food item will not be placed at these coordinates.
        """
        if coordinates is not None:
            self.coords = generate_non_overlapping_coordinates(
                coordinates = coordinates,
                grid_width = self.__width_grid_size,
                grid_height = self.__height_grid_size,
                box_size = self.box_size
                )
        else:
            self.coords = random_coordinates(
                grid_width = self.__width_grid_size,
                grid_height = self.__height_grid_size,
                box_size = self.box_size
                )
        
        self.coords = validate_coordinates(self.coords, self.box_size)
        
        if self.food:
            self._move_resize_food(self.coords)
        
        else:
            self._create_food_oval(self.coords)
    
    def return_id(self) -> int:
        """
        Return the food id as a int.
        """
        return self.food
    
    def initial_posision(self) -> None:
        """
        Initialize the food position to the default.
        """
        self.coords = (0 , 0)
        self.delete_all()
        self.avialable = True
        self._calculate_dimension()
        self._create_food_oval(self.coords)
    
    def update_color(self, color:str) -> None:
        """Update the color of the Food.

        Args:
            color (str): The new color of the Food.
        """
        self.color = color
        
        if self.food:
            self.canvas.itemconfig(self.food, fill = self.color)
    
    def update_size(self, box_size:int) -> None:
        """
        Update the size of the Food.

        Args:
            box_size (int): The new size of the food box.
        """
        self.box_size = box_size
        self._calculate_dimension()
        self.coords = validate_coordinates(self.coords, self.box_size)
        
        if self.food:
            self._move_resize_food(self.coords)
            
            
class Heart:
    """
    This class helps create hearts, remove hearts, and manipulate heart shapes on a canvas.
    This class will not perform any calculations for coordinates.
    
    Attributes:
        Canvas (Canvas): The canvas where item will be drawn.
        box_size (int): the size of each box or grid size
        color (str): the color of the item
        canvas_width (int): the width of the game area.
        canvas_height (int): The height of the game area.
        hearts (list[int,int,int]): the list containing heart shape id
        coords (tuple[int,int]): the tuple contaiing x1 and y1 coordinates of the item
        avialable (bool): saying if the item is visually appeared in the canvas or not
            
    Methods:
        __init__(canvas, color, box_size, initialize): inisialize new heart obj
        _calculate_dimension():  Calculate width height and more of canvas
        _create_heart_shape(coordinates): create an heart shape on canvas
        _move_resize_heart_shape(coordinates, heart): move or resize the current shape to new possition
        delete_all(hide): delete the items that persent in canvas or hide them
        new_heart(coordinates): create a new heart item on canvas this is main method for it
        return_id(): return the current heart item id
        initial_posision(): take everything back to there inisisal possition
        update_color(): update the color of the heart
        update_size(): update the size of the heart
    """
    def __init__(self, canvas:Canvas, color:str, box_size:int, initialize:bool = True) -> None:
        """
        Initialize the Heart object.

        Args:
            canvas (Canvas): The Canvas on which to draw the heart.
            color (str): Thr color of the Heart.
            box_size (int): The size of the Heart box.
            initialize (bool, optional): Whether to initialize the Heart position. Defaults to True.
        """
        self.canvas = canvas
        self.box_size = box_size
        self.color = color
        
        self.hearts = None
        self.coords = (0 , 0)
        self.avialable = False
        
        if initialize:
            self.initial_posision()
    
    def _calculate_dimension(self) -> None:
        """
        Calculate and store the width and height of the canvas.
        """
        self.canvas_width = int(self.canvas.cget("width"))
        self.canvas_height = int(self.canvas.cget("height"))
        # calculating grid
        self.__width_grid_size = (self.canvas_width // self.box_size) - 1
        self.__height_grid_size = (self.canvas_height // self.box_size) - 1
    
    def _create_heart_shape(self, coordinates:tuple[int,int]) -> tuple[int,int,int]:
        """
        Draws a heart shape on the canvas.

        Args:
            coordinates (tuple[int,int]): The x and y coordinates where the heart will be drawn.

        Returns:
            tuple[int,int,int]: tuple containing heart shapes id size will be 3
        """
        self.avialable = True
        x1 , y1 = coordinates
        x2 , y2 = x1 + self.box_size, y1+ self.box_size
        self.coords = (x1 , y1)
        
        new_x1 = (self.box_size / 2) + x1
        new_y1 = (self.box_size / 2) + y1
        radius = (new_y1 - y1) / 2
        
        first = self.canvas.create_arc(x1, new_y1 - radius, new_x1, new_y1 + radius, fill = self.color, start = 0, extent = 180)
        second = self.canvas.create_arc(new_x1, new_y1 - radius, x2, new_y1 + radius, fill = self.color,start = 0, extent = 180)
        third = self.canvas.create_polygon(x1, new_y1, x2, new_y1, (x1 + x2) / 2, y2, fill = self.color)
        
        self.hearts = (first, second, third)
        return self.hearts
    
    def _move_resize_heart_shape(self, coordinates:tuple[int,int], heart:tuple|None = None) -> None:
        """
        Move and resizes the heart shape on the canvas.

        Args:
            coordinates (tuple[int,int]): The new x and y coordinates
            heart (tuple | None, optional): this method takes heart items tuple. Defaults to None.
        """
        self.avialable = True
        heart = self.hearts if not heart else heart
        
        x1 , y1 = coordinates
        x2 , y2 = x1 + self.box_size, y1 + self.box_size
        
        new_y1 = (self.box_size / 2) + y1
        new_x1 = (self.box_size / 2) + x1
        radius = (new_y1 - y1) / 2
        self.coords = (x1 , y1)
        
        self.canvas.coords(
            heart[0], x1, new_y1 - radius, new_x1, new_y1 + radius
        )
        self.canvas.coords(
            heart[1], new_x1, new_y1 - radius, x2, new_y1 + radius
        )
        self.canvas.coords(
            heart[2], x1, new_y1, x2, new_y1, (x1 + x2) / 2, y2
        )
        for body in heart:
            self.canvas.itemconfig(body, state = "normal")
    
    def delete_all(self, hide:bool = True) -> None:
        """
        Deletes or hides the heart shape from the canvas.

        Args:
            hide (bool): If True, hides the heart shape instead of deleting it.

        Returns:
            None
        """
        self.avialable = False
        
        if self.hearts is None:
            return None
        
        if hide:
            for heart in self.hearts:
                self.canvas.itemconfig(heart, state = "hidden")
            return None
        
        for heart in self.hearts:
            self.canvas.delete(heart)
        
        self.hearts = None
    
    def new_heart(self, coordinates:list|tuple|None = None) -> None:
        """
        Creates a new heart shape on the canvas optionally at specified coordinates.

        Args:
            coordinates (list or tuple or None): Optional coordinates to place the hearts item.
                If provided, the hearts item will not be placed at these coordinates.

        Returns:
            None
        """
        if coordinates is not None:
            self.coords = generate_non_overlapping_coordinates(
                coordinates = coordinates,
                grid_width = self.__width_grid_size,
                grid_height = self.__height_grid_size,
                box_size = self.box_size
            )
        else:
            self.coords = random_coordinates(
                grid_width = self.__width_grid_size,
                grid_height = self.__height_grid_size,
                box_size = self.box_size
            )
        #validating coordinates
        self.coords = validate_coordinates(self.coords, self.box_size)
        
        if self.hearts:
            self._move_resize_heart_shape(self.coords)
        
        else:
            self._create_heart_shape(self.coords)
    
    def return_id(self) -> tuple[int,int,int]:
        """
        Return the heart id as a int.
        """
        return self.hearts
        
    def initial_posision(self) -> None:
        """
        Initialize the heart position to the default.
        """
        self.coords = (0 , 0)
        self.delete_all()
        self.avialable = True
        self._calculate_dimension()
        self._create_heart_shape(self.coords)
    
    def update_color(self, color:str) -> None:
        """
        Change the color of the heart shape.

        Args:
            color (str): The new color of the heart shape.
        """
        self.color = color
        
        if self.hearts is None:
            return None
        
        for heart in self.hearts:
            self.canvas.itemconfig(heart, fill = self.color)
    
    def update_size(self, box_size:int) -> None:
        """
        change the size of the heart shape.

        Args:
            box_size (int): The new size of the heart shape.
        """
        self.box_size = box_size
        self._calculate_dimension()
        self.coords = validate_coordinates(self.coords,self.box_size)
        
        if self.hearts:
            self._move_resize_heart_shape(self.coords)



class Coin:
    """
    Represents a coin object that can be drawn on a canvas.
    
    Attributes:
        Canvas (Canvas): The canvas where item will be drawn.
        box_size (int): the size of each box or grid size
        color (str): the color of the item (hax)
        sec_color(str): the color of the 2nd circule (hax)
        canvas_width (int): the width of the game area.
        canvas_height (int): The height of the game area.
        coins (list[int,int,int]): the list containing coin shape id
        coords (tuple[int,int]): the tuple contaiing x1 and y1 coordinates of the item
        avialable (bool): saying if the item is visually appeared in the canvas or not
            
    Methods:
        __init__(canvas, color, box_size, initialize): inisialize new coin obj
        _calculate_dimension():  Calculate width height and more of canvas
        _create_coin_shape(coordinates): create an coin shape on canvas
        _move_resize_coin_shape(coordinates, coin): move or resize the current shape to new possition
        delete_all(hide): delete the items that persent in canvas or hide them
        new_coin(coordinates): create a new coin item on canvas this is main method for it
        return_id(): return the current coin item id
        initial_posision(): take everything back to there inisisal possition
        update_color(): update the color of the coin
        update_size(): update the size of the coin
    """
    def __init__(self, canvas:Canvas, color:str, box_size:int, initialize:bool = True) -> None:
        """
        Initialize the Coin object.

        Args:
            canvas (Canvas): The Canvas on which to draw the Coin.
            color (str): Thr color of the Coin should be hax color
            box_size (int): The size of the grid .
            initialize (bool, optional): Whether to initialize the coin position. Defaults to True.
        """
        self.canvas = canvas
        self.box_size = box_size
        self.color = color
        
        self.coins = None
        self.coords = (0 , 0)
        self.avialable = False
        self.sec_color = darken_hex_color(self.color)
        
        if initialize:
            self.initial_posision()
    
    def _calculate_dimension(self) -> None:
        """
        Calculate and store the width and height of the canvas.
        """
        self.canvas_width = int(self.canvas.cget("width"))
        self.canvas_height = int(self.canvas.cget("height"))
        # calculating grid
        self.__width_grid_size = (self.canvas_width // self.box_size) - 1
        self.__height_grid_size = (self.canvas_height // self.box_size) - 1
    
    def _create_coin_shape(self, coordinates:tuple[int,int]) -> tuple[int,int,int]:
        """
        Creates a new coin at the specified coordinates.
        
        Args:
            coordinates (tuple[int,int]): The x and y coordinates where the coin will be drawn.

        Returns:
            tuple[int,int,int]: tuple containing coin shapes id size will be 3
        """
        self.avialable = True
        x1 , y1 = coordinates
        self.coords = coordinates
        
        #innerx1 and box_size
        innerx1 = (self.box_size // 10) + x1
        innery1 = (self.box_size // 10) + y1
        inner_boxsize = self.box_size - (self.box_size // 10) * 2
        #inner_smile_coords
        middlex1 = innerx1 + (inner_boxsize // 2)
        middley1 = innery1 + (inner_boxsize // 2)
        #text_size = pixels * (72 / dpi(96) == 0.75)
        text_size = inner_boxsize // 5
        text_size = int(text_size * 7.5) // 2
        
        first = self.canvas.create_oval(x1, y1, x1+self.box_size, y1+self.box_size, fill=self.color, outline="black")
        secoend = self.canvas.create_oval(innerx1, innery1, innerx1+inner_boxsize, innery1+inner_boxsize, outline="black",fill=self.sec_color)
        third = self.canvas.create_text(middlex1, middley1, text="!", justify="center",fill="black",font=("Arial",text_size,"bold"))
        
        self.coins = (first, secoend, third)
        return self.coins
    
    def _move_resize_coin_shape(self, coordinates:tuple[int,int], coin:tuple|None = None) -> None:
        """
        Moves and resizes the coin shape to the specified coordinates.

        Args:
            coordinates (tuple[int,int]): The new x and y coordinates
            coin (tuple | None, optional): this method takes coin items tuple. Defaults to None.
        """
        self.avialable = True
        coin = self.coins if not coin else coin
        self.coords = coordinates
        x1 , y1 = coordinates
        
        #innerx1 and box_szie
        innerx1 = (self.box_size // 10) + x1
        innery1 = (self.box_size // 10) + y1
        inner_boxsize = self.box_size - (self.box_size // 10) * 2
        #inner_smile_cords
        middlex1 = innerx1 + (inner_boxsize // 2)
        middley1 = innery1 + (inner_boxsize // 2)
        #text_size = pixels * (72 / dpi(96))==0.75
        text_size = inner_boxsize // 5
        text_size = int(text_size * 7.5) // 2
        
        self.canvas.coords(
            coin[0], x1, y1, x1 + self.box_size, y1 + self.box_size
        )
        self.canvas.coords(
            coin[1], innerx1, innery1, innerx1 + inner_boxsize, innery1 + inner_boxsize
        )
        self.canvas.coords(
            coin[2], middlex1 , middley1
        )
        
        self.canvas.itemconfig(coin[0], state = "normal")
        self.canvas.itemconfig(coin[1], state = "normal")
        self.canvas.itemconfig(coin[2], state = "normal", font = ("Arial",text_size,"bold"))
    
    def delete_all(self, hide:bool = True) -> None:
        """
        Deletes or hides the coin shape from the canvas.

        Args:
            hide (bool): If True, hides the coin shape instead of deleting it.
        """
        self.avialable = False
        
        if self.coins is None:
            return None
        
        if hide:
            for coin in self.coins:
                self.canvas.itemconfig(coin, state = "hidden")
            return None
        
        for coin in self.coins:
            self.canvas.delete(coin)
        
        self.coins = None
    
    def new_coin(self, coordinates:list|tuple|None = None) -> None:
        """
        Creates a new coin or moves an existing one to the specified coordinates.

        Args:
            coordinates (list or tuple or None): Optional coordinates to not place the coin item.
                If provided, the coin item will not be placed at these coordinates.

        """
        if coordinates is not None:
            self.coords = generate_non_overlapping_coordinates(
                coordinates = coordinates,
                grid_width = self.__width_grid_size,
                grid_height = self.__height_grid_size,
                box_size = self.box_size
            )
        else:
            self.coords = random_coordinates(
                grid_width = self.__width_grid_size,
                grid_height = self.__height_grid_size,
                box_size = self.box_size
            )
        #validating coordinates
        self.coords = validate_coordinates(self.coords, self.box_size)
        
        if self.coins:
            self._move_resize_coin_shape(self.coords)
        
        else:
            self._create_coin_shape(self.coords)
    
    def return_id(self) -> tuple[int,int,int]:
        """
        Return the coin id as a int.
        """
        return self.coins
        
    def initial_posision(self) -> None:
        """
        Initialize the coin position to the default.
        """
        self.coords = (0 , 0)
        self.delete_all()
        self.avialable = True
        self._calculate_dimension()
        self._create_coin_shape(self.coords)
    
    def update_color(self, color:str) -> None:
        """
        Change the color of the coin shape.

        Args:
            color (str): The new color of the coin shape.
        """
        self.color = color
        self.sec_color = darken_hex_color(self.color)
        
        if self.coins is None:
            return None
        
        self.canvas.itemconfig(self.coins[0], fill = self.color)
        self.canvas.itemconfig(self.coins[1], fill = self.sec_color)
    
    def update_size(self, box_size:int) -> None:
        """
        Changes the size of the coin.

        Args:
            box_size (int): The new size of the grid.
        """
        self.box_size = box_size
        self._calculate_dimension()
        self.coords = validate_coordinates(self.coords, self.box_size)
        
        if self.coins:
            self._move_resize_coin_shape(self.coords)


class Heart_NEV:
    """
    Represents a heart object that can be drawn on a canvas.
    
    Attributes:
        Canvas (Canvas): The canvas where item will be drawn.
        color (str): the color of the item (hax)
        initial_heart(int): the size of the heart to draww inisisaly
        heart_list:tuple[tuple[int,int,int]....]: heart list contain heart ids
        limit(int) : the limit size of the heart that can be drawn in nevigation
        heart(int): the heart object with all fuction to manage heart
        box_size (int): the box_size of heart 
        distance (int): the distance between each heart
        canvas_height (int): The height of the game area.
        coins (list[int,int,int]): the list containing coin shape id
        coords (tuple[int,int]): the tuple contaiing x1 and y1 coordinates of the item
        avialable (bool): saying if the item is visually appeared in the canvas or not
            
    Methods:
        __init__(canvas, color, box_size, initialize): inisialize new heart obj
        _calculate_dimension():  Calculate width height and more of canvas
        __update_coords(update): update the coords by given parameter (ih,iv,dh,dv)
        remove_one_heart(): Remove the last heart from the canvas.
        add_one_heart(check): Add one heart to the canvas.
        add_heart_in_range(range_int): Add hearts to the canvas within a specified range.
        delete_all(hide): delete the items that persent in canvas or hide them
        new_heart(coordinates): create a new heart item on canvas this is main method for it
        return_id(): return the current heart id
        initial_posision(): take everything back to there inisisal possition
        update_color(): update the color of the heart
        update_size(): update the size of the heart
    """
    def __init__(self, canvas:Canvas, color:str, initial_heart:int = 1, limit:int = 5, initialize:bool = True) -> None:
        """
        Initialize the Heart_NEV object.

        Args:
            canvas (Canvas): The canvas on which the heart will be drawn.
            color (str): The color of the heart. should be hax color
            initial_heart (int, optional): The number of hearts to initialize. Defaults to 1.
            limit(int, optional): the number after heart wont add
            initialize (bool, optional): Whether to initialize the coin position. Defaults to True.
        """
        self.canvas = canvas
        self.color = color
        self.initial_heart = initial_heart
        
        self._calculate_dimension()
        self.limit = limit
        self.heart_list = []
        self.heart = Heart(self.canvas, self.color, self.box_size, False)
        
        if initialize:
            self.initial_posision()
    
    def __update_coords(self, update:str) -> None:
        """
        Update the coords under given update parameters.

        Args:
            update (str): Update coords on bases parameter (ih, iv, dh, dv)
            
        Note:
            ih : increase coords horizontally
            iv : increase coords vertically
            dh : decrease coords horizontally
            dv : decrease coords vertically
        """
        update = update.lower()
        if update == "ih":
            self.coords = (self.coords[0] - self.box_size - self.distance, self.coords[1])
        elif update == "iv":
            self.coords = (self.coords[0], self.coords[1] - self.box_size - self.distance)
        elif update == "dh":
            self.coords = (self.coords[0] + self.box_size + self.distance, self.coords[1])
        elif update == "dv":
            self.coords = (self.coords[0], self.coords[1] + self.box_size + self.distance)
        else:
            raise ValueError(f"Unexpected update parameter: {update}")
    
    def _calculate_dimension(self) -> None:
        """
        Calculate and store the width and height of the canvas.
        """
        canvas_width = int(self.canvas.cget("width"))
        canvas_height = int(self.canvas.cget("height"))
        # calculating grid
         # Calculate padding and box size
        padding = canvas_height // 8
        box_size = padding * 7
        
        # Determine coordinates
        y = padding
        x = canvas_width - box_size
        
        # Set instance variables
        self.box_size = box_size
        self.coords = (x, y)
        self.distance = box_size // 4
            
    def add_one_heart(self , check:bool = True) -> None:
        """
        Add one heart to the canvas.

        Args:
            check (bool, optional): If True, check if the limit is set and if the number of hearts exceeds the limit.Defaults to True.
        """
        if check and self.limit and len(self.heart_list) >= self.limit:
            return None
        
        heart = self.heart._create_heart_shape(self.coords)
        
        self.heart_list.append(heart)
        self.__update_coords(update = "ih")
    
    def add_heart_in_range(self, range_int:int = 0) -> None:
        """
        Add hearts to the canvas within a specified range.

        Args:
            range_int (int, optional): The number of hearts to add. Defaults to initial_heart if not provided.
        """
        if not range_int:
            range_int = self.initial_heart
        
        for _ in range(range_int):
            self.add_one_heart(check = False)
    
    def remove_one_heart(self) -> None:
        """
        Remove the last heart from the canvas.
        """
        if self.heart_list == []:
            return None
        
        for ids in self.heart_list.pop():
            self.canvas.delete(ids)
        
        self.__update_coords(update = "dh")
    
    def delete_all(self, hide:bool = True) -> None:
        """
        Deletes or hides the heart shape from the canvas.

        Args:
            hide (bool): Does nothing in this method
        """
        for _ in range(len(self.heart_list)):
            self.remove_one_heart()
    
    def return_id(self) -> tuple[tuple,tuple]:
        """
        Return the heart id as a tuple[tuple[int,int,int],tuple,tuple..].
        """
        return self.heart_list
        
    def initial_posision(self) -> None:
        """
        Initialize the heart position to the default.
        """
        self.delete_all()
        self._calculate_dimension()
        self.add_heart_in_range(self.initial_heart)
    
    def update_color(self, color:str) -> None:
        """
        Update the color of the Heart.

        Args:
            color (str): The new color of the Heart.
        """
        self.color = color
        self.heart.color = color
        
        for heart in self.heart_list:
            for ids in heart:
                self.canvas.itemconfig(ids, fill = self.color)
    
    def update_size(self) -> None:
        """
        Changes the size of the heart.
        """
        self._calculate_dimension()
        self.heart.box_size = self.box_size
        
        for heart in reversed(self.heart_list):
            self.heart._move_resize_heart_shape(self.coords,heart)
            self.__update_coords(update= "ih")

class goofy_Snakes:
    """
    Represents a goofy snake in the game.

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
    
    def __init__(self, master:Canvas, color:str, coordinates:tuple, lenght:int, inisial_direction:str, box_size:int) -> None:
        """
        Initialize a new goofy_Snakes object.

        Args:
            master (Canvas): The canvas on which the snake will be drawn.
            color (str): The color of the snake.
            coordinates (tuple): The initial coordinates of the snake.
            length (int): The initial length of the snake.
            initial_direction (str): The initial direction of the snake.
            box_size (int): The size of each box representing a segment of the snake.
        """
        self.master = master
        self.direction = inisial_direction
        
        self.snake = Snake(
            canvas = self.master,
            lenght = lenght,
            color  = color,
            box_size = box_size,
            coordinates = coordinates
        )

    def random_direction(self):
        """
        Randomly choose a new direction for the snake.
        """
        new_direction = choice(("down","right","down","right","down","left","up","down"))
        
        if new_direction in ("down","up") and self.direction in ("down","up"):
            pass
        elif new_direction in ("right","left") and self.direction in ("right","left"):
            pass
        else: self.direction = new_direction
    
    def calculate_new_coordinates(self):
        """
        Calculate new coordinates for the snake's head based on its current direction.
        """
        self.random_direction()
        
        x , y =self.snake.snake_coordinates[0]
        
        if self.direction == "up":
            y -= self.snake.box_size
            
        elif self.direction == "down":
            y += self.snake.box_size
            
        elif self.direction == "right":
            x += self.snake.box_size
            
        elif self.direction == "left":
            x -= self.snake.box_size
        
        #adjusting screen :0
        canvas_width = int(self.master.cget("width"))
        canvas_height = int(self.master.cget("height"))
        
        x = canvas_width if x < 0 else 0 if x > canvas_width else x
        y = canvas_width if y < 0 else 0 if y > canvas_height else y
        
        self.coordinates = (x,y)
    
    def move_the_snakes(self):
        """
        Move the snake to the new coordinates.
        """
        self.calculate_new_coordinates()
        x , y = self.coordinates
        self.snake.move_snake(x , y , True)
    
    def return_id(self) -> tuple[int]:
        """
        return the snake id
        """
        return self.snake.snake_body()

    def delete_all(self) -> None:
        """
        delete all snake drawn
        """
        self.snake.delete_all()
        
    def update_color(self , color) -> None:
        """
        Update the color of the goofy snake.

        Args:
            color (str): The new color of the goofy snake.
        """
        self.snake.update_color(color)
        
    def update_size(self , box_size) -> None:
        """
        Updates the size of the box and the snake.
        
        Args:
            box_size (int): The new size of the box.
        """
        self.snake.update_size(box_size)