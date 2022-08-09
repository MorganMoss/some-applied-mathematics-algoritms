import pyglet
from pyglet import shapes

import graph_approximation




def initialize():
    global width, height, to_draw, batch
    display = pyglet.canvas.Display()
    screen = display.get_default_screen()
    width = screen.width
    height = screen.height

    batch = pyglet.graphics.Batch()
    to_draw = list()
        

def modify(f_s = 20, l_w = 5, sc = ..., y_o = ... , ask=False):
    global font_size, line_width, scale, y_offset

    if sc == ...:
        scale =  max(height, width)/3
    else:
        scale = sc
    
    if y_o == ... :
        y_offset = scale/3*4
    else:
        y_offset = y_o

    if ask:
        sc = input("enter the scale (Enter for default) : ")
        if sc != "": 
            scale = int(sc)

        y_o = input("enter the y offset (Enter for default) : ")
        if y_o != "": 
            y_offset = int(y_o)
    
    font_size = f_s
    line_width = l_w


def draw_axis(line_width = 1):
    global to_draw
    x_axis = shapes.Line(0, height/2-y_offset, width, height/2-y_offset,
        line_width, color = (255, 225, 255), batch = batch)
    y_axis = shapes.Line(width/2, 0, width/2, height,
        line_width, color = (255, 225, 255), batch = batch)
    to_draw += [x_axis,  y_axis]


def make_point(x_, y_, color_, offset = 20, line_width = 8):
    global to_draw
    offset = offset/10*font_size
    r = 3
    to_draw += [shapes.Circle(x_+width/2, y_+height/2,line_width,color=color_,batch = batch)]
    color_ = (*color_,255)
    to_draw += [pyglet.text.Label(text = f"({round(x_/scale, r)},{round((y_-y_offset)/scale, r)})",
        font_name='Times New Roman',
        font_size=font_size,
        x=x_+width/2+2,
        y=y_+height/2+offset, 
        color = color_,
        anchor_y='center', batch=batch)]


def plot(f, x_ls, color, text_vertical_offset = 20):
    global to_draw

    for x in range(width):
        x -= width / 2
        prev_x = x - 1

        y = (f(x/scale))*scale-y_offset
        prev_y = (f(prev_x/scale))*scale-y_offset
        to_draw += [shapes.Line(prev_x+width/2, prev_y+height/2, x+width/2, y+height/2,
            line_width, color = color, batch = batch)]
    
    for x in x_ls:
        x *= scale
        y = (f( x / scale )) * scale - y_offset
        make_point(x, y, color, text_vertical_offset)


def show():
    global batch, width, height

    draw_axis()   

    window = pyglet.window.Window(width, height, "Graphs")
    pyglet.gl.glClearColor(0.2,0.2,0.2,0.2)
    
    @window.event
    def on_draw():
        window.clear()
        batch.draw()
 
    pyglet.app.run()


def draw_graphs():
        x_ls = [-1, -0.5, 0, 0.25, 0.5]

        plot(graph_approximation.actual,
            x_ls, (255, 255, 255), 60)
        plot(graph_approximation.lagrange_interpolating_polynomial, 
            x_ls, (0, 255, 255), 40)
        plot(graph_approximation.newtons_divided_difference_formula, 
            x_ls, (255, 0, 255), 20)
        plot(graph_approximation.bezier_point_y_only, 
            x_ls, (255, 255, 0), -20)
        plot(graph_approximation.linear_least_squares_polynomial, 
            x_ls, (0, 255, 0), -40)
        plot(graph_approximation.least_squares_polynomial, 
            x_ls, (0, 0, 255), -60) 
        plot(graph_approximation.least_squares_exponential_form, 
            x_ls, ( 255, 0, 0), -80)


def label():
    global to_draw

    g_list = [
        ("Actual", (255,255,255,255)),
        ("Lagrange Interpolating Polynomial", (100, 255, 255 ,255)),
        ("Newtons Divided Difference Formula", (255, 100, 255 ,255)),
        ("Bezier Curve", (255, 255, 100,255)),
        ("Linear Least Squares", (100, 255, 100,255)),
        ("Least Squares of Degree 2", (100, 100, 255,255)),
        ("Least Squares (Exponential)", (255, 100, 100,255))
    ]

    i = 1

    for g in g_list:
        name, color = g
        to_draw += [pyglet.text.Label(text = f"―――\t {name}",
            font_name='Times New Roman',
            font_size= font_size,
            x=5,
            y=height-i*font_size*1.5, 
            color = color,
            anchor_y='center', batch=batch)]
        i+=1


if __name__ == "__main__":

    initialize()
    modify(ask=True)
    draw_graphs()
    label()
    show()


