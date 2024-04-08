from PyQt6.QtWidgets import (QTabWidget, QMainWindow)

from ui.QWidgetFloryFit import FloryFitTab
from ui.QWidgetBobSimu import BobSimuTab

class Session(QTabWidget):
    """
    Cette classe gère les intéractions et échange de données entre les différents onglets d'une session.

    Attributes:
        
    """
    def __init__(self, parent: QMainWindow) -> None:
        super(Session,self).__init__(parent)
        self.FloryFitTab = FloryFitTab()
        self.BobSimuTab = BobSimuTab()
        self.addTab(self.FloryFitTab,"Flory Fitting")
        self.addTab(self.BobSimuTab,"Bob Simulation")


