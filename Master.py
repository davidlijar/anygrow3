from Gui_Master import RootGUI, ComGui
from Serial_Socket_Com_ctrl import SerialCtrl
from Data_Com_ctrl import DataMaster
from Gui_Master import DisGUI


MySerial = SerialCtrl()


MyData = DataMaster()
RootMaster = RootGUI(MySerial, MyData)

ComMaster = ComGui(RootMaster.root, MySerial, MyData)

RootMaster.root.mainloop()
