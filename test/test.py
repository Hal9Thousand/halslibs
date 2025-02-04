import os, sys, json

current_dir = os.path.abspath(os.path.dirname(__file__))
src_dir = os.path.abspath(os.path.join(current_dir, "../"))
sys.path.append(src_dir)
print(src_dir)
from src.halslibs import hcli

T = hcli.text(background="gray")
T.print("Hello, World!")
 
J = {
    "key": T.apply("Hello, World!"),
}
print(json.dumps(J).replace("\\u001b","\033"))
 