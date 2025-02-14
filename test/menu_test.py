import os, sys, json

current_dir = os.path.abspath(os.path.dirname(__file__))
src_dir = os.path.abspath(os.path.join(current_dir, "../"))
sys.path.append(src_dir)
from src.halslibs import hcli

mymenu = hcli.menu(
    [
        ["1", "Option 1", lambda: print("Option 1 selected")],
        ["2", "Option 2", lambda: print("Option 2 selected")] 
    ],
    prompt="Select:",
    name="My Menu",
    header="This is the header" 
)

mymenu.start()