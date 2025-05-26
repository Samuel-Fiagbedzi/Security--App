import os
import numpy as np
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
from deepface import DeepFace as Dp
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.uic import loadUi
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import Qt
import imutils
import time
import cv2 as cv
from threading import Thread
from PIL import Image as Im
from pathlib import Path as Pt
import os
import signal

try:
    faceCascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
except Exception as e:
    print('Warning...', e)


class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainUi, self).__init__()
        loadUi("new.ui", self)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.showMaximized()
        self.fourcc = cv.VideoWriter.fourcc(*'XVID')
        # screen sizes
        self.screen_width = self.screen().size().width()
        self.screen_height = self.screen().size().height()
        # setMaximumSize(QtCore.QSize(100, 16777215))
        self.findframe.setMaximumSize(QtCore.QSize((self.screen_width - 100), (self.screen_height - 100)))
        self.imagesframe_2.setMaximumSize(QtCore.QSize((self.screen_width - 100), (self.screen_height - 100)))
        self.videoviewscreen.setMaximumSize(QtCore.QSize((self.screen_width - 100), (self.screen_height - 100)))
        self.add_screen.setMaximumSize(QtCore.QSize((self.screen_width - 100), (self.screen_height - 100)))
        # icon images
        find_btn_icon = QIcon()
        find_btn_icon.addPixmap(QtGui.QPixmap("feather/search.svg"))
        self.find_btn.setIcon(find_btn_icon)
        toggle_icon = QIcon()
        toggle_icon.addPixmap(QtGui.QPixmap("feather/menu.svg"))
        self.toggle.setIcon(toggle_icon)
        verify_sidebar_icon = QIcon()
        verify_sidebar_icon.addPixmap(QtGui.QPixmap("feather/check.svg"))
        self.verify_sidebar.setIcon(verify_sidebar_icon)
        video_icon = QIcon()
        video_icon.addPixmap(QtGui.QPixmap("icons/9054240_bx_cctv_icon.png"))
        self.video.setIcon(video_icon)
        icon_add = QIcon()
        icon_add.addPixmap(QtGui.QPixmap("feather/plus.svg"))
        self.add_btn.setIcon(icon_add)
        icon_light = QIcon()
        icon_light.addPixmap(QtGui.QPixmap("feather/sun.svg"))
        self.light_btn.setIcon(icon_light)
        icon_dark = QIcon()
        icon_dark.addPixmap(QtGui.QPixmap("feather/moon.svg"))
        self.dark_btn.setIcon(icon_dark)
        icon_min = QIcon()
        icon_min.addPixmap(QtGui.QPixmap("feather/minus.svg"))
        self.min_btn.setIcon(icon_min)
        icon_max = QIcon()
        icon_max.addPixmap(QtGui.QPixmap("feather/maximize.svg"))
        self.max_btn.setIcon(icon_max)
        icon_cancel = QIcon()
        icon_cancel.addPixmap(QtGui.QPixmap("feather/x.svg"))
        self.cancel_btn.setIcon(icon_cancel)

        # hiding frames to review welcome screen
        self.video_feed4 = 1
        self.video_feed1 = 1
        self.video_feed2 = 1
        self.video_feed3 = 1
        self.verify_image_1 = None
        self.verify_image_2 = None
        self.findimage = ""
        self.camera = None
        self.camera_2 = None
        self.camera_3 = None
        self.camera_4 = None
        self.closing = False
        self.closing_2 = False
        self.closing_3 = False
        self.closing_4 = False
        self.fps = 0
        self.fps4 = 0
        self.fps2 = 0
        self.fps3 = 0
        self.image_loaded = None
        self.image_loaded_2 = None
        self.image_loaded_3 = None
        self.image_loaded_4 = None
        self.centralwidget.setStyleSheet("background-color: rgb(92, 78, 78);"
                                         "color: dark;")
        self.findframemain.hide()
        self.verifyscreen.hide()
        self.videoviewscreen.hide()

        # add functionalities to the sidebar buttons
        self.video_thread = None
        self.video_thread2 = None
        self.video_thread3 = None
        self.video_thread4 = None
        self.Feedbtn1.clicked.connect(self.check_feed_area1)
        self.Feedbtn2.clicked.connect(self.check_feed_area2)
        self.Feedbtn3.clicked.connect(self.check_feed_area3)
        self.Feedbtn4.clicked.connect(self.check_feed_area4)
        self.cancel_btn.clicked.connect(self.close_)
        self.find_btn.clicked.connect(self.show_find)
        self.toggle.clicked.connect(self.toggled)
        self.verify_sidebar.clicked.connect(self.show_verify)
        self.video.clicked.connect(self.show_video)
        self.add_btn.clicked.connect(self.show_add_screen)
        # adding functionalities to verify/find buttons
        verify_thread = Thread(target=self.verify)
        find_thread = Thread(target=self.find_func)
        self.image1btn_2.clicked.connect(self.upload_verify_image_1)
        self.image2btn_2.clicked.connect(self.upload_verify_image_2)
        self.imagebtn_2.clicked.connect(self.upload_find_image1)
        self.dark_btn.clicked.connect(self.dark_theme_func)
        self.light_btn.clicked.connect(self.light_theme_func)
        self.verifybtn_4.clicked.connect(lambda: verify_thread.start())
        self.find_btn_4.clicked.connect(lambda: find_thread.start())

    def end_processes(self):
        os.killpg(os.getpgid(os.getpid()), signal.SIGTERM)

    def close_(self):
        self.closing = True
        self.closing_2 = True
        self.closing_3 = True
        self.closing_4 = True
        cv.destroyAllWindows()
        self.close()
        app.exit()

    def toggled(self):
        if self.sidebarmenucontainer_2.width() == 100:

            self.findframe.setMaximumSize(
                QtCore.QSize((self.screen_width - 58), (self.screen_height - 100)))
            self.imagesframe_2.setMaximumSize(
                QtCore.QSize((self.screen_width - 58), (self.screen_height - 100)))
            self.videoviewscreen.setMaximumSize(
                QtCore.QSize((self.screen_width - 58), (self.screen_height - 100)))
            self.add_screen.setMaximumSize(
                QtCore.QSize((self.screen_width - 58), (self.screen_height - 100)))
            self.sidebarmenucontainer_2.setFixedWidth(50)
            self.toggle.setText("")
            self.find_btn.setText("")
            self.verify_sidebar.setText("")
            self.video.setText("")
            self.add_btn.setText("")
            self.light_btn.setText("")
            self.dark_btn.setText("")
        else:
            self.findframe.setMaximumSize(
                QtCore.QSize((self.screen_width - 100), (self.screen_height - 100)))
            self.imagesframe_2.setMaximumSize(
                QtCore.QSize((self.screen_width - 100), (self.screen_height - 100)))
            self.videoviewscreen.setMaximumSize(
                QtCore.QSize((self.screen_width - 100), (self.screen_height - 100)))
            self.add_screen.setMaximumSize(
                QtCore.QSize((self.screen_width - 100), (self.screen_height - 100)))
            self.sidebarmenucontainer_2.setFixedWidth(100)
            self.toggle.setText("Menu")
            self.find_btn.setText("Find")
            self.verify_sidebar.setText("Verify")
            self.video.setText("Video")
            self.add_btn.setText("Add")
            self.light_btn.setText("Light")
            self.dark_btn.setText("Dark")

    def show_find(self):
        self.add_screen.hide()
        self.verifyscreen.hide()
        self.videoviewscreen.hide()
        self.findframemain.show()
        self.find_btn.setEnabled(False)

    def show_verify(self):
        self.add_screen.hide()
        self.verifyscreen.show()
        self.videoviewscreen.hide()
        self.findframemain.hide()

    def show_add_screen(self):
        self.add_screen.show()
        self.verifyscreen.hide()
        self.videoviewscreen.hide()
        self.findframemain.hide()

    def show_video(self):
        self.add_screen.hide()
        self.verifyscreen.hide()
        self.videoviewscreen.show()
        self.findframemain.hide()

    def dark_theme_func(self):
        self.setStyleSheet("background-color: rgb(92, 78, 78);"
                           "color: white;")
        self.centralwidget.setStyleSheet("background-color: rgb(92, 78, 78);"
                                         "color: white;")
        self.toggle.setStyleSheet("color:rgb(255, 255, 255);\n"
                                  "background-color:rgb(152, 134, 134);\n"
                                  "height: 20;\n"
                                  "border-radius: 10;\n"
                                  
                                  "padding: 5px;\n"
                                  "font: 10pt \"Arial Rounded MT Bold\";\n"
                                  "")
        self.find_btn.setStyleSheet("color:rgb(255, 255, 255);\n"
                                   "background-color:rgb(152, 134, 134);\n"
                                   "height: 20;\n"
                                   "border-radius: 10;\n"
                                   
                                   "padding: 5px;\n"
                                   "font: 10pt \"Arial Rounded MT Bold\";\n"
                                   "")
        self.add_btn.setStyleSheet("color:rgb(255, 255, 255);\n"
                                  "background-color:rgb(152, 134, 134);\n"
                                  "height: 20;\n"
                                  "border-radius: 10;\n"
                                  
                                  "padding: 5px;\n"
                                  "font: 10pt \"Arial Rounded MT Bold\";\n"
                                  "")
        self.light_btn.setStyleSheet("color:rgb(255, 255, 255);\n"
                                 "background-color:rgb(152, 134, 134);\n"
                                 "height: 20;\n"
                                 "border-radius: 10;\n"
                                 
                                 "padding: 5px;\n"
                                 "font: 10pt \"Arial Rounded MT Bold\";\n"
                                 "")
        self.dark_btn.setStyleSheet("color:rgb(255, 255, 255);\n"
                                 "background-color:rgb(152, 134, 134);\n"
                                 "height: 20;\n"
                                 "border-radius: 10;\n"
                                 
                                 "padding: 5px;\n"
                                 "font: 10pt \"Arial Rounded MT Bold\";\n"
                                 "")
        self.verify_sidebar.setStyleSheet("color:rgb(255, 255, 255);\n"
                                         "background-color:rgb(152, 134, 134);\n"
                                         "height: 20;\n"
                                         "border-radius: 10;\n"
                                         
                                         "padding: 5px;\n"
                                         "font: 10pt \"Arial Rounded MT Bold\";\n"
                                         "")
        self.video.setStyleSheet("color:rgb(255, 255, 255);\n"
                                 "background-color:rgb(152, 134, 134);\n"
                                 "height: 20;\n"
                                 "border-radius: 10;\n"
                                 
                                 "padding: 5px;\n"
                                 "font: 10pt \"Arial Rounded MT Bold\";\n"
                                 "")
        self.add_screen.setStyleSheet(
            "background-color:#988686;\n"
            "border-radius: 10;\n"

        )
        self.welcomemiddleframe.setStyleSheet(
            "background-color:rgb(152, 134, 134);\n"
            "border-radius: 10;\n"

        )
        self.videoviewscreen.setStyleSheet(
            "background-color:rgb(92, 78, 78)\n"
            "border-radius: 10;\n"

        )
        self.camera1.setStyleSheet(
            "background-color:#988686;\n"
            "border-radius: 10;\n"

        )
        self.camera2.setStyleSheet(
            "background-color:#988686;\n"
            "border-radius: 10;\n"

        )
        self.camera3.setStyleSheet(
            "background-color:#988686;\n"
            "border-radius: 10;\n"

        )
        self.camera4.setStyleSheet(
            "background-color:#988686;\n"
            "border-radius: 10;\n"

        )
        self.imagesframe_2.setStyleSheet(
            "background-color: rgb(92, 78, 78);\n"
            "border-radius: 10;\n"

        )
        self.image1_2.setStyleSheet(
            "background-color:#988686;\n"
            "border-radius: 10;\n"

        )
        self.image2_2.setStyleSheet(
            "background-color:#988686;\n"
            "border-radius: 10;\n"

        )
        self.findframe.setStyleSheet(
            "background-color:rgb(92, 78, 78)\n"
            "border-radius: 10;\n"

        )

        self.findimage_2.setStyleSheet(
            "background-color:#988686;\n"
            "border-radius: 10;\n"

        )
        self.results_2.setStyleSheet(
            "background-color:#988686;\n"
            "border-radius: 10;\n"

        )

        self.imagebtn_2.setStyleSheet("color:rgb(255, 255, 255);\n"
                                      "background-color:rgb(152, 134, 134);\n"
                                      "height: 20;\n"
                                      "border-radius: 10;\n"
                                      
                                      "padding: 5px;\n"
                                      "font: 10pt \"Arial Rounded MT Bold\";\n"
                                      "")
        self.find_btn_4.setStyleSheet("color:rgb(255, 255, 255);\n"
                                     "background-color:rgb(152, 134, 134);\n"
                                     "height: 20;\n"
                                     "border-radius: 10;\n"
                                     
                                     "padding: 5px;\n"
                                     "font: 10pt \"Arial Rounded MT Bold\";\n"
                                     "")
        self.image1btn_2.setStyleSheet("color:rgb(255, 255, 255);\n"
                                       "background-color:rgb(152, 134, 134);\n"
                                       "height: 20;\n"
                                       "border-radius: 10;\n"
                                       
                                       "padding: 5px;\n"
                                       "font: 10pt \"Arial Rounded MT Bold\";\n"
                                       "")
        self.image2btn_2.setStyleSheet("color:rgb(255, 255, 255);\n"
                                       "background-color:rgb(152, 134, 134);\n"
                                       "height: 20;\n"
                                       "border-radius: 10;\n"
                                       
                                       "padding: 5px;\n"
                                       "font: 10pt \"Arial Rounded MT Bold\";\n"
                                       "")
        self.verifybtn_4.setStyleSheet("color:rgb(255, 255, 255);\n"
                                       "background-color:rgb(152, 134, 134);\n"
                                       "height: 20;\n"
                                       "border-radius: 10;\n"
                                       
                                       "padding: 5px;\n"
                                       "font: 10pt \"Arial Rounded MT Bold\";\n"
                                       "")
        self.Feedbtn1.setStyleSheet("color:rgb(255, 255, 255);\n"
                                    "background-color:rgb(92, 78, 78);\n"
                                    "height: 20;\n"
                                    "border-radius: 10;\n"
                                    
                                    "padding: 5px;\n"
                                    "font: 10pt \"Arial Rounded MT Bold\";\n"
                                    "")
        self.Feedbtn2.setStyleSheet("color:rgb(255, 255, 255);\n"
                                    "background-color:rgb(92, 78, 78);\n"
                                    "height: 20;\n"
                                    "border-radius: 10;\n"
                                    
                                    "padding: 5px;\n"
                                    "font: 10pt \"Arial Rounded MT Bold\";\n"
                                    "")
        self.Feedbtn3.setStyleSheet("color:rgb(255, 255, 255);\n"
                                    "background-color:rgb(92, 78, 78);\n"
                                    "height: 20;\n"
                                    "border-radius: 10;\n"
                                    
                                    "padding: 5px;\n"
                                    "font: 10pt \"Arial Rounded MT Bold\";\n"
                                    "")
        self.Feedbtn4.setStyleSheet("color:rgb(255, 255, 255);\n"
                                    "background-color:rgb(92, 78, 78);\n"
                                    "height: 20;\n"
                                    "border-radius: 10;\n"
                                    
                                    "padding: 5px;\n"
                                    "font: 10pt \"Arial Rounded MT Bold\";\n"
                                    "")
        self.feed_area1.setStyleSheet("color:rgb(255, 255, 255);\n"
                                      "background-color:rgb(92, 78, 78);\n"
                                      "height:30;\n"
                                      "border-radius: 10;\n"
                                      
                                      "padding: 5px;\n"
                                      "font: 15pt \"Arial Rounded MT Bold\";\n"
                                      "")
        self.feed_area2.setStyleSheet("color:rgb(255, 255, 255);\n"
                                      "background-color:rgb(92, 78, 78);\n"
                                      "height: 30;\n"
                                      "border-radius: 10;\n"
                                      
                                      "padding: 5px;\n"
                                      "font5 15pt \"Arial Rounded MT Bold\";\n"
                                      "")
        self.feed_area3.setStyleSheet("color:rgb(255, 255, 255);\n"
                                      "background-color:rgb(92, 78, 78);\n"
                                      "height: 30;\n"
                                      "border-radius: 10;\n"
                                      
                                      "padding: 5px;\n"
                                      "font5 15pt \"Arial Rounded MT Bold\";\n"
                                      "")
        self.feed_area4.setStyleSheet("color:rgb(255, 255, 255);\n"
                                      "background-color:rgb(92, 78, 78);\n"
                                      "height: 30;\n"
                                      "border-radius: 10;\n"
                                      
                                      "padding: 5px;\n"
                                      "font5 15pt \"Arial Rounded MT Bold\";\n"
                                      "")

    def light_theme_func(self):
        self.setStyleSheet("background-color:rgb(179, 179, 179);"
                           "color: black;")
        self.centralwidget.setStyleSheet("background-color:rgb(179, 179, 179)\n"
                                         "color: black;")
        self.toggle.setStyleSheet("color:rgb(0, 0, 0);\n"
                                  "background-color:rgb(212, 212, 212);\n"
                                  "height: 20;\n"
                                  "border-radius: 10;\n"
                                  
                                  "padding: 5px;\n"
                                  "font: 10pt \"Arial Rounded MT Bold\";\n"
                                  "")
        self.find_btn.setStyleSheet("color:rgb(0, 0, 0);\n"
                                   "background-color:rgb(212, 212, 212);\n"
                                   "height: 20;\n"
                                   "border-radius: 10;\n"

                                   "padding: 5px;\n"
                                   "font: 10pt \"Arial Rounded MT Bold\";\n"
                                   "")
        self.add_btn.setStyleSheet("color:rgb(0, 0, 0);\n"
                                  "background-color:rgb(212, 212, 212);\n"
                                  "height: 20;\n"
                                  "border-radius: 10;\n"
                                  
                                  "padding: 5px;\n"
                                  "font: 10pt \"Arial Rounded MT Bold\";\n"
                                  "")
        self.light_btn.setStyleSheet("color:rgb(0, 0, 0);\n"
                                 "background-color:rgb(212, 212, 212);\n"
                                 "height: 20;\n"
                                 "border-radius: 10;\n"
                                 
                                 "padding: 5px;\n"
                                 "font: 10pt \"Arial Rounded MT Bold\";\n"
                                 "")
        self.dark_btn.setStyleSheet("color:rgb(0, 0, 0);\n"
                                 "background-color:rgb(212, 212, 212);\n"
                                 "height: 20;\n"
                                 "border-radius: 10;\n"
                                 
                                 "padding: 5px;\n"
                                 "font: 10pt \"Arial Rounded MT Bold\";\n"
                                 "")
        self.verify_sidebar.setStyleSheet("color:rgb(0, 0, 0);\n"
                                         "background-color:rgb(212, 212, 212);\n"
                                         "height: 20;\n"
                                         "border-radius: 10;\n"
                                         
                                         "padding: 5px;\n"
                                         "font: 10pt \"Arial Rounded MT Bold\";\n"
                                         "")
        self.video.setStyleSheet("color:rgb(0, 0, 0);\n"
                                 "background-color:rgb(212, 212, 212);\n"
                                 "height: 20;\n"
                                 "border-radius: 10;\n"
                                 
                                 "padding: 5px;\n"
                                 "font: 10pt \"Arial Rounded MT Bold\";\n"
                                 "")
        self.add_screen.setStyleSheet(
            "background-color:rgb(212, 212, 212);\n"
            "border-radius: 10;\n"

        )
        self.welcomemiddleframe.setStyleSheet(
            "background-color:rgb(212, 212, 212);\n"
            "border-radius: 10;\n"

        )
        self.videoviewscreen.setStyleSheet(
            "background-color:rgb(179, 179, 179)\n"
            "border-radius: 10;\n"

        )
        self.camera1.setStyleSheet(
            "background-color:rgb(0, 0, 0)\n"
            "border-radius: 10;\n"

        )
        self.camera2.setStyleSheet(
            "background-color:rgb(0, 0, 0)\n"
            "border-radius: 10;\n"

        )
        self.camera3.setStyleSheet(
            "background-color:rgb(0, 0, 0)\n"
            "border-radius: 10;\n"

        )
        self.camera4.setStyleSheet(
            "background-color:rgb(0, 0, 0)\n"
            "border-radius: 10;\n"

        )
        self.imagesframe_2.setStyleSheet(
            "background-color:rgb(179, 179, 179)\n"
            "border-radius: 10;\n"

        )
        self.image1_2.setStyleSheet(
            "background-color:rgb(0, 0, 0)\n"
            "border-radius: 10;\n"

        )
        self.image2_2.setStyleSheet(
            "background-color:rgb(0, 0, 0)\n"
            "border-radius: 10;\n"

        )
        self.findframe.setStyleSheet(
            "background-color:rgb(179, 179, 179)\n"
            "border-radius: 10;\n"

        )
        self.findimage_2.setStyleSheet(
            "background-color:rgb(0, 0, 0)\n"
            "border-radius: 10;\n"

        )
        self.results_2.setStyleSheet(
            "background-color:rgb(0, 0, 0)\n"
            "border-radius: 10;\n"

        )

        self.imagebtn_2.setStyleSheet("color:rgb(0, 0, 0);\n"
                                      "background-color:rgb(212, 212, 212);\n"
                                      "height: 20;\n"
                                      "border-radius: 10;\n"
                                      
                                      "padding: 5px;\n"
                                      "font: 10pt \"Arial Rounded MT Bold\";\n"
                                      "")
        self.find_btn_4.setStyleSheet("color:rgb(0, 0, 0);\n"
                                     "background-color:rgb(212, 212, 212);\n"
                                     "height: 20;\n"
                                     "border-radius: 10;\n"
                                     
                                     "padding: 5px;\n"
                                     "font: 10pt \"Arial Rounded MT Bold\";\n"
                                     "")
        self.image1btn_2.setStyleSheet("color:rgb(0, 0, 0);\n"
                                       "background-color:rgb(212, 212, 212);\n"
                                       "height: 20;\n"
                                       "border-radius: 10;\n"
                                       
                                       "padding: 5px;\n"
                                       "font: 10pt \"Arial Rounded MT Bold\";\n"
                                       "")
        self.image2btn_2.setStyleSheet("color:rgb(0, 0, 0);\n"
                                       "background-color:rgb(212, 212, 212);\n"
                                       "height: 20;\n"
                                       "border-radius: 10;\n"
                                       
                                       "padding: 5px;\n"
                                       "font: 10pt \"Arial Rounded MT Bold\";\n"
                                       "")
        self.verifybtn_4.setStyleSheet("color:rgb(0, 0, 0);\n"
                                       "background-color:rgb(212, 212, 212);\n"
                                       "height: 20;\n"
                                       "border-radius: 10;\n"
                                       
                                       "padding: 5px;\n"
                                       "font: 10pt \"Arial Rounded MT Bold\";\n"
                                       "")
        self.Feedbtn1.setStyleSheet("color:rgb(0, 0, 0);\n"
                                    "background-color:rgb(179, 179, 179);\n"
                                    "height: 20;\n"
                                    "border-radius: 10;\n"
                                    
                                    "padding: 5px;\n"
                                    "font: 10pt \"Arial Rounded MT Bold\";\n"
                                    "")
        self.Feedbtn2.setStyleSheet("color:rgb(0, 0, 0);\n"
                                    "background-color:rgb(179, 179, 179);\n"
                                    "height: 20;\n"
                                    "border-radius: 10;\n"
                                    
                                    "padding: 5px;\n"
                                    "font: 10pt \"Arial Rounded MT Bold\";\n"
                                    "")
        self.Feedbtn3.setStyleSheet("color:rgb(0, 0, 0);\n"
                                    "background-color:rgb(179, 179, 179);\n"
                                    "height: 20;\n"
                                    "border-radius: 10;\n"
                                    
                                    "padding: 5px;\n"
                                    "font: 10pt \"Arial Rounded MT Bold\";\n"
                                    "")
        self.Feedbtn4.setStyleSheet("color:rgb(0, 0, 0);\n"
                                    "background-color:rgb(179, 179, 179);\n"
                                    "height: 20;\n"
                                    "border-radius: 10;\n"
                                    
                                    "padding: 5px;\n"
                                    "font: 10pt \"Arial Rounded MT Bold\";\n"
                                    "")
        self.feed_area1.setStyleSheet("color:rgb(0, 0, 0);\n"
                                      "background-color:rgb(179, 179, 179);\n"
                                      "height: 30;\n"
                                      "border-radius: 10;\n"
                                      
                                      "padding: 5px;\n"
                                      "font: 15pt \"Arial Rounded MT Bold\";\n"
                                      "")
        self.feed_area2.setStyleSheet("color:rgb(0, 0, 0);\n"
                                      "background-color:rgb(179, 179, 179);\n"
                                      "height: 30;\n"
                                      "border-radius: 10;\n"
                                      
                                      "padding: 5px;\n"
                                      "font: 15pt \"Arial Rounded MT Bold\";\n"
                                      "")
        self.feed_area3.setStyleSheet("color:rgb(0, 0, 0);\n"
                                      "background-color:rgb(179, 179, 179);\n"
                                      "height: 30;\n"
                                      "border-radius: 10;\n"
                                      
                                      "padding: 5px;\n"
                                      "font: 15pt \"Arial Rounded MT Bold\";\n"
                                      "")
        self.feed_area4.setStyleSheet("color:rgb(0, 0, 0);\n"
                                      "background-color:rgb(179, 179, 179);\n"
                                      "height: 30;\n"
                                      "border-radius: 10;\n"
                                      
                                      "padding: 5px;\n"
                                      "font: 15pt \"Arial Rounded MT Bold\";\n"
                                      "")

    def system(self):
        pass

    def check_feed_area1(self):
        if str(self.feed_area1.text()) == "":
            pass
        else:
            if str(self.feed_area1.text()) in ["1", "2", "0", "4"]:
                self.video_feed1 = int(self.feed_area1.text())
                self.video_thread = Thread(target=self.load_image, args=(self.video_feed1,))
                self.video_thread.start()
            else:
                self.video_feed1 = self.feed_area1.text()
                self.video_thread = Thread(target=self.load_image, args=(self.video_feed1,))
                self.video_thread.start()

    def check_feed_area2(self):
        if str(self.feed_area2.text()) == "":
            pass
        else:
            if str(self.feed_area2.text()) in ["1", "2", "0", "4"]:
                self.video_feed2 = int(self.feed_area2.text())
                self.video_thread2 = Thread(target=self.load_image2, args=(self.video_feed2,))
                self.video_thread2.start()
            else:
                self.video_feed2 = self.feed_area2.text()
                self.video_thread2 = Thread(target=self.load_image2, args=(self.video_feed2,))
                self.video_thread2.start()

    def check_feed_area3(self):
        if str(self.feed_area3.text()) == "":
            pass
        else:
            if str(self.feed_area3.text()) in ["1", "2", "0", "4"]:
                self.video_feed3 = int(self.feed_area3.text())
                self.video_thread3 = Thread(target=self.load_image3, args=(self.video_feed3,))
                self.video_thread3.start()
            else:
                self.video_thread3 = Thread(target=self.load_image3, args=(self.video_feed3,))
                self.video_thread3.start()

    def check_feed_area4(self):
        if str(self.feed_area4.text()) == "":
            pass
        else:
            if str(self.feed_area4.text()) in ["1", "2", "0", "4"]:
                self.video_feed4 = int(self.feed_area4.text())
                self.video_thread4 = Thread(target=self.load_image4, args=(self.video_feed4,))
                self.video_thread4.start()
            else:
                self.video_thread4 = Thread(target=self.load_image4, args=(self.video_feed4,))
                self.video_thread4.start()

    def retrieve_video_feed(self):
        if len(self.video_feeds) > 0:
            for x in self.video_feeds:
                cv.VideoCapture(x)

    def load_image(self, feed):
        """ This function will load the camera device, obtain the image
            and set it to label using the set_photo function
        """
        self.add_screen.hide()
        self.verifyscreen.hide()
        self.videoviewscreen.show()
        self.show_video()
        self.findframemain.hide()
        self.camera = cv.VideoCapture(feed)
        out = cv.VideoWriter('Camera 1' + str \
            (time.strftime("%Y-%b-%d at %H.%M.%S %p")) + '.avi', self.fourcc, 20, (640, 480))
        old_time = time.perf_counter()
        while True:
            if self.closing:
                break
            else:
                ret, img = self.camera.read()
                if ret:
                    new = time.perf_counter()
                    if (new - old_time) > 5:
                        out = cv.VideoWriter('Camera 1' + str \
                            (time.strftime("%Y-%b-%d at %H.%M.%S %p")) + '.avi', self.fourcc, 20, (640, 480))
                        old_time = new
                    out.write(img)
                    fps = self.camera.get(cv.CAP_PROP_FPS)
                    img = cv.flip(img, 1)
                    img = cv.putText(img, f'Camera 1 {fps} fps',
                                     (0, 20),  # top-left corner coordinates
                                     cv.FONT_HERSHEY_SIMPLEX,  # Font type (SIMPLEX, PLAIN, etc.)
                                     0.5,  # Font scale
                                     (0, 0, 0),  # Font color (BGR)
                                     1,  # Text thickness
                                     cv.LINE_AA)  # Line type (AA for antialiasing)
                    frame = cv.cvtColor(img, cv.COLOR_BGR2RGB)
                    image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
                    self.image_loaded = image
                    self.label_14.setPixmap(QPixmap.fromImage(image))
        self.camera.release()

    def load_image_2(self, feed_2):
        """ This function will load the camera device, obtain the image
            and set it to label using the set_photo function
        """
        self.add_screen.hide()
        self.verifyscreen.hide()
        self.videoviewscreen.show()
        self.show_video()
        self.findframemain.hide()
        self.camera_2 = cv.VideoCapture(feed_2)
        out_2 = cv.VideoWriter('Camera 2' + str \
            (time.strftime("%Y-%b-%d at %H.%M.%S %p")) + '.avi', self.fourcc, 20, (640, 480))
        old_time_2 = time.perf_counter()
        while True:
            if self.closing2:
                self.camera2.release()
                break
            else:
                ret_2, img_2 = self.camera_2.read()
                if ret_2:
                    new_2 = time.perf_counter()
                    if (new_2 - old_time_2) > 5:
                        out_2 = cv.VideoWriter('Camera 2' + str \
                            (time.strftime("%Y-%b-%d at %H.%M.%S %p")) + '.avi', self.fourcc, 20, (640, 480))
                        old_time_2 = new_2
                    out_2.write(img_2)
                    fps_2 = self.camera_2.get(cv.CAP_PROP_FPS)
                    img_2 = cv.flip(img_2, 1)
                    img_2 = imutils.resize(img_2, width=int((self.videoviewscreen.width() - 30) / 2),
                                         height=int((self.videoviewscreen.height() - 30) / 2))
                    img_2 = cv.putText(img_2, f'Camera 2 {fps_2} fps',
                                     (0, 20),  # top-left corner coordinates
                                     cv.FONT_HERSHEY_SIMPLEX,  # Font type (SIMPLEX, PLAIN, etc.)
                                     0.5,  # Font scale
                                     (0, 0, 0),  # Font color (BGR)
                                     1,  # Text thickness
                                     cv.LINE_AA)  # Line type (AA for antialiasing)
                    frame_2 = cv.cvtColor(img_2, cv.COLOR_BGR2RGB)
                    image_2 = QImage(frame_2, frame_2.shape[1], frame_2.shape[0], frame_2.strides[0], QImage.Format_RGB888)
                    self.image_loaded_2 = image_2
                    self.label_15.setPixmap(QPixmap.fromImage(image_2))

    def load_image_3(self, feed_3):
        """ This function will load the camera device, obtain the image
            and set it to label using the set_photo function
        """
        self.add_screen.hide()
        self.verifyscreen.hide()
        self.videoviewscreen.show()
        self.show_video()
        self.findframemain.hide()
        self.camera_3 = cv.VideoCapture(feed_3)
        out_3 = cv.VideoWriter('Camera 3' + str \
            (time.strftime("%Y-%b-%d at %H.%M.%S %p")) + '.avi', self.fourcc, 20, (640, 480))
        old_time_3 = time.perf_counter()
        while True:
            if self.closing3:
                self.camera3.release()
                break
            else:
                ret_3, img_3 = self.camera_3.read()
                if ret_3:
                    new_3 = time.perf_counter()
                    if (new_3 - old_time_3) > 5:
                        out_3 = cv.VideoWriter('Camera 3' + str \
                            (time.strftime("%Y-%b-%d at %H.%M.%S %p")) + '.avi', self.fourcc, 20, (640, 480))
                        old_time_3 = new_3
                    out_3.write(img_3)
                    fps_3 = self.camera_3.get(cv.CAP_PROP_FPS)
                    img_3 = cv.flip(img_3, 1)
                    img_3 = imutils.resize(img_3, width=int((self.videoviewscreen.width() - 30) / 2),
                                         height=int((self.videoviewscreen.height() - 30) / 2))
                    img_3 = cv.putText(img_3, f'Camera 3 {fps_3} fps',
                                     (0, 20),  # top-left corner coordinates
                                     cv.FONT_HERSHEY_SIMPLEX,  # Font type (SIMPLEX, PLAIN, etc.)
                                     0.5,  # Font scale
                                     (0, 0, 0),  # Font color (BGR)
                                     1,  # Text thickness
                                     cv.LINE_AA)  # Line type (AA for antialiasing)
                    frame_3 = cv.cvtColor(img_3, cv.COLOR_BGR2RGB)
                    image_3 = QImage(frame_3, frame_3.shape[1], frame_3.shape[0], frame_3.strides[0], QImage.Format_RGB888)
                    self.image_loaded_3 = image_3
                    self.label_16.setPixmap(QPixmap.fromImage(image_3))

    def load_image4(self, feed_4):
        """ This function will load the camera device, obtain the image
            and set it to label using the set_photo function
        """
        self.add_screen.hide()
        self.verifyscreen.hide()
        self.videoviewscreen.show()
        self.show_video()
        self.findframemain.hide()
        self.camera_4 = cv.VideoCapture(feed_4)
        out_4 = cv.VideoWriter('Camera 4' + str \
            (time.strftime("%Y-%b-%d at %H.%M.%S %p")) + '.avi', self.fourcc, 20, (640, 480))
        old_time_4 = time.perf_counter()
        while True:
            if self.closing_4:
                break
            else:
                ret_4, img_4 = self.camera_4.read()
                if ret_4:
                    new_4 = time.perf_counter()
                    if (new_4 - old_time_4) > 5:
                        out_4 = cv.VideoWriter('Camera 4' + str \
                            (time.strftime("%Y-%b-%d at %H.%M.%S %p")) + '.avi', self.fourcc, 20, (640, 480))
                        old_time_4 = new_4
                    out_4.write(img_4)
                    fps_4 = self.camera_4.get(cv.CAP_PROP_FPS)
                    img_4 = cv.flip(img_4, 1)
                    img_4 = imutils.resize(img_4, width=int((self.videoviewscreen.width() - 30) / 2),
                                         height=int((self.videoviewscreen.height() - 30) / 2))
                    img_4 = cv.putText(img_4, f'Camera 4 {fps_4} fps',
                                     (0, 20),  # top-left corner coordinates
                                     cv.FONT_HERSHEY_SIMPLEX,  # Font type (SIMPLEX, PLAIN, etc.)
                                     0.5,  # Font scale
                                     (0, 0, 0),  # Font color (BGR)
                                     1,  # Text thickness
                                     cv.LINE_AA)  # Line type (AA for antialiasing)
                    frame_4 = cv.cvtColor(img_4, cv.COLOR_BGR2RGB)
                    image_4 = QImage(frame_4, frame_4.shape[1], frame_4.shape[0], frame_4.strides[0], QImage.Format_RGB888)
                    self.image_loaded_4 = image_4
                    self.label_17.setPixmap(QPixmap.fromImage(image_4))
        self.camera4.release()

    def upload_verify_image_1(self):
        # setMaximumSize(QtCore.QSize(100, 16777215))
        print(self.size().width())
        self.label_18.setMaximumSize(QtCore.QSize((self.label_18.size().width()), (self.label_18.size().width())))
        image1 = QFileDialog.getOpenFileName()
        self.verify_image_1 = image1[0]
        self.label_18.setPixmap(QtGui.QPixmap(str(image1[0])))

    def upload_verify_image_2(self):
        self.label_18.setMaximumSize(QtCore.QSize(self.label_18.size().width(), self.label_18.size().width()))
        image2 = QFileDialog.getOpenFileName()
        self.verify_image_2 = image2[0]
        self.label_19.setPixmap(QtGui.QPixmap(str(image2[0])))

    def upload_find_image1(self):
        image2 = QFileDialog.getOpenFileName()
        self.findimage = image2[0]
        self.label_20.setPixmap(QtGui.QPixmap(str(image2[0])))

    def verify(self):
        result = Dp.verify(img1_path=self.verify_image_1, img2_path=self.verify_image_2)

        print(Pt(self.verify_image_2))
        img = np.array(Im.open(self.verify_image_2))
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        img = cv.putText(img, str(result["verified"]),
                         (400, 0),  # top-left corner coordinates
                         cv.FONT_HERSHEY_SIMPLEX,  # Font type (SIMPLEX, PLAIN, etc.)
                         7,  # Font scale
                         (0, 0, 0),  # Font color (BGR)
                         5,  # Text thickness
                         cv.LINE_AA)  # Line type (AA for antialiasing)
        frame = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        self.label_19.setPixmap(QtGui.QPixmap.fromImage(image))

    def find_func(self):
        try:
            result = Dp.find(img_path=self.findimage, db_path="dataset")
            # print(result[0]["identity"][0])
            # img_path = path.Path(str(result[0]["identity"][0]))
            # img = imutils.resize(img_path, width=int((self.results_2.width() - 30) / 2),
            #                      height=int((self.results_2.height() - 30) / 2))
            # frame = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            # image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
            # self.found_label.setPixmap(QPixmap.fromImage(image))
            self.found_label.setPixmap(QtGui.QPixmap(str(result[0]["identity"][0])))
        except Exception as exception:
            print(exception)

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MainUi()
    ui.show()
    sys.exit(app.exec())
