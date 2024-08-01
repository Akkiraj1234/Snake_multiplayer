from random import randint,choice


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

def random_coordinates(grid_width:int, grid_height:int, box_size:int) -> tuple[int,int]:
    """
    Generate random coordinates within the given grid dimensions, adjusted by the box size.

    Args:
        grid_width (int): The width of the grid in terms of number of boxes.
        grid_height (int): The height of the grid in terms of number of boxes.
        box_size (int): The size of each box in the grid.

    Returns:
        tuple[int, int]: A tuple containing the random (x, y) coordinates.
    """
    # The approach divides the screen into a grid of cells, where each cell represents a possible position for the food.
    # The grid is defined by the box_size, which determines the size of each cell.
    # To select a random cell, we choose a random integer index along the x-axis (vertical lines) and y-axis (horizontal lines).
    # We then multiply these indices by the box_size to obtain the exact coordinates within the canvas where the food can be placed.
    x = randint(0, grid_width)* box_size
    y = randint(0, grid_height)* box_size
    return (x , y)

def generate_non_overlapping_coordinates(
    coordinates : list|tuple,
    grid_width : int,
    grid_height : int,
    box_size : int
    ) -> tuple[int,int]|None:
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
    def coordinates_to_dict(coordinates, box_size) -> dict[int:set]:
        """
        Convert a list of coordinates into a dictionary for quick lookup.
        """
        dict1 = {}
        for x , y in coordinates:
            x //= box_size
            y //= box_size
            
            if x in dict1:
                dict1[x].add(y)
            else:
                dict1[x] = {y}
        return dict1
    
    #genrating random cordss in box_size
    x = randint(0 , grid_width)
    y = randint(0 , grid_height)
    
    dict1 = coordinates_to_dict(coordinates, box_size)
    
    #there is no infinite loop possible
    # If the current x is in the dictionary and all possible y values are taken (column is full),
    # move to the next x value. Wrap around to 0 if the end of the grid is reached.
    # If we've cycled back to the original x value, it means no available x-coordinate was found.
    # the same thing going on with 2nd while loop
    
    original_x = x
    while (x in dict1) and (len(dict1[x]) == grid_width + 1):
        x = (x + 1) if x < grid_width else 0
        if original_x == x:
            return None
        
    # there is no infinite loop possible
    original_y = y
    while (x in dict1) and (y in dict1[x]):
        y = (y + 1) if y < grid_height else 0
        if original_y == y:
            return None
    
    return x * box_size , y * box_size

def validate_coordinates(cords ,box_size:int) -> tuple[int:int]:
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

def check_cords_in_range(list_cords:list[tuple], coordinates:tuple[int]) -> bool:
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

def round_up_coords(height:int, width:int, box_size:int, coordinates:tuple) -> tuple[int,int]:
    coordinates[0] = min((height // box_size),max(0,coordinates[0]))*box_size
    coordinates[1] = min((width // box_size),max(0,coordinates[1]))*box_size
    return coordinates
