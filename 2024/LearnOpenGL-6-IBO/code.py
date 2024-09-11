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
    str2 = '索引缓冲对象'


code1_src = '''
<fc #9cdcfe>vertices</fc><fc #d4d4d4> = </fc><fc #4ec9b0>np</fc><fc #d4d4d4>.</fc><fc #dcdcaa>array</fc><fc #d4d4d4>([</fc>
    <fc #6a9955># 第一个三角形</fc>
    <fc #b5cea8>0.5</fc><fc #d4d4d4>, </fc><fc #b5cea8>0.5</fc><fc #d4d4d4>, </fc><fc #b5cea8>0.0</fc><fc #d4d4d4>,      </fc><fc #6a9955># 右上角</fc>
    <fc #b5cea8>0.5</fc><fc #d4d4d4>, -</fc><fc #b5cea8>0.5</fc><fc #d4d4d4>, </fc><fc #b5cea8>0.0</fc><fc #d4d4d4>,     </fc><fc #6a9955># 右下角</fc>
<fc #d4d4d4>    -</fc><fc #b5cea8>0.5</fc><fc #d4d4d4>, </fc><fc #b5cea8>0.5</fc><fc #d4d4d4>, </fc><fc #b5cea8>0.0</fc><fc #d4d4d4>,     </fc><fc #6a9955># 左上角</fc>
    <fc #6a9955># 第二个三角形</fc>
    <fc #b5cea8>0.5</fc><fc #d4d4d4>, -</fc><fc #b5cea8>0.5</fc><fc #d4d4d4>, </fc><fc #b5cea8>0.0</fc><fc #d4d4d4>,     </fc><fc #6a9955># 右下角</fc>
<fc #d4d4d4>    -</fc><fc #b5cea8>0.5</fc><fc #d4d4d4>, -</fc><fc #b5cea8>0.5</fc><fc #d4d4d4>, </fc><fc #b5cea8>0.0</fc><fc #d4d4d4>,    </fc><fc #6a9955># 左下角</fc>
<fc #d4d4d4>    -</fc><fc #b5cea8>0.5</fc><fc #d4d4d4>, </fc><fc #b5cea8>0.5</fc><fc #d4d4d4>, </fc><fc #b5cea8>0.0</fc>      <fc #6a9955># 左上角</fc>
<fc #d4d4d4>], </fc><fc #9cdcfe>dtype</fc><fc #d4d4d4>=</fc><fc #ce9178>'f4'</fc><fc #d4d4d4>)</fc>
<fc #9cdcfe>vbo</fc><fc #d4d4d4> = </fc><fc #9cdcfe>ctx</fc><fc #d4d4d4>.</fc><fc #dcdcaa>buffer</fc><fc #d4d4d4>(</fc><fc #9cdcfe>vertices</fc><fc #d4d4d4>.</fc><fc #dcdcaa>tobytes</fc><fc #d4d4d4>())</fc>
'''

code2_src = '''
<fc #9cdcfe>indices</fc><fc #d4d4d4> = </fc><fc #4ec9b0>np</fc><fc #d4d4d4>.</fc><fc #dcdcaa>array</fc><fc #d4d4d4>([</fc>
    <fc #b5cea8>0</fc><fc #d4d4d4>, </fc><fc #b5cea8>1</fc><fc #d4d4d4>, </fc><fc #b5cea8>3</fc><fc #d4d4d4>,    </fc><fc #6a9955># 第一个三角形</fc>
    <fc #b5cea8>1</fc><fc #d4d4d4>, </fc><fc #b5cea8>2</fc><fc #d4d4d4>, </fc><fc #b5cea8>3</fc>     <fc #6a9955># 第二个三角形</fc>
<fc #d4d4d4>], </fc><fc #9cdcfe>dtype</fc><fc #d4d4d4>=</fc><fc #ce9178>'i4'</fc><fc #d4d4d4>)</fc>
<fc #9cdcfe>ibo</fc><fc #d4d4d4> = </fc><fc #9cdcfe>ctx</fc><fc #d4d4d4>.</fc><fc #dcdcaa>buffer</fc><fc #d4d4d4>(</fc><fc #9cdcfe>indices</fc><fc #d4d4d4>.</fc><fc #dcdcaa>tobytes</fc><fc #d4d4d4>())</fc>
'''

