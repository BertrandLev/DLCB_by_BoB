# fit_result_model.py
import numpy as np
from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex

class ParameterTableModel(QAbstractTableModel):
    def __init__(self, parameters :list, errors : list, numFlory : int) -> None:
        super().__init__()
        self.numFlory = numFlory
        self.parameters = parameters
        self.errors = errors
        if self.numFlory ==1:
            self.parameters = [1.0] + self.parameters
            self.errors = [0.0] + self.errors

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return self.numFlory
    
    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 5
    
    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> np.Any:
        if not index.isValid():
            return None
        
        row = index.row()
        col = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            if col == 5:
                return np.divide(1,self.parameters[1+2*row])
            elif col%2 == 0:
                return self.parameters[col//2 + 2*row]
            else :
                return self.errors[col//2 + 2*row]
        
        return None
    
    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole) -> np.Any:
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                title = ('m_i','std m_i','Tau_i','std Tau_i','Mn')
                return title[section]
            elif orientation == Qt.Orientation.Vertical:
                return str(section + 1)

        return None

    

    
