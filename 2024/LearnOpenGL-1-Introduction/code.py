# flake8: noqa

import random
import sys

sys.path.append('.')

from janim.imports import *

from utils.template import *


class CPU(Group):
    def __init__(self, **kwargs):
        self.outer = Square(fill_color=BLACK, fill_alpha=1)
        self.inner = Square(color=GREY).points.scale(0.9).r
        self.text = Text('CPU')
        super().__init__(self.outer, self.inner, self.text, **kwargs)


class GPU(Group):
    def __init__(self, **kwargs):
        self.outer = Rect(3, 2, color=ORANGE, fill_color=BLACK, fill_alpha=1)
        self.inner = Rect(2.8, 1.8, color='#f79655')
        self.text = Text('GPU', color=ORANGE)
        super().__init__(self.outer, self.inner, self.text, **kwargs)


class VCross(VItem):
    def __init__(self, color=RED, fill_alpha=1, stroke_alpha=0, **kwargs):
        super().__init__(
            color=color,
            fill_alpha=fill_alpha,
            stroke_alpha=stroke_alpha,
            **kwargs
        )

        self.points.set_as_corners([
            UP * 0.5, UP * 0.5 + UR, RIGHT * 0.5 + UR, RIGHT * 0.5,
            RIGHT * 0.5 + DR, DOWN * 0.5 + DR, DOWN * 0.5,
            DOWN * 0.5 + DL, LEFT * 0.5 + DL, LEFT * 0.5,
            LEFT * 0.5 + UL, UP * 0.5 + UL, UP * 0.5
        ])
        self.points.scale(0.15).move_to(ORIGIN)


class Voice(Audio):
    def __init__(self, filepath: str, *args, **kwargs):
        super().__init__(filepath, *args, **kwargs)
        self.mul(2)


class Code(Group):
    def __init__(self, richtext: str, **kwargs):
        txt = Text(richtext, format=Text.Format.RichText, **kwargs)
        rect = Rect()
        super().__init__(txt, rect)


opening_typ = '''
#set par(first-line-indent: 2em, justify: true)
#set text(font: "Noto Sans S Chinese", fill: luma(70%))
#set page(width: 40em, height: auto)

= 写在前面
#fake-par
原 Learn-OpenGL 教程在 C++ 中进行 OpenGL 开发教学，本教程使用 Python 的 ModernGL 进行教学，
因为我认为这样更好地理解 OpenGL 的运作机制，而不用关心一些繁琐的步骤。
'''


class Opening(Template):
    def construct(self) -> None:
        txt = TypstDoc(opening_typ).show()
        txt.points.to_center()
        self.forward(3)


class Title(TitleTemplate):
    str1 = 'Learn OpenGL'
    str2 = '基本介绍'


class Subtitle_WhatIsOpenGL(SubtitleTemplate):
    name = '什么是 OpenGL'


