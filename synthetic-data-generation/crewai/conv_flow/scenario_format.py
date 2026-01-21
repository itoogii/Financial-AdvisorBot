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
            obj, pos = decoder.raw_decode(content, pos)
            objects.append(obj)
        except json.JSONDecodeError:
            break
    
    with open(file_path, 'w') as f:
        json.dump(objects, f, indent=4)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scenario_format.py <path-to-file>")
        sys.exit(1)
    file_path = sys.argv[1]
    format_json(file_path)