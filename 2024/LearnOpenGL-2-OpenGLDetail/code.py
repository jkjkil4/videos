# flake8: noqa
import itertools
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


def triplewise(iterable):
    # 创建三个独立的迭代器
    a, b, c = itertools.tee(iterable, 3)
    # 将每个迭代器向前推进不同的步数
    next(b, None)
    next(c, None)
    next(c, None)
    return zip(a, b, c)


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


class Background_Addition(TextDisplayTemplate):
    typ_src = typ1_src


class CoreModeAndImmediateMode_Subtitle(SubtitleTemplate):
    name = 'OpenGL 核心模式与立即渲染模式'


typ2_typ3_template = '''
#set text(font: "LXGW WenKai Lite", weight: "bold")
#show text: t => align(center, t)

#box(
    stroke: {color},
    fill: {color}.darken(50%),
    inset: 8pt
)[
    {zhcn}

    #set text(size: 0.7em)

    {en}
]
'''

typ2_src = typ2_typ3_template.format(zhcn='立即渲染模式',
                                     en='Immediate Mode',
                                     color='lime')

typ3_src = typ2_typ3_template.format(zhcn='核心模式',
                                     en='Core-profile',
                                     color='aqua')


class CoreModeAndImmediateMode1(Template):
    def construct(self) -> None:
        #########################################################

        opengl = ImageItem('opengl.png', height=1.5, depth=2)
        shadow = Rect(
            Config.get.frame_width, Config.get.frame_height,
            stroke_alpha=0,
            fill_alpha=0.5,
            fill_color=BLACK,
            depth=1
        )

        txt1 = TypstText(typ2_src, depth=-1)
        txt2 = TypstText(typ3_src, depth=-1)

        #########################################################

        t = self.aas(
            '26.mp3',
            [
                '早期的 OpenGL 使用立即渲染模式',
                '（Immediate Mode，也就是固定渲染管线）'
            ],
            scale=[1, 0.7]
        )

        self.prepare(
            Succession(
                FadeIn(opengl, scale=1.2),
                Wait(0.5),
                AnimGroup(
                    FadeIn(shadow),
                    FadeIn(txt1[0]),
                    Create(txt1[1:])
                )
            )
        )

        self.forward_to(t.end + 0.6)
        t = self.aas('27.mp3', '这个模式下绘制图形很方便')
        self.forward_to(t.end + 0.4)
        t = self.aas('28.mp3', '但是由于 OpenGL 的大多数功能都被库隐藏起来')

        self.play(
            FadeOut(shadow),
            opengl.anim.points.shift(LEFT * 2.5),
            txt1.anim.points.shift(RIGHT * 2.5 + UP).scale(0.8),
            duration=2
        )
        arrow1 = Arrow(opengl, txt1, color=GREEN)
        txt1_stat = txt1.copy()
        self.prepare(GrowArrow(arrow1))

        self.forward_to(t.end + 0.3)
        t = self.aas('29.mp3', '开发者很少有控制 OpenGL 如何进行计算的自由')
        self.forward_to(t.end + 0.5)
        t = self.aas('30.mp3', '而开发者迫切希望能有更多的灵活性')
        self.forward_to(t.end + 0.8)
        t = self.aas('31.mp3', 'OpenGL3.2 开始')
        self.forward_to(t.end + 0.3)
        t = self.aas('32.mp3', '规范文档开始废弃立即渲染模式')

        self.prepare(
            Group(arrow1, txt1)(VItem).anim.color.fade(0.5)
        )

        self.forward_to(t.end + 0.4)
        t = self.aas('33.mp3', '并鼓励开发者在 OpenGL 的核心模式下进行开发')

        self.play(
            FadeIn(shadow),
            FadeIn(txt2[0]),
            Create(txt2[1:]),
            at=1
        )
        self.forward(0.5)
        self.play(
            FadeOut(shadow),
            txt2.anim.points.shift(RIGHT * 2.5 + DOWN).scale(0.8)
        )
        arrow2 = Arrow(opengl, txt2, color=BLUE)
        self.prepare(GrowArrow(arrow2))

        self.forward_to(t.end + 0.5)
        t = self.aas('34.mp3', '这个分支的规范完全移除了旧的特性')
        self.forward_to(t.end)

        self.play(
            arrow1.anim.color.set(alpha=1),
            txt1.anim.become(txt1_stat)
        )

        #########################################################

        machine1 = SVGItem('machine.svg')
        machine1.points.scale(0.17).next_to(txt1, buff=LARGE_BUFF)

        machine2 = machine1.copy()
        machine2.points.set_y(txt2.points.box.y)

        camera_stat = self.camera.store()

        sq1 = Square(0.1, color=RED, fill_alpha=0.5, depth=1)
        sq1.points.next_to(machine1, LEFT, buff=0).shift(UP * 0.25 + RIGHT * 0.2)
        ci1 = Circle(0.05, color=GREEN, fill_alpha=0.5, depth=1)
        ci1.points.next_to(machine1, RIGHT, buff=0).shift(DOWN * 0.35 + LEFT * 0.3)

        gears = SVGItem('gears.svg')
        gears.points.move_to(machine2).scale(0.11).shift(LEFT * 0.06)

        txt_33 = Text('OpenGL3.3', font_size=16)
        txt_33.points.next_to(arrow2, DOWN)

        #########################################################

        t = self.aas('35.mp3', '立即渲染模式就像一台有着基本功能的机器')

        self.prepare(
            Create(machine1),
            self.camera.anim.points.scale(0.5).move_to(Group(txt1, machine1)),
            duration=2.5
        )

        self.forward_to(t.end + 0.3)
        t = self.aas('36.mp3', '略去了很多内部的运作细节')

        for i in range(4):
            self.prepare(
                FadeIn(sq1, RIGHT, rate_func=rush_into),
                FadeOut(ci1, RIGHT, rate_func=rush_from),
                lag_ratio=1,
                duration=2,
                at=i * 0.35
            )

        self.forward_to(t.end + 1)
        t = self.aas('37.mp3', '与之相反，核心模式给了我们定制这个机器的机会')

        self.play(
            self.camera.anim.points.set_y(machine2.points.box.y),
            Create(machine2),
            duration=2
        )
        self.prepare(
            machine2[0].anim.fill.set(alpha=0.3),
            duration=1.5
        )

        self.forward_to(t.end + 0.4)
        t = self.aas('38.mp3', '我们能够定制这个机器中的每一个零件')

        self.prepare(
            FadeOut(machine2[1:], at=1),
            FadeIn(
                gears,
                scale=0.8,
                lag_ratio=0.2,
                at=1.5,
                duration=t.duration - 1.5
            )
        )

        self.forward_to(t.end + 0.3)
        t = self.aas('39.mp3', '给了我们更高的灵活性')
        self.forward_to(t.end + 0.5)
        t = self.aas('40.mp3', '并且通过这种方式将更多的任务交给了 GPU')

        self.prepare(
            self.camera.anim.restore(camera_stat).points.shift(RIGHT),
            at=2,
            duration=3
        )

        self.forward_to(t.end + 0.3)
        t = self.aas('41.mp3', '充分发挥其并行计算的优势')
        self.forward_to(t.end + 0.5)
        t = self.aas('42.mp3', '这也是为什么我们的教程面向 OpenGL3.3 的核心模式')

        self.prepare(Write(txt_33), at=2.3, duration=1.3)

        self.forward_to(t.end + 0.4)
        t = self.aas('43.mp3', '虽然上手更困难，但这份努力是值得的')
        self.forward_to(t.end + 2)


