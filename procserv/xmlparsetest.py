import xmltodict
import json
from pprint import pprint

def main():
    with open("case_2_input_data.xml", "r", encoding="utf-8") as f:
        o = f.read()
        data = xmltodict.parse(o)
        pprint(json.dumps(o))

if __name__ == "__main__":
    main()