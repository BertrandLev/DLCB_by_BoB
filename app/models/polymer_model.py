# polymer_model.py
import numpy as np
from PyQt6.QtCore import QObject, Qt, QAbstractTableModel, QModelIndex, QVariant

class Poly_model(QAbstractTableModel):

    def __init__(self, model: str = None) -> None:
        super().__init__()
        self.model_type = model
        self.parameters = {}

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 1
    
    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 0
    
    def data(self, index: QModelIndex, role: int = ...):
        return super().data(index, role)
    
    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...):
        return super().headerData(section, orientation, role)
    
    def get_params(self) -> str:
        str_parameters = f""
        return str_parameters
    

class mPE_model(Poly_model):

    def __init__(self) -> None:
        super().__init__("mPE")
        self.title = ('num_gen','type','Mw','bm')
        self.parameters = [2000, 20, 20000, 0.2]
        
    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 4
    
    def data(self, index: QModelIndex, role: int = ...):
        if not index.isValid():
            return None
        
        col = index.column()
        if role == Qt.ItemDataRole.DisplayRole:
            if col == 3:
                return "{:.4f}".format(self.parameters[col])
            else:
                return "{:d}".format(self.parameters[col])
        if role == Qt.ItemDataRole.EditRole:
            if col == 3:
                return float(self.parameters[col])
            else:
                return self.parameters[col]
        if role == Qt.ItemDataRole.BackgroundRole:
            return Qt.GlobalColor.white
         
        return QVariant()
            
    def setData(self, index: QModelIndex, value, role: int = Qt.ItemDataRole.EditRole) -> bool:
        if role == Qt.ItemDataRole.EditRole:
            col = index.column()
            if col == 3:
                try:
                    self.parameters[col] = float(value)
                except ValueError:
                    return False
            else:
                self.parameters[col] = value            
            self.dataChanged.emit(index,index)
            return True
        
        return False
    
    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self.title[section]
            elif orientation == Qt.Orientation.Vertical:
                return str(f"#{section + 1}")
        return QVariant()
    
    def flags(self, index):
        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsEnabled
    
    def get_params(self) -> str:
        str_parameters = f"{self.parameters[0]} {self.parameters[1]}\n{self.parameters[2]} {self.parameters[3]}\n"
        return str_parameters