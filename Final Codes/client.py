import sys

from PyQt4.QtGui import QWidget, QImage, QApplication, QPainter
from PyQt4 import QtCore
from naoqi import ALProxy

import vision_definitions
import socket
import struct

import os
import glob

HOST = '172.16.21.209'    # The remote host
PORT = 50009              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

i = 0
flag = 0

def bytes_to_int(bytes):
    result = 0
    for b in bytes:
        result = result * 256 + int(b)
    return result

class ImageWidget(QWidget):

    def __init__(self, IP, PORT, CameraID, parent=None):
        """
        Initialization.
        """
        QWidget.__init__(self, parent)
        self.initUI()
        self._image = QImage()
        self.setWindowTitle('Nao')

        self._imgWidth =100
        self._imgHeight =100
        self._cameraID = CameraID
        self.resize(self._imgWidth, self._imgHeight)

        # Proxy to ALVideoDevice.
        self._videoProxy = None

        # Our video module name.
        self._imgClient = ""

        # This will contain this alImage we get from Nao.
        self._alImage = None
        self.nao_ip = IP
        self.nao_port = PORT

        self._registerImageClient(IP, PORT)

        # Trigget 'timerEvent' every 100 ms.
        self.startTimer(100)


    def _registerImageClient(self, IP, PORT):
        """
        Register our video module to the robot.
        """
        self._videoProxy = ALProxy("ALVideoDevice", IP, PORT)
        resolution = vision_definitions.kQQVGA
        colorSpace = vision_definitions.kRGBColorSpace
        self._imgClient = self._videoProxy.subscribe("_client", resolution, colorSpace, 5)

        # Select camera.
        self._videoProxy.setParam(vision_definitions.kCameraSelectID,
                                  self._cameraID)

    def _unregisterImageClient(self):
        """
        Unregister our naoqi video module.
        """
        if self._imgClient != "":
            self._videoProxy.unsubscribe(self._imgClient)


    def paintEvent(self, event):
        """
        Draw the QImage on screen.
        """
        # painter = QPainter(self)
        # painter.drawImage(painter.viewport(), self._image)


    def _updateImage(self):
        """
        Retrieve a new image from Nao.
        """

        global i
        global flag
        
        self._alImage = self._videoProxy.getImageRemote(self._imgClient)
        self._image = QImage(self._alImage[6],           # Pixel array.
                             self._alImage[0],           # Width.
                             self._alImage[1],           # Height.
                             QImage.Format_RGB888)

        # print (flag)

        if flag == 1:
            if i < 10:
                filename = './temp/test_img/0' + str(i) + '.png'
            else:
                filename = './temp/test_img/' + str(i) + '.png'
            self._image.save(filename)
            i +=1

    def timerEvent(self, event):
        """
        Called periodically. Retrieve a nao image, and update the widget.
        """
        self._updateImage()
        # print('aaa')
        self.update()


    def __del__(self):
        """
        When the widget is deleted, we unregister our naoqi video module.
        """
        self._unregisterImageClient()

    def initUI(self):      
        
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Event handler')
        self.show()
        
    def keyPressEvent(self, e):
        global flag
        global i

        if e.key() == QtCore.Qt.Key_S:
            # files = glob.glob('./temp/test_img/*')
            # for f in files:
            #     os.remove(f)

            flag = 1
            i = 0
            print ("Start Capture")
        elif e.key() == QtCore.Qt.Key_Q: 
            flag = 0 
            print ("End Capture")

            s.sendall('Event')
            data = s.recv(1024)
            # s.close()
            # print 'Received', repr(data)
            ans = int(data.encode('hex'), 16)
            print(ans)

            tts = ALProxy("ALTextToSpeech", self.nao_ip, self.nao_port)
            
            if ans == 0:
                # no gesture
                tts.say("No Gesture Detected")
            elif ans == 1:
                # left
                pi_2 = -3.1415/2

                postureProxy = ALProxy("ALRobotPosture", self.nao_ip, self.nao_port)
                posture = postureProxy.getPosture()
                
                if(posture == 'Sit'):
                    tts.say("I need to stand first")
                    postureProxy.goToPosture("Stand", 1.0)

                tts.say("Moving to your Left")

                motion = ALProxy("ALMotion", self.nao_ip, self.nao_port)
                motion.moveInit()
                motion.moveTo(0, 0, pi_2)
                motion.moveTo(0.2, 0, 0)
            elif ans == 2:
                # right
                pi_2 = 3.1415/2
                postureProxy = ALProxy("ALRobotPosture", self.nao_ip, self.nao_port)
                posture = postureProxy.getPosture()
                
                if(posture == 'Sit'):
                    tts.say("I need to stand first")
                    postureProxy.goToPosture("Stand", 1.0)

                tts.say("Moving to your Right")

                motion = ALProxy("ALMotion", self.nao_ip, self.nao_port)
                motion.moveInit()
                motion.moveTo(0, 0, pi_2)
                motion.moveTo(0.2, 0, 0)
            elif ans == 3:
                # down
                tts.say("Sit Down")

                postureProxy = ALProxy("ALRobotPosture", self.nao_ip, self.nao_port)
                postureProxy.goToPosture("Sit", 1.0)

            elif ans == 4:
                # up
                tts.say("Stand Up")

                postureProxy = ALProxy("ALRobotPosture", self.nao_ip, self.nao_port)
                postureProxy.goToPosture("Stand", 1.0)
            elif ans == 5:
                # shaking hand
                tts.say("Hi")
            elif ans == 6:
                # stop
                postureProxy = ALProxy("ALRobotPosture", self.nao_ip, self.nao_port)
                posture = postureProxy.getPosture()
                
                if(posture == 'Sit'):
                    tts.say("I need to stand first")
                    postureProxy.goToPosture("Stand", 1.0)

                tts.say("Moving Back")

                motion = ALProxy("ALMotion", self.nao_ip, self.nao_port)
                motion.moveInit()
                motion.moveTo(-0.2, 0, 0)
            elif ans == 7:
                # forward
                postureProxy = ALProxy("ALRobotPosture", self.nao_ip, self.nao_port)
                posture = postureProxy.getPosture()
                
                if(posture == 'Sit'):
                    tts.say("I need to stand first")
                    postureProxy.goToPosture("Stand", 1.0)

                tts.say("Moving Forward")
                
                motion = ALProxy("ALMotion", self.nao_ip, self.nao_port)
                motion.moveInit()
                motion.moveTo(0.2, 0, 0)

            files = glob.glob('./temp/test_img/*')
            for f in files:
                os.remove(f)
        
            self.close()
            s.close()

        # elif e.key() == QtCore.Qt.Key_X:
        #     self.close()
        #     s.close()

if __name__ == '__main__':
    IP = "172.16.21.202"  # Replace here with your NaoQi's IP address.
    PORT = 9559
    CameraID = 0

    # Read IP address from first argument if any.
    if len(sys.argv) > 1:
        IP = sys.argv[1]

    # Read CameraID from second argument if any.
    if len(sys.argv) > 2:
        CameraID = int(sys.argv[2])

    aware = ALProxy("ALBasicAwareness",IP,PORT)
    aware.setEngagementMode("FullyEngaged")
    aware.setStimulusDetectionEnabled("Sound",False)
    aware.startAwareness()

    app = QApplication(sys.argv)
    myWidget = ImageWidget(IP, PORT, CameraID)
    myWidget.show()
    sys.exit(app.exec_())
