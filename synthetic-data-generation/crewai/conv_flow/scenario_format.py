# This code fixes the JSON format for the original Scenario file. 
# I updated the main code to fix the issue at the source
# Kept the code for reference.
import json
import sys

def format_json(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    objects = []
    decoder = json.JSONDecoder()
    pos = 0
    while pos < len(content):
        try:
            # The raw_decode returns an object and the new position of the next object
            # so in the next iteration it will use the new position to retrieve the next object
            obj, pos = decoder.raw_decode(content, pos)
            objects.append(obj)
        except json.JSONDecodeError:
            break
    
    with open(file_path, 'w') as f:
        # the .dump serializes the objects[] to JSON string and writes it to the file
        json.dump(objects, f, indent=4)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scenario_format.py <path-to-file>")
        sys.exit(1)
    file_path = sys.argv[1]
    format_json(file_path)