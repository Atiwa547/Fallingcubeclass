try:
    from PySide2 import QtCore, QtGui, QtWidgets
    from shiboken2 import wrapInstance
except:
    from PySide6 import QtCore, QtGui, QtWidgets
    from shiboken6 import wrapInstance
import maya.OpenMayaUI as omui


IMAGE_DIR = 'D:/661310547'

class FallingCubeDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('AmaZing FallingCube')
        self.resize(480, 500)

        self.setStyleSheet("""
            QDialog {
                background-color: #E3C4BD;
                font-family: 'Segoe UI';
                font-size: 12pt;
            }
            QLabel {
                font-weight: bold;
                color: #4B1E0E;
            }
            QLineEdit {
                border: 2px solid #E36346;
                border-radius: 6px;
                padding: 6px;
                background-color: #FFF5F3;
                color: #0E1900;
            }
            QPushButton {
                background-color: #E36346;
                color: white;
                border-radius: 8px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #FF705A;
            }
            QSlider::groove:horizontal {
                border: 1px solid #bbb;
                background: #eee;
                height: 8px;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #E36346;
                border: 1px solid #5c5c5c;
                width: 18px;
                margin: -4px 0;
                border-radius: 9px;
            }
        """)

         self.imageLabel = QtWidgets.QLabel()
        self.imagePixmap = QtGui.QPixmap(f'{IMAGE_DIR}/left.png')
        scaledPixmap = self.imagePixmap.scaled(
            QtCore.QSize(64,64),
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation
        )

        self.imageLabel.setPixmap(scaledPixmap)
        self.imageLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.mainLayout.setSpacing(12)

        self.headerFrame = QtWidgets.QFrame()
        self.headerFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.headerFrame.setStyleSheet("QFrame { background-color: #E6A891; border-radius: 10px; }")

        headerLayout = QtWidgets.QVBoxLayout(self.headerFrame)
        headerLabel = QtWidgets.QLabel("✨ AMAZING FALLINGCUBE ✨")
        headerLabel.setAlignment(QtCore.Qt.AlignCenter)
        headerLabel.setStyleSheet("""
            QLabel {
                font-size: 18pt;
                font-weight: bold;
                color: #4B1E0E;
                letter-spacing: 1px;
            }
        """)
        headerLayout.addWidget(headerLabel)
        self.mainLayout.addWidget(self.headerFrame)

        self.infoLayout = QtWidgets.QGridLayout()
        self.mainLayout.addLayout(self.infoLayout)

        self.bestScoreLabel = QtWidgets.QLabel("Best Score:")
        self.bestScoreValue = QtWidgets.QLabel("0")

        self.playerLabel = QtWidgets.QLabel("Player Name:")
        self.playerInput = QtWidgets.QLineEdit()

        self.infoLayout.addWidget(self.bestScoreLabel, 0, 0)
        self.infoLayout.addWidget(self.bestScoreValue, 0, 1)
        self.infoLayout.addWidget(self.playerLabel, 1, 0)
        self.infoLayout.addWidget(self.playerInput, 1, 1)

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

        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.startButton = QtWidgets.QPushButton("START GAME")
        self.stopButton = QtWidgets.QPushButton("STOP GAME")
        self.buttonLayout.addWidget(self.startButton)
        self.buttonLayout.addWidget(self.stopButton)
        self.mainLayout.addLayout(self.buttonLayout)

        self.controlFrame = QtWidgets.QFrame()
        self.controlFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.controlFrame.setStyleSheet("QFrame { background-color: #E6A891; border-radius: 10px; }")

        controlLayout = QtWidgets.QVBoxLayout(self.controlFrame)
        controlLabel = QtWidgets.QLabel("CONTROL PLAYER")
        controlLabel.setAlignment(QtCore.Qt.AlignCenter)
        controlLabel.setStyleSheet("font-weight: bold; color: #4B1E0E;")
        controlLayout.addWidget(controlLabel)
        self.mainLayout.addWidget(self.controlFrame)

        self.mainLayout.addStretch()


def run():
    global ui
    try:
        ui.close()
    except:
        pass

    ptr = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
    ui = FallingCubeDialog(parent=ptr)
    ui.show()
