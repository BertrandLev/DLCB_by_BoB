import pyqtgraph as pg
import numpy as np
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton,QLabel, 
                             QLineEdit, QSplitter, QTableView)


class FloryFitTab(QWidget):
    def __init__(self) -> None:
        super().__init__()

        # Main Layout
        main_layout = QHBoxLayout()
        main_splitter = QSplitter(self)
        main_splitter.setOrientation(Qt.Orientation.Horizontal)
        main_layout.addWidget(main_splitter)

        # Left Part
        left_part = QWidget(main_splitter)
        left_layout = QGridLayout(left_part)
        file_label = QLabel("File Name")
        file_entry = QLineEdit()
        file_button = QPushButton("...")
        file_infoTitle = QLabel("Sample info:")
        file_info = QLabel("Description du sample")
        file_info.setFrameShape(QLabel.Shape.Box)
        file_info.setAlignment(Qt.AlignmentFlag.AlignTop)
        left_layout.addWidget(file_label,0,0)
        left_layout.addWidget(file_entry,1,0)
        left_layout.addWidget(file_button,1,1)
        left_layout.addWidget(file_infoTitle,2,0)
        left_layout.addWidget(file_info,3,0,1,2)
        left_layout.setRowStretch(3,1)

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

        # TEST Generate some sample data
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        self.plot_GPC.plot(x, y, pen='b', name='Sine Curve')

        # Set layouts
        self.setLayout(main_layout)

