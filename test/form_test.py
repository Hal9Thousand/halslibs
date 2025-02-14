import os, sys, json

current_dir = os.path.abspath(os.path.dirname(__file__))
src_dir = os.path.abspath(os.path.join(current_dir, "../"))
sys.path.append(src_dir) 
from src.halslibs import hcli 

data_sub_record = {
    "transaction_id": "TR0001",
    "details": "Transaction Details +1\nTransaction Details +2\nTransaction Details +1\nTransaction Details +4",
    "items": "Item 1\nItem 2",
}

sub_form = hcli.form(
    [
        hcli.form.field("transaction_id", 5, 1, 10, "ID"),
        hcli.form.field("details", 17, 1, 28),
        #hcli.form.field("items", 52, 1, 18),
    ],
    width=60,
    style=1,
) 

SubFormContent = sub_form.render(data_sub_record)
#print(SubFormContent)


TEXT = """
    ID          details                                   X
    TR0001tttt  Transaction Details +1dddddd              X
                Transaction Details +2dddddd              X
                Transaction Details +1dddddd              X
                Transaction Details +4dddddd              X
"""
data_record = {
    "id": "AT0001",
    "name": "TPS Report 573612",
    "details": "Value Added +1\nValue Added +2\nValue Added +1\nValue Added +4",
    "services": "Some Service\nAnother Service",
    "transactions":  SubFormContent,
} 

myform = hcli.form(
    [
        hcli.form.field("id", 5, 1, 10),
        hcli.form.field("name", 17, 1, 30),
        hcli.form.field("details", 5, 2, 18),
        hcli.form.field("services", 25, 2, 18),
        hcli.form.field("transactions", 52, 1, 82),
    ],
    style=1,
    width = 160
)

myform.show(data_record)
#print(SubFormContent)

import re

def remove_ansi(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

mytext = f"\033[31mHello\033[0m"
mytext2 = remove_ansi(mytext) 

print(mytext, len(mytext))  
print(mytext2, len(mytext2))