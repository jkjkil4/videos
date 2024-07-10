# flake8: noqa
import sys

sys.path.append('.')

from colour import Color
from janim.imports import *

from utils.template import *


code1_src = '''<fc #dcdcaa>glBindBuffer</fc><fc #cccccc>(</fc><fc #4fc1ff>GL_ARRAY_BUFFER</fc><fc #cccccc>, </fc><fc #b5cea8>0</fc><fc #cccccc>)</fc>
<fc #dcdcaa>glBindBuffer</fc><fc #cccccc>(</fc><fc #4fc1ff>GL_ELEMENT_ARRAY_BUFFER</fc><fc #cccccc>, </fc><fc #b5cea8>0</fc><fc #cccccc>)</fc>
<fc #dcdcaa>glClear</fc><fc #cccccc>(</fc><fc #4fc1ff>GL_COLOR_BUFFER_BIT</fc><fc #cccccc>)</fc>
<fc #dcdcaa>glUseProgram</fc><fc #cccccc>(</fc><fc #9cdcfe>shaderProgram</fc><fc #cccccc>)</fc>
<fc #dcdcaa>glBindVertexArray</fc><fc #cccccc>(</fc><fc #4fc1ff>VAO</fc><fc #cccccc>)</fc>
<fc #dcdcaa>glDrawArrays</fc><fc #cccccc>(</fc><fc #4fc1ff>GL_TRIANGLES</fc><fc #cccccc>, </fc><fc #b5cea8>0</fc><fc #cccccc>, </fc><fc #b5cea8>6</fc><fc #cccccc>)</fc>
<fc #cccccc>...</fc>'''


class Title(TitleTemplate):
    str1 = 'Learn OpenGL'
    str2 = 'OpenGL 具体介绍'


class Intro(SubtitlesTemplate2):
    subtitles = [
        ('1.mp3', '这一节', 0.3, dict(clip=(0.85, 1.6))),
        ('2.mp3', '我们会对 OpenGL 的一些基本知识进行介绍', 0.5, {}),
        ('3.mp3', '虽然主要是一些文字内容', 0.3, {}),
        ('4.mp3', '但是这对你理解 OpenGL 是什么、怎么用有一定的帮助', 0.2, {})
    ]

    def construct(self) -> None:
        opengl = ImageItem('opengl.png', height=2)
        self.prepare(
            FadeIn(opengl),
            at=2
        )
        super().construct()
        self.play(FadeOut(opengl))


class Background_Subtitle(SubtitleTemplate):
    name = 'OpenGL 背景知识'


