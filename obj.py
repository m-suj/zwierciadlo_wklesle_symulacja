import arcade
from math import radians, tan, sqrt


def print_prec(args: dict[str: float]):
    for k, v in args.items():
        v = round(v, 2)
        print(f'{k}={v}', end=', ')
    print()



class Mirror:
    def __init__(self, x_o: float, y_o: float, r: float, degrees):
        self.x = x_o
        self.y = y_o
        self.r = r
        self.f = self.r / 2
        self.degrees = degrees
        self.x_f, self.y_f = self.x + self.r / 2, self.y

    def draw(self):
        arcade.draw_line(0, self.y, 1200, self.y, arcade.color.GRAY)
        arcade.draw_arc_outline(self.x, self.y, self.r * 2, self.r * 2, arcade.color.BLACK, -self.degrees, self.degrees, 5)
        arcade.draw_point(self.x, self.y, arcade.color.BLACK, 5)
        arcade.draw_point(self.x + self.r / 2, self.y, arcade.color.BLACK, 3)



class Object:
    def __init__(self, mirror: Mirror, x: float, height=50, color=arcade.color.BLUE):
        self.mirror = mirror
        self.x = x
        self.height = height
        self.color = color
        x_o, y_o, r = self.mirror.x, self.mirror.y, self.mirror.r
        b = y_o + self.height
        delta = (-2*x_o)**2 - 4*(x_o**2 + b**2 + y_o**2 - 2*b*y_o - r**2)
        # Tip of an arrow
        self.x_s, self.y_s = x_o + r - self.x, y_o + self.height
        # Cross Point of first ray
        self.x_e = (2*x_o + sqrt(delta)) / 2
        self.y_e = b
        # Reflected first ray
        x_f, y_f = self.mirror.x_f, self.mirror.y_f
        self.a_r1 = (self.y_e - y_f) / (self.x_e - x_f)
        self.b_r1 = y_f - self.a_r1 * x_f
        # Cross Point of second ray
        self.x_e2, self.y_e2 = x_o + r, y_o
        # Reflected second ray
        self.a_r2 = -(self.y_e2 - self.y_s) / (self.x_e2 - self.x_s)
        self.b_r2 = self.y_e2 - self.a_r2 * self.x_e2

        # Cross Point of two reflected rays
        self.x_image = (self.b_r2 - self.b_r1) / (self.a_r1 - self.a_r2)
        self.y_image = self.a_r2 * self.x_image + self.b_r2

    def draw_arrow(self):
        arcade.draw_line(self.x_s, self.y_s - self.height, self.x_s, self.y_s, self.color, 5)

    def draw_arrow_image(self):
        arcade.draw_line(self.x_image, self.y_s - self.height, self.x_image, self.y_image, self.color, 5)

    def draw_first_ray(self):
        arcade.draw_line(self.x_s, self.y_s, self.x_e, self.y_e, self.color, 3)
        arcade.draw_line(self.x_e, self.y_e, 100, self.a_r1 * 100 + self.b_r1, self.color, 3)
        # x < f
        if self.x < self.mirror.f:
            arcade.draw_line(self.x_e, self.y_e, 800, self.a_r1 * 800 + self.b_r1, self.color)

    def draw_second_ray(self):
        arcade.draw_line(self.x_s, self.y_s, self.x_e2, self.y_e2, self.color, 3)
        arcade.draw_line(self.x_e2, self.y_e2, 100, self.a_r2 * 100 + self.b_r2, self.color, 3)
        # x < f
        if self.x < self.mirror.f:
            arcade.draw_line(self.x_e2, self.y_e2, 800, self.a_r2 * 800 + self.b_r2, self.color)


    def draw(self):
        self.draw_arrow()
        self.draw_first_ray()
        self.draw_second_ray()
        self.draw_arrow_image()



class Simulation:
    def __init__(self):
        self.mirror: Mirror = Mirror(
            x_o=300,
            y_o=300,
            r=200,
            degrees=80,
        )
        self.objects: list[Object] = [
            Object(self.mirror, x=300, height=50, color=arcade.color.RED),
            Object(self.mirror, x=200, height=50, color=arcade.color.ORANGE),
            Object(self.mirror, x=150, height=50, color=arcade.color.YELLOW_GREEN),
            Object(self.mirror, x=100, height=50, color=arcade.color.BLUE),
            Object(self.mirror, x=50, height=50, color=arcade.color.PURPLE),
        ]

    def draw(self):
        for obj in self.objects:
            obj.draw()
        self.mirror.draw()