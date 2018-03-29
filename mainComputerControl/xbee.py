import serial
import time

class XBee(object):

    def __init__(self, serial_port="COM9"):

        self.xbee_port = None

        while True:
            try:
                self.xbee_port = serial.Serial(serial_port, 57600, timeout=5)
                print "XBee connection successful!"
                break
            except serial.SerialException:
                print "Failed to connect to XBee, retrying..."
                time.sleep(3)


    def send_command(self, strOut):
        # Send the data

        if (strOut in range(256)):
            self.xbee_port.write(chr(int(strOut)))
        else:
            self.xbee_port.write(chr(int(strOut)))
            print "Trying to write the impossible!: ", strOut
