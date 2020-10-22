#!/usr/local/bin/python3

import os
import sys
import json

class NoteExtractor:
    def __init__(self):
        pass

    def write_help(self):
        print("Commands are written like this: NoteExtractor [command]")
        print("Available commands:")
        print("help - opens this dialog")
        print("name - only parses the file with this name")

    def extract(self, name=None):
        if name is not None:
            self._write_info(name)
        else:
            for f in os.scandir('.'):
                if f.path.endswith('.json') and f.is_file():
                    self._write_info(f.name)

    def _write_info(self, file):
        # Open json file and get data
        with open(file) as f:
            data = json.load(f)
            f.close()
        
        # Check for title and content
        try:
            data["title"]
            data["content"]
        except KeyError:
            # If no title or no content, return
            return

        # Create title of note
        title = "%s.md" % data["title"].replace("/", "_")

        # Check if note was in a directory
        directory = data["folderPathname"].split("/")
        if len(directory) > 1:
            directory = directory[1]
            dirs = []
            for f in os.scandir('.'):
                if f.is_dir():
                    dirs.append(f.name)

            if directory not in dirs:
                print("Make directory %s" % directory)
                os.mkdir(directory)
            
            path = os.path.join(os.getcwd(), directory, title)
        else:
            path = os.path.join(os.getcwd(), title)

        # Write data to file
        print("Writing file %s to %s" % (title, path))
        f = open(path, "w")
        f.write(data["content"])
        f.close()

if __name__ == "__main__":
    extract = NoteExtractor()

    # Parse command line
    if len(sys.argv) > 3:
        print("Too many arguments")
    elif len(sys.argv) < 3:
        extract.extract()
    elif sys.argv[2] == "help":
        extract.write_help()
    else:
        extract.extract(sys.argv[2])
    