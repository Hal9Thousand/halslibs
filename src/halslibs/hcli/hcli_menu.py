import os
import sys
import tty
import termios
import types 

class menu:
    """
    A simple console-based menu system.
    """

    def __init__(
        self,
        menu_items: list[list[str, str, callable]] = [
            ["1", "Add Menu Items...", None]
        ],
        **kwargs,
    ) -> None:
        """
        Initialize the menu object.

        This method sets up the menu with the provided items and additional options.

        Parameters:
        menu_items (list[list[str, str, callable]]): A list of menu items. Each item is a tuple containing:
            - A string representing the menu item key
            - A string representing the menu item description
            - A callable function to be executed when the item is selected
            Default is a single item prompting to add more menu items.

        **kwargs: Additional keyword arguments:
            - prompt (str): Custom prompt message (default: "Select an option:")
            - name (str): Name of the menu (default: "Main Menu")
            - auto_start (bool): If True, automatically start the menu after initialization (default: False)

        Returns:
        None
        """
        self.menu_items = self.validate_menu_items(menu_items)
        self.menu_prompt = kwargs.get("prompt", "Select an option:")
        self.menu_name = kwargs.get("name", "Main Menu")
        self.menu_header = kwargs.get("header", None)
        self.menu_footer = kwargs.get("footer", None)
        if kwargs.get("auto_start", False):
            self.start()

    def show(self):
        """
        Display the menu and prompt for user input.

        This method prints the menu name, lists all menu items with their corresponding keys,
        displays the menu prompt, and waits for user input.

        Returns:
        str: A single character representing the user's input. This can be either:
             - An uppercase letter or number corresponding to a menu item
             - "ESC" if the user pressed the Escape key
        """
        print(f"\n{self.menu_name}:\n")
        if self.menu_header:
            print(f'\n{self.menu_header}\n')
        for menu_item in self.menu_items: 
            key, value, callback = menu_item
            print(f"\t{key.upper()}. {value}")
        print("")

        print(f"{self.menu_prompt} ", end="", flush=True)
        return menu._get_single_key()

    def start(self):
        self.__main_loop() 

    def __main_loop(self):
        """
        Main loop of the menu system.

        This method handles the core functionality of the menu, including displaying
        options, processing user input, and executing callbacks.

        The loop continues until the user chooses to exit (by pressing ESC).

        Parameters:
        None

        Returns:
        None
        """
        user_input = self.show()
        print(f"{user_input}\n")
        if user_input == "ESC": 
            return

        menu_option = next((o for o in self.menu_items if o[0].upper() == user_input), None)

        if menu_option is not None:
            callback = menu_option[2]
            if callback is not None:
                callback()
            else:
                print(f"Option {user_input} is not available.")
        else:
            print("Invalid option. Please try again.")

        self.__main_loop()

    def confirm_sure()->bool:

        print("Aro You Sure? (y/n) ", end="", flush=True)
        if menu._get_single_key().upper() == "Y":
            print("Y")
            return True
        return False

    def _get_single_key():
        """
        Get a single keypress from the user without requiring Enter to be pressed.

        This method handles both Windows and Unix-like systems differently:
        - On Windows, it uses msvcrt to get a single character.
        - On Unix-like systems, it temporarily changes terminal settings to read a single character.

        The method also handles special cases:
        - Ctrl+C (^C) raises a KeyboardInterrupt
        - ESC key returns "ESC"

        Returns:
        str: A single character representing the key pressed by the user.
             For special keys:
             - "ESC" is returned for the Escape key

        Raises:
        KeyboardInterrupt: If Ctrl+C is pressed.
        """
        if os.name == 'nt':  # Windows
            import msvcrt
            key = msvcrt.getch()
            if key in (b'\x03',):  # Ctrl+C
                raise KeyboardInterrupt
            return key.decode('utf-8').upper()
        else:  # Unix/Linux/Mac
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                key = sys.stdin.read(1)
                if key == '\x1b':  # Check for the Escape Character

                    #tty.setcbreak(fd)  # Adjust to read more bytes without blocking
                    #print("Hit ESC again to exit this menu. ", end="", flush=True)
                    #additional_key = sys.stdin.read(1)
                    #if additional_key == '\x1b':
                        return "ESC"

                if key == '\x03':  # Ctrl+C
                    raise KeyboardInterrupt

                return key
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    
    def validate_menu_items(self, menu_items) -> list[list[str, str, callable]]:
        """
        Validate and format the menu items.

        This function processes the input menu items, ensuring they are in the correct format
        and have all necessary components. It assigns default values where needed and
        standardizes the structure of each menu item.

        Parameters:
        menu_items (list or any): The input menu items to be validated. If not a list,
                                  it will be converted to a single-item list.

        Returns:
        list[list[str, str, callable]]: A list of validated menu items, where each item is a list containing:
            - A string representing the menu item key (a single character or number)
            - A string representing the menu item description
            - A callable function to be executed when the item is selected (or None if not provided)

        """
        def is_lambda_function(obj):

            return isinstance(obj, types.LambdaType) and obj.__name__ == "<lambda>"

        validated_menu_items = []

        if type(menu_items) is not list:
            menu_items = [menu_items]

        default_menu_id = 0
        for menu_item in menu_items: 

            default_menu_id += 1
            menu_item_params = menu_item if type(menu_item) is list else [menu_item] 
            menu_item_id = next(
                (s.upper() for s in menu_item_params if type(s) is str and len(s) == 1),
                str(default_menu_id),
            )
            menu_item__callback = next(
                (c for c in menu_item_params if callable(c)),
                None,
            )

            default_menu_title = (
                f"Option {menu_item_id}"
                if menu_item__callback is None
                or is_lambda_function(menu_item__callback)
                else menu_item__callback.__name__
            )
            menu_item__title = next(
                (s for s in menu_item_params if type(s) is str and len(s) > 1),
                default_menu_title,
            )
            validated_menu_item = [
                f"{menu_item_id}",
                menu_item__title,
                menu_item__callback,
            ] 
            validated_menu_items.append(validated_menu_item)

        return validated_menu_items