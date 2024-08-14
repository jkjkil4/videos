# flake8: noqa
import random
import sys

sys.path.append('.')

from janim.imports import *

from utils.template import *


class TrafficTemplate(Template):
    CONFIG = Config(
        background_color=Color('#FFEAC7'),
        preview_fps=15
    )


class Road(Group):
    def __init__(
        self,
        width: float,
        height: float | None = None,
        lanes: int = 2,
        ticks: int | None = None,
        depth: float = 100,
        **kwargs
    ):
        xr = width / 2
        if height is None:
            height = lanes
        if ticks is None:
            ticks = math.ceil(width * 1.4)

        line = Line(LEFT * xr,RIGHT * xr)

        dashed_line = Group(*[
            Line(RIGHT * l, RIGHT * r)
            for l, r in np.linspace(-xr, xr, ticks).reshape((-1, 2))
        ])

        dashed_lines = []
        if lanes == 2:
            dashed_lines = [dashed_line]
        elif lanes > 2:
            dashed_lines = dashed_line * (lanes - 1)

        lines = Group(
            line,
            *dashed_lines,
            line.copy()
        )
        lines.points.arrange(DOWN).set_height(height, stretch=True)

        super().__init__(
            Rect(
                width, height,
                stroke_alpha=0,
                fill_alpha=1,
                fill_color=GREY_D
            ),
            lines,
            depth=depth,
            **kwargs
        )


class Car(SVGItem):
    def __init__(self, height=1, **kwargs):
        super().__init__('car.svg', height=height, **kwargs)


class Tree(SVGItem):
    def __init__(self, height=2, **kwargs):
        super().__init__('行道树.svg', height=height, **kwargs)


class SyncTraffic(TrafficTemplate):
    def construct(self) -> None:
        #########################################################

        road = Road(Config.get.frame_width * 5, lanes=1).show()
        road.points.to_border(LEFT, buff=0)

        tree = Tree()
        tree.points.shift(UP * 2)

        random.seed(114514)
        trees = tree * 10
        trees.show()
        trees.points.arrange(buff=2, center=False).shift(LEFT * 7)
        for tree in trees:
            tree.points.scale(0.7 + 0.3 * random.random(), about_edge=DOWN)

        car = Car()
        car.points.shift(UP * 0.3)

        cars = car * 5
        cars.show()
        cars.points.arrange(buff=1.5, center=False).shift(LEFT * 21)

        dog = SVGItem('dog.svg', height=0.6)
        dog.points.shift(RIGHT * 28 + UP * 0.2)

        #########################################################

        def combine_rush_into_and_linear(t: float, slope: float) -> float:
            return (1 - t) * rush_into(t) + t * linear((t - 1) * slope + 1)

        def combine_linear_and_rush_from(t: float, slope: float) -> float:
            return (1 - t) * linear(t * slope) + t * rush_from(t)

        self.forward()
        self.play(
            cars.anim(rate_func=linear)
                .points.shift(RIGHT * 10),
            duration=2
        )
        self.play(
            cars.anim(rate_func=linear)
                .points.shift(RIGHT * 5),
            self.camera.anim(rate_func=partial(combine_rush_into_and_linear, slope=5/9))
                .points.shift(RIGHT * 9),
            duration=1
        )
        self.prepare(
            FadeIn(dog, DOWN),
            at=2.5
        )
        self.play(
            cars.anim(rate_func=linear)
                .points.shift(RIGHT * 15),
            self.camera.anim(rate_func=linear)
                .points.shift(RIGHT * 15),
            duration=3
        )
        self.play(
            cars.anim(rate_func=partial(combine_linear_and_rush_from, slope=4/5))
                .points.shift(RIGHT * 4)
        )
        self.play(FadeOut(dog, DOWN))
        self.play(
            cars.anim(rate_func=partial(combine_rush_into_and_linear, slope=4/5))
                .points.shift(RIGHT * 4)
        )
        self.play(
            cars.anim(rate_func=linear)
                .points.shift(RIGHT * 15),
            duration=3
        )
        self.forward()


