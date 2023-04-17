import sys
import os
import numpy as np
from PyQt5.QtWidgets import (QWidget, QTextEdit, QVBoxLayout, QSizePolicy, QGroupBox, QGridLayout, QHBoxLayout, QCheckBox, QToolTip, QMessageBox, QApplication, QPushButton, QRadioButton, QLabel)
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot
#from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavBar
from matplotlib.figure import Figure
from scipy.special import j1

        
class ApplicationWindow(QWidget):
    
    def __init__(self): #constructor, used to initialize the data
        super().__init__()
        self.title = 'Fourier Series Simulation'#window title
        self.left = 300
        self.top = 200
        self.width = 800
        self.height= 800
        self.setWindowIcon(QIcon('web.png')) #window icon on corner of window
        
        self.initUI()
         
    def initUI(self):               
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)#sets position and size of window
        
        self.createGridLayout()#creates layout to place widgets in window
        
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)
        self.show()
        
    def createGridLayout(self):
        #widgets
        """Contains all widgets and sets the layout for the main window."""
        
        #The first parameter of the constructor is the label of the button. The second parameter is the parent widget.
        l1=QLabel("Function shape:",self)#creates label (short piece of text)
        l1.text()#makes the label display the text written in the parentheses before
        font1=QFont()#creates a type of font
        font1.setBold(True)#makes this font bold
        l1.setFont(font1)#sets bold font to the text in the label
        #radio buttons
        self.sqfuncBtn= QRadioButton('Square',self)
        self.sqfuncBtn.resize(self.sqfuncBtn.sizeHint())#resizes the button to an appropriate size according to rest of layout
        self.sqfuncBtn.setChecked(True) #makes the checkbox initially appear checked
        self.sqfuncBtn.toggled.connect(self.radiobtnState)#connects the state of the button to a function within the same class, so an action can be set off from the button being on or off
        self.sqfuncBtn.toggled.connect(self.radiobtnStateL)
        
        self.tfuncBtn= QRadioButton('Triangle',self)
        self.tfuncBtn.resize(self.tfuncBtn.sizeHint())
        self.tfuncBtn.toggled.connect(self.radiobtnState)
        self.tfuncBtn.toggled.connect(self.radiobtnStateL)
        
        self.scfuncBtn= QRadioButton('Semi-circle',self)
        self.scfuncBtn.resize(self.scfuncBtn.sizeHint())
        self.scfuncBtn.toggled.connect(self.radiobtnState)
        self.scfuncBtn.toggled.connect(self.radiobtnStateL)
        #push buttons
        plotBtn = QPushButton('Plot', self)
        plotBtn.setToolTip('Plot the Fourier Series approximation for the order(s) selected')
        plotBtn.resize(plotBtn.sizeHint())
        plotBtn.clicked.connect(self.plot_click)
        #signal and slot system mechanism, if click on botton, the signal clicked is emitted.
        #the sender is the push button, the receiver is the application object.
        
        l2=QLabel("Order of expansion:",self)
        l2.text()
        l2.setFont(font1)
        
        infoBtn = QPushButton('Explanation', self)
        infoBtn.setToolTip('Why does the plot look like this?')
        infoBtn.clicked.connect(self.info_click)
        
        repBtn = QPushButton('Report', self)
        repBtn.setToolTip('Open Report')
        repBtn.resize(repBtn.sizeHint())
        repBtn.clicked.connect(self.rep_click)
        #checkboxes
        self.ord1Btn = QCheckBox('1', self)
        self.ord1Btn.resize(self.ord1Btn.sizeHint())
        self.ord1Btn.setChecked(True) 
        self.ord1Btn.stateChanged.connect(self.checkboxState)#similar as with radio buttons
        
        self.ord5Btn = QCheckBox('5', self)
        self.ord5Btn.resize(self.ord5Btn.sizeHint()) 
        self.ord5Btn.stateChanged.connect(self.checkboxState)
        
        self.ord10Btn = QCheckBox('10', self)
        self.ord10Btn.resize(self.ord10Btn.sizeHint()) 
        self.ord10Btn.stateChanged.connect(self.checkboxState)
        
        self.ord100Btn = QCheckBox('100', self)
        self.ord100Btn.resize(self.ord100Btn.sizeHint()) 
        self.ord100Btn.stateChanged.connect(self.checkboxState)
        
        self.ord500Btn = QCheckBox('500', self)
        self.ord500Btn.resize(self.ord500Btn.sizeHint())
        self.ord500Btn.stateChanged.connect(self.checkboxState)
        
        l3=QLabel("Instructions:",self)
        l3.text()
        l3.setFont(font1)
        textBox1=QTextEdit()
        textBox1.setText("Select a function to plot as a finite Fourier Series approximation. A general equation of the function and its Fourier Series approximation will be displayed where L is the half period of the function (taken to be pi).\nSelect the order 'n' of expansion for the curve(s) to be plotted.\nPress 'Plot' to plot the curve(s).\nUse the toolbar below the figure to zoom in, edit the axes and save an image of the figure.\nPress 'Explanation' to read about the physical explanation of the plot.\nPress 'Report' to open the report.")
        textBox1.setReadOnly(True) #so text edit cannot be edited and it is just displayed
        
        #images
        l4=QLabel("Equations:",self)
        l4.text()
        l4.setFont(font1)
        self.l1Img=QLabel()
        img1=QPixmap('sqEq.gif')
        self.l1Img.setPixmap(img1)
        self.l2Img=QLabel()
        img2=QPixmap('sqFourierEq.gif')
        self.l2Img.setPixmap(img2)
        self.l3Img=QLabel()
        img3=QPixmap('tEq.gif')
        self.l3Img.setPixmap(img3)
        self.l4Img=QLabel()
        img4=QPixmap('tFourierEq.gif')
        self.l4Img.setPixmap(img4)
        self.l5Img=QLabel()
        img5=QPixmap('scEq.gif')
        self.l5Img.setPixmap(img5)
        self.l6Img=QLabel()
        img6=QPixmap('scFourierEq.gif')
        self.l6Img.setPixmap(img6)
        
        #create variable to be able to plot the figure (from another class) within this class
        self.plotspace=WidgetPlot(self.radiobtnState(),self.checkboxState())
        #self.radiobtnState() calls the function, which will return our 'y' values
        #self.checkboxState() calls the function, which will return our 'n' values
        #need self.(function_name) to be able to access the function from another function
        
        #layout structure
        self.horizontalGroupBox = QGroupBox()
        self.layout = QGridLayout()
        self.layout.setHorizontalSpacing(20) #So columns are not touching
        
        #create one layout box so all buttons are placed together
        self.horizontalGroupBox1 = QGroupBox()
        self.layout1 = QGridLayout()
        
        self.layout1.addWidget(l1,0,0)  #row and column number within this layout box
        self.layout1.addWidget(self.sqfuncBtn,1,0)
        self.layout1.addWidget(self.tfuncBtn,2,0)
        self.layout1.addWidget(self.scfuncBtn,3,0)
        self.layout1.addWidget(plotBtn,4,0)
        self.layout1.addWidget(infoBtn,5,0)
        self.layout1.addWidget(repBtn,6,0)
        self.layout1.addWidget(l2,7,0)
        self.layout1.addWidget(self.ord1Btn,8,0)
        self.layout1.addWidget(self.ord5Btn,9,0)
        self.layout1.addWidget(self.ord10Btn,10,0)
        self.layout1.addWidget(self.ord100Btn,11,0)
        self.layout1.addWidget(self.ord500Btn,12,0)
        self.horizontalGroupBox1.setLayout(self.layout1)
        
        self.horizontalGroupBox2 = QGroupBox()
        self.layout2 = QGridLayout()

        self.layout2.addWidget(l3,0,0) #row and column number, and row and column span in this layout
        self.layout2.addWidget(textBox1,1,0,1,5)
        self.layout2.addWidget(l4,3,0)
        self.layout2.addWidget(self.l1Img,5,0,2,5) #places all possible images of equations on same place
        self.layout2.addWidget(self.l2Img,7,0,2,5)
        self.layout2.addWidget(self.l3Img,5,0,2,5)
        self.layout2.addWidget(self.l4Img,7,0,2,5)
        self.layout2.addWidget(self.l5Img,5,0,2,5)
        self.layout2.addWidget(self.l6Img,7,0,2,5)
        self.l3Img.hide() #hides all images except the ones that are meant to be checked at the start
        self.l4Img.hide()
        self.l5Img.hide()
        self.l6Img.hide()
        
        self.layout2.addWidget(self.plotspace,9,0,4,5)
        self.horizontalGroupBox2.setLayout(self.layout2)
        
        self.layout.addWidget(self.horizontalGroupBox1,0,0) #adds both layout boxes to the main layout
        self.layout.addWidget(self.horizontalGroupBox2,0,1,12,5)
        
        self.horizontalGroupBox.setLayout(self.layout)
    
    def checkboxState(self): #creates a list of n values (for the order of expansion) to plot multiple curves depending on if the corresponding checkboxes are ticked or not
        """Returns a list of order of expansion 'n' values depending on the checkboxes that are checked."""
        n1=[]
        if self.ord1Btn.isChecked() == True:
            n1.append(1)
        if self.ord5Btn.isChecked() == True:
            n1.append(5)
        if self.ord10Btn.isChecked() == True:
            n1.append(10)
        if self.ord100Btn.isChecked() == True:
            n1.append(100)
        if self.ord500Btn.isChecked() == True:
            n1.append(500)
        return n1 
            
    def radiobtnState(self): #creates a list of y values to plot multiple curves depending on if the radio buttons are on or off
        """Returns a list of 'y' values corresponding to the list of 'n' values which depends on the radiobutton that is checked."""
        y1=[]
        if self.sqfuncBtn.isChecked() == True:
            for i in range(0,len(self.checkboxState())): #for loop that goes through every element in the n1 list returned from the checkboxState function
                y1.append(self.fouriersqfunc(self.checkboxState()[i])) #takes each element of the n1 element as the n variable for the fouriersqfunc function
        if self.tfuncBtn.isChecked() == True:
            for i in range(0,len(self.checkboxState())):
                y1.append(self.fouriertfunc(self.checkboxState()[i])) #uses the function corresponding to the radio button that's on to return the y curve
        if self.scfuncBtn.isChecked() == True:
            for i in range(0,len(self.checkboxState())):
                y1.append(self.fourierscfunc(self.checkboxState()[i]))
        return y1
    
    def radiobtnStateL(self): #adds corresponding equation image for each radio button function to layout
        """Toggles the equations shown on the layout depending on the radio button that is checked."""
        self.l1Img.hide() #hides all images again for each time this function is run(in case some of the images have been shown)
        self.l2Img.hide()
        self.l3Img.hide()
        self.l4Img.hide()
        self.l5Img.hide()
        self.l6Img.hide()
        if self.sqfuncBtn.isChecked() == True:
            self.l1Img.show() #shows corresponding images for equations
            self.l2Img.show()
        if self.tfuncBtn.isChecked() == True:
            self.l3Img.show()
            self.l4Img.show()
        if self.scfuncBtn.isChecked() == True:
            self.l5Img.show()
            self.l6Img.show()
            
    def plot_click(self):#replots the curve(s) selected on the checkboxes and radio button onto the plotcanvas when the 'plot' button is clicked
        """Plots the function with the new selected parameters on the plot canvas."""
        self.plotspace.plot(self.radiobtnState(),self.checkboxState()) #uses WidgetPlot.plot(y,n), which therefore calls PlotCanvas.plot(y,n)
        
    def info_click(self):#displays message box on new window when 'Explanation' is clicked
        "Displays 'Explanation' message box in a new window."
        QMessageBox.about(self,'Explanation', 'As the order of the expansion increases, the approximation for the function generally becomes more accurate as more terms are added to the Fourier series expansion.\n\nThe overshoot seen at both sides of a step in functions such as the square wave is called the "Gibbs phenomenon". It appears when trying to approximate a function which has simple discontinuities, such as a jump, with a Fourier series containing a finite number of terms. ')
        
    def rep_click(self):#opens report file in new window when 'Report' button is clicked
        """Opens the report."""
        os.startfile("ProjectReport.pdf")
        
    def fouriersqfunc(self,N):
        '''
        Sums the values of a Fourier series up to the nth term for a square wave.
        x is defined in range 0 to 2 pi and N is an integer representing the number of terms wanted.
        '''
        x=np.linspace(0, 2 * np.pi, 1000)
        L=np.pi #defining half the period of the function we are appoximating (period is 2L)
        fouriersum=0 #defining the variable so more things can be added to it further on
        a0half=0 
        for n in range(1, N+1,2): #n is a variable which we are using in the loop and it ranges from 1 to N+1 (stopping the loop before using the N+1 value). n will go up in steps of 2 each time it is used.
            #Steps of 2 are used this time because bn will only give non-zero values for odd n values.
            an=0 #a0 and an are 0 in this case but are included so the same code can be used to approximate functions for which these values are non-zero
            bn= 4 / (np.pi * n) 
            fouriersum += (an * np.cos((n*np.pi*x)/L) ) +( bn * np.sin((n*np.pi*x)/L)) #each time the loop runs it will add one of these terms to the original fouriersum variable. The n is the variable previosuly defined which changes its value with each run of the loop.
        fourier=a0half + fouriersum #this line of code is included to make the user-defined function more general so it can be used for expansions of other functions 
        return fourier    
        
    def fouriertfunc(self,N):
        '''
        Sums the values of a Fourier series up to the nth term for a triangle wave.
        x is defined in range 0 to 2 pi and N is an integer representing the number of terms wanted.
        '''
        x=np.linspace(0, 2 * np.pi, 1000)
        L=np.pi
        fouriersum=0 
        a0half=0
        for n in range(1, N+1,2): 
            #Steps of 2 are used this time because bn will only give non-zero values for odd n values.
            an=0 
            bn= (8 * (-1)**((n-1)/2)) / ((np.pi)**2 * n**2) 
            fouriersum += (an * np.cos((n*np.pi*x)/L) ) +( bn * np.sin((n*np.pi*x)/L)) 
        fourier=a0half + fouriersum 
        return fourier

    def fourierscfunc(self,N):
        '''
        Sums the values of a Fourier series up to the nth term for a semi-circle wave.
        x is defined in range 0 to 2 pi and N is an integer representing the number of terms wanted.
        '''
        x=np.linspace(0, 2 * np.pi, 1000)
        L=np.pi
        fouriersum=0 
        a0half=(np.pi*L)/4
        for n in range(1, N+1): 
            an= (((-1)**n) *L * (j1(n * np.pi)))/n
            bn=0
            fouriersum += (an * np.cos((n*np.pi*x)/L) ) +( bn * np.sin((n*np.pi*x)/L)) 
        fourier=a0half + fouriersum  
        return fourier
        
    def closeEvent(self, event):
        """Displays a question when the user tries to close the window to ask for confirmation on closing the window."""
        
        reply = QMessageBox.question(self, 'Message', #creates a message box with a question that the user needs to answer, first string appears in titlebar, second string is message displayed by the dialog
            "Are you sure you want to quit?", QMessageBox.Yes |   #give message in the box and what combination of buttons appear in the dialog, and what the default button is
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes: #if user says yes, the widget will close
            event.accept()
            exit()
        else: #otherwise widget won't close
            event.ignore()  

class WidgetPlot(QWidget): #widget containing plotcanvas and toolbar in same place
    """Creates a widget to place the plot and the toolbar."""
    def __init__(self,y:list,n:list, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.setLayout(QVBoxLayout())
        self.canvas = PlotCanvas(y,n)
        self.toolbar = NavBar(self.canvas, self)
        self.layout().addWidget(self.canvas)
        self.layout().addWidget(self.toolbar) #toolbar goes after so is placed below canvas
    def plot(self,y:list,n:list): #this function will run PlotCanvas.plot(y,n) when called from the WidgetPlot class (as this one is the one defined in the layout above)
        self.canvas.plot(y,n)

class PlotCanvas(FigureCanvas):
    """Plots the function with the y and n parameters specified, where y and n are lists."""
    def __init__(self,y:list,n:list, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111) #creates subplot

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self) #allows figure to change size with window
        self.plot(y,n) #plots the curve
    def plot(self,y:list,n:list): #sets variables of function (have to be lists)
        ax = self.figure.add_subplot(111)
        ax.clear() #clears plot on the plot canvas before plotting the new curve(s)
        x=np.linspace(0, 2 * np.pi, 1000)
        for i in range(0,len(n)): #for loop covering all elements in the n list so multiple curves can be plotted corresponding to each value
            ax.plot(x, y[i], label="n={}".format(n[i])) #plots different curves with each element of the y list (which has same length as the n list because they are linked)
        ax.set_title('Plot of Fourier Series Expansion')
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.legend() #creates a legend for each curve with different orders 'n'
        self.draw() #draws the curve(s) on the canvas
        
        
if __name__ == "__main__":
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv) #creates an application object
    myGUI = ApplicationWindow() #uses class where the main application window is
    myGUI.show()
    sys.exit(app.exec_())