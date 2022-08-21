import xmltodict
import json
from pprint import pprint

def main():
    with open("main/case_2_input_data.xml", "r", encoding="utf-8") as f:
        o = f.read()
        print(type(o))
        print(o)
        data = xmltodict.parse(o)
        j = json.dumps(data, ensure_ascii=False)
        # print(j)
        return data

if __name__ == "__main__":
    main()