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


typ1_src = '''
#set text(font: "LXGW WenKai Lite")
- 使用 anaconda 等工具创建更高版本的虚拟环境（推荐）
- 卸载并安装更高版本（不推荐）
'''


class UpgradeMethods(Template):
    def construct(self) -> None:
        txt = TypstText(typ1_src)
        sur = SurroundingRect(
            txt,
            buff=LARGE_BUFF,
            color=None,
            fill_color=BLACK,
            fill_alpha=0.5,
            stroke_alpha=0,
            depth=1
        )

        self.show(sur)
        self.play(Write(txt), FadeIn(sur, duration=0.3))
        self.forward(2)


class CreateWindowParams(Template):
    def construct(self) -> None:
        window = ImageItem('window-col.png', height=5).show()
        width = window.points.box.width
        height = window.points.box.height
        woffset = RIGHT * width / 2
        hoffset = DOWN * (height / 2 - 0.18)

        hline = Group(
            g := Group(
                Line(-woffset + DOWN * 0.2, -woffset + UP * 0.2),
                DoubleArrow(-woffset, woffset),
                Line(woffset + DOWN * 0.2, woffset + UP * 0.2)
            ),
            Text('800').points.next_to(g[1], UP, buff=SMALL_BUFF).r
        )
        hline.points.next_to(window, UP, buff=SMALL_BUFF)

        vline = Group(
            g := Group(
                Line(-hoffset + LEFT * 0.2, -hoffset + RIGHT * 0.2),
                DoubleArrow(-hoffset, hoffset),
                Line(hoffset + LEFT * 0.2, hoffset + RIGHT * 0.2)
            ),
            Text('600').points.rotate(PI / 2).next_to(g[1], LEFT, buff=SMALL_BUFF).r
        )
        vline.points.next_to(window, LEFT, buff=SMALL_BUFF, aligned_edge=DOWN)

        rect = Rect(1.2, 0.5, color=YELLOW)
        rect.points.shift(LEFT * 2.5 + UP * 2.35)

        def growline(line):
            direction = normalize(line[0][1].points.start_direction)
            return AnimGroup(
                GrowDoubleArrow(line[0][1]),
                FadeIn(line[0][0], -direction, at=0.3, duration=0.7),
                FadeIn(line[0][2], direction, at=0.3, duration=0.7),
                Write(line[1], at=0.2, duration=0.8)
            )

        self.play(FadeIn(window, scale=1.2))
        self.forward()
        self.play(
            growline(hline),
            growline(vline),
            lag_ratio=0.5
        )
        self.forward()
        self.play(
            ShowCreationThenFadeOut(
                rect,
                create_kwargs=dict(
                    auto_close_path=False
                )
            )
        )
        self.forward()


code1_template = '<fc #9cdcfe>ctx</fc><fc #cccccc>.</fc><fc #9cdcfe>viewport</fc>' \
                 ' <fc #d4d4d4>=</fc><fc #cccccc> ' \
                 '(</fc><fc #b5cea8>{:<3.0f}</fc><fc #cccccc>, </fc><fc #b5cea8>{:<3.0f}</fc><fc #cccccc>, </fc><fc #b5cea8>{:<3.0f}</fc><fc #cccccc>, </fc><fc #b5cea8>{:<3.0f}</fc><fc #cccccc>)</fc>'

code1_src = code1_template.format(0, 0, 800, 600)

