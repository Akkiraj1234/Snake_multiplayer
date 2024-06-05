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

---

## need to improve :0

1. in `game_idles.py` under `Food class` there is `new_food(...)` method which creating new cordinates method is wrong which need to fix :0

```python
def new_coordinates(self, occupied_coordinates):
    """Generate new random coordinates for the food item, ensuring they do not overlap with occupied coordinates."""
    # Define grid dimensions based on game width and height
    num_columns = self.game_width // self.box_size
    num_rows = self.game_height // self.box_size
    
    # Create sets to track available coordinates
    available_columns = set(range(num_columns))
    available_rows = set(range(num_rows))
    
    # Remove occupied coordinates from available sets
    for x, y in occupied_coordinates:
        if x in available_columns:
            available_columns.remove(x)
        if y in available_rows:
            available_rows.remove(y)
    
    # Check if any available coordinates remain
    if not available_columns or not available_rows:
        # No available coordinates
        return
    
    # Choose a random available column and row
    new_x = choice(list(available_columns)) * self.box_size
    new_y = choice(list(available_rows)) * self.box_size
    
    # Update food coordinates
    self.x, self.y = new_x, new_y
```

thinking to use this after modification :0