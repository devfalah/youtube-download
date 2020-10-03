from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import os
from os import path
import os.path
from PyQt5.uic import loadUiType
import  urllib.request
import pafy
import humanize

ui,_ = loadUiType('main.ui')

class MainApp(QMainWindow , ui):
    def __init__(self , parent=None):
        super(MainApp , self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.InitUi()
        self.Handel_Buttons()






    def InitUi(self):
        #contain all ui changes in loading
        self.tabWidget.tabBar().setVisible(False)
        self.Move_Box_1()
        self.Move_Box_2()
        self.Move_Box_3()
        self.Move_Box_4()

    def Handel_Buttons(self):
        #Handel all button in the app
        self.pushButton.clicked.connect(self.Downloade)
        self.pushButton_2.clicked.connect(self.Handel_Brwose)
        self.pushButton_4.clicked.connect(self.Get_Video_Data)
        self.pushButton_3.clicked.connect(self.Download_Video)
        self.pushButton_5.clicked.connect(self.Save_Brwose)
        self.pushButton_7.clicked.connect(self.Playlist_Download)
        self.pushButton_6.clicked.connect(self.Playlist_Save_Browse)
        self.pushButton_8.clicked.connect(self.Open_Home)
        self.pushButton_9.clicked.connect(self.Open_Download)
        self.pushButton_10.clicked.connect(self.Open_Youtube)
        self.pushButton_11.clicked.connect(self.Open_Settings)
        self.pushButton_12.clicked.connect(self.Apply_DarkOrange_style)
        self.pushButton_13.clicked.connect(self.Apply_DarkGray_style)
        self.pushButton_14.clicked.connect(self.Apply_QDark_Style)
        self.pushButton_25.clicked.connect(self.Apply_QDarkblue_Style)








    def Handel_Progress(self,blockNum,blockSize,totalSize):
        #calculate the progress
        readedData=blockNum*blockSize
        if totalSize > 0:
            downloadPercentage=readedData*100/totalSize
            self.progressBar.setValue(downloadPercentage)
            QApplication.processEvents()

    def Handel_Brwose(self):
        #enable brwosing to our os , pick stove location
        savelocation = QFileDialog.getSaveFileName(self, caption="Save as", directory=".", filter="All Files(*.*)")
        print(savelocation)
        self.lineEdit_2.setText(str(savelocation[0]))

    def Downloade(self):
        #downloading any file
        print("Starting Download")
        downloadUrl=self.lineEdit.text()
        saveLocation=self.lineEdit_2.text()
        if downloadUrl=="" or saveLocation=="":
            QMessageBox.warning(self, "Data Error","Provide a valid URL or save location")
        else:
            try:
                urllib.request.urlretrieve(downloadUrl,saveLocation,self.Handel_Progress)
            except Exception:
                QMessageBox.warning(self,"Download Error","Provide a valid URL or save location")
                return
        QMessageBox.information(self, "Download Completed","The Download Completed Successfully")
        self.lineEdit.setText("")
        self.lineEdit_2.setText("")
        self.progressBar.setValue(0)

    def Save_Brwose(self):
        #save location in the line edit
        pass
#########################################
######Download Youtube Single Video######
    def Save_Brwose(self):
        # save location in the line edit
        saveLocation = QFileDialog.getSaveFileName(self , caption="Save as" , directory="." , filter="All Files(*.*)")
        print(saveLocation)
        self.lineEdit_4.setText(str(saveLocation[0]))
    def Get_Video_Data(self):
        videoUrl=self.lineEdit_3.text()
        if videoUrl=="":
            QMessageBox.warning(self, "Data Error","Provide a valid video URL ")
        else:
            video=pafy.new(videoUrl)
            # print(video.title)
            # print(video.duration)
            # print(video.author)
            # print(video.length)
            # print(video.viewcount)
            # print(video.likes)
            # print(video.dislikes)
            videoStreams = video.videostreams
            for stream in videoStreams:
                data = "{} {} {} ".format(stream.mediatype, stream.extension, stream.quality,)
                self.comboBox.addItem(data)




    def Download_Video(self):
        videoUrl=self.lineEdit_3.text()
        saveLocation=self.lineEdit_4.text()
        if videoUrl=="" or saveLocation=="":
            QMessageBox.warning(self, "Data Error","Provide a valid URL or save location")

        else:
            video=pafy.new(videoUrl)
            videoStream=video.streams
            videoQuality=self.comboBox.currentIndex()
            download=videoStream[videoQuality].download(filepath=saveLocation,callback=self.Video_progress)
            QMessageBox.information(self, "Download Completed", "The Download Completed Successfully")
            self.lineEdit_3.setText("")
            self.lineEdit_4.setText("")
            self.progressBar_2.setValue(0)
    def Video_progress(self, total , received , ratio , rate , time):
        readData = received
        if total > 0:
            downloadPercentage = readData * 100 / total
            self.progressBar_2.setValue(downloadPercentage)
            remainingTime = round(time / 60, 2)

            self.label_5.setText(str('{} minutes remaining'.format(remainingTime)))
            QApplication.processEvents()
 ################################################
    ######### Youtube Playlist Download
    def Playlist_Download(self):
        playlist_url = self.lineEdit_5.text()
        save_location = self.lineEdit_6.text()

        if playlist_url == '' or save_location == '':
            QMessageBox.warning(self, "Data Error", "Provide a valid Playlist URL or save location")

        else:
            playlist = pafy.get_playlist(playlist_url)
            playlist_videos = playlist['items']

            self.lcdNumber_2.display(len(playlist_videos))

        os.chdir(save_location)
        if os.path.exists(str(playlist['title'])):
            os.chdir(str(playlist['title']))

        else:
            os.mkdir(str(playlist['title']))
            os.chdir(str(playlist['title']))

        current_video_in_download = 1
        quality = self.comboBox_2.currentIndex()

        QApplication.processEvents()

        for video in playlist_videos:
            current_video = video['pafy']
            current_video_stream = current_video.videostreams
            self.lcdNumber.display(current_video_in_download)
            download = current_video_stream[quality].download(callback=self.Playlist_Progress)
            QApplication.processEvents()

            current_video_in_download += 1


    def Playlist_Progress(self, total , received , ratio , rate , time):
            read_data = received
            if total > 0:
                download_percentage = read_data * 100 / total
                self.progressBar_3.setValue(download_percentage)
                remaining_time = round(time / 60, 2)

                self.label_6.setText(str('{} minutes remaining'.format(remaining_time)))
                QApplication.processEvents()

    def Playlist_Save_Browse(self):
        playlistSaveLocation = QFileDialog.getExistingDirectory(self, "Select Download Directory")
        self.lineEdit_6.setText(playlistSaveLocation)



##########################################
##### UI change Methods
    def Open_Home(self):
        self.tabWidget.setCurrentIndex(0)


    def Open_Download(self):
        self.tabWidget.setCurrentIndex(1)

    def Open_Youtube(self):
        self.tabWidget.setCurrentIndex(2)

    def Open_Settings(self):
        self.tabWidget.setCurrentIndex(3)





    #####################################
    ####App Themes#######################
    def Apply_DarkOrange_style(self):
        style=open("themes/darkorange.css")
        style=style.read()
        self.setStyleSheet(style)



    def Apply_QDark_Style(self):
        style = open("themes/qdark.css")
        style = style.read()
        self.setStyleSheet(style)


    def Apply_DarkGray_style(self):
        style = open("themes/qdarkgray.css")
        style = style.read()
        self.setStyleSheet(style)

    def Apply_QDarkblue_Style(self):
        style = open("themes/darkblu.css")
        style = style.read()
        self.setStyleSheet(style)


    ##########################################
    ####### App Animation

    def Move_Box_1(self):
        box_animation1 = QPropertyAnimation(self.groupBox_2 , b"geometry")
        box_animation1.setDuration(2500)
        box_animation1.setStartValue(QRect(0,0,0,0))
        box_animation1.setEndValue(QRect(60,40,281,141))
        box_animation1.start()
        self.box_animation1 = box_animation1


    def Move_Box_2(self):
        box_animation2 = QPropertyAnimation(self.groupBox_6 , b"geometry")
        box_animation2.setDuration(2500)
        box_animation2.setStartValue(QRect(0,0,0,0))
        box_animation2.setEndValue(QRect(380,40,281,141))
        box_animation2.start()
        self.box_animation2 = box_animation2


    def Move_Box_3(self):
        box_animation3 = QPropertyAnimation(self.groupBox_4 , b"geometry")
        box_animation3.setDuration(2500)
        box_animation3.setStartValue(QRect(0,0,0,0))
        box_animation3.setEndValue(QRect(60,210,281,141))
        box_animation3.start()
        self.box_animation3 = box_animation3


    def Move_Box_4(self):
        box_animation4 = QPropertyAnimation(self.groupBox_5 , b"geometry")
        box_animation4.setDuration(2500)
        box_animation4.setStartValue(QRect(0,0,0,0))
        box_animation4.setEndValue(QRect(380,210,281,141))
        box_animation4.start()
        self.box_animation4 = box_animation4
def main():
    app=QApplication(sys.argv)
    window=MainApp()
    window.show()
    app.exec_()
if __name__=='__main__':
    main()
