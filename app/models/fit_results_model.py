# fit_result_model.py
import numpy as np
from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex

class ParameterTableModel(QAbstractTableModel):
    def __init__(self) -> None:
        super().__init__()
        self.nb_Flory = 0
        self.parameters = []
        self.errors = []

    def setParameters(self, parameters :list, errors : list, nb_Flory : int) -> None:
        self.nb_Flory = nb_Flory
        self.parameters = parameters
        self.errors = errors
        if self.nb_Flory == 1:
            self.parameters = np.append(1.0, self.parameters)
            self.errors = np.append(0.0, self.errors)
        else:
            m_N = 1 - np.sum([self.parameters[0:self.nb_Flory]])
            std_m_N = np.sum([self.errors[0:self.nb_Flory]])
            self.parameters = np.insert(self.parameters, self.nb_Flory-1, m_N)
            self.errors = np.insert(self.errors, self.nb_Flory-1, std_m_N)
        
        self.layoutChanged.emit()

    def resetData(self):
        self.nb_Flory = 0
        self.parameters.clear()
        self.errors.clear()
        self.layoutChanged.emit()

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return self.nb_Flory
    
    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 5
    
    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        
        row = index.row()
        col = index.column()
        if role == Qt.ItemDataRole.DisplayRole:
            if col == 0:
                return "{:.4f}".format(self.parameters[row])
            elif col == 1:
                return "{:.4e}".format(self.errors[row])
            elif col == 2:
                return "{:.4e}".format(self.parameters[self.nb_Flory + row])
            elif col == 3:
                return "{:.4e}".format(self.errors[self.nb_Flory + row])
            else:
                return str(int(np.divide(1,self.parameters[self.nb_Flory + row])))
        
        if role == Qt.ItemDataRole.TextAlignmentRole:
            return int(Qt.AlignmentFlag.AlignCenter)

        return None
    
    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                title = ('m_i','std m_i','Tau_i','std Tau_i','Mn')
                return title[section]
            elif orientation == Qt.Orientation.Vertical:
                return str(f"#{section + 1}")
        return None

    

    
