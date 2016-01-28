"""Until Dynamo team find a better solution this file creates a pkg.json file for Ladybug."""
import json
import os

def createPkg(definitionsPath):
    ladybugData = {"license":"GPL.V3",
                    "file_hash":None,
                    "name":"Ladybug",
                    "version":"0.0.1",
                    "description":"Ladybug is an environmental analysis plugin.",
                    "group":"Ladybug Analysis Tools",
                    "keywords":["ladybug","environmental","analysis","sunpath", "radition", "solar"],
                    "dependencies":[],
                    "contents": "",
                    "engine_version":"0.9.1.3872",
                    "engine":"dynamo",
                    "engine_metadata":"",
                    "site_url":"https://www.facebook.com/LadybugAnalysisTools",
                    "repository_url":"https://github.com/ladybug-analysis-tools/ladybug-dynamo",
                    "contains_binaries":False,
                    "node_libraries":[]}

    contents = []
    #each definition should go as
    # " name - description" separated by ,"
    files = os.listdir(definitionsPath)
    for f in files:
        _fullpath = os.path.join(definitionsPath, f)
        if not os.path.isfile(_fullpath): continue
        with open(_fullpath, "rb") as dyf:
            l = dyf.readline()
            name = l.split('Name=')[-1].split("Description")[0].strip()[1:-1]
            description = l.split('Description=')[-1].split("ID")[0].strip()[1:-1]
            contents.append(" " + name + " - " + description)

    ladybugData["contents"] = ",".join(contents)

    with open(os.path.join(definitionsPath + "\\pkg.json"), "wb") as pkg:
        json.dump(ladybugData, pkg)

path = r"C:\Users\Administrator\Desktop\Dynamo Backup\0.9\definitions"
createPkg(path)
