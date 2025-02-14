import types
import copy
import re
from .hcli_text import text

class form:
    """
    A form builder class for generating text-based forms.
    """

    class field:
        """
        A field object for the form.
        """

        def __init__(self, field_name: str, x : int = 1, y : int = 1, width: int = 0, label : str = None):
            """
            Initialize a field object.

            :param field_name: The name of the field.
            :type field_name: str

            :param x: The horizontal position of the field.
            :type x: int

            :param y: The vertical position of the field.
            :type y: int

            :param width: The width of the field.
            :type width: int

            :param label: The label for the field.
            :type label: str
            """
            self.field_name : str = field_name
            self.x : int = x
            self.y : int = y
            self.width : str = width
            self.label : str = label if label is not None else self.field_name

    class style:

        def __init__(self, text_color: str = "white", cell_color : str = "black", form_color: str = "gray", label_color: str = "white"):
            """
            Initialize form style.

            :param text_color: The text color for the form.
            :type text_color: str

            :param cell_color: The cell color for the form.
            :type cell_color: str

            :param form_color: The form color.
            :type form_color: str

            :param label_color: The label color for the form.
            :type label_color: str
            """
            
            self.text_color : text = text(color=text_color, background=cell_color) 
            self.form_color : text = text(background=form_color)
            self.label_color : text = text(color=label_color, dim=True, italic=True)

    def __init__(self, fields: list[field], width: int = None, style : int = 0):
        """
        Initialize a form builder.

        :param fields: A list of field objects.
        :type fields: list[form.field]

        :param width: The maximum width of the form.
        :type width: int

        :param style: The index of the form style to use.
        :type style: int
        """
        
        self.labels = True
        self.fields : list[form.field] = fields
        self.max_form_width = width if width is not None else self.__find_width()
        styles : list[form.style] = [
            form.style(), 
            form.style(text_color="cyan", cell_color="black", form_color="dark_blue", label_color="cyan") 
        ]
        self.form_style : form.style = styles[style]

    def __find_width(self) -> int:
        """
        Find the maximum width of the form based on the farthest right position of the fields.

        :return: The maximum width of the form.
        :rtype: int
        """ 
        farthest_right = sorted(list(field.x + field.width for field in self.fields))[-1] + 1
        return farthest_right + 2

    def show(self, data: dict):
        """
        Show the form with the given data.

        :param data: The data to populate the form with.
        :type data: dict
        """
        print(self.render(data))

    def render(self, data_record: dict = {}) -> str:
        """
        Render the form with the given data.

        :param data: The data to populate the form with.
        :type data: dict
        :return: The rendered form.
        :rtype: str
        """
        finished = False
        line = 0 
        form_lines: list[str] = []
        data = data_record.copy()
        template_fields : list[form.field] = []
        for field in self.fields:
            template_fields.append(
                form.field(
                    field_name=field.field_name,
                    x=field.x,
                    y=field.y,
                    width=field.width,
                    label=field.label, 
                )
            ) 
        labels = True
        if labels:
            for field in template_fields: 
                field.y = field.y * 3
         
        
        extra_cell_lines = []
        for field in template_fields:
            if field.field_name in data: 

                def is_lambda_function(obj): 
                    return isinstance(obj, types.LambdaType) and obj.__name__ == "<lambda>"

                field_Value =  data[field.field_name]() if is_lambda_function(data[field.field_name]) else data[field.field_name] 
                field_lines = field_Value.split("\n")
                if len(field_lines) >  0:
                    data[field.field_name] = field_lines[0]
                    for fx in range(1, len(field_lines)):
                        extra_cell_name = f"{field.field_name}__{fx}"
                        data[extra_cell_name] = field_lines[fx]
                        extra_cell_field = form.field(extra_cell_name, x = field.x, y=field.y + fx, width=field.width, label=None)
                        extra_cell_lines.append(extra_cell_field)

        render_fields = [field for field in template_fields + extra_cell_lines]
        
        last_line = sorted(list(field.y for field in render_fields))[-1] + 1 

        while not finished:
            line += 1
            line_text = self.form_style.form_color.apply()

            for col in range(1, self.max_form_width): 
                
                labels = list(
                    field
                    for field in template_fields
                    if field.field_name in data
                    and field.label is not None
                    and field.y == line + 1
                    and col > field.x
                    and col <= len(field.label) + field.x
                ) 
                

                if len(labels) > 0:

                    index = (col - labels[0].x) - 1  
                    if index == 0: 
                        line_text += self.form_style.label_color.apply()

                    line_text += labels[0].label[index : index + 1]

                    if index == len(labels[0].label) - 1:
                        line_text += text.styles.get("format", "reset")
                        line_text += self.form_style.form_color.apply()
                else:

                    def remove_ansi(text):
                        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
                        return ansi_escape.sub('', str(text)) 
                
                    def value_width(field: form.field) -> int: 
                        return field.width if field.width > 0 else len(remove_ansi(data[field.field_name])) 
                     
                    values = list(
                        field
                        for field in render_fields
                        if field.field_name in data
                        and field.y == line
                        and col > field.x
                        and col <= field.x + value_width(field)
                    )
                    
                    if len(values) > 0:
                        index = (col - values[0].x) - 1
                        value_text = str(data[values[0].field_name])
                        field_width = value_width(values[0]) 

                        if index == 0:
                            line_text += text.styles.get("format", "reset")
                            line_text += self.form_style.text_color.apply() 

                        line_text += value_text[index : index + 1]
                        if index >= len(remove_ansi(value_text)):
                            line_text += values[0].field_name[0] # "."
                        if index == field_width - 1: 
                            line_text += text.styles.get("format", "reset")
                            line_text += self.form_style.form_color.apply()
                    else:
                        line_text += " "

            line_text += text.styles.get("format", "reset") + "X"
            form_lines.append(line_text)
            if line >= last_line:
                finished = True
         
        return "\n".join(form_lines)
