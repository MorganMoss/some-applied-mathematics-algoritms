import pyglet
from pyglet import shapes

import main



to_draw = list()



def draw_axis(line_width = 1):
    global to_draw
    x_axis = shapes.Line(0, height/2-y_offset, width, height/2-y_offset,
        line_width, color = (255, 225, 255), batch = batch)
    y_axis = shapes.Line(width/2, 0, width/2, height,
        line_width, color = (255, 225, 255), batch = batch)
    to_draw += [x_axis,  y_axis]


def draw_graphs(line_width = 1):
    global to_draw
    for x in range(width):
        x-=width/2
        prev_x = x -1

        y = main.actual(x/scale)*scale-y_offset
        prev_y = main.actual(prev_x/scale)*scale-y_offset
        to_draw += [shapes.Line(prev_x+width/2, prev_y+height/2, x+width/2, y+height/2,
            line_width, color = (255, 255, 255), batch = batch)]

        y = main.lagrange_interpolating_polynomial(x/scale)*scale-y_offset
        prev_y = main.lagrange_interpolating_polynomial(prev_x/scale)*scale-y_offset

        to_draw += [shapes.Line(prev_x+width/2, prev_y+height/2, x+width/2, y+height/2,
            line_width, color = (255, 0, 0), batch = batch)]

        y = main.newtons_divided_difference_formula(x/scale)*scale-y_offset
        prev_y = main.newtons_divided_difference_formula(prev_x/scale)*scale-y_offset

        to_draw += [shapes.Line(prev_x+width/2, prev_y+height/2, x+width/2, y+height/2,
            line_width, color = (0, 255, 0), batch = batch)]
    
        x,y = main.bezier_point(x/scale)
        x,y = x*scale, y*scale-y_offset
        prev_x,prev_y = main.bezier_point(prev_x/scale)
        prev_x,prev_y = prev_x*scale, prev_y*scale-y_offset

        to_draw += [shapes.Line(prev_x+width/2, prev_y+height/2, x+width/2, y+height/2,
            line_width, color = (0, 0, 255), batch = batch)]


def make_point(x_, y_, color_, offset = 20, line_width = 3):
    global to_draw
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

        y = main.actual(x/scale)*scale-y_offset
        make_point(x, y, (255, 255, 255), 60)

        y = main.lagrange_interpolating_polynomial(x/scale)*scale-y_offset
        make_point(x, y, (255, 0,0), 40)

        y = main.newtons_divided_difference_formula(x/scale)*scale-y_offset
        make_point(x, y, (0, 255, 0))

        x,y = main.bezier_point(x/scale)
        x,y = x*scale, y*scale-y_offset
        make_point(x, y, (100,100,255), -20)


def label():
    global to_draw

    g_list = [
        ("Actual", (255,255,255,255)),
        ("Lagrange Interpolating Polynomial", (255, 0,0,255)),
        ("Newtons Divided Difference Formula", (0, 255, 0,255)),
        ("Bezier Curve", (100,100,255,255))
    ]

    i = 0

    for g in g_list:
        name, color = g
        to_draw += [pyglet.text.Label(text = f"{name}  ⎯⎯⎯⎯⎯⎯",
            font_name='Times New Roman',
            font_size=global_font_size,
            x=5,
            y=height-10-i*global_font_size*2.5, 
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
    batch = pyglet.graphics.Batch()
    text_batch = pyglet.graphics.Batch()

    global_font_size = 12

    
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

    main.main()

