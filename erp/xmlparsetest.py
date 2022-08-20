import xmltodict
import json
from pprint import pprint

def main():
    with open("main/case_2_input_data.xml", "r", encoding="utf-8") as f:
        o = f.read()
        data = xmltodict.parse(o)
        pprint(json.dumps(data, ensure_ascii=False))

if __name__ == "__main__":
    main()