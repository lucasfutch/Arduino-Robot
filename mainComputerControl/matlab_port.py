import socket

class MatlabPort(object):
    def __init__(self):
        self.host = ''
        self.port = 5560
        self.s = None
        self.conn = None

        self.setupServer()
        self.setupConnection()

    def close(self):
            self.s.close()

    def setupServer(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print "Socet created."
        try:
            self.s.bind((self.host, self.port))
        except socket.error as msg:
            print msg
        print "Socket bind complete."

    def setupConnection(self):
        self.s.listen(1) # allows one connection at a time
        self.conn, address = self.s.accept()
        print "Connected to " + address[0] + ":" + str(address[1])

    def send_byte(self, byte):
        self.conn.sendall(chr(byte))
