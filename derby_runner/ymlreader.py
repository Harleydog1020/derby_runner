import yaml

mfile = open("../resources/dr_menus.yml","r")
menusTxt: dict = yaml.safe_load(mfile)

print(menusTxt)

for x in menusTxt.values():
    for iKey, iValue in x.items():
        if iKey == "menulabel": print("Label is: ", iValue)
        else: print("Entry is:", iValue)

mfile.close()
