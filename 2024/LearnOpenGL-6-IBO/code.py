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

        t = self.aas('1.mp3', '在上一节我们使用三个顶点渲染了一个三角形')

        self.play(
            FadeIn(dc),
            Create(tri, auto_close_path=False),
            lag_ratio=1
        )
        self.prepare(
            FadeOut(dc),
            tri.anim.digest_styles(**orange_config),
            duration=1.6
        )

        self.forward_to(t.end + 1)

        t = self.aas('2.mp3', '在渲染顶点这一话题上我们还有最后一个',
                     clip=(0.6, 3.17))
        self.forward_to(t.end)
        t = self.aas('3.mp3', '需要讨论的东西——索引缓冲对象',
                     clip=(0.22, 2.5))
        self.forward_to(t.end + 0.3)
        t = self.aas('4.mp3', '也叫元素缓冲对象')
        self.forward_to(t.end + 0.6)
        t = self.aas('5.mp3', '要解释索引缓冲对象的工作方式最好还是举个例子')
        self.forward_to(t.end + 1)

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

        self.prepare(
            Transform(tri, rect),
            at=1.6
        )

        t = self.aas('6.mp3', '假设我们不再绘制一个三角形而是绘制一个矩形')
        self.forward_to(t.end + 0.5)
        t = self.aas('7.mp3', '由于 OpenGL 主要处理三角形')
        self.forward_to(t.end + 0.2)

        self.prepare(
            FadeIn(tri1, DL),
            FadeIn(tri2, UR),
            at=1
        )

        t = self.aas('8.mp3', '我们可以绘制两个三角形来组成一个矩形')
        self.forward_to(t.end + 0.3)

        self.prepare(
            Write(code1[1]),
            duration=1,
            at=0.7
        )

        t = self.aas('9.mp3', '这会生成下面的顶点的集合')
        self.forward_to(t.end)

        tri1.depth.set(-1)
        self.play(
            Write(code1[2]),
            tri1.anim.color.set(YELLOW)
        )

        def show_vert(v, line):
            dot = Dot(v, radius=0.2, color=YELLOW)
            self.timeout(0.15, line.show)
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

        t = self.aas('10.mp3', '由于使用 mgl.TRIANGLES 的选项渲染时', delay=-0.4)
        self.forward_to(t.end + 0.1)
        t = self.aas('11.mp3', '会将每三个顶点渲染为一个三角形')
        self.forward_to(t.end + 0.5)

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

        self.prepare(
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
            lag_ratio=0.5,
            at=1
        )

        t = self.aas('12.mp3', '所以这六个顶点就会绘制出两个三角形')
        self.forward_to(t.end + 0.3)

        self.prepare(
            FadeOut(Group(tris, sur1, sur2)),
            at=1
        )

        t = self.aas('13.mp3', '在这里也就构成了一个矩形')
        self.forward_to(t.end + 0.5)

        tris.become(tris_stat)
        self.play(FadeIn(tris))

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

        t = self.aas('14.mp3', '可以发现，有几个顶点叠加了')
        self.forward_to(t.end + 0.5)

        self.prepare(
            FadeIn(dr_sur[:2]),
            FadeIn(dr_sur[2], scale=0.5),
            at=0.5
        )

        t = self.aas('15.mp3', '我们指定了右下角两次')
        self.forward_to(t.end + 0.3)

        self.prepare(
            FadeOut(dr_sur),
            FadeIn(ul_sur[:2], at=0.3),
            FadeIn(ul_sur[2], scale=0.5, at=0.3),
        )

        t = self.aas('16.mp3', '左上角也是两次！')
        self.forward_to(t.end + 0.5)

        self.prepare(
            FadeOut(ul_sur),
            *[
                GrowArrow(arrow, rate_func=rush_from)
                for arrow in arrows[:4]
            ]
        )
        self.prepare(
            Transform(Group(arrows[1]), Group(arrows[1], arrows[4])),
            Transform(Group(arrows[3]), Group(arrows[3], arrows[5])),
            at=2
        )

        self.forward(0.6)

        t = self.aas('17.mp3', '本来只有 4 个顶点的矩形却用了 6 个顶点来表示')
        self.forward_to(t.end + 0.4)

        t = self.aas('18.mp3', '这样就产生了 50% 的额外开销')
        self.forward_to(t.end + 0.7)

        self.prepare(
            FadeIn(trisimg, at=0.8)
        )

        t = self.aas('19.mp3', '当我们有包括上千个三角形的模型之后')
        self.forward_to(t.end + 0.1)
        t = self.aas('20.mp3', '这个问题会更糟糕')
        self.forward_to(t.end + 0.2)
        t = self.aas('21.mp3', '这会产生一大堆浪费')
        self.forward_to(t.end)

        self.play(FadeOut(trisimg))
        self.prepare(
            Transform(Group(arrows[1], arrows[4]), Group(arrows[1])),
            Transform(Group(arrows[3], arrows[5]), Group(arrows[3])),
            at=0.9
        )

        t = self.aas('22.mp3', '更好的解决方案是只储存不同的顶点')
        self.forward_to(t.end + 0.5)
        t = self.aas('23.mp3', '并设定绘制这些顶点的顺序')

        circle.points.move_to(arrows[0])
        circle.show()
        self.forward(0.3)
        circle.points.move_to(arrows[1])
        self.forward(0.3)
        circle.points.move_to(arrows[3])
        self.forward(0.3)
        circle.points.move_to(arrows[1])
        self.forward(0.3)
        circle.points.move_to(arrows[2])
        self.forward(0.3)
        circle.points.move_to(arrows[3])
        self.forward(0.3)
        circle.hide()

        self.forward_to(t.end + 0.1)

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

        t = self.aas('24.mp3', '这样子我们只要储存 4 个顶点就能绘制矩形了')
        self.forward_to(t.end + 0.3)
        t = self.aas('25.mp3', '之后只要指定绘制的顺序就行')
        self.forward_to(t.end + 0.4)
        t = self.aas('26.mp3', '如果 OpenGL 提供这个功能就好了，对吧？')
        self.forward_to(t.end + 0.6)
        t = self.aas('27.mp3', f'值得庆幸的是，索引缓冲对象{s1}(IBO){s2}的工作方式正是如此',
                     format=Text.Format.RichText)
        self.forward_to(t.end + 0.8)

        arrows[5:].points.shift(RIGHT * 1.5)
        self.prepare(
            Group(arrows[:4], rect, tris).anim.points.shift(RIGHT * 1.5),
            Write(Group(code2[1], code2[4:]), at=0.5),
            at=0.2
        )

        t = self.aas('28.mp3', 'IBO 是一个缓冲区，就像一个顶点缓冲区对象一样')
        self.forward_to(t.end + 0.2)

        self.prepare(
            FadeIn(sur, scale=0.8),
            at=0.4
        )

        t = self.aas('29.mp3', '它存储 OpenGL 用来决定要绘制哪些顶点的索引')
        self.forward_to(t.end + 0.4)

        self.prepare(
            FadeOut(sur),
            at=1
        )

        t = self.aas('30.mp3', f'这种所谓的索引绘制{s1}(Indexed Drawing){s2}正是我们问题的解决方案',
                     format=Text.Format.RichText)
        self.forward_to(t.end + 0.7)

        self.prepare(Uncreate(Group(code1[2], code1[5:8])))

        t = self.aas('31.mp3', '我们先把重复的去掉')
        self.forward_to(t.end + 0.2)

        code1.remove(code1[2], *code1[5:8])
        self.prepare(
            code1.anim.arrange_in_lines(),
            at=0.3
        )

        t = self.aas('32.mp3', '定义不重复的 4 个顶点')
        self.forward_to(t.end + 0.4)

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

        self.prepare(
            *[
                FadeTransform(src, txt[0], path_arc=-60 * DEGREES, hide_src=False)
                for src, txt in zip(
                    [code1[i][24:] for i in [2, 3, 4, 5]],
                    txts
                )
            ],
            lag_ratio=0.5
        )

        t = self.aas('33.mp3', '并且从 0 开始按顺序索引这些顶点')
        self.forward_to(t.end + 0.3)

        self.prepare(FadeIn(brect, duration=1.4), at=0.5)

        t = self.aas('34.mp3', '接着我们就可以给出绘制出矩形所需的索引')
        self.forward_to(t.end + 0.3)

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
        self.forward(0.5)

        t = self.aas('35.mp3', '另外需要注意的是，和 VBO 类似')
        self.forward_to(t.end + 0.3)

        self.prepare(FocusOn(code2[4][9:13]), at=0.8)

        t = self.aas('36.mp3', '这里我们指定 IBO 的数据类型是 \'i4\'')
        self.forward_to(t.end + 0.5)
        t = self.aas('37.mp3', f'表示每个索引使用 4 字节的整数{s1}(int){s2}存储',
                     format=Text.Format.RichText)
        self.forward_to(t.end + 1)

        self.prepare(
            code1.anim.points.shift(DOWN * 1),
            code2.anim.points.shift(UP * 0.1),
            Group(rect, tris, arrows[:4], txts).anim
                .points.shift(UR * 0.4).scale(0.8)
        )

        t = self.aas('38.mp3', '我们把这个索引缓冲')
        self.forward_to(t.end + 0.3)

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

        self.prepare(
            Write(code3),
            Transform(code3[0][43:], code4[0][43:]),
            lag_ratio=1
        )

        t = self.aas('39.mp3', '通过 index_buffer=ibo 的方式传递给 vao')
        self.forward_to(t.end + 0.6)
        t = self.aas('40.mp3', '这样设置后')
        self.forward_to(t.end + 0.2)
        t = self.aas('41.mp3', '这个 vao 在渲染时就会参照这个索引缓冲')
        self.forward_to(t.end)
        t = self.aas('42.mp3', '渲染出两个三角形')
        self.forward_to(t.end)

        self.forward(2)


class IntroExampleSubtitle(SubtitlesTemplate):
    subtitles = [
        ('43.mp3', '现在运行代码，你看到的还是这个橘黄色的矩形'),
        ('44.mp3', '如果你遇到了什么问题'),
        ('45.mp3', '可以参考一下这里给出的源码'),
    ]


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
