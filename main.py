from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget,QPushButton, QVBoxLayout, QFileDialog, QGraphicsView
import sys
from PyQt5.uic.properties import QtCore
from numpy import linspace, cos, sin, pi, ceil, floor, arange
import numpy
import pandas as pd
from scipy import signal 
SignalsCounter = -1
signals_components = []

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('sample.ui', self)
        self.setWindowIcon(QtGui.QIcon("appicon.png"))
        self.setWindowTitle("Sample illust")
        self.Upload.clicked.connect(self.open)
        self.Plotdata.clicked.connect(self.plot)
        self.SamplingPoints.clicked.connect(self.plotSamples)
        self.ShowSampledGraph.clicked.connect(self.plotSeparateSamples)
        self.PlotComposer.clicked.connect(self.composer)
        self.confirm.clicked.connect(self.composerSum)
        self.horizontalSlider.setMaximum(600)
        self.horizontalSlider.valueChanged.connect(self.plotSamples)
        self.clearSample.clicked.connect(self.clear)
        self.showSample.clicked.connect(self.showw)
        self.Remove.clicked.connect(self.remove)
        self.show()

    def open(self):
        global data
        path = QFileDialog.getOpenFileName(self, 'Open a file', '', 'All Files (*.*)')
        if path != ('', ''):
            data = path[0]
            print("File path: " + data)
            
##########################################################
        data1 = pd.read_csv(data)
        t = data1['# t']
        x = data1['x']
        spec = numpy.fft.rfft(x)
        peak = numpy.argmax(spec)
        val = numpy.abs(peak) # Find magnitude
        print(val/6)
        self.horizontalSlider.setMaximum((val/6)*3*6)
 ########################################################## 
    def plot(self):
        global data
        global data1
        data1 = pd.read_csv(data)
       
   
        self.graph1.clear()
        self.graph1.plot(data1['# t'], data1['x'] , pen='b')
        self.graph1.setBackground('black')

    def plotSamples(self):
        self.graph1.clear()
        data1 = pd.read_csv(data)
        x = data1['# t']
        y = data1['x']
        #print(len(y))
        slider=self.horizontalSlider.value()
        global f
        global xnew
        f = signal.resample(y, slider)
        #print(f)
        xnew = numpy.linspace(-3, 3, slider)
        self.graph1.plot(data1['# t'], data1['x'], pen='b')
        self.graph1.plot(xnew, f, symbol='o', pen='r')

    def plotSeparateSamples(self):
        self.graph2.clear()
        self.graph2.plot(xnew, f, pen='r')
        self.graph2.setBackground('black')

    def composer(self):
        global SignalsCounter
        self.graph3.clear()
        tmin = -3;
        tmax = 3;
        global time
        time = linspace(tmin, tmax, 900);
        freq = int(self.FreqTextBox.text())
  ########################################      
       # SignalsFreq.append(freq)
      #  print(SignalsFreq)
       # self.horizontalSlider.setMaximum(3*6*5*max(SignalsFreq))
 ##########################################################       
        amp = int(self.AmpTextBox.text())
        phase = int(self.PhaseTextBox.text())
        global signals_components
        signal_part = amp * sin(2 * pi * freq * time + phase)
        signals_components.append(signal_part)
        self.ComboBox.addItem(str(SignalsCounter + 1))
        self.graph3.plot(time, signal_part, pen='orange')
        SignalsCounter = SignalsCounter + 1

    def composerSum(self):
        self.graph4.clear()
        self.graph4.plot(time, sum(signals_components), pen='green')
        SavedSignal = numpy.asarray([ time,sum(signals_components)])
        numpy.savetxt('Generated Signal'+str(SignalsCounter)+'.csv', SavedSignal.T,header="t,x", delimiter=",")
        
    def remove(self):
        global SignalsCounter
        self.ComboBox.removeItem(self.ComboBox.currentIndex())
        signals_components.pop(self.ComboBox.currentIndex())        
    def showw(self):
        self.splitter.setGeometry(0, 0, 850, 780)
    def clear(self):
        self.splitter.setGeometry(0,0,850,1560)

app = 0
app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()