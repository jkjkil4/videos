# flake8: noqa
import random
import sys

sys.path.append('.')

from janim.imports import *

from utils.template import *

s1 = '<fs 0.7><c GREY_A>'
s2 = '</c></fs>'


class TitleTl(TitleTemplate):
    str1 = 'Learn OpenGL'
    str2 = '你好，三角形'


class Pipeline1(Template):
    def construct(self) -> None:
        #########################################################

        plane = NumberPlane(
            (-4, 4), (-4, 4),
            faded_line_ratio=2,
            background_line_style=dict(
                stroke_color=BLUE_E
            ),
            depth=2
        ).show()
        vecright = Vector(RIGHT * 2, depth=1, color=RED).show()
        vecup = Vector(UP * 2, depth=1, color=GREEN).show()
        vecout = Vector(OUT * 2, color=BLUE, tip_kwargs=dict(rotation=PI / 2)).show()

        #########################################################

        self.forward()
        self.prepare(
            self.camera.anim
                .points.rotate(60 * DEGREES, axis=RIGHT).rotate(30 * DEGREES, axis=OUT, absolute=True),
            duration=2
        )
        t = self.aas('1.mp3', '在 OpenGL 中')
        self.forward_to(t.end + 0.3)

        #########################################################

        cam = self.camera.copy()
        info = cam.points.info
        cam_loc = info.camera_location

        cam_rect = FrameRect(cam, depth=-1)
        cam_rect.points.scale(0.2, about_point=cam_loc)
        cam_lines = Group(
            *[
                Line(cam_loc, point)
                for point in cam_rect.points.get_anchors()
            ]
        )
        cam_dot = DotCloud(cam_loc, *cam_rect.points.get_anchors())

        #########################################################

        self.prepare(
            Write(cam_rect, duration=0.5),
            AnimGroup(
                FadeIn(cam_dot, duration=0.3),
                FadeIn(cam_lines, at=0.1, duration=0.3),
                self.camera.anim.points
                    .rotate(-3 * DEGREES, axis=info.horizontal_vect, absolute=True)
                    .rotate(20 * DEGREES, absolute=True)
                    .move_to(cam_loc * 0.3)
            ),
            at=0.8,
            lag_ratio=1
        )
        t = self.aas('2.mp3', '任何事物都在 3D 空间中')
        self.forward_to(t.end)
        self.forward(0.8)
        self.play(
            Rotate(self.camera, 80 * DEGREES, axis=UP),
            Group(cam_dot, cam_lines).anim
                .digest_styles(color=GREY),
            duration=2
        )

        #########################################################

        w = 16 * 2
        h = 9 * 2

        center = info.camera_location * 0.8
        hvec_half = info.horizontal_vect / 2 * 0.2
        vvec_half = info.vertical_vect / 2 * 0.2
        hunit = 0.01 * normalize(hvec_half)
        vunit = 0.01 * normalize(vvec_half)

        pixels = Group(
            *[
                VItem().points.set_as_corners([
                    center + h1 + v1 + hunit + vunit,
                    center + h1 + v2 + hunit - vunit,
                    center + h2 + v2 - hunit - vunit,
                    center + h2 + v1 - hunit + vunit,
                    center + h1 + v1 + hunit + vunit,
                ]).r
                for h1, h2 in it.pairwise(np.linspace(-hvec_half,
                                                      hvec_half,
                                                      w))
                for v1, v2 in it.pairwise(np.linspace(-vvec_half,
                                                      vvec_half,
                                                      h))
            ],
            stroke_alpha=0,
            fill_alpha=1,
            fill_color=BLUE,
            depth=-0.7
        ).shuffle()

        line = Line(ORIGIN, cam_loc, color=GOLD)

        def convert_mapped_point(x: float, y: float) -> np.ndarray:
            return center + hvec_half * x + vvec_half * y

        square = Square(4, stroke_alpha=0, fill_alpha=1, depth=1.5, color=GOLD)
        mapped_square = VItem(
            *[
                convert_mapped_point(x, y)
                for x, y in info.map_points(square.points.get())
            ],
            color=RED,
            depth=-2
        )

        #########################################################

        self.prepare(
            FadeIn(pixels, lag_ratio=0.01),
            at=1.3
        )

        t = self.aas('3.mp3', '而屏幕和窗口却是 2D 像素数组')
        self.forward_to(t.end + 0.5)

        self.prepare(FadeIn(square, scale=0.8), at=1)

        t = self.aas('4.mp3', '这导致 OpenGL 的大部分工作')
        self.forward_to(t.end + 0.3)

        self.prepare(
            Create(mapped_square, auto_close_path=False, duration=3),
            ItemUpdater(
                None,
                lambda p: Line(
                    convert_mapped_point(*info.map_points([square.points.pfp(p.alpha)])[0]),
                    square.points.pfp(p.alpha),
                    color=RED,
                    alpha=0.7,
                    depth=-1
                ),
                duration=3
            ),
            ItemUpdater(
                None,
                lambda p: Line(
                    cam_loc,
                    square.points.pfp(p.alpha),
                    color=RED,
                    alpha=0.8,
                    depth=-0.5
                ),
                duration=3
            ),
            ItemUpdater(
                None,
                lambda p: DotCloud(
                    square.points.pfp(p.alpha),
                    color=RED,
                    radius=0.1
                ),
                duration=3
            ),
            at=1
        )

        t = self.aas('5.mp3', '都是关于把 3D 坐标转变为适应你屏幕的 2D 像素')
        self.forward_to(t.end)

        stat = self.camera.copy()

        self.play(
            mapped_square.anim
                .fill.set(alpha=0.7)
                .r.stroke.set(alpha=0),
            FadeOut(pixels),
            FadeOut(cam_lines),
            self.camera.anim.become(cam),
            duration=1
        )
        self.forward()

        self.camera.become(stat)
        cam_lines.show()

        #########################################################

        arrow = Arrow(RIGHT, LEFT * 3 + UP * 0.2).fix_in_frame()
        tip = Text(
            '（Graphics Pipeline，大多译为管线，实际上指的是一堆原始图形数据途经一个输送管道，期间经过各种变化处理最终出现在屏幕的过程）',
            font_size=12,
            color=GREY
        ).fix_in_frame()
        tip.points.to_border(UL)

        #########################################################

        self.prepare(
            GrowArrow(arrow),
            at=1
        )
        t = self.aas('6.mp3', '3D 坐标转为 2D 坐标的处理过程')
        self.forward_to(t.end + 0.3)

        t = self.aas('7.mp3', '是由 OpenGL 的图形渲染管线管理的')
        tip.show()
        self.forward_to(t.end)
        tip.hide()

        self.play(
            self.camera.anim.points
                .shift(self.camera.points.info.vertical_vect * -0.2)
                .rotate(-8 * DEGREES, axis=RIGHT),
            arrow.anim.points.shift(UP * 1.6),
            plane(VItem).anim.color.fade(0.5)
        )

        #########################################################

        coords3d = Group(vecright, vecup, vecout).copy().fix_in_frame()
        coords3d.points \
            .rotate(-50 * DEGREES, axis=RIGHT) \
            .rotate(-30 * DEGREES, axis=UP) \
            .rotate(-40 * DEGREES) \
            .shift(DL * 2 + LEFT * 2) \
            .scale(0.5)
        coords3d[-1].tip.points.rotate(PI / 2, axis=coords3d[-1].points.end_direction)

        coords3d_txt = Text('3D 坐标').fix_in_frame()
        coords3d_txt.points.next_to(coords3d, DOWN, coor_mask=(1, 1, 0)).shift(LEFT * 0.2 + DOWN * 0.1)

        coords2d = Group(vecright, vecup).copy().fix_in_frame()
        coords2d.points \
            .set_x(0) \
            .shift(DOWN * 2.8) \
            .scale(0.6)

        coords2d_txt = Text('2D 坐标').fix_in_frame()
        coords2d_txt.points.next_to(coords2d, DOWN)

        sq = partial(Square, 0.3, stroke_alpha=0, fill_alpha=1)

        pixels = Group(
            sq(color=PURPLE),
            sq(color=MAROON),
            sq(color=YELLOW_B),
            sq(color=LIGHT_PINK)
        ).fix_in_frame()
        pixels.points.arrange_in_grid(buff=0.1).shift(RIGHT * 4 + DOWN * 1.9)

        pixels_txt = Text('有颜色的像素').fix_in_frame()
        pixels_txt.points.next_to(pixels, DOWN, buff=0.45)

        arrow1 = Arrow(
            LEFT * 3 + DOWN * 1.9,
            LEFT + DOWN * 1.9
        ).fix_in_frame()
        arrow2 = Arrow(
            RIGHT + DOWN * 1.9,
            RIGHT * 3 + DOWN * 1.9
        ).fix_in_frame()

        def get_multi_arrow(arrow: Arrow) -> Group[Arrow]:
            arrows = arrow * 10
            arrows.points.arrange_by_offset(DOWN * 0.05, center=False)
            for i, ar in enumerate(arrows):
                fade = i / len(arrows)
                ar.color.fade(fade)
            return arrows

        arrows1 = get_multi_arrow(arrow1)
        arrows2 = get_multi_arrow(arrow2)

        def get_txts(text: str, font_size=12):
            prog1 = Group(
                txt := Text(text, font_size=font_size, depth=-19),
                SurroundingRect(
                    txt,
                    fill_alpha=1,
                    fill_color=GREY,
                    stroke_color=PURPLE_A,
                    depth=-9
                )
            ).fix_in_frame()
            prog1.points.move_to(arrows1)

            prog2 = prog1.copy()
            prog2.points.move_to(arrows2)

            progs = Group(prog1, prog2)
            progs.points.shift(LEFT * 0.1)
            return progs

        progs = get_txts('程\n序')
        prog1, prog2 = progs

        shaders = get_txts('着\n色\n器', font_size=15)
        shader1, shader2 = shaders

        arrow_bodies = Group(
            *[
                arrow.copy(root_only=True)
                for arrow in it.chain(arrows1, arrows2)
            ]
        )

        highlight = boolean_ops.Difference(
            FrameRect(),
            boolean_ops.Union(
                SurroundingRect(Group(shader1, arrows1)),
                SurroundingRect(Group(shader2, arrows2))
            ),
            stroke_alpha=0,
            fill_alpha=0.7,
            color=BLACK,
            depth=-100
        ).fix_in_frame()

        #########################################################

        t = self.aas('8.mp3', '图形渲染管线可以被划分为两个主要部分：')
        self.forward_to(t.end + 0.7)

        self.schedule(self.current_time + 1, lambda: self.show(coords3d, coords3d_txt))
        self.schedule(self.current_time + 3, lambda: self.show(arrow1, coords2d, coords2d_txt))

        t = self.aas('9.mp3', '第一部分把你的 3D 坐标转换为屏幕上的 2D 坐标')
        self.forward_to(t.end + 0.7)

        self.schedule(self.current_time + 3, lambda: self.show(arrow2, pixels, pixels_txt))

        t = self.aas('10.mp3', '第二部分是把 2D 坐标转变为实际的有颜色的像素')
        self.forward_to(t.end + 0.9)

        self.prepare(
            *[
                GrowArrow(ar, rate_func=rush_from)
                for ar in it.chain(arrows1, arrows2)
            ],
            at=1.4
        )

        t = self.aas('11.mp3', '图形渲染管线具有并行执行的特性')
        self.forward_to(t.end + 0.4)
        t = self.aas('12.mp3', '当今大多数显卡都有成千上万的小处理核心')
        self.forward_to(t.end + 0.3)

        self.prepare(
            FadeIn(prog1),
            FadeIn(prog2),
            at=3
        )

        t = self.aas('13.mp3', '它们在 GPU 上为每一个（渲染管线）阶段运行各自的小程序')
        self.forward_to(t.end + 0.3)

        self.prepare(
            *[
                ShowPassingFlash(arrow_bodies, rate_func=linear, duration=0.5)
                for _ in range(6)
            ],
            lag_ratio=0.3,
            at=1.5
        )

        t = self.aas('14.mp3', '从而在图形渲染管线中快速处理你的数据')
        self.forward_to(t.end + 0.6)

        self.prepare(
            Transform(prog1, shader1),
            Transform(prog2, shader2),
            at=1
        )

        t = self.aas('15.mp3', '这些小程序叫做着色器（Shader）')
        self.forward_to(t.end + 0.4)

        self.prepare(
            ShowPassingFlashAround(shader1, duration=2),
            at=1
        )

        t = self.aas('16.mp3', '规定了 3D 坐标是如何转换到 2D 坐标')
        self.forward_to(t.end + 0.3)

        self.prepare(
            ShowPassingFlashAround(shader2, duration=2),
            at=1
        )

        t = self.aas('17.mp3', '以及 2D 坐标如何转变为实际像素的')
        self.forward_to(t.end + 0.7)
        t = self.aas('18.mp3', '有些着色器可以由开发者配置')
        self.forward_to(t.end + 0.4)

        self.prepare(FadeIn(highlight), at=3)

        t = self.aas('19.mp3', '因为允许用 OpenGL 着色器语言(GLSL)编写着色器来代替默认的')
        self.forward_to(t.end + 0.3)
        t = self.aas('20.mp3', '这样就能够更细致地控制')
        self.forward_to(t.end)
        t = self.aas('21.mp3', '图形渲染管线中的特定部分了',
                     clip=(0.3, 2.4))
        self.forward_to(t.end + 0.8)

        self.prepare(FadeOut(highlight), at=1.5)

        t = self.aas('22.mp3', '在之后我们再具体研究 GLSL')
        self.forward_to(t.end + 0.5)
        t = self.aas('23.mp3', '在这一节我们先了解一下基本的概念')
        self.forward_to(t.end + 0.4)
        t = self.aas('24.mp3', '并且使用最简单的例子画出一个三角形')
        self.forward_to(t.end)

        self.forward()


