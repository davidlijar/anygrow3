from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class RootGUI:
    def __init__(self, serial, data):
        self.root = Tk()
        self.root.title("Serial Communication")
        self.root.geometry("360x120")
        self.root.config(bg="white")

        self.serial = serial
        self.data = data

        self.root.protocol("WM_DELETE_WINDOW", self.close_window)

    def close_window(self):
        print("Closing the window and exit")
        self.root.destroy()
        self.serial.SerialClose()
        self.serial.threading = False
        self.data.ClearData()


class ComGui:
    def __init__(self, root, serial, data):
        self.root = root
        self.serial = serial
        self.data = data

        self.pady = 15
        self.padx = 20

        self.frame = LabelFrame(
            root, text="Com Manager", width=60, padx=5, pady=5, bg="white"
        )
        self.label_com = Label(
            self.frame, text="Available Port(s): ", bg="white", width=15, anchor="w"
        )

        self.label_bd = Label(
            self.frame, text="Baude Rate: ", bg="white", width=15, anchor="w"
        )

        self.comOptionMenu()
        self.baudOptionMenu()

        self.btn_refresh = Button(
            self.frame, text="Refresh", width=10, command=self.com_refresh
        )
        self.btn_connect = Button(
            self.frame,
            text="Connect",
            width=10,
            state="disabled",
            command=self.serial_connect,
        )

        self.padx = 20
        self.pady = 5
        self.public()

    def public(self):
        self.frame.grid(row=0, column=0, rowspan=3, columnspan=3, padx=5, pady=5)
        self.label_com.grid(column=1, row=2)
        self.drop_com.grid(column=2, row=2)
        self.label_bd.grid(column=1, row=3, pady=self.pady)
        self.drop_bd.grid(column=2, row=3, pady=self.pady)

        self.btn_refresh.grid(column=3, row=2)
        self.btn_connect.grid(column=3, row=3, pady=self.pady)

    def comOptionMenu(self):
        self.serial.getCOMList()  # to get available serial ports
        coms = self.serial.com_list
        self.clicked_com = StringVar()
        self.clicked_com.set(coms[0])
        self.drop_com = OptionMenu(
            self.frame, self.clicked_com, *coms, command=self.connect_ctrl
        )
        self.drop_com.config(width=10)

    def baudOptionMenu(self):
        bds = [
            "-",
            "300",
            "600",
            "1200",
            "2400",
            "4800",
            "9600",
            "14400",
            "19200",
            "28800",
            "38400",
            "56000",
            "57600",
            "115200",
            "256000",
        ]
        self.clicked_bd = StringVar()
        self.clicked_bd.set(bds[0])
        self.drop_bd = OptionMenu(
            self.frame, self.clicked_bd, *bds, command=self.connect_ctrl
        )
        self.drop_bd.config(width=10)

    def connect_ctrl(self, other):
        print("Connect Ctrl")
        if "-" in self.clicked_com.get() or "-" in self.clicked_bd.get():
            self.btn_connect["state"] = "disable"
        else:
            self.btn_connect["state"] = "active"

    def com_refresh(self):
        self.drop_com.destroy()
        self.comOptionMenu()
        self.drop_com.grid(column=2, row=2)

        logic = []
        self.connect_ctrl(logic)

    def serial_connect(self):
        if self.btn_connect["text"] in "Connect":
            self.serial.SerialOpen(self)
            if self.serial.ser.status:
                self.btn_connect["text"] = "Disconnect"
                self.btn_refresh["state"] = "disable"
                self.drop_bd["state"] = "disable"
                self.drop_com["state"] = "disable"

                InfoMsg = f"Successful UART connection using {self.clicked_com.get()}"
                messagebox.showinfo("Showinfo", InfoMsg)

                self.conn = ConnGUI(self.root, self.serial, self.data)

                self.serial.t1 = threading.Thread(
                    target=self.serial.SerialComm, args=(self,), daemon=True
                )
                self.serial.t1.start()
            else:
                ErrorMsg = f"Failure to establish UART connection using {self.clicked_com.get()}"
                messagebox.showerror("Showerror", ErrorMsg)
        else:
            self.serial.threading = False
            self.serial.SerialClose()
            self.conn.ConnGUIClose()

            self.conn.display.DisGUIClose()
            self.conn.display.all_frame_close = True
            self.data.ClearData()

            print("Disconnected")

            InfoMsg = f"UART connection using {self.clicked_com.get()} is now closed"
            messagebox.showwarning("Showinfo", InfoMsg)

            self.btn_connect["text"] = "Connect"
            self.btn_refresh["state"] = "active"
            self.drop_bd["state"] = "active"
            self.drop_com["state"] = "active"


