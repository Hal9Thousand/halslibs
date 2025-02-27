class text:

    def __init__(self, **kwargs):
        """
        Initialize a text object with optional ANSI color and style settings.

        :param kwargs: Optional keyword arguments for color, background, bold, italic, underline, dim
        :type kwargs: dict
        
        """ 

        self.color: str = kwargs.get("color", None)
        self.background: str = kwargs.get("background", None) 
        self.bold: bool = kwargs.get("bold", False)
        self.italic: bool = kwargs.get("italic", False)
        self.underline: bool = kwargs.get("underline", False)
        self.dim: bool = kwargs.get("dim", False)

    def set(self, **kwargs):
        """
        Set ANSI color and style settings for this text object.

        :param kwargs: Optional keyword arguments for color, background, bold, italic, underline, dim
        :type kwargs: dict
        """

        self.color = kwargs.get("color", self.color)
        self.background = kwargs.get("background", self.background)  
        self.bold = kwargs.get("bold", self.bold)
        self.italic = kwargs.get("italic", self.italic)
        self.underline = kwargs.get("underline", self.underline)
        self.dim = kwargs.get("dim", self.dim)

    def reset(self):
        """
        Reset ANSI color and style settings to default.
        """
 
        return text.ansi_colors["format"]["reset"]

    class styles:
        """
        Class for ANSI color and style settings.
        """
        def get(style_category, style_name):
            """
            Return ANSI color code for a specific style.

            :param style_category: The category of the style (text, background, format).
            :type style_category: str

            :param style_name: The name of the style.
            :type style_name: str

            :return: ANSI color code for the specified style.
            :rtype: str
            """
 
            if (
                style_category in text.ansi_colors
                and style_name in text.ansi_colors[style_category]
            ):
                val = text.ansi_colors[style_category][style_name]
                return f"\033[{val}m"
            return ""

    def apply(self, text_string: str = None):
        """
        Apply ANSI color and style settings to the specified text string.

        :param text_string: The text to apply the settings to.
        :type text_string: str

        :return: The text string with ANSI color and style settings applied.
        :rtype: str
        """
        pre_format = text.styles.get("format", "bold") if self.bold else ""
        pre_format += text.styles.get("format", "italic") if self.italic else ""
        pre_format += text.styles.get("format", "underline") if self.underline else ""
        pre_format += text.styles.get("format", "dim") if self.dim else "" 
        pre_format += text.styles.get("text", self.color)
        pre_format += text.styles.get("background", self.background)

        post_format = text.styles.get("format", "reset")
 
        if text_string is not None:
            return f"{pre_format}{text_string}{post_format}"
        else:
            return pre_format

    def print(self, text_string: str):
        """
        Print the specified text string with ANSI color and style settings applied.

        :param text_string: The text to print.
        :type text_string: str
        """
        print(self.apply(text_string))

    def get_color(color: str, text_string: str):
        """
        Return ANSI color code for a specific text color.

        :param color: The text color.
        :type color: str

        :param text_string: The text to apply the color to.
        :type text_string: str

        :return: ANSI color code for the specified text color.
        :rtype: str
        """ 
        
        if color in text.ansi_colors["text"]:
            return f"{text.ansi_colors['text'][color]}{text_string}{text.ansi_colors['format']['reset']}"
        pass

    ansi_colors = {
        "text": {
            "black": "30",
            "gray": "90",
            "dark_red": "31",
            "red": "91",
            "dark_green": "32",
            "green": "92",
            "dark_yellow": "33",
            "yellow": "93",
            "dark_blue": "34",
            "blue": "94",
            "dark_magenta": "35",
            "magenta": "95",
            "dark_cyan": "36",
            "cyan": "96",
            "dark_white": "37",
            "white": "97",
        },
        "background": {
            "black": "40",
            "gray": "100",
            "dark_red": "41",
            "red": "101",
            "dark_green": "42",
            "green": "102",
            "dark_yellow": "43",
            "yellow": "103",
            "dark_blue": "44",
            "blue": "104",
            "dark_magenta": "45",
            "magenta": "105",
            "dark_cyan": "46",
            "cyan": "106",
            "dark_white": "47",
            "white": "107",
        },
        "format": {
            "reset": "0",
            "bold": "1",
            "dim": "2",
            "italic": "3",
            "underline": "4",
            "blink": "5",
            "inverted": "7",
            "hidden": "8",
        },
    }