class Pipeline2(Template):
    def construct(self) -> None:
        #########################################################

        pipeline = ImageItem('pipeline.png', height=4).show()

        hl_blue = boolean_ops.Difference(
            FrameRect(),
            VItem().points.set_as_corners([
                ORIGIN,
                LEFT * 1.7,
                UL * 1.7 + UP * 0.3,
                UR * 1.7 + UP * 0.3,
                DR * 1.7 + DOWN * 0.4,
                DOWN * 2.1,
                ORIGIN
            ]).r,
            **HighlightRect.difference_config_d
        )

        hl_one = boolean_ops.Difference(
            Rect(20, 20),
            Rect(1.6, 2)
                .points.shift(LEFT * 0.885 + UP)
                .r,
            **HighlightRect.difference_config_d
        )

        #########################################################

        self.forward()

        t = self.aas('25.mp3', '这是图形渲染管线每个阶段的抽象展示')
        self.forward_to(t.end + 0.7)

        self.prepare(FadeIn(hl_blue), at=1)

        t = self.aas('26.mp3', '要注意蓝色部分代表的是',
                     clip=(0.4, 2.3))
        self.forward_to(t.end)

        t = self.aas('27.mp3', '我们可以注入自定义的着色器的部分')
        self.forward_to(t.end)

        self.play(FadeOut(hl_blue))

        t = self.aas('28.mp3', '如你所见，图形渲染管线包含很多部分')
        self.forward_to(t.end + 0.4)

        self.prepare(FadeIn(hl_one), duration=0.8)
        self.prepare(hl_one.anim.points.shift(RIGHT * 1.73), duration=0.8, at=0.8)
        self.prepare(hl_one.anim.points.shift(RIGHT * 1.7), duration=0.8, at=1.6)
        self.prepare(hl_one.anim.points.shift(DOWN * 2.1), duration=0.8, at=2.4)
        self.prepare(hl_one.anim.points.shift(LEFT * 1.7), duration=0.8, at=3.2)
        self.prepare(hl_one.anim.points.shift(LEFT * 1.73), duration=0.8, at=4.0)
        self.prepare(FadeOut(hl_one), duration=0.8, at=4.8)

        t = self.aas('29.mp3', '每个部分都将在转换顶点数据到最终像素这一过程中')
        self.forward_to(t.end)
        t = self.aas('30.mp3', '处理各自特定的阶段')
        self.forward_to(t.end + 0.6)
        t = self.aas('31.mp3', '我概括性地解释一下渲染管线的每个部分')
        self.forward_to(t.end + 0.3)
        t = self.aas('32.mp3', '让你对图形渲染管线的工作方式有个大概了解')
        self.forward_to(t.end + 0.7)
        t = self.aas('33.mp3', '注意这只是概括性的哈',
                     clip=(0.3, 1.9))
        self.forward_to(t.end + 0.4)
        t = self.aas('34.mp3', '一些具体处理不太懂很正常')
        self.forward_to(t.end + 0.3)
        t = self.aas('35.mp3', '之后我们还要具体再学的')
        self.forward_to(t.end + 0.4)

        self.prepare(
            pipeline.anim.points.scale(3).shift(DOWN * 2.7 + RIGHT * 10),
            duration=3
        )

        t = self.aas('36.mp3', '这里只是过一遍流程让你有个整体的概念')
        self.forward_to(t.end + 0.8)

        #########################################################

        dot = Group(
            Dot(),
            Typst('(x,y,z) space (#text(fill: red)[r],#text(fill: green)[g],#text(fill: blue)[b])')
        )
        dot.points.arrange(LEFT)

        dots = dot * 3
        dots.points.arrange(DOWN, buff=MED_LARGE_BUFF).shift(LEFT * 2)

        rect1 = SurroundingRect(Group(*[dot[0] for dot in dots]), color=GREY, buff=MED_LARGE_BUFF)
        rect2 = SurroundingRect(dots, color=GREY, buff=MED_LARGE_BUFF)

        tip = Text('顶点(Vertex)', color=GREY)
        tip.points.shift(RIGHT * 0.2 + UP * 2.3)
        tiparrow = Arrow(tip, dots[0][0], color=GREY)

        frag_tip = Text(
            'OpenGL 中的一个片段是渲染一个像素所需的所有数据\n'
            '片段着色器是处理单个像素的，我们会对屏幕上的每一个像素都使用一遍片段着色器',
            font_size=16,
            stroke_alpha=1,
            stroke_color=BLACK,
            stroke_background=True,
            fill_color=GREY_A
        ).fix_in_frame()
        # frag_tip.points.arrange(DOWN, aligned_edge=RIGHT, buff=SMALL_BUFF)
        # frag_tip.points.to_border(UR)
        frag_tip.points.to_border(UL)

        #########################################################

        self.prepare(
            Write(Group(*[dot[0] for dot in dots]), lag_ratio=0.3),
            at=2
        )

        t = self.aas('37.mp3', '首先，我们以数组的形式传递 3 个 3D 坐标')
        self.forward_to(t.end + 0.3)
        t = self.aas('38.mp3', '作为图形渲染管线的输入')
        self.forward_to(t.end + 0.1)

        self.prepare(
            self.camera.anim.points.shift(RIGHT * 3),
            at=0.4
        )

        t = self.aas('39.mp3', '用来表示一个三角形')
        self.forward_to(t.end)

        self.prepare(
            self.camera.anim.points.shift(LEFT * 3),
            at=0.4,
            duration=2
        )
        self.forward(0.6)
        self.prepare(
            Create(
                rect1,
                auto_close_path=False
            ),
            at=1
        )
        self.prepare(
            Write(tip),
            GrowArrow(tiparrow),
            at=2.5
        )

        t = self.aas('40.mp3', f'这个数组叫做顶点数据{s1}（Vertex Data）{s2}',
                     format=Text.Format.RichText)
        self.forward_to(t.end + 0.3)
        t = self.aas('41.mp3', '它是一系列顶点的集合')
        self.forward_to(t.end + 0.5)
        t = self.aas('42.mp3', f'一个顶点的数据是用顶点属性{s1}（Vertex Attribute）{s2}表示的',
                     format=Text.Format.RichText)
        self.forward_to(t.end + 0.3)
        t = self.aas('43.mp3', '它可以包含任何我们想用的数据')
        self.forward_to(t.end + 0.2)
        t = self.aas('44.mp3', '但是简单起见，我们还是假定')
        self.forward_to(t.end)

        self.prepare(
            Transform(rect1, rect2),
            AnimGroup(
                *[
                    DrawBorderThenFill(dot[1])
                    for dot in dots
                ],
            ),
            lag_ratio=0.7,
            at=1
        )

        t = self.aas('45.mp3', '每个顶点只由一个 3D 位置和一些颜色值组成吧')
        self.forward_to(t.end + 0.6)

        self.prepare(
            FadeOut(Group(rect2, tip, tiparrow, *[dot[1] for dot in dots])),
            FadeOut(Group(*[dot[0] for dot in dots]), RIGHT * 6),
            self.camera.anim.points.shift(RIGHT * 7).scale(1.3),
            at=0.5,
            duration=2
        )

        t = self.aas('46.mp3', f'图形渲染管线的第一个部分是顶点着色器{s1}（Vertex Shader）{s2}',
                     format=Text.Format.RichText)
        self.forward_to(t.end + 0.4)
        t = self.aas('47.mp3', '它把一个单独的顶点作为输入')
        self.forward_to(t.end + 0.4)

        self.prepare(
            CircleIndicate(Dot(RIGHT * 6.03 + DOWN * 0.58), scale=1.2),
            CircleIndicate(Dot(RIGHT * 8.23 + UP * 1.26), scale=1.2),
            CircleIndicate(Dot(RIGHT * 8.36 + DOWN * 1.15), scale=1.2),
            lag_ratio=0.4,
            at=0.8,
            duration=3
        )

        t = self.aas('48.mp3', '并允许你将这个顶点进行一些操作和变换（之后会具体解释）')
        self.forward_to(t.end + 0.3)
        t = self.aas('49.mp3', '以及对顶点属性进行一些基本处理')
        self.forward_to(t.end)

        self.prepare(
            self.camera.anim.points.shift(RIGHT * 5),
            duration=2
        )
        self.forward(0.6)

        t = self.aas('50.mp3', '几何着色器是可选的（也就是可以不写）')
        self.forward_to(t.end + 0.4)
        t = self.aas('51.mp3', '允许我们根据顶点着色器传递过来的点')
        self.forward_to(t.end + 0.3)

        self.prepare(
            ShowCreationThenDestruction(
                Rect(2.5, 0.4, color=YELLOW)
                    .points.shift(RIGHT * 13.12 + DOWN * 0.63).rotate(-50 * DEGREES)
                    .r
            ),
            duration=2
        )

        t = self.aas('52.mp3', '去生成新的几何结构')
        self.forward_to(t.end)

        self.play(
            self.camera.anim.points.shift(RIGHT * 5),
            duration=0.7
        )
        self.play(
            self.camera.anim.points.shift(DOWN * 6),
            duration=0.7
        )
        self.play(
            self.camera.anim.points.shift(LEFT * 5),
            duration=0.7
        )

        t = self.aas('53.mp3', '片段着色器的主要目的是')
        self.forward_to(t.end)
        t = self.aas('54.mp3', '计算一个像素的最终颜色')
        self.forward_to(t.end + 0.4)
        t = self.aas('55.mp3', '这也是所有 OpenGL 高级效果产生的地方')
        self.forward_to(t.end + 0.4)
        t = self.aas('56.mp3', '通常，片段着色器包含 3D 场景的数据（比如光照、阴影、光的颜色等等）')
        self.forward_to(t.end + 0.3)
        t = self.aas('57.mp3', '这些数据可以被用来计算最终像素的颜色')
        self.forward_to(t.end + 0.5)
        t = self.aas('58.mp3', '并且，由于大部分传递给片段着色器的数据都会被插值')
        self.forward_to(t.end + 0.4)

        self.prepare(
            self.camera.anim.points.shift(UP * 2),
            duration=2,
            at=0.5
        )

        t = self.aas('59.mp3', '所以即使前面传入的是分散的点')
        self.forward_to(t.end + 0.3)

        self.prepare(
            self.camera.anim.points.shift(DOWN * 2),
            duration=2,
            at=0.8
        )
        frag_tip.show()

        t = self.aas('60.mp3', '这里也会由于插值的缘故得到连续的坐标和颜色')
        self.forward_to(t.end + 0.8)

        frag_tip.hide()
        self.prepare(
            self.camera.anim.points.move_to(pipeline).scale(2),
            duration=2,
            at=0.5
        )

        t = self.aas('61.mp3', '可以看到，图形渲染管线非常复杂')
        self.forward_to(t.end + 0.3)

        #########################################################

        highlight = boolean_ops.Difference(
            FrameRect(self.camera),
            boolean_ops.Union(
                Rect([5.04, 3.29, 0], [14.96, -2.63, 0]),
                Rect([10.19, 3.17, 0], [15.06, -8.96, 0])
            ),
            **HighlightRect.difference_config_d
        )

        path1 = VItem(
            [4.87, 2.28, 0], [4.2, -0.32, 0], [4.68, -1.62, 0], [5.41, -2.92, 0], [6.8, -2.92, 0],
            [8.22, -2.77, 0], [9.25, -1.57, 0], [10.04, -0.2, 0], [9.83, 1.37, 0], [9.37, 2.86, 0],
            [8.29, 3.54, 0], [7.24, 3.73, 0], [6.41, 3.25, 0], [5.77, 3.04, 0], [5.74, 2.72, 0],
            stroke_radius=0.06,
            color=YELLOW
        )
        path2 = VItem(
            [10.19, -3.81, 0], [9.37, -6.14, 0], [10, -7.42, 0], [11.07, -8.81, 0], [12.7, -8.91, 0],
            [14.08, -8.75, 0], [14.77, -7.32, 0], [15.27, -5.47, 0], [14.67, -3.76, 0], [13.72, -2.72, 0],
            [12.31, -2.75, 0], [11.12, -2.83, 0], [10.39, -3.42, 0], [9.77, -3.86, 0], [9.86, -4.48, 0],
            stroke_radius=0.06,
            color=YELLOW
        )

        #########################################################

        self.prepare(FadeIn(highlight), at=0.5)

        t = self.aas('62.mp3', '它包含很多可配置的部分')
        self.forward_to(t.end)

        self.prepare(FadeOut(highlight))
        self.forward(0.5)

        t = self.aas('63.mp3', '然而，对于大多数场合')
        self.forward_to(t.end + 0.3)

        self.prepare(
            Create(path1),
            Create(path2),
            lag_ratio=0.5,
            at=1.3
        )

        t = self.aas('64.mp3', '我们只需要配置顶点和片段着色器就行了')
        self.forward_to(t.end + 0.4)
        t = self.aas('65.mp3', '几何着色器是可选的')
        self.forward_to(t.end)
        t = self.aas('66.mp3', '通常使用它默认的着色器就行',
                     clip=(0.4, 2.6))
        self.forward_to(t.end + 0.5)
        t = self.aas('67.mp3', '在现代 OpenGL 中')
        self.forward_to(t.end + 0.2)
        t = self.aas('68.mp3', '我们必须定义至少一个顶点着色器和一个片段着色器（因为GPU中没有默认的顶点/片段着色器）')
        self.forward_to(t.end + 0.4)
        t = self.aas('69.mp3', '出于这个原因')
        self.forward_to(t.end + 0.3)
        t = self.aas('70.mp3', '刚开始学习现代 OpenGL 的时候可能会非常困难')
        self.forward_to(t.end + 0.3)
        t = self.aas('71.mp3', '因为在你能够渲染自己的第一个三角形之前已经需要了解一大堆知识了')
        self.forward_to(t.end + 0.5)
        t = self.aas('72.mp3', '在本节结束你最终渲染出你的三角形的时候')
        self.forward_to(t.end + 0.2)

        self.prepare(
            FadeOut(path1),
            FadeOut(path2)
        )

        t = self.aas('73.mp3', '你也会了解到非常多的图形编程知识')
        self.forward_to(t.end)

        self.forward()


