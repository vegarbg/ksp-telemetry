from COMPortSelectForm import COMPortSelectForm
import wx

if __name__ == "__main__":
    app = wx.App(False)
    frame = COMPortSelectForm()
    frame.Show()
    app.MainLoop()
