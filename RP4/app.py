import time
import requests
from pirc522 import RFID  # RFID Library for Raspberry Pi

# Setup RFID reader
rdr = RFID()

SERVER_URL = "http://192.168.178.189:5000/nfc-scan"  # Replace with your server IP

def scan_nfc_tag():
    rdr.wait_for_tag()
    (error, tag_type) = rdr.request()
    if not error:
        print("Tag detected")
        (error, uid) = rdr.anticoll()
        if not error:
            uid_str = "".join([str(i) for i in uid])
            print(f"UID: {uid_str}")
            return uid_str
    return None

def send_data_to_server(uid):
    data = {"uid": uid}
    try:
        response = requests.post(SERVER_URL, json=data)
        if response.status_code == 200:
            print("Data sent successfully!")
        else:
            print(f"Failed to send data: {response.status_code}")
    except Exception as e:
        print(f"Error sending data: {str(e)}")

def main():
    while True:
        uid = scan_nfc_tag()
        if uid:
            send_data_to_server(uid)
        time.sleep(2)

if __name__ == "__main__":
    main()