class Background(Template):
    def construct(self) -> None:
        opengl = ImageItem('opengl.png', height=1)
        rect = boolean_ops.Difference(
            SurroundingRect(opengl, buff=0.16),
            SurroundingRect(opengl),
            color=BLUE,
            stroke_radius=0.015,
            fill_alpha=0.5
        )
        openglg = Group(opengl, rect)
        openglg.points.shift(LEFT * 2)

        gpu = SVGItem('gpu.svg', height=3)
        gpu.points.shift(RIGHT * 2)

        lines = Line(ORIGIN, RIGHT * 2) * 5
        lines(VItem).color.set(BLUE)
        lines.depth.arrange(2)
        lines.points.arrange(DOWN, buff=0.15).next_to(openglg, buff=0)

        lines_flash = lines.copy()
        lines_flash(VItem).color.set(YELLOW)
        lines_flash.depth.arrange(1)

        lines_flash_reversed = lines_flash.copy()
        for subitem in lines_flash_reversed.children:
            subitem.points.reverse()

        #########################################################

        self.forward()

        t = self.aas('5.mp3', '在前一节中我们提到')
        self.forward_to(t.end + 0.2)
        t = self.aas('6.mp3', '可以使用 OpenGL 与显卡进行交互')

        self.play(
            Succession(
                AnimGroup(
                    FadeIn(openglg, LEFT),
                    FadeIn(gpu, RIGHT)
                ),
                Write(lines)
            )
        )
        self.prepare(
            Succession(
                Succession(*[
                    ShowPassingFlash(lines_flash)
                    for _ in range(5)
                ]),
                Succession(*[
                    ShowPassingFlash(lines_flash_reversed)
                    for _ in range(5)
                ]),
                Wait(2),
                Succession(*[
                    ShowPassingFlash(lines_flash)
                    for _ in range(5)
                ]),
                Succession(*[
                    ShowPassingFlash(lines_flash_reversed)
                    for _ in range(5)
                ]),
                Wait(2),
                Succession(*[
                    ShowPassingFlash(lines_flash)
                    for _ in range(5)
                ]),
                Succession(*[
                    ShowPassingFlash(lines_flash_reversed)
                    for _ in range(5)
                ])
            ),
            duration=6
        )

        self.forward_to(t.end + 0.2)
        t = self.aas('7.mp3', '进行快速的大批量图形渲染')
        self.forward_to(t.end + 0.5)
        t = self.aas('8.mp3', '所以说一般而言')
        self.forward_to(t.end + 0.2)
        t = self.aas('9.mp3', 'OpenGL 被认为是一个 API')
        self.forward_to(t.end + 0.3)

        #########################################################

        code1 = Text(code1_src, format=Text.Format.RichText)
        code1.points.scale(0.3).move_to(opengl)

        note1 = Text(
            '这里用作示意的函数是 C 里的\n等会我们用的是 ModernGL，做了一层封装',
            font_size=8,
            color=GREY
        )
        note1.points.next_to(openglg, UP, aligned_edge=LEFT, buff=SMALL_BUFF)

        pack = SVGItem('pack.svg', height=1)
        pack.points.move_to(opengl)

        spec = Text('Specification', font='LXGW WenKai Lite', font_size=16)
        spec.points.move_to(pack).shift(DOWN * 0.2)

        camera_stat = self.camera.store()

        #########################################################

        t = self.aas('10.mp3', '包含了一系列可以操作图形、图像的函数')

        self.prepare(
            Succession(
                AnimGroup(
                    self.camera.anim.points.scale(0.5).move_to(openglg),
                    FadeOut(opengl, duration=0.4),
                    Write(code1, stroke_radius=0.002)
                ),
                FadeIn(note1)
            )
        )

        self.forward_to(t.end + 0.5)
        t = self.aas('11.mp3', '然而，OpenGL 本身其实并不是一个 API')
        self.forward_to(t.end + 0.3)
        t = self.aas('12.mp3', '它仅仅是由 Khronos（我不会读）组织制定并维护的规范（Specification）')

        self.prepare(
            AnimGroup(
                code1(VItem).anim.color.fade(0.8),
                FadeIn(pack),
            ),
            Write(spec, stroke_radius=0.002),
            lag_ratio=0.7,
            at=1
        )

        self.forward_to(t.end + 0.7)

        t = self.aas('13.mp3', 'OpenGL 规范严格规定了',
                     clip=(0.5, 2.8))

        specg = Group(pack, spec)

        specg_target = specg.copy()
        specg_target.points.scale(1.5).shift(LEFT)

        self.prepare(
            AnimGroup(
                *map(FadeOut, (rect, note1, lines, gpu)),
                # duration=
            ),
            specg.anim.become(specg_target),
            code1.anim.fill.set(alpha=1).r.points.scale(2.5).next_to(specg_target, buff=LARGE_BUFF),
            self.camera.anim.restore(camera_stat)
        )

        self.forward_to(t.end)

        #########################################################

        arrow1 = SVGItem('arrow-right.svg', height=code1[1].points.box.height * 0.8)
        arrow1.points.next_to(code1[1], LEFT)

        arrow2 = arrow1.copy()
        arrow2.points.next_to(code1[1], RIGHT)

        #########################################################

        t = self.aas('14.mp3', '每个函数该如何执行，以及它们的输出值')

        self.prepare(
            Succession(
                Write(arrow1),
                Write(arrow2)
            ),
            at=0.6,
            duration=t.duration - 0.6
        )
        self.prepare(
            FadeOut(arrow1),
            FadeOut(arrow2),
            at=t.duration
        )

        self.forward_to(t.end + 0.4)
        t = self.aas('15.mp3', '至于内部具体每个函数是如何实现的')

        self.prepare(
            *[Indicate(line, scale_factor=1.05) for line in code1[:-1]],
            lag_ratio=0.7,
            at=0.5,
            duration=1.5
        )

        self.forward_to(t.end + 0.2)
        t = self.aas('16.mp3', '将由编写 OpenGL 库的开发者自行决定')
        self.forward_to(t.end + 0.4)
        t = self.aas('17.mp3', '只要我们作为用户在调用它们的时候不会感受到功能的差异就行了')

        self.prepare(
            FadeOut(specg),
            FadeOut(code1),
            at=2,
            duration=t.duration - 2
        )

        self.forward_to(t.end + 0.8)

        #########################################################

        nvdia = SVGItem('NVDIA.svg', height=1.3)
        amd = SVGItem('Amd.svg', height=1.3)

        comps = Group(nvdia, amd)
        comps.points.arrange(DOWN, buff=MED_LARGE_BUFF).shift(LEFT * 2)

        opengl.points.to_center().scale(1.4).shift(RIGHT * 2)

        apple = SVGItem('apple-fill.svg', height=1.3)
        apple.points.shift(LEFT * 2)
        linux = Group(
            linux_svg := SVGItem('linux.svg', height=1.3),
            SurroundingRect(
                linux_svg,
                depth=1,
                stroke_alpha=0,
                fill_alpha=0.5,
                fill_color=WHITE
            )
        )
        linux.points.shift(LEFT * 2)

        #########################################################

        t = self.aas('18.mp3', '实际的 OpenGL 库的开发者通常是显卡的生产商')

        self.prepare(
            Succession(
                AnimGroup(
                    FadeIn(opengl, LEFT),
                    FadeIn(comps, RIGHT),
                ),
                Wait(0.4),
                AnimGroup(
                    *map(ShowPassingFlashAround, comps)
                )
            ),
            at=1.6
        )

        self.forward_to(t.end + 0.3)
        t = self.aas('19.mp3', '你购买的显卡所支持的 OpenGL 版本都为这个系列的显卡专门开发的')
        self.forward_to(t.end + 0.8)
        t = self.aas('20.mp3', '当你使用 Apple 系统的时候')

        self.prepare(
            FadeOut(comps, LEFT),
            FadeIn(apple, RIGHT),
            lag_ratio=0.7
        )

        self.forward_to(t.end + 0.2)
        t = self.aas('21.mp3', 'OpenGL 库是由 Apple 自身维护的')

        self.prepare(
            ShowPassingFlashAround(apple),
            at=1
        )

        self.forward_to(t.end + 0.5)
        t = self.aas('22.mp3', '在 Linux 下，有显卡生产商提供的 OpenGL 库')

        self.prepare(
            FadeOut(apple, LEFT),
            FadeIn(linux, RIGHT),
            lag_ratio=0.3
        )

        self.forward_to(t.end + 0.2)
        t = self.aas('23.mp3', '也有一些爱好者改编的版本')
        self.forward_to(t.end + 0.6)
        t = self.aas('24.mp3', '这也意味着任何时候 OpenGL 库表现的行为与规范规定的不一致时')

        self.prepare(
            FadeOut(linux, LEFT),
            opengl.anim(duration=1.5).points.to_center()
        )

        self.forward_to(t.end + 0.2)
        t = self.aas('25.mp3', '基本都是库的开发者留下的 bug')
        self.forward_to(t.end)

        self.play(FadeOut(opengl))
        self.forward(0.5)


