# Sneck Safari README

---

## Project Overview

Sneck Safari is a Python-based snake game developed using the tkinter library. It offers a classic snake gameplay experience with additional features such as offline and online modes, customizable snake skins and background colors, a ranking system, a shop for purchasing in-game items, and various settings adjustments.

---

## Features

1. **Home Menu:** Upon launching the game, players are greeted with a home menu featuring buttons for Play, Shop, Settings, and Credits.

2. **Offline and Online Modes:** Players can choose between offline mode for solo play or online mode for multiplayer action. In online mode, players can compete with others and view the top-ranked players via a leaderboard.

3. **Customization:** Sneck Safari offers customization options in the shop where players can purchase different snake colors, skins, and background colors to personalize their gaming experience.

4. **Settings:** The settings menu allows players to adjust various game settings such as sound, controls, and display preferences to suit their preferences.

5. **Multiplayer:** In online mode, players can create IDs and play against other players in real-time multiplayer matches, adding a competitive edge to the gameplay.

---

## Future Development

1. **Enhanced Ranking System:** Implementing a more robust ranking system with detailed player statistics and rewards for top players.

2. **Expanded Shop:** Adding more items for purchase in the shop, such as power-ups, additional snake skins, and background themes.

3. **Improved UI/UX:** Continuously refining the user interface and user experience to make the game more visually appealing and intuitive to navigate.

## need to improve :0

1. in game_idles.py under Food class there is 0new_food(...) method which creating new cordinates method is fixed by that code.  ->  `FIXED`

2. needed to update the snake's segment coordinates to fit a new box size while maintaining their alignment and direction without overlap. -> `FIXED`

## probleams fixed :0

1. You encountered an issue with a previous implementation for generating new coordinates within a grid. The problem arose when attempting to ensure that the new coordinates did not overlap with existing coordinates. The initial approach unintentionally formed squares in the grid due to incorrect handling of occupied coordinates.

    **Solution Approach:**\
    To address this problem, you implemented a new function named get_new_cords with the goal of generating coordinates that avoided overlap with existing ones, thus preventing the formation of unintended squares.

    **Implementation Details:**
    - The `get_new_cords` function takes as input a dictionary `dict1` representing occupied coordinates, along with the dimensions of the grid `(width_box, height_box)`, and the size of each box `(box_size)`.
    - In the function, you randomly generate x and y coordinates within the grid.
    - You then iterate through the occupied x coordinates to ensure that the new x coordinate does not result in a full column. If it does, you adjust the x coordinate accordingly.
    - Similarly, you iterate through the occupied y coordinates to ensure that the new y coordinate does not result in a full row. If it does, you adjust the y coordinate accordingly.
    - After ensuring that the new coordinates do not overlap with existing ones, you return the newly generated x and y coordinates.

    ```python
    def generate_non_overlapping_coordinates(self, list1, width_box, height_box, box_size):
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
        
        def x_y_dict(list1, box_size) -> dict:
            """
            Convert a list of coordinates into a dictionary for quick lookup.
            """
            dict1 = {}
            for x, y in list1:
                x //= box_size
                y //= box_size
                
                if x in dict1:
                    dict1[x].add(y)
                else:
                    dict1[x] = {y}
            return dict1
        
        x = randint(0, width_box)
        y = randint(0, height_box)
        
        dict1 = x_y_dict(list1, box_size)
        original_x = x
        while (x in dict1) and (len(dict1[x]) == width_box + 1):
            x = (x + 1) if x < width_box else 0
            if original_x == x:
                return None
            
        original_y = y
        while (x in dict1) and (y in dict1[x]):
            y = (y + 1) if y < height_box else 0
            if original_y == y:
                return None
        
        return x * box_size, y * box_size

    ```

2. You encountered an issue where you needed to update the coordinates of a snake's segments to fit within a new box size in a grid-based game. The challenge was to adjust the positions of the snake's segments to align properly with the new box size while maintaining their relative positions and movement direction, and avoiding any overlap.

    **Solution Approach:**\
    To address this problem, you implemented a function named update_cords that recalculates the coordinates of the snake's segments based on the new box size. The function ensures that the snake's segments adjust their positions correctly and continue to move in the same direction without overlapping.

    **Implementation Details:**
    - The update_cords function takes the new box size as an argument and calculates the increment based on the difference between the new and old box sizes.
    - The function iterates through each segment of the snake, starting from the head.
    - For each segment, it adjusts the x and y coordinates based on the calculated increment, ensuring that - the relative position of each segment remains consistent.
    The adjustments are made in such a way that the direction of the snake's movement is preserved.
    - After updating the coordinates, the function validates the new coordinates to ensure they fit within the grid's boundaries.

    ```python
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
    ```
