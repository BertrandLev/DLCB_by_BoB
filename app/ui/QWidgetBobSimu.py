from utils.Log_box import Log_box
from models.polymer_model import mPE_model
import pyqtgraph as pg
import numpy as np
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton,QLabel, 
                             QLineEdit, QSplitter, QTableView, QFileDialog, QGroupBox, QSpinBox,
                             QComboBox, QTextEdit, QScrollArea, QHeaderView)

class Bob_chem_param(QGroupBox):
    
    def __init__(self, log : Log_box) -> None:
        super().__init__("Chemical Parameters")
        self.log = log
        layout = QGridLayout(self)
        self.M0_entry = QLineEdit()
        layout.addWidget(QLabel("Mo ="),0,0,Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.M0_entry,0,1,Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("g/mol"),0,2,Qt.AlignmentFlag.AlignLeft)
        self.Ne_entry = QLineEdit()
        layout.addWidget(QLabel("Ne ="),1,0,Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.Ne_entry,1,1,Qt.AlignmentFlag.AlignCenter)
        self.rho_entry = QLineEdit()
        layout.addWidget(QLabel("\u03c1 ="),2,0,Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.rho_entry,2,1,Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("g/cc"),2,2,Qt.AlignmentFlag.AlignLeft)
        self.tau_entry = QLineEdit()
        layout.addWidget(QLabel("\u03c4e ="),3,0,Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.tau_entry,3,1,Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("s"),3,2,Qt.AlignmentFlag.AlignLeft)
        self.temp_entry = QLineEdit()
        layout.addWidget(QLabel("T ="),4,0,Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.temp_entry,4,1,Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("°K"),4,2,Qt.AlignmentFlag.AlignLeft)

    def get_param(self) -> dict:
        parameters = {
            'Mo':float(self.M0_entry.text()),
            'Ne':int(self.Ne_entry.text()),
            'rho':float(self.rho_entry.text()),
            'tau':float(self.tau_entry.text()),
            'T':float(self.temp_entry.text())
        }
        return parameters     

class Bob_componant(QGroupBox):

    def __init__(self, log: Log_box, comp_index: int) -> None:
        super().__init__(title=f"Componant #{comp_index+1}")
        self.index = comp_index
        self.log = log
        layout = QGridLayout(self)
        self.fraction = QLineEdit()
        layout.addWidget(QLabel("Weight fraction :"), 0, 0)
        layout.addWidget(self.fraction, 0, 1)
        self.type = QComboBox()
        self.type.addItem("mPE")
        self.type.activated.connect(self.on_type_change)
        layout.addWidget(QLabel("Type :"), 1, 0)
        layout.addWidget(self.type, 1, 1)
        self.param_table = QTableView()
        layout.addWidget(self.param_table, 2, 0, 1, 2)
        self.poly_model = mPE_model()
        self.param_table.setModel(self.poly_model)
        
    def on_type_change(self,index) -> None:
        self.log.appendLogMessage(f"Componant #{self.index} type change to {self.type.itemText(index)}")
        if self.type.itemText(index) == "mPE":
            self.poly_model = mPE_model()
            self.param_table.setModel(self.poly_model)


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
        # Componants box
        self.comp_list = []
        bob_comp_scrollArea = QScrollArea()
        bob_comp_scrollArea.setMinimumHeight(300)
        bob_comp_scrollArea.setStyleSheet("background-color: transparent;")
        self.bob_comp_box = QGroupBox("Componants")
        self.bob_comp_layout = QGridLayout(self.bob_comp_box)
        bob_comp_Nb_value = QSpinBox()
        bob_comp_Nb_value.valueChanged.connect(self.on_comp_number_change)
        self.bob_comp_layout.addWidget(QLabel("Number of componants :"),0,0,Qt.AlignmentFlag.AlignTop)
        self.bob_comp_layout.addWidget(bob_comp_Nb_value,0,1,1,2,Qt.AlignmentFlag.AlignTop)
        bob_comp_scrollArea.setWidget(self.bob_comp_box)
        bob_comp_scrollArea.setWidgetResizable(True)
        # Add start and reset button
        bob_reset_button = QPushButton("Reset")
        bob_reset_button.clicked.connect(self.reset_bob_param)
        bob_start_button = QPushButton("Start")
        bob_start_button.clicked.connect(self.start_bob_simu)
        bob_layout.addWidget(bob_chem_param,0,0,1,3)
        bob_layout.addWidget(bob_comp_scrollArea,1,0,1,3)
        bob_layout.addWidget(bob_reset_button,2,1)
        bob_layout.addWidget(bob_start_button,2,2)
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

    def on_comp_number_change(self, value) -> None:
        self.log.appendLogMessage(f"Change of componant number to {value}")
        # Suppression des anciens composants
        if self.comp_list :
            for componant in self.comp_list:
                componant.deleteLater()
            self.comp_list.clear()
        # Ajout des composants
        for i in range(value):
            self.comp_list.append(Bob_componant(self.log, i))
            self.bob_comp_layout.addWidget(self.comp_list[i], 1+i, 0, 1, 3, Qt.AlignmentFlag.AlignTop)
            self.comp_list[i].setStyleSheet("background-color: LightGray;")

    def start_bob_simu(self) -> None:
        self.log.appendLogMessage("Simulation Start...")
        
        self.log.appendLogMessage("Simulation Finished!")

    def reset_bob_param(self) -> None:
        self.log.appendLogMessage("Parameters reset.")