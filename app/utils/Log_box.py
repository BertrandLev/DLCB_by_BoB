from PyQt6.QtWidgets import (QVBoxLayout, QGroupBox, QTextEdit)

class Log_box(QGroupBox):

    def __init__(self,title :str = None) -> None:
        super().__init__(title=title)
        layout = QVBoxLayout(self)
        self.display = QTextEdit()
        self.display.setReadOnly(True)
        layout.addWidget(self.display,0)

    def appendLogMessage(self, message:str) -> None:
        self.display.append("> "+message)

    def appendErrorMessage(self, message:str) -> None:
        errorMessage = "<font color='red'>"+"Error: "+message+"</font>"
        self.appendLogMessage(errorMessage)