code1_src = '''
<fc #9cdcfe>vertices</fc> <fc #d4d4d4>=</fc> <fc #4ec9b0>np</fc><fc #cccccc>.</fc><fc #dcdcaa>array</fc><fc #cccccc>([</fc>
    <fc #d4d4d4>-</fc><fc #b5cea8>0.5</fc><fc #cccccc>, </fc><fc #d4d4d4>-</fc><fc #b5cea8>0.5</fc><fc #cccccc>, </fc><fc #b5cea8>0.0</fc><fc #cccccc>,</fc>
     <fc #b5cea8>0.5</fc><fc #cccccc>, </fc><fc #d4d4d4>-</fc><fc #b5cea8>0.5</fc><fc #cccccc>, </fc><fc #b5cea8>0.0</fc><fc #cccccc>,</fc>
     <fc #b5cea8>0.0</fc><fc #cccccc>,  </fc><fc #b5cea8>0.5</fc><fc #cccccc>, </fc><fc #b5cea8>0.0</fc>
<fc #cccccc>], </fc><fc #9cdcfe>dtype</fc><fc #d4d4d4>=</fc><fc #ce9178>'f4'</fc><fc #cccccc>)</fc>
'''


class VertexInput(Template):
    def construct(self) -> None:
        #########################################################

        cam_stat = self.camera.copy()

        pipeline = ImageItem('pipeline.png', height=4.8).show()
        cover = boolean_ops.Difference(
            Rect([-4.26, 2.61, 0], [4.17, -2.72, 0]),
            Rect([-2.33, 0.72, 0], [-4.07, 1.5, 0]),
            stroke_alpha=0,
            fill_alpha=1,
            color=BLACK
        )
        g = Group(pipeline, cover, depth=10000).fix_in_frame()
        g_stat = g.copy()

        axis_x = NumberLine(
            (-1, 1, 1),
            unit_size=2,
            numbers_to_exclude=[0],
            include_numbers=True
        )
        axis_y = axis_x.copy()
        axis_y.points.rotate(PI / 2, about_point=ORIGIN)
        axis_z = axis_y.copy()
        axis_z.points.rotate(PI / 2, about_point=ORIGIN, axis=RIGHT)

        axisg = Group(axis_x, axis_y, axis_z)

        #########################################################

        self.forward()

        t = self.aas('74.mp3', '开始绘制图形之前')
        self.forward_to(t.end + 0.2)

        self.prepare(FadeIn(cover))
        self.prepare(
            g.anim.points.shift(LEFT * 2.5 + DOWN * 4),
            at=1.5
        )

        t = self.aas('75.mp3', '我们需要先给 OpenGL 输入一些顶点数据')
        self.forward_to(t.end + 0.7)

        t = self.aas('76.mp3', 'OpenGL 是一个 3D 图形库')
        self.forward_to(t.end + 0.2)

        self.prepare(
            *[
                AnimGroup(
                    Write(axis, root_only=True),
                    Write(axis.ticks)
                )
                for axis in axisg
            ],
            self.camera.anim.points
                .rotate(40 * DEGREES, axis=RIGHT)
                .rotate(30 * DEGREES, axis=OUT, absolute=True),
            at=1.5,
            duration=2
        )

        t = self.aas('77.mp3', f'所以在 OpenGL 中我们指定的所有坐标都是 3D 坐标{s1}（x、y 和 z）{s2}',
                     format=Text.Format.RichText)
        self.forward_to(t.end + 0.5)
        t = self.aas('78.mp3', 'OpenGL 仅当最终输出的 3D 坐标')
        self.forward_to(t.end)

        self.prepare(
            *[
                Write(axis.numbers)
                for axis in axisg
            ],
            at=1
        )

        t = self.aas('79.mp3', f'在 3 个轴{s1}（x、y 和 z）{s2}上的值在 -1.0 到 1.0',
                     clip=(0.3, 2.7), format=Text.Format.RichText)
        self.forward_to(t.end)
        t = self.aas('80.mp3', '的范围内时才处理它',
                     clip=(0.35, 2.0))
        self.forward_to(t.end + 0.5)

        #########################################################

        cam_stat2 = self.camera.copy()

        vertices = np.array([
            -0.5, -0.5, 0.0,
             0.5, -0.5, 0.0,
             0.0,  0.5, 0.0
        ], dtype='f4')
        vertices = vertices.reshape((3, 3)) * 2
        tri = VItem(stroke_radius=0.01)
        tri.points.set_as_corners(vertices).close_path()

        verts = DotCloud(*vertices, radius=0.1)
        code1 = Text(
            code1_src,
            font_size=16,
            format=Text.Format.RichText,
            depth=-20
        ).fix_in_frame()
        code1.points.to_border(UL)

        z_coords = Group(
            code1[2][16:19],
            code1[3][16:19],
            code1[4][16:19]
        ).fix_in_frame()

        z = Typst('z', color=YELLOW).fix_in_frame()
        z.points.next_to(z_coords, DOWN)

        tip = Text(
            '<fa 0.5>注：这里用到 <fc #4ec9b0>np</fc> 需要你在代码开头加上 <fc #c586c0>import</fc> <fc #4ec9b0>numpy</fc> <fc #c586c0>as</fc> <fc #4ec9b0>np</fc></fa>',
            font_size=12,
            format=Text.Format.RichText
        ).fix_in_frame()
        tip.points.next_to(code1, RIGHT, aligned_edge=UP)

        #########################################################

        t = self.aas('81.mp3', '所有在这个范围内的坐标叫做')
        self.forward_to(t.end)
        t = self.aas(
            '82.mp3',
            [
                '标准化设备坐标',
                '<c GREY_A>(Normalized Device Coordinates)</c>'
            ],
            scale=[1, 0.7],
            format=Text.Format.RichText
        )
        self.forward_to(t.end + 0.4)

        self.prepare(
            self.camera.anim.become(cam_stat),
            at=0.5,
            duration=2
        )

        t = self.aas(
            '83.mp3',
            [
                '此范围内的坐标最终显示在屏幕上',
                '<c GREY_A>（在这个范围以外的坐标则不会显示）</c>'
            ],
            scale=[1, 0.7],
            format=Text.Format.RichText
        )
        self.forward_to(t.end + 0.5)

        self.prepare(
            Create(tri, auto_close_path=False),
            at=1
        )

        t = self.aas('84.mp3', '由于我们希望渲染一个三角形')
        self.forward_to(t.end + 0.2)

        self.prepare(
            FadeIn(verts),
            at=0.6
        )

        t = self.aas('85.mp3', '一共要指定三个顶点')
        self.forward_to(t.end + 0.3)

        self.prepare(
            self.camera.anim.become(cam_stat2),
            duration=2
        )

        t = self.aas('86.mp3', '每个顶点都有一个 3D 位置')
        self.forward_to(t.end + 0.5)
        t = self.aas('87.mp3', '我们会将它们以标准化设备坐标的形式')
        self.forward_to(t.end)

        self.prepare(
            Write(code1),
            FadeIn(tip),
            at=0.5,
            lag_ratio=0.5
        )

        t = self.aas('88.mp3', '定义为一个 numpy 数组')
        self.forward_to(t.end + 0.4)

        self.prepare(
            *[
                ShowCreationThenDestruction(
                    Underline(code_line, buff=0.02, color=YELLOW).fix_in_frame()
                )
                for code_line in code1[2:5]
            ],
            lag_ratio=0.1,
            at=0.4
        )

        t = self.aas('89.mp3', '它定义了三个坐标')
        self.forward_to(t.end + 0.3)

        self.prepare(
            FocusOn(code1[5][9:13].fix_in_frame())
        )

        t = self.aas('90.mp3', '这里 dtype=\'f4\' 表示每个坐标分量',
                     clip=(0.3, 3.65))
        self.forward_to(t.end)
        t = self.aas('91.mp3', f'都是用 4 字节的浮点数{s1}(float){s2}存储的',
                     format=Text.Format.RichText)
        self.forward_to(t.end + 0.6)
        t = self.aas('92.mp3', '明确每个分量所占的字节数很重要')
        self.forward_to(t.end + 0.2)
        t = self.aas('93.mp3', '因为使用 GPU 进行图形渲染涉及到传递规定长度的数据')
        self.forward_to(t.end + 0.6)

        self.prepare(
            ShowCreationThenFadeOut(
                axisg.copy()(VItem)
                    .color.set(YELLOW).r
                    .depth.arrange(-10).r,
            ),
            at=0.7
        )

        t = self.aas('94.mp3', '由于 OpenGL 是在 3D 空间中工作的')
        self.forward_to(t.end + 0.3)

        self.prepare(
            Indicate(Group(tri, verts), scale_factor=1.1),
            at=1
        )

        t = self.aas('95.mp3', '而我们渲染的是一个 2D 三角形')
        self.forward_to(t.end + 0.4)

        self.prepare(
            ShowCreationThenFadeAround(z_coords),
            AnimGroup(
                FadeIn(z, duration=0.5),
                FadeOut(z, duration=0.5, at=1.5)
            ),
            at=1,
            duration=3
        )

        t = self.aas('96.mp3', '所以这里将它这几个顶点的z坐标都设置为 0.0')
        self.forward_to(t.end + 0.2)

        t = self.prepare(
            self.camera.anim.become(cam_stat),
            at=0.5,
            duration=2
        )
        self.schedule(t.end, axis_z.hide)

        t = self.aas('97.mp3', '从而使它看上去像是 2D 的')
        self.forward_to(t.end + 1)

        #########################################################

        axisg = Group(axis_x, axis_y)

        for axis in axisg:
            for v in axis.numbers:
                v.set_stroke_background(True)
            axis.numbers(VItem).stroke.set(BLACK, 1)

        window = ImageItem('window-col.png', depth=1)

        #########################################################

        t = self.aas('98.mp3', '当显示到窗口上时')
        self.forward_to(t.end + 0.3)
        t = self.aas('99.mp3', '我们现在看到的这个标准化设备坐标')
        self.forward_to(t.end)

        self.prepare(
            FadeIn(window),
            Group(axisg, tri, verts).anim
                .points.set_size(6.55, 4.9)
                       .shift(LEFT * 0.01 + DOWN * 0.13),
            lag_ratio=0.4
        )

        t = self.aas('100.mp3', '会直接被拉伸到视口上')
        self.forward_to(t.end + 0.7)

        #########################################################

        x = Typst('x', width=0.3)
        x.points.next_to(axis_x, item_root_only=True)

        y = Typst('y', width=0.3)
        y.points.next_to(axis_y, UP, item_root_only=True)

        xy = Group(x, y)
        xy.digest_styles(stroke_color=BLACK, stroke_alpha=1, stroke_background=True)

        verts_color = (LIGHT_PINK, YELLOW_E, PURPLE)

        rects = Group(*[
            SurroundingRect(
                line if line is code1[4] else line[:-1],
                buff=0.025,
                stroke_alpha=0,
                fill_alpha=0.5,
                depth=-10,
                color=c
            )
            for line, c in zip(code1[2:5], verts_color)
        ])

        dots = Group(*[
            Dot(pos, color=c, depth=-10)
            for pos, c in zip(verts.points.get(), verts_color)
        ])

        #########################################################

        t = self.aas('101.mp3', '在我们的例子中便是拉伸到全窗口画面')
        self.forward_to(t.end + 0.5)

        self.prepare(
            FadeIn(xy, lag_ratio=0.5)
        )

        t = self.aas('102.mp3', '这也意味着它与通常的屏幕坐标不同')
        self.forward_to(t.end + 0.3)

        self.prepare(
            ShowCreationThenDestruction(
                axis_y.store()
                    .depth.set(-1)
                    .r.color.set(YELLOW)
                    .r.radius.set(0.04)
                    .r,
                root_only=True
            ),
            duration=2
        )

        t = self.aas('103.mp3', '它的 y 轴正方向为向上')
        self.forward_to(t.end + 0.2)

        self.prepare(
            CircleIndicate(
                SmallDot(axis_x.n2p(0)),
                scale=1.2,
                rate_func=there_and_back_with_pause
            ),
            duration=2
        )

        t = self.aas('104.mp3', '(0,0) 坐标在屏幕的中心，而不是在左上角')
        self.forward_to(t.end + 0.6)

        self.prepare(
            ShowCreationThenDestruction(Rect([-2.96, 2.08, 0], [2.98, -2.37, 0], color=YELLOW)),
            at=1,
            duration=2
        )

        t = self.aas('105.mp3', '最终你希望所有（变换过的）坐标都在这个坐标空间中')
        self.forward_to(t.end + 0.2)
        t = self.aas('106.mp3', '否则它们就不可见了')
        self.forward_to(t.end + 0.6)

        self.prepare(
            ShowPassingFlashAround(code1),
            at=0.5,
            duration=2
        )

        t = self.aas('107.mp3', '现在我们再来看之前定义的这组顶点数据')
        self.forward_to(t.end + 0.4)

        self.prepare(
            Create(rects, lag_ratio=0.7),
            at=0.5
        )

        t = self.aas('108.mp3', '它定义的这三个顶点')
        self.forward_to(t.end)

        self.prepare(
            *[
                AnimGroup(
                    Transform(r, d, path_arc=-60 * DEGREES),
                    FadeIn(r, duration=0.2)
                )
                for r, d in zip(rects, dots)
            ],
            lag_ratio=0.3
        )

        t = self.aas('109.mp3', '分别对应屏幕上的这三个位置')
        self.forward_to(t.end + 1)

        self.play(
            FadeOut(Group(rects, tip), duration=0.3),
            FadeOut(Group(tri, verts, dots, axisg, window, xy)),
            code1.anim.points.to_center().shift(LEFT * 3).scale(1.5),
            duration=1.5
        )

        #########################################################

        gpu = SVGItem('gpu.svg', depth=-200, height=3)
        gpu.points.shift(RIGHT * 4)

        arrow = Arrow(code1, gpu)
        arrow_txt1 = arrow.create_text('顶点缓冲对象')
        arrow_txt2 = arrow.create_text('VBO', under=True)

        highlight = boolean_ops.Difference(
            Rect([-5.28, 2.11, 0], [5.52, -1.59, 0]),
            SurroundingRect(gpu),
            depth=-210,
            **HighlightRect.difference_config_d
        )

        cover2 = boolean_ops.Difference(
            Rect([-6.78, -1.48, 0], [1.61, -4.85, 0]),
            Rect([-6.61, -1.61, 0], [-2.7, -3.93, 0]),
            stroke_alpha=0,
            fill_alpha=1,
            color=BLACK
        )

        #########################################################

        self.prepare(
            FadeIn(gpu, scale=1.2),
            GrowArrow(arrow),
            lag_ratio=0.4,
            at=0.5
        )

        t = self.aas('110.mp3', '为了将这组顶点数据发送给 GPU')
        self.forward_to(t.end + 0.2)

        self.prepare(
            Write(arrow_txt1),
            Write(arrow_txt2),
            at=0.5
        )

        t = self.aas('111.mp3', f'我们通过顶点缓冲对象{s1}(Vertex Buffer Object, VBO){s2}',
                     clip=(0.3, 2.1), format=Text.Format.RichText)
        self.forward_to(t.end)
        t = self.aas('112.mp3', '管理这个内存')
        self.forward_to(t.end + 0.4)
        t = self.aas('113.mp3', '它会在 GPU 内存（通常被称为显存）中储存大量顶点')
        self.forward_to(t.end + 0.7)
        t = self.aas('114.mp3', '使用这些缓冲对象的好处是')
        self.forward_to(t.end)

        self.prepare(
            ShowCreationThenFadeAround(code1),
            at=1.5,
            duration=3
        )

        t = self.aas('115.mp3', '我们可以一次性的发送一大批数据到显卡上')
        self.forward_to(t.end + 0.4)
        t = self.aas('116.mp3', '而不是每个顶点发送一次')
        self.forward_to(t.end + 0.7)
        t = self.aas('117.mp3', '从 CPU 把数据发送到显卡相对较慢')
        self.forward_to(t.end + 0.3)
        t = self.aas('118.mp3', '所以只要可能我们都要尝试')
        self.forward_to(t.end)
        t = self.aas('119.mp3', '尽量一次性发送尽可能多的数据',
                     mul=[0.7, 1])
        self.forward_to(t.end + 1)

        self.prepare(
            FadeIn(highlight),
            duration=2
        )

        t = self.aas('120.mp3', '当数据发送至显卡的内存中后')
        self.forward_to(t.end + 0.4)

        self.prepare(
            Transform(cover, cover2)
        )

        t = self.aas('121.mp3', '顶点着色器几乎能立即访问顶点')
        self.forward_to(t.end + 0.5)
        t = self.aas('122.mp3', '这是个非常快的过程')
        self.forward_to(t.end + 0.2)
        t = self.aas('123.mp3', '并且在下一次渲染时也可以直接使用')
        self.forward_to(t.end)
        t = self.aas('124.mp3', '而不用再次传递')
        self.forward_to(t.end + 1)
        t = self.aas('125.mp3', '顶点缓冲对象是我们在 OpenGL 教程中')
        self.forward_to(t.end)
        t = self.aas('126.mp3', '第一个出现的 OpenGL 对象')
        self.forward_to(t.end + 0.5)

        self.prepare(
            FadeOut(Group(highlight, arrow, arrow_txt1, arrow_txt2, gpu)),
            Transform(cover2, cover),
            duration=2
        )

        t = self.aas('127.mp3', '由于 moderngl 做了易用的封装')
        self.forward_to(t.end + 0.3)

        #########################################################

        code2 = Text(
            '<fc #9cdcfe>vbo</fc> <fc #d4d4d4>=</fc> <fc #9cdcfe>ctx</fc><fc #cccccc>.</fc><fc #dcdcaa>buffer</fc><fc #cccccc>(</fc><fc #9cdcfe>vertices</fc><fc #cccccc>.</fc><fc #dcdcaa>tobytes</fc><fc #cccccc>())</fc>',
            format=Text.Format.RichText,
            font_size=23
        )
        code2.points.next_to(code1, DOWN, aligned_edge=LEFT)

        code3 = Text(
            '<fc #9cdcfe>vbo</fc> <fc #d4d4d4>=</fc> <fc #9cdcfe>ctx</fc><fc #cccccc>.</fc><fc #dcdcaa>buffer</fc><fc #cccccc>(</fc><fc #9cdcfe>vertices</fc><fc #cccccc>.</fc><fc #dcdcaa>tobytes</fc><fc #cccccc>(), </fc><fc #9cdcfe>dynamic</fc><fc #d4d4d4>=</fc><fc #569cd6>True</fc><fc #cccccc>)</fc>',
            format=Text.Format.RichText,
            font_size=23
        )
        code3.points.next_to(code1, DOWN, aligned_edge=LEFT)

        underline = Underline(code2[0][17:35], color=YELLOW)

        path1 = VItem(
            [-2.12, 1.71, 0], [-2.38, 1.27, 0], [-2.21, 0.82, 0], [-2, 0.23, 0], [-1.45, -0.06, 0],
            [-0.77, -0.24, 0], [-0.23, 0.27, 0], [0.1, 1.16, 0], [-0.08, 2.08, 0], [-0.38, 2.57, 0],
            [-0.95, 2.53, 0], [-1.53, 2.49, 0], [-1.92, 2.23, 0], [-2.19, 2.06, 0], [-2.05, 1.82, 0],
            color=YELLOW,
            stroke_radius=0.03
        )
        path2 = VItem(
            [0.27, -0.29, 0], [0.04, -1, 0], [0.08, -1.55, 0], [0.08, -2.18, 0], [0.44, -2.45, 0],
            [1.03, -2.65, 0], [1.66, -2.31, 0], [2.11, -1.76, 0], [2.14, -1.03, 0], [2.06, -0.43, 0],
            [1.64, -0.12, 0], [1.22, 0.08, 0], [0.79, 0.01, 0], [0.44, -0, 0], [0.27, -0.18, 0],
            color=YELLOW,
            stroke_radius=0.03
        )

        #########################################################

        self.prepare(
            Write(code2),
            at=0.7
        )

        t = self.aas('128.mp3', '所以我们这样就可以创建一个在 GPU 上的顶点数据')
        self.forward_to(t.end + 1)
        t = self.aas('129.mp3', '由于我们要发送给 GPU 的是原始字节数据')
        self.forward_to(t.end + 0.5)

        self.prepare(
            Create(underline),
            at=1
        )

        t = self.aas('130.mp3', '所以我们先使用 .tobytes() 将 numpy 数组转为字节数据')
        self.forward_to(t.end + 0.4)
        t = self.aas('131.mp3', '然后再传递给 ctx.buffer 就得到 vbo 了')
        self.forward_to(t.end)

        self.play(Destruction(underline))

        t = self.aas('132.mp3', '这里稍微提一下')
        self.forward_to(t.end + 0.3)

        self.prepare(
            Transform(code2[0][35:], code3[0][35:]),
            at=1.7
        )

        t = self.aas('133.mp3', 'ctx.buffer 有个参数是 dynamic')
        self.forward_to(t.end + 0.5)
        t = self.aas('134.mp3', '如果你需要经常修改这个 vbo 的顶点数据')
        self.forward_to(t.end + 0.3)
        t = self.aas('135.mp3', '将其置为 True 会比较有用')
        self.forward_to(t.end + 0.3)
        t = self.aas('136.mp3', '这样就能提示显卡把数据放在能够高速写入的内存部分')
        self.forward_to(t.end + 0.5)

        self.prepare(
            Transform(code3[0][35:], code2[0][35:]),
            at=1
        )

        t = self.aas('137.mp3', '对于大部分的情况，我们忽略这个就行了')
        self.forward_to(t.end + 0.7)

        self.play(
            FadeOut(Group(code1, code2), duration=0.6),
            g.anim.become(g_stat)
        )
        self.prepare(
            FadeOut(cover)
        )
        self.prepare(
            Create(path1),
            Create(path2),
            lag_ratio=0.7,
            at=1
        )

        t = self.aas('138.mp3', '接下来我们创建顶点着色器和片段着色器')
        self.forward_to(t.end)
        t = self.aas('139.mp3', '来真正处理这些数据')
        self.forward_to(t.end + 0.5)
        t = self.aas('140.mp3', '因为我们打算做渲染的话')
        self.forward_to(t.end + 0.2)

        t = self.aas('141.mp3', '现代 OpenGL 需要我们至少设置一个顶点和一个片段着色器')
        self.forward_to(t.end + 0.5)
        t = self.aas('142.mp3', '对着色器更详细的讨论会放在之后的几节')
        self.forward_to(t.end + 0.3)
        t = self.aas('143.mp3', '我们现在先简要介绍一下着色器')
        self.forward_to(t.end + 0.3)
        t = self.aas('144.mp3', '以及配置两个非常简单的着色器')
        self.forward_to(t.end)
        t = self.aas('145.mp3', '来绘制我们第一个三角形')
        self.forward_to(t.end)
        self.play(
            FadeOut(Group(path1, path2))
        )
        self.forward()


