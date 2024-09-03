import json
import tabulate
from collections import defaultdict

region = "en_US"

def loadJSON(filename):
    with open(f'ArknightsGameData_YoStar/{region}/gamedata/excel/{filename}') as f:
        return json.loads(f.read())

uniequip_json = loadJSON("uniequip_table.json")
stage_json = loadJSON("stage_table.json")
character_json = loadJSON("character_table.json")

modules = uniequip_json["equipDict"]
missions = uniequip_json["missionList"]
stages = stage_json["stages"]

modulesByStage = defaultdict(lambda: [])
for moduleID, body in modules.items():
    if "missionList" in body:
        for mission in body["missionList"]:
            for param in missions[mission]["paramList"]:
                if param in stages:
                    modulesByStage[param].append(moduleID)

total = 0

data = []
for mission, modulesThisMission in sorted(modulesByStage.items()):
    moduleDescriptions = [f'{character_json[modules[module]["charId"]]["name"]} {modules[module].get("typeName", None) or modules[module]["typeName1"] + "-" + modules[module]["typeName2"]}' for module in modulesThisMission]
    dataRow = [stages[mission]["code"], ", ".join(moduleDescriptions)]
    data.append(dataRow)

    total += len(modulesThisMission)

print(tabulate.tabulate(data))
print("{} total modules".format(total))
