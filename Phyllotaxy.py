from tkinter import Tk, Canvas, Frame, BOTH, YES, TOP, Scrollbar, RIGHT, LEFT, Y, Listbox
import math
from PIL import Image
import numpy as np


class Example(Frame):

    points=[]

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.master.title("Lines")
        self.pack(fill=BOTH, expand=1)
        #espacement = 1
        espacement = 2
        print("esp : ", espacement)
        mm=7
        nb_points=180

        centerx=400
        centery=400

        print ("x=", centerx, " et y=", centery)

        canvas = Canvas(self)
        canvas.create_oval(centerx-mm/2, centery-mm/2, centerx+mm/2, centery+mm/2, fill='red', outline='blue')

        self.draw_spirale(canvas, nb_points, centerx, centery, espacement, mm)


        canvas.pack(fill=BOTH, expand=1)
    
    def draw_spirale(self, canvas, nb_points, centerx, centery, espacement, mm):
        ang=137.51

        points=[]

        for i in range (0,nb_points):
            basex=centerx
            basey=centery
            baserad=((ang*(nb_points-i-1))*(math.pi/180))
            #print("rad : ", baserad)

            oval=[basex, basey, baserad]
            points.append(oval)

            newpoints=[]

            for point in points:

                centerxp=point[0]+math.cos(point[2])*espacement
                centeryp=point[1]-math.sin(point[2])*espacement

                oval=[centerxp, centeryp, point[2]]
                newpoints.append(oval)
        
            points=[]
            points=newpoints

        
        pixels=points

        
        for pixel in pixels:

            x0=pixel[0]-mm/2
            y0=pixel[1]-mm/2
            x1=pixel[0]+mm/2
            y1=pixel[1]+mm/2

            canvas.create_oval(x0, y0, x1, y1, fill='blue', outline='red')



def main():

    root = Tk()

    ex = Example()
    root.geometry("800x800+300+300")
    
    root.mainloop()


if __name__ == '__main__':
    main()