class WhatIsOpenGL(Template):
    def construct(self) -> None:
        txt1 = Text("OpenGL", font_size=80)
        txt2 = Text(
            "Open G<c GREY>raphics</c> L<c GREY>ibrary</c>",
            font_size=60,
            format=Text.Format.RichText
        )

        self.forward()

        t = self.play_audio(
            Voice('1.mp3'),
            begin=1.4,
            end=3
        )
        self.subtitle('OpenGL 全称', t)

        self.play(DrawBorderThenFill(txt1), duration=t.duration)

        t = self.play_audio(
            Voice('2.mp3'),
            begin=0.8,
            end=3
        )

        self.play(
            Transform(txt1[0][:4], txt2[0][:4]),
            Transform(Group(txt1[0][4]), txt2[0][5:13]),
            Transform(Group(txt1[0][5]), txt2[0][14:21]),
            duration=2
        )
        self.forward()
        self.play(Uncreate(txt2, lag_ratio=0.4), duration=0.6)

        t = self.play_audio(
            Voice('3.mp3'),
            begin=1.8,
            end=3.2
        )
        self.subtitle('它是用来做什么的呢？', t)
        self.forward_to(t.end + 0.7)

        t = self.play_audio(
            Voice('4.mp3'),
            begin=0.6,
            end=3.7
        )
        self.subtitle('我们编写的大多数代码是在 CPU 上执行的', t)
        t = self.play_audio(
            Voice('5.mp3'),
            delay=t.duration,
            begin=0.5,
            end=3.1
        )
        self.subtitle('在 CPU 上执行通用的任务十分方便', t)

        self.forward()

        cpu_in1 = Group(
            Circle(color=RED, fill_alpha=0.5),
            Square(color=BLUE, fill_alpha=0.5)
        )
        cpu_in1.points.scale(0.2).arrange(DOWN).shift(LEFT * 0.6)

        cpu_out1 = boolean_ops.Union(
            Circle(),
            Square().points.scale(0.85).r,
            color=GREEN,
            fill_alpha=0.5
        )
        cpu_out1.points.scale(0.2).shift(RIGHT * 0.6)

        cpu_in2 = Circle(color=RED, fill_alpha=0.5)
        cpu_in2.points.scale(0.2).shift(LEFT * 0.6)

        cpu_out2 = Square(color=RED, fill_alpha=0.5)
        cpu_out2.points.scale(0.2).shift(RIGHT * 0.6)

        cpu_in3 = Circle(color=BLUE, fill_alpha=0.5)
        cpu_in3.points.scale(0.2).shift(LEFT * 0.6)
        cpu_out3 = Group(
            Square(color=RED, fill_alpha=0.5),
            Triangle(color=YELLOW, fill_alpha=0.5)
        )
        cpu_out3.points.scale(0.2).arrange(DOWN).shift(RIGHT * 0.6)

        choices = [
            (cpu_in1, cpu_out1),
            (cpu_in2, cpu_out2),
            (cpu_in3, cpu_out3)
        ]

        cpu = CPU()

        screen = Rect(1920 / 400, 1080 / 400)
        b1 = Brace(screen, UP)
        b2 = Brace(screen, LEFT)
        g_screen = Group(
            screen,
            b1,
            b1.points.create_text('1920'),
            b2,
            b2.points.create_text('1080')
        )
        g_screen[1:](VItem).color.set(PURPLE)
        g_screen.depth.arrange(2)

        pixel_num = Text(str(1920 * 1080))
        pixel_num.points.next_to(screen, DOWN)

        self.play(FadeIn(cpu, scale=1.2))
        self.forward()

        for cpu_in, cpu_out in choices:
            self.play(
                FadeIn(
                    cpu_in,
                    RIGHT * 4,
                    hide_at_begin=False,
                    show_at_end=False,
                    rate_func=rush_into
                ),
                duration=0.75
            )
            self.play(
                FadeOut(
                    cpu_out,
                    RIGHT * 4,
                    hide_at_begin=False,
                    show_at_end=False,
                    rate_func=rush_from
                ),
                duration=0.75
            )
        self.forward(0.2)

        t = self.play_audio(
            Voice('6.mp3'),
            begin=1.6,
            end=4.0
        )
        self.subtitle('但是，当我们需要进行图形渲染时', t)

        self.forward_to(t.end)

        t = self.play_audio(
            Voice('7.mp3'),
            begin=0.8,
            end=3.7
        )
        self.subtitle('比如一个 1920x1080 的游戏画面', t)

        cpu_state = cpu.copy()

        self.prepare(
            FadeIn(g_screen, scale=0.8),
            cpu(VItem).anim.color.fade(0.6),
            at=0.5
        )
        self.forward_to(t.end)

        t = self.play_audio(
            Voice('8.mp3'),
            begin=0.3,
            end=4.6
        )
        self.subtitle('CPU 需要面对 207,3600 个像素', t)

        self.forward(1.8)

        g_screen(VItem).color.fade(0.6)
        cpu.become(cpu_state)
        pixel_num.show()

        self.forward_to(t.end + 0.5)

        t = self.play_audio(
            Voice('9.mp3'),
            begin=1.3,
            end=4.8
        )
        self.subtitle('甚至你命令它要在一秒内完成几十遍这样的任务！', t)

        self.forward(0.5)

        t = self.prepare(
            Group(cpu.outer, cpu.inner)(VItem)
            .anim.stroke.set(RED)
            .r.fill.set('#880000'),

            duration=2.8
        )

        random.seed(114514)
        for i in range(1, 32):
            cpu_in, cpu_out = random.choice(choices)
            self.prepare(
                FadeIn(
                    cpu_in,
                    RIGHT * 4,
                    hide_at_begin=False,
                    show_at_end=False,
                    rate_func=rush_into
                ),
                FadeOut(
                    cpu_out,
                    RIGHT * 4,
                    hide_at_begin=False,
                    show_at_end=False,
                    rate_func=rush_from,
                    at=0.9
                ),
                duration=0.5
            )
            self.forward(0.2 / i + 0.05)

        self.forward_to(t.end + 1)

        t = self.play_audio(
            Voice('10.mp3'),
            begin=2.1,
            end=4.4
        )
        self.subtitle('这时候就轮到 GPU 登场了', t)

        gpu = GPU()

        self.forward(0.5)
        self.play(
            FadeOut(Group(cpu, pixel_num, g_screen)),
            FadeIn(gpu)
        )
        self.forward_to(t.end + 0.6)

        t = self.play_audio(
            Voice('11.mp3'),
            begin=0.8,
            end=3.9
        )
        self.subtitle('因为渲染时，每个像素点的流程是基本一致的（尽管结果不一样）', t)

        self.forward_to(t.end + 0.6)


        t1 = self.play_audio(
            Voice('12_1_1.mp3').mul(1.5),
            begin=1.1,
            end=1.5
        )
        t2 = self.play_audio(
            Voice('12_1.mp3'),
            delay=t1.duration,
            begin=1.55,
            end=3.1
        )
        self.subtitle('所以类似于批量化流水线', t1.duration + t2.duration)

        self.forward_to(t2.end + 0.2)

        t = self.play_audio(
            Voice('12_2.mp3'),
            begin=0.9,
            end=2.9
        )
        self.subtitle('GPU 通过特制的并行计算', t)

        self.forward_to(t.end + 0.2)

        t = self.play_audio(
            Voice('13.mp3'),
            begin=0.4,
            end=1.8
        )
        self.subtitle('大大提高渲染效率', t)

        self.forward_to(t.end + 1)

        t = self.play_audio(
            Voice('14.mp3'),
            begin=1,
            end=5.8
        )
        self.subtitle('但是，我们并不能直接用C++、Python等语言去编写 GPU 程序', t)

        self.forward(1.5)

        cpp = ImageItem('assets/cpp.png', height=1)
        cpp.points.next_to(gpu, UP, buff=0)
        cross = VCross()
        cross.points.move_to(gpu.points.box.top)

        self.play(FadeIn(cpp, DOWN, rate_func=rush_into), duration=0.4)
        cross.show()
        self.forward(0.08)
        cross.hide()
        self.forward(0.08)
        cross.show()
        self.forward_to(t.end)

        t = self.play_audio(
            Voice('15.mp3'),
            begin=0.4,
            end=4.4
        )
        self.subtitle('GPU 无法执行我们交给 CPU 执行的如此复杂的程序', t)

        self.forward()
        cross.hide()
        self.play(cpp.anim(rate_func=rush_from).points.shift(UP * 0.5), duration=0.4)
        self.play(cpp.anim(rate_func=rush_into).points.shift(DOWN * 0.5), duration=0.4)
        cross.show()
        self.forward(0.08)
        cross.hide()
        self.forward(0.08)
        cross.show()
        self.forward_to(t.end + 0.2)

        t = self.play_audio(
            Voice('16.mp3'),
            begin=1.0,
            end=4.3
        )
        self.subtitle('因为 GPU 是为了高效并行计算而特制的', t)

        self.forward_to(t.end + 0.3)

        t = self.play_audio(
            Voice('17.mp3'),
            begin=0.9,
            end=2.7
        )
        self.subtitle('自然无法执行通用的程序', t)

        self.forward_to(t.end)
        self.play(FadeOut(Group(cpp, cross)))

        self.forward(0.7)

        t = self.play_audio(
            Voice('18.mp3'),
            begin=0.9,
            end=4.0
        )
        self.subtitle('因此，我们就可以使用 OpenGL 进行编程', t)

        note = Text(
            '当然，不是只有 OpenGL 提供了调用 GPU 的能力，还有 DirectX 和 vulkan 等',
            font_size=12,
            color=GREY
        )
        note.points.to_border(UL)

        opengl = ImageItem('assets/opengl.png', height=1)
        opengl.points.next_to(gpu, UP, buff=0)
        glsl = Text('GLSL')
        glsl.points.align_to(opengl, DR).shift(LEFT * 0.2 + UP * 0.02)

        g_opengl = Group(opengl, glsl)
        g_opengl.depth.arrange(1)

        self.forward(1.3)
        note.show()
        self.play(FadeIn(g_opengl), duration=0.8)
        self.play(g_opengl.anim.points.shift(DOWN * 0.3), duration=0.8)
        self.forward_to(t.end)

        t = self.play_audio(
            Audio('19.mp3').clip(0.6, 3.6).mul([1, 2, 2, 2]),
        )
        self.subtitle('告诉 GPU 要如何处理提供给它的数据', t)

        tri = Triangle()
        tri.points.scale(0.8).shift(DOWN * 0.1 + LEFT * 0.5).rotate(-10 * DEGREES)
        in_vert = Group(
            tri,
            Group(*[
                Dot(pos, fill_alpha=1, fill_color=BLACK, stroke_alpha=1, stroke_radius=0.02)
                for pos in tri.points.get_anchors()
            ])
        )
        in_vert.depth.arrange(1)

        self.forward(0.5)
        self.play(
            FadeIn(
                in_vert,
                RIGHT * 4,
                rate_func=linear,
                show_at_end=False
            ),
            duration=2
        )

        self.forward_to(t.end + 0.2)

        t = self.play_audio(
            Voice('20.mp3'),
            begin=0.6,
            end=2.4
        )
        self.subtitle('并得到渲染完成的图像', t)

        out_graph = Triangle(color=[RED, GREEN, BLUE], fill_alpha=1)
        out_graph.points.scale(0.8).shift(DOWN * 0.1 + RIGHT * 0.5).rotate(-10 * DEGREES)
        out_graph.depth.set(1)

        self.play(
            FadeOut(
                out_graph,
                RIGHT * 4,
                rate_func=linear
            ),
            duration=2
        )

        self.forward(1)

        t = self.play_audio(
            Voice('21_refactor_1.mp3'),
            begin=1.7,
            end=6.5
        )
        self.subtitle('所以说，OpenGL 的主要用途是进行高效的图像计算和处理', t)

        note2 = Text(
            '也可以只用于进行数据的并行计算，之后会讲',
            font_size=12,
            color=GREY
        ).show()
        note2.points.next_to(note, DOWN, aligned_edge=LEFT)

        self.forward(0.3)
        glsl.hide()
        self.play(FadeOut(gpu), opengl.anim.points.to_center())
        self.forward_to(t.end)

        self.forward(2)


