from utils.Log_box import Log_box
import pyqtgraph as pg
import numpy as np
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton,QLabel, 
                             QLineEdit, QSplitter, QTableView, QFileDialog, QGroupBox, QSpinBox,
                             QComboBox, QTextEdit)

class Bob_chem_param(QGroupBox):
    
    def __init__(self, log : Log_box) -> None:
        super().__init__("Chemical Parameters")
        self.log = log
        layout = QGridLayout(self)
        layout.addWidget(QLabel("Polymer :"),0,0,Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.pol_nat_combo,0,1)
        self.M0_entry = QLineEdit()
        layout.addWidget(QLabel("Mo ="),1,0,Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.M0_entry,1,1,Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("g/mol"),1,2,Qt.AlignmentFlag.AlignLeft)
        self.Ne_entry = QLineEdit()
        layout.addWidget(QLabel("Ne ="),2,0,Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.Ne_entry,2,1,Qt.AlignmentFlag.AlignCenter)
        self.rho_entry = QLineEdit()
        layout.addWidget(QLabel("\u03c1 ="),3,0,Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.rho_entry,3,1,Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("g/cc"),3,2,Qt.AlignmentFlag.AlignLeft)
        self.tau_entry = QLineEdit()
        layout.addWidget(QLabel("\u03c4e ="),4,0,Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.tau_entry,4,1,Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("s"),4,2,Qt.AlignmentFlag.AlignLeft)
        self.temp_entry = QLineEdit()
        layout.addWidget(QLabel("T ="),5,0,Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.temp_entry,5,1,Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("°K"),5,2,Qt.AlignmentFlag.AlignLeft)

    def get_param(self) -> dict:
        parameters = {
            'Mo':float(self.M0_entry.text()),
            'Ne':int(self.Ne_entry.text()),
            'rho':float(self.rho_entry.text()),
            'tau':float(self.tau_entry.text()),
            'T':float(self.temp_entry.text())
        }
        return parameters     

class BobSimuTab(QWidget):

    def __init__(self) -> None:
        super().__init__()
        # Data

        # Main Layout
        main_layout = QHBoxLayout(self)
        main_splitter = QSplitter()
        main_splitter.setOrientation(Qt.Orientation.Horizontal)
        main_layout.addWidget(main_splitter)
        # Log box
        self.log = Log_box("Simulation Log")
        
        # Left Part
        left_part = QWidget(main_splitter)
        left_layout = QVBoxLayout(left_part)
        # Bob Simulation box
        bob_box = QGroupBox("Bob simulation imputs")
        bob_layout = QGridLayout(bob_box)
        bob_chem_param = Bob_chem_param(self.log)
        bob_reset_button = QPushButton("Reset")
        bob_reset_button.clicked.connect(self.reset_bob_param)
        bob_start_button = QPushButton("Start")
        bob_start_button.clicked.connect(self.start_bob_simu)
        bob_layout.addWidget(bob_chem_param,0,0,1,3)
        bob_layout.addWidget(bob_reset_button,1,1)
        bob_layout.addWidget(bob_start_button,1,2)
        # Left layout
        left_layout.addWidget(bob_box)
        left_layout.addWidget(self.log)
        
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

        # End of init
        self.log.appendLogMessage("Start of Bob simulation session...")

    def start_bob_simu(self) -> None:
        self.log.appendLogMessage("Simulation Start...")
        
        self.log.appendLogMessage("Simulation Finished!")

    def reset_bob_param(self) -> None:
        self.log.appendLogMessage("Parameters reset.")