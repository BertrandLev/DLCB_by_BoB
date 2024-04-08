import pyqtgraph as pg
import numpy as np
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton,QLabel, 
                             QLineEdit, QSplitter, QTableView, QFileDialog, QGroupBox, QSpinBox,
                             QTextEdit)

class BobSimuTab(QWidget):

    def __init__(self) -> None:
        super().__init__()
        # Data

        # Main Layout
        main_layout = QHBoxLayout(self)
        main_splitter = QSplitter()
        main_splitter.setOrientation(Qt.Orientation.Horizontal)
        main_layout.addWidget(main_splitter)

        # Left Part
        left_part = QWidget(main_splitter)
        left_layout = QVBoxLayout(left_part)
        # Bob Simulation box
        bob_box = QGroupBox("Bob simulation imputs")
        bob_layout = QGridLayout(bob_box)
        bob_start_button = QPushButton("Start")
        bob_start_button.clicked.connect(self.start_bob_simu)
        bob_layout.addWidget(bob_start_button,0,2)
        # Log box
        log_box = QGroupBox("Simulation Log")
        log_layout = QVBoxLayout(log_box)
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        log_layout.addWidget(self.log_display,0)
        self.appendLogMessage("Start of session...")
        # Left layout
        left_layout.addWidget(bob_box)
        left_layout.addWidget(log_box)
        
        # Right Part
        #top
        right_splitter = QSplitter(main_splitter)
        right_splitter.setOrientation(Qt.Orientation.Vertical)
        r_top_part = QWidget(right_splitter)
        r_top_layout = QVBoxLayout(r_top_part)
        self.plot_GPC = pg.PlotWidget()
        RDA_box = QGroupBox("RDA File")
        RDA_layout = QGridLayout(RDA_box)
        self.RDA_entry = QLineEdit("")
        self.RDA_button = QPushButton("...")
        RDA_layout.addWidget(self.RDA_entry,0,0,1,3)
        RDA_layout.addWidget(self.RDA_button,0,3,1,1)
        RDA_layout.setColumnStretch(0,1)
        r_top_layout.addWidget(RDA_box)
        r_top_layout.addWidget(self.plot_GPC)
        #bot
        r_bot_part = QWidget(right_splitter)
        r_bot_layout = QVBoxLayout(r_bot_part)


    def appendLogMessage(self, message:str) -> None:
        self.log_display.append("> "+message)

    def appendErrorMessage(self, message:str) -> None:
        errorMessage = "<font color='red'>"+"Error: "+message+"</font>"
        self.appendLogMessage(errorMessage)

    def start_bob_simu(self) -> None:
        self.appendLogMessage("Simulation Start...")
        
        self.appendLogMessage("Simulation Finished!")