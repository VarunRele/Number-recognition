import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from tinyvgg import *
import ast

# Global variables to track drawing state
drawing = False
last_x, last_y = None, None
pen_color = "black"
model = torch.load('cnn_model.pt', weights_only=False)

def start_drawing(event):
    global drawing
    drawing = True
    global last_x, last_y
    last_x, last_y = event.x, event.y

def stop_drawing(event):
    global drawing
    drawing = False

def draw(event, canvas):
    global last_x, last_y

    if drawing:
        x, y = event.x, event.y
        canvas.create_line((last_x, last_y, x, y), fill=pen_color, width=10)
        last_x, last_y = x, y

def change_color(new_color):
    global pen_color
    pen_color = new_color

def get_canvas_contents(canvas, mat, width=28, height=28):
    # Create a 2D matrix initialized with 0.0
    matrix = torch.zeros((height, width))
    
    # Get all items on the canvas
    items = canvas.find_all()
    
    for item in items:
        coords = canvas.coords(item)
        
        # Fill the matrix based on the item's coordinates
        # for x in range(int(coords[0]), int(coords[2])):  # x1 to x2
        #     for y in range(int(coords[1]), int(coords[3])):  # y1 to y2
        #         if 0 <= x < width and 0 <= y < height:
        #             matrix[y][x] = 1.0  # Mark the cell as drawn
        x, y = coords[0], coords[1]
        x_scaled = int(x * width / canvas.winfo_width())
        y_scaled = int(y * height / canvas.winfo_height())
        matrix[y_scaled][x_scaled] = 1.0
    
    # plt.imshow(matrix);
    # plt.show()
    value = matrix.unsqueeze(dim=0)
    preds = model.predict(value, probs=True)[0]
    preds = {i:s for i,s in enumerate(preds)}
    lit = sorted(preds.items(), key=lambda x: -x[1])
    label_0_string.set(f'{lit[0][0]} - {lit[0][1]:.4%}')
    label_1_string.set(f'{lit[1][0]} - {lit[1][1]:.4%}')
    label_2_string.set(f'{lit[2][0]} - {lit[2][1]:.4%}')
    label_3_string.set(f'{lit[3][0]} - {lit[3][1]:.4%}')
    label_4_string.set(f'{lit[4][0]} - {lit[4][1]:.4%}')
    label_5_string.set(f'{lit[5][0]} - {lit[5][1]:.4%}')
    label_6_string.set(f'{lit[6][0]} - {lit[6][1]:.4%}')
    label_7_string.set(f'{lit[7][0]} - {lit[7][1]:.4%}')
    label_8_string.set(f'{lit[8][0]} - {lit[8][1]:.4%}')
    label_9_string.set(f'{lit[9][0]} - {lit[9][1]:.4%}')
    # print(preds)
    mat.set(preds)
    # return matrix

def create_labels(canvas, mats):
    mats = ast.literal_eval(mats)
    lit = sorted(mats.items(), key=lambda x: -x[1])
    print(lit)


root = tk.Tk()
root.title("Paint Application")

frame = tk.Frame(root, width=400, height=300)
frame2 = tk.Frame(frame)
canvas = tk.Canvas(frame, width=400, height=300, bg="white")
canvas.pack(side=tk.LEFT)
frame.pack()
frame2.pack(side=tk.LEFT)

colors = ["red", "green", "blue", "black", "orange", "pink"]

color_buttons = []
for color in colors:
    color_buttons.append(tk.Button(root, text=color.capitalize(), bg=color, command=lambda c=color: change_color(c)))
    color_buttons[-1].pack(side=tk.LEFT)

mat = tk.Variable()
set_button = tk.Button(root, text='Save', command=lambda: get_canvas_contents(canvas, mat, 28, 28))
set_button.pack(side=tk.LEFT)

clear_button = tk.Button(root, text="Clear Canvas", command=lambda: canvas.delete('all'))
clear_button.pack(side=tk.LEFT)

# pmat = tk.Button(root, text='print mat', command=lambda: create_labels(canvas, mat.get()))
# pmat.pack(side=tk.LEFT)

canvas.bind("<Button-1>", start_drawing)
canvas.bind("<ButtonRelease-1>", stop_drawing)
canvas.bind("<B1-Motion>", lambda event: draw(event, canvas))

label_0_string = tk.StringVar(value='0 label')
label_0 = tk.Label(frame2, text='Empty', font='Calibri 20', textvariable=label_0_string)
label_0.pack(side=tk.TOP)

label_1_string = tk.StringVar(value='Empty')
label_1 = tk.Label(frame2, text='Empty', font='Calibri 20', textvariable=label_1_string)
label_1.pack(side=tk.TOP)

label_2_string = tk.StringVar(value='Empty')
label_2 = tk.Label(frame2, text='Empty', font='Calibri 20', textvariable=label_2_string)
label_2.pack(side=tk.TOP)

label_3_string = tk.StringVar(value='Empty')
label_3 = tk.Label(frame2, text='Empty', font='Calibri 20', textvariable=label_3_string)
label_3.pack(side=tk.TOP)

label_4_string = tk.StringVar(value='Empty')
label_4 = tk.Label(frame2, text='Empty', font='Calibri 20', textvariable=label_4_string)
label_4.pack(side=tk.TOP)

label_5_string = tk.StringVar(value='Empty')
label_5 = tk.Label(frame2, text='Empty', font='Calibri 20', textvariable=label_5_string)
label_5.pack(side=tk.TOP)

label_6_string = tk.StringVar(value='Empty')
label_6 = tk.Label(frame2, text='Empty', font='Calibri 20', textvariable=label_6_string)
label_6.pack(side=tk.TOP)

label_7_string = tk.StringVar(value='Empty')
label_7 = tk.Label(frame2, text='Empty', font='Calibri 20', textvariable=label_7_string)
label_7.pack(side=tk.TOP)

label_8_string = tk.StringVar(value='Empty')
label_8 = tk.Label(frame2, text='Empty', font='Calibri 20', textvariable=label_8_string)
label_8.pack(side=tk.TOP)

label_9_string = tk.StringVar(value='Empty')
label_9 = tk.Label(frame2, text='Empty', font='Calibri 20', textvariable=label_9_string)
label_9.pack(side=tk.TOP)

root.mainloop()