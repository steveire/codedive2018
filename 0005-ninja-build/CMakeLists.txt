
# cmake .. -G Ninja -DCMAKE_CXX_COMPILER=/home/steveire/dev/prefix/clang/bin/clang-tidy

cmake_minimum_required(VERSION 3.9)
project(ctninja NONE)

# Set to the location of the compile_commands.json file
set(COMPDB_DIR "/home/steveire/dev/src/llvm/build")
set(headerFilter -header-filter=llvm)
set(tidyChecks "-checks=-*,misc-my-first-check")


# For Exposition Only CMake Hacks - Never do this!
set(CMAKE_CXX_COMPILER_WORKS 1)
# Override linker to just echo the 'object files'
set(CMAKE_CXX_CREATE_SHARED_LIBRARY "\"${CMAKE_COMMAND}\" -E echo <OBJECTS>")
set(CMAKE_CXX_COMPILE_OBJECT "<CMAKE_CXX_COMPILER> <FLAGS> <SOURCE>")

enable_language(CXX)

set(CMAKE_DEPFILE_FLAGS_CXX)
set(CMAKE_POSITION_INDEPENDENT_CODE OFF)

execute_process(COMMAND
    python
    ${CMAKE_SOURCE_DIR}/ctgenerator.py
    ${COMPDB_DIR}
    RESULT_VARIABLE outRes
    OUTPUT_VARIABLE cmdOut
)

include(${CMAKE_CURRENT_BINARY_DIR}/tidyCommands.cmake)