class WhatIsOpenGL2(Template):
    def construct(self) -> None:
        group = Group(*map(
            SVGItem,
            ('study.svg', 'work.svg', 'customer-interests.svg')
        ))
        group(VItem).color.set(WHITE)
        group.points.scale(0.4).arrange(buff=LARGE_BUFF)

        t = self.play_audio(
            Voice('22.mp3').mul([0.5, 1, 1]),
            begin=1.0,
            end=5.4
        )
        self.subtitle('无论你学习 OpenGL 是为了学业，找工作，或仅仅是因为兴趣', t)

        self.forward(1.6)
        self.prepare(FadeIn(group[0], scale=0.8))
        self.forward(0.65)
        self.prepare(FadeIn(group[1], scale=0.8))
        self.forward(1)
        self.prepare(FadeIn(group[2], scale=0.8))

        self.forward_to(t.end + 0.2)

        t = self.play_audio(
            Voice('23.mp3'),
            begin=2.1,
            end=5.2
        )
        self.subtitle('这里都将能够教会你现代 OpenGL 的知识', t)

        txt = Text('现代(Core-profile) OpenGL')
        txt.points.shift(DOWN * 0.7)

        self.forward(1.4)
        self.prepare(
            group.anim.points.shift(UP * 0.5).scale(0.7),
            Write(txt, duration=1)
        )


        self.forward_to(t.end + 1)


