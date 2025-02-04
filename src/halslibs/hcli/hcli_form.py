from .hcli_text import text

class form:

    def __init__(self, template: dict):

        self.template = self.validate_template(template)
        self.max_form_width = 120
        self.labels = True

    def validate_template(self, template: dict):

        validated_template = {}
        for k, v in template.items():
            if len(v) > 1:
                validated_template[k] = [v[0], v[1]]
                other_options = v[2:] 
                
                label_text_lookup = list(o for o in other_options if isinstance(o, str))
                label_text = None
                if label_text_lookup:
                    label_text = label_text_lookup[0]
                else:
                    label_text = k

                    
                field_width_lookup = list(o for o in other_options if isinstance(o, int))
                field_width = None
                if field_width_lookup:
                    field_width = field_width_lookup[0]

                validated_template[k].append(field_width)
                validated_template[k].append(label_text)

        return validated_template

    def fill(self, data: dict):

        finished = False
        line = 0
        template = self.template.copy()
        for k, v in template.items():
            v[1] = v[1] * 3

        last_line = sorted(list(v[1] for k, v in template.items()))[-1] + 1
        
        label_format = text(italic=True, underline=True, color="yellow", dim=True)
        field_format = text(color="blue", bright=True, background="black", background_bright=True)

        while not finished:
            line += 1
            line_text = ""
            for col in range(1, self.max_form_width): 
                
                labels = list(
                    {'key': k, "template": v, "value" : k}
                    for k, v in  template.items()
                    if v[1] == line + 1 and col > v[0] and col <= len(v[3]) + v[0]
                )

                values = list(
                    {'key': k, "template": v, "value" : data[k]}
                    for k, v in  template.items()
                    if v[1] == line and col > v[0] and col <= len(str(data[k])) + v[0]
                )

                values = list(
                    {'key': k, "template": v, "value" : data[k]}
                    for k, v in  template.items()
                    if v[1] == line and col > v[0] and col <=  v[2] + v[0]
                )

                if len(labels) > 0: 

                    index = (col - labels[0]['template'][0]) - 1
                    #label_text = str(labels[0]['value'])
                    label_text = str(labels[0]['template'][3])
                    
                    if index == 0:
                        line_text += label_format.apply()
                    
                    line_text += label_text[index:index+1]

                    if index == len(label_text) - 1:
                        line_text += label_format.reset()
                else:
                    if len(values) > 0:
                        index = (col - values[0]['template'][0]) - 1 
                        value_text = str(values[0]['value'])
                        field_width = int(values[0]['template'][2]) if values[0]['template'][2] else len(value_text)
                        
                        if index == 0:
                            line_text += field_format.apply()

                        line_text +=  value_text[index:index+1]
                        if index >= len(value_text):
                            line_text += " "
                        if index == field_width - 1:
                            line_text += field_format.reset()
                    else:
                        line_text += " " 

            print(line_text)
            if line >= last_line:
                finished = True

        pass
