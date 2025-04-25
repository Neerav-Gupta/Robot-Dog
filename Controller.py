from pyPS4Controller.controller import Controller
from Walk import walk, reset, walk_right, walk_left, walk_back, turn_right, turn_left, dance, sit, lift


class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    def on_L3_up(self, value):
        pass
    def on_L3_down(self, value):
        pass
    def on_L3_right(self, value):
        pass
    def on_L3_left(self, value):
        pass
    def on_R3_up(self, value):
        pass
    def on_R3_down(self, value):
        pass
    def on_R3_right(self, value):
        pass
    def on_R3_left(self, value):
        pass
    def on_R3_y_at_rest(self):
        pass
    def on_R3_x_at_rest(self):
        pass
    def on_L3_x_at_rest(self):
        pass
    def on_L3_y_at_rest(self):
        pass
    def on_down_arrow_press(self):
        turn_left()
    def on_up_arrow_press(self):
        turn_right()
    def on_up_down_arrow_release(self):
        pass
    def on_R2_press(self, value):
        walk()
    def on_L2_press(self, value):
        walk_back()
    def on_R2_release(self):
        pass
    def on_L2_release(self):
        pass
    def on_x_press(self):
        reset()
    def on_x_release(self):
        pass
    def on_circle_press(self):
        sit()
    def on_circle_release(self):
        pass
    def on_square_press(self):
        dance()
    def on_square_release(self):
        pass
    def on_triangle_press(self):
        lift()
    def on_triangle_release(self):
        pass
    def on_left_arrow_press(self):
        walk_left()
    def on_right_arrow_press(self):
        walk_right()
    def on_left_right_arrow_release(self):
        pass
    
reset()
controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
# you can start listening before controller is paired, as long as you pair it within the timeout window
controller.listen(timeout=60)