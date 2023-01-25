import json

mname = input("name: ")

with open('name.json', 'w') as file:
    json.dump(mname, file, indent=2, ensure_ascii=False)

    
with open('name.json', 'r') as file:
    pass
