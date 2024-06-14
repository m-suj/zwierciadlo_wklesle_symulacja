import arcade
from math import radians, tan, sqrt

MIRROR_X = 300
MIRROR_Y = 300
MIRROR_R = 200


def print_prec(args: dict[str: float]):
    for k, v in args.items():
        v = round(v, 2)
        print(f'{k}={v}', end=', ')
    print()


class Ray:
    def __init__(self, angle, delay=0, color=arcade.color.BRICK_RED):
        self.angle = angle
        self.color = color
        theta = radians(angle)
        a = tan(theta)
        b = MIRROR_Y - a * OBJECT_POSX
        start_x, start_y = OBJECT_POSX, MIRROR_Y + delay
        x_o, y_o = MIRROR_X, MIRROR_Y
        eq_a, eq_b, eq_c = (
            1 + a**2,
            -2*x_o + 2*a*(b-y_o),
            x_o ** 2 + (b - y_o) ** 2 - MIRROR_R ** 2
        )
        delta = eq_b ** 2 - 4 * eq_a * eq_c
        d = sqrt(delta)
        n, d = -eq_b + d, 2 * eq_a
        end_x = n / d
        end_y = a * end_x + b

        # Reflected ray
        # Tangent
        a_t = (x_o - end_x) / (end_y - y_o)
        b_t = end_y - a_t * end_x

        # Perpendicular
        a_p = -1 / a_t
        b_p = end_y - a_p * end_x

        # Parallel
        b_s = start_y - a_t * start_x

        # Cross point
        x_x = (b_s - b_p) / (a_p - a_t)
        y_x = a_t * x_x + b_s

        # Symmetrical point
        delta_x = x_x - start_x
        delta_y = y_x - start_y
        x_s, y_s = x_x + delta_x, y_x + delta_y

        # Reflected ray
        a_r = (end_y - y_s) / (end_x - x_s)
        b_r = y_s - a_r * x_s


        self.start_x, self.start_y = start_x, start_y
        self.end_x, self.end_y = end_x, end_y
        self.a_t, self.b_t = a_t, b_t
        self.a_r, self.b_r = a_r, b_r

    def draw(self):
        arcade.draw_line(
            start_x=self.start_x,
            start_y=self.start_y,
            end_x=self.end_x,
            end_y=self.end_y,
            color=arcade.color.BLUE,
            line_width=1
        )
        s, e = (self.end_x, self.end_y), (100, self.a_r*100 + self.b_r)
        if self.a_r < 0 and self.end_y > MIRROR_Y or self.a_r > 0 and self.end_y < MIRROR_Y:
            e = (600, self.a_r*600 + self.b_r)
        arcade.draw_line(s[0], s[1], e[0], e[1], self.color, 1)


class Object:
    def __init__(self, x, height=50, color=arcade.color.BLUE):
        self.x = x
        self.height = height
        self.color = color

    def draw_arrow(self):
        arcade.draw_line(self.x)

    def draw(self):
        self.draw_arrow()



class Mirror:
    def __init__(self, x, y, r, degrees):
        self.x = x
        self.y = y
        self.r = r
        self.degrees = degrees

    def draw(self):
        arcade.draw_line(0, self.y, 1200, self.y, arcade.color.GRAY)
        arcade.draw_arc_outline(self.x, self.y, self.r * 2, self.r * 2, arcade.color.BLACK, -self.degrees, self.degrees, 5)
        arcade.draw_point(self.x, self.y, arcade.color.RED, 3)
        arcade.draw_point(self.x + self.r / 2, self.y, arcade.color.BLACK, 3)


class Simulation:
    def __init__(self):
        self.mirror: Mirror = Mirror(MIRROR_X, MIRROR_Y, MIRROR_R, 90)
        self.objects: list[Object] = [Object(100)]

    def draw(self):
        for obj in self.objects:
            obj.draw()
        arcade.draw_point(OBJECT_POSX, self.mirror.y, arcade.color.BUD_GREEN, 6)