code4_src = '''
<fc #569cd6>#version</fc> <fc #b5cea8>330</fc><fc #cccccc> core</fc>

<fc #569cd6>in</fc> <fc #569cd6>vec3</fc><fc #cccccc> in_vert;</fc>

<fc #569cd6>void</fc><fc #cccccc> main()</fc>
<fc #cccccc>{</fc>
    <fc #9cdcfe>gl_Position</fc> <fc #d4d4d4>=</fc> <fc #569cd6>vec4</fc><fc #cccccc>(in_vert.x, in_vert.y, in_vert.z, </fc><fc #b5cea8>1.0</fc><fc #cccccc>);</fc>
<fc #cccccc>}</fc>
'''

typ1_src = '''
#align(center)[
    #set text(font: "Consolas")
    GLSL 330 $<=>$ OpenGL 3.3

    GLSL 420 $<=>$ OpenGL 4.2

    ......
]
'''

typ2_src = '''
#show raw: set text(font: ("Consolas", "LXGW WenKai Lite"))

```glsl
float
vec2 // 由 2 个 float 组成
vec3 // 由 3 个 float 组成
vec4 // 由 4 个 float 组成
```
'''


class VertexShader(Template):
    def construct(self) -> None:
        #########################################################

        pipeline = ImageItem('pipeline.png', height=4.8).show()
        cover = boolean_ops.Difference(
            Rect([-4.26, 2.61, 0], [4.17, -2.72, 0]),
            Rect([-1.91, 0.11, 0], [-0.2, 2.31, 0]),
            stroke_alpha=0,
            fill_alpha=1,
            color=BLACK
        )
        g = Group(pipeline, cover, depth=10000).fix_in_frame()
        g_stat = g.copy()

        glsl = Text(
            'GLSL\n<fs 0.7><c GREY>OpenGL Shading Language</c></fs>',
            font_size=30,
            format=Text.Format.RichText
        )
        glsl.points.arrange(DOWN)

        code4 = Text(code4_src, font_size=18, format=Text.Format.RichText)

        sur_config = dict(
            stroke_radius=0.01,
            fill_alpha=0.2,
            color=YELLOW,
            depth=10
        )
        psur = partial(SurroundingRect, **sur_config)

        rect = psur(code4[1])

        typ1 = TypstDoc(typ1_src)
        typ1.points.shift(DOWN * 1.8 + RIGHT)

        typ2 = TypstDoc(typ2_src)
        typ2.points.shift(DOWN * 2.3 + RIGHT * 5.5)

        vec4_var = Text('vec4', color='#569cd6')
        vec4_coords = Text('.x\n.y\n.z\n.w')
        vec4 = Group(vec4_var, Brace(vec4_coords, LEFT, color='#569cd6'), vec4_coords)
        vec4.points.arrange().shift(UP * 0.7)

        #########################################################

        self.forward()

        self.prepare(
            FadeIn(cover),
            at=0.5,
            duration=2
        )

        t = self.aas('146.mp3', '顶点着色器(Vertex Shader)是几个可编程着色器中的一个')
        self.forward_to(t.end + 0.6)

        self.prepare(
            g.anim.points.shift(LEFT * 4.5 + DOWN * 3.8),
            at=0.5
        )

        t = self.aas('147.mp3', '我们需要做的第一件事')
        self.forward_to(t.end)

        self.prepare(
            Write(glsl),
            at=0.6
        )

        t = self.aas('148.mp3', '是用着色器语言 GLSL 编写顶点着色器')
        self.forward_to(t.end + 0.4)
        t = self.aas('149.mp3', '然后编译这个着色器')
        self.forward_to(t.end)
        t = self.aas('150.mp3', '这样我们就可以在程序中使用它了')
        self.forward_to(t.end + 0.6)

        self.prepare(
            FadeOut(glsl),
            Write(code4),
            duration=3
        )

        t = self.aas('151.mp3', '这是一个非常基础的 GLSL 顶点着色器的源代码')
        self.forward_to(t.end + 1)
        t = self.aas('152.mp3', '可以看到，GLSL 看起来很像 C语言')
        self.forward_to(t.end + 0.6)

        self.prepare(
            Write(rect),
            at=1
        )

        t = self.aas('153.mp3', '每个着色器都起始于一个版本声明')
        self.forward_to(t.end + 0.6)
        t = self.aas('154.mp3', 'OpenGL 3.3 以及更高版本中')
        self.forward_to(t.end + 0.2)

        self.prepare(
            rect.anim.become(psur(code4[1][9:12])),
            FadeIn(typ1),
            at=0.5,
            duration=2
        )

        t = self.aas('155.mp3', 'GLSL 版本号和 OpenGL 的版本是匹配的')
        self.forward_to(t.end + 0.3)

        self.prepare(
            rect.anim.become(psur(code4[1][-4:])),
            FadeOut(typ1, duration=0.6),
            at=1.5
        )

        t = self.aas('156.mp3', '我们同样明确表示我们会使用核心模式')
        self.forward_to(t.end + 0.6)

        self.prepare(
            rect.anim.become(psur(code4[3])),
            at=0.5
        )

        t = self.aas('157.mp3', '下一步，使用 in 关键字',
                     clip=(0.2, 2.1))
        self.forward_to(t.end)
        t = self.aas('158.mp3', '在顶点着色器中声明所有的输入顶点属性')
        self.forward_to(t.end + 0.6)

        self.prepare(
            FadeIn(typ2),
            at=0.5
        )

        t = self.aas('159.mp3', 'GLSL 有一些向量数据类型')
        self.forward_to(t.end + 0.2)
        t = self.aas('160.mp3', '它包含 1 到 4 个 float 分量')
        self.forward_to(t.end + 0.5)
        t = self.aas('161.mp3', '包含的数量可以从它的后缀数字看出来')
        self.forward_to(t.end + 0.3)
        t = self.aas('162.mp3', '比如 vec2 就是含有两个 float 分量')
        self.forward_to(t.end + 0.2)
        t = self.aas('163.mp3', 'vec3 就是含有三个 float 分量')
        self.forward_to(t.end + 0.6)

        self.prepare(FadeOut(typ2))

        t = self.aas('164.mp3', '现在我们只关心位置数据')
        self.forward_to(t.end + 0.2)

        self.prepare(
            rect.anim.become(psur(code4[3][8:15])),
            at=1.5
        )

        t = self.aas('165.mp3', '所以我们只需要一个顶点属性 in_vert')
        self.forward_to(t.end + 0.5)
        t = self.aas('166.mp3', '由于每个顶点都有一个 3D 坐标')
        self.forward_to(t.end + 0.2)

        self.prepare(
            rect.anim.become(psur(code4[3][3:7])),
            at=1
        )

        t = self.aas('167.mp3', '所以我们给他的类型是 vec3')
        self.forward_to(t.end + 0.5)

        self.prepare(
            rect.anim.become(psur(code4[3][3:15])),
            at=0.5,
            duration=1.5
        )

        t = self.aas('168.mp3', '这样，in_vert 就是一个向量')
        self.forward_to(t.end + 0.2)
        t = self.aas('169.mp3', '并且它表示 3D 空间中的一个位置')
        self.forward_to(t.end + 0.3)

        arrow = Arrow(rect, code4[7][30:32])
        self.schedule(self.current_time + 0.8, arrow.show)
        self.prepare(
            Transform(
                arrow,
                arrow := Arrow(rect, code4[7][41:43])
            ),
            at=1.1,
            duration=0.5
        )
        self.prepare(
            Transform(
                arrow,
                arrow := Arrow(rect, code4[7][52:54])
            ),
            at=1.9,
            duration=0.5
        )

        t = self.aas('170.mp3', '我们可以通过 .x、.y 和 .z 分别得到它坐标的三个值')
        self.forward_to(t.end + 0.6)

        arrow.hide()
        self.prepare(
            Write(vec4),
            at=0.8
        )

        t = self.aas('171.mp3', '如果是一个 4D 的，即 vec4 向量')
        self.forward_to(t.end + 0.2)

        self.prepare(
            vec4_coords[-1].anim
                .points.scale(1.5)
                .r.color.set(YELLOW),
            at=0.7
        )

        t = self.aas('172.mp3', '还会有一个 .w 分量')
        self.forward_to(t.end + 0.5)
        t = self.aas('173.mp3', '注意这不是用来表达空间中位置的')
        self.forward_to(t.end + 0.2)
        t = self.aas('174.mp3', f'而是用在所谓的透视除法{s1}(Perspective Division){s2}上',
                     format=Text.Format.RichText)
        self.forward_to(t.end + 0.3)

        self.prepare(
            Uncreate(vec4),
            at=0.6,
            duration=1.5
        )

        t = self.aas('175.mp3', '我们会在之后更加详细地讨论它的用途')
        self.forward_to(t.end + 1)

        self.prepare(
            rect.anim.become(psur(code4[5:])),
            at=0.7
        )

        t = self.aas('176.mp3', '接下来便是 main 函数')
        self.forward_to(t.end + 0.9)
        t = self.aas('177.mp3', '在这里面，为了设置顶点着色器的输出')
        self.forward_to(t.end + 0.3)

        self.prepare(
            rect.anim.become(psur(code4[7])),
            at=1.5
        )

        t = self.aas(
            '178.mp3',
            [
                '我们必须把位置数据赋值给预定义的 gl_Position 变量',
                f'{s1}（这个变量名是 OpenGL 约定好的）{s2}'
            ],
            format=Text.Format.RichText
        )
        self.forward_to(t.end + 0.7)

        ########################################################

        vec4 = Text('vec4', color='#569cd6')
        vec4.points.next_to(code4[7][4:15], DOWN, buff=LARGE_BUFF).shift(RIGHT * 0.3)
        arrow = Arrow(vec4, code4[7][4:15], color='#569cd6')

        vec3sur = psur(code4[3][3:7])

        vec3_args_udl = Underline(code4[7][23:54], color=YELLOW)
        vec3_1d0_udl = Underline(code4[7][56:59], color=YELLOW)
        vec3_1d0_udl.points.shift(DOWN * 0.06)

        arrow_inout = Arrow()

        ########################################################

        self.prepare(
            Write(vec4),
            GrowArrow(arrow, rate_func=rush_from),
            lag_ratio=0.5,
            at=0.5
        )

        t = self.aas('179.mp3', '它在幕后是 vec4 类型的')
        self.forward_to(t.end + 0.6)
        t = self.aas('180.mp3', '在 main 函数中我们将 gl_Position 设置的值')
        self.forward_to(t.end)
        t = self.aas('181.mp3', '会成为该顶点着色器的输出')
        self.forward_to(t.end + 0.7)

        self.prepare(
            FadeOut(Group(vec4, arrow)),
            rect.anim.color.fade(0.7),
            Write(vec3sur, at=0.7)
        )

        t = self.aas('182.mp3', f'由于我们的输入是一个 3 分量的向量',
                     format=Text.Format.RichText)
        self.forward_to(t.end + 0.4)
        t = self.aas('183.mp3', '我们必须把它转换为 4 分量的')
        self.forward_to(t.end + 0.6)

        self.prepare(
            Create(vec3_args_udl),
            at=1,
            duration=2
        )

        t = self.aas('184.mp3', '我们可以把 vec3 的数据作为 vec4 构造器的参数')
        self.forward_to(t.end + 0.4)

        self.prepare(
            Create(vec3_1d0_udl),
            at=0.8,
            duration=1.5
        )

        t = self.aas('185.mp3', f'同时把 w 分量设置为 1.0{s1}（我们会在后面解释为什么）{s2}来完成这一任务',
                     format=Text.Format.RichText)
        self.forward_to(t.end + 1)

        self.prepare(
            FadeOut(Group(rect, vec3sur, vec3_args_udl, vec3_1d0_udl)),
            duration=2
        )

        t = self.aas('186.mp3', '当前这个顶点着色器')
        self.forward_to(t.end)
        t = self.aas('187.mp3', '可能是我们能想到的最简单的顶点着色器了')
        self.forward_to(t.end + 0.5)
        t = self.aas('188.mp3', '因为我们对输入数据什么都没有处理')
        self.forward_to(t.end)
        t = self.aas('189.mp3', '就把它传到着色器的输出了')
        self.forward_to(t.end + 0.8)
        t = self.aas('190.mp3', '在真实的程序里')
        self.forward_to(t.end)
        t = self.aas('191.mp3', '输入数据通常都不是标准化设备坐标')
        self.forward_to(t.end + 0.4)
        t = self.aas('192.mp3', '在那些情况下我们首先要进行必要的转换')
        self.forward_to(t.end)

        self.play(
            FadeOut(code4),
            g.anim.become(g_stat),
            at=0.3,
            duration=1.5
        )
        self.play(
            FadeOut(cover)
        )
        self.forward()


