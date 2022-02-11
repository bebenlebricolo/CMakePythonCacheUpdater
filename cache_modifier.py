import sys, os
import re
from pathlib import Path

from numpy import empty


class CacheParseException(Exception) :
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class CacheVar :
    name : str
    value : str
    kind : str

    def __init__(self, name : str = "", kind : str = "",  value : str = "") -> None:
        self.name = name
        self.value = value
        self.kind = kind

    def repr(self) -> None :
        return "CacheVar : name = {} ; kind = {} ; value = {}".format(self.name, self.kind, self.value)

    def from_line(self, line : str) -> None :
        pattern = re.compile("(.*):([A-Z]*)=(.*)")
        match = re.search(pattern, line)
        if match is not None :
            try :
                self.name = match.group(1) if match.group(1) is not None else ""
                self.kind = match.group(2) if match.group(2) is not None else ""
                self.value = match.group(3) if match.group(3) is not None else ""
            except Exception :
                raise CacheParseException("Could not parse line from CmakeCache : {}".format(line))

        if self.empty():
            print("Found empty with line : {}".format(line))

    def empty(self) -> bool :
        return self.kind == "" or self.name == ""

    def format(self) -> None :
        return "{}:{}={}".format(self.name, self.kind.upper(), self.value)



def parse_cached_vars(cache : Path) -> None :
    """Parses a CMakeCache.txt file and retrieves cached variables from it"""

    contents = list()
    try :
        with open(cache, 'r') as file :
            contents = file.readlines()
    except IOError as exception :
        print(exception)
        return

    cache_vars = list()
    for line in contents :
        stripped = line.lstrip()
        if not stripped.startswith("#") and not stripped.startswith("//") and not len(stripped) == 0:
            cache_var = CacheVar("","")
            try :
                cache_var.from_line(line)
            except CacheParseException :
                continue
            cache_vars.append(cache_var)

    return cache_vars


def append_variable_to_cache(cache : Path, var : CacheVar) -> None :
    try :
        with open(cache, "a") as file :
            file.write(var.format() + "\n")
    except IOError as exception :
        print(exception)



# Checking for variables in parsed CMakeCache.txt
if __name__ == "__main__" :
    if len(sys.argv) < 1 :
        print("Expected one argument : cache filepath")

    cache_filepath = Path(sys.argv[1])

    print("[DEBUG] : Current working dir is : {}".format(os.getcwd()))
    print("[DEBUG] : Cache file is located at : {}".format(cache_filepath))

    test_path_cache_var = CacheVar("TEST_PATH", "PATH", Path("/tmp/PackageManager/MyPackage/build"))

    # In case we run the script first, create a basic CMakeCache.txt that'll be read and updated by Cmake
    if not cache_filepath.exists() :
        print("{} does not exist yet, trying to create it then run Cmake".format(cache_filepath))
        append_variable_to_cache(cache_filepath, test_path_cache_var)
        exit(0)


    cached_vars = parse_cached_vars(cache_filepath)
    try :
        found_item = next(n for n in cached_vars if n.name == test_path_cache_var.name)
        print("Found my new path in cache !")
    except StopIteration:
        print("Adding variable")
        append_variable_to_cache(cache_filepath, test_path_cache_var)



