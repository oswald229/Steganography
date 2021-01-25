from tkinter import Tk, Canvas, Frame, BOTH, YES, TOP
import math

class Example(Frame):

    points=[]

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.master.title("Lines")
        self.pack(fill=BOTH, expand=1)
        espacement = 1
        mm=5
        nb_points=200
        centerx=550
        centery=550

        canvas = Canvas(self)
        canvas.create_oval(centerx-mm/2, centery-mm/2, centerx+mm/2, centery+mm/2, fill='red', outline='blue')

        self.draw_spirale(canvas, nb_points, espacement, mm)


        canvas.pack(fill=BOTH, expand=1)
    
    def draw_spirale(self, canvas, nb_points, espacement, mm):
        ang=222

        points=[]

        for i in range (0,nb_points):
            basex=550
            basey=550
            baserad=((ang*i)*(math.pi/180))

            oval=[basex, basey, baserad]
            points.append(oval)

            newpoints=[]

            for point in points:

                centerx=point[0]+math.cos(point[2])*espacement
                centery=point[1]-math.sin(point[2])*espacement

                oval=[centerx, centery, point[2]]
                newpoints.append(oval)
        
            points=[]
            points=newpoints


        for point in points:

            x0=point[0]-mm/2
            y0=point[1]-mm/2
            x1=point[0]+mm/2
            y1=point[1]+mm/2

            canvas.create_oval(x0, y0, x1, y1, fill='blue', outline='red')
        




def main():

    root = Tk()
    ex = Example()
    root.geometry("1100x1100+300+300")
    root.mainloop()


if __name__ == '__main__':
    main()