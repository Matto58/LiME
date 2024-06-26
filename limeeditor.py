from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
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
		self.projNameBar.editingFinished.connect(self.updateName)

		self.saveBtn = QPushButton("Save", self)
		self.saveBtn.resize(96, 28)
		self.saveBtn.move(1280-100, 4)
		self.saveBtn.clicked.connect(lambda _: self.project.save())

		self.initSuccess = True

	def updateName(self):
		self.project.fullName = self.projNameBar.text()
	
	def create(projectLocation: str | None = None, projectAuthor: str | None = None):
		editor = LiMEEditorWin(projectLocation, projectAuthor)
		if not editor.initSuccess:
			msg = QMessageBox()
			msg.setWindowTitle(LiMEInfo.createTitle("Error"))
			msg.setText("Project failed to create.")
			msg.exec()
			return
		return editor