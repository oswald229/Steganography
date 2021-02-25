from tkinter import Tk, Canvas, Frame, BOTH, YES, TOP, Scrollbar, RIGHT, LEFT, Y, Listbox
import math
from PIL import Image
import numpy as np


img = Image.open("full_jpg.jpg")
imgtomodify = img

msg = "Ce texte est caché grâce à la phyllotaxie dans une image de Hubble !"
binary = []

for i in range(0, len(msg)):
    temp = ord(msg[i])
    temp = format(temp, '08b')
    for i in range (0, int(len(temp)/2)):
        toadd=temp[i*2:(i+1)*2]
        binary.append(toadd)

class Example(Frame):

    points=[]

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        espacement = math.floor((img.size[0]/2)/len(binary))
        print("espacement : ", espacement)
        
        ang = 137.51
        print("ang :", ang)

        nb_points=len (binary)

        centerx=img.size[0]/2
        centery=img.size[1]/2

        self.draw_spirale(nb_points, centerx, centery, espacement, ang)
    
    def draw_spirale(self, nb_points, centerx, centery, espacement, ang):

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

        points.reverse()
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
        
        for pixel in pixels:

            newim=img.load()
            pixelG = newim[pixel[0],pixel[1]][1]
            pixelB = newim[pixel[0],pixel[1]][2]

            pixelR = bin(newim[pixel[0],pixel[1]][0] >> 2)
            pixelR = pixelR.replace('0b', '')
            pixelR = pixelR+binary[pixels.index(pixel)]
            
            pixelR = int(pixelR, 2)

            imgtomodify.putpixel((pixel[0], pixel[1]), (pixelR, pixelG, pixelB))

        imgtomodify.save("Phyllo.png", "PNG")
        

def main():

    ex = Example()

if __name__ == '__main__':
    main()