# flake8: noqa
import random
import sys

sys.path.append('.')

from janim.imports import *

from utils.template import *


class TitleTl(TitleTemplate):
    str1 = 'Learn OpenGL'
    str2 = '处理输入与背景颜色'


class GetKey_Subtitle(SubtitleTemplate):
    name = '处理输入'


class GetKey(Template):
    def construct(self) -> None:
        #########################################################

        keyboard = SVGItem('keyboard.svg', height=1)
        keyboard.points.shift(LEFT)
        mouse = SVGItem('mouse.svg', height=1.2)
        mouse.points.shift(RIGHT * 1.6 + UP * 0.1)

        funcs = Group(*[
            Text(
                f'<fc #4ec9b0>glfw</fc><fc #cccccc>.</fc><fc #dcdcaa>{s}</fc>',
                format=Text.Format.RichText
            )
            for s in [
                'get_key',
                'get_mouse_button',
                'set_key_callback',
                'set_mouse_button_callback',
                'get_gamepad_state'
            ]
        ])

        random.seed(1145140000)
        for func in funcs:
            func.points.rotate(random.random() * PI * 0.4 - PI * 0.2)
            func.points.shift(
                (random.random() * 2 - 1) * RIGHT +
                (random.random() * 2 - 1) * UP
            )

        getkey = Text(
            '<fc #4ec9b0>glfw</fc><fc #cccccc>.</fc><fc #dcdcaa>get_key</fc><fc #cccccc>(</fc><fc #9cdcfe>window</fc><fc #cccccc>, </fc><fc #9cdcfe>key</fc><fc #cccccc>)</fc>',
            format=Text.Format.RichText,
            font_size=30
        )
        getkey_name = getkey[0][:12]
        getkey_args = getkey[0][12:]

        #########################################################

        self.forward()
        t = self.aas('1.mp3', '我们同样希望能够在 GLFW 中实现一些输入控制')

        self.prepare(
            FadeIn(keyboard),
            FadeIn(mouse),
            lag_ratio=0.5,
            at=2
        )

        self.forward_to(t.end + 0.5)
        t = self.aas('2.mp3', '这可以通过使用 GLFW 的几个输入函数来完成')

        self.prepare(
            AnimGroup(
                keyboard(VItem).anim.color.fade(0.5),
                mouse(VItem).anim.color.fade(0.5),
            ),
            AnimGroup(
                *[
                    FadeIn(func, scale=0.8)
                    for func in funcs
                ],
                lag_ratio=0.7,
                duration=2.5
            ),
            at=1,
            lag_ratio=1
        )

        self.forward_to(t.end + 0.7)
        t = self.aas('3.mp3', '我们用到 glfw.get_key 函数')

        self.prepare(
            funcs[1:](VItem).anim.color.fade(0.7)
        )

        self.forward_to(t.end)

        self.play(
            Transform(funcs[0][0][:], getkey_name),
            AnimGroup(
                *map(FadeOut, (keyboard, mouse, funcs[1:])),
                duration=0.5
            )
        )

        t = self.aas('4.mp3', '它需要一个窗口以及一个按键作为输入')

        self.prepare(
            Write(getkey_args),
            duration=2.2
        )

        self.forward_to(t.end + 0.5)
        t = self.aas('5.mp3', '我们可以通过这个函数检查特定的按键是否按下')

        self.prepare(
            Indicate(getkey_args[9:12]),
            at=2
        )

        self.forward_to(t.end + 1)


class PressKey(Template):
    def construct(self) -> None:
        #########################################################

        arrow = Arrow(ORIGIN, RIGHT * 0.8, max_length_to_tip_length_ratio=0.6)

        txt1 = Text('返回值 <c RED>glfw.RELEASE</c>', format=Text.Format.RichText)
        txt2 = Text('返回值 <c GREEN>glfw.PRESS</c>', format=Text.Format.RichText)

        for txt in (txt1, txt2):
            txt.points.next_to(arrow)

        btn_line = Line(LEFT * 0.5, RIGHT * 0.5)
        btn_black = Rect(1, 1, color=BLACK, fill_alpha=1, depth=1)
        btn_black.points.next_to(btn_line, DOWN, buff=0)
        btn_body = Rect(0.5, 0.2, fill_color=GREY, fill_alpha=1, depth=2)
        btn_body.points.next_to(btn_line, UP, buff=0)
        btn_txt = Text('ESC', font_size=20)
        btn_txt.points.next_to(btn_line, DOWN, buff=SMALL_BUFF)

        btn = Group(btn_line, btn_black, btn_body, btn_txt)

        def btn_press(**kwargs) -> MethodTransform:
            return btn_body.anim(**kwargs).points.next_to(btn_line, DOWN, buff=0)

        def btn_release(**kwargs) -> MethodTransform:
            return btn_body.anim(**kwargs).points.next_to(btn_line, UP, buff=0)

        Group(
            btn,
            Group(arrow, txt1, txt2)
        ).points.arrange(DOWN, aligned_edge=LEFT)

        finger = SVGItem('finger.svg', color=WHITE, height=0.8)
        finger.points.rotate(-100 * DEGREES).shift(LEFT * 2.1 + UP * 1.2)

        self.show(arrow, txt1, btn, finger)

        #########################################################

        self.forward()

        t = self.aas('6.mp3', '此时，如果我们没有按下')
        self.forward_to(t.end + 0.4)
        t = self.aas('7.mp3', 'glfw.get_key 会返回 glfw.RELEASE')

        self.prepare(
            ShowPassingFlashAround(txt1[0][4:]),
            at=1
        )

        self.forward_to(t.end + 0.5)
        t = self.aas('8.mp3', '不会命中这个条件判断')
        self.forward_to(t.end + 0.8)
        t = self.aas('9.mp3', '如果我们按下了 ESC 键')

        self.play(
            finger.anim.points.shift(DOWN * 0.3).rotate(-30 * DEGREES),
            btn_press(at=0.5, duration=0.5, rate_func=rush_from)
        )
        txt1.hide()
        txt2.show()

        self.forward_to(t.end + 0.4)
        t = self.aas('10.mp3', 'glfw.get_key 就会返回 glfw.PRESS', mul=1.4)

        self.prepare(
            ShowPassingFlashAround(txt2[0][4:]),
            at=0.5
        )

        self.forward_to(t.end + 1)


