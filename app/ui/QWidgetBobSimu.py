from utils.Log_box import Log_box
from utils.Plot_box import Plot_box
from models.polymer_model import mPE_model
from datetime import datetime
import pyqtgraph as pg
import numpy as np
import os
import re
import subprocess
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton,QLabel, 
                             QLineEdit, QSplitter, QTableView, QFileDialog, QGroupBox, QSpinBox,
                             QComboBox, QTextEdit, QScrollArea, QApplication)

class Bob_chem_param(QGroupBox):
    
    def __init__(self, log : Log_box) -> None:
        super().__init__("Chemical Parameters")
        self.log = log
        layout = QGridLayout(self)
        self.M0_entry = QLineEdit()
        self.M0_entry.setText("28.0")
        layout.addWidget(QLabel("Mo ="),0,0,Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.M0_entry,0,1,Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("g/mol"),0,2,Qt.AlignmentFlag.AlignLeft)
        self.Ne_entry = QLineEdit()
        self.Ne_entry.setText("40")
        layout.addWidget(QLabel("Ne ="),1,0,Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.Ne_entry,1,1,Qt.AlignmentFlag.AlignCenter)
        self.rho_entry = QLineEdit()
        self.rho_entry.setText("0.760")
        layout.addWidget(QLabel("\u03c1 ="),2,0,Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.rho_entry,2,1,Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("g/cc"),2,2,Qt.AlignmentFlag.AlignLeft)
        self.tau_entry = QLineEdit()
        self.tau_entry.setText("2.0e-7")
        layout.addWidget(QLabel("\u03c4e ="),3,0,Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.tau_entry,3,1,Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("s"),3,2,Qt.AlignmentFlag.AlignLeft)
        self.temp_entry = QLineEdit()
        self.temp_entry.setText("463.15")
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
        self.fraction.setFixedWidth(80)
        layout.addWidget(QLabel("Weight fraction :"), 0, 0)
        layout.addWidget(self.fraction, 0, 1, Qt.AlignmentFlag.AlignLeft)
        self.type = QComboBox()
        self.type.addItem("mPE")
        self.type.setFixedWidth(150)
        self.type.activated.connect(self.on_type_change)
        layout.addWidget(QLabel("Type :"), 1, 0)
        layout.addWidget(self.type, 1, 1, Qt.AlignmentFlag.AlignLeft)
        self.param_table = QTableView()
        layout.addWidget(self.param_table, 2, 0, 1, 3)
        self.poly_model = mPE_model()
        self.param_table.setModel(self.poly_model)
        layout.setColumnStretch(2,1)
        
    def on_type_change(self,index) -> None:
        self.log.appendLogMessage(f"Componant #{self.index} type change to {self.type.itemText(index)}")
        if self.type.itemText(index) == "mPE":
            self.poly_model = mPE_model()
            self.param_table.setModel(self.poly_model)

    def get_comp_param(self) -> dict:
        parameters = {
            'f':self.fraction.text(),
            'params':self.poly_model.get_params()
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
        # Left Part
        left_splitter = QSplitter(main_splitter)
        left_splitter.setOrientation(Qt.Orientation.Vertical)
        # Bob Simulation box
        bob_box = QGroupBox(title="Bob simulation imputs", parent=left_splitter)
        bob_layout = QGridLayout(bob_box)
        # Log box
        self.log = Log_box(title="Simulation Log", parent=left_splitter)
        self.bob_chem_param = Bob_chem_param(self.log)
        # Componants box
        self.comp_list = []
        bob_comp_scrollArea = QScrollArea()
        bob_comp_scrollArea.setMinimumHeight(300)
        bob_comp_scrollArea.setStyleSheet("background-color: transparent;")
        self.bob_comp_box = QGroupBox("Componants")
        self.bob_comp_layout = QGridLayout(self.bob_comp_box)
        self.bob_comp_Nb_value = QSpinBox()
        self.bob_comp_Nb_value.valueChanged.connect(self.on_comp_number_change)
        self.bob_comp_Nb_value.setFixedWidth(70)
        self.bob_comp_layout.addWidget(QLabel("Number of componants :"),0,0,Qt.AlignmentFlag.AlignTop)
        self.bob_comp_layout.addWidget(self.bob_comp_Nb_value,0,1,1,2,Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        bob_comp_scrollArea.setWidget(self.bob_comp_box)
        bob_comp_scrollArea.setWidgetResizable(True)
        # Add start and reset button
        bob_reset_button = QPushButton("Reset")
        bob_reset_button.clicked.connect(self.reset_bob_param)
        bob_start_button = QPushButton("Start")
        bob_start_button.clicked.connect(self.start_bob_simu)
        bob_layout.addWidget(self.bob_chem_param,0,0,1,3)
        bob_layout.addWidget(bob_comp_scrollArea,1,0,1,3)
        bob_layout.addWidget(bob_reset_button,2,1)
        bob_layout.addWidget(bob_start_button,2,2)
        
        # Right Part
        right_splitter = QSplitter(main_splitter)
        right_splitter.setOrientation(Qt.Orientation.Vertical)
        #top
        r_top_part = QWidget(right_splitter)
        r_top_layout = QVBoxLayout(r_top_part)
        self.plot_GPC = Plot_box()
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

    def reset_bob_param(self) -> None:
        self.log.appendLogMessage("Parameters reset.")
        self.treat_result()

    def start_bob_simu(self) -> None:
        self.log.appendLogMessage("Simulation Start...")
        try:
            self.log.appendLogMessage("Input File generation...")
            self.generate_input_file()
            QApplication.processEvents()
            self.log.appendLogMessage("Launch of bob2P5.exe...")
            self.launch_Bob()
            QApplication.processEvents()
            self.log.appendLogMessage("Treatment of the results...")
            self.treat_results_files()
            QApplication.processEvents()
            self.log.appendLogMessage("Simulation finished.")
        except Exception as e:
            self.log.appendErrorMessage("Simulation failed. Error :",e)

    def generate_input_file(self) -> bool:
        output_file = os.path.join("app/data/Bob","inputBob.dat")
        chem_param = self.bob_chem_param.get_param()
        nb_comp = self.bob_comp_Nb_value.value()
        try:
            with open(output_file, "w") as file:
                file.write("50000 500000\n")
                file.write("1.0\n")
                file.write("1\n")
                file.write(f"{chem_param['Mo']} {chem_param['Ne']} {chem_param['rho']}\n")
                file.write(f"{chem_param['tau']} {chem_param['T']}\n")
                file.write(f"{str(nb_comp)}\n")
                for i in range(0,nb_comp):
                    bob_comp_params = self.comp_list[i].get_comp_param()
                    file.write(bob_comp_params['f']+"\n")
                    file.write(bob_comp_params['params'])
            return True
        except Exception as e:
            self.log.appendErrorMessage("Fail to write inputBob.dat file. Error:",e)
            return False

    def launch_Bob(self) -> bool:
        Bob_folder = "app/data/Bob"
        Bob_inputFile = "inputBob.dat"
        try:
            Bob_exe = os.path.join(Bob_folder,"bob2P5.exe")
            command = [Bob_exe,'-i', Bob_inputFile]
            subprocess.run(command, cwd = Bob_folder)
            return True
        except Exception as e:
            self.log.appendErrorMessage("An error append while launching Bob. Error :",e)
            return False
    
    def treat_results_files(self) -> bool:
        Bob_folder = os.path.abspath("app/data/Bob")
        result_folder = os.path.abspath("app/data/Results")
        today_date = datetime.today().date().strftime("%Y%m%d")
         # Creation of output folder name
        pattern = rf"{today_date}_\d{{3}}$"
        simu_num = 1
        try:
            for item in os.listdir(result_folder):
                if os.path.isdir(os.path.join(result_folder,item)):
                    if bool(re.match(pattern, item)):
                        num_tmp = int(item[-3:])+1
                        simu_num = num_tmp if num_tmp > simu_num else simu_num
            output_folder = os.path.join(result_folder, today_date + "_" + "{:03d}".format(simu_num))
            os.makedirs(output_folder)
        except Exception as e:
            self.log.appendErrorMessage("Error while creating the result folder. Error :", e)
        # Transfering file to output folder
        files = ("gt.dat","gtp.dat","info.txt","maxwell.dat","polyconf.dat","supertube.dat")
        try:
            for file in files:
                source_file = os.path.join(Bob_folder,file)
                if os.path.exists(source_file):
                    os.rename(source_file, os.path.join(output_folder,file))
        except Exception as e:
            self.log.appendErrorMessage("Error while moving results files. Error :", e)