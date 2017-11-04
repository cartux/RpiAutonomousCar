#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of FSE 2017.
#
# FSE 2017 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# FSE 2017 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with FSE 2017.  If not, see <http://www.gnu.org/licenses/>.

import socket
import time
from threading import Thread

from ..drivers.led import LED
from ..drivers.motor_driver import MotorDriver
from ..drivers.ultrasonic_ranger import UltrasonicRanger

VERBOSE = False
IP_PORT = 22000


# TODO: These are not constants, they're used in the script, so move it down
# to the main.
# TODO: These looks like classes. PEP8.
UltrasonicObj = UltrasonicRanger()
LedObj = LED()
RobotDriveObj = MotorDriver()

# TODO: Docstrings!
class SocketHandler(Thread):
    def __init__(self, conn):
        Thread.__init__(self)
        self.conn = conn

    def run(self):
        # TODO: No globals.
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
        # TODO: No globals!
        global RobotDrive

        #debug("Calling executeCommand() with  cmd: " + cmd)
        state = cmd[:-1]# remove trailing "\0"
        print "Reporting current state:", state
        self.conn.sendall(state + "\0")
        self.conn.sendall(state + "\0")

        # TODO: This is modified later to use new API
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

# TODO: What's the point?
def setup():
    pass

# TODO: Replace with debug from logging, also mentioned elsewhere
def debug(text):
    if VERBOSE:
        print "Debug:---", text

def loop():
    # TODO: PEP8
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # close port when process exits:
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    debug("Socket created")
    HOSTNAME = "" # Symbolic name meaning all available interfaces

    try:
        serverSocket.bind((HOSTNAME, IP_PORT))
    except socket.error as msg:
        # TODO: Raise an exception, don't sys.exit(). You never know who'll
        # import this code and sys.exit kills the whole process.
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
        # TODO: This never terminates. What's the point of isConnected?
        while isConnected:
            print "Server connected at", t, "s"
            time.sleep(10)
            t += 10



if __name__ == "__main__":

    try:
        setup()
        loop()
    except KeyboardInterrupt:
        UltrasonicObj.__exit__()
        LedObj.__exit__()
        RobotDriveObj.__exit__()
