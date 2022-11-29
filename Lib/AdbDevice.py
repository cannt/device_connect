class AdbDevice(object):
    def __init__(self, device, serial, os, ip, state):
        self.device = device
        self.serial = serial
        self.os = os
        self.ip = ip
        self.state = state

    def __str__(self):
        return
