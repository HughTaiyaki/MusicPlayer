"""

author: hugh yau
date: 2024/01/09
1. 打开文件夹
2. 播放音乐
"""
import os, time
from random import random

from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import *


class Player(QWidget):
    # 初始化
    def __init__(self):
        super().__init__()
        # 音乐列表声明与定义
        self.cur_playing_song = ''
        self.songs_list = []
        self.song_formats = ['mp3', 'm4a', 'flac', 'wav', 'ogg']
        # self.settingfilename = 'setting.ini'
        self.is_pause = True
        # 播放/暂停
        self.player = QMediaPlayer()
        self.is_switching = False
        self.playMode = 0  # 默认顺序播放

        self.init_UI()
        self.open_btn.clicked.connect(self.openDir)
        self.play_btn.clicked.connect(self.playMusic)
        self.prev_btn.clicked.connect(self.prevMusic)
        self.next_btn.clicked.connect(self.nextMusic)
        self.music_list.itemDoubleClicked.connect(self.doubleClicked)
        self.combo_btn.clicked.connect(self.playModeSet)
        self.volume_slider.valueChanged.connect(self.setVolume)
    # 初始化UI
    def init_UI(self):
        self.setWindowTitle('音乐播放器')
        self.setWindowIcon(QIcon('resource/image/favicon.png'))
        self.resize(900, 600)
        # 设置背景图片
        # self.setStyleSheet("background-image: url('background.jpg');")

        # UI设计外部布局器
        self.main_container = QVBoxLayout()

        # 音乐列表
        self.music_list = QListWidget()
        self.main_container.addWidget(self.music_list)

        # 播放条
        self.start_label = QLabel('00:00')
        self.end_label = QLabel('00:00')
        self.slider = QSlider(Qt.Horizontal, self)
        self.h_box_slider = QHBoxLayout()
        self.h_box_slider.addWidget(self.start_label)
        self.h_box_slider.addWidget(self.slider)
        self.h_box_slider.addWidget(self.end_label)

        # 功能按钮
        self.combo_btn = QPushButton('顺序播放[可切换]', self)
        # self.combo_btn.addItem('顺序播放')
        # self.combo_btn.addItem('单曲循环')
        # self.combo_btn.addItem('随机播放')

        self.play_btn = QPushButton('播放', self)
        self.prev_btn = QPushButton('上一曲', self)
        self.next_btn = QPushButton('下一曲', self)
        self.open_btn = QPushButton('打开文件夹', self)
        self.h_box_button = QHBoxLayout()
        # 添加控件
        self.h_box_button.addWidget(self.play_btn)
        self.h_box_button.addWidget(self.next_btn)
        self.h_box_button.addWidget(self.prev_btn)
        self.h_box_button.addWidget(self.combo_btn)
        self.h_box_button.addWidget(self.open_btn)

        # 音量
        self.volume_slider = QSlider(Qt.Horizontal, self)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(50)  # Default
        self.volume_slider.setTickInterval(10)
        self.volume_slider.setTickPosition(QSlider.TicksBelow)
        self.volume_label = QLabel('音量:', self)
        self.h_box_volume = QHBoxLayout()
        self.h_box_volume.addWidget(self.volume_label)
        self.h_box_volume.addWidget(self.volume_slider)

        # 设置布局器
        self.main_container.addLayout(self.h_box_slider)
        self.main_container.addLayout(self.h_box_button)
        self.main_container.addLayout(self.h_box_volume)
        self.setLayout(self.main_container)

    # 打开文件夹
    def openDir(self):
        self.cur_path = QFileDialog.getExistingDirectory(self, "选取音乐文件夹", './')
        if self.cur_path:
            self.showMusicList()
            self.cur_playing_song = ''
            self.start_label.setText('00:00')
            self.end_label.setText('00:00')
            self.slider.setSliderPosition(0)
            self.is_pause = True
            self.play_btn.setText('播放')

    # def showMusicList(self):
    #     self.music_list.clear()
    #     for song in os.listdir(self.cur_path):
    #         if song.split('.')[-1] in self.song_formats:
    #             self.songs_list.append([song, os.path.join(self.cur_path, song).replace('\\', '/')])
    #             self.music_list.addItem(song)
    #     self.music_list.setCurrentRow(0)
    #     if self.songs_list:
    #         self.cur_playing_song = self.songs_list[self.music_list.currentRow()][-1]
    def showMusicList(self):
        self.music_list.clear()
        for song in os.listdir(self.cur_path):
            if song.split('.')[-1] in self.song_formats:
                song_path = os.path.join(self.cur_path, song).replace('\\', '/')
                song_name = os.path.splitext(song)[0]  # 移除后缀名
                self.songs_list.append([song_name, song_path])
                self.music_list.addItem(song_name)
        self.music_list.setCurrentRow(0)
        if self.songs_list:
            self.cur_playing_song = self.songs_list[self.music_list.currentRow()][-1]

    # 播放音乐
    def setCurPlaying(self):
        self.cur_playing_song = self.songs_list[self.music_list.currentRow()][-1]
        self.player.setMedia(QMediaContent(QUrl(self.cur_playing_song)))

    def playMusic(self):
        if self.music_list.count() == 0:
            QMessageBox.about(self, "tip", '当前路径无可播放的音乐')
            return
        if not self.player.isAudioAvailable():
            self.setCurPlaying()
        if self.is_pause or self.is_switching:
            self.player.play()
            self.is_pause = False
            self.play_btn.setText('暂停')
        elif (not self.is_pause) and (not self.is_switching):
            self.player.pause()
            self.is_pause = True
            self.play_btn.setText('播放')

    # 更改音量
    def setVolume(self):
        volume = self.volume_slider.value()
        self.player.setVolume(volume)
    # 上一曲
    def prevMusic(self):
        self.slider.setValue(0)
        if self.music_list.count() == 0:
            return
        pre_row = self.music_list.currentRow()-1 if self.music_list.currentRow() != 0 else self.music_list.count() - 1
        self.music_list.setCurrentRow(pre_row)
        self.is_switching = True
        self.setCurPlaying()
        self.playMusic()
        self.is_switching = False

    # 下一曲
    def nextMusic(self):
        self.slider.setValue(0)
        if self.music_list.count() == 0:
            return
        next_row = self.music_list.currentRow()+1 if self.music_list.currentRow() != self.music_list.count()-1 else 0
        self.music_list.setCurrentRow(next_row)
        self.is_switching = True
        self.setCurPlaying()
        self.playMusic()
        self.is_switching = False

        # 双击歌曲名称播放音乐
    def doubleClicked(self):
        self.slider.setValue(0)
        self.is_switching = True
        self.setCurPlaying()
        self.playMusic()
        self.is_switching = False

    # 根据播放模式自动播放，并刷新进度条
    def playByMode(self):
        # 刷新进度条
        if (not self.is_pause) and (not self.is_switching):
            self.slider.setMinimum(0)
            self.slider.setMaximum(self.player.duration())
            self.slider.setValue(self.slider.value() + 1000)
        self.start_label.setText(time.strftime('%M:%S', time.localtime(self.player.position()/1000)))
        self.end_label.setText(time.strftime('%M:%S', time.localtime(self.player.duration()/1000)))
        # 顺序播放
        if (self.playMode == 0) and (not self.is_pause) and (not self.is_switching):
            if self.music_list.count() == 0:
                return
            if self.player.position() == self.player.duration():
                self.nextMusic()
        # 单曲循环
        elif (self.playMode == 1) and (not self.is_pause) and (not self.is_switching):
            if self.music_list.count() == 0:
                return
            if self.player.position() == self.player.duration():
                self.is_switching = True
                self.setCurPlaying()
                self.slider.setValue(0)
                self.playMusic()
                self.is_switching = False
        # 随机播放
        elif (self.playMode == 2) and (not self.is_pause) and (not self.is_switching):
            if self.music_list.count() == 0:
                return
            if self.player.position() == self.player.duration():
                self.is_switching = True
                self.music_list.setCurrentRow(random.randint(0, self.music_list.count()-1))
                self.setCurPlaying()
                self.slider.setValue(0)
                self.playMusic()
                self.is_switching = False

    def playModeSet(self):
        self.combo_btn.setStyleSheet("QPushButton { background-color: lightblue; color: black; }")
        # 设置为单曲循环模式
        if self.playMode == 0:
            self.playMode = 1
            self.combo_btn.setText('单曲循环[可切换]')
        # 设置为随机播放模式
        elif self.playMode == 1:
            self.playMode = 2
            self.combo_btn.setText('随机播放[可切换]')
        # 设置为顺序播放模式
        elif self.playMode == 2:
            self.playMode = 0
            self.combo_btn.setText('顺序播放[可切换]')
