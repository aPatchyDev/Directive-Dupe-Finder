# Directive Dupe Finder

A simple python script using grep to scan a C/C++ project for duplicated #include directives.

This script only finds potential candidates, organized by file.  
It makes no guarantees whether the statement is actually redundant or not.  
It does not even differentiate plain text from source code.

Therefore, you must review each search result to check whether they are actually redundant or not.

### Usage
`./search.py <path to project root>`
