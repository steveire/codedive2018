#!/usr/bin/env python

import os, sys
import json

basePath = os.path.abspath(sys.argv[1])

generatedCMake = """
add_custom_target(delfixes ALL
    COMMAND ${CMAKE_COMMAND} -E remove_directory ${CMAKE_CURRENT_BINARY_DIR}/fixes
)
"""

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

if True:
    basePath = os.path.abspath(sys.argv[1])

    cdb = os.path.join(basePath, "compile_commands.json")

    cppFiles = []
    objNames = []

    jsondb = json.load(open(cdb))

    for jsondict in jsondb:

        cppFile = jsondict["file"]

        if (cppFile.endswith(".cpp")):

            cppFiles.append(cppFile)

            objName = os.path.splitext(os.path.basename(cppFile))[0]
            objNames.append(objName)

    targetCount = 1

    for zipped in chunks(zip(cppFiles, objNames), 3):

        unzipped = zip(*zipped)

        cppFiles_ = unzipped[0]
        objNames_ = unzipped[1]

        objFiles = []

        targetName = os.path.basename(os.path.split(basePath)[0]) + "_" + os.path.basename(basePath) + str(targetCount)
        targetCount += 1

        for cpf, objn in zip(cppFiles_, objNames_):

            objf = "CMakeFiles/{targetName}.dir/{objName}.obj".format(targetName=targetName, objName=objn)
            objFiles.append("${CMAKE_CURRENT_BINARY_DIR}/" + objf)

            generatedCMake += """
set_source_files_properties(
    {cppFile}
#    PROPERTY COMPILE_FLAGS "-export-fixes={objFile}"
    PROPERTY COMPILE_FLAGS "-c -o {objFile}"
)
""".format(cppFile=cpf, objFile=objf)

        generatedCMake += """
add_library({targetName} SHARED
    {cppFiles}
)
add_dependencies({targetName} delfixes)
target_compile_options({targetName} PRIVATE
    ${{headerFilter}} ${{tidyChecks}} -p={basePath}
)
add_custom_command(TARGET {targetName} PRE_LINK
    COMMAND python ${{CMAKE_CURRENT_SOURCE_DIR}}/gatherFixes.py
    ${{CMAKE_CURRENT_BINARY_DIR}}
    {objFiles}
)
""".format(targetName=targetName,
    cppFiles='\n    '.join(cppFiles_),
    basePath=basePath.replace("\\", "/"),
    objFiles='\n    '.join(objFiles)
    )

with open("tidyCommands.cmake", "w") as auxFile:
    auxFile.write(generatedCMake)
