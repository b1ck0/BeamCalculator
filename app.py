import matplotlib.pyplot as plt
import matplotlib.patches as patches

import numpy as np

from Tkinter import * # builds graphical user interface

class rectLoad:
    def __init__(self,x1,x2,w):
        self.q = w/(x2 - x1) #calculating the load intensity
        
class triLoad:
    def __init__(self,x1,x2,w):
        self.q = []
        l = x2 - x1
        step = (l)/100.0
        for i in np.arange(x1,x2,step):
            x = x2-i
            xL = x/(l)            
            self.q.append( np.round(2*w/(l)*xL,3) )
            
class beam:
    def calculatey(self):
        self.A1 = self.Height * self.Thickness #web
        self.A2 = self.AddedFlangeWidth1 * self.AddedFlangeThickness1 #top flange
        self.A3 = self.AddedFlangeWidth2 * self.AddedFlangeThickness2 #bottom flange

        self.y1 = self.Height/2.0 + self.AddedFlangeThickness2  #web
        self.y2 = self.Height + self.AddedFlangeThickness1/2.0 + self.AddedFlangeThickness2 #top flange
        self.y3 = self.AddedFlangeThickness2/2.0 #bottom flange
        
        self.A = self.A1+self.A2+self.A3
        self.y = (self.A1*self.y1+self.A2*self.y2+self.A3*self.y3)/(self.A)

    def calculateIW(self):
        I10 = (self.Thickness*self.Height**3)/12.0
        I20 = (self.AddedFlangeWidth1*self.AddedFlangeThickness1**3)/12.0
        I30 = (self.AddedFlangeWidth2*self.AddedFlangeThickness2**3)/12.0

        I11 = self.A1 * (self.y-self.y1)**2
        I21 = self.A2 * (self.y-self.y2)**2
        I31 = self.A3 * (self.y-self.y3)**2
        
        self.I = I10 + I20 + I30 + I11 + I21 + I31
        
        H = self.Height + self.AddedFlangeThickness1 + self.AddedFlangeThickness2
        if self.y > H/2.0:
            self.W = self.I/self.y
        else:
            self.W = self.I/(H-self.y)

    def __init__(self,L,H,t,F1b,F1t,F2b,F2t):
        self.Length  = L
        self.Height = H
        self.Thickness = t
        self.AddedFlangeWidth1 = F1b
        self.AddedFlangeThickness1 = F1t
        self.AddedFlangeWidth2 = F2b
        self.AddedFlangeThickness2 = F2t
        self.Supports = []
        self.PointLoads = []
        self.DistributedLoads = []
        self.Locations = []

        self.calculatey()
        self.calculateIW()
        
    def addSupport(self,x):
        self.Supports.append(x)
        self.Locations.append(x)
        
    def addPointLoad(self,x):
        self.PointLoads.append(x)
        self.Locations.append(x)
        
    def addRectLoad(self,x1,x2,w):
        load = rectLoad(x1,x2,w)
        self.DistributedLoads.append(load)
        step = (x2 - x1)/100
        for i in range(x1,x2,step):
            self.Locations.append(i)
            
    def addTrigLoad(self,x1,x2,w):
        load = triLoad(x1,x2,w)
        self.DistributedLoads.append(load)
        step = (x2 - x1)/100.0
        for i in np.arange(x1,x2,step):
            self.Locations.append(i)
        
    def getI(self):
        return self.I
        
    def getW(self):
        return self.W
        
    def gety(self):
        return self.y
        
    def drawSection(self):
        x  = -self.Thickness/2.0
        y = self.AddedFlangeThickness2
        W = self.Thickness
        H = self.Height
        
        X = max(self.AddedFlangeWidth2,self.AddedFlangeWidth1)
        Y = self.AddedFlangeThickness2 + self.Height + self.AddedFlangeThickness1
        
        fig1 = plt.figure(1)
        plt.plot([0,0,0],[self.y3,self.y1,self.y2],'ro')
        plt.axis([-X/2.0-50,X/2.0+50,-20,Y+20])
        plt.title('Beam Section')
        plt.xlabel('X-coordinate')
        plt.ylabel('Y-coordinate')
        
        ax1 = fig1.add_subplot(111)
        
        ax1.add_patch(
            patches.Rectangle(
                (x, y),   # (x,y)
                W,          # width
                H,          # height
            )
        )

        x  = -self.AddedFlangeWidth2/2.0
        y = 0.0
        W = self.AddedFlangeWidth2
        H = self.AddedFlangeThickness2

        ax1.add_patch(
            patches.Rectangle(
                (x, y),   # (x,y)
                W,          # width
                H,          # height
            )
        )

        x  = -self.AddedFlangeWidth1/2.0
        y = Y - self.AddedFlangeThickness1
        W = self.AddedFlangeWidth1
        H = self.AddedFlangeThickness1

        ax1.add_patch(
            patches.Rectangle(
                (x, y),   # (x,y)
                W,          # width
                H,          # height
            )
        )
        
        fig1.show()

b = beam(1000.0,700.0,11.0,550.0,8.0,550.0,8.0) #all dimensions in mm L,H,t,F1b,F1t,F2b,F2t
b.drawSection()
b.addTrigLoad(150.0,250.0,50.0)