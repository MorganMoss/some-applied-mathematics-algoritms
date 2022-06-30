import main
import pyglet
from pyglet import shapes
 
title = "Graphs"
width = 900
height = 800

window = pyglet.window.Window(width, height, title)
batch = pyglet.graphics.Batch()



line_width = 1
y_offset = 225

 
x_axis = shapes.Line(0, height/2-y_offset, width, height/2-y_offset,
    line_width, color = (255, 225, 255), batch = batch)
y_axis = shapes.Line(width/2, 0, width/2, height,
    line_width, color = (255, 225, 255), batch = batch)

lines = list()
scale = 300

line_width = 1
for x in range(width):
    x-=width/2
    prev_x = x -1

    y = main.actual(x/scale)*scale-y_offset
    prev_y = main.actual(prev_x/scale)*scale-y_offset
    lines += [shapes.Line(prev_x+width/2, prev_y+height/2, x+width/2, y+height/2,
        line_width, color = (255, 255, 255), batch = batch)]

    y = main.lagrange_interpolating_polynomial(x/scale)*scale-y_offset
    prev_y = main.lagrange_interpolating_polynomial(prev_x/scale)*scale-y_offset

    lines += [shapes.Line(prev_x+width/2, prev_y+height/2, x+width/2, y+height/2,
        line_width, color = (255, 0, 0), batch = batch)]

    y = main.newtons_divided_difference_formula(x/scale)*scale-y_offset
    prev_y = main.newtons_divided_difference_formula(prev_x/scale)*scale-y_offset

    lines += [shapes.Line(prev_x+width/2, prev_y+height/2, x+width/2, y+height/2,
        line_width, color = (0, 255, 0), batch = batch)]
 
    x,y = main.bezier_point(x/scale)
    x,y = x*scale, y*scale-y_offset
    prev_x,prev_y = main.bezier_point(prev_x/scale)
    prev_x,prev_y = prev_x*scale, prev_y*scale-y_offset

    lines += [shapes.Line(prev_x+width/2, prev_y+height/2, x+width/2, y+height/2,
        line_width, color = (0, 0, 255), batch = batch)]




line_width = 3
x_ls = [-1, -0.5, 0, 0.25, 0.5]

def make_point(x_, y_, color_, offset = 20):
    global lines
    r = 3
    lines += [shapes.Circle(x_+width/2, y_+height/2,line_width,color=color_,batch = batch)]
    color_ = (*color_,255)
    lines += [pyglet.text.Label(text = f"({round(x_/scale, r)},{round((y_-y_offset)/scale, r)})",
        font_name='Times New Roman',
        font_size=8,
        x=x_+width/2,
        y=y_+height/2+offset, 
        color = color_,
        # anchor_x='center',
        anchor_y='center', batch=batch)]

for x in x_ls:
    # x-=width/2
    x*=scale

    y = main.actual(x/scale)*scale-y_offset
    make_point(x, y, (255, 255, 255), 60)

    y = main.lagrange_interpolating_polynomial(x/scale)*scale-y_offset
    make_point(x, y, (255, 0,0), 40)

    y = main.newtons_divided_difference_formula(x/scale)*scale-y_offset
    make_point(x, y, (0, 255, 0))

    x,y = main.bezier_point(x/scale)
    x,y = x*scale, y*scale-y_offset
    make_point(x, y, (100,100,255), -20)


# window draw event
@window.event
def on_draw():
     
    window.clear()
     
    batch.draw()
 
pyglet.app.run()