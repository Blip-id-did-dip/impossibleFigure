from PIL import Image, ImageTk
from texture import texture
import tkinter as tk
from impossibleFigure import impossibleFigure



window = tk.Tk()
window.geometry('1700x1100')

global myFigure
global displayHeight
global displayWidth

displayHeight = 1000
displayWidth = 1500
myFigure = impossibleFigure()

#myFigure.left_texture.setTexture("local/RedJC.jpg")
#myFigure.right_texture.setTexture("test.jpg")
#myFigure.top_texture.setTexture("brick.jpg")

myArray = myFigure.loadPreview()

def testPos(event):

    print("original")
    print(event.x)
    print(event.y)

    

    myFigure.updateBoxlist(event.y / displayHeight ,event.x / displayWidth, leftIndicator.get() * forceIndicator.get(), topIndicator.get()* forceIndicator.get(), rightIndicator.get()* forceIndicator.get())
    myArray = myFigure.updatePreview(event.y / displayHeight , event.x / displayWidth)
    im = Image.fromarray(myArray)
    #im.show()
    tkimage = ImageTk.PhotoImage(im.resize((displayWidth,displayHeight)))
    #tkimage = ImageTk.PhotoImage(im)
    event.widget.config(image = tkimage)
    event.widget.image = tkimage


def renderMe():
    renderedArray = myFigure.getFigure()
    renderedImage = Image.fromarray(renderedArray)
    renderedImage = renderedImage.save("local\example1.png")

def saveFigure():
    myFigure.saveFigure()

def loadFigure():
    myFigure.loadFigure()
    myArray = myFigure.updatePreview(0,0,True)
    im = Image.fromarray(myArray)
    #im.show()
    tkimage = ImageTk.PhotoImage(im.resize((displayWidth,displayHeight)))
    #tkimage = ImageTk.PhotoImage(im)
    label.config(image = tkimage)
    label.image = tkimage

im = Image.fromarray(myArray)
tkimage = ImageTk.PhotoImage(im.resize((displayWidth,displayHeight)) )

frameImage = tk.Frame(window)
frameButtons = tk.Frame(window)

label = tk.Label(frameImage , image = tkimage)
label.bind("<Button-1>", testPos)
label.pack()
frameImage.pack(side='left')

topIndicator = tk.IntVar()
leftIndicator = tk.IntVar()
rightIndicator = tk.IntVar()
forceIndicator = tk.IntVar()

topCheckBox = tk.Checkbutton(frameButtons, text='top', variable=topIndicator, onvalue=1, offvalue=0)
leftCheckBox = tk.Checkbutton(frameButtons, text='left', variable=leftIndicator, onvalue=1, offvalue=0)
rightCheckBox = tk.Checkbutton(frameButtons, text='right', variable=rightIndicator, onvalue=1, offvalue=0)
forcedCheckBox = tk.Checkbutton(frameButtons, text='force',variable = forceIndicator, onvalue= 2, offvalue=1)
topCheckBox.pack(side='top')
leftCheckBox.pack(side='top')
rightCheckBox.pack(side='top')
forcedCheckBox.pack(side='top')
forcedCheckBox.select()
forcedCheckBox.deselect()

renderButton = tk.Button(frameImage, text = "Render", command = renderMe)
saveButton = tk.Button(frameButtons, text="Save", command = saveFigure)
loadButton = tk.Button(frameButtons, text="Load", command = loadFigure)

renderButton.pack()
saveButton.pack(side = 'right')
loadButton.pack(side = 'right')

frameButtons.pack(side='left')

window.mainloop()
