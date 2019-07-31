from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtCore import * #QSize
from PyQt5.QtWidgets import * #QApplication, QWidget, QPushButton, QMessageBox, QSlider
from PyQt5.QtGui import * #QImage, QPalette, QBrush
from phue import Bridge
import sys, time, datetime, requests
from weather import Weather

b = Bridge("192.168.50.175")
b.connect()

allLights = b.get_light_objects('name')


kitchenLights = [   allLights['K1'],
                    allLights['K2'],
                    allLights['K3'],
                    allLights['K4'] ]

livingRoomLights = [ allLights['Lamp'] ]

w = Weather()

class MainView(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainView, self).__init__()
        self.statusBar().setSizeGripEnabled(False)
        self.setFixedSize(self.sizeHint())
        bgImg = QImage("./img/bg.png")
        sImage = bgImg.scaled(QSize(800,480))
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))                     
        self.setPalette(palette)
        
        self.shortcut = QShortcut(QKeySequence("Ctrl+Q"), self)
        self.shortcut.activated.connect(self.close)
        
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.screenSaver())
        
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
        
        self.timer.start(300000)
        
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
        self.timer.stop()
        self.dialog = ScreenSaver(self)
        self.dialog.show()
        self.close()
        
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
        
        self.clockTimer = QTimer()
        self.clockTimer.timeout.connect(self.updateDateTime)
        self.clockTimer.start(60000)
        
        self.weatherTimer = QTimer()
        self.weatherTimer.timeout.connect(self.updateWeather)
        self.weatherTimer.start(600000)
        
        self.lblCurrentTemp = self.findChild(QtWidgets.QLabel, 'lblCurrentTemp')
        self.lblWeatherIcon = self.findChild(QtWidgets.QLabel, 'lblweatherIcon')
        
        self.lblDate = self.findChild(QtWidgets.QLabel, 'lblDate')
        self.lblDate.setText(datetime.datetime.now().strftime("%b %d %Y"))
        
        self.lblClock = self.findChild(QtWidgets.QLabel, 'lblClock')
        self.lblClock.setText(datetime.datetime.now().strftime("%-I:%M"))
        
        self.lblDayFcst1 = self.findChild(QtWidgets.QLabel, 'lblDayFcst1')
        self.lblDayFcst2 = self.findChild(QtWidgets.QLabel, 'lblDayFcst2')
        self.lblDayFcst3 = self.findChild(QtWidgets.QLabel, 'lblDayFcst3')
        
        self.lblDayFcstTemp1 = self.findChild(QtWidgets.QLabel, 'lblDayFcstTemp1')
        self.lblDayFcstTemp2 = self.findChild(QtWidgets.QLabel, 'lblDayFcstTemp2')
        self.lblDayFcstTemp3 = self.findChild(QtWidgets.QLabel, 'lblDayFcstTemp3')
        
        self.lblDayFcstTime1 = self.findChild(QtWidgets.QLabel, 'lblDayFcstTime1')
        self.lblDayFcstTime2 = self.findChild(QtWidgets.QLabel, 'lblDayFcstTime2')
        self.lblDayFcstTime3 = self.findChild(QtWidgets.QLabel, 'lblDayFcstTime3')
        
        self.lblWkFcst1 = self.findChild(QtWidgets.QLabel, 'lblWkFcst1')
        self.lblWkFcst2 = self.findChild(QtWidgets.QLabel, 'lblWkFcst2')
        self.lblWkFcst3 = self.findChild(QtWidgets.QLabel, 'lblWkFcst3')
        self.lblWkFcst4 = self.findChild(QtWidgets.QLabel, 'lblWkFcst4')
        self.lblWkFcst5 = self.findChild(QtWidgets.QLabel, 'lblWkFcst5')
        
        self.lblWkFcstDay1 = self.findChild(QtWidgets.QLabel, 'lblWkFcstDay1')
        self.lblWkFcstDay2 = self.findChild(QtWidgets.QLabel, 'lblWkFcstDay2')
        self.lblWkFcstDay3 = self.findChild(QtWidgets.QLabel, 'lblWkFcstDay3')
        self.lblWkFcstDay4 = self.findChild(QtWidgets.QLabel, 'lblWkFcstDay4')
        self.lblWkFcstDay5 = self.findChild(QtWidgets.QLabel, 'lblWkFcstDay5')
        
        self.lblWkFcstTemp1 = self.findChild(QtWidgets.QLabel, 'lblWkFcstTemp1')
        self.lblWkFcstTemp2 = self.findChild(QtWidgets.QLabel, 'lblWkFcstTemp2')
        self.lblWkFcstTemp3 = self.findChild(QtWidgets.QLabel, 'lblWkFcstTemp3')
        self.lblWkFcstTemp4 = self.findChild(QtWidgets.QLabel, 'lblWkFcstTemp4')
        self.lblWkFcstTemp5 = self.findChild(QtWidgets.QLabel, 'lblWkFcstTemp5')
        
        self.wkForecastIcons = [self.lblWkFcst1, self.lblWkFcst2, self.lblWkFcst3, self.lblWkFcst4, self.lblWkFcst5]
        self.wkForecastDays = [self.lblWkFcstDay1, self.lblWkFcstDay2, self.lblWkFcstDay3, self.lblWkFcstDay4, self.lblWkFcstDay5]
        self.wkForecastTemps = [self.lblWkFcstTemp1, self.lblWkFcstTemp2, self.lblWkFcstTemp3, self.lblWkFcstTemp4, self.lblWkFcstTemp5]
        self.dayForecastIcons = [self.lblDayFcst1, self.lblDayFcst2, self.lblDayFcst3]
        self.dayForecastTemps = [self.lblDayFcstTemp1, self.lblDayFcstTemp2, self.lblDayFcstTemp3]
        self.dayForecastTimes = [self.lblDayFcstTime1, self.lblDayFcstTime2, self.lblDayFcstTime3]
        
        self.btnReturn = self.findChild(QtWidgets.QPushButton, 'btnReturnToMain')
        self.btnReturn.clicked.connect(self.returnToMain)
        
        self.updateWeather()
        self.updateDateTime()
        
    def returnToMain(self):
        self.dialog = MainView()
        self.dialog.show()
        self.close()
        
    def updateDateTime(self):
        self.lblClock.setText(datetime.datetime.now().strftime("%-I:%M"))
        self.lblDate.setText(datetime.datetime.now().strftime("%b %d %Y"))
        
    def updateWeather(self):
        current_weather = w.getCurrentWeather()
        week_forecast = w.getWeekForecast()
        current_forecast = w.getDayForecast()
        
        for i in range(0, len(week_forecast)):
            temp_icon = QtGui.QImage()
            temp_icon.loadFromData(w.getIconImage(week_forecast[i]["weather"][0]["icon"]))
            self.wkForecastIcons[i].setPixmap(QtGui.QPixmap(temp_icon))
            self.wkForecastDays[i].setText(time.strftime("%a", time.gmtime(week_forecast[i]["dt"])))
            self.wkForecastTemps[i].setText(str(int(week_forecast[i]["main"]["temp"])) + u'\N{DEGREE SIGN}')
            
        for i in range(0,3):
            temp_icon = QtGui.QImage()
            temp_icon.loadFromData(w.getIconImage(current_forecast[i]["weather"][0]["icon"]))
            self.dayForecastIcons[i].setPixmap(QtGui.QPixmap(temp_icon))
            self.dayForecastTemps[i].setText(str(int(current_forecast[i]["main"]["temp"])) + u'\N{DEGREE SIGN}')
            self.dayForecastTimes[i].setText(time.strftime("%-I %p", time.gmtime(current_forecast[i]["dt"])))
            
        current_weather_icon = QtGui.QImage()
        current_weather_icon.loadFromData(current_weather[2])
        
        self.lblCurrentTemp.setText(current_weather[0])
        self.lblWeatherIcon.setPixmap(QtGui.QPixmap(current_weather_icon))


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