code5_src = '''
<fc #569cd6>#version</fc> <fc #b5cea8>330</fc><fc #cccccc> core</fc>

<fc #569cd6>out</fc> <fc #569cd6>vec4</fc><fc #cccccc> FragColor;</fc>

<fc #569cd6>void</fc><fc #cccccc> main()</fc>
<fc #cccccc>{</fc>
<fc #cccccc>    FragColor </fc><fc #d4d4d4>=</fc> <fc #569cd6>vec4</fc><fc #cccccc>(</fc><fc #b5cea8>1.0</fc><fc #cccccc>, </fc><fc #b5cea8>0.5</fc><fc #cccccc>, </fc><fc #b5cea8>0.2</fc><fc #cccccc>, </fc><fc #b5cea8>1.0</fc><fc #cccccc>);</fc>
<fc #cccccc>}</fc>
'''


class FragmentShader(Template):
    def construct(self) -> None:
        #########################################################

        pipeline = ImageItem('pipeline.png', height=4.8).show()
        cover = boolean_ops.Difference(
            Rect([-4.26, 2.61, 0], [4.17, -2.72, 0]),
            boolean_ops.Difference(
                Rect([0.17, -0.2, 0], [1.98, -2.43, 0]),
                Rect([2.09, -0.09, 0], [1.85, -1.81, 0])
            ),
            stroke_alpha=0,
            fill_alpha=1,
            color=BLACK
        )
        g = Group(pipeline, cover, depth=10000).fix_in_frame()
        g_stat = g.copy()

        code5 = Text(code5_src, font_size=18, format=Text.Format.RichText)

        sur_config = dict(
            stroke_radius=0.01,
            fill_alpha=0.2,
            color=YELLOW,
            depth=10
        )
        psur = partial(SurroundingRect, **sur_config)

        rect = psur(code5[3][:3])

        rgba = Text(
            '(<c RED>r</c>, <c GREEN>g</c>, <c BLUE>b</c>, a)',
            format=Text.Format.RichText
        )
        rgba.points.next_to(code5[3], buff=MED_LARGE_BUFF)

        udl1 = Underline(rgba[0][1:8], color=YELLOW)
        udl2 = Underline(rgba[0][10], color=YELLOW)
        udl2.points.shift(DOWN * 0.08)

        blue_rect = Rect(
            3, 3,
            stroke_alpha=0,
            fill_alpha=0.8,
            color=BLUE
        )
        blue_rect_dot = blue_rect.copy()
        blue_rect_dot.points.scale(0, about_edge=UL)

        tracker = ValueTracker(0.8)

        def txt_updater(p: UpdaterParams):
            txt = Text(f'alpha = {tracker.current().data.get():.2f}')
            txt.points.next_to(blue_rect, DOWN)
            return txt

        orange_rect = Rect(
            0.5, 0.5,
            stroke_alpha=0,
            fill_alpha=1,
            color=[1.0, 0.5, 0.2]
        )
        orange_rect.points.next_to(code5[7])

        ########################################################

        self.forward()

        self.prepare(
            FadeIn(cover),
            duration=3
        )
        self.prepare(
            g.anim.points.shift(LEFT * 6.5 + DOWN * 1.2),
            at=3,
            duration=2
        )

        t = self.aas('193.mp3', f'片段着色器{s1}(Fragment Shader){s2}是第二个也是最后一个',
                     clip=(0.6, 3.7), format=Text.Format.RichText)
        self.forward_to(t.end)
        t = self.aas('194.mp3', '我们打算创建的用于渲染三角形的着色器')
        self.forward_to(t.end + 0.4)

        self.prepare(
            Write(code5),
            at=0.5
        )

        t = self.aas('195.mp3', '片段着色器所做的是计算像素最后的颜色输出')
        self.forward_to(t.end + 0.6)

        self.prepare(
            Write(rect),
            at=1.5
        )

        t = self.aas('196.mp3', f'片段着色器只需要一个输出变量{s1}（out 表示输出）{s2}',
                     format=Text.Format.RichText)
        self.forward_to(t.end + 0.4)

        self.prepare(
            rect.anim.become(psur(code5[3][4:18])),
            at=0.8
        )

        t = self.aas('197.mp3', '这个变量是一个 4 分量向量')
        self.forward_to(t.end + 0.2)

        self.prepare(
            Write(rgba),
            at=1.5
        )

        t = self.aas('198.mp3', '它表示的是最终的输出颜色')
        self.forward_to(t.end + 0.5)

        self.prepare(
            Create(udl1),
            at=1.5
        )

        t = self.aas('199.mp3', '这个 4 分量向量的前 3 个分量')
        self.forward_to(t.end)
        t = self.aas('200.mp3', '正是我们上一节提到的 RGB 颜色值')
        self.forward_to(t.end + 0.5)

        self.prepare(
            Create(udl2),
            at=1
        )

        t = self.aas('201.mp3', f'这里的最后一个分量则表示“不透明度{s1}(Alpha){s2}”',
                     format=Text.Format.RichText)
        self.forward_to(t.end + 0.4)
        t = self.aas('202.mp3', '当其不为 1.0 时')
        self.forward_to(t.end + 0.2)
        t = self.aas('203.mp3', '则会具有一定的透明度')
        self.forward_to(t.end + 0.6)

        self.prepare(
            Transform(blue_rect_dot, blue_rect),
            at=0.5,
            duration=2
        )
        self.schedule(self.current_time + 2, lambda: blue_rect_dot.fill.set(alpha=1))

        t = self.aas('204.mp3', '比如我现在在屏幕上画出的这个蓝色矩形')
        self.forward_to(t.end)
        t = self.aas('205.mp3', '它的不透明度是 0.8')
        self.forward_to(t.end + 0.4)

        t = self.aas('206.mp3', '如果我把它调成 0.3 就会更浅')
        self.aas('207.mp3', '调成 1.0 就完全不透明', delay=t.duration + 0.4)

        self.prepare(
            ItemUpdater(None, txt_updater),
            duration=5
        )
        self.forward()
        self.prepare(
            DataUpdater(
                blue_rect,
                lambda data, p: data.fill.set(alpha=tracker.current().data.get())
            ),
            duration=3
        )
        self.play(
            tracker.anim.data.set(0.3)
        )
        self.forward()
        self.play(
            tracker.anim.data.set(1)
        )
        blue_rect.anim.fill.set(alpha=1)
        self.forward()
        self.prepare(
            Transform(blue_rect, blue_rect_dot, show_target=False),
            FadeOut(Group(udl1, udl2))
        )
        self.prepare(
            ShowPassingFlashAround(rgba),
            at=1.5
        )

        t = self.aas('208.mp3', '这四个分量一起构成了 RGBA 形式表示的颜色')
        self.forward_to(t.end + 0.8)

        self.prepare(
            FadeOut(rgba),
            rect.anim.become(psur(code5[7])),
            at=0.6
        )

        t = self.aas('209.mp3', '一般而言这里的 FragColor 是要我们编写程序')
        self.forward_to(t.end + 0.2)
        t = self.aas('210.mp3', '通过顶点、颜色、光照计算出来的值')
        self.forward_to(t.end + 0.5)
        t = self.aas('211.mp3', '为了让事情更简单')
        self.forward_to(t.end + 0.3)

        self.prepare(
            FadeIn(orange_rect),
            at=2.2
        )

        t = self.aas('212.mp3', '在这里我们让片段着色器一直输出不透明的橘黄色 (<c RED>1.0</c>, <c GREEN>0.5</c>, <c BLUE>0.2</c>, 1.0)',
                     format=Text.Format.RichText)
        self.forward_to(t.end + 0.5)

        self.play(
            FadeOut(Group(code5, rect, orange_rect)),
            g.anim(duration=1.5).become(g_stat)
        )
        self.play(
            FadeOut(cover)
        )
        self.forward()