class Subtitle_Reason(SubtitleTemplate):
    name = '你选择这个教程的原因'


reason_code_1 = '''<fc #569cd6>#version</fc> <fc #b5cea8>330</fc><fc #cccccc> core</fc>
<fc #569cd6>layout</fc><fc #cccccc> (location </fc><fc #d4d4d4>=</fc> <fc #b5cea8>0</fc><fc #cccccc>) </fc><fc #569cd6>in</fc> <fc #569cd6>vec3</fc><fc #cccccc> aPos;</fc>
<fc #569cd6>layout</fc><fc #cccccc> (location </fc><fc #d4d4d4>=</fc> <fc #b5cea8>1</fc><fc #cccccc>) </fc><fc #569cd6>in</fc> <fc #569cd6>vec3</fc><fc #cccccc> aColor;</fc>

<fc #569cd6>out</fc> <fc #569cd6>vec3</fc><fc #cccccc> ourColor;</fc>

<fc #569cd6>void</fc><fc #cccccc> main()</fc>
<fc #cccccc>{</fc>
    <fc #9cdcfe>gl_Position</fc> <fc #d4d4d4>=</fc> <fc #569cd6>vec4</fc><fc #cccccc>(aPos, </fc><fc #b5cea8>1.0</fc><fc #cccccc>);</fc>
<fc #cccccc>    ourColor </fc><fc #d4d4d4>=</fc><fc #cccccc> aColor;</fc>
<fc #cccccc>}</fc>'''


