from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon, QFont
from sys import argv
from limeinfo import LiMEInfo
from limeeditor import LiMEEditorWin
import yaml, io, os

from limeproject import LiMEProject

app = QApplication(argv)

try:
	configHandle = io.open("config.yaml")
	config = yaml.safe_load(configHandle)
	print("CONFIG: " + str(config))
	configHandle.close()
except FileNotFoundError:
	print("ERROR: config not found")
except yaml.YAMLError as e:
	print(f"ERROR: invalid config ({repr(e)})")

class LiMEInitWin(QMainWindow):
	def __init__(self):
		super().__init__()

		self.setWindowTitle(LiMEInfo.createTitle())
		self.setFixedSize(300, 200)
		self.setWindowIcon(QIcon("logo.png"))

		layout = QVBoxLayout()

		welcomeTxt = QLabel("Welcome to LiME")
		welcomeTxt.setAlignment(Qt.AlignmentFlag.AlignCenter)
		f = QFont(welcomeTxt.font())
		f.setPointSize(18)
		welcomeTxt.setFont(f)
		layout.addWidget(welcomeTxt)

		newProjBtn = QPushButton("New project")
		newProjBtn.clicked.connect(self.newProj)
		layout.addWidget(newProjBtn)

		openProjBtn = QPushButton("Open project")
		openProjBtn.clicked.connect(self.openProj)
		layout.addWidget(openProjBtn)

		centralWidget = QWidget()
		centralWidget.setLayout(layout)
		self.setCentralWidget(centralWidget)
	
	def newProj(self):
		self.projProps = LiMEInitProjPropsWin(self)
		self.projProps.show()
	
	def openProj(self):
		dirSelection = QFileDialog(self)
		dirSelection.setFileMode(QFileDialog.FileMode.Directory)
		if dirSelection.exec() == 0: return

		directory = dirSelection.selectedFiles()[0]
		projName = directory.split("/")[-1]

		if LiMEProject.formProjDir(projName) != directory + "/":
			msg = QMessageBox()
			msg.setWindowTitle(LiMEInfo.createTitle("Error"))
			msg.setText(f"Project isn't in the projects folder.")
			msg.exec()
			return

		self.editor = LiMEEditorWin.create(projName)
		if not self.editor: return
		self.editor.show()
		self.editor.setFocus()
		self.hide()

class LiMEInitProjPropsWin(QMainWindow):
	def __init__(self, parent: QWidget):
		super().__init__(parent)

		self.setWindowTitle(LiMEInfo.createTitle("Project properties"))
		self.setFixedSize(350, 150)
		self.setWindowIcon(QIcon("logo.png"))

		label1 = QLabel("Name:", self)
		label1.move(8, 6)
		label2 = QLabel("Author:", self)
		label2.move(8, 38)

		self.nameInput = QLineEdit("New Project", self)
		self.nameInput.move(64, 8)
		self.nameInput.resize(350-72, 28)

		self.authorInput = QLineEdit(os.getlogin(), self)
		self.authorInput.move(64, 40)
		self.authorInput.resize(350-72, 28)

		self.createBtn = QPushButton("Create", self)
		self.createBtn.move(350-100, 150-32)
		self.createBtn.resize(96, 28)
		self.createBtn.clicked.connect(lambda _: self.complete())
	
	def complete(self):
		self.editor = LiMEEditorWin.create(self.nameInput.text(), self.authorInput.text())
		if not self.editor: return
		self.editor.show()
		self.editor.setFocus()
		self.hide()
		self.parentWidget().hide()


win = LiMEInitWin()
win.show()
app.exec()