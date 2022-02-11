# Index
- [Index](#index)
- [Cmake environment setup bootstrapping with python](#cmake-environment-setup-bootstrapping-with-python)
  - [Cache modifier script](#cache-modifier-script)

# Cmake environment setup bootstrapping with python
This repo aims to provide Cmake with external development setup capabilities using Python.
This can surely be done with CMake scripting system, but I feel like having other means to edit the CMakeCache would be helpful and easier to handle with python rather than in plain CMake.

For now, the python script parses a CMakeCache.txt and looks for a TEST_PATH variable somewhere in it.
If none was found, a new entry is created and appended to the CMakeCache.txt.
Cmake then reads back the cache and regenerates it at each run (and it also reorders the variables at the same time)

## Cache modifier script
Essentially this script can be called independently from CMake ; in case a CMakeCache.txt exists at the targeted location, it is scanned and the new variable is appended in case it is missing from the cache.
Otherwise, when the cache does not exist, it creates a bare skeleton and adds the variable, which will be capture by CMake on next run.