class CoreModeAndImmediateMode2(Template):
    def construct(self) -> None:
        #########################################################

        stick = Rect(
            0.5, Config.get.frame_height + 0.1,
            color=GREY,
            fill_alpha=0.8
        )

        box33 = Group(
            Rect(
                4.5, 0.7,
                color=BLUE,
                fill_alpha=0.6
            ),
            Text('OpenGL3.3')
        )

        more = Rect(
            3.5, 0.5,
            color=GOLD,
            fill_alpha=0.6
        )
        stack = Group(box33)

        #########################################################

        self.forward(0.5)
        t = self.aas('44.mp3', '由于更高版本的 OpenGL 都是基于 3.3 的')

        self.play(
            FadeIn(box33, scale=1.2),
            at=t.duration - 2,
            duration=2
        )

        self.forward_to(t.end + 0.3)
        t = self.aas('45.mp3', '没有改动核心架构')
        self.forward_to(t.end + 0.5)
        t = self.aas('46.mp3', '因此，所有的概念和技术在现代 OpenGL 版本里都保持一致')

        self.prepare(
            FadeIn(stick, UP * 5, rate_func=rush_from),
            duration=2,
            at=2
        )

        self.forward_to(t.end + 0.3)
        t = self.aas('47.mp3', '这也正是我们面向 OpenGL3.3 进行学习的原因')
        self.forward_to(t.end + 0.5)
        t = self.aas('48.mp3', '所有 OpenGL 更高的版本都是在 3.3 的基础上引入了额外的功能')

        self.forward(2.3)
        for _ in range(3):
            one = more.copy()
            one.points.next_to(stack, UP, buff=0)
            self.play(
                FadeIn(one, DOWN, rate_func=rush_into),
                duration=0.5
            )
            stack.add(one)
            self.play(
                stack.anim(rate_func=rush_from).points.shift(DOWN * 0.15),
                duration=0.2
            )

        self.forward_to(t.end + 0.4)

        #########################################################

        arrow = Vector(LEFT, color=BLUE)
        arrow.points.next_to(box33)

        tickbox = Square(
            0.5,
            stroke_color=GREY,
            fill_color=GREY_D,
            fill_alpha=1
        )
        tick = SVGItem('tick.svg', height=0.6)
        tickg = Group(tickbox, tick)

        cursor = SVGItem('cursor.svg', height=1)

        #########################################################

        t = self.aas('49.mp3', '当你的经验足够')

        self.prepare(
            GrowArrow(arrow),
            at=t.duration + 0.3 - 1,
        )

        self.forward_to(t.end + 0.3)
        t = self.aas('50.mp3', '你可以轻松使用来自更高版本 OpenGL 的新特性')

        self.prepare(
            arrow.anim
            .points.set_y(one.points.box.y)
            .r.color.set(GOLD),
            duration=2
        )

        self.forward_to(t.end + 0.5)
        t = self.aas('51.mp3', '但是，使用新版本的 OpenGL 特性时')
        self.forward_to(t.end + 0.3)
        t = self.aas('52.mp3', '只有新一代的显卡能够支持你的应用程序')
        self.forward_to(t.end + 0.4)
        t = self.aas('53.mp3', '这也是为什么大多数开发者基于较低版本的 OpenGL 编写程序')

        self.prepare(
            arrow.anim
            .points.set_y(box33.points.box.y)
            .r.color.set(BLUE),
            duration=2,
            at=1
        )

        self.forward_to(t.end + 0.4)
        t = self.aas('54.mp3', '并只提供选项启用新版本的特性')

        offset = 5 * LEFT
        tickg.points.next_to(stack[-2], buff=LARGE_BUFF)
        cursor.points.move_to(tickg).shift(DR * 0.4).shift(-offset)

        def click():
            self.play(
                cursor.anim(rate_func=rush_into)
                .points.scale(0.8, about_edge=UL),
                duration=0.1
            )
            self.play(
                cursor.anim(rate_func=rush_from)
                .points.scale(1 / 0.8, about_edge=UL),
                duration=0.1
            )

        self.play(FadeIn(tickbox, scale=0.8))
        self.play(cursor.anim(path_arc=-60 * DEGREES).points.shift(offset))
        click()
        tick.show()
        self.forward(2)

        # self.forward_to(t.end + 1)


