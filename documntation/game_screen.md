# Game_screen

## shop_window (class)

### money expences system

money manage directally by this class and at a time updated to var element that may create some sort of probleam... for fixing it we gonna do thease :

1. take current `var.PLAYERP_COINE` and copy it as artibute in this class under `_current_value` artibute

2. `var.PLAYERP_COINE` will only be updated when `button_method2` will run with index 3 (for saving )

3. all transection will made by `_current_value` under this class

by doing that we can pervent money loss if player dont click on save and goes... to other page..

### inisial methods

1. `set_up() -> None:`
Sets up the main canvas and initializes various graphical elements.
its create all text id shape ids that can be manupluated later by various gui method.. and data inserted\
i. set up method also do styling work..

2. `resize_window(width, height) -> None:`
Resizes the window and arranges shapes and buttons in a grid layout on the canvas. according to the width and height for creating resposvie desigen\
i. its get the coords.. again for each shape id in canvas... for checking which shape player click on canvas ~by calling `_get_coords()` method ~ by the same method resize_window

3. `_bind_key() -> None:` this method bind the canvas with button-1 click with a method _calling_func_method

### how backend_work

the backend work in this module is to buy things.. add new shop items.. accoding to the new items list that may given to the class by change_window(method)
managing purchase and shopitem persentaiton in gui.. form save button next and back button everything... 
how data will manage inside the method and purchassing etc...

1. tha calling method accrding to the click work with thease methos\
a. `_bind_key()`\
b. `_get_coords()`\
c. `_calling_func_method(event)`\
d. `_button_method(index_num)`\
e. `_button2_method(index_num)`

`_bind_key()` this method set the inisial point by binding button-1 to the canvas.. and then after that for figurring out where player clicked we need coordinates of each shape..
`_get_coords()` for that we use get_coords method.. that calculate each clickable shape coordinates.. and then for calling we bind the method `_calling_func_method(event)` with button-1 method under bind_key() method.. the method _calling_func_method(event) will call according to which coords shape where clicked.. by finding that it will call `_button_method(index_num)` or `_button2_method(index_num)` according to what we clicked and provide it with current index of button we clicked .. then main work begin under thease 2 method `_button_method(index_num)` and `_button2_method(index_num)`

2. for getting new data in class... we need to manage few things.. and get the new data method that used is `change_window(self, data:dict, update_method:callable, save_method:callable) -> None:`\
this method uses 2 personal method that are :-\
a. `_add_info_shopitems(data[tuple[dict]]):`\
b. `_add_info_upgradable(self):`

### other methods

1. `delete_window(self) -> None:`
2. `set_to_defult(self) -> None:`
3. `update_size_and_color -> None:`

## account_screen (class)

### frontend works

hello hi
