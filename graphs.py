import pyglet
from pyglet import shapes

import graph_approximation

def draw_axis(line_width = 1):
    global to_draw
    x_axis = shapes.Line(0, height/2-y_offset, width, height/2-y_offset,
        line_width, color = (255, 225, 255), batch = batch)
    y_axis = shapes.Line(width/2, 0, width/2, height,
        line_width, color = (255, 225, 255), batch = batch)
    to_draw += [x_axis,  y_axis]


def draw_graphs(line_width = 5):
    global to_draw
    for x in range(width):
        x-=width/2
        prev_x = x -1

        y = graph_approximation.actual(x/scale)*scale-y_offset
        prev_y = graph_approximation.actual(prev_x/scale)*scale-y_offset
        to_draw += [shapes.Line(prev_x+width/2, prev_y+height/2, x+width/2, y+height/2,
            line_width, color = (255, 255, 255), batch = batch)]

        y = graph_approximation.lagrange_interpolating_polynomial(x/scale)*scale-y_offset
        prev_y = graph_approximation.lagrange_interpolating_polynomial(prev_x/scale)*scale-y_offset

        to_draw += [shapes.Line(prev_x+width/2, prev_y+height/2, x+width/2, y+height/2,
            line_width, color = (255, 0, 0), batch = batch)]

        y = graph_approximation.newtons_divided_difference_formula(x/scale)*scale-y_offset
        prev_y = graph_approximation.newtons_divided_difference_formula(prev_x/scale)*scale-y_offset

        to_draw += [shapes.Line(prev_x+width/2, prev_y+height/2, x+width/2, y+height/2,
            line_width, color = (0, 255, 0), batch = batch)]
    
        y = graph_approximation.bezier_point(x/scale)[1]*scale-y_offset
        prev_y = graph_approximation.bezier_point(prev_x/scale)[1]*scale-y_offset

        to_draw += [shapes.Line(prev_x+width/2, prev_y+height/2, x+width/2, y+height/2,
            line_width, color = (0, 0, 255), batch = batch)]
        
        y = graph_approximation.linear_least_squares_polynomial(x/scale)*scale-y_offset
        prev_y = graph_approximation.linear_least_squares_polynomial(prev_x/scale)*scale-y_offset

        to_draw += [shapes.Line(prev_x+width/2, prev_y+height/2, x+width/2, y+height/2,
            line_width, color = (255, 255, 0), batch = batch)]

        y = graph_approximation.least_squares_polynomial(x/scale)*scale-y_offset
        prev_y = graph_approximation.least_squares_polynomial(prev_x/scale)*scale-y_offset

        to_draw += [shapes.Line(prev_x+width/2, prev_y+height/2, x+width/2, y+height/2,
            line_width, color = (0, 255, 255), batch = batch)]

        y = graph_approximation.least_squares_exponential_form(x/scale)*scale-y_offset
        prev_y = graph_approximation.least_squares_exponential_form(prev_x/scale)*scale-y_offset

        to_draw += [shapes.Line(prev_x+width/2, prev_y+height/2, x+width/2, y+height/2,
            line_width, color = (255, 0, 255), batch = batch)]


def make_point(x_, y_, color_, offset = 20, line_width = 8):
    global to_draw
    offset = offset/10*global_font_size
    r = 3
    to_draw += [shapes.Circle(x_+width/2, y_+height/2,line_width,color=color_,batch = batch)]
    color_ = (*color_,255)
    to_draw += [pyglet.text.Label(text = f"({round(x_/scale, r)},{round((y_-y_offset)/scale, r)})",
        font_name='Times New Roman',
        font_size=global_font_size,
        x=x_+width/2+2,
        y=y_+height/2+offset, 
        color = color_,
        anchor_y='center', batch=text_batch)]


def plot_points( x_ls = [-1, -0.5, 0, 0.25, 0.5]):
    for x in x_ls:
        x*=scale
        
        y = graph_approximation.actual(x/scale)*scale-y_offset
        make_point(x, y, (255, 255, 255), 60)

        y = graph_approximation.lagrange_interpolating_polynomial(x/scale)*scale-y_offset
        make_point(x, y, (255, 0,0),-40)

        y = graph_approximation.newtons_divided_difference_formula(x/scale)*scale-y_offset
        make_point(x, y, (0, 255, 0), 40)

        y = graph_approximation.bezier_point(x/scale)[1]*scale-y_offset
        make_point(x, y, (100,100,255), -20)

        y = graph_approximation.linear_least_squares_polynomial(x/scale)*scale-y_offset
        make_point(x, y, (255, 255, 0), 80)

        y = graph_approximation.least_squares_polynomial(x/scale)*scale-y_offset
        make_point(x, y, (0, 255, 255), -60)
        
        y = graph_approximation.least_squares_exponential_form(x/scale)*scale-y_offset
        make_point(x, y, (255, 0, 255), -80)


def label():
    global to_draw

    g_list = [
        ("Actual", (255,255,255,255)),
        ("Lagrange Interpolating Polynomial", (255, 0,0,255)),
        ("Newtons Divided Difference Formula", (0, 255, 0,255)),
        ("Bezier Curve", (100,100,255,255)),
        ("Linear Least Squares", (255,255,100,255)),
        ("Least Squares of Degree 2", (100,255,255,255)),
        ("Least Squares (Exponential)", (255,100,255,255))
    ]

    i = 1

    for g in g_list:
        name, color = g
        to_draw += [pyglet.text.Label(text = f"―――\t {name}",
            font_name='Times New Roman',
            font_size=global_font_size,
            x=5,
            y=height-i*global_font_size*1.5, 
            color = color,
            anchor_y='center', batch=text_batch)]
        i+=1


if __name__ == "__main__":
    display = pyglet.canvas.Display()
    screen = display.get_default_screen()
    width = screen.width
    height = screen.height


    scale = input("enter the scale (Enter for default) : ")
    if scale == "": 
        scale = max(height, width)/3
    else: 
        scale = int(scale)

    y_offset = input("enter the y offset (Enter for default) : ")
    if y_offset == "": 
        y_offset = scale/3*4
    else: 
        y_offset = int(y_offset)

    window = pyglet.window.Window(width, height, "Graphs")
    pyglet.gl.glClearColor(0.2,0.2,0.2,0.2)
    
    batch = pyglet.graphics.Batch()
    text_batch = pyglet.graphics.Batch()

    global_font_size = 20

    to_draw = list()
    draw_axis()
    draw_graphs()
    plot_points()
    label()

    @window.event
    def on_draw():
        window.clear()
        batch.draw()
        text_batch.draw()
 
    pyglet.app.run()