class RealTraffic(TrafficTemplate):
    def construct(self) -> None:
        self.camera.points.scale(1.5)
        # self.camera.points.scale(4).shift(LEFT * 16)
        #########################################################

        road = Road(Config.get.frame_width * 5, lanes=1).show()
        road.points.to_border(RIGHT, buff=0).shift(RIGHT * 6)

        tree = Tree()
        tree.points.shift(UP * 2)

        random.seed(114514)
        trees = tree * 14
        trees.show()
        trees.points.arrange(LEFT, buff=2, center=False).shift(RIGHT * 10)
        for tree in trees:
            tree.points.scale(0.7 + 0.3 * random.random(), about_edge=DOWN)

        car = Car()
        car.points.shift(UP * 0.3)

        cars = car * 30
        cars.show()
        cars.points.arrange(LEFT, buff=1.5, center=False).shift(RIGHT * 5)

        normal_cars = cars[:4]
        normal_cars.depth.arrange(-2)
        brake_cars = cars[4:]
        brake_cars.depth.arrange(-1)
        speed = 5

        def s_func(brake_at: float, brake_slope: float, run_at: float, run_slope: float) -> Callable[[float], float]:
            brake_t = speed / brake_slope
            run_t = speed / run_slope

            if brake_at + brake_t <= run_at:
                def s(t: float) -> float:
                    if t < brake_at:
                        return t * speed
                    if t < brake_at + brake_t:
                        return t * speed - brake_slope * (t - brake_at)**2 / 2
                    dst1 = (brake_at + brake_t / 2) * speed
                    if t < run_at:
                        return dst1
                    full_speed_t = run_at + run_t
                    if t < full_speed_t:
                        return dst1 + run_slope * (t - run_at)**2 / 2
                    return dst1 + (t - full_speed_t + run_t / 2) * speed

                return s

            else:
                minimum_v = speed - (run_at - brake_at) * brake_slope
                run_t = (speed - minimum_v) / run_slope

                def s(t: float) -> float:
                    if t < brake_at:
                        return t * speed
                    if t < run_at:
                        return t * speed - brake_slope * (t - brake_at)**2 / 2
                    dst1 = brake_at * speed + (run_at - brake_at) * (speed + minimum_v) / 2
                    if t < run_at + run_t:
                        return dst1 + minimum_v * (t - run_at) + run_slope * (t - run_at)**2 / 2
                    dst2 = dst1 + run_t * (speed + minimum_v) / 2
                    return dst2 + (t - (run_at + run_t)) * speed

                return s

        dog = SVGItem('dog.svg', height=0.6).show()
        dog.depth.arrange(-1.5)
        dog.points.shift(RIGHT * 0.2 + UP * 0.2 + UP * 0.8)

        #########################################################

        for car in normal_cars:
            self.prepare(
                car.anim(rate_func=linear)
                    .points.shift(RIGHT * 5 * speed),
                duration=5
            )

        for i, car in enumerate(brake_cars):
            alpha = (i / len(brake_cars))**2 * len(brake_cars)
            s = s_func(1 + 0.25 * i,
                       2.5 + 0.25 * alpha,
                       2 + 0.4 * i,
                       1 + 0.7 * alpha)
            def updater(car: Car, p: UpdaterParams, s=s):
                car.points.shift(RIGHT * s(p.global_t - p.range.at))
            self.prepare(
                GroupUpdater(
                    car,
                    updater,
                    rate_func=linear,
                    duration=11
                )
            )

        self.prepare(
            dog.anim(rate_func=rush_from)
                .points.shift(DOWN * 1.6 + RIGHT),
            at=1,
            duration=1
        )

        self.prepare(
            self.camera.anim
                .points.scale(4 / 1.5).shift(LEFT * 16),
            at=3,
            duration=3
        )

        self.forward(11)

