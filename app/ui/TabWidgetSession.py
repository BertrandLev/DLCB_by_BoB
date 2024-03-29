from PyQt6.QtWidgets import (QTabWidget, QMainWindow)

class Session(QTabWidget):
    """
    Cette classe gère les intéractions et échange de données entre les différents onglets d'une session.

    Attributes:
        
    """
    def __init__(self, parent: QMainWindow) -> None:
        super(Session,self).__init__(parent)
