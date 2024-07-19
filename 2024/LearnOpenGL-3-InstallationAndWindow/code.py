# flake8: noqa
import random
import sys

sys.path.append('.')

from janim.imports import *

from utils.template import *


class TitleTl(TitleTemplate):
    str1 = 'Learn OpenGL'
    str2 = '安装与创建窗口'


class ModernGLAndGLFW(SubtitleTemplate2):
    name = 'moderngl 与 GLFW'

    def construct(self) -> None:
        #########################################################

        py = ImageItem('python.png', height=4, alpha=0.2)
        py.points.shift(RIGHT * 3)

        opengl = ImageItem('opengl.png', height=1)
        opengl.points.shift(LEFT * 2)

        pyopengl = Text('PyOpenGL')
        pyopengl.points.shift(RIGHT * 2 + UP)

        moderngl = Group(
            ImageItem('moderngl.png', height=1),
            Text('moderngl', font_size=12)
        )
        moderngl.points.arrange(DOWN, buff=SMALL_BUFF).shift(RIGHT * 2 + DOWN)

        arrow1 = Arrow(opengl, pyopengl)
        txt1 = arrow1.create_text('C 绑定', font_size=20)

        arrow2 = Arrow(opengl, moderngl)
        txt2 = arrow2.create_text('封装', font_size=20, under=True)

        #########################################################

        self.prepare(
            FadeIn(py),
            at=1
        )
        super().construct()

        self.play(self.title.txt[0][:8](VItem).anim.color.set(YELLOW))

        t = self.aas('1.mp3', 'moderngl 是在 Python 中对 OpenGL 的封装')

        self.prepare(
            Succession(
                FadeIn(opengl, scale=1.2),
                FadeIn(moderngl, scale=1.2),
                GrowArrow(arrow2)
            )
        )

        self.forward_to(t.end + 0.5)
        t = self.aas('2.mp3', '他与另一个 Python 库 PyOpenGL 不同的是')

        self.play(
            Succession(
                FadeIn(pyopengl, scale=1.2),
                GrowArrow(arrow1)
            ),
            at=0.7
        )

        self.forward_to(t.end + 0.3)
        t = self.aas('3.mp3', 'PyOpenGL 仅仅是对 C 中的 OpenGL 函数的绑定')

        self.prepare(
            Write(txt1),
            at=2.5
        )

        self.forward_to(t.end + 0.5)
        t = self.aas('4.mp3', '而 moderngl 做了许多易用的封装')

        self.prepare(
            Write(txt2),
            at=1.5
        )

        self.forward_to(t.end + 0.3)
        t = self.aas('5.mp3', '使其更符合 Python 中的使用习惯')

        self.prepare(
            FocusOn(moderngl)
        )

        self.forward_to(t.end)

        random.seed(1145140)
        self.play(
            FadeOut(
                Group(opengl, arrow1, arrow2, txt1, txt2, pyopengl, moderngl, py)
                .shuffle(),
                lag_ratio=0.1,
                duration=1.5
            ),
            self.title.txt[0][:8](VItem).anim.color.set(WHITE),
            self.title.txt[0][11:](VItem).anim(at=0.5, duration=1).color.set(YELLOW),
        )
        self.forward(0.8)

        #########################################################

        window = ImageItem('window-col.png', height=5)

        windows = SVGItem('windows.svg', height=1)
        apple = SVGItem('apple-fill.svg', height=1)
        linux = SVGItem('linux.svg', height=1)

        systems = Group(windows, apple, linux)
        systems.points.arrange(buff=MED_LARGE_BUFF)

        txt1 = Text('创建窗口')
        txt2 = Text('处理用户输入')
        txts = Group(txt1, txt2)
        txts.points.arrange(buff=LARGE_BUFF)

        sur = SurroundingRect(txts, buff=0.3, color=GREY)

        glfw = Text('GLFW', font_size=30)
        glfw.points.next_to(sur, UP)

        #########################################################

        t = self.aas('6.mp3', '在我们画出出色的效果之前，首先肯定得创建一个窗口')

        self.schedule(self.current_time + 3.8, window.show)

        self.forward_to(t.end + 0.3)
        t = self.aas('7.mp3', '这样才能方便看到渲染结果对吧！')
        self.forward_to(t.end + 0.8)
        t = self.aas('8.mp3', '然而，这在每个操作系统上都是不一样的')

        self.prepare(
            *[
                FadeIn(s, scale=0.7, about_point=ORIGIN, rate_func=linear)
                for s in systems
            ],
            lag_ratio=0.2,
            duration=2,
            rate_func=smooth
        )

        self.forward_to(t.end + 0.5)
        t = self.aas('9.mp3', 'OpenGL 有意的将这些操作抽象（Abstract）出去')
        self.forward_to(t.end + 0.4)
        t = self.aas('10.mp3', '这意味着我们不得不自己处理创建窗口')

        self.prepare(
            FadeOut(Group(window, windows, apple, linux)),
            Write(txt1, at=1.7)
        )

        self.forward_to(t.end + 0.3)
        t = self.aas('11.mp3', '以及处理用户输入')

        self.prepare(
            Write(txt2),
            at=0.3
        )

        self.forward_to(t.end + 0.6)
        t = self.aas('12.mp3', '幸运的是，有一些库已经提供了我们所需的功能')
        self.forward_to(t.end + 0.3)
        t = self.aas('13.mp3', '其中一部分是特别针对 OpenGL 的')

        self.prepare(
            Create(
                sur,
                auto_close_path=False,
                duration=6,
                rate_func=rush_from
            )
        )

        self.forward_to(t.end + 0.5)
        t = self.aas('14.mp3', '这些库节省了我们书写操作系统相关代码的时间')
        self.forward_to(t.end + 0.3)
        t = self.aas('15.mp3', '提供给我们一个窗口用来渲染')
        self.forward_to(t.end + 0.8)
        t = self.aas('16.mp3', '在这里我们使用的是 GLFW')

        self.prepare(
            Transform(
                self.title.txt[0][11:],
                Group(*glfw[0]),
                hide_src=False
            ),
            at=1.5
        )

        self.forward_to(t.end + 0.8)

        #########################################################

        txtsur = Group(txts, sur)

        modules = Group(*[
            Text(s)
            for s in [
                'pyglet',
                'pygame',
                'pyside6',
                'moderngl-window'
            ]
        ])
        modules.points.arrange(DOWN).next_to(glfw, DOWN)

        #########################################################

        t = self.aas('17.mp3', '当然，学习完 OpenGL 后')
        self.forward_to(t.end + 0.4)
        t = self.aas('18.mp3', '你也可以尝试用其它的库来创建窗口')

        self.prepare(
            FadeOut(txtsur),
            at=0.5
        )

        self.forward_to(t.end + 0.5)
        t = self.aas('19.mp3', '比如在 Python 中常见的有这几个界面库')

        self.play(
            Write(modules[:-1]),
            at=1
        )

        self.forward_to(t.end + 0.4)
        t = self.aas('20.mp3', '并且 moderngl 自己也做了一个叫作 moderngl-window 的扩展库')

        self.play(
            Write(modules[-1]),
            at=2
        )

        self.forward_to(t.end + 0.5)

        random.seed(11451400)
        self.play(
            FadeOut(
                Group(glfw, *modules).shuffle(),
                lag_ratio=0.1
            ),
            self.title.txt[0][11:](VItem).anim.color.set(WHITE)
        )

        #########################################################

        txt_mgl = Text('moderngl')
        txt_glfw = Text('GLFW')
        txts = Group(txt_mgl, txt_glfw)
        txts.points.arrange(RIGHT, buff=LARGE_BUFF)

        #########################################################

        t = self.aas('21.mp3', '总而言之')
        self.forward_to(t.end + 0.4)
        t = self.aas('22.mp3', '我们将使用 moderngl 来创建与使用 OpenGL 上下文')

        self.prepare(Write(txt_mgl), at=1)

        self.forward_to(t.end + 0.4)
        t = self.aas('23.mp3', '并且使用 GLFW 创建窗口进行显示')

        self.prepare(Write(txt_glfw), at=1)

        self.forward_to(t.end + 1)