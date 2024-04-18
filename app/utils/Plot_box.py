import pyqtgraph as pg

class Plot_box(pg.PlotWidget):

    def __init__(self, xlabel:str ="", ylabel:str = ""):
        super().__init__()
        
        # Customize graph and set initial value
        self.setBackground('w')
        self.showGrid(x=True, y=True)
        # self.plot_GPC.setMouseEnabled(False)
        self.getPlotItem().getViewBox().setBorder(pg.mkPen(color=(0,0,0),width=1))
        self.setLabel('left',f'<span style="color: red; font-size: 18px">{ylabel}</span>')
        self.setLabel('bottom',f'<span style="color: red; font-size: 18px">{xlabel}</span>')
        self.addLegend(labelTextSize='10pt', labelTextColor=(0, 0, 0),
                       pen={'color':(0, 0, 0),'width':1},
                       brush=(240, 240, 240, 150))