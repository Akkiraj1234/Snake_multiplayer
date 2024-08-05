# Game_screen

## shop_window (class)

### Money Expenses System

To manage money efficiently and prevent issues when players navigate away without saving:

1. Copy `var.PLAYERP_COINE` to `_current_value` attribute in the class.
2. Update `var.PLAYERP_COINE` only when `button_method2` runs with index 3 (for saving).
3. Handle all transactions using `_current_value`.

### Initial Methods

1. `set_up() -> None`
   - Sets up the main canvas and initializes graphical elements, including text and shape IDs.
   - Performs styling tasks.

2. `resize_window(width, height) -> None`
   - Resizes the window and arranges shapes and buttons responsively.
   - Recalculates coordinates for each shape ID on the canvas by calling `_get_coords()`.

3. `_bind_key() -> None`
   - Binds the canvas with a button-1 click to `_calling_func_method`.

### Backend Work

The backend handles buying items, adding new shop items, and managing purchases and shop item presentation in the GUI. It also handles interactions for save, next, and back buttons.

#### Click Handling Methods

1. `_bind_key()`
   - Binds button-1 to the canvas for initial point setting.

2. `_get_coords()`
   - Calculates coordinates of each clickable shape.

3. `_calling_func_method(event)`
   - Calls appropriate methods based on which shape's coordinates were clicked, invoking `_button_method(index_num)` or `_button2_method(index_num)`.

4. `_button_method(index_num)`
   - Handles main functionality for button clicks.

5. `_button2_method(index_num)`
   - Handles additional functionality for button clicks, including updating `var.PLAYERP_COINE` when index 3 is clicked.

#### Data Management Methods

1. `change_window(self, data: dict, update_method: callable, save_method: callable) -> None`
   - Manages new data and updates the window using the provided methods.

2. `_add_info_shopitems(data: tuple[dict])`
   - Adds new shop items based on the provided data.

3. `_add_info_upgradable(self)`
   - Adds information about upgradable items.

### Other Methods

1. `delete_window(self) -> None`
   - Deletes the current window.

2. `set_to_defult(self) -> None`
   - Resets the window to its default state.

3. `update_size_and_color(self) -> None`
   - Updates the size and color of elements.

## account_screen (class)

### Frontend Works

Handles frontend tasks related to account management.

`hello hi`
