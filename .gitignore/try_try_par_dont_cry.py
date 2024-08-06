from tkinter import Canvas , Tk , Frame , Button, messagebox
from variable import Variable

class WindowCreator:
    """
    A class to create and manage a shopping interface window with multiple selectable and upgradable items.

    Attributes:
    master (Frame|Tk): The parent widget for the main canvas.
    var (Variable): An instance of the Variable class to hold theme and other settings.
    main_canvas (Canvas): The main canvas widget where all elements are drawn.
    shop_shape_id (list): List of canvas IDs for shop item shapes.
    shop_button_id (list): List of canvas IDs for shop item buttons.
    shape_text_id (list): List of canvas IDs for shop item text.
    button_text_id (list): List of canvas IDs for button text.
    footer_shape_id (list): List of canvas IDs for footer shapes.
    footer_text_id (list): List of canvas IDs for footer text.
    upgradable_id (list): List of canvas IDs for upgradable items.
    upgradable_text (int): Canvas ID for upgradable item text.
    current_data (dict): Current data dictionary for shop items and upgradables.
    current_Sindex (int): Index of the currently selected item.
    current_update_method (callable): Method to update the canvas when an item is selected or upgraded.
    current_save_method (callable): Method to save the current state of the window.
    
    """
    def __init__(self,master:Frame|Tk, var:Variable, width:int, height:int) -> None:
        """
        Initializes the WindowCreator with the parent widget and variable instance.

        Parameters:
        master (Frame|Tk): The parent widget for the main canvas.
        var (Variable): An instance of the Variable class to hold theme and other settings.
        """
        self.main_canvas = None
        self.shop_shape_id = []
        self.shop_button_id = []
        self.shape_text_id = []
        self.button_text_id = []
        self.footer_shape_id = []
        self.footer_text_id = []
        self.upgradable_id = []
        self.upgradable_text = None
        self.master = master
        self.var = var
        
        
        self.current_data = None
        self.current_Sindex = None
        self.current_update_method = None
        self.current_save_method = None
        
        self.set_up()
        self.resize_window(width,height)
    
    def _bind_key_and_get_cords(self) -> None:
        """
        The way its contains coordinates are :
        _button_coords = index-[0,1,2,3,4,5,6,7,8,9]
        From 0 to 5 its shop canvas button coordinates.
        From 6 to 9 its conatins coordinates in this squence:
        upgradable_id[1](button), footer_shape_id[0-2](back,save,next)
        """
        self.main_canvas.bind("<Button-1>",self._calling_func_method)
        
        self._button_coords = [
            self.main_canvas.bbox(self.shop_button_id[num]) for num in range(6)
        ]
        self._button_coords.append(
            self.main_canvas.bbox(self.upgradable_id[1])
        )
        for id in self.footer_shape_id:
            self._button_coords.append(self.main_canvas.bbox(id))
    
    def _unbind_keys(self) -> None:
        self.main_canvas.unbind_all("<Button-1>")
    
    def _add_info_shopitems(self,data:tuple[dict]) -> None:
        """
        add info in canvas and gui according to the data
        for 6 shapes shapes, shape_text, button shape and text

        Args:
            data (tuple[dict]): data for the updation should be a tuple
            containing 6 dict from 0 index to 5 index
        """
        for num in range(len(data)):
            dict_data = data[num]
            
            self.main_canvas.itemconfig(
                self.shop_shape_id[num],
                fill = dict_data["color"],
                state = "normal"
            )
            self.main_canvas.itemconfig(
                self.shop_button_id[num],
                state = "normal"
            )
            self.main_canvas.itemconfig(
                self.shape_text_id[num],
                text = "" if dict_data["purchased"]
                else dict_data["price"],
                state = "normal"
            )
            self.main_canvas.itemconfig(
                self.button_text_id[num],
                text = "Buy" if not dict_data["purchased"]
                else "Selected" if dict_data["selected"] 
                else "Select",
                state = "normal"
            )
    
    def _add_info_upgradable(self) -> None:
        for num in range(self.current_data["upgradable"]):
            self.main_canvas.itemconfig(
            self.upgradable_id[2 + num],
            fill = "yellow",
            state = "normal"
            )
        power = self.current_data["upgradable"]
        charge = self.current_data["charge"]
        self.main_canvas.itemconfig(
            self.upgradable_text,
            text = power * charge,
            state = "normal"
        )
        if self.current_data["upgradable"]:
            for id in self.upgradable_id:
                self.main_canvas.itemconfig(id,state = "normal") 
        
    def _calling_func_method(self,event) -> None:
        """
        Internal method to update the canvas based on the current data.
        """
        def check_coords_in_range(list_coords,coords):
            x , y = coords
            x1 , y1 , x2 , y2 = list_coords
            
            if x1 < x < x2 and y1 < y < y2:
                return True
            return False
        
        coords = (event.x , event.y)
        
        if check_coords_in_range(self._button_coords[0],coords):
            self._button_method(0)
            
        elif check_coords_in_range(self._button_coords[1],coords):
            self._button_method(1)
            
        elif check_coords_in_range(self._button_coords[2],coords):
            self._button_method(2)
            
        elif check_coords_in_range(self._button_coords[3],coords):
            self._button_method(3)
            
        elif check_coords_in_range(self._button_coords[4],coords):
            self._button_method(4)
            
        elif check_coords_in_range(self._button_coords[5],coords):
            self._button_method(5)
            
        elif check_coords_in_range(self._button_coords[6],coords):
            self._button2_method(1)
            
        elif check_coords_in_range(self._button_coords[7],coords):
            self._button2_method(2)
            
        elif check_coords_in_range(self._button_coords[8],coords):
            self._button2_method(3)
            
        elif check_coords_in_range(self._button_coords[9],coords):
            self._button2_method(4)
    
    def _button_method(self,index_num) -> None:
        """
        handeling button event acording to button index
        """
        index = self.current_Sindex + index_num
        data = self.current_data["items"]
        selected = self.current_data["selected_index"]
                
        if not data[index]["purchased"]:
            # handelling buying
            if self.var.PLAYERP_COINE >= data[index]["price"]:
                self.var.PLAYERP_COINE -= data[index]["price"]
            else:
                messagebox.showwarning("buying info","purchase cant be made becouse of less money")
                return
            
            data[index]["purchased"] = True
            
            self.main_canvas.itemconfig(
                self.button_text_id[index_num],
                text = "select"
            )
            self.main_canvas.itemconfig(
                self.shape_text_id[index_num],
                text = ""
            )
        
        if data[index]["purchased"] and data[index]["selected"]:
            return 
        
        if data[index]["purchased"] and not data[index]["selected"]:
            
            data[index]["selected"] = True
            data[selected]["selected"] = False
            
            self.main_canvas.itemconfig(
                self.button_text_id[index_num],
                text = "selected"
            )
            print(selected%5)
            self.main_canvas.itemconfig(
                self.button_text_id[(selected%5)-1],
                text = "select"
            )
            self.current_data["selected_index"] = index
            
        self.current_data["items"] = data
        self.current_update_method(data[index]["color"])
    
    def _button2_method(self,index_num) -> None:
        """
        handel button event for upgrade button save button
        back and next button
        """
        if index_num == 1:
            power = self.current_data["upgradable"]
            money = power * self.current_data["charge"]
            if power < 5 and self.var.PLAYERP_COINE >= money:
                self.current_data["upgradable"] += 1
                self._add_info_upgradable()
                self.var.PLAYERP_COINE -= money
            else:
                messagebox.showwarning("buying info","purchase cant be made becouse of less money")
            
        elif index_num == 2:
            if not self.current_Sindex <= 5:
                self.set_to_defult()
                self.current_Sindex -= 6
                
                data = self.current_data["items"]\
                [self.current_Sindex:self.current_Sindex+6]
                
                self._add_info_shopitems(data)
                
                
        elif index_num == 3:
            print("save")
            
        elif index_num == 4:
            if len(self.current_data["items"]) > 6:
                self.set_to_defult()
                self.current_Sindex += 6
                
                data = self.current_data["items"]\
                [self.current_Sindex:self.current_Sindex+6]
                
                self._add_info_shopitems(data)
        
        self.current_update_method(None)
        
    def set_up(self) -> None:
        """
        Sets up the main canvas and initializes various graphical elements.

        Parameters:
        width (int): The width of the canvas.
        height (int): The height of the canvas.
        """
        # Create the main canvas if it does not already exist
        if not self.main_canvas : self.main_canvas = Canvas(
            master = self.master,
            bg = self.var.theme1
        )
        # Create hidden rectangles for shop shapes if they do not already exist
        if not self.shop_shape_id : self.shop_shape_id = [
            self.main_canvas.create_rectangle(
                0 , 0 , 0 , 0 ,
               state = "hidden"
            ) for _ in range(6)
        ]
        # Create hidden rectangles for shop buttons if they do not already exist
        if not self.shop_button_id : self.shop_button_id = [
            self.main_canvas.create_rectangle(
                0 , 0 , 0 , 0 ,
               state = "hidden",
               
            ) for _ in range(6)
        ]
        # Create hidden text elements for shape texts if they do not already exist
        if not self.shape_text_id : self.shape_text_id = [
            self.main_canvas.create_text(
                0 , 0 , state = "hidden" ,
                anchor = "center", text = "buy"
            ) for _ in range(6)
        ]
        # Create hidden text elements for button texts if they do not already exist
        if not self.button_text_id : self.button_text_id = [
            self.main_canvas.create_text(
                0 , 0 , state = "hidden" ,
                anchor = "center", text = "buy"
            ) for _ in range(6)
        ]
        if not self.upgradable_id : self.upgradable_id = [
            self.main_canvas.create_rectangle(
                0 , 0 , 0 , 0 , 
                state = "hidden"
            ) for _ in range(7)
        ]
        if not self.upgradable_text : 
            self.upgradable_text =  self.main_canvas.create_text(
                0 , 0 , state = "hidden" ,
                anchor = "center", text = "buy"
            )
            
        if not self.footer_shape_id : self.footer_shape_id = [
            self.main_canvas.create_rectangle(
                0 , 0 , 0 , 0 ,
                state = "disabled"
            ) for _ in range(3)
        ]
        if not self.footer_text_id : self.footer_text_id = [
            self.main_canvas.create_text(
                0 , 0 , state = "hidden" ,
                anchor = "center", text = "buy"
            ) for _ in range(3)
        ]
    
    def resize_window(self, width:int , height:int) -> None:
        """
        Resizes the window and arranges shapes and buttons in a grid layout on the canvas.

        Parameters:
        width (int): The width of the window.
        height (int): The height of the window.
        """
        self._unbind_keys()
        
        
        self.main_canvas.config(
            width=width,
            height=height
        )
        
        self.shape_width = (width / 1.4) // 3
        self.padx = (width / 3.25) // 4
        
        devision = height / 4
        self.mini_pady = (devision / 2) / 4
        self.pady = (devision / 2) / 3
        self.button_height = devision / 3
        self.shape_height = self.button_height * 2
        print("pady" , self.pady,"\nmini_pady", self.mini_pady)
        
        def configure_canvas_item(number, x, y):
            self.main_canvas.coords(
                self.shop_shape_id[number],
                x, y, 
                x + self.shape_width,
                y + self.shape_height
            )
            self.main_canvas.coords(
                self.shape_text_id[number],
                (x + x + self.shape_width) / 2,
                (y + y + self.shape_height) / 2
            )
            button_y = y + self.shape_height + self.mini_pady
            self.main_canvas.coords(
                self.shop_button_id[number],
                x, button_y,
                x + self.shape_width,
                button_y + self.button_height
            )
            self.main_canvas.coords(
                self.button_text_id[number],
                (x + x + self.shape_width) / 2,
                (button_y + button_y + self.button_height) / 2
            )

        x, y = self.padx, self.pady
        number = 0

        for row in range(2):
            for col in range(3):
                configure_canvas_item(number, x, y)
                number += 1
                x += self.shape_width + self.padx
            x = self.padx
            y += self.shape_height + self.button_height + self.mini_pady + self.pady

        #calculation for creating upgradable :0
        x = self.padx
        remain_height = height / 3
        upgradable_width = (self.shape_width * 2 ) + self.padx
        upgradable_height = (remain_height - self.pady*2 ) // 2
        
        #setting up on canvas :0
        #main shape and button eastablization:0
        self.main_canvas.coords(
            self.upgradable_id[0],
            x , y ,
            x + upgradable_width, y + upgradable_height
        )
        
        x += upgradable_width + self.padx
        self.main_canvas.coords(
            self.upgradable_id[1],
            x , y ,
            x + self.shape_width, y + upgradable_height
        )
        self.main_canvas.coords(
            self.upgradable_text,
            (x + x + self.shape_width) // 2 ,
            (y + y + upgradable_height) // 2
        )
        
        dividiablex = upgradable_width / 3
        dividiabley = upgradable_height / 3
        new_width = (dividiablex * 2 ) / 5
        new_height = dividiabley * 2
        new_padx = dividiablex / 6
        new_pady = dividiabley / 2
        new_x = self.padx + new_padx
        new_y = y + new_pady
        # setting up the widget items ":0"
        for id in self.upgradable_id[2:]:
            self.main_canvas.coords( id ,
                new_x , new_y,
                new_x + new_width, new_y + new_height
            )
            new_x += new_width + new_padx
        
        # setting up footer things ---------
        x = self.padx
        y += self.pady + upgradable_height
        for number in range(3):
            self.main_canvas.coords(
                self.footer_shape_id[number],
                x , y ,
                x + self.shape_width, y + upgradable_height
            )
            self.main_canvas.coords(
                self.footer_text_id[number],
                (x + x + self.shape_width) / 2,
                (y + y + upgradable_height) / 2
            )
            x += self.shape_width + self.padx
        
        #binding keys
        self._bind_key_and_get_cords()
        print(self._button_coords)
    
    def change_window(self, data:dict, update_method:callable, save_method:callable) -> None:
        """
        Changes the window's content based on the provided data, save method, and update method.

        Parameters:
        data (dict): The data to be displayed in the window.
        save_method (callable): Method to save the current state of the window.
        update_method (callable): Method to update the canvas when an item is selected or upgraded.
        """
        
        self.current_data = data
        self.current_update_method = update_method
        self.current_save_method = save_method
        self.current_Sindex = 0
        
        self.set_to_defult()
        
        #adding data to items :0
        self._add_info_shopitems(self.current_data["items"][0:6])
        self._add_info_upgradable()
        self._bind_key_and_get_cords()
        
    def delete_window(self) -> None:
        """
        Deletes the current window and all its elements.
        """
        for id in self.shop_shape_id:
            self.main_canvas.delete(id)
        
        for id in self.shop_button_id:
            self.main_canvas.delete(id)
        
        for id in self.shape_text_id:
            self.main_canvas.delete(id)
        
        for id in self.button_text_id:
            self.main_canvas.delete(id)
        
        for id in self.upgradable_id:
            self.main_canvas.delete(id)
        
        self.main_canvas.delete(self.upgradable_text)
        
        # self._button_coords = None
    
    def set_to_defult(self) -> None:
        """
        Resets the window and all its elements to their default state.
        """
        for id in self.shop_shape_id:
            self.main_canvas.itemconfig(id,state = "hidden")
        
        for id in self.shop_button_id:
            self.main_canvas.itemconfig(id,state = "hidden")
        
        for id in self.shape_text_id:
            self.main_canvas.itemconfig(id,state = "hidden")
        
        for id in self.button_text_id:
            self.main_canvas.itemconfig(id,state = "hidden")
        
        if not self.current_data["upgradable"]:
            for id in self.upgradable_id:
                self.main_canvas.itemconfig(id,state = "hidden")
            
            self.main_canvas.itemconfig(
                self.upgradable_text,state = "hidden"
            )
    
    def add_to_window(self) -> None:
        self.main_canvas.pack()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# lol = Tk()
# var = Variable()

# var.PLAYERP_COINE = 10000000
# var.update()
# demo = {
#     "selected_index" : 0,
#     "items" : [
#         {"color":"#FFFFFF","selected":True, "purchased":True, "price":0},
#         {"color":"#333333","selected":False, "purchased":False, "price":200},
#         {"color":"#4B0082","selected":False, "purchased":False,"price":380},
#         {"color":"#2F4F4F","selected":False, "purchased":False, "price":230},
#         {"color":"#800000","selected":False, "purchased":False, "price":250},
#         {"color":"#000000", "selected":False, "purchased":True, "price":0},
#         {"color":"#F8F8FF","selected":False, "purchased":False, "price":380},
#         {"color":"#D3D3D3","selected":False, "purchased":False, "price":350},
#         {"color":"#FFD700","selected":False, "purchased":False, "price":500},
#         {"color":"#00FF00","selected":False, "purchased":False, "price":500}
#     ],
#     "upgradable" : 1 ,
#     "charge":0
# }

# lol202 = WindowCreator(lol , var, 200, 300)
# lol202.add_to_window()

# def something1(event):
#     print(event)
# def something2(event):
#     print(event)
# lol202.change_window(demo,something1, something2)


# lol.mainloop()