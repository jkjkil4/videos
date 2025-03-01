# flake8: noqa
from janim.imports import *


class Cursor(boolean_ops.Union):
    def __init__(self, length: float = 1, stroke_alpha=0, fill_alpha=1, **kwargs):
        rect = Rect(0.05, length)
        tip1 = ArrowTip(angle=-PI / 2,
                        center_anchor=CenterAnchor.Back,
                        back_width=DEFAULT_ARROWTIP_BACK_WIDTH * 0.85,
                        body_length=DEFAULT_ARROWTIP_BODY_LENGTH * 0.85)
        tip1.move_anchor_to(length / 2 * UP)
        tip2 = ArrowTip(angle=PI / 2,
                        center_anchor=CenterAnchor.Back,
                        back_width=DEFAULT_ARROWTIP_BACK_WIDTH * 0.85,
                        body_length=DEFAULT_ARROWTIP_BODY_LENGTH * 0.85)
        tip2.move_anchor_to(length / 2 * DOWN)
        super().__init__(
            rect,
            tip1,
            tip2,
            stroke_alpha=stroke_alpha,
            fill_alpha=fill_alpha,
            **kwargs
        )


class Logo(Timeline):
    CONFIG = Config(
        frame_height=int(Config.get.frame_height * 0.25),
        pixel_height=int(Config.get.pixel_height * 0.25)
    )
    def construct(self) -> None:
        FrameRect(stroke_alpha=0, fill_alpha=1, color=BLACK).show()

        circle = Circle(radius=0.15, fill_alpha=1, stroke_alpha=0, color=GREEN).show()

        cursor = Cursor(color=BLUE)
        txt = Text('JAnim', font='LXGW WenKai Lite', font_size=80)

        g = Group(cursor, txt).show()
        g.points.arrange()
        circle.points.move_to(cursor.points.box.top).shift(DR * 0.25)
        self.forward()


if __name__ == '__main__':
    built = Logo().build()
    built.capture(0).save('logo.png')
