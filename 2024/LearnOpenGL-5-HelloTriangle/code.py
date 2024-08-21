# flake8: noqa
import random
import sys

sys.path.append('.')

from janim.imports import *

from utils.template import *


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
        self.play(
            self.camera.anim
                .points.rotate(60 * DEGREES, axis=RIGHT).rotate(30 * DEGREES, axis=OUT, absolute=True),
            duration=2
        )
        self.forward()

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

        self.play(
            Write(cam_rect)
        )
        self.forward()

        self.play(
            FadeIn(cam_dot, duration=0.3),
            FadeIn(cam_lines, at=0.1, duration=0.3),
            self.camera.anim.points
                .rotate(-3 * DEGREES, axis=info.horizontal_vect, absolute=True)
                .rotate(20 * DEGREES, absolute=True)
                .move_to(cam_loc * 0.3)
        )
        self.play(
            Rotate(self.camera, 80 * DEGREES, axis=UP),
            Group(cam_dot, cam_lines).anim
                .digest_styles(color=GREY),
            duration=2
        )
        self.forward()

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
        ).shuffle().show()

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
            stroke_alpha=0,
            fill_alpha=0.7,
            depth=-2
        )

        #########################################################

        self.play(
            FadeIn(pixels, lag_ratio=0.01)
        )
        self.forward()
        self.play(FadeIn(square, scale=0.8))
        self.forward()
        self.play(
            Write(mapped_square, duration=6, rate_func=double_smooth),
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
            )
        )

        stat = self.camera.copy()

        self.play(
            FadeOut(pixels),
            FadeOut(cam_lines),
            self.camera.anim.become(cam),
            duration=2
        )
        self.forward()

        self.camera.become(stat)
        cam_lines.show()

        self.forward()

        #########################################################

        arrow = Arrow(RIGHT, LEFT * 3 + UP * 0.2).fix_in_frame().show()
        tip = Text(
            '（Graphics Pipeline，大多译为管线，实际上指的是一堆原始图形数据途经一个输送管道，期间经过各种变化处理最终出现在屏幕的过程）',
            font_size=12,
            color=GREY
        ).fix_in_frame().show()
        tip.points.to_border(UL)

        #########################################################

        self.play(
            GrowArrow(arrow)
        )
        self.forward()
        tip.hide()

        self.play(
            self.camera.anim.points
                .shift(self.camera.points.info.vertical_vect * -0.2)
                .rotate(-8 * DEGREES, axis=RIGHT),
            arrow.anim.points.shift(UP * 1.6),
            plane(VItem).anim.color.fade(0.5)
        )
        self.forward()

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

        self.show(coords3d, coords3d_txt)
        self.forward()
        self.show(arrow1, coords2d, coords2d_txt)
        self.forward()
        self.show(arrow2, pixels, pixels_txt)
        self.forward()
        self.play(
            *[
                GrowArrow(ar, rate_func=rush_from)
                for ar in it.chain(arrows1, arrows2)
            ],
        )
        self.forward()
        self.play(
            FadeIn(prog1),
            FadeIn(prog2)
        )
        self.forward()
        self.play(
            *[
                ShowPassingFlash(arrow_bodies, rate_func=linear, duration=0.5)
                for _ in range(6)
            ],
            lag_ratio=0.3
        )
        self.forward()
        self.play(
            Transform(prog1, shader1),
            Transform(prog2, shader2)
        )
        self.forward()
        self.play(ShowPassingFlashAround(shader1))
        self.forward()
        self.play(ShowPassingFlashAround(shader2))
        self.forward()
        self.play(FadeIn(highlight))
        self.forward()
        self.play(FadeOut(highlight))
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
        self.play(FadeIn(hl_blue))
        self.forward()
        self.play(FadeOut(hl_blue))
        self.forward()
        self.play(FadeIn(hl_one))
        self.play(hl_one.anim.points.shift(RIGHT * 1.73))
        self.play(hl_one.anim.points.shift(RIGHT * 1.7))
        self.play(hl_one.anim.points.shift(DOWN * 2.1))
        self.play(hl_one.anim.points.shift(LEFT * 1.7))
        self.play(hl_one.anim.points.shift(LEFT * 1.73))
        self.play(FadeOut(hl_one))
        self.forward()
        self.play(
            pipeline.anim.points.scale(3).shift(DOWN * 2.7 + RIGHT * 10),
            duration=2
        )
        self.forward()

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
            stroke_background=True
        ).fix_in_frame()
        # frag_tip.points.arrange(DOWN, aligned_edge=RIGHT, buff=SMALL_BUFF)
        # frag_tip.points.to_border(UR)
        frag_tip.points.to_border(UL)

        #########################################################

        self.play(
            Write(Group(*[dot[0] for dot in dots]), lag_ratio=0.3)
        )
        self.forward()
        self.play(
            self.camera.anim.points.shift(RIGHT * 3)
        )
        self.play(
            self.camera.anim.points.shift(LEFT * 3)
        )
        self.forward()
        self.play(
            Create(
                rect1,
                auto_close_path=False
            )
        )
        self.forward()
        self.play(
            Write(tip),
            GrowArrow(tiparrow)
        )
        self.forward()
        self.play(
            Transform(rect1, rect2),
            AnimGroup(
                *[
                    DrawBorderThenFill(dot[1])
                    for dot in dots
                ],
            ),
            lag_ratio=0.7
        )
        self.forward()
        self.play(
            FadeOut(Group(rect2, tip, tiparrow, *[dot[1] for dot in dots])),
            FadeOut(Group(*[dot[0] for dot in dots]), RIGHT * 6),
            self.camera.anim.points.shift(RIGHT * 7).scale(1.3)
        )
        self.forward()
        self.play(
            CircleIndicate(Dot(RIGHT * 6.03 + DOWN * 0.58), scale=1.2),
            CircleIndicate(Dot(RIGHT * 8.23 + UP * 1.26), scale=1.2),
            CircleIndicate(Dot(RIGHT * 8.36 + DOWN * 1.15), scale=1.2),
            lag_ratio=0.4
        )
        self.forward()
        self.play(
            self.camera.anim.points.shift(RIGHT * 5)
        )
        self.forward()
        self.play(
            ShowCreationThenDestruction(
                Rect(2.5, 0.4, color=YELLOW)
                    .points.shift(RIGHT * 13.12 + DOWN * 0.63).rotate(-50 * DEGREES)
                    .r
            ),
            duration=2
        )
        self.forward()
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
        self.forward()
        self.play(
            self.camera.anim.points.shift(UP * 2)
        )
        self.forward()
        self.play(
            self.camera.anim.points.shift(DOWN * 2)
        )
        frag_tip.show()
        self.forward(2)
        frag_tip.hide()
        self.play(
            self.camera.anim.points.move_to(pipeline).scale(2)
        )
        self.forward()

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

        self.play(FadeIn(highlight))
        self.forward()
        self.play(FadeOut(highlight))
        self.forward()
        self.play(
            Create(path1),
            Create(path2),
            lag_ratio=0.5
        )
        self.forward()
        self.play(
            FadeOut(path1),
            FadeOut(path2)
        )
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
        self.play(FadeIn(cover))
        self.play(g.anim.points.shift(LEFT * 2.5 + DOWN * 4))
        self.forward()
        self.play(
            *[
                AnimGroup(
                    Write(axis, root_only=True),
                    Write(axis.ticks)
                )
                for axis in axisg
            ],
            self.camera.anim.points
                .rotate(40 * DEGREES, axis=RIGHT)
                .rotate(30 * DEGREES, axis=OUT, absolute=True)
        )
        self.forward()
        self.play(
            *[
                Write(axis.numbers)
                for axis in axisg
            ]
        )
        self.forward()

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

        #########################################################

        self.play(self.camera.anim.become(cam_stat))
        self.play(Create(tri, auto_close_path=False))
        self.forward()
        self.play(FadeIn(verts))
        self.play(self.camera.anim.become(cam_stat2))
        self.forward()
        self.play(Write(code1))
        self.forward()
        self.play(
            *[
                ShowCreationThenDestruction(
                    Underline(code_line, buff=0.02, color=YELLOW).fix_in_frame()
                )
                for code_line in code1[2:5]
            ],
            lag_ratio=0.1
        )
        self.forward()
        self.play(FocusOn(code1[5][9:13].fix_in_frame()))
        self.forward()
        self.play(
            ShowCreationThenFadeOut(
                axisg.copy()(VItem)
                    .color.set(YELLOW).r
                    .depth.arrange(-10).r,
            )
        )
        self.forward()
        self.play(
            Indicate(Group(tri, verts), scale_factor=1.1)
        )
        self.forward()
        self.play(
            ShowCreationThenFadeAround(z_coords),
            AnimGroup(
                FadeIn(z, duration=0.5),
                FadeOut(z, duration=0.5, at=1.5)
            )
        )
        self.forward()
        self.play(
            self.camera.anim.become(cam_stat)
        )
        axis_z.hide()
        self.forward()

        #########################################################

        axisg = Group(axis_x, axis_y)

        for axis in axisg:
            for v in axis.numbers:
                v.set_stroke_background(True)
            axis.numbers(VItem).stroke.set(BLACK, 1)

        window = ImageItem('window-col.png', depth=1)

        #########################################################

        self.play(
            FadeIn(window),
            Group(axisg, tri, verts).anim
                .points.set_size(6.55, 4.9)
                       .shift(LEFT * 0.01 + DOWN * 0.13),
            lag_ratio=0.4
        )
        self.forward()

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

        self.play(FadeIn(xy, lag_ratio=0.5))
        self.forward()
        self.play(
            ShowCreationThenDestruction(
                axis_y.store()
                    .depth.set(-1)
                    .r.color.set(YELLOW)
                    .r.radius.set(0.04)
                    .r,
                root_only=True
            )
        )
        self.forward()
        self.play(
            CircleIndicate(
                SmallDot(axis_x.n2p(0)),
                scale=1.2,
                rate_func=there_and_back_with_pause
            )
        )
        self.forward()
        self.play(ShowCreationThenDestruction(Rect([-2.96, 2.08, 0], [2.98, -2.37, 0], color=YELLOW)))
        self.forward()
        self.play(ShowPassingFlashAround(code1))
        self.forward()
        self.play(
            Create(rects, lag_ratio=0.7)
        )
        self.forward()
        self.play(
            *[
                AnimGroup(
                    Transform(r, d, path_arc=-60 * DEGREES),
                    FadeIn(r, duration=0.2)
                )
                for r, d in zip(rects, dots)
            ],
            lag_ratio=0.3
        )
        self.forward()
        self.play(
            FadeOut(rects, duration=0.3),
            FadeOut(Group(tri, verts, dots, axisg, window, xy)),
            code1.anim.points.to_center().shift(LEFT * 3).scale(1.5)
        )
        self.forward()

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

        self.play(
            FadeIn(gpu, scale=1.2),
            GrowArrow(arrow),
            lag_ratio=0.4
        )
        self.forward()
        self.play(
            Write(arrow_txt1),
            Write(arrow_txt2)
        )
        self.forward(2)
        self.play(
            ShowCreationThenFadeAround(code1)
        )
        self.forward()
        self.play(FadeIn(highlight))
        self.forward()
        self.play(Transform(cover, cover2))
        self.forward()
        self.play(
            FadeOut(Group(highlight, arrow, arrow_txt1, arrow_txt2, gpu)),
            Transform(cover2, cover)
        )
        self.forward()

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

        self.play(
            Write(code2)
        )
        self.forward()
        self.play(
            Create(underline)
        )
        self.forward()
        underline.points.reverse()
        self.play(
            Uncreate(underline)
        )
        self.play(
            Transform(code2[0][35:], code3[0][35:])
        )
        self.forward()
        self.play(
            Transform(code3[0][35:], code2[0][35:])
        )
        self.forward()
        self.play(
            FadeOut(Group(code1, code2), duration=0.6),
            g.anim.become(g_stat)
        )
        self.play(
            FadeOut(cover)
        )
        self.play(
            Create(path1),
            Create(path2),
            lag_ratio=0.2
        )
        self.forward(2)
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
        self.play(FadeIn(cover))
        self.play(g.anim.points.shift(LEFT * 4.5 + DOWN * 3.8))
        self.forward()
        self.play(Write(glsl))
        self.forward()
        self.play(
            FadeOut(glsl),
            Write(code4)
        )
        self.forward()
        self.play(Write(rect))
        self.forward()
        self.play(
            rect.anim.become(psur(code4[1][9:12])),
            FadeIn(typ1)
        )
        self.forward()
        self.play(
            rect.anim.become(psur(code4[1][-4:])),
            FadeOut(typ1, duration=0.6)
        )
        self.forward()
        self.play(
            rect.anim.become(psur(code4[3]))
        )
        self.forward()
        self.play(FadeIn(typ2))
        self.forward()
        self.play(FadeOut(typ2))
        self.forward()
        self.play(
            rect.anim.become(psur(code4[3][8:15]))
        )
        self.forward()
        self.play(
            rect.anim.become(psur(code4[3][3:7]))
        )
        self.forward()
        self.play(
            rect.anim.become(psur(code4[3][3:15]))
        )
        self.forward()

        arrow = Arrow(rect, code4[7][30:32])
        arrow.show()

        self.forward()
        self.play(
            Transform(
                arrow,
                arrow := Arrow(rect, code4[7][41:43])
            )
        )
        self.forward()
        self.play(
            Transform(
                arrow,
                arrow := Arrow(rect, code4[7][52:54])
            )
        )
        self.forward()
        arrow.hide()
        self.forward()
        self.play(Write(vec4))
        self.forward()
        self.play(
            vec4_coords[-1].anim
                .points.scale(1.5)
                .r.color.set(YELLOW)
        )
        self.forward()
        self.play(Uncreate(vec4))
        self.forward()
        self.play(
            rect.anim.become(psur(code4[5:]))
        )
        self.forward()
        self.play(
            rect.anim.become(psur(code4[7]))
        )
        self.forward()

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

        self.play(
            Write(vec4),
            GrowArrow(arrow, rate_func=rush_from),
            lag_ratio=0.5
        )
        self.forward()
        self.play(
            FadeOut(Group(vec4, arrow)),
            rect.anim.color.fade(0.7)
        )
        self.forward()
        self.play(
            Write(vec3sur)
        )
        self.forward()
        self.play(
            Create(vec3_args_udl)
        )
        self.forward()
        self.play(
            Create(vec3_1d0_udl)
        )
        self.forward()
        self.play(
            FadeOut(Group(rect, vec3sur, vec3_args_udl, vec3_1d0_udl))
        )
        self.forward()
        self.play(
            FadeOut(code4),
            g.anim.become(g_stat)
        )
        self.play(
            FadeOut(cover)
        )
        self.forward()


class FragmentShader(Template):
    def construct(self) -> None:
        pass


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
        ]

        txts = Group(*[
            Text(note, font_size=12, format=Text.Format.RichText)
            for note in notes
        ])
        txts.points.arrange(DOWN, buff=SMALL_BUFF, aligned_edge=LEFT)

        bgf = partial(
            SurroundingRect,
            fill_alpha=1,
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