code6_src = '''
<fc #9cdcfe>vertex_shader</fc> <fc #d4d4d4>=</fc> <fc #ce9178>\'''</fc>
<fc #ce9178>#version 330 core</fc>

<fc #ce9178>in vec3 in_vert;</fc>

<fc #ce9178>void main()</fc>
<fc #ce9178>{</fc>
<fc #ce9178>    gl_Position = vec4(in_vert.x, in_vert.y, in_vert.z, 1.0);</fc>
<fc #ce9178>}</fc>
<fc #ce9178>\'''</fc>

<fc #9cdcfe>fragment_shader</fc> <fc #d4d4d4>=</fc> <fc #ce9178>\'''</fc>
<fc #ce9178>#version 330 core</fc>

<fc #ce9178>out vec4 FragColor;</fc>

<fc #ce9178>void main()</fc>
<fc #ce9178>{</fc>
<fc #ce9178>    FragColor = vec4(1.0, 0.5, 0.2, 1.0);</fc>
<fc #ce9178>}</fc>
<fc #ce9178>\'''</fc>

<fc #9cdcfe>prog</fc> <fc #d4d4d4>=</fc> <fc #9cdcfe>ctx</fc><fc #cccccc>.</fc><fc #dcdcaa>program</fc><fc #cccccc>(</fc><fc #9cdcfe>vertex_shader</fc><fc #cccccc>, </fc><fc #9cdcfe>fragment_shader</fc><fc #cccccc>)</fc>
'''

