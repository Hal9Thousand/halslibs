from src.halslibs import hcli
from example_data.employee_directory import employee_directory
from example_data.product_inventory import product_inventory
from example_data.weather_data import weather_data
 
myform = hcli.form(
    [
        hcli.form.field("first", 3, 1, 18),
        hcli.form.field("last", 24, 1, 18),
        hcli.form.field("position", 3, 2, 18),
        hcli.form.field("department", 24, 2, 12), 
        hcli.form.field("phone", 3, 3, 12),
        hcli.form.field("email", 18, 3, 26),
    ]
)
text = myform.show(employee_directory[2])
