import pyqtgraph as pg
import numpy as np
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QWidget, QGridLayout, QVBoxLayout,QPushButton,QLabel, QLineEdit,
                             QSplitter)


class FloryFitTab(QWidget):
    def __init__(self) -> None:
        super().__init__()

        # Main Layout
        main_layout = QVBoxLayout()
        splitter = QSplitter(self)
        splitter.setOrientation(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)

        # Left Part
        left_part = QWidget(splitter)
        left_layout = QGridLayout(left_part)
        file_label = QLabel("File Name")
        file_entry = QLineEdit()
        file_button = QPushButton("...")
        file_infoTitle = QLabel("Sample info:")
        file_info = QLabel("Desciption du sample", )
        file_info.setFrameShape(QLabel.Shape.Box)
        file_info.setAlignment(Qt.AlignmentFlag.AlignTop)
        left_layout.addWidget(file_label,0,0)
        left_layout.addWidget(file_entry,1,0)
        left_layout.addWidget(file_button,1,1)
        left_layout.addWidget(file_infoTitle,2,0)
        left_layout.addWidget(file_info,3,0,1,2)
        left_layout.setRowStretch(3,1)

        # Right Part
        right_part = QWidget(splitter)
        right_layout = QVBoxLayout(right_part)
        self.plot_GPC = pg.PlotWidget()
        right_layout.addWidget(self.plot_GPC,1)

        # TEST Generate some sample data
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        self.plot_GPC.plot(x, y, pen='b', name='Sine Curve')

        # Set layouts
        # main_layout.addLayout(left_layout,0,0)
        # main_layout.addLayout(right_layout,0,1)
        self.setLayout(main_layout)

