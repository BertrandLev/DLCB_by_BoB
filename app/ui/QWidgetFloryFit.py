import pyqtgraph as pg
import numpy as np
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QWidget, QGridLayout, QVBoxLayout)


class FloryFitTab(QWidget):
    def __init__(self) -> None:
        super().__init__()

        # Grid Layout
        main_layout = QGridLayout()

        # Left Part
        left_layout = QVBoxLayout()


        # Right Part
        right_layout = QVBoxLayout()
        self.plot_GPC = pg.PlotWidget()
        right_layout.addWidget(self.plot_GPC)

        # TEST Generate some sample data
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        self.plot_GPC.plot(x, y, pen='b', name='Sine Curve')

        # Set layouts
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        self.setLayout(main_layout)

