import re


class DataMaster:
    def __init__(self):
        self.sync = "#?#\n"
        self.sync_ok = "!"
        self.StartStream = "#A#\n"
        self.StopStream = "#S#\n"
        self.SynchChannel = 0

        self.requestCode = bytes.fromhex(
            "0202FF53FF00FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF03"
        )

        self.led_on = bytes.fromhex(
            "0201FF4CFF00FF01FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF03"
        )
        self.led_mood = bytes.fromhex(
            "0201FF4CFF00FF02FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF03"
        )
        self.led_off = bytes.fromhex(
            "0201FF4CFF00FF00FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF03"
        )

        self.temp = 0
        self.humi = 0
        self.co2 = 0
        self.ill = 0

        # self.save_data_state = False

    def ClearData(self):
        self.received_data = ""
        self.temp = 0
        self.humi = 0
        self.co2 = 0
        self.ill = 0

    def Decode(self):

        for i in range(len(self.received_data)):
            if (i % 2) == 0 and i != 0:
                self.received_data = self.received_data + ","
            self.received_data = self.received_data + self.received_data[i : i + 1]

        # print(self.received_data)

        packet = ""
        ETX = "ff,ff"

        packet += self.received_data

        def match(packet):
            pattern = re.compile(rf"{ETX}")
            if pattern.search(packet):
                return True
            else:
                return False

        def hex2dec(arr, first, last):
            result = ""

            for i in range(first, last + 1):
                result += str((int(arr[i]) - 30))
            return int(result)

        if match(packet):
            self.arr_receiveData = packet.split(",")
            # print(self.arr_receiveData)

            if len(self.arr_receiveData) == 30:
                if self.arr_receiveData[1] == "02":
                    self.temp = hex2dec(self.arr_receiveData, 10, 12) / 10
                    self.humi = hex2dec(self.arr_receiveData, 14, 16) / 10
                    self.co2 = hex2dec(self.arr_receiveData, 18, 21)
                    self.ill = hex2dec(self.arr_receiveData, 23, 26)

        if self.temp == 0 and self.humi == 0 and self.co2 == 0 and self.ill == 0:
            print("None")

        else:

            print("Temperature:", self.temp)
            print("Humidity:", self.humi)
            print("CO2:", self.co2)
            print("Illumination:", self.ill)
            print("\n\n")
