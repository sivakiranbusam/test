import yaml
import sys


myarglist = sys.argv
a_yaml_file = open(myarglist[2], "r")
parsed_yaml_file = yaml.load(a_yaml_file, Loader=yaml.FullLoader)
mylist = parsed_yaml_file["resources"]
for i in range(len(mylist)):
    if mylist[i].startswith(myarglist[3]):
        mylist[i] = myarglist[3] + myarglist[1]
        break
parsed_yaml_file["resources"] = mylist
a_yaml_file.close()
with open(myarglist[2], "w") as file:
    doc = yaml.dump(parsed_yaml_file, file, default_flow_style=False, sort_keys=False)
print(mylist[i])