code7_src = '''
<fc #9cdcfe>vertices</fc> <fc #d4d4d4>=</fc> <fc #4ec9b0>np</fc><fc #cccccc>.</fc><fc #dcdcaa>array</fc><fc #cccccc>([</fc>
    <fc #d4d4d4>-</fc><fc #b5cea8>0.5</fc><fc #cccccc>, </fc><fc #d4d4d4>-</fc><fc #b5cea8>0.5</fc><fc #cccccc>, </fc><fc #b5cea8>0.0</fc><fc #cccccc>,</fc>
     <fc #b5cea8>0.5</fc><fc #cccccc>, </fc><fc #d4d4d4>-</fc><fc #b5cea8>0.5</fc><fc #cccccc>, </fc><fc #b5cea8>0.0</fc><fc #cccccc>,</fc>
     <fc #b5cea8>0.0</fc><fc #cccccc>,  </fc><fc #b5cea8>0.5</fc><fc #cccccc>, </fc><fc #b5cea8>0.0</fc>
<fc #cccccc>], </fc><fc #9cdcfe>dtype</fc><fc #d4d4d4>=</fc><fc #ce9178>'f4'</fc><fc #cccccc>)</fc>

<fc #9cdcfe>vbo</fc> <fc #d4d4d4>=</fc> <fc #9cdcfe>ctx</fc><fc #cccccc>.</fc><fc #dcdcaa>buffer</fc><fc #cccccc>(</fc><fc #9cdcfe>vertices</fc><fc #cccccc>.</fc><fc #dcdcaa>tobytes</fc><fc #cccccc>())</fc>
'''


class ShaderProgramAndVertexArray(Template):
    def construct(self) -> None:
        ########################################################

        cam_stat = self.camera.copy()

        code6 = Text(code6_src, font_size=16, format=Text.Format.RichText)

        progn = Text('着色器程序', font_size=16)
        progn.points.next_to(code6[23][:4], DOWN).shift(DOWN * 0.6 + RIGHT * 0.3)

        arrow = Arrow(progn, code6[23][:4])

        rects = Rect(6, 4) * 2
        rects.points.arrange().to_border(UP)

        code7 = Text(code7_src, font_size=16, format=Text.Format.RichText)
        code7.points.move_to(rects[1])

        txt1 = Text('如何处理<c GREY><fs 0.6>（着色器程序）</fs></c>', format=Text.Format.RichText)
        txt1.points.next_to(rects[0], DOWN, aligned_edge=LEFT)

        txt2 = Text('顶点数据<c GREY><fs 0.6>（VBO）</fs></c>', format=Text.Format.RichText)
        txt2.points.next_to(rects[1], DOWN, aligned_edge=LEFT)

        code8 = Text(
            '<fc #9cdcfe>vao</fc> <fc #d4d4d4>=</fc> <fc #9cdcfe>ctx</fc><fc #cccccc>.</fc><fc #dcdcaa>vertex_array</fc><fc #cccccc>(</fc><fc #9cdcfe>prog</fc><fc #cccccc>, </fc><fc #9cdcfe>vbo</fc><fc #cccccc>, </fc><fc #ce9178>\'in_vert\'</fc><fc #cccccc>)</fc>',
            format=Text.Format.RichText,
            font_size=20
        )
        code8.points.shift(DOWN * 2)

        ########################################################

        t = self.aas('213.mp3', '好，现在已经初步认识了需要实现的两个最基本的着色器')
        self.forward_to(t.end + 0.5)
        t = self.aas('214.mp3', '现在到 Python 中')
        self.forward_to(t.end)

        self.prepare(
            Write(code6[:22]),
            at=1
        )

        t = self.aas('215.mp3', '将前面提到的顶点着色器和片段着色器存储在字符串中')
        self.forward_to(t.end + 0.6)
        t = self.aas('216.mp3', '为了能够让 OpenGL 使用它')
        self.forward_to(t.end + 0.3)
        t = self.aas('217.mp3', '我们必须在运行时动态编译它的源代码')
        self.forward_to(t.end + 0.3)

        self.prepare(
            Write(code6[23]),
            self.camera.anim(duration=2)
                .points.shift(DOWN * 2),
            at=0.7
        )

        t = self.aas('218.mp3', '在这里我们传给 ctx.program 就行了')
        self.forward_to(t.end + 0.5)
        t = self.aas('219.mp3', '它会将 GLSL 代码进行编译')
        self.forward_to(t.end + 0.3)

        self.prepare(
            FadeIn(Group(progn, arrow), scale=0.8),
            at=0.5
        )

        t = self.aas('220.mp3', f'并链接为着色器程序对象{s1}(Shader Program Object){s2}',
                     format=Text.Format.RichText)
        self.forward_to(t.end + 0.3)
        t = self.aas('221.mp3', '这样的一个着色器程序定义了我们之前提到的图形渲染管线中的流程')
        self.forward_to(t.end + 1)

        self.prepare(
            FadeOut(Group(progn, arrow), duration=0.3),
            self.camera.anim.become(cam_stat),
            FadeIn(rects),
            code6.anim.points
                .replace(rects[0], dim_to_match=1)
                .align_to(rects[0], LEFT)
                .scale(0.9),
            FadeIn(code7)
        )
        self.prepare(
            Write(txt2[0][:4]),
            at=1.2
        )

        t = self.aas('222.mp3', '现在，我们已经把输入顶点数据发送给了 GPU')
        self.forward_to(t.end + 0.3)

        self.prepare(
            Write(txt1[0][:4]),
            at=1
        )

        t = self.aas('223.mp3', '并指示了 GPU 如何在顶点和片段着色器中处理它')
        self.forward_to(t.end + 0.5)
        t = self.aas('224.mp3', '我们要将这些东西')
        self.forward_to(t.end + 0.3)

        self.prepare(
            Write(txt2[0][4:]),
            Write(txt1[0][4:]),
            lag_ratio=0.8,
            at=1
        )

        t = self.aas('225.mp3', '也就是前面弄好的顶点缓冲(VBO)和着色器程序')
        self.forward_to(t.end + 0.1)
        t = self.aas('226.mp3', '打包到一起')
        self.forward_to(t.end + 0.3)

        pt = self.prepare(
            Write(code8[0][:23]),
            Transform(code6[-2][:4], code8[0][23:27], path_arc=-70 * DEGREES, hide_src=False),
            Write(code8[0][27]),
            Transform(code7[-2][:3], code8[0][29:32], path_arc=-50 * DEGREES, hide_src=False),
            Write(code8[0][32:]),
            lag_ratio=1,
            offset=-0.4,
            duration=3,
            at=1.6
        )

        t = self.aas('227.mp3', f'将这个状态存储在顶点数组对象{s1}(Vertex Array Object, VAO){s2}中',
                     format=Text.Format.RichText)
        self.forward_to(pt.end)

        ########################################################

        vao = Text('顶点数组对象', font_size=16, color=GREY)
        vao.points.next_to(code8, DL)

        arrow = Arrow(vao, code8[0][:3], color=GREY)

        conn = VItem(
            [0.7, 0.67, 0], [0.34, 0.63, 0], [0.11, 0.78, 0], [-0.07, 0.93, 0], [-0.2, 1.26, 0],
            [-0.37, 1.67, 0], [-0.57, 2.07, 0], [-0.77, 2.38, 0], [-1.04, 2.52, 0], [-1.37, 2.66, 0],
            [-1.72, 2.69, 0], [-2.01, 2.71, 0], [-2.28, 2.69, 0], [-2.59, 2.69, 0], [-2.91, 2.69, 0],
            [-3.19, 2.69, 0], [-3.44, 2.69, 0], [-3.73, 2.69, 0], [-4, 2.69, 0], [-4.26, 2.69, 0],
            [-4.48, 2.69, 0],
            color=YELLOW
        )
        conn.add_tip()

        udl1 = Underline(code8[0][29:32], color=YELLOW)
        udl2 = Underline(code8[0][23:27], color=YELLOW)
        udl3 = Underline(code8[0][34:-1], color=YELLOW)

        verts_color = (LIGHT_PINK, YELLOW_E, PURPLE)

        rects = Group(*[
            SurroundingRect(
                line if line is code7[4] else line[:-1],
                buff=0.025,
                stroke_alpha=0,
                fill_alpha=0.5,
                depth=10,
                color=c
            )
            for line, c in zip(code7[2:5], verts_color)
        ])

        ########################################################

        self.prepare(
            Write(vao),
            GrowArrow(arrow),
            at=1
        )

        t = self.aas('228.mp3', '这行代码创建的顶点数组对象')
        self.forward_to(t.end + 0.3)

        self.prepare(
            ShowCreationThenDestruction(udl1, at=1),
            ShowCreationThenDestruction(udl2, at=3.7)
        )

        t = self.aas('229.mp3', '表示了一个将 vbo 对应的顶点数据，通过着色器程序 prog 进行渲染的过程')
        self.forward_to(t.end + 0.5)

        self.prepare(
            Create(udl3, at=0.4),
            Create(conn, at=2.5, duration=2)
        )

        t = self.aas('230.mp3', '最后的 \'in_vert\' 表示将顶点数据与着色器程序的 in_vert 关联')
        self.forward_to(t.end + 0.6)
        t = self.aas('231.mp3', '因为我们写明了 in_vert 的类型是 vec3')
        self.forward_to(t.end + 0.4)
        t = self.aas('232.mp3', '所以在渲染时')
        self.forward_to(t.end + 0.2)

        self.prepare(
            Create(rects, lag_ratio=0.6),
            at=0.5
        )

        t = self.aas('233.mp3', '它会把顶点数据中的每三个值作为一组')
        self.forward_to(t.end + 0.2)
        t = self.aas('234.mp3', '传递给顶点着色器')
        self.forward_to(t.end + 0.4)
        t = self.aas('235.mp3', '这也就是我们期望的“每三个值表示一个坐标”')
        self.forward_to(t.end + 1)
        t = self.aas('236.mp3', '如果你有在 C++ 中写过 OpenGL 程序')
        self.forward_to(t.end + 0.3)
        t = self.aas('237.mp3', '你可能会发现这里没有使用 glVertexAttribPointer 和 glEnableVertexAttribArray 链接顶点属性')
        self.forward_to(t.end + 0.3)
        t = self.aas('238.mp3', '这其实是 moderngl 的封装帮我们做完了')
        self.forward_to(t.end + 0.5)
        t = self.aas('239.mp3', '但其实 moderngl 的 vertex_array 也可以手动指定顶点属性的链接方式')
        self.forward_to(t.end + 0.3)
        t = self.aas('240.mp3', '不过我们这里暂时用不到')
        self.forward_to(t.end)

        self.forward(5)