class Reason(Template):
    CONFIG = Config(
        preview_fps=30
    )
    def construct(self) -> None:
        random.seed(114514)

        doc = SVGItem('document.svg', color=WHITE)
        doc.points.scale(0.25)

        rows = 4
        cols = 8
        g_doc = (doc * (rows * cols))
        g_doc.points.arrange_in_grid(rows, cols, buff=MED_LARGE_BUFF)
        g_doc.shuffle()

        self.forward()

        t = self.play_audio(
            Voice('25.mp3'),
            begin=0.4,
            end=5.5
        )
        t2 = self.subtitle('在互联网上', 1.2)
        self.subtitle('有关学习 OpenGL 的有成千上万的文档与资源',
                      t.end - t2.end,
                      t2.duration)

        self.play(
            Succession(
                *[FadeIn(item, scale=1.2) for item in g_doc],
                buff=-0.95
            ),
            duration=t.duration
        )
        self.forward(0.5)

        t = self.play_audio(
            Voice('26.mp3'),
            begin=0.9,
            end=5.7
        )
        self.subtitle(
            [
                '然而其中有很多的资源仅仅讨论了OpenGL的立即渲染模式',
                '（Immediate Mode，通常会说旧 OpenGL）'
            ],
            t,
            scale=[1, 0.7]
        )

        self.forward(0.5)
        self.play(
            g_doc[:20](VItem).anim.color.fade(0.7),
            duration=2
        )
        self.forward_to(t.end + 0.7)

        t = self.play_audio(
            Voice('27.mp3'),
            begin=0.7,
            end=3.2
        )
        self.subtitle('亦或是不完整，缺少适当的文档', t)

        self.forward(0.7)
        self.play(
            g_doc[20:25](VItem).anim.color.fade(0.7)
        )
        self.forward_to(t.end + 0.7)

        t = self.play_audio(
            Voice('28.mp3'),
            begin=0.6,
            end=2.5
        )
        self.subtitle('甚至是仅仅不适合你的口味', t)

        self.forward(0.4)
        self.play(
            g_doc[25:29](VItem).anim.color.fade(0.7)
        )
        self.forward()
        self.play(Uncreate(g_doc))
        self.forward()

        random.seed(1145141)
        def rand_rotation(item: Points) -> None:
            item.points.rotate(10 * DEGREES * (random.random() * 2 - 1))

        txt = Text(reason_code_1, format=Text.Format.RichText)
        txt.points.scale(0.8)
        imgs = [
            ImageItem(path)
            for path in [
                'shaders3.png',
                'tex_coords.png',
                'textures_funky.png'
            ]
        ]

        t = self.play_audio(
            Voice('29.mp3'),
            begin=0.7,
            end=3.5
        )
        self.subtitle('如果你很享受提供手把手指导的教程', t)

        t = self.play_audio(
            Voice('30.mp3'),
            delay=t.duration,
            begin=0.4,
            end=2.3
        )
        self.subtitle('以及提供清晰例子的教程', t)

        self.forward(0.5)
        for item in (txt, *imgs):
            rand_rotation(item)
            self.play(FadeIn(item, scale=0.9))
            self.forward(0.2)

        t = self.play_audio(
            Audio('31.mp3').mul([1, 2, 2]),
            begin=0.6,
            end=2.9
        )
        self.subtitle('那么这个教程很可能就很适合你', t)

        self.forward_to(t.end + 0.2)

        self.play(
            Succession(
                *map(FadeOut, (txt, *imgs)),
                buff=-0.7
            )
        )

        noob = SVGItem('noob.svg', color=WHITE)
        expert = SVGItem('expert.svg', color=WHITE)
        g = Group(noob, expert)
        g.points.scale(0.2).arrange(buff=LARGE_BUFF)

        t = self.play_audio(
            Voice('32.mp3'),
            begin=0.5,
            end=4.6
        )
        self.subtitle('这个教程旨在让那些没有图形编程经验的人们能够理解', t)

        self.forward(1.4)
        self.play(FadeIn(noob, scale=1.2))
        self.forward_to(t.end + 0.4)

        t = self.play_audio(
            Audio('33.mp3').mul([1.4, 2, 2]),
            begin=0.5,
            end=3.3
        )
        self.subtitle('又让那些有经验的读者有阅读下去的兴趣', t)

        self.forward(0.4)
        self.play(FadeIn(expert, scale=1.2))
        self.forward_to(t.end + 0.4)

        self.play(
            *map(Uncreate, g)
        )

        self.forward()


