#!/usr/bin/env python

import os, sys, shutil
import json
import re
from collections import defaultdict
import subprocess
import yaml


def fixYamlPaths(yamlFile):
    handle = open(yamlFile, 'r')
    content = yaml.safe_load(handle)
    handle.close()

    if not content:
        return

    ytree = content.get("Diagnostics", [])

    if not ytree:
        return

    for i, item in enumerate(ytree):
        content["Diagnostics"][i]["FilePath"] = os.path.abspath(item["FilePath"])
            
        if not item["Replacements"]:
            continue

        for ri, r in enumerate(item["Replacements"]):
            content["Diagnostics"][i]["Replacements"][ri]["FilePath"] = os.path.abspath(r["FilePath"])

    os.path.splitext(yamlFile)
    newYamlFile = os.path.join(sys.argv[1], "fixes", os.path.relpath(os.path.splitext(yamlFile)[0], sys.argv[1])) + ".yaml"
    newYamlFile = newYamlFile.replace("\\", "/")
    
    try:
        os.makedirs(os.path.abspath(os.path.join(newYamlFile, os.pardir)).replace("\\", "/"))
    except:
        pass

    with open(newYamlFile, 'w') as out:
      yaml.safe_dump(content, out, width=1000)

for arg in sys.argv[2:]:
    if os.path.exists(arg):
        fixYamlPaths(arg)