class ConnGUI:
    def __init__(self, root, serial, data):
        self.root = root
        self.serial = serial
        self.data = data

        self.pady = 15
        self.padx = 20

        self.frame = LabelFrame(
            root, text="Connection Manager", padx=5, pady=5, bg="white", width=60
        )

        self.connection_label = Label(
            self.frame, text="Connection Status: ", bg="white", width=15, anchor="w"
        )
        self.connection_status = Label(
            self.frame, text="....", bg="white", fg="orange", width=5
        )

        self.receiving_label = Label(
            self.frame, text="Receiving Data: ", bg="white", width=15, anchor="w"
        )
        self.receiving_data_status = Label(
            self.frame, text="...", bg="white", fg="orange", width=10, anchor="w"
        )

        self.btn_start_stream = Button(
            self.frame,
            text="Start",
            state="disabled",
            width=5,
            command=self.start_stream,
        )
        self.btn_stop_stream = Button(
            self.frame, text="Stop", state="disabled", width=5, command=self.stop_stream
        )

        # self.save = False
        # self.SaveVar = IntVar()
        # self.save_check = Checkbutton(
        #     self.frame,
        #     text="Save data",
        #     variable=self.SaveVar,
        #     onvalue=1,
        #     offvalue=0,
        #     bg="white",
        #     state="disabled",
        #     command=self.save_data,
        # )

        self.ConnGUIOpen()

    def ConnGUIOpen(self):
        self.root.geometry("650x120")
        self.frame.grid(row=0, column=4, rowspan=3, columnspan=5, padx=5, pady=5)
        self.connection_label.grid(column=1, row=1)
        self.connection_status.grid(column=2, row=1)

        self.receiving_label.grid(row=2, column=1)
        self.receiving_data_status.grid(row=2, column=2, pady=self.pady)

        self.btn_start_stream.grid(column=3, row=1, padx=self.padx)
        self.btn_stop_stream.grid(column=3, row=2, padx=self.padx)

        # self.save_check.grid(column=4, row=2, columnspan=2)

    def ConnGUIClose(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.destroy()
        self.root.geometry("360x120")

    def start_stream(self):
        self.display = DisGUI(self.root, self.serial, self.data)

        self.btn_start_stream["state"] = "disabled"
        self.btn_stop_stream["state"] = "active"
        self.serial.t1 = threading.Thread(
            target=self.serial.SerialDataStream, args=(self,), daemon=True
        )
        self.serial.t1.start()

        self.display.bar_chart()

    def stop_stream(self):
        self.btn_start_stream["state"] = "active"
        self.btn_stop_stream["state"] = "disabled"

        self.display.led_state = "OFF"
        self.serial.threading = False

    # def save_data(self):
    #     if self.SaveVar.get() == 1:
    #         self.data.save_data_state = True
    #     else:
    #         self.data.save_data_state = False


class DisGUI:
    def __init__(self, root, serial, data):
        self.root = root
        self.serial = serial
        self.data = data

        # check if all frames are closed
        self.all_frame_close = False

        self.DisFrame = LabelFrame(root, text=" Sensor Data", width=120)
        self.sensor_frame = LabelFrame(self.DisFrame, text="Live Sensor Data")
        self.graph_frame = LabelFrame(self.DisFrame, text="Graph")

        self.temp_label = Label(
            self.sensor_frame, text=f"Temperature[℃] : ", width=20, anchor="w", fg="red"
        )
        self.humi_label = Label(
            self.sensor_frame, text=f"Humidity[%] : ", width=20, anchor="w", fg="orange"
        )
        self.co2_label = Label(
            self.sensor_frame, text=f"CO2[ppm] : ", width=20, anchor="w", fg="green"
        )
        self.ill_label = Label(
            self.sensor_frame,
            text=f"Illumination[lx] : ",
            width=20,
            anchor="w",
            fg="blue",
        )

        # LED controller
        self.serial.led_state = "OFF"

        self.led_frame = LabelFrame(self.DisFrame, text="LED Controller")
        self.led_on_btn = Button(
            self.led_frame,
            text="LED ON",
            width=10,
            fg="green",
            command=lambda: self.led_handler("ON", "green"),
        )
        self.led_mood_btn = Button(
            self.led_frame,
            text="LED MOOD",
            width=10,
            fg="orange",
            command=lambda: self.led_handler("MOOD", "orange"),
        )
        self.led_off_btn = Button(
            self.led_frame,
            text="LED OFF",
            width=10,
            fg="red",
            command=lambda: self.led_handler("OFF", "red"),
        )
        self.led_status = Label(
            self.led_frame, text="LED status : ", width=15, anchor="w", fg="red"
        )

        self.DisGUIOpen()

    def DisGUIOpen(self):
        self.root.geometry("650x400")
        self.DisFrame.grid(row=3, column=0, columnspan=10, padx=10, pady=10)

        self.sensor_frame.grid(row=0, rowspan=5, column=0, padx=5, pady=5)
        self.temp_label.grid(row=0, column=0, padx=5, pady=5)
        self.humi_label.grid(row=1, column=0, padx=5, pady=5)
        self.co2_label.grid(row=2, column=0, padx=5, pady=5)
        self.ill_label.grid(row=3, column=0, padx=5, pady=5)

        self.graph_frame.grid(row=0, column=1, columnspan=4, padx=10, pady=5)

        self.led_frame.grid(row=0, column=10, rowspan=4, padx=10, pady=5)
        self.led_on_btn.grid(row=0, column=0, padx=5, pady=5)
        self.led_mood_btn.grid(row=1, column=0, padx=5, pady=5)
        self.led_off_btn.grid(row=2, column=0, padx=5, pady=5)
        self.led_status.grid(row=3, column=0, padx=5, pady=5)

    def DisGUIClose(self):
        for widget in self.DisFrame.winfo_children():
            widget.destroy()
        self.DisFrame.destroy()

    def led_handler(self, state, color):
        self.serial.led_state = state

        self.led_status["fg"] = color
        print("LED : ", self.serial.led_state)

    def bar_chart(self):
        # canvas for bar chart
        self.canvas_width = 250
        self.canvas_height = 150
        self.canvas = Canvas(
            self.graph_frame, width=self.canvas_width, height=self.canvas_height
        )
        self.canvas.grid(row=1, column=0, padx=10, pady=5)
        #

        # bar chart
        sensor_data = [self.data.temp, self.data.humi, self.data.co2, self.data.ill]
        color = ["red", "orange", "green", "blue"]
        x0 = 50
        x1 = 80
        y0 = 150
        self.bars = []

        for i in range(len(sensor_data)):

            if i == 2:
                y1 = y0 - (sensor_data[i] * y0 / 500)
            else:
                y1 = y0 - (sensor_data[i] * y0 / 100)  # y1 = bar height

            bar = self.canvas.create_rectangle(
                x0, y0, x1, y1, fill=color[i], outline=""
            )
            self.bars.append(bar)
            self.canvas.create_text((x0 + x1) / 2, y1 - 10, text=str(sensor_data[i]))
            x0 += 40
            x1 += 40


if __name__ == "__main__":
    RootGUI()
    ComGui()
