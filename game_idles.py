from tkinter import Canvas
from random import randint,choice
# import gc #use gc.collect()

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

def lighten_hex_color(hex_color, lighten_factor=0.1) -> str:
    """
    Lightens a given hex color.

    Args:
        hex_color (str): The hex color string to lighten, e.g., '#RRGGBB'.
        lighten_factor (float): The factor by which to lighten the color, where 0 is no change
                                and 1 is white. Default is 0.1 (10% lighter).

    Returns:
        str: The lightened hex color string.
    """
    if hex_color.startswith('#'):
        hex_color = hex_color[1:]
    r = int(hex_color[:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:], 16)
    r = int(r + (255 - r) * lighten_factor)
    g = int(g + (255 - g) * lighten_factor)
    b = int(b + (255 - b) * lighten_factor)
    r = min(255, max(0, r))
    g = min(255, max(0, g))
    b = min(255, max(0, b))
    lightened_hex_color = f'#{r:02X}{g:02X}{b:02X}'
    return lightened_hex_color

def darken_hex_color(hex_color, darken_factor=0.1) -> str:
    """
    Darkens a given hex color.

    Args:
        hex_color (str): The hex color string to darken, e.g., '#RRGGBB'.
        darken_factor (float): The factor by which to darken the color, where 0 is no change
                               and 1 is black. Default is 0.1 (10% darker).

    Returns:
        str: The darkened hex color string.
    """
    if hex_color.startswith('#'):
        hex_color = hex_color[1:]
    r = int(hex_color[:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:], 16)
    r = int(r * (1 - darken_factor))
    g = int(g * (1 - darken_factor))
    b = int(b * (1 - darken_factor))
    r = min(255, max(0, r))
    g = min(255, max(0, g))
    b = min(255, max(0, b))
    darkened_hex_color = f'#{r:02X}{g:02X}{b:02X}'
    return darkened_hex_color



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
            
        Time Complexity: O(n), where n is the number of snake segments.
        Space Complexity: O(n), where n is the number of snake segments.
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
        canvas_width (int): The width of the game area.
        canvas_height (int): The height of the game area.
        food (int): The ID of the current food item on the canvas.
        x (int): The x-coordinate of the food item.
        y (int): The y-coordinate of the food item.

    Methods:
        __init__(canvas, color, box_size): Initialize a new Food object.\n
        _calculate_dimensions: Calculate width height and more for Food obj\n
        _create_food_oval(): Create an oval-shaped food item on the canvas.\n
        _delete_food(): Delete the current food item from the canvas.\n
        move_resize_food(): Move current Food obj to new coordinates\n
        new_coordinates(): Generate new random coordinates for the food item.\n
        generate_non_overlapping_coordinates(coordinates:tuple|list):
        genrate coordinates that does not overlap given cords[(int,int),(int,int)] list\n
        new_food(coordinates:tuple|list|None = None): Create a new food items\n
        update_color(color): update the color of Food and for obj\n
        update_size(box_size); update the box_size of Food \n
        
    """
    def __init__(self, canvas:Canvas, color:str, box_size:int)-> None:
        """
        Initialize the Food object.

        Args:
            canvas (Canvas): The canvas on which the food item will be drawn.
            box_size (int): The size of each box representing the food item.
            color (str): The color of the food item.
        
        Attributes:
            food (int): The ID of the current food item on the canvas
            x (int): The x cordinate of current food 
            y (int): The y cordinate of current food
        """
        self.canvas = canvas
        self.box_size = box_size
        self.color = color
        
        self.food = None
        self.x = 0
        self.y = 0
        
        self._calculate_dimensions()
        self.x, self.y = self.new_coordinates()
        self.new_food()
    
    def _calculate_dimensions(self) -> None:
        """
        Calculate and store the width and height of the canvas.
        """
        self.canvas_width = int(self.canvas.cget("width"))
        self.canvas_height = int(self.canvas.cget("height"))
        #calculating grid
        self.__width_grid_size = (self.canvas_width // self.box_size) - 1
        self.__height_grid_size = (self.canvas_height // self.box_size) - 1
        
    def _create_food_oval(self) -> None:
        """
        Create an oval-shaped food item.
        """
        
        iteme_id = self.canvas.create_oval(
            self.x , self.y, #x1 and y1
            self.x + self.box_size, #x2
            self.y + self.box_size, #y2
            fill=self.color #color
        )
        self.food = iteme_id
    
    def _delete_food(self) -> None:
        """
        Delete the current food item from the canvas.
        """
        if self.food is None:
            return None
        
        self.canvas.delete(self.food)
    
    def move_resize_food(self) -> None:
        """
        Update the position and size of the food item on the canvas.
        
        Moves the food item to (self.x, self.y) and resizes it to self.box_size.
        """
        self.canvas.coords(
            self.food, self.x, self.y, self.x + self.box_size, self.y + self.box_size 
        )
        
    def new_coordinates(self) -> tuple[int,int]:
        """
        Generate new random coordinates for the food item.
        """
        # The approach divides the screen into a grid of cells, where each cell represents a possible position for the food.
        # The grid is defined by the box_size, which determines the size of each cell.
        # To select a random cell, we choose a random integer index along the x-axis (vertical lines) and y-axis (horizontal lines).
        # We then multiply these indices by the box_size to obtain the exact coordinates within the canvas where the food can be placed.
        
        x = randint(0, self.__width_grid_size)* self.box_size
        y =  randint(0, self.__height_grid_size)* self.box_size
        return x,y

    def generate_non_overlapping_coordinates(self, coordinates:list|tuple) -> tuple[int,int]:
        """
        Generate new coordinates within a grid that do not overlap with existing coordinates.

        Args:
            list1 (list of tuples): List of current coordinates.
            width_box (int): Width of the grid in terms of boxes.
            height_box (int): Height of the grid in terms of boxes.
            box_size (int): Size of each box.

        Returns:
            tuple: New x, y coordinates in terms of pixels if available, otherwise None.
        
        Time Complexity: 𝑂(𝑛 + width_box + height_box)
        Space Complexity: 𝑂(𝑛)

        """
        
        def x_y_dict(coordinates, box_size) -> dict:
            """
            Convert a list of coordinates into a dictionary for quick lookup.
            """
            dict1 = {}
            for x, y in coordinates:
                x //= box_size
                y //= box_size
                
                if x in dict1:
                    dict1[x].add(y)
                else:
                    dict1[x] = {y}
            return dict1
        
        #genrating random cordss in box_size
        x = randint(0, self.__width_grid_size)
        y = randint(0, self.__height_grid_size)
        
        dict1 = x_y_dict(coordinates, self.box_size)
        
        original_x = x
        while (x in dict1) and (len(dict1[x]) == self.__width_grid_size + 1):
            x = (x + 1) if x < self.__width_grid_size else 0
            if original_x == x:
                return None
            
        original_y = y
        while (x in dict1) and (y in dict1[x]):
            y = (y + 1) if y < self.__height_grid_size else 0
            if original_y == y:
                return None
        
        return x * self.box_size, y * self.box_size

    
    def new_food(self, cordinates:list|tuple|None = None) -> None:
        """
        Create a new food item of the specified type and optionally at specified coordinates.

        Args:
            coordinates (list or tuple or None): Optional coordinates to place the food item.
                If provided, the food item will be placed at these coordinates.
        """
        if cordinates is not None:
            self.x , self.y = self.generate_non_overlapping_coordinates(cordinates)
        else:
            self.x, self.y = self.new_coordinates()
            
        if self.food:
            self.move_resize_food()
        else:
            self._create_food_oval()
        
    def update_color(self , color:str) -> None:
        """Update the color of the Food.

        Args:
            color (str): The new color of the Food.
        """
        self.color = color
        if self.food:
            self.canvas.itemconfig(self.food, fill = self.color)
        else:
            self._create_food_oval()
    
    def update_size(self , box_size:int) -> None:
        self.box_size = box_size
        self._calculate_dimensions()
        self.x , self.y = validate_cordinates((self.x , self.y), self.box_size)
        
        if self.food:
            self.move_resize_food()
        else:
            self._create_food_oval()
            
class Heart:
    """
    This class helps create hearts, remove hearts, and manipulate heart shapes on a canvas.
    This class will not perform any calculations for coordinates.
    
    Attributes:
        canvas (Canvas): The canvas on which the heart shapes will be drawn.
        box_size (int): The size of the heart shape.
        color (str): The color of the heart shape.
        hearts (tuple): A tuple containing the IDs of the components of the heart shape on the canvas.
        coords (tuple): The coordinates of the heart shape.
    """
    def __init__(self, canvas:Canvas, box_size:int, color:str, insalize = True, cords = (0,0)) -> None:
        """
        Initializes a Heart object with the given canvas, box size, and color.

        Args:
            canvas (Canvas): The canvas on which the heart shape will be drawn.
            box_size (int): The size of the heart shape.
            color (str): The color of the heart shape.

        Returns:
            None
        """
        self.canvas = canvas
        self.box_size = box_size
        self.color = color
        
        self.hearts = None
        self.coords = (None,None)
        self.avialable = False
        
        if insalize:
            self.new_heart(cords)
            
    def _create_heart_shape(self, coordinates:tuple[int, int], return_:bool = False) -> None:
        """
        Draws a heart shape on the canvas.

        Args:
            coordinates (tuple[int, int]): The x and y coordinates where the heart will be drawn.
            return_ (bool): Asking if the item it shoude be returned or not defult False

        Note:
            This method is can be cause of data leakage use it carfully.
        """
        self.avialable = True
        x1, y1 = coordinates
        x2, y2 = x1 + self.box_size, y1 + self.box_size
        self.coords = (x1, y1)

        new_y1 = (self.box_size / 2) + y1
        new_x1 = (self.box_size / 2) + x1
        radius = (new_y1 - y1) / 2
        
        first = self.canvas.create_arc(x1, new_y1 - radius, new_x1, new_y1 + radius, fill=self.color, start=0, extent=180)
        second = self.canvas.create_arc(new_x1, new_y1 - radius, x2, new_y1 + radius, fill=self.color, start=0, extent=180)
        third = self.canvas.create_polygon(x1, new_y1, x2, new_y1, (x1 + x2) / 2, y2, fill=self.color)
        
        if return_:
            return (first, second, third)
        self.hearts = (first, second, third)
    
    def _move_resize_heart_shape(self, coordinates:tuple[int, int], heart:tuple = None) -> None:
        """
        Moves and resizes the heart shape on the canvas.

        Args:
            coordinates (tuple[int, int]): The new x and y coordinates for the heart shape.
            heart (tuple): this method takes heart items tupple shoude be the same canvas as this method canvas hold defult none if not given takes self.hearts the body

        Returns:
            None
        """
        self.avialable = True
        
        if not heart:
            heart = self.hearts
            
        x1, y1 = coordinates
        x2, y2 = x1 + self.box_size, y1 + self.box_size

        new_y1 = (self.box_size / 2) + y1
        new_x1 = (self.box_size / 2) + x1
        radius = (new_y1 - y1) / 2
        self.coords = (x1, y1)
        
        self.canvas.coords(heart[0],
            x1, new_y1 - radius, new_x1, new_y1 + radius
        )
        self.canvas.coords(heart[1],
            new_x1, new_y1 - radius, x2, new_y1 + radius
        )
        self.canvas.coords(heart[2],
            x1, new_y1, x2, new_y1, (x1 + x2) / 2, y2
        )
        
        for body in heart:
            self.canvas.itemconfig(body, state='normal', fill=self.color)
        
    def delete_heart(self, hide: bool = True) -> None:
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
                self.canvas.itemconfig(heart, state="hidden")
            return None
        
        for heart in self.hearts:
            self.canvas.delete(heart)
        self.hearts = None
        
    def new_heart(self, coordinates, validate:bool = True):
        """
        Creates a new heart shape on the canvas.

        Args:
            coordinates (tuple[int, int]): The x and y coordinates where the heart will be drawn.

        Returns:
            None
        """
        if validate:
            coordinates = validate_cordinates(coordinates,self.box_size)
        if self.hearts is None:
            self._create_heart_shape(coordinates)
        else:
            self._move_resize_heart_shape(coordinates)
            
    def update_color(self, color: str):
        """
        Changes the color of the heart shape.

        Args:
            color (str): The new color of the heart shape.

        Returns:
            None
        """
        self.color = color
        
        if self.hearts is None:
            return None
        
        for heart in self.hearts:
            self.canvas.itemconfig(heart, fill=self.color)
    
    def update_size(self, box_size: int):
        """
        Changes the size of the heart shape.

        Args:
            box_size (int): The new size of the heart shape.

        Returns:
            None
        """
        self.box_size = box_size
        
        if self.hearts is None:
            return None
        self.new_heart(self.coords)


class Coin:
    """
    Represents a coin object that can be drawn on a canvas.

    Attributes:
    canvas (Canvas): The canvas on which the coin will be drawn.
    box_size (int): The size of the coin.
    color (str): The color of the coin.
    inner_color (str): The color of the inner part of the coin.
    coin (tuple): The coin shape consisting of graphical elements.
    coords (tuple): The coordinates of the top-left corner of the coin.
    """
    def __init__(self, canvas:Canvas, box_size:int, color:str, insalize:bool = True, cords:tuple = (0,0)) -> None:
        """
        Initializes a Coin object.

        Parameters:
        canvas (Canvas): The canvas on which the coin will be drawn.
        box_size (int): The size of the coin.
        color (str): The color of the coin.
        """
        self.canvas = canvas
        self.box_size = box_size
        self.color = color
        self.inner_color = darken_hex_color(self.color , 0.1)
        
        self.coin = None
        self.coords = (None,None)
        self.avialable = False
        
        if insalize:
            self.new_coin(cords)
        
    def _create_coin(self, coordinates:tuple[int,int]):
        """
        Creates a new coin at the specified coordinates.

        Parameters:
        coordinates (tuple[int, int]): The (x, y) coordinates for the top-left corner of the coin.
        """
        self.avialable = True
        
        x1 , y1 = coordinates
        self.coords = coordinates
        #innerx1 and box_szie
        innerx1 = (self.box_size // 10) + x1
        innery1 = (self.box_size // 10) + y1
        inner_boxsize = self.box_size - (self.box_size // 10) * 2
        #inner_smile_cords
        middlex1 = innerx1+(inner_boxsize//2)
        middley1 = innery1+(inner_boxsize//2)
        #text_size = pixels * (72 / dpi(96)==0.75)
        text_size = inner_boxsize // 5
        text_size = int(text_size * 7.5)//2
        
        first = self.canvas.create_oval(x1, y1, x1+self.box_size, y1+self.box_size,fill = self.color, outline = "black")
        secoend = self.canvas.create_oval(innerx1, innery1, innerx1+inner_boxsize, innery1+inner_boxsize, outline="black", fill=self.inner_color)
        third = self.canvas.create_text(middlex1 , middley1, text="!",justify="center",fill="black",font=("Arial",text_size,"bold"))
        self.coin = (first , secoend , third)
    
    def _move_resize_coin_shape(self, coordinates:tuple[int, int]) -> None:
        """
        Moves and resizes the coin shape to the specified coordinates.

        Parameters:
        coordinates (tuple[int, int]): The (x, y) coordinates for the top-left corner of the coin.
        """
        self.avialable = True
        
        x1 ,y1 = coordinates
        self.coords = coordinates
        #innerx1 and box_szie
        innerx1 = (self.box_size // 10) + x1
        innery1 = (self.box_size // 10) + y1
        inner_boxsize = self.box_size - (self.box_size // 10) * 2
        #inner_smile_cords
        middlex1 = innerx1+(inner_boxsize//2)
        middley1 = innery1+(inner_boxsize//2)
        #text_size = pixels * (72 / dpi(96))==0.75
        text_size = inner_boxsize // 5
        text_size = int(text_size * 7.5)//2
        
        self.canvas.coords(self.coin[0],
            x1, y1, x1+self.box_size, y1+self.box_size
        )
        self.canvas.coords(self.coin[1],
            innerx1, innery1, innerx1+inner_boxsize, innery1+inner_boxsize
        )
        self.canvas.coords(self.coin[2],
            middlex1 , middley1
        )
        
        self.canvas.itemconfig(self.coin[0], state='normal')
        self.canvas.itemconfig(self.coin[1], state='normal')
        self.canvas.itemconfig(self.coin[2], state='normal',font=("Arial",text_size,"bold"))
        
    def delete_coin(self, hide: bool = True) -> None:
        """
        Deletes or hides the coin from the canvas.

        Parameters:
        hide (bool): If True, hides the coin; otherwise, deletes it from the canvas.
        """
        self.avialable = False
        
        if self.coin is None:
            return None
        
        if hide:
            for coin in self.coin:
                self.canvas.itemconfig(coin, state="hidden")
            return None
        
        for coin in self.coin:
            self.canvas.delete(coin)
        self.hearts = None
        
    def new_coin(self, coordinates, validate:bool = True):
        """
        Creates a new coin or moves an existing one to the specified coordinates.

        Parameters:
        coordinates (tuple[int, int]): The (x, y) coordinates for the top-left corner of the coin.
        """
        if validate:
            coordinates = validate_cordinates(coordinates,self.box_size)
        if self.coin is None:
            self._create_coin(coordinates)
        else:
            self._move_resize_coin_shape(coordinates)
            
    def update_color(self, color: str):
        """
        Changes the color of the coin.

        Parameters:
        color (str): The new color of the coin.
        """
        self.color = color
        self.inner_color = darken_hex_color(self.color , 0.1)
        
        if self.coin is None:
            return None
        
        self.canvas.itemconfig(self.coin[0], fill = self.color)
        self.canvas.itemconfig(self.coin[1], fill = self.inner_color)
    
    def update_size(self, box_size:int):
        """
        Changes the size of the coin.

        Parameters:
        box_size (int): The new size of the coin.
        """
        self.box_size = box_size
        
        if self.coin is None:
            return None
        self.new_coin(self.coords)


class Heart_NEV:
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
        initial_heart (int): The number of hearts to initialize.
    """
    def __init__(self, canvas:Canvas, color:str, inisial_heart=1) -> None:
        """
        Initialize a Heart_NEV object.

        Args:
            canvas (Canvas): The canvas on which the heart will be drawn.
            color (str): The color of the heart.
            initial_heart (int, optional): The number of hearts to initialize. Defaults to 1.
        """
        self.inisial_heart = inisial_heart
        self.canvas = canvas
        self.color = color
        self.limit = None
        self.calulating_diameters()
        self.heart = Heart(self.canvas, self.box_size, self.color,insalize=False)
        
        self.hearts_list = []
        self.add_heart_in_range(self.inisial_heart)
    
    def calulating_diameters(self) -> None:
        """
        Calculate box size, coordinates, and distance.
        """
        # Get canvas dimensions
        canvas_height = int(self.canvas.cget("height"))
        canvas_width = int(self.canvas.cget("width"))
        
        # Calculate padding and box size
        padding = canvas_height // 8
        box_size = padding * 7
        
        # Determine coordinates
        y = padding
        x = canvas_width - box_size
        
        # Set instance variables
        self.box_size = box_size
        self.cordinates = (x, y)
        self.distance = box_size // 4
    
    def remmove_heart(self) -> None:
        """
        Remove the last heart from the canvas.
        """
        if self.hearts_list == []:
            return None
        
        for ids in self.hearts_list.pop():
            self.canvas.delete(ids)
            
        self.cordinates = (self.cordinates[0]+self.box_size+self.distance , self.cordinates[1])
        
    def remove_all_heart(self) -> None:
        """
        remove all the heart left on the canvas.
        """
        for _ in range(len(self.hearts_list)):
            self.remmove_heart()
            
    def add_heart_in_range(self,num = 0) -> None:
        """
        Add hearts to the canvas within a specified range.

        Args:
            num (int, optional): The number of hearts to add. Defaults to initial_heart if not provided.
        """
        if not num:
            num = self.inisial_heart
        
        for _ in range(num):
            self.add_one_heart(check = False)
    
    def add_one_heart(self , check:bool = True) -> None:
        """
        Add one heart to the canvas.

        Args:
            check (bool, optional): If True, check if the limit is set and if the number of hearts exceeds the limit.Defaults to True.
        """
        if check and self.limit and len(self.hearts_list) >= self.limit:
            return None
        
        heart = self.heart._create_heart_shape(self.cordinates , return_=True)
        
        self.hearts_list.append(heart)
        self.cordinates = (self.cordinates[0]-self.box_size-self.distance , self.cordinates[1])
        
    def update_color(self,color:str):
        """Update the color of the Heart.

        Args:
            color (str): The new color of the Heart.
        """
        self.color = color
        self.heart.color = color
        
        for hearts in self.hearts_list:
            self.canvas.itemconfig(hearts[0],fill = self.color)
            self.canvas.itemconfig(hearts[1],fill = self.color)
            self.canvas.itemconfig(hearts[2],fill = self.color)
    
    def update_size(self) -> None:
        self.calulating_diameters()
        self.heart.box_size = self.box_size
        
        for heart in reversed(self.hearts_list):
            self.heart._move_resize_heart_shape(self.cordinates,heart)
            self.cordinates = (self.cordinates[0]+self.box_size+self.distance , self.cordinates[1])
        

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
        
    def update_color(self , color):
        """
        Update the color of the goofy snake.

        Args:
            color (str): The new color of the goofy snake.
        """
        self.snake.update_color(self.color)
        
    def update_size(self , box_size):
        """
        Updates the size of the box and the snake.
        
        Args:
            box_size (int): The new size of the box.
        """
        self.snake.update_size(box_size)