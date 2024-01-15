# Code snippet to rotate a polygon using the arrow keys
# TODO adapt and integrate into the scene editor
# Also adapt the tkinter imports from here, comment for Tkinter >= 8.6

from tkinter import *
from tkinter import ttk
import math

lastx, lasty = 0, 0
poly = None  # New global variable to store the polygon's ID
angle = 0  # New global variable to store the current angle of rotation
rot_step = 5  # Rotation step in degrees

def xy(event):
    global lastx, lasty
    lastx, lasty = event.x, event.y

def createPoly(event):
    global lastx, lasty, poly  # Include poly in the global statement
    size = 50
    width = 20
    x1 = lastx - size/2
    y1 = lasty - width/2
    x2 = lastx + size/2
    y2 = lasty + width/2
    poly = canvas.create_polygon((x1, y1, x2, y1, x2, y2, x1, y2), outline="white", fill="blue")  # Assign the polygon's ID to poly
    lastx, lasty = event.x, event.y

def movePoly(event):  # New function to move the polygon
    global lastx, lasty
    x, y = event.x, event.y
    poly = canvas.find_withtag(CURRENT)  # Get the ID of the polygon under the cursor
    if poly:
        canvas.move(poly, x - lastx, y - lasty)
    lastx, lasty = x, y

def rotatePoly(event):  # New function to rotate the polygon
    global lastx, lasty, angle, rot_step
    poly = canvas.find_withtag(CURRENT)  # Get the ID of the polygon under the cursor
    if poly:
        if event.keysym == "Right":
            angle = rot_step
        elif event.keysym == "Left":
            angle = -rot_step
        points = rotate(canvas.coords(poly), math.radians(angle), (lastx, lasty))  # Rotate the polygon
        canvas.coords(poly, *points)  # Update the polygon coordinates using canvas.coords method
def rotate(points, angle, center):
    """Rotate a point counterclockwise by a given angle around a given origin."""
    return [(math.cos(angle) * (px-center[0]) - math.sin(angle) * (py-center[1]) + center[0],
             math.sin(angle) * (px-center[0]) + math.cos(angle) * (py-center[1]) + center[1]) for px, py in zip(points[::2], points[1::2])]

root = Tk()
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

canvas = Canvas(root, highlightthickness=0) # Set highlightthickness to 0 to avoid a 1 pixel border around the canvas
canvas.grid(column=0, row=0, sticky=(N, W, E, S))
canvas.bind("<Button-1>", xy)
canvas.bind("<B1-Motion>", movePoly)  # Bind <B1-Motion> to movePoly instead of addLine
canvas.bind("<Right>", rotatePoly)  # Bind <Right> key to rotatePoly for clockwise rotation
canvas.bind("<Left>", rotatePoly)  # Bind <Left> key to rotatePoly for counterclockwise rotation
canvas.bind("<Double-Button-1>", createPoly)

canvas.focus_set()  # Set the focus to the canvas widget

root.mainloop()