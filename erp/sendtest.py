import requests
import time

def XMLsend(filename):
    with open(filename, "r") as f:
            xmlstr = f.read()
            headers = {'Content-Type': 'application/xml'}
            r = requests.post("http://127.0.0.1:1234/api/store/", data=xmlstr.encode('utf-8'), headers=headers)


if __name__ == "__main__":
    filename = "case_3_input_data.xml"
    print(f'sending xml named "{filename}" in 5 seconds...')
    time.sleep(5)
    print("sending...")
    XMLsend(filename)