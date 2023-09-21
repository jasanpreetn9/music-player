import os
import sys
import random
import pygame
import datetime
import asyncio
from multiprocessing import Process
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

# inheritance
# the relationship between BringOnWidget and QMainWindow is BringWidgets is a QMainWindow


class BringOnWidgets(QMainWindow):
    def __init__(self):
        # QMainWindow.__init__(self)
        super().__init__()
        pygame.mixer.init()  # Initialize the mixer to be used in the program
        pygame.init()

        self.playlist = []
        self.currentSongIndex = 0
        self.currentSongTitle = ''
        self.shuffleBol = False
        self.shufflePlaylist = []
        self.playing = True
        self.stopped = False
        self.updateBarProcess = ""
        buttonStyle = """
                             font-size: 13px;
                             background-color: white;
                             color: black;
                             padding: 2px;
                             border-radius: 3px;
                             """
        for path in os.listdir("assets/songs"):
            path = path.replace('.mp3', '')
            self.playlist.append(path)

        for song in self.playlist:
            if song[0] == ".":
                self.playlist.remove(song)

        self.setFixedSize(800, 600)
        self.setWindowTitle('Phantom')
        self.setStyleSheet("background-color: #0D111A;")

        self.album = QLabel(self)
        self.album.setGeometry(175, 50, 500, 250)
        self.pixmap = QPixmap(f'assets/albumCovers/{self.playlist[self.currentSongIndex]}.jpeg')
        self.pixmap = self.pixmap.scaled(self.album.size(), Qt.AspectRatioMode.KeepAspectRatio)
        self.album.setPixmap(self.pixmap)

        pygame.mixer.music.load(f'assets/songs/{self.playlist[self.currentSongIndex]}.mp3')
        pygame.mixer.music.play(fade_ms=1000)
        pygame.mixer.music.queue(f'assets/songs/{self.playlist[self.currentSongIndex + 1]}.mp3')
        
        
        self.name = QLabel(
            self.playlist[self.currentSongIndex].replace('-', ' '), self)
        self.name.setGeometry(175, 300, 445, 50)

        self.timeRemainingTxt = QLabel('0', self)
        self.timeRemainingTxt.setGeometry(575, 300, 445, 50)

        progressBarBackground = QFrame(self)
        progressBarBackground.setGeometry(175, 350, 445, 10)
        progressBarBackground.setStyleSheet("""
                                  background-color: grey;
                                  border-radius: 3px;
                                  """)

        self.progressBar = QFrame(self)
        self.progressBar.setGeometry(175, 350, 0, 10)
        self.progressBar.setStyleSheet("""
                                  background-color: red;
                                  border-radius: 3px;
                                  """)
        buttons = QFrame(self)
        buttons.setGeometry(175, 370, 445, 180)
        buttons.setStyleSheet("""
                             background-color: transparent;
                             """)

        previous = QPushButton('', buttons)
        previous.setGeometry(0, 0, 100, 30)
        previous.setIcon(QIcon('assets/icons/previous.svg'))
        previous.clicked.connect(lambda: self.nextPreviousSong('previous'))
        previous.setStyleSheet(buttonStyle)

        self.playPauseBtn = QPushButton('', buttons)
        self.playPauseBtn.setGeometry(172, 0, 100, 30)
        self.playPauseBtn.setIcon(QIcon('assets/icons/pause.svg'))
        self.playPauseBtn.clicked.connect(lambda: self.playPauseSong())
        self.playPauseBtn.setStyleSheet(buttonStyle)

        next = QPushButton('', buttons)
        next.setGeometry(345, 0, 100, 30)
        next.setIcon(QIcon('assets/icons/next.svg'))
        next.clicked.connect(lambda: self.nextPreviousSong('next'))
        next.setStyleSheet(buttonStyle)

        rewind = QPushButton('', buttons)
        rewind.setGeometry(0, 40, 100, 30)
        rewind.setIcon(QIcon('assets/icons/rewind.svg'))
        rewind.clicked.connect(lambda: self.rewindForward('rewind'))
        rewind.setStyleSheet(buttonStyle)

        shuffleBtn = QPushButton('', buttons)
        shuffleBtn.setGeometry(172, 40, 100, 30)
        shuffleBtn.setIcon(QIcon('assets/icons/shuffle.svg'))
        shuffleBtn.clicked.connect(lambda: self.shuffle())
        shuffleBtn.setStyleSheet(buttonStyle)

        forward = QPushButton('', buttons)
        forward.setGeometry(345, 40, 100, 30)
        forward.setIcon(QIcon('assets/icons/forward.svg'))
        forward.clicked.connect(lambda: self.rewindForward('forward'))
        forward.setStyleSheet(buttonStyle)

        stopBtn = QPushButton('', buttons)
        stopBtn.setGeometry(172, 80, 100, 30)
        stopBtn.setIcon(QIcon('assets/icons/stop.svg'))
        stopBtn.clicked.connect(lambda: self.stopSong())
        stopBtn.setStyleSheet(buttonStyle)

        pygame.time.set_timer(pygame.USEREVENT + 1, 1000)
        self.show()
        Process(target=self.update_progress_bar())
        # asyncio.run(self.update_progress_bar())
        # timer = QTimer()
        # timer.timeout.connect(self.update_progress_bar())
        # timer.start(1000)


    def playPauseSong(self):
        if self.playing == True:
            self.playing = False
            pygame.mixer.music.pause()
            self.playPauseBtn.setIcon(QIcon('assets/icons/play.svg'))
        elif self.playing == False:
            self.playing = True
            self.playPauseBtn.setIcon(QIcon('assets/icons/pause.svg'))
            pygame.mixer.music.unpause()

    def nextPreviousSong(self, buttonInput):
        playlist = self.playlist
        nextPrevious = False
        if self.shuffleBol:
            playlist = self.shufflePlaylist
        if buttonInput == 'previous' and self.currentSongIndex != 0:
            self.currentSongIndex -= 1
            nextPrevious = True
        elif buttonInput == 'next' and self.currentSongIndex < len(self.playlist) - 1:
            self.currentSongIndex += 1
            nextPrevious = True
        if nextPrevious:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            pygame.mixer.music.load(
                f'assets/songs/{playlist[self.currentSongIndex]}.mp3')
            pygame.mixer.music.play()
            self.pixmap = QPixmap(
                f'assets/albumCovers/{playlist[self.currentSongIndex]}.jpeg')
            self.pixmap = self.pixmap.scaled(
                self.album.size(), Qt.AspectRatioMode.KeepAspectRatio)
            self.album.setPixmap(self.pixmap)
            self.currentSongName = playlist[self.currentSongIndex].replace(
                '-', ' ').replace('.mp3', '')
            self.name.setText(self.currentSongName)
            self.playing = True
            self.playPauseBtn.setIcon(QIcon('assets/icons/pause.svg'))
            pygame.mixer.music.queue(f'assets/songs/{self.playlist[self.currentSongIndex + 1]}.mp3')


    def rewindForward(self, direction):
        current_time = pygame.mixer.music.get_pos() // 1000
        print(current_time)
        if direction == 'rewind':
            print(f'Rewind Function: {current_time} : {current_time - 10}')
            pygame.mixer.music.play(start=current_time - 10)
        elif direction == 'forward':
            print(f'Forward Function: {current_time} : {current_time + 10}')
            pygame.mixer.music.play(start=current_time + 10)

    def shuffle(self):
        self.shuffleBol = not self.shuffleBol
        self.shufflePlaylist = self.playlist
        random.shuffle(self.shufflePlaylist)

    def stopSong(self):
        self.playing = False
        self.stopped = True
        self.playPauseBtn.setIcon(QIcon('assets/icons/play.svg'))
        pygame.mixer.music.stop()
        self.progressBar.setGeometry(175, 350, 0, 10)
        self.timeRemainingTxt.setText('0:00')
        pygame.mixer.music.play()
        pygame.mixer.music.pause()
        # pygame.time.set_timer(pygame.USEREVENT + 1, 1000)

    def update_progress_bar(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT + 1:
                    current_song_duration = pygame.mixer.Sound.get_length(
                        pygame.mixer.Sound(f'assets/songs/{self.playlist[self.currentSongIndex]}.mp3'))
                    time_elapsed = pygame.mixer.music.get_pos() / 1000
                    time_remaining = current_song_duration - time_elapsed
                    print(f'Progress Bar update function: {int(time_remaining)}')
                    self.timeRemainingTxt.setText(str(datetime.timedelta(seconds=int(time_remaining))))
                    progress = int((time_elapsed / current_song_duration) * 100)
                    self.progressBar.setGeometry(175, 350, 0, 10)
                    self.progressBar.setGeometry(175, 350, int(progress * 4.45), 10)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BringOnWidgets()
    window.show()
    sys.exit(app.exec())
