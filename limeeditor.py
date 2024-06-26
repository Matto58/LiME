from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon
from limeinfo import LiMEInfo
from limeproject import LiMEProject

class LiMEEditorWin(QMainWindow):
	def __init__(self, projectLocation: str | None = None, projectAuthor: str | None = None):
		super().__init__()
		self.initSuccess = False

		self.setWindowTitle(LiMEInfo.createTitle("Editor"))
		self.setFixedSize(1280, 720)
		self.setWindowIcon(QIcon("logo.png"))

		self.project: LiMEProject = LiMEProject.create(projectLocation, projectAuthor)
		if not self.project: return
		self.project.save()
		
		self.projNameBar = QLineEdit(self.project.fullName, self)
		self.projNameBar.resize(256, 28)
		self.projNameBar.move(4, 4)
		self.projNameBar.textEdited.connect(self.updateName)

		self.saveBtn = QPushButton("Save", self)
		self.saveBtn.resize(96, 28)
		self.saveBtn.move(1280-100, 4)
		self.saveBtn.clicked.connect(lambda _: self.project.save())

		self.bpmLabel = QLabel("BPM:", self)
		self.bpmLabel.move(8, 720-32)
		self.bpmBar = QLineEdit(str(self.project.bpm), self)
		self.bpmBar.resize(96, 28)
		self.bpmBar.move(48, 720-32)

		self.initSuccess = True
		self.savedSinceLastChange = True
	
	def closeEvent(self, event):
		if not self.close(): event.ignore()

	def updateName(self):
		self.project.fullName = self.projNameBar.text()
		self.savedSinceLastChange = False
	def updateBpm(self):
		if not self.bpmBar.text().isdecimal():
			msg = QMessageBox()
			msg.setWindowTitle(LiMEInfo.createTitle("Error"))
			msg.setText(f"The specified BPM ({self.bpmBar.text()}) is not a valid number.")
			msg.exec()
			return
		self.project.bpm = float(self.projNameBar.text())
		self.savedSinceLastChange = False
	
	def create(projectLocation: str | None = None, projectAuthor: str | None = None):
		editor = LiMEEditorWin(projectLocation, projectAuthor)
		if not editor.initSuccess:
			msg = QMessageBox()
			msg.setWindowTitle(LiMEInfo.createTitle("Error"))
			msg.setText("Project failed to load.")
			msg.exec()
			return
		return editor
	
	def save(self):
		self.savedSinceLastChange = True
		self.project.save()
	def close(self):
		if self.savedSinceLastChange: return True
		msg = QMessageBox(self)
		msg.setWindowTitle(LiMEInfo.createTitle())
		msg.setText("You have unsaved changes. Are you sure you want to exit?")
		msg.setStandardButtons(QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel)
		msg.setDefaultButton(QMessageBox.StandardButton.Save)
		option = msg.exec()
		if option == QMessageBox.StandardButton.Save:
			self.save()
			return True
		if option == QMessageBox.StandardButton.Discard:
			return True
		return False
