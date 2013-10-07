import os, serial, wx
from serial.tools import list_ports

from COMPort import COMPort

class COMPortSelectForm(wx.Frame):
    def __init__(self):
        # Create non-resizable frame
        wx.Frame.__init__(self, None, title="Select Arduino COM port", style=wx.DEFAULT_FRAME_STYLE^wx.RESIZE_BORDER, size=(200, 135))
        self.Centre()
        panel = wx.Panel(self, wx.ID_ANY)

        # Create a drop down menu with all available COM ports
        comPortChoices = []
        combobox = wx.ComboBox(panel, size=wx.DefaultSize, choices=comPortChoices, style=wx.CB_READONLY)
        self.combobox = combobox
        for comport in COMPortSelectForm.list_serial_ports():
            combobox.Append(comport.name, comport)
        combobox.SetSelection(0)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(panel, label="Select Arduino COM port"), flag=wx.LEFT|wx.RIGHT|wx.TOP|wx.ALIGN_CENTER_HORIZONTAL, border=10)
        sizer.Add(combobox, 0, flag=wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND, border=10)
        selectButton = wx.Button(panel, label="Select", size=(-1, 30))
        sizer.Add(selectButton, 0, flag=wx.ALL|wx.EXPAND, border=10)
        selectButton.Bind(wx.EVT_BUTTON, self.onClick)
        panel.SetSizer(sizer)

    def onClick(self, event):
        print "You selected: " + self.combobox.GetStringSelection()

    # Source: http://stackoverflow.com/a/14224477
    @staticmethod
    def list_serial_ports():
        # Windows
        if os.name == "nt":
            # Scan for available ports
            available = []
            for i in range(256):
                try:
                    s = serial.Serial(i)
                    available.append(COMPort(i, "COM"+str(i + 1)))
                    s.close()
                except serial.SerialException:
                    pass
            return available
        else:
            # Mac / Linux
            return [COMPort(port[0], port[0]) for port in list_ports.comports()]
