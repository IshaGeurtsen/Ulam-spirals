from math import sqrt, floor, ceil
from dataclasses import dataclass
from turtle import Turtle, Screen
from contextlib import contextmanager


class Settings:
    base_stride = 20
    ulam_spiral_start = 1
    base_rotation_in_degrees = 90
    number_of_cycles = 10


@dataclass(frozen=True)
class Point:
    x: float
    y: float

    def __iter__(self):
        yield from (self.x, self.y)

    @classmethod
    def from_turtle(cls, turtle: Turtle):
        return cls(turtle.xcor(), turtle.ycor())

    def goto(self, turtle):
        turtle.goto(self.x, self.y)

    def __sub__(self, other):
        return type(self)(self.x - other.x, self.y - other.y)

class Draw:
    @classmethod
    @contextmanager
    def save_turtle(cls, turtle: Turtle):
        clone: Turtle = turtle.clone()
        clone.speed("fastest")
        clone.hideturtle()
        yield clone

    @classmethod
    def line(cls, turtle: Turtle, A: Point, B: Point):
        with cls.save_turtle(turtle) as line_turtle:
            line_turtle.penup()
            A.goto(line_turtle)
            line_turtle.pendown()
            B.goto(line_turtle)
            line_turtle.penup()


points = {}


def is_square(n):
    return sqrt(n) % 1 == 0


def is_prime(prime):
    if prime < 2:
        return False
    return all(prime % n > 0 for n in range(2, prime))


def on_point(turtle, i):
    """on_point is called on every point along the spiral"""
    point = Point.from_turtle(turtle)
    points[i] = point
    sqrt_lower = points[floor(sqrt(i))]
    sqrt_higher = points[ceil(sqrt(i))]
    delta_sqrt = sqrt(i) % 1
    if delta_sqrt == 0:
        sqrt_point = sqrt_lower
    else:
        # move the point between point at floor and point at ceil a % based on the floating point part of sqrt(i)
        delta_point = sqrt_higher - sqrt_lower
        sqrt_point = Point(
            sqrt_lower.x + delta_point.x * delta_sqrt,
            sqrt_lower.y + delta_point.y * delta_sqrt,
        )
    # turtle.dot()
    # if is_prime(i):
    Draw.line(turtle, point, sqrt_point)


def slide(turtle, stride, i):
    """
    move the turtle in base stride steps forward a stride
    for every point inbetween increment i and call on_point
    return the updated i
    """
    for _ in range(0, stride, Settings.base_stride):
        turtle.forward(Settings.base_stride)
        i += 1
        on_point(turtle, i)
    return i


def cycle(turtle, stride, i):
    "move turtle a single cycle along the spiral"
    i = slide(turtle, Settings.base_stride, i)
    stride += Settings.base_stride
    turtle.left(Settings.base_rotation_in_degrees)
    i = slide(turtle, stride, i)
    turtle.left(Settings.base_rotation_in_degrees)
    stride += Settings.base_stride
    i = slide(turtle, stride, i)
    turtle.left(Settings.base_rotation_in_degrees)
    i = slide(turtle, stride, i)
    turtle.left(Settings.base_rotation_in_degrees)
    i = slide(turtle, stride, i)
    return stride, i


def ulam_spiral():
    stride = 0
    i = Settings.ulam_spiral_start
    turtle.penup()
    on_point(turtle, i)
    for _ in range(Settings.number_of_cycles):
        stride, i = cycle(turtle, stride, i)


def func():
    ulam_spiral()


turtle = Turtle()
turtle.speed("fastest")
screen = Screen()
screen.ontimer(func, 0)
screen.mainloop()
