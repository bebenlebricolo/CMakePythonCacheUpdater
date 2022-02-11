cmake_minimum_required(VERSION 3.18)
project(toto CXX)

find_program(PythonExe "python")
add_custom_target( ExternalCacheUpdate ALL
        COMMAND ${PythonExe} ${CMAKE_SOURCE_DIR}/cache_modifier.py ${CMAKE_BINARY_DIR}/CMakeCache.txt
        WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
)

if(NOT TEST_PATH)
    message(STATUS "TEST_PATH was not found in cache :(")
else()
    message(STATUS "TEST_PATH was found in cache ! :) ")
endif()

