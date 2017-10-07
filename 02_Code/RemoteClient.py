# DataClient1.py
import pygame
from threading import Thread
import socket, time, sys, os

VERBOSE = False
IP_ADDRESS = "192.168.0.31"
IP_PORT = 22000

# TODO: Replace this with logging.debug. Easiest is like this:
# >>> from logging import debug
# Then you don't have to modify the code which calls this.
def debug(text):
    if VERBOSE:
        print "Debug:---", text


class Receiver(Thread):
    def run(self):
        debug("Receiver thread started")
        while True:
            try:
                rxData = self.readServerData()
            except:
                debug("Exception in Receiver.run()")
                isReceiverRunning = False
                closeConnection()
                break

        debug("Receiver thread terminated")


    def readServerData(self):
        debug("Calling readResponse")
        bufSize = 4096
        data = ""
        while data[-1:] != "\0": # reply with end-of-message indicator
            try:
                blk = sock.recv(bufSize)
                if blk != None:
                    debug("Received data block from server, len: " + \
                        str(len(blk)))
                else:
                    debug("sock.recv() returned with None")
            except:
                raise Exception("Exception from blocking sock.recv()")
            data += blk
        print "Data received:", data


def startReceiver():
    debug("Starting Receiver thread")
    receiver = Receiver()
    receiver.start()

# TODO: Escape need for global by passing in connection to send command to
def sendCommand(cmd):
    debug("sendCommand() with cmd = " + cmd)
    try:
        # append \0 as end-of-message indicator
        sock.sendall(cmd + "\0")
    except:
        debug("Exception in sendCommand()")
        closeConnection()

# TODO: PEP8
def closeConnection():
    # TODO: No globals.
    global isConnected
    debug("Closing socket")
    sock.close()
    # TODO: Don't set this here. Don't use globals. Set after closing socket
    # in main.
    isConnected = False

# TODO: Replace return False with exception
def connect():
    # TODO: No globals. Eliminate the need by returning it.
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    debug("Connecting...")
    try:
        sock.connect((IP_ADDRESS, IP_PORT))
    except:
        debug("Connection failed.")
        return False
    startReceiver()
    return True


if __name__ == "__main__":
    try:

        sock = None
        isConnected = False

        pygame.init()
        pygame.display.set_mode((1,1))
        pygame.key.set_repeat(100, 100)



        if connect():
            # TODO: PEP8
            isConnected = True
            print "Connection established"
            time.sleep(1)
            while isConnected:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            sendCommand("forward")
                        elif event.key == pygame.K_DOWN:
                            sendCommand("reverse")
                        elif event.key == pygame.K_LEFT:
                            sendCommand("left")
                        elif event.key == pygame.K_RIGHT:
                            sendCommand("right")
                    if event.type == pygame.KEYUP:
                        sendCommand("stop")
        else:
            print "Connection to %s:%d failed" % (IP_ADDRESS, IP_PORT)
        print "done"
    except (KeyboardInterrupt, SystemExit):
        closeConnection()
        sys.exit(0)

