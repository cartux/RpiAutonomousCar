#!/usr/bin/env python()
import socket
import time
from threading import Thread

from LED import LED
from MotorDriver import MotorDriver
from UltrasonicRanger import UltrasonicRanger

VERBOSE = False
IP_PORT = 22000


UltrasonicObj = UltrasonicRanger()
LedObj = LED()
RobotDriveObj = MotorDriver()

class SocketHandler(Thread):
    def __init__(self, conn):
        Thread.__init__(self)
        self.conn = conn

    def run(self):
        global isConnected
        debug("SocketHandler started")
        while True:
            cmd = ""
            try:
                debug("Calling blocking conn.recv()")
                cmd = self.conn.recv(1024)
            except:
                debug("exception in conn.recv()") 
                # happens when connection is reset from the peer
                break
            debug("Received cmd: " + cmd + " len: " + str(len(cmd)))
            if len(cmd) == 0:
                break
            self.executeCommand(cmd)
        conn.close()
        print "Client disconnected. Waiting for next client..."
        isConnected = False
        debug("SocketHandler terminated")

    def executeCommand(self, cmd):
        global RobotDrive

        #debug("Calling executeCommand() with  cmd: " + cmd)
        state = cmd[:-1]# remove trailing "\0"
        print "Reporting current state:", state
        self.conn.sendall(state + "\0")
        self.conn.sendall(state + "\0")

        if state == "forward":
            RobotDriveObj.forward()
        elif state == "reverse":
            RobotDriveObj.reverse()
        elif state == "left":
            RobotDriveObj.left()
        elif state == "right":
            RobotDriveObj.right()
        elif state == "stop":
            RobotDriveObj.stop()
        else:
            RobotDriveObj.stop()

def setup():
    pass

def debug(text):
    if VERBOSE:
        print "Debug:---", text

def loop():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # close port when process exits:
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    debug("Socket created")
    HOSTNAME = "" # Symbolic name meaning all available interfaces

    try:
        serverSocket.bind((HOSTNAME, IP_PORT))
    except socket.error as msg:
        print "Bind failed", msg[0], msg[1]
        sys.exit()
    serverSocket.listen(10)

    print "Waiting for a connecting client..."
    isConnected = False

    while True:
        debug("Calling blocking accept()...")
        conn, addr = serverSocket.accept()
        print "Connected with client at " + addr[0]
        isConnected = True
        socketHandler = SocketHandler(conn)
        # necessary to terminate it at program termination:
        socketHandler.setDaemon(True)
        socketHandler.start()
        t = 0
        while isConnected:
            print "Server connected at", t, "s"
            time.sleep(10)
            t += 10



if __name__ == "__main__":

    try:
        setup()
        loop()
    except KeyboardInterrupt:
        UltrasonicObj.destroy()
        LedObj.destroy()
        RobotDriveObj().destroy()

