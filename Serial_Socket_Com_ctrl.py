import serial.tools.list_ports
import time
import socketio


class SerialCtrl:
    def __init__(self):
        self.com_list = []
        # self.socket_connect = False

        # my
        self.led_state = "OFF"

        # Connect to the server
        self.sio = socketio.Client()

        self.connect()

    def connect(self):
        @self.sio.event
        def connect():
            print("Connected to server")

        @self.sio.event
        def disconnect():
            print("Disconnected from server")

        @self.sio.on("ledState")
        def handle_ledON(data):
            self.led_state = data
            print("LED State :", data)

        # socket connect to the server once the serial comm established
        self.sio.connect("http://10.2.24.16:8000")
        self.socket_connect = True

        # Send a message to the server
        self.sio.emit("message", "Hello from the client!")

    def getCOMList(self):
        ports = serial.tools.list_ports.comports()
        self.com_list = [com[0] for com in ports]
        self.com_list.insert(0, "-")

    def SerialOpen(self, ComGUI):
        self.ComGUI = ComGUI
        try:
            self.ser.is_open
        except:
            PORT = ComGUI.clicked_com.get()
            BAUD = ComGUI.clicked_bd.get()
            self.ser = serial.Serial()
            self.ser.port = PORT
            self.ser.baudrate = BAUD
            self.ser.timeout = 0.1  # 100ms

        try:
            if self.ser.is_open:
                self.ser.status = True
            else:
                PORT = ComGUI.clicked_com.get()
                BAUD = ComGUI.clicked_bd.get()
                self.ser = serial.Serial()
                self.ser.port = PORT
                self.ser.baudrate = BAUD
                self.ser.timeout = 0.1  # 100ms

                self.ser.open()
                self.ser.status = True

        except:
            self.ser.status = False

    def SerialClose(self):
        self.ser.close()
        self.ser.status = False

    def SerialComm(self, gui):
        self.threading = True

        while True:
            if self.threading:
                gui.conn.connection_status["text"] = "OK"
                gui.conn.connection_status["fg"] = "green"

                self.ser.write(gui.data.requestCode)

                gui.data.received_data = self.ser.readline().hex()
                # print(gui.data.received_data)
                if len(gui.data.received_data) > 0:
                    gui.conn.receiving_data_status["text"] = "Receiving.."
                    gui.conn.receiving_data_status["fg"] = "green"

                    # print("[Receiving] ", True)
                    gui.conn.btn_start_stream["state"] = "active"
                    # gui.conn.save_check["state"] = "active"

                    print("[CONNECTED] Ready To Stream!")
                    self.threading = False

                    break

                time.sleep(1)

            else:
                self.SerialClose()
                print("Serial Port closed")
                print("[Threading]", self.threading)

                # Disconnect from the server
                self.sio.disconnect()
                self.socket_connect = False
                break

            time.sleep(1)

    def SerialDataStream(self, gui):
        self.threading = True

        # connect or reconnect(when socketio is closed) to the server
        if self.socket_connect == False:
            self.sio.connect("http://10.2.24.16:8000")

        while True:
            if self.threading:
                self.SerialOpen(self.ComGUI)

                # led controller
                if self.led_state == "ON":
                    self.ser.write(gui.data.led_on)
                    # update led_color
                    gui.display.led_status["fg"] = "green"

                    # send to the server
                    self.sio.emit("message", self.led_state)

                elif self.led_state == "MOOD":
                    self.ser.write(gui.data.led_mood)
                    # update led_color
                    gui.display.led_status["fg"] = "orange"

                    # send to the server
                    self.sio.emit("message", self.led_state)

                elif self.led_state == "OFF":
                    self.ser.write(gui.data.led_off)
                    # update led_color
                    gui.display.led_status["fg"] = "red"

                    # send to the server
                    self.sio.emit("message", self.led_state)

                self.ser.write(gui.data.requestCode)
                gui.data.received_data = self.ser.readline().hex()
                gui.data.Decode()
                gui.display.temp_label["text"] = f"Temperature[℃] : {gui.data.temp}"
                gui.display.humi_label["text"] = f"Humidity[%] : {gui.data.humi}"
                gui.display.co2_label["text"] = f"CO2[ppm] : {gui.data.co2}"
                gui.display.ill_label["text"] = f"Illumination[lx] : {gui.data.ill}"

                gui.display.led_status["text"] = f"LED status : {self.led_state}"

                # bar chart update
                gui.display.bar_chart()

                # socketio
                data = {
                    "temp": gui.data.temp,
                    "humi": gui.data.humi,
                    "co2": gui.data.co2,
                    "ill": gui.data.ill,
                }
                self.sio.emit("message", data)

            else:

                gui.data.ClearData()

                if gui.display.all_frame_close == False:
                    gui.display.temp_label["text"] = f"Temperature[℃] : {gui.data.temp}"
                    gui.display.humi_label["text"] = f"Humidity[%] : {gui.data.humi}"
                    gui.display.co2_label["text"] = f"CO2[ppm] : {gui.data.co2}"
                    gui.display.ill_label["text"] = f"Illumination[lx] : {gui.data.ill}"

                    # open serial port if close to write led off
                    self.SerialOpen(self.ComGUI)
                    self.ser.write(gui.data.led_off)
                    gui.display.led_status["text"] = f"LED status : OFF"
                    gui.display.led_status["fg"] = "red"

                    gui.display.canvas.delete("all")

                # socketio
                data = {
                    "temp": gui.data.temp,
                    "humi": gui.data.humi,
                    "co2": gui.data.co2,
                    "ill": gui.data.ill,
                }
                self.sio.emit("message", data)

                self.sio.disconnect()
                self.socket_connect = False
                self.SerialClose()
                print("Serial Closed")
                print("[Threading]", self.threading)
                break
            time.sleep(1)


if __name__ == "__main__":
    SerialCtrl()