code3_src = '''<fc #9cdcfe>vao</fc><fc #d4d4d4> = </fc><fc #9cdcfe>ctx</fc><fc #d4d4d4>.</fc><fc #dcdcaa>vertex_array</fc><fc #d4d4d4>(</fc><fc #9cdcfe>prog</fc><fc #d4d4d4>, </fc><fc #9cdcfe>vbo</fc><fc #d4d4d4>, </fc><fc #ce9178>'in_vert'</fc><fc #d4d4d4>)</fc>'''

code4_src = '''<fc #9cdcfe>vao</fc><fc #d4d4d4> = </fc><fc #9cdcfe>ctx</fc><fc #d4d4d4>.</fc><fc #dcdcaa>vertex_array</fc><fc #d4d4d4>(</fc><fc #9cdcfe>prog</fc><fc #d4d4d4>, </fc><fc #9cdcfe>vbo</fc><fc #d4d4d4>, </fc><fc #ce9178>'in_vert'</fc><fc #d4d4d4>, </fc><fc #9cdcfe>index_buffer</fc><fc #d4d4d4>=</fc><fc #9cdcfe>ibo</fc><fc #d4d4d4>)</fc>'''


class Intro(Template):
    def construct(self) -> None:
        #########################################################

        verts = np.array([DL, DR, UP])
        verts[:, 1] *= 0.85

        tri = Polygon(*verts)
        dc = DotCloud(*verts)

        orange_config = dict(
            fill_alpha=1,
            fill_color=[1.0, 0.5, 0.2],
            stroke_alpha=0
        )

        #########################################################

        self.forward()
        self.play(FadeIn(dc))
        self.play(Create(tri, auto_close_path=False))
        self.forward()
        self.play(
            FadeOut(dc),
            tri.anim.digest_styles(**orange_config)
        )
        self.forward()

        #########################################################

        rect = Rect(3, 2, **orange_config)
        rbox = rect.points.box

        tri1_verts = [rbox.get(d) for d in (UR, DR, UL)]
        tri1 = Polygon(*tri1_verts)
        tri2_verts = [rbox.get(d) for d in (DR, DL, UL)]
        tri2 = Polygon(*tri2_verts)

        code1 = Text(
            code1_src,
            format=Text.Format.RichText,
            font_size=16,
        )
        code1.points.to_border(UL)

        #########################################################

        self.play(Transform(tri, rect))
        self.forward()
        self.play(
            FadeIn(tri1, DL),
            FadeIn(tri2, UR)
        )
        self.forward()
        self.play(Write(code1[1]), duration=1)
        tri1.depth.set(-1)
        self.play(
            Write(code1[2]),
            tri1.anim.color.set(YELLOW)
        )

        def show_vert(v, line):
            dot = Dot(v, radius=0.2, color=YELLOW)
            self.timeout(0.1, line.show)
            self.play(FadeIn(dot, scale=0.5), duration=0.5)
            self.forward(0.2)
            self.hide(dot)

        for v, line in zip(tri1_verts, code1[3:6]):
            show_vert(v, line)

        def sf():
            tri1.color.set(WHITE)
            tri2.color.set(YELLOW)
            tri2.depth.set(-2)
            self.detect_changes_of_all()

        self.timeout(0.4, sf)
        self.play(Write(code1[6]))

        for v, line in zip(tri2_verts, code1[7:10]):
            show_vert(v, line)

        self.forward(0.4)

        self.play(
            Write(code1[10:]),
            tri2.anim.color.set(WHITE)
        )

        self.forward()

        #########################################################

        psur = partial(
            SurroundingRect,
            buff=0.05,
            fill_alpha=0.5,
            stroke_alpha=0,
            depth=1
        )

        sur1 = psur(code1[3:6], color=PURPLE)
        sur2 = psur(code1[7:10], color=MAROON)

        tris = Group(tri1, tri2)
        tris_stat = tris.copy()

        #########################################################

        self.play(
            AnimGroup(
                Create(sur1),
                tri1.anim(duration=0.7).fill.set(PURPLE, 1)
                    .r.stroke.set(alpha=0)
            ),
            AnimGroup(
                Create(sur2),
                tri2.anim(duration=0.7).fill.set(MAROON, 1)
                    .r.stroke.set(alpha=0)
            ),
            lag_ratio=0.5
        )
        self.forward()
        self.play(FadeOut(Group(tris, sur1, sur2)))
        self.forward()
        tris.become(tris_stat)
        self.play(FadeIn(tris))
        self.forward()

        #########################################################

        psur = partial(
            SurroundingRect,
            buff=0.05
        )

        dr_sur = Group(
            psur(code1[4]),
            psur(code1[7]),
            Dot(rbox.get(DR), radius=0.2, depth=-5),
            color=YELLOW
        )

        ul_sur = Group(
            psur(code1[5]),
            psur(code1[9]),
            Dot(rbox.get(UL), radius=0.2, depth=-5),
            color=YELLOW
        )

        arrows = Group(
            *[
                Arrow(corner + d * 0.7, corner)
                for d in (UR, DR, DL, UL)
                for corner in [rbox.get(d)]
            ],
            Arrow(rbox.get(DR) + RIGHT + DOWN * 0.3, rbox.get(DR)),
            Arrow(rbox.get(UL) + LEFT + UP * 0.3, rbox.get(UL)),
            color=YELLOW
        )

        trisimg = ImageItem('tris.png', depth=10, height=18, alpha=0.25)

        circle = Circle(0.5, color=YELLOW)

        #########################################################

        self.play(
            FadeIn(dr_sur[:2]),
            FadeIn(dr_sur[2], scale=0.5)
        )
        self.forward()
        self.play(
            FadeOut(dr_sur),
            FadeIn(ul_sur[:2], at=0.3),
            FadeIn(ul_sur[2], scale=0.5, at=0.3)
        )
        self.forward()
        self.play(FadeOut(ul_sur))
        self.forward()
        self.play(
            *[
                GrowArrow(arrow, rate_func=rush_from)
                for arrow in arrows[:4]
            ]
        )
        self.forward()
        self.play(
            Transform(Group(arrows[1]), Group(arrows[1], arrows[4])),
            Transform(Group(arrows[3]), Group(arrows[3], arrows[5]))
        )
        self.forward()
        self.play(FadeIn(trisimg))
        self.forward()
        self.play(FadeOut(trisimg))
        self.forward()
        self.play(
            Transform(Group(arrows[1], arrows[4]), Group(arrows[1])),
            Transform(Group(arrows[3], arrows[5]), Group(arrows[3]))
        )
        self.forward()

        circle.points.move_to(arrows[0])
        circle.show()
        self.forward(0.5)
        circle.points.move_to(arrows[1])
        self.forward(0.5)
        circle.points.move_to(arrows[3])
        self.forward(0.5)
        circle.points.move_to(arrows[1])
        self.forward(0.5)
        circle.points.move_to(arrows[2])
        self.forward(0.5)
        circle.points.move_to(arrows[3])
        self.forward(0.5)
        circle.hide()
        self.forward()

        #########################################################

        code2 = Text(
            code2_src,
            format=Text.Format.RichText,
            font_size=16
        )
        code2.points.next_to(code1, DOWN, aligned_edge=LEFT, buff=MED_LARGE_BUFF)

        sur = SurroundingRect(
            code2[2:4],
            stroke_alpha=0,
            fill_alpha=0.5,
            fill_color=YELLOW,
            depth=1,
            buff=0
        )

        code1.show()

        #########################################################

        arrows[5:].points.shift(RIGHT * 1.5)
        self.play(
            Group(arrows[:4], rect, tris).anim.points.shift(RIGHT * 1.5),
            Write(Group(code2[1], code2[4:]), at=0.5)
        )
        self.forward()
        self.play(FadeIn(sur, scale=0.8))
        self.forward()
        self.play(FadeOut(sur))
        self.forward()
        self.play(Uncreate(Group(code1[2], code1[5:8])))
        code1.remove(code1[2], *code1[5:8])
        self.play(
            code1.anim.arrange_in_lines()
        )
        self.forward()

        #########################################################

        txts = Group(*[
            Text(str(i), font_size=30)
                .points.next_to(arrow, -arrow.points.start_direction)
                .r
            for i, arrow in enumerate(arrows[:4])
        ])

        brect = boolean_ops.Difference(
            FrameRect(),
            boolean_ops.Union(
                Rect([-6.26, -0.31, 0], [-2.39, -0.89, 0]),
                Rect([-1.67, 2.48, 0], [4.83, -2.76, 0])
            ),
            **HighlightRect.difference_config_d
        )

        #########################################################

        self.play(
            *[
                FadeTransform(src, txt[0], path_arc=-60 * DEGREES, hide_src=False)
                for src, txt in zip(
                    [code1[i][24:] for i in [2, 3, 4, 5]],
                    txts
                )
            ],
            lag_ratio=0.5
        )
        self.forward()
        self.play(FadeIn(brect))
        self.forward()

        circle.points.move_to(arrows[0])
        circle.show()
        code2[2][4:6].show()
        self.forward(0.5)
        circle.points.move_to(arrows[1])
        code2[2][7:9].show()
        self.forward(0.5)
        circle.points.move_to(arrows[3])
        code2[2][10:12].show()
        self.forward(0.5)
        self.play(Write(code2[2][16:]))
        self.forward(0.5)
        circle.points.move_to(arrows[1])
        code2[3][4:6].show()
        circle.show()
        self.forward(0.5)
        circle.points.move_to(arrows[2])
        code2[3][7:9].show()
        self.forward(0.5)
        circle.points.move_to(arrows[3])
        code2[3][10:12].show()
        self.forward(0.5)
        self.play(Write(code2[3][16:]))
        self.forward(0.5)
        circle.hide()
        self.play(FadeOut(brect))
        self.forward()
        self.play(FocusOn(code2[4][9:13]))
        self.forward()

        self.play(
            code1.anim.points.shift(DOWN * 1),
            code2.anim.points.shift(UP * 0.1),
            Group(rect, tris, arrows[:4], txts).anim
                .points.shift(UR * 0.4).scale(0.8)
        )
        self.forward()

        #########################################################

        code3 = Text(
            code3_src,
            format=Text.Format.RichText,
            font_size=16
        )
        code4 = Text(
            code4_src,
            format=Text.Format.RichText,
            font_size=16
        )

        for code in (code3, code4):
            code.points.next_to(code2, DOWN, aligned_edge=LEFT, buff=MED_LARGE_BUFF)

        #########################################################

        self.play(Write(code3))
        self.forward()
        self.play(Transform(code3[0][43:], code4[0][43:]))
        self.forward()


class Notes(Template):
    CONFIG = Config(
        fps=120
    )
    def construct(self) -> None:
        notes = [
            '顶点缓冲对象 <fs 0.8>(Vertex Buffer Object, VBO)</fs>',
            '索引缓冲对象 <fs 0.8>(Index Buffer Object, IBO)</fs>',
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
            self.forward(0.5)
            self.play(
                bg.anim(duration=0.3)
                    .become(bgf(txts[:i + 1])),
                Write(txt, duration=1)
            )

        self.forward(0.5)
