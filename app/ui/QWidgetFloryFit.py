import pyqtgraph as pg
import numpy as np
from utils.GPC_data import GPC
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton,QLabel, 
                             QLineEdit, QSplitter, QTableView, QFileDialog, QGroupBox, QSpinBox,
                             QTextEdit)


class FloryFitTab(QWidget):
    
    
    def __init__(self) -> None:
        super().__init__()
        # Data
        self.data_GPC = GPC()

        # Main Layout
        main_layout = QHBoxLayout(self)
        main_splitter = QSplitter()
        main_splitter.setOrientation(Qt.Orientation.Horizontal)
        main_layout.addWidget(main_splitter)

        # Left Part
        left_part = QWidget(main_splitter)
        left_layout = QVBoxLayout(left_part)
        # Add file widgets
        file_box = QGroupBox("File Selection")
        file_layout = QGridLayout(file_box)
        file_label = QLabel("File Name")
        self.file_entry = QLineEdit("")
        file_button = QPushButton("...")
        file_button.clicked.connect(self.openFileDialog)
        file_infoTitle = QLabel("Sample info:")
        self.file_info = QTextEdit()
        self.file_info.setFrameShape(QLabel.Shape.Box)
        self.file_info.setReadOnly(True)
        self.file_info.setFixedHeight(100)
        file_layout.addWidget(file_label,0,0)
        file_layout.addWidget(self.file_entry,1,0)
        file_layout.addWidget(file_button,1,1)
        file_layout.addWidget(file_infoTitle,2,0)
        file_layout.addWidget(self.file_info,3,0,1,2)
        # Add fitting option widgets
        fit_box = QGroupBox("Fit Options")
        fit_layout = QGridLayout(fit_box)
        fit_label = QLabel("Number of Flory")
        self.fit_entry = QSpinBox()
        self.fit_entry.setMinimumWidth(80)
        self.fit_entry.setValue(1)
        fit_layout.addWidget(fit_label,0,0,)
        fit_layout.addWidget(self.fit_entry,0,1)
        fit_layout.setColumnStretch(0,1)
        # Add log widgets
        log_box = QGroupBox("Log")
        log_layout = QVBoxLayout(log_box)
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        log_layout.addWidget(self.log_display,0)
        self.appendLogMessage("Demarrage du logiciel...")
        # Left layout
        left_layout.addWidget(file_box,0)
        left_layout.addWidget(fit_box,1)
        left_layout.addWidget(log_box,2)
        left_layout.setStretch(1,0)
        left_layout.setStretch(2,1)

        # Right Part
        right_splitter = QSplitter(main_splitter)
        right_splitter.setOrientation(Qt.Orientation.Vertical)
        r_top_part = QWidget(right_splitter)
        r_top_layout = QVBoxLayout(r_top_part)
        self.plot_GPC = pg.PlotWidget()
        r_top_layout.addWidget(self.plot_GPC)
        r_bot_part = QWidget(right_splitter)
        r_bot_layout = QVBoxLayout(r_bot_part)
        self.result_table = QTableView()
        r_bot_layout.addWidget(self.result_table)        

        # Customize graph and set initial value
        self.plot_GPC.setBackground('w')
        self.plot_GPC.showGrid(True, True)
        self.plot_GPC.setMouseEnabled(False)
        self.plot_GPC.getPlotItem().getViewBox().setBorder(pg.mkPen(color=(0,0,0),width=1))
        # self.plot_GPC.getAxis('top').setStyle(showValues=True)
        # self.plot_GPC.getAxis('right').setStyle(showValues=True)
        self.plot_GPC.setLabel('left',
                               '<span style="color: red; font-size: 18px">w</span>')
        self.plot_GPC.setLabel('bottom',
                               '<span style="color: red; font-size: 18px">Log M</span>')
        self.x = np.array([0,0])
        self.y = np.array([0,0])
        pen = pg.mkPen(color=(255, 0, 0), width=2)
        self.GPC_curve = self.plot_GPC.plot(
            self.x, self.y,
            pen=pen,
            name='GPC Data')

    def appendLogMessage(self, message:str)-> None:
        self.log_display.append(message)

    def openFileDialog(self):
        # Open a file dialog
        filename, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)")
        # Display the selected file name
        if filename:
            self.file_entry.setText(filename)
            self.data_GPC.import_file(filename)
            self.file_info.append(self.data_GPC.__repr__())
            self.GPC_curve.setData(self.data_GPC.logM,self.data_GPC.w)

    