code9_src = '''
<fc #6a9955># 导入需要的库</fc>
<fc #c586c0>import</fc> <fc #4ec9b0>glfw</fc>
<fc #c586c0>import</fc> <fc #4ec9b0>moderngl</fc> <fc #c586c0>as</fc> <fc #4ec9b0>mgl</fc>
<fc #c586c0>import</fc> <fc #4ec9b0>numpy</fc> <fc #c586c0>as</fc> <fc #4ec9b0>np</fc>

<fc #6a9955># 初始化 GLFW</fc>
<fc #c586c0>if</fc> <fc #569cd6>not</fc> <fc #4ec9b0>glfw</fc><fc #cccccc>.</fc><fc #dcdcaa>init</fc><fc #cccccc>():</fc>
    <fc #c586c0>raise</fc> <fc #4ec9b0>Exception</fc><fc #cccccc>(</fc><fc #ce9178>'GLFW出错'</fc><fc #cccccc>)</fc>

<fc #6a9955># 创建窗口</fc>
<fc #9cdcfe>window</fc> <fc #d4d4d4>=</fc> <fc #4ec9b0>glfw</fc><fc #cccccc>.</fc><fc #dcdcaa>create_window</fc><fc #cccccc>(</fc><fc #b5cea8>800</fc><fc #cccccc>, </fc><fc #b5cea8>600</fc><fc #cccccc>, </fc><fc #ce9178>'LearnOpenGL'</fc><fc #cccccc>, </fc><fc #569cd6>None</fc><fc #cccccc>, </fc><fc #569cd6>None</fc><fc #cccccc>)</fc>
<fc #c586c0>if</fc> <fc #569cd6>not</fc> <fc #9cdcfe>window</fc><fc #cccccc>:</fc>
    <fc #4ec9b0>glfw</fc><fc #cccccc>.</fc><fc #dcdcaa>terminate</fc><fc #cccccc>()</fc>
    <fc #c586c0>raise</fc> <fc #4ec9b0>Exception</fc><fc #cccccc>(</fc><fc #ce9178>'window出错'</fc><fc #cccccc>)</fc>

<fc #6a9955># 获得上下文</fc>
<fc #4ec9b0>glfw</fc><fc #cccccc>.</fc><fc #dcdcaa>make_context_current</fc><fc #cccccc>(</fc><fc #9cdcfe>window</fc><fc #cccccc>)</fc>
<fc #9cdcfe>ctx</fc> <fc #d4d4d4>=</fc> <fc #4ec9b0>mgl</fc><fc #cccccc>.</fc><fc #dcdcaa>create_context</fc><fc #cccccc>()</fc>

<fc #6a9955># 视口</fc>
<fc #569cd6>def</fc> <fc #dcdcaa>framebuffer_size_callback</fc><fc #cccccc>(</fc><fc #9cdcfe>window</fc><fc #cccccc>, </fc><fc #9cdcfe>width</fc><fc #cccccc>, </fc><fc #9cdcfe>height</fc><fc #cccccc>):</fc>
    <fc #9cdcfe>ctx</fc><fc #cccccc>.</fc><fc #9cdcfe>viewport</fc> <fc #d4d4d4>=</fc><fc #cccccc> (</fc><fc #b5cea8>0</fc><fc #cccccc>, </fc><fc #b5cea8>0</fc><fc #cccccc>, </fc><fc #9cdcfe>width</fc><fc #cccccc>, </fc><fc #9cdcfe>height</fc><fc #cccccc>)</fc>

<fc #4ec9b0>glfw</fc><fc #cccccc>.</fc><fc #dcdcaa>set_framebuffer_size_callback</fc><fc #cccccc>(</fc><fc #9cdcfe>window</fc><fc #cccccc>, </fc><fc #dcdcaa>framebuffer_size_callback</fc><fc #cccccc>)</fc>

<fc #6a9955># 处理输入</fc>
<fc #569cd6>def</fc> <fc #dcdcaa>process_input</fc><fc #cccccc>(</fc><fc #9cdcfe>window</fc><fc #cccccc>):</fc>
    <fc #c586c0>if</fc> <fc #4ec9b0>glfw</fc><fc #cccccc>.</fc><fc #dcdcaa>get_key</fc><fc #cccccc>(</fc><fc #9cdcfe>window</fc><fc #cccccc>, </fc><fc #4ec9b0>glfw</fc><fc #cccccc>.</fc><fc #9cdcfe>KEY_ESCAPE</fc><fc #cccccc>) </fc><fc #d4d4d4>==</fc> <fc #4ec9b0>glfw</fc><fc #cccccc>.</fc><fc #9cdcfe>PRESS</fc><fc #cccccc>:</fc>
        <fc #4ec9b0>glfw</fc><fc #cccccc>.</fc><fc #dcdcaa>set_window_should_close</fc><fc #cccccc>(</fc><fc #9cdcfe>window</fc><fc #cccccc>, </fc><fc #569cd6>True</fc><fc #cccccc>)</fc>

<fc #6a9955># 着色器程序</fc>
<fc #9cdcfe>vertex_shader</fc> <fc #d4d4d4>=</fc> <fc #ce9178>\'''</fc>
<fc #ce9178>#version 330 core</fc>

<fc #ce9178>in vec3 in_vert;</fc>

<fc #ce9178>void main()</fc>
<fc #ce9178>{</fc>
<fc #ce9178>    gl_Position = vec4(in_vert.x, in_vert.y, in_vert.z, 1.0);</fc>
<fc #ce9178>}</fc>
<fc #ce9178>\'''</fc>

<fc #9cdcfe>fragment_shader</fc> <fc #d4d4d4>=</fc> <fc #ce9178>\'''</fc>
<fc #ce9178>#version 330 core</fc>

<fc #ce9178>out vec4 FragColor;</fc>

<fc #ce9178>void main()</fc>
<fc #ce9178>{</fc>
<fc #ce9178>    FragColor = vec4(1.0, 0.5, 0.2, 1.0);</fc>
<fc #ce9178>}</fc>
<fc #ce9178>\'''</fc>

<fc #9cdcfe>prog</fc> <fc #d4d4d4>=</fc> <fc #9cdcfe>ctx</fc><fc #cccccc>.</fc><fc #dcdcaa>program</fc><fc #cccccc>(</fc><fc #9cdcfe>vertex_shader</fc><fc #cccccc>, </fc><fc #9cdcfe>fragment_shader</fc><fc #cccccc>)</fc>

<fc #6a9955># 顶点数据</fc>
<fc #9cdcfe>vertices</fc> <fc #d4d4d4>=</fc> <fc #4ec9b0>np</fc><fc #cccccc>.</fc><fc #dcdcaa>array</fc><fc #cccccc>([</fc>
    <fc #d4d4d4>-</fc><fc #b5cea8>0.5</fc><fc #cccccc>, </fc><fc #d4d4d4>-</fc><fc #b5cea8>0.5</fc><fc #cccccc>, </fc><fc #b5cea8>0.0</fc><fc #cccccc>,</fc>
     <fc #b5cea8>0.5</fc><fc #cccccc>, </fc><fc #d4d4d4>-</fc><fc #b5cea8>0.5</fc><fc #cccccc>, </fc><fc #b5cea8>0.0</fc><fc #cccccc>,</fc>
     <fc #b5cea8>0.0</fc><fc #cccccc>,  </fc><fc #b5cea8>0.5</fc><fc #cccccc>, </fc><fc #b5cea8>0.0</fc>
<fc #cccccc>], </fc><fc #9cdcfe>dtype</fc><fc #d4d4d4>=</fc><fc #ce9178>'f4'</fc><fc #cccccc>)</fc>

<fc #9cdcfe>vbo</fc> <fc #d4d4d4>=</fc> <fc #9cdcfe>ctx</fc><fc #cccccc>.</fc><fc #dcdcaa>buffer</fc><fc #cccccc>(</fc><fc #9cdcfe>vertices</fc><fc #cccccc>.</fc><fc #dcdcaa>tobytes</fc><fc #cccccc>())</fc>

<fc #6a9955># 顶点数组对象</fc>
<fc #9cdcfe>vao</fc> <fc #d4d4d4>=</fc> <fc #9cdcfe>ctx</fc><fc #cccccc>.</fc><fc #dcdcaa>vertex_array</fc><fc #cccccc>(</fc><fc #9cdcfe>prog</fc><fc #cccccc>, </fc><fc #9cdcfe>vbo</fc><fc #cccccc>, </fc><fc #ce9178>'in_vert'</fc><fc #cccccc>)</fc>

<fc #6a9955># 渲染循环</fc>
<fc #c586c0>while</fc> <fc #569cd6>not</fc> <fc #4ec9b0>glfw</fc><fc #cccccc>.</fc><fc #dcdcaa>window_should_close</fc><fc #cccccc>(</fc><fc #9cdcfe>window</fc><fc #cccccc>):</fc>
    <fc #6a9955># 输入</fc>
    <fc #dcdcaa>process_input</fc><fc #cccccc>(</fc><fc #9cdcfe>window</fc><fc #cccccc>)</fc>

    <fc #6a9955># 渲染指令</fc>
    <fc #9cdcfe>ctx</fc><fc #cccccc>.</fc><fc #dcdcaa>clear</fc><fc #cccccc>(</fc><fc #b5cea8>0.2</fc><fc #cccccc>, </fc><fc #b5cea8>0.3</fc><fc #cccccc>, </fc><fc #b5cea8>0.3</fc><fc #cccccc>)</fc>
    <fc #9cdcfe>vao</fc><fc #cccccc>.</fc><fc #dcdcaa>render</fc><fc #cccccc>(</fc><fc #4ec9b0>mgl</fc><fc #cccccc>.</fc><fc #9cdcfe>TRIANGLES</fc><fc #cccccc>)</fc>

    <fc #6a9955># 处理事件、交换缓冲</fc>
    <fc #4ec9b0>glfw</fc><fc #cccccc>.</fc><fc #dcdcaa>poll_events</fc><fc #cccccc>()</fc>
    <fc #4ec9b0>glfw</fc><fc #cccccc>.</fc><fc #dcdcaa>swap_buffers</fc><fc #cccccc>(</fc><fc #9cdcfe>window</fc><fc #cccccc>)</fc>

<fc #6a9955># 终止 GLFW</fc>
<fc #4ec9b0>glfw</fc><fc #cccccc>.</fc><fc #dcdcaa>terminate</fc><fc #cccccc>()</fc>
'''


class RenderTriangle(Template):
    def construct(self) -> None:
        self.forward()

        ########################################################

        code9 = Text(code9_src, font_size=20, format=Text.Format.RichText).show()
        line75 = code9[75].hide()
        self.camera.points \
            .next_to(code9, UP, coor_mask=(0, 1, 0)) \
            .shift(UP * Config.get.frame_y_radius)

        udl = Underline(line75[15:28], color=YELLOW)

        ########################################################

        self.prepare(
            self.camera.anim
                .points.align_to(code9, DOWN).shift(UP * 3.5),
            duration=2.5
        )
        self.schedule(self.current_time + 2.5, code9[:60].hide)

        self.forward()
        t = self.aas('241.mp3', '我们在渲染循环中')
        self.forward_to(t.end)

        self.prepare(
            Write(line75),
            at=0.3
        )

        t = self.aas('242.mp3', '调用 vao.render(mgl.TRIANGLES) 来绘制图元')
        self.forward_to(t.end + 1)

        self.prepare(
            Create(udl),
            at=0.5,
            duration=2
        )

        t = self.aas('243.mp3', 'render 的参数是我们打算绘制的 OpenGL 图元的类型')
        self.forward_to(t.end + 0.4)
        t = self.aas('244.mp3', '由于我们希望绘制的是一个三角形')
        self.forward_to(t.end + 0.3)
        t = self.aas('245.mp3', '所以这里传递 mgl.TRIANGLES 给它')
        self.forward_to(t.end)

        self.play(Destruction(udl))
        self.forward()


class Notes(Template):
    CONFIG = Config(
        fps=120
    )
    def construct(self) -> None:
        notes = [
            'OpenGL 着色器语言 <fs 0.8>(OpenGL Shading Language, GLSL)</fs>',
            '顶点数据 <fs 0.8>(Vertex Data)</fs>',
            '标准化设备坐标 <fs 0.8>(Normalized Device Coordinates)</fs>',
            '顶点缓冲对象 <fs 0.8>(Vertex Buffer Object, VBO)</fs>',
            '顶点着色器 <fs 0.8>(Vertex Shader)</fs>',
            '片段着色器 <fs 0.8>(Fragment Shader)</fs>',
            '着色器程序对象 <fs 0.8>(Shader Program Object)</fs>',
            '顶点数组对象 <fs 0.8>(Vertex Array Object)</fs>'
        ]

        txts = Group(*[
            Text(note, font_size=12, format=Text.Format.RichText)
            for note in notes
        ])
        txts.points.arrange(DOWN, buff=SMALL_BUFF, aligned_edge=LEFT)

        bgf = partial(
            SurroundingRect,
            stroke_alpha=0.7,
            fill_alpha=0.7,
            fill_color=GREY_D,
            stroke_color=GREY_B,
            depth=100
        )
        bg = bgf(txts[0])

        g = Group(bg, txts)

        g.points.to_border(UR, buff=SMALL_BUFF)

        self.play(
            FadeIn(bg, duration=0.5),
            Write(txts[0], duration=1)
        )

        for i, txt in enumerate(txts[1:], start=1):
            self.forward(0.2)
            self.play(
                bg.anim(duration=0.3)
                    .become(bgf(txts[:i + 1])),
                Write(txt, duration=1)
            )

        self.forward(0.2)