class Viewport(Template):
    def construct(self) -> None:
        #########################################################

        title = Title('Viewport').show()

        window = ImageItem('window-col.png', width=6.5)
        window.points.shift(LEFT * 2.5)

        content = ImageItem('window-content.png', width=6.5)
        content.points.next_to(window.points.box.bottom, UP, buff=0)

        content_rect = Rect(content.points.box.get(DL), content.points.box.get(UR))

        code1 = Text(code1_src, format=Text.Format.RichText)
        code1.points.scale(0.8).next_to(content, aligned_edge=UP)

        udl1 = Underline(code1[0][16:25], color=BLUE)
        udl1.points.close_path()
        udl2 = Underline(code1[0][26:34], color=GREEN)

        dl = Circle(
            0.1,
            fill_alpha=1,
            fill_color=BLACK,
            stroke_color=BLUE,
            depth=-1
        )

        wline = Line(color=GREEN, stroke_radius=0.05)
        hline = Line(DOWN, UP, color=GREEN, stroke_radius=0.05)

        xtracker = ValueTracker(0)
        ytracker = ValueTracker(0)
        wtracker = ValueTracker(800)
        htracker = ValueTracker(600)

        def code_updater(p: UpdaterParams) -> Text:
            txt = Text(
                code1_template.format(xtracker.current().data.get(),
                                      ytracker.current().data.get(),
                                      wtracker.current().data.get(),
                                      htracker.current().data.get()),
                format=Text.Format.RichText
            )
            txt.points.replace(code1)
            return txt

        def content_updater(data: ImageItem, p: UpdaterParams):
            box = content_rect.points.box
            data.points.set_size(
                box.width * wtracker.current().data.get() / 800,
                box.height * htracker.current().data.get() / 600
            )
            xoffset = box.width * xtracker.current().data.get() / 800
            yoffset = box.height * ytracker.current().data.get() / 600
            data.points.next_to(box.get(DL) + RIGHT * xoffset + UP * yoffset, UR, buff=0)

        def dl_updater(data: Circle, p: UpdaterParams):
            data.points.move_to(content.current().points.box.get(DL))

        def wline_updater(data: Line, p: UpdaterParams):
            box = content.current().points.box
            data.points.set_width(box.width - 0.2)
            data.points.next_to(box.get(DR), DOWN, buff=0, aligned_edge=RIGHT)

        def hline_updater(data: Line, p: UpdaterParams):
            box = content.current().points.box
            data.points.set_height(box.height - 0.2)
            data.points.next_to(box.get(UL), LEFT, buff=0, aligned_edge=UP)

        dl_updater(dl, None)
        wline_updater(wline, None)
        hline_updater(hline, None)

        #########################################################

        window.show()

        self.forward()
        t = self.aas('24.mp3', '在我们开始渲染之前还有一件重要的事情要做')
        self.forward_to(t.end + 0.6)
        t = self.aas('25.mp3', '我们必须告诉 OpenGL 渲染区域的尺寸大小')

        self.prepare(
            FadeIn(content),
            at=2
        )

        self.forward_to(t.end + 0.4)
        t = self.aas('26.mp3', '即视口（Viewport）')

        self.prepare(FadeIn(code1), duration=t.duration)

        self.forward_to(t.end + 0.5)
        t = self.aas('27.mp3', '这样 OpenGL 才只能知道怎样根据窗口大小显示数据和坐标')
        self.forward_to(t.end + 0.7)
        t = self.aas('28.mp3', '在这四个参数中')

        self.prepare(
            ShowCreationThenDestruction(
                Underline(code1[0][16:34], color=YELLOW)
            )
        )

        self.forward_to(t.end + 0.4)
        t = self.aas('29.mp3', '前两个参数控制视口左下角的位置')

        self.play(
            Succession(
                Create(udl1),
                Transform(
                    udl1, dl,
                    hide_src=False,
                    path_arc=-PI / 2,
                    duration=1.3
                ),
                Wait(0.5),
                AnimGroup(*[
                    CircleIndicate(
                        item,
                        scale=2,
                        rate_func=there_and_back_with_pause,
                        duration=1.6
                    )
                    for item in [dl, code1[0][16:25]]
                ])
            )
        )

        # self.forward_to(t.end + 0.4)
        self.forward(0.6)

        t = self.aas('30.mp3', '第三个和第四个参数控制渲染视口的宽度和高度（像素）')

        self.prepare(
            Succession(
                Create(udl2),
                Wait(0.9),
                Transform(udl2, wline, hide_src=False),
                Transform(udl2, hline, hide_src=False)
            )
        )

        self.forward_to(t.end + 0.8)

        t = self.aas('30_2.mp3', '我们看看调整这些数值会有怎样的效果')
        self.forward_to(t.end + 0.8)

        def updater_anims():
            return AnimGroup(
                ItemUpdater(
                    code1,
                    code_updater,
                    show_at_end=False
                ),
                DataUpdater(
                    content,
                    content_updater
                ),
                DataUpdater(
                    dl,
                    dl_updater
                ),
                DataUpdater(
                    wline,
                    wline_updater
                ),
                DataUpdater(
                    hline,
                    hline_updater
                )
            )

        self.play(
            Aligned(
                Succession(
                    wtracker.anim.data.set(600),
                    htracker.anim.data.set(450),
                    AnimGroup(
                        xtracker.anim.data.set(100),
                        ytracker.anim.data.set(50)
                    )
                ),
                updater_anims()
            )
        )
        code1 = code_updater(None).show()

        self.forward()

        t = self.aas('31.mp3', '（如果）我们将视口的大小设置得比 GLFW 窗口的小')
        self.forward_to(t.end + 0.4)
        t = self.aas('32.mp3', '这样子之后所有的 OpenGL 渲染将会在一个更小的区域中显示')

        inrect = Rect(
            stroke_alpha=0,
            fill_color=YELLOW,
            fill_alpha=0.6,
            depth=-2
        )
        inrect.points.replace(content, stretch=True)

        exrect = boolean_ops.Difference(
            content_rect,
            inrect,
            stroke_alpha=0,
            fill_color=YELLOW,
            fill_alpha=0.6,
            depth=-2
        )

        self.prepare(
            FadeIn(
                inrect,
                show_at_end=False,
                rate_func=there_and_back_with_pause,
                duration=2,
            ),
            at=2.7
        )

        self.forward_to(t.end + 0.8)
        t = self.aas('33.mp3', '这样子的话我们也可以将一些其它元素显示在 OpenGL 视口之外')

        self.prepare(
            FadeIn(
                exrect,
                show_at_end=False,
                rate_func=there_and_back_with_pause,
                duration=3,
            ),
            at=1.5
        )

        self.forward_to(t.end + 1)
        t = self.aas('34.mp3', '一般来说我们设置成全范围就好了')

        self.play(
            Aligned(
                AnimGroup(
                    wtracker.anim.data.set(800),
                    htracker.anim.data.set(600),
                    xtracker.anim.data.set(0),
                    ytracker.anim.data.set(0),
                ),
                updater_anims()
            ),
            at=1.2
        )
        code1 = code_updater(None).show()

        self.forward_to(t.end + 2)