class StateMachine_Subtitle(SubtitleTemplate):
    name = '状态机'


class StateMachine(Template):
    def construct(self) -> None:
        #########################################################

        border = Group(
            Text('状态机 <fs 0.8>State Machine</s>', format=Text.Format.RichText),
            Rect(8, 5, fill_color=GREY_E, fill_alpha=1)
        )
        border.points.arrange(DOWN)

        corners = [
            border[1].points.box.get(hor + UP)
            for hor in [LEFT, RIGHT]
        ]

        edges = Group(
            Line(corners[0], corners[0] + IN * 2),
            Line(corners[1], corners[1] + IN * 2),
            Line(corners[0] + IN * 2, corners[1] + IN * 2),
            color=GREY,
            depth=1
        )

        p1 = LEFT * 0.27 + DOWN * 0.2
        p2 = RIGHT * 0.27 + UP * 0.2

        circle_kw = dict(
            radius=0.05,
            stroke_radius=0.015,
            fill_alpha=1,
            fill_color=GREY_E
        )

        sd1 = Group(
            Rect(1, 1),
            Line(p1, p2),
            Circle(**circle_kw).points.move_to(p1).r,
            Circle(**circle_kw).points.move_to(p2).r
        )
        sd1.points.next_to(border[1].points.box.get(UL), DR)

        p1 = LEFT * 0.27 + DOWN * 0.1
        p2 = RIGHT * 0.05 + UP * 0.27
        p3 = RIGHT * 0.27 + DOWN * 0.2

        sd2 = Group(
            Rect(1, 1),
            Line(p1, p2),
            Line(p2, p3),
            Line(p3, p1),
            Circle(**circle_kw).points.move_to(p1).r,
            Circle(**circle_kw).points.move_to(p2).r,
            Circle(**circle_kw).points.move_to(p3).r,
        )
        sd2.points.next_to(sd1)

        srcpoints = [
            LEFT * 1.2,
            UP * 0.8 + LEFT * 0.2,
            DOWN * 0.6 + RIGHT * 0.2,
            RIGHT * 1.1 + DOWN * 0.5
        ]

        srcbox = Group(
            Square(3),
            *[
                Circle(**circle_kw).points.move_to(p).r
                for p in srcpoints
            ]
        )
        srcbox.points.next_to(border[1].points.box.get(DL), UR)

        arrow = Group(
            Rect(0.5, 0.4, fill_alpha=0.2),
            Typst('=>')
        )
        arrow.points.scale(1.5).set_y(srcbox.points.box.y)

        resbox = Group(
            Square(3),
            # [1]
            VItem().points.set_as_corners(srcpoints).r,
            # [2]
            Group(*[
                VItem(
                    stroke_color=GREY_E,
                    fill_color=WHITE,
                    fill_alpha=1
                ).points.set_as_corners(corners).close_path().r
                for corners in triplewise(srcpoints)
            ])
        )
        resbox.points.next_to(border[1].points.box.get(DR), UL)

        machineg = Group(border, edges, sd1, sd2, srcbox, arrow, resbox[0])

        cursor_offset = LEFT * 9.5 + UP * 2
        cursor = SVGItem('cursor.svg', height=1).show().fix_in_frame()
        cursor[1].color.set(BLUE_E)
        cursor.points.shift(UP * 0.6 + LEFT * 1.7 - cursor_offset)

        def click():
            self.play(
                cursor.anim(rate_func=rush_into)
                .points.scale(0.8, about_edge=UL),
                duration=0.1
            )
            self.play(
                cursor.anim(rate_func=rush_from)
                .points.scale(1 / 0.8, about_edge=UL),
                duration=0.1
            )

        #########################################################

        self.forward(0.5)
        t = self.aas('55.mp3', 'OpenGL 自身是一个巨大的状态机')

        self.schedule(self.current_time + 2.5, machineg.show)

        self.forward_to(t.end + 0.4)
        t = self.aas('56.mp3', '一系列的变量描述 OpenGL 此刻应当如何运行')

        t2 = self.play(
            self.camera.anim.points.rotate(30 * DEGREES, axis=LEFT)
        )
        self.prepare(
            cursor.anim(path_arc=-60 * DEGREES).points.shift(cursor_offset),
            at=t.duration - t2.duration - 1.5,
            duration=1.5
        )

        self.forward_to(t.end + 0.2)

        click()
        sd2_stat = sd2.copy()
        sd2(VItem).color.set(YELLOW)

        self.play(cursor.anim.points.shift(DR * 2))
        click()
        resbox[2].show()

        self.forward(0.3)

        t = self.aas('57.mp3', '假设我们想告诉 OpenGL 去画线段而不是三角形')
        self.forward_to(t.end + 0.4)
        t = self.aas('58.mp3', '我们通过改变一些上下文变量来改变 OpenGL 状态')

        cursor_offset = UL * 2 + LEFT * 1.4
        self.play(
            cursor.anim.points.shift(cursor_offset),
            at=2
        )
        click()
        sd2.become(sd2_stat)
        sd1(VItem).color.set(YELLOW)

        self.forward_to(t.end + 0.3)
        t = self.aas('59.mp3', '从而告诉 OpenGL 如何去绘图')
        self.forward_to(t.end + 0.5)
        t = self.aas('60.mp3', '一旦我们改变了 OpenGL 的状态为绘制线段')

        self.prepare(
            Flash(sd1, flash_radius=1, line_length=0.4),
            at=1.5,
            duration=2
        )

        self.forward_to(t.end + 0.3)
        t = self.aas('61.mp3', '下一个绘制命令就会画出线段而不是三角形')

        self.play(cursor.anim.points.shift(-cursor_offset))
        click()
        resbox[2].hide()
        resbox[1].show()

        self.forward_to(t.end + 0.7)
        t = self.aas('62.mp3', '当使用 OpenGL 的时候，我们会遇到一些状态设置函数')

        self.prepare(
            anim := ShowCreationThenFadeAround(
                Group(sd1, sd2),
                surrounding_rect_config=dict(
                    color=BLUE
                )
            ),
            at=2.2,
            duration=4
        )

        self.forward_to(t.end + 0.3)
        t = self.aas('63.mp3', '这类函数将会改变上下文')
        self.forward_to(t.end + 0.5)
        t = self.aas('64.mp3', '以及状态使用函数')

        self.prepare(
            ShowCreationThenFadeAround(
                arrow,
                surrounding_rect_config=dict(
                    color=BLUE
                )
            ),
            at=0.7,
            duration=4.5
        )

        self.forward_to(t.end + 0.3)
        t = self.aas('65.mp3', '这类函数会根据当前 OpenGL 的状态执行一些操作')
        self.forward_to(t.end + 0.5)
        t = self.aas('66.mp3', '只要你记住 OpenGL 本质上是个大状态机')

        self.prepare(
            cursor.anim(path_arc=50 * DEGREES).points.shift(RIGHT * 6 + DOWN * 3.4),
            self.camera.anim.points.rotate(30 * DEGREES, axis=RIGHT),
            at=0.8,
            duration=3
        )

        self.forward_to(t.end + 0.3)
        t = self.aas('67.mp3', '就能更容易理解它的大部分特性')
        self.forward_to(t.end + 1.5)


typ4_src = '''
#set par(first-line-indent: 2em, justify: true)
#set text(font: "Noto Sans S Chinese")
#set page(margin: 14.7em)
#par(box[])

在 LearnOpenGL 原文中，还提及了“扩展”和“对象”的小节，由于我们的侧重不在此或与我们将要使用的 ModernGL 无关，故略去。

若对这部分内容感兴趣，可以阅读原文章。
'''


class Other(TextDisplayTemplate):
    typ_src = typ4_src
