import json
import sys

with open("scenarios.json", "r") as f:
    scenarios = json.load(f)

def main():
    if len(sys.argv) < 2:
        print("Usage: python user_lookup.py <full_name>")
        sys.exit(1)
    full_name = sys.argv[1]
    try:
        index = (i for i, entry in enumerate(scenarios) if entry["user"].get("full_name") == full_name).__next__()
        print(f"Found '{full_name}' at index: {index}")
    except Exception as e:
        print(f"User '{full_name}' not found. error: {e}")


if __name__ == "__main__":
    main()