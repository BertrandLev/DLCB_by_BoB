# polymer_model.py
import numpy as np
from PyQt6.QtCore import QObject, Qt, QAbstractTableModel, QModelIndex, QVariant

class Poly_model(QAbstractTableModel):

    def __init__(self, model: str = None, fraction: float = 1) -> None:
        super().__init__()
        self.model_type = model
        self.titles = ()
        self.fraction = fraction
        self.parameters = []

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 1
    
    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self.parameters)
    
    def data(self, index: QModelIndex, role: int = ...):
        return super().data(index, role)
    
    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self.titles[section]
            elif orientation == Qt.Orientation.Vertical:
                return str(f"#{section + 1}")
        return QVariant()
    
    def flags(self, index):
        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsEnabled
    
    def get_params(self) -> dict:
        return dict(zip(self.titles, self.parameters))
    
    def iterate_model(self):
        yield None

class mPE_model(Poly_model):

    def __init__(self, fraction:float=1) -> None:
        super().__init__(model="mPE", fraction=fraction)
        self.titles = ('num_gen','type','Mw','bm')
        self.parameters = [2000, 20, 20000, 0.2]
    
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
    
    def iterate_model(self):
        input_str = f"{self.fraction}\n{self.parameters[0]} {self.parameters[1]}\n{self.parameters[2]} {self.parameters[3]}"
        yield input_str
    
class mPE_bm_var_model(Poly_model):

    def __init__(self, fraction:float=1) -> None:
        super().__init__(model="mPE", fraction=fraction)
        self.titles = ('num_gen','type','Mw','bm_min','bm_max','bm_iteration')
        self.parameters = [2000, 20, 20000, 0.0, 0.2, 20]
           
    def data(self, index: QModelIndex, role: int = ...):
        if not index.isValid():
            return None
        
        col = index.column()
        if role == Qt.ItemDataRole.DisplayRole:
            if col == 3 or col == 4:
                return "{:.4f}".format(self.parameters[col])
            else:
                return "{:d}".format(self.parameters[col])
        if role == Qt.ItemDataRole.EditRole:
            if col == 3 or col == 4:
                return float(self.parameters[col])
            else:
                return self.parameters[col]
        if role == Qt.ItemDataRole.BackgroundRole:
            return Qt.GlobalColor.white
         
        return QVariant()
            
    def setData(self, index: QModelIndex, value, role: int = Qt.ItemDataRole.EditRole) -> bool:
        if role == Qt.ItemDataRole.EditRole:
            col = index.column()
            if col == 3 or col == 4:
                try:
                    self.parameters[col] = float(value)
                except ValueError:
                    return False
            else:
                self.parameters[col] = value            
            self.dataChanged.emit(index,index)
            return True
        
        return False
    
    def iterate_model(self):
        bm_values = np.linspace(start=self.parameters[3],
                                stop=self.parameters[4],
                                num=self.parameters[5])
        for bm in bm_values:
            input_str = f"{self.fraction}\n{self.parameters[0]} {self.parameters[1]}\n{self.parameters[2]} {bm}"
            yield input_str