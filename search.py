#!/usr/bin/env python3
from subprocess import run
from pathlib import Path
import os, sys

def rgrep(root_dir: str, pattern: str):
    """
    Perform recursive grep relative to root_dir
    """
    old_cwd = Path.cwd()
    os.chdir(root_dir)
    cmd = ["grep", "-r", pattern]
    res = run(cmd, text=True, capture_output=True, check=True)
    os.chdir(old_cwd)
    return res.stdout.splitlines(False)

def parse_grep(lines: 'list[str]', delim: str):
    """
    Parse lines of grep result as <filename>:<delim><token>
    and return {filename:[token]}
    """
    res = dict() # type: dict[str, list[str]]
    for line in lines:
        if not line.startswith("Binary file"):
            fsplit = line.split(':', 1)
            index = fsplit[1].find(delim) + len(delim)

            fname = fsplit[0]
            match = fsplit[1][index:].strip()
            if fname in res:
                res[fname].append(match)
            else:
                res[fname] = [match]

    return res

def find_dupes(map: 'dict[Any, list]'):
    """
    Find duplicate entries in a list for each key
    """
    res = dict() # type: dict[Any, list]
    for key in map:
        was_found = set()
        for entry in map[key]:
            if entry in was_found:
                if key in res:
                    res[key].append(entry)
                else:
                    res[key] = [entry]
            else:
                was_found.add(entry)


    return res

def main():
    if len(sys.argv) != 2:
        exit(f"Usage: {sys.argv[0]} <proj root>")

    target_dir = Path(sys.argv[1])
    if not target_dir.is_dir():
        exit(f"{target_dir} is not a valid directory")

    c_incl_pat = "#\s*include\s\{1,\}" # Using standard regex for + operator
    grep_res = rgrep(target_dir, c_incl_pat)
    parse_res = parse_grep(grep_res, "include")
    results = find_dupes(parse_res)
    for file in results:
        print(file)
        for dupe in results[file]:
            print(f"\t{dupe}")
        print()

if __name__ == "__main__":
    main()
