try:
    from PySide2 import QtCore, QtGui, QtWidgets
    from shiboken2 import wrapInstance
except:
    from PySide6 import QtCore, QtGui, QtWidgets
    from shiboken6 import wrapInstance

import maya.OpenMayaUI as omui
import os, random

IMAGE_DIR = 'D:/661310547'
SCORE_FILE = os.path.join(IMAGE_DIR, "fallingcube_score.txt")


def getMayaMainWindow():
    ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(ptr), QtWidgets.QWidget)


class FallingCubeDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('AmaZing FallingCube')
        self.resize(480, 580)

        self.setStyleSheet("""
            QDialog { background-color: #E3C4BD; font-family: 'Segoe UI'; font-size: 12pt; }
            QLabel { font-weight: bold; color: #4B1E0E; }
            QLineEdit {
                border: 2px solid #E36346; border-radius: 6px;
                padding: 6px; background-color: #FFF5F3; color: #0E1900;
            }
            QPushButton {
                background-color: #D98F64; border-radius: 12px;
                font-size: 14px; font-family: Papyrus; font-weight: bold;
                padding: 6px; color: #fff;
            }
            QPushButton:hover { background-color: #E0A07C; }
        """)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.cube_size = 20
        self.player_x = 200
        self.player_y = 350
        self.cubes = []
        self.best_score = 0
        self.score = 0
        self.player_name = "Player1"

        if os.path.exists(SCORE_FILE):
            try:
                with open(SCORE_FILE, "r") as f:
                    self.best_score = int(f.read())
            except:
                self.best_score = 0

        self.mainLayout = QtWidgets.QVBoxLayout(self)

        headerFrame = QtWidgets.QFrame()
        headerFrame.setStyleSheet("background-color: #E6A891; border-radius: 10px;")
        headerLayout = QtWidgets.QVBoxLayout(headerFrame)
        headerLabel = QtWidgets.QLabel("✨ AMAZING FALLINGCUBE ✨")
        headerLabel.setAlignment(QtCore.Qt.AlignCenter)
        headerLabel.setStyleSheet("font-size: 18pt; font-weight: bold; color: #4B1E0E;")
        headerLayout.addWidget(headerLabel)
        self.mainLayout.addWidget(headerFrame)

        infoLayout = QtWidgets.QGridLayout()
        self.mainLayout.addLayout(infoLayout)
        self.bestScoreLabel = QtWidgets.QLabel("Best Score:")
        self.bestScoreValue = QtWidgets.QLabel(str(self.best_score))
        self.playerLabel = QtWidgets.QLabel("Player Name:")
        self.playerInput = QtWidgets.QLineEdit("Player1")
        infoLayout.addWidget(self.bestScoreLabel, 0, 0)
        infoLayout.addWidget(self.bestScoreValue, 0, 1)
        infoLayout.addWidget(self.playerLabel, 1, 0)
        infoLayout.addWidget(self.playerInput, 1, 1)

        self.spawnLayout = QtWidgets.QFormLayout()
        self.mainLayout.addLayout(self.spawnLayout)

        self.spawnSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.spawnSlider.setRange(1, 20)
        self.spawnSlider.setValue(5)
        self.spawnLabel = QtWidgets.QLabel("5")
        self.spawnSlider.valueChanged.connect(lambda v: self.spawnLabel.setText(str(v)))
        spawnHBox = QtWidgets.QHBoxLayout()
        spawnHBox.addWidget(self.spawnSlider)
        spawnHBox.addWidget(self.spawnLabel)
        self.spawnLayout.addRow("Cube Amount:", spawnHBox)

        self.speedSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.speedSlider.setRange(1, 10)
        self.speedSlider.setValue(5)
        self.speedLabel = QtWidgets.QLabel("5")
        self.speedSlider.valueChanged.connect(lambda v: self.speedLabel.setText(str(v)))
        speedHBox = QtWidgets.QHBoxLayout()
        speedHBox.addWidget(self.speedSlider)
        speedHBox.addWidget(self.speedLabel)
        self.spawnLayout.addRow("Cube Speed:", speedHBox)

        self.canvas = QtWidgets.QLabel()
        self.canvas.setFixedSize(440, 400)
        self.canvas.setStyleSheet("background-color: #333; border: 2px solid #555; border-radius: 8px;")
        self.mainLayout.addWidget(self.canvas, alignment=QtCore.Qt.AlignCenter)
        self.canvas_pixmap = QtGui.QPixmap(440, 400)
        self.canvas_pixmap.fill(QtGui.QColor("#333"))

        btnLayout = QtWidgets.QHBoxLayout()
        self.startButton = QtWidgets.QPushButton("START GAME")
        self.stopButton = QtWidgets.QPushButton("STOP GAME")
        btnLayout.addWidget(self.startButton)
        btnLayout.addWidget(self.stopButton)
        self.mainLayout.addLayout(btnLayout)

        controlFrame = QtWidgets.QFrame()
        controlFrame.setStyleSheet("background-color: #E6A891; border-radius: 10px;")
        controlLayout = QtWidgets.QVBoxLayout(controlFrame)
        controlLabel = QtWidgets.QLabel("CONTROL PLAYER")
        controlLabel.setAlignment(QtCore.Qt.AlignCenter)
        controlLabel.setStyleSheet("font-weight: bold; color: #4B1E0E;")
        controlLayout.addWidget(controlLabel)
        btnLayout2 = QtWidgets.QHBoxLayout()
        self.leftBtn = QtWidgets.QPushButton()
        self.rightBtn = QtWidgets.QPushButton()
        for btn, img_file in zip([self.leftBtn, self.rightBtn], ["left.png", "right.png"]):
            img_path = os.path.join(IMAGE_DIR, img_file)
            if os.path.exists(img_path):
                btn.setIcon(QtGui.QIcon(img_path))
                btn.setIconSize(QtCore.QSize(64, 64))
            btn.setFixedSize(72, 72)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #FADCD9; border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: #F8BFB3;
                }
            """)
        btnLayout2.addWidget(self.leftBtn)
        btnLayout2.addWidget(self.rightBtn)
        controlLayout.addLayout(btnLayout2)
        self.mainLayout.addWidget(controlFrame)

        self.mainLayout.addStretch()

        self.startButton.clicked.connect(self.startGame)
        self.stopButton.clicked.connect(self.stopGame)
        self.leftBtn.clicked.connect(lambda: self.movePlayer(-20))
        self.rightBtn.clicked.connect(lambda: self.movePlayer(20))
        self.timer.timeout.connect(self.safeUpdateGame)

        self.updateCanvas()

    def startGame(self):
        self.score = 0
        self.cubes = []
        self.player_name = self.playerInput.text()
        self.timer.start()
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(True)

    def stopGame(self):
        self.timer.stop()
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        if self.score > self.best_score:
            self.best_score = self.score
            self.bestScoreValue.setText(str(self.best_score))
            try:
                with open(SCORE_FILE, "w") as f:
                    f.write(str(self.best_score))
            except:
                pass

    def movePlayer(self, dx):
        self.player_x = max(0, min(440 - 40, self.player_x + dx))
        self.updateCanvas()

    def safeUpdateGame(self):
        try:
            self.updateGame()
        except Exception as e:
            print("Error in updateGame:", e)
            self.stopGame()

    def updateGame(self):
        if len(self.cubes) < self.spawnSlider.value():
            x = random.randint(0, 420)
            self.cubes.append([x, 0])

        speed = self.speedSlider.value()
        new_cubes = []
        for x, y in self.cubes:
            y += speed
            if y > 400:
                self.score += 1
            else:
                if (self.player_x < x + 20 and self.player_x + 40 > x and
                    self.player_y < y + 20 and self.player_y + 20 > y):
                    self.stopGame()
                    return
                new_cubes.append([x, y])
        self.cubes = new_cubes
        self.updateCanvas()

    def updateCanvas(self):
        pixmap = self.canvas_pixmap.copy()
        painter = QtGui.QPainter(pixmap)
        painter.setBrush(QtGui.QColor("#00bfff"))
        for x, y in self.cubes:
            painter.drawRect(x, y, 20, 20)
        painter.setBrush(QtGui.QColor("#ff8844"))
        painter.drawRect(self.player_x, self.player_y, 40, 20)
        painter.setPen(QtGui.QColor("#fff"))
        painter.setFont(QtGui.QFont("Segoe UI", 10, QtGui.QFont.Bold))
        painter.drawText(self.player_x, self.player_y - 5, self.player_name)
        painter.end()
        self.canvas.setPixmap(pixmap)


def run():
    global ui
    try:
        ui.close()
    except:
        pass
    ptr = getMayaMainWindow()
    ui = FallingCubeDialog(parent=ptr)
    ui.show()
    return ui
