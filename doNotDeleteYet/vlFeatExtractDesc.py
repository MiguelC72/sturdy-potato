import numpy as np
import os 
from PIL import Image

vlFeat = "/home/maotouying/Code/LSDMProject/imagesAndKeyPoints/sturdy-potato/vlfeat-0.9.20/bin/glnxa64/sift "
params = "--edge-thresh 10 --peak-thresh 5"

laptopIm = Image.open('laptop.jpg').convert('L')
laptopIm.save('laptop.pgm')
laptopImName = 'laptop.pgm'

cmmd = str(vlFeat + laptopImName + " --output=laptop.sift" + " " + params)

os.system(cmmd)

notebookIm = Image.open('notebook.png').convert('L')
notebookIm.save('notebook.pgm')
notebookImName = 'notebook.pgm'
					
cmmd = str(vlFeat + notebookImName + " --output=notebook.sift" + " " + params)

os.system(cmmd)

pencilIm = Image.open('pencil.jpg').convert('L')
pencilIm.save('pencil.pgm')
pencilImName = 'pencil.pgm'
					
cmmd = str(vlFeat + pencilImName + " --output=pencil.sift" + " " + params)

os.system(cmmd)

printerIm = Image.open('printer.jpg').convert('L')
printerIm.save('printer.pgm')
printerImName = 'printer.pgm'
					
cmmd = str(vlFeat + printerImName + " --output=printer.sift" + " " + params)

os.system(cmmd)

cleanUp = "rm *.pgm"
os.system(cleanUp)