class Subtitle_WhatWillLearn(SubtitleTemplate):
    name = '你将学会什么呢？'


class WhatWillLearn(Template):
    def construct(self) -> None:
        self.forward()

        t = self.play_audio(
            Voice('34.mp3'),
            begin=0.5,
            end=3.1
        )
        self.subtitle('这个教程的核心是现代 OpenGL', t)

        opengl = ImageItem('opengl.png', height=2)
        self.forward(0.5)
        self.play(FadeIn(opengl))

        self.forward_to(t.end + 0.3)

        pre1 = Text('图形编程')
        pre2 = Text('幕后运作')
        g = Group(pre1, pre2)
        g.points.arrange(buff=LARGE_BUFF).shift(DOWN * 0.8)

        t1 = self.play_audio(
            Voice('35.mp3').mul(1.6),
            begin=0.4,
            end=0.9
        )
        t2 = self.play_audio(
            Voice('35.mp3').mul([1.5, 2, 2.5]),
            delay=t1.duration,
            begin=1.3,
            end=8.7
        )
        st1 = self.subtitle('学习（和使用）现代OpenGL需要用户', 2.2)
        st2 = self.subtitle('对图形编程以及 OpenGL 的幕后运作', 2.4, st1.duration)
        delay = st1.duration + st2.duration
        audio_duration = t1.duration + t2.duration
        self.subtitle('有非常好的理解才能在编程中有很好的发挥', audio_duration - delay, delay)

        self.play(
            opengl.anim.points.scale(0.6).shift(UP * 0.8),
            at=1.3
        )
        self.play(Write(pre1))
        self.forward(0.5)
        self.play(Write(pre2))

        self.forward_to(t2.end + 1)

        t = self.play_audio(
            Voice('36.mp3').mul([1.5, 2]),
            begin=0.8,
            end=3.5
        )
        self.subtitle('所以，我们会先讨论核心的图形学概念', t)

        self.forward_to(t.end + 0.1)

        t = self.play_audio(
            Voice('37.mp3').mul(1.7),
            begin=0.5,
            end=3.2
        )
        self.subtitle('OpenGL怎样将像素绘制到屏幕上', t)

        img = ImageItem('instancing_asteroids.png', height=3)
        width, height = img.image.get().size

        img_pixels = Group(*[
            Rect(
                img.pixel_to_point(x, y),
                img.pixel_to_point(x + 4, y + 4),
                stroke_color=GREY_E,
                stroke_radius=0.001,
                fill_color=img.pixel_to_rgba(x, y)[:3],
                fill_alpha=1
            )
            for y in range(0, height, 8)
            for x in range(0, width, 8)
        ])

        self.forward(0.5)
        self.prepare(
            *map(FadeOut, (opengl, pre1, pre2)),
            FadeIn(img_pixels, scale=0.5, duration=3, lag_ratio=0.005)
        )

        self.forward_to(t.end + 0.3)

        t = self.play_audio(
            Voice('38.mp3').mul(1.7),
            begin=0.2,
            end=2.9
        )
        self.subtitle('以及如何利用黑科技做出一些很酷的效果', t)

        self.forward_to(t.end + 0.3)

        self.play(FadeOut(img_pixels))

        t = self.play_audio(
            Voice('39.mp3').mul([1, 1.8]),
            begin=0.8,
            end=3.8
        )
        self.subtitle('除了核心概念之外，我们还会讨论许多有用的技巧', t)

        self.forward_to(t.end + 0.2)

        t = self.play_audio(
            Voice('40.mp3').mul([1, 2.7]),
            begin=0.4,
            end=2.2
        )
        self.subtitle('它们都可以用在你的程序中', t)

        self.forward_to(t.end + 0.4)

        t = self.play_audio(
            Voice('41.mp3').mul(1.7),
            begin=0.5,
            end=3.4
        )
        self.subtitle('比如说在场景中移动、做出漂亮的光照', t)

        self.forward_to(t.end + 0.1)

        t = self.play_audio(
            Voice('42.mp3').mul([1, 2]),
            begin=0.6,
            end=2.9
        )
        self.subtitle('加载建模软件导出的自定义模型', t)

        self.forward_to(t.end + 0.1)

        t = self.play_audio(
            Voice('43.mp3').mul([1.4, 2.9]),
            begin=0.6,
            end=2.7
        )
        self.subtitle('做一些很酷的后期处理技巧等', t)

        # self.forward_to(t.end + 0.4)
        self.forward_to(t.end + 1.5)

        # t = self.play_audio(
        #     Voice('44.mp3').mul([1.2, 1.4, 1.8]),
        #     begin=0.6,
        #     end=4.5
        # )
        # self.subtitle('最后，我们也将会使用我们已学的知识从头开始做一个小游戏', t)

        # self.forward_to(t.end + 0.2)

        # t = self.play_audio(
        #     Audio('45.mp3').mul([1.3, 1.5, 3, 5]),
        #     begin=0.4,
        #     end=2.5
        # )
        # self.subtitle('让你真正体验一把图形编程的魅力', t)

        # self.forward_to(t.end + 1.5)


