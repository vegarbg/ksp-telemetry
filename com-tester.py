#!/usr/bin/env python
# -*- coding: utf-8 -*-

from COMPort import COMPort
from COMPortSelectForm import COMPortSelectForm
import wx

if __name__ == "__main__":
    app = wx.App(False)
    result = COMPort()
    frame = COMPortSelectForm(result)
    frame.Show()
    app.MainLoop()
    if result:
        print result.name
    else:
        print "Failure!"
