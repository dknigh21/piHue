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

lightDict = {
    "btnKitchen" : [allLights['K1'], allLights['K2'], allLights['K3'], allLights['K4']],
    "btnLivingRoom" : [ allLights['Lamp'] ]
    }

activeLights = []

w = Weather()

class MainView(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainView, self).__init__()
        self.statusBar().setSizeGripEnabled(False)
        self.setFixedSize(self.sizeHint())
        
        self.shortcut = QShortcut(QKeySequence("Ctrl+Q"), self)
        self.shortcut.activated.connect(self.close)
        
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.screenSaver())
        
        uic.loadUi("pyHue.ui", self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
                
            
        #Button Connections
        
        self.btnClose = self.findChild(QtWidgets.QPushButton, 'btnClose')
        self.btnClose.clicked.connect(self.close)
        
        self.btnLivingRoom = self.findChild(QtWidgets.QPushButton, 'btnLivingRoom')
        lrIcon = QIcon()
        lrIcon.addPixmap(QPixmap('./icons/livingroom'), QIcon.Normal, QIcon.On)
        lrIcon.addPixmap(QPixmap('./icons/livingroom_off'), QIcon.Normal, QIcon.Off)
        self.btnLivingRoom.setIcon(lrIcon)
        self.btnLivingRoom.clicked.connect(self.activeRooms)
        
        self.btnKitchen = self.findChild(QtWidgets.QPushButton, 'btnKitchen')
        kitchenIcon = QIcon()
        kitchenIcon.addPixmap(QPixmap('./icons/fridge'), QIcon.Normal, QIcon.On)
        kitchenIcon.addPixmap(QPixmap('./icons/fridge_off'), QIcon.Normal, QIcon.Off)
        self.btnKitchen.setIcon(kitchenIcon)
        self.btnKitchen.clicked.connect(self.activeRooms)
        
        self.btnAllOn = self.findChild(QtWidgets.QPushButton, 'btnAllOn')
        self.btnAllOn.setIcon(QtGui.QIcon('./icons/lightOn.png'))
        self.btnAllOn.clicked.connect(lambda: self.allLightsOn(True))
        
        self.btnAllOff = self.findChild(QtWidgets.QPushButton, 'btnAllOff')
        self.btnAllOff.setIcon(QtGui.QIcon('./icons/lightOff.png'))
        self.btnAllOff.clicked.connect(lambda: self.allLightsOff(True))
        
        self.btnAway = self.findChild(QtWidgets.QPushButton, 'btnAway')
        awayIcon = QIcon()
        awayIcon.addPixmap(QPixmap('./icons/away'), QIcon.Normal, QIcon.On)
        awayIcon.addPixmap(QPixmap('./icons/away_off'), QIcon.Normal, QIcon.Off)
        self.btnAway.setIcon(awayIcon)
        self.btnKitchen.clicked.connect(self.away)
        
        self.btnBedroom = self.findChild(QtWidgets.QPushButton, 'btnBedroom')
        bedroomIcon = QIcon()
        bedroomIcon.addPixmap(QPixmap('./icons/bed'), QIcon.Normal, QIcon.On)
        bedroomIcon.addPixmap(QPixmap('./icons/bed_off'), QIcon.Normal, QIcon.Off)
        self.btnBedroom.setIcon(bedroomIcon)
        
        self.btnStudio = self.findChild(QtWidgets.QPushButton, 'btnStudio')
        studioIcon = QIcon()
        studioIcon.addPixmap(QPixmap('./icons/studio'), QIcon.Normal, QIcon.On)
        studioIcon.addPixmap(QPixmap('./icons/studio_off'), QIcon.Normal, QIcon.Off)
        self.btnStudio.setIcon(studioIcon)
        self.btnStudio.clicked.connect(self.screenSaver)
        
        self.btnDanaOffice = self.findChild(QtWidgets.QPushButton, 'btnDanaOffice')
        danaOfficeIcon = QIcon()
        danaOfficeIcon.addPixmap(QPixmap('./icons/danaOffice'), QIcon.Normal, QIcon.On)
        danaOfficeIcon.addPixmap(QPixmap('./icons/danaOffice_off'), QIcon.Normal, QIcon.Off)
        self.btnDanaOffice.setIcon(danaOfficeIcon)
        #self.btnDanaOffice.clicked.connect(lambda: self.roomSettings(danaOfficeLights))
        
        self.btnDanielOffice = self.findChild(QtWidgets.QPushButton, 'btnDanielOffice')
        danielOfficeIcon = QIcon()
        danielOfficeIcon.addPixmap(QPixmap('./icons/danielOffice'), QIcon.Normal, QIcon.On)
        danielOfficeIcon.addPixmap(QPixmap('./icons/danielOffice_off'), QIcon.Normal, QIcon.Off)
        self.btnDanielOffice.setIcon(danielOfficeIcon)
        #self.btnDanielOffice.clicked.connect(lambda: self.roomSettings(danielOfficeLights))
        
        self.btnParty = self.findChild(QtWidgets.QPushButton, 'btnParty')
        partyIcon = QIcon()
        partyIcon.addPixmap(QPixmap('./icons/partymode'), QIcon.Normal, QIcon.On)
        partyIcon.addPixmap(QPixmap('./icons/partymode_off'), QIcon.Normal, QIcon.Off)
        self.btnParty.setIcon(partyIcon)
        self.btnParty.clicked[bool].connect(self.partyMode)
        
        self.brightnessSlider = self.findChild(QtWidgets.QSlider, 'brightnessSlider')
        self.brightnessSlider.valueChanged.connect(self.changeBrightness)
        
        self.btnSelectedOn = self.findChild(QtWidgets.QPushButton, 'btnSelectedOn')
        selectedOnIcon = QIcon()
        selectedOnIcon.addPixmap(QPixmap('./icons/lightOn'), QIcon.Normal, QIcon.On)
        selectedOnIcon.addPixmap(QPixmap('./icons/lightOn_off'), QIcon.Normal, QIcon.Off)
        self.btnSelectedOn.setIcon(selectedOnIcon)
        
        self.btnSelectedOff = self.findChild(QtWidgets.QPushButton, 'btnSelectedOff')
        selectedOffIcon = QIcon()
        selectedOffIcon.addPixmap(QPixmap('./icons/lightOff'), QIcon.Normal, QIcon.On)
        selectedOffIcon.addPixmap(QPixmap('./icons/lightOff_off'), QIcon.Normal, QIcon.Off)
        self.btnSelectedOff.setIcon(selectedOffIcon)
        
        
        self.timer.start(300000)
        self.show()
        
    def changeBrightness(self):
        for i in activeLights:
            for l in i:
                l.brightness = int(self.brightnessSlider.value())
    
    def away(self):
        pass
    
    def partyMode(self, checked):

        if checked:

            for l in b.lights:
                l.effect = "colorloop"

        if not checked:
            
            for l in b.lights:
                l.effect = "none"

    def activeRooms(self):
        
        activeLights.clear()
        
        for b in self.findChildren(QtWidgets.QPushButton):
            if b.isChecked():
                activeLights.append(lightDict[str(b.objectName())])
                
        if not activeLights:
            self.brightnessSlider.setEnabled(False)
        else:
            self.brightnessSlider.setEnabled(True)
        #self.dialog = RoomParams(self, currentLights)
        #self.dialog.show()
    
    def allLightsOn(self, all):
        if all:
            for l in b.lights:
                if not l.on:
                    l.on = True
        else:
            for l in activeLights:
                if not l.on:
                    l.on = True
                
    def allLightsOff(self, all):
        if all:
            for l in b.lights:
                if l.on:
                    l.on = False
        else:
            for l in activeLights:
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
        self.btnOn.clicked.connect(self.lightsOn)
        
        self.btnOff = self.findChild(QtWidgets.QPushButton, 'btnOff')
        self.btnOff.setIcon(QtGui.QIcon('./icons/lightOff.png'))
        self.btnOff.clicked.connect(self.lightsOff)
        
    def changeBrightness(self):
        for l in self.currentLights:
            l.brightness = int(self.brightnessSlider.value())
        
    def returnToMain(self):
        self.close()

    def lightsOn(self):
        for l in self.currentLights:
            l.on = True

    def lightsOff(self):
        for l in self.currentLights:
            l.on = False
        


app = QtWidgets.QApplication(sys.argv)
window = MainView()
app.exec_()
