from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtCore import * #QSize
from PyQt5.QtWidgets import * #QApplication, QWidget, QPushButton, QMessageBox, QSlider
from PyQt5.QtGui import * #QImage, QPalette, QBrush
from phue import Bridge
import sys, time, datetime

b = Bridge("192.168.50.175")
b.connect()

allLights = b.get_light_objects('name')


kitchenLights = [	allLights['K1'],
					allLights['K2'],
					allLights['K3'],
					allLights['K4'] ]

livingRoomLights = [ allLights['Lamp'] ]

class MainView(QtWidgets.QMainWindow):
	def __init__(self):
		super(MainView, self).__init__()
		
		bgImg = QImage("./img/bg.png")
		sImage = bgImg.scaled(QSize(800,480))
		palette = QPalette()
		palette.setBrush(10, QBrush(sImage))                     
		self.setPalette(palette)
		
		self.timer = QTimer()
		#self.timer.timeout.connect(lambda: self.screenSaver())
		
		uic.loadUi("pyHue.ui", self)
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		
		#Button Connections
		self.btnLivingRoom = self.findChild(QtWidgets.QPushButton, 'btnLivingRoom')
		self.btnLivingRoom.setIcon(QtGui.QIcon('./icons/livingroom.png'))
		self.btnLivingRoom.clicked.connect(lambda: self.roomSettings(livingRoomLights))
		
		self.btnKitchen = self.findChild(QtWidgets.QPushButton, 'btnKitchen')
		self.btnKitchen.setIcon(QtGui.QIcon('./icons/kitchen.png'))
		self.btnKitchen.clicked.connect(lambda: self.roomSettings(kitchenLights))
		
		self.btnAllOn = self.findChild(QtWidgets.QPushButton, 'btnAllOn')
		self.btnAllOn.setIcon(QtGui.QIcon('./icons/lightOn.png'))
		self.btnAllOn.clicked.connect(self.allLightsOn)
		
		self.btnAllOff = self.findChild(QtWidgets.QPushButton, 'btnAllOff')
		self.btnAllOff.setIcon(QtGui.QIcon('./icons/lightOff.png'))
		self.btnAllOff.clicked.connect(self.allLightsOff)
		
		self.btnAway = self.findChild(QtWidgets.QPushButton, 'btnAway')
		self.btnAway.setIcon(QtGui.QIcon('./icons/away.png'))
		
		self.btnBedroom = self.findChild(QtWidgets.QPushButton, 'btnBedroom')
		self.btnBedroom.setIcon(QtGui.QIcon('./icons/bed.png'))
		
		self.btnStudio = self.findChild(QtWidgets.QPushButton, 'btnStudio')
		self.btnStudio.setIcon(QtGui.QIcon('./icons/studio.png'))
		self.btnStudio.clicked.connect(self.screenSaver)
		
		self.btnDanaOffice = self.findChild(QtWidgets.QPushButton, 'btnDanaOffice')
		self.btnDanaOffice.setIcon(QtGui.QIcon('./icons/danaOffice.png'))
		#self.btnDanaOffice.clicked.connect(lambda: self.roomSettings(danaOfficeLights))
		
		self.btnDanielOffice = self.findChild(QtWidgets.QPushButton, 'btnDanielOffice')
		self.btnDanielOffice.setIcon(QtGui.QIcon('./icons/danielOffice.png'))
		#self.btnDanielOffice.clicked.connect(lambda: self.roomSettings(danielOfficeLights))
		
		self.timer.start(5000)
		
		self.show()
		
		
		
	def roomSettings(self, currentLights):
		
		self.dialog = RoomParams(self, currentLights)
		self.dialog.show()
	
	def allLightsOn(self):
		for l in b.lights:
			if not l.on:
				l.on = True
				
	def allLightsOff(self):
		for l in b.lights:
			if l.on:
				l.on = False
	
	def screenSaver(self):
		self.dialog = ScreenSaver(self)
		self.dialog.show()
		
class ScreenSaver(QtWidgets.QMainWindow):
	def __init__(self, parent=None):
		super(ScreenSaver, self).__init__()

		bgImg = QImage("./img/bg.png")
		
		sImage = bgImg.scaled(QSize(800,480))
		palette = QPalette()
		palette.setBrush(10, QBrush(sImage))                     
		self.setPalette(palette)
		
		uic.loadUi("screenSaver.ui", self)
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		
		self.timer = QTimer()
		self.timer.timeout.connect(self.updateDateTime)
		self.timer.start(60000)
		
		self.lblDate = self.findChild(QtWidgets.QLabel, 'lblDate')
		self.lblClock = self.findChild(QtWidgets.QLabel, 'lblClock')
		self.lblClock.setText(datetime.datetime.now().strftime("%H:%M"))
		self.lblDate.setText(datetime.datetime.now().strftime("%b %d %Y"))
		
	def updateDateTime(self):
		self.lblClock.setText(datetime.datetime.now().strftime("%H:%M"))
		self.lblDate.setText(blur(self, datetime.datetime.now().strftime("%b %d %Y")))
		
	def blur(self, pixmap):
		effect = QtWidgets.QGraphicsBlurEffect()
		scene = QtWidgets.QGraphicsScene()
		item = QtWidgets.QGraphicsPixmapItem(pixmap)
		scene.addItem(item)
		item.setGraphicsEffect(effect)
		image = pixmap.toImage()
		image.fill(QtCore.Qt.transparent)
		painter = QtGui.QPainter(image)
		scene.render(painter)
		painter.end()
		return QtGui.QPixmap(image)

class RoomParams(QtWidgets.QMainWindow):
	def __init__(self, parent=None, currentLights=None):
		super(RoomParams, self).__init__()
		
		bgImg = QImage("./img/bg.png")
		
		sImage = bgImg.scaled(QSize(800,480))
		palette = QPalette()
		palette.setBrush(10, QBrush(sImage))                     
		self.setPalette(palette)
		
		uic.loadUi("roomParams.ui", self)
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		
		self.currentLights = currentLights
		
		self.btnReturn = self.findChild(QtWidgets.QPushButton, 'btnReturn')
		self.btnReturn.setIcon(QtGui.QIcon('./icons/back2.png'))
		self.btnReturn.clicked.connect(self.returnToMain)
		
		self.brightnessSlider = self.findChild(QtWidgets.QSlider, 'brightnessSlider')
		self.brightnessSlider.valueChanged.connect(self.changeBrightness)
		
		self.btnOn = self.findChild(QtWidgets.QPushButton, 'btnOn')
		self.btnOn.setIcon(QtGui.QIcon('./icons/lightOn.png'))
		
		self.btnOff = self.findChild(QtWidgets.QPushButton, 'btnOff')
		self.btnOff.setIcon(QtGui.QIcon('./icons/lightOff.png'))
		
	def changeBrightness(self):
		for l in self.currentLights:
			l.brightness = int(self.brightnessSlider.value())
		
	def returnToMain(self):
		self.close()
		


app = QtWidgets.QApplication(sys.argv)
window = MainView()
app.exec_()
