import main
import pyglet
from pyglet import shapes
 
title = "Graphs"
width = 900
height = 500

window = pyglet.window.Window(width, height, title)
batch = pyglet.graphics.Batch()

 
line_width = 3
y_offset = 250

 
x_axis = shapes.Line(0, height/2-y_offset, width, height/2-y_offset,
    line_width, color = (255, 225, 255), batch = batch)
y_axis = shapes.Line(width/2, 0, width/2, height,
    line_width, color = (255, 225, 255), batch = batch)

lines = list()
scale = 200

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
for x in x_ls:
    # x-=width/2
    x*=scale

    y = main.actual(x/scale)*scale-y_offset
   
    lines += [shapes.Circle(x+width/2, y+height/2,line_width,color=(255, 255, 255),batch = batch)]
 

    y = main.lagrange_interpolating_polynomial(x/scale)*scale-y_offset

    lines += [shapes.Circle(x+width/2, y+height/2,line_width,color=(255, 0, 0),batch = batch)]


    y = main.newtons_divided_difference_formula(x/scale)*scale-y_offset

    lines += [shapes.Circle(x+width/2, y+height/2,line_width,color=(0, 255, 0),batch = batch)]

 
# for x in [0, 0.25, 0.5, 0.25, 1]:
    # x*=scale
    x,y = main.bezier_point(x/scale)
    x,y = x*scale, y*scale-y_offset

    lines += [shapes.Circle(x+width/2, y+height/2,line_width,color=(0, 0, 255),batch = batch)]


# window draw event
@window.event
def on_draw():
     
    window.clear()
     
    batch.draw()
 
pyglet.app.run()