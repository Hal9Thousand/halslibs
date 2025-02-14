from .hcli_menu import menu

class settings_menu:

    def __init__(self, default_settings : dict, current_settings : dict = {}, auto_start = True):
        """
        Initialize the settings menu object.

        :param default_settings: The default settings as a dictionary.
        :type default_settings: dict

        :param current_settings: The current settings as a dictionary. If not provided, it will be initialized as a copy of default_settings.
        :type current_settings: dict

        :param auto_start: An optional boolean indicating whether to start the menu automatically.
        :type auto_start: bool
        """
        self.default_settings = default_settings
        self.current_settings = current_settings.copy() if current_settings else default_settings

        if auto_start:
            self.start()
         
        self.default_settings : dict = default_settings
        self.current_settings : dict = current_settings

        if auto_start:
            self.start()

    def update_setting(self, setting_name : str):
        """
        Update the current setting value from user input.

        :param setting_name: The name of the setting to update.
        :type setting_name: str
        """ 

        default_value = self.default_settings[setting_name]
        if setting_name not in self.current_settings.keys(): 
            self.current_settings[setting_name] = default_value 
         
        if type(default_value) == bool: 
            if self.current_settings[setting_name] == False:
                self.current_settings[setting_name] = True
            else:
                self.current_settings[setting_name] = False 
        if type(default_value) == int: 
            try:
                new_value = int(input(f"Enter new value for '{setting_name}': "))
                self.current_settings[setting_name] = new_value
            except:
                print("Invalid Input") 
            
        if type(default_value) == list:
            option_select = menu(menu_items=default_value, name = f"set value for '{setting_name}'", auto_start = False).show()
            try:
                option_value = default_value[int(option_select)-1]
                self.current_settings[setting_name] = option_value
            except:
                print("Invalid Option")

    def main_loop(self):
        """
        Main loop of the settings menu.

        This method handles the main functionality of the menu, including displaying
        settings, updating settings, and exiting the menu.

        The loop continues until the user chooses to exit (by pressing ESC).
        """
        
        menu_items = []
        for key, default_value in self.default_settings.items():
            current_value = self.current_settings.get(key, default_value)
            if type(current_value) == list and len(current_value) > 0:
                current_value = current_value[0]
            label = f"{key}{' ' * (20 - len(key))}{current_value}" 
            menu_items.append([label])

        smenu = menu( menu_items=menu_items)
        user_input = smenu.show()
        if user_input != "ESC":
            try:
                setting_key = list(self.default_settings.keys())[int(user_input)-1]
                self.update_setting(setting_key)
            except ValueError:
                pass 

            self.main_loop()
            

    def start(self):
        """
        Start the settings menu.

        This method initializes the menu, displays the settings, and enters the main loop.
        Use this method to start the settings menu if auto_start is set to False.
        """
        self.main_loop()