typ1_src = '''
#set par(first-line-indent: 2em, justify: true)
#set text(font: "Noto Sans S Chinese")
#set page(margin: 12em)
#par(box[])

由于 OpenGL 的大多数实现都是由显卡厂商编写的，当产生一个 bug 时通常可以通过升级显卡驱动来解决。这些驱动会包括你的显卡能支持的最新版本的 OpenGL，这也是为什么总是建议你偶尔更新一下显卡驱动。

所有版本的OpenGL规范文档都被公开的寄存在 Khronos 那里。你有兴趣的话可以找到OpenGL3.3（我们将要使用的版本）的规范文档。如果你想深入到 OpenGL 的细节（只关心函数功能的描述而不是函数的实现），这是个很好的选择。如果你想知道每个函数具体的运作方式，这个规范也是一个很棒的参考。
'''


class Background_Addition(Template):
    def construct(self) -> None:
        txt1 = TypstDoc(typ1_src)
        txt1.points.to_center()

        rect = Rect(
            Config.get.frame_width, 0.2,
            stroke_alpha=0,
            fill_alpha=1,
            fill_color=RED_E
        )
        rect.points.to_border(UP, buff=0)
        rect.points.shift(LEFT * Config.get.frame_width)

        self.play(Write(txt1))
        self.play(
            rect.anim(rate_func=linear)
            .points.shift(RIGHT * Config.get.frame_width),

            duration=2.5
        )
        self.play(FadeOut(txt1), FadeOut(rect))
        self.forward(0.5)