class CtxClear(Template):
    def construct(self) -> None:
        #########################################################

        FrameRect(
            stroke_alpha=0,
            fill_alpha=0.5,
            color=BLACK
        ).show()

        rgb_bar = Group(
            *(
                Group(
                    Rect(0.2, 1, stroke_alpha=0, fill_alpha=1)
                        .points.set_height(0, stretch=True, about_edge=DOWN)
                        .r,
                    Rect(0.2, 1, stroke_radius=0.01, depth=-1)
                ) * 3
            ),
            Text('R', color=RED),
            Text('G', color=GREEN),
            Text('B', color=BLUE),
        )

        for i in range(3):
            c = [0, 0, 0]
            c[i] = 1
            rgb_bar[i][0].color.set(c)

        rgb_bar.points.arrange_in_grid(
            n_cols=3,
            h_buff=0.3,
            v_buff=0.7,
            by_center_point=True
        )

        arrow = Arrow()

        col = Square(1.3, fill_color=[0, 1, 0], fill_alpha=1)

        g = Group(rgb_bar, arrow, col)
        g.points.arrange()

        #########################################################

        self.forward()
        t = self.aas('11.mp3', '简单来说，我们可以给这个函数传入 0~1 之间的 <c RED>R</c><c GREEN>G</c><c BLUE>B</c> 颜色分量',
                     format=Text.Format.RichText)

        self.prepare(
            Write(rgb_bar),
            at=4
        )

        self.forward_to(t.end + 0.6)
        t = self.aas('12.mp3', '比如 (<c RED>0.0</c>, <c GREEN>1.0</c>, <c BLUE>0.0</c>) 就是完全只有绿色分量',
                     format=Text.Format.RichText)

        self.prepare(
            rgb_bar[1][0].anim.points.set_height(1, stretch=True, about_edge=DOWN),
            at=0.5
        )

        self.forward_to(t.end)

        self.prepare(GrowArrow(arrow))
        self.forward(0.5)

        t = self.aas('13.mp3', '表现为纯绿色')

        self.prepare(FadeIn(col, scale=1.2, rate_func=rush_from))

        self.forward_to(t.end + 0.6)
        t = self.aas('14.mp3', '在这里我们写上 (<c RED>0.2</c>, <c GREEN>0.3</c>, <c BLUE>0.3</c>) 这个颜色',
                     format=Text.Format.RichText)

        self.prepare(
            rgb_bar[0][0].anim.points.set_height(0.2, stretch=True, about_edge=DOWN),
            rgb_bar[1][0].anim.points.set_height(0.3, stretch=True, about_edge=DOWN),
            rgb_bar[2][0].anim.points.set_height(0.3, stretch=True, about_edge=DOWN),
            col.anim.fill.set([0.2, 0.3, 0.3]),
            at=1.5,
            duration=2
        )

        self.forward_to(t.end + 1)


class Highlight(Template):
    def construct(self) -> None:
        # path = r'C:\Users\jkjki\AppData\Roaming\PotPlayerMini64\Capture\2024-07-27 10-53-52.mp4_20240727_111624.743.jpg'
        # img = ImageItem(path).show()

        kwargs = dict(
            color=YELLOW
        )

        rect = Rect(4.4, 0.9, **kwargs)
        rect.points.shift(LEFT * 1.5 + DOWN * 0.2)

        line = Line(LEFT * 3.6, ORIGIN, **kwargs)
        line.points.shift(RIGHT * 0.6 + DOWN * 0.1)

        self.play(Create(rect, auto_close_path=False))
        self.forward()
        self.play(Create(line, auto_close_path=False))
        self.forward()
