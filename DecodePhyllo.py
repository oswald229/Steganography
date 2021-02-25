from tkinter import Tk, Canvas, Frame, BOTH, YES, TOP, Scrollbar, RIGHT, LEFT, Y, Listbox
import math
from PIL import Image


img = Image.open("Phyllo.png")
imgtomodify = img

class Example(Frame):

    points=[]

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        espacement = 6
        ang=137.51

        nb_points=int((img.size[0]/2)/espacement)
        print (nb_points)

        centerx=img.size[0]/2
        centery=img.size[1]/2


        self.decode(nb_points, centerx, centery, espacement, ang)

    
    def decode(self, nb_points, centerx, centery, espacement, ang):

        points=[]

        for i in range (0,nb_points):
            basex=centerx
            basey=centery
            baserad=((ang*(nb_points-i-1))*(math.pi/180))

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

        
        pixels=[]

        for point in points:
            thepoint=[int(round(point[0],0)), int(round(point[1],0))]
            pixels.append(thepoint)

        for i in range (0, len(pixels)):
            for j in range (0, len(pixels)):
                if(i != j):
                    x=pixels[i][0]
                    y=pixels[i][1]
                    xp=pixels[j][0]
                    yp=pixels[j][1]
                    if(x == xp and y == yp):
                        print("SAME !!")

        
        pixels.reverse()
        newim=img.load()

        decoded=""
        fini=False
        for pixel in pixels:
            if (pixels.index(pixel)%4 == 0):
                if(pixels.index(pixel) != 0):
                    letter = chr(int(letter, 2))
                    decoded += letter
                    if (letter == '!'):
                        fini=True
                letter = '0b'
                pixelR = newim[pixel[0],pixel[1]][0]
                letter += bin(pixelR)[-2:]
            else:
                pixelR = newim[pixel[0],pixel[1]][0]
                letter += bin(pixelR)[-2:]
            
            if fini:
                break

        print (decoded)
    

def main():

    ex = Example()



if __name__ == '__main__':
    main()