class Subtitle_Prerequisite(SubtitleTemplate):
    name = '前置知识'


class Prerequisite(Template):
    def construct(self) -> None:
        self.forward()

        t = self.play_audio(
            Voice('100.mp3').mul(1.2),
            begin=1.6,
            end=3.6
        )
        self.subtitle('由于 OpenGL 是一个图形 API', t)

        opengl = ImageItem('opengl.png', height=1.5)
        python = ImageItem('python.png', height=1.5)
        g = Group(opengl, python)
        g.points.arrange(buff=LARGE_BUFF)

        self.prepare(
            FadeIn(opengl),
            at=0.3
        )

        self.forward_to(t.end + 0.1)

        t = self.play_audio(
            Voice('101.mp3').mul(1.1),
            begin=0.6,
            end=2.2
        )
        self.subtitle('并不是一个独立的平台', t)

        self.forward_to(t.end + 0.2)

        t = self.play_audio(
            Audio('102.mp3').mul(1.5),
            begin=1.1,
            end=2.8
        )
        self.subtitle('它需要一个编程语言来工作', t)

        self.forward_to(t.end + 0.1)

        t = self.play_audio(
            Audio('103.mp3').mul(1.5),
            begin=0.7,
            end=2.3
        )
        self.subtitle('在这里我们使用的是 Python', t)

        self.prepare(
            FadeIn(python),
            at=0.6
        )

        self.forward_to(t.end + 0.5)

        t = self.play_audio(
            Audio('104.mp3').mul(1.6),
            begin=0.5,
            end=4.5
        )
        self.subtitle('所以，有一定的 Python 基础在学习这个教程中是必不可少的', t)

        self.prepare(
            Flash(python, flash_radius=1),
            at=2.8
        )

        self.forward_to(t.end + 0.4)

        t = self.play_audio(
            Audio('105.mp3').mul(1.6),
            begin=0.6,
            end=3.8
        )
        self.subtitle('当然，我仍将尝试解释大部分用到的概念', t)

        self.forward_to(t.end + 0.1)

        t = self.play_audio(
            Voice('106.mp3'),
            begin=0.5,
            end=3.7
        )
        self.subtitle('所以，你并不一定要是一个 Python 专家才能来学习', t)

        self.forward_to(t.end + 0.4)

        t = self.play_audio(
            Audio('107.mp3').mul(1.6),
            begin=0.5,
            end=4.1
        )
        self.subtitle('不过，请确保你至少应该能写个比 Hello World 复杂的程序', t)

        self.forward_to(t.end)
        self.play(FadeOut(g))

        t = self.play_audio(
            Audio('108.mp3').mul(1.7),
            begin=1.1,
            end=3.5
        )
        self.subtitle('除此之外，我们也将用到一些数学知识', t)

        square = Square(fill_alpha=1, stroke_alpha=0, color=GREY)
        arrow1 = Arrow(ORIGIN, RIGHT, buff=0, color=RED)
        arrow2 = Arrow(ORIGIN, UP, buff=0, color=GREEN)
        arrow3 = Arrow(ORIGIN, OUT, buff=0, color=BLUE)
        g = Group(square, arrow1, arrow2, arrow3)
        g_state = g.copy()

        self.play(
            FadeIn(g),
            at=0.5
        )
        self.prepare(
            Rotate(g, 30 * DEGREES, axis=UP, about_point=ORIGIN),
            at=1.5,
            duration=3,
        )
        self.prepare(
            Rotate(g, 90 * DEGREES, axis=DR, about_point=ORIGIN),
            at=4.5,
            duration=5
        )
        self.prepare(
            Rotate(g, 70 * DEGREES, axis=UL, about_point=ORIGIN),
            at=9.5,
            duration=5
        )

        self.forward_to(t.end + 0.7)

        t = self.play_audio(
            Audio('109.mp3'),
            begin=0.9,
            end=2.9
        )
        self.subtitle('同样我也会尝试解释这些概念', t)

        self.forward_to(t.end + 0.4)

        t = self.play_audio(
            Audio('112.mp3').mul(1.4),
            begin=1,
            end=2.1
        )
        self.subtitle('在必须的时候', t)

        self.forward_to(t.end + 0.1)

        t = self.play_audio(
            Audio('113.mp3').mul(1.4),
            begin=0.7,
            end=2.3
        )
        self.subtitle('我会链接一些不错的资料', t)

        self.forward_to(t.end + 0.2)

        t = self.play_audio(
            Audio('114.mp3').mul(1.4),
            begin=0.4,
            end=2.6
        )
        self.subtitle('他们会将这些概念解释地更加全面', t)

        self.forward_to(t.end + 0.5)

        t = self.play_audio(
            Audio('115.mp3').mul(1.4),
            begin=0.7,
            end=2.7
        )
        self.subtitle('不要被必须的数学知识吓到了', t)

        self.forward_to(t.end + 0.2)

        t = self.play_audio(
            Audio('116.mp3').mul(1.4),
            begin=0.6,
            end=4.0
        )
        self.subtitle('几乎所有的概念只要有基础的数学背景都可以理解', t)

        self.forward_to(t.end + 0.2)

        t = self.play_audio(
            Audio('117.mp3').mul(1.4),
            begin=0.7,
            end=2.8
        )
        self.subtitle('我也会将数学的内容压缩至极限', t)

        self.play(
            g.anim(rate_func=rush_into).points.scale(0),
            duration=t.duration
        )
        g.hide()
        self.forward(0.1)

        t = self.play_audio(
            Audio('118.mp3').mul(1.4),
            begin=0.5,
            end=3.7
        )
        self.subtitle('大部分的功能甚至都不需要你理解所有的数学知识', t)

        self.forward_to(t.end + 0.2)

        t = self.play_audio(
            Audio('119.mp3').mul(1.4),
            begin=0.8,
            end=2.3
        )
        self.subtitle('因为数学是底层原理', t)

        self.forward_to(t.end + 0.1)

        t = self.play_audio(
            Audio('120.mp3').mul(1.4),
            begin=1.05,
            end=3.9
        )
        self.subtitle('大多数情况下已经有别人替我们完成了这部分', t)

        gsvg = SVGItem('g.svg', color=GREEN)
        gsvg.points.scale(0.4)

        self.prepare(SpinInFromNothing(gsvg), at=0.2, duration=4)
        self.forward_to(t.end + 0.1)

        t = self.play_audio(
            Audio('121.mp3').mul(1.2),
            begin=0.5,
            end=1.7
        )
        self.subtitle('只要你会使用就行', t)

        self.forward_to(t.end + 0.2)

        t = self.play_audio(
            Audio('122.mp3').mul(1.4),
            begin=0.6,
            end=2.8
        )
        self.subtitle('但是知道它的原理也不是一件坏事', t)

        self.prepare(FadeOut(gsvg), at=1)

        self.forward_to(t.end + 0.2)
