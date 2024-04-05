import pyqtgraph as pg
import numpy as np
from openpyxl import Workbook
from models.fit_results_model import ParameterTableModel
from utils.GPC_data import GPC
from utils import Flory_fit
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton,QLabel, 
                             QLineEdit, QSplitter, QTableView, QFileDialog, QGroupBox, QSpinBox,
                             QTextEdit)


class FloryFitTab(QWidget):
    
    def __init__(self) -> None:
        super().__init__()
        # Data
        self.data_GPC = GPC()
        self.param_model = ParameterTableModel()

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
        self.fit_entry.valueChanged.connect(self.floryNumberChange)
        fit_layout.addWidget(fit_label,0,0,)
        fit_layout.addWidget(self.fit_entry,0,1)
        fit_layout.setColumnStretch(0,1)
        # Add log widgets
        log_box = QGroupBox("Log")
        log_layout = QVBoxLayout(log_box)
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        log_layout.addWidget(self.log_display,0)
        self.appendLogMessage("Start of session...")
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
        r_bot_layout = QGridLayout(r_bot_part)
        self.result_display = QTextEdit()
        self.export_button = QPushButton("Export to Excel",)
        self.export_button.setFixedSize(120,40)
        self.result_table = QTableView()
        self.result_table.setModel(self.param_model)
        r_bot_layout.addWidget(self.result_table,0,0,2,2)
        r_bot_layout.addWidget(self.result_display,0,2,1,1,alignment=Qt.AlignmentFlag.AlignRight)
        r_bot_layout.addWidget(self.export_button,1,2,1,1,Qt.AlignmentFlag.AlignRight)
        
        # Customize graph and set initial value
        self.plot_GPC.setBackground('w')
        self.plot_GPC.showGrid(x=True, y=True)
        # self.plot_GPC.setMouseEnabled(False)
        self.plot_GPC.getPlotItem().getViewBox().setBorder(pg.mkPen(color=(0,0,0),width=1))
        self.plot_GPC.setLabel('left',
                               '<span style="color: red; font-size: 18px">w</span>')
        self.plot_GPC.setLabel('bottom',
                               '<span style="color: red; font-size: 18px">Log M</span>')
        self.plot_GPC.addLegend(labelTextSize='10pt', labelTextColor=(0, 0, 0),
                               pen={'color':(0, 0, 0),'width':1},
                               brush=(240, 240, 240, 150))

        # Message de démarrage
        self.appendLogMessage("Session ready. Select a GPC-ONE file to begin.")

    def appendLogMessage(self, message:str) -> None:
        self.log_display.append("> "+message)

    def appendErrorMessage(self, message:str) -> None:
        errorMessage = "<font color='red'>"+"Error: "+message+"</font>"
        self.appendLogMessage(errorMessage)

    def floryNumberChange(self, value):
        if value < 1:
            self.fit_entry.setValue(1)
            self.appendErrorMessage("Number of Flory curve should be at least one.")
        else:
            self.fitFlory()

    def openFileDialog(self) -> None:
        # Open a file dialog
        filename, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)")
        # Display the selected file name
        if filename:
            self.appendLogMessage(f"Load of file: {filename}")
            self.file_entry.setText(filename)
            # Chargement du fichier
            self.data_GPC.import_file(filename)
            # Affichage des informations de l'échantillons
            self.file_info.clear()
            self.file_info.append(self.data_GPC.__repr__())
            # Fit de la courbe expérimentale
            self.fitFlory()

    def fitFlory(self) -> None:
        logM = self.data_GPC.logM
        w = self.data_GPC.w
        N = self.fit_entry.value()
        # Effectue le fit de la courbe expérimentale
        self.appendLogMessage(f"Start of fitting with {N} Flory.")
        try:
            params, pcov = Flory_fit.fit_N_Flory(logM,w,N)
            self.appendLogMessage("End of Fitting with success.")
            self.param_model.setParameters(params, np.sqrt(np.diag(pcov)), N)
            # Affiche la courbe
            self.displayFitFlory(params)
        except Exception as e:
            self.appendErrorMessage("Fitting failure. Error : {e}")

    def displayFitFlory(self) -> None:
        # Reset l'affichage des courbes
        self.plot_GPC.clear()
        # Affichage de la courbes de GPC expérimentales
        # pen = pg.mkPen(color=(255, 0, 0))
        self.plot_GPC.scatterPlot(self.data_GPC.logM, self.data_GPC.w,
                                  symbol='o', symbolSize=4, symbolBrush='r', symbolPen=None,
                                  name='GPC Data')
        # Affichage des fits
        colors = ('g','m','c','b','y',(200,200,200),(200,200,0),(200,0,200),(200,200,0))
        w = Flory_fit.get_model_prediction(self.data_GPC.logM,
                                           self.fit_entry.value(),
                                           self.param_model.parameters)
        for i in range(0,w.shape[0]):
            pen = pg.mkPen(color=colors[i], style=Qt.PenStyle.DashLine, width=1.5)
            self.plot_GPC.plot(self.data_GPC.logM, w[i,:],pen=pen, name=f"Flory #{i+1}")
        
        if w.shape[0]>1:
            pen = pg.mkPen(color=(0, 0, 0), width=2)
            self.plot_GPC.plot(self.data_GPC.logM, np.sum(w,axis=0),pen=pen, name=f"Flory Sum")
        R2 = Flory_fit.r_squared(self.data_GPC.w, np.sum(w,axis=0))
        self.result_display.clear()
        self.result_display.append("Fit Result :")
        self.result_display.append(f"R² = {R2}")

    def Export_Excel(self) -> None:
        wb = Workbook()
        ws = wb.active




    
