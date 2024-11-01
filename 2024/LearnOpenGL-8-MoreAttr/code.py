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
    str2 = '更多属性（彩色三角形）'


code1_src = '''
<fc #9cdcfe>vertices</fc><fc #d4d4d4> = </fc><fc #4ec9b0>np</fc><fc #d4d4d4>.</fc><fc #dcdcaa>array</fc><fc #d4d4d4>([</fc>
     <fc #6a9955># 位置            # 颜色</fc>
     <fc #b5cea8>0.5</fc><fc #d4d4d4>, -</fc><fc #b5cea8>0.5</fc><fc #d4d4d4>, </fc><fc #b5cea8>0.0</fc><fc #d4d4d4>,  </fc><fc #b5cea8>1.0</fc><fc #d4d4d4>, </fc><fc #b5cea8>0.0</fc><fc #d4d4d4>, </fc><fc #b5cea8>0.0</fc><fc #d4d4d4>,    </fc><fc #6a9955># 右下</fc>
<fc #d4d4d4>    -</fc><fc #b5cea8>0.5</fc><fc #d4d4d4>, -</fc><fc #b5cea8>0.5</fc><fc #d4d4d4>, </fc><fc #b5cea8>0.0</fc><fc #d4d4d4>,  </fc><fc #b5cea8>0.0</fc><fc #d4d4d4>, </fc><fc #b5cea8>1.0</fc><fc #d4d4d4>, </fc><fc #b5cea8>0.0</fc><fc #d4d4d4>,    </fc><fc #6a9955># 左下</fc>
     <fc #b5cea8>0.0</fc><fc #d4d4d4>,  </fc><fc #b5cea8>0.5</fc><fc #d4d4d4>, </fc><fc #b5cea8>0.0</fc><fc #d4d4d4>,  </fc><fc #b5cea8>0.0</fc><fc #d4d4d4>, </fc><fc #b5cea8>0.0</fc><fc #d4d4d4>, </fc><fc #b5cea8>1.0</fc>     <fc #6a9955># 顶部</fc>
<fc #d4d4d4>], </fc><fc #9cdcfe>dtype</fc><fc #d4d4d4>=</fc><fc #ce9178>'f4'</fc><fc #d4d4d4>)</fc>

<fc #9cdcfe>vbo</fc><fc #d4d4d4> = </fc><fc #9cdcfe>ctx</fc><fc #d4d4d4>.</fc><fc #dcdcaa>buffer</fc><fc #d4d4d4>(</fc><fc #9cdcfe>vertices</fc><fc #d4d4d4>.</fc><fc #dcdcaa>tobytes</fc><fc #d4d4d4>())</fc>
'''

code2_src = '''
<fc #569cd6>#version</fc> <fc #b5cea8>330</fc><fc #d4d4d4> core</fc>

<fc #569cd6>in</fc> <fc #569cd6>vec3</fc><fc #d4d4d4> in_vert;    </fc><fc #6a9955>// 输入一个位置</fc>
<fc #569cd6>in</fc> <fc #569cd6>vec3</fc><fc #d4d4d4> in_color;   </fc><fc #6a9955>// 输入一个颜色</fc>

<fc #569cd6>out</fc> <fc #569cd6>vec3</fc><fc #d4d4d4> v_color;   </fc><fc #6a9955>// 向片段着色器输出一个颜色</fc>

<fc #569cd6>void</fc><fc #d4d4d4> main()</fc>
<fc #d4d4d4>{</fc>
    <fc #9cdcfe>gl_Position</fc><fc #d4d4d4> = </fc><fc #569cd6>vec4</fc><fc #d4d4d4>(in_vert, </fc><fc #b5cea8>1.0</fc><fc #d4d4d4>);</fc>
<fc #d4d4d4>    v_color = in_color;</fc>
<fc #d4d4d4>}</fc>
'''

code3_src = '''
<fc #569cd6>#version</fc> <fc #b5cea8>330</fc><fc #d4d4d4> core</fc>

<fc #569cd6>in</fc> <fc #569cd6>vec3</fc><fc #d4d4d4> v_color;</fc>

<fc #569cd6>out</fc> <fc #569cd6>vec4</fc><fc #d4d4d4> FragColor;</fc>

<fc #569cd6>void</fc><fc #d4d4d4> main()</fc>
<fc #d4d4d4>{</fc>
<fc #d4d4d4>    FragColor = </fc><fc #569cd6>vec4</fc><fc #d4d4d4>(v_color, </fc><fc #b5cea8>1.0</fc><fc #d4d4d4>);</fc>
<fc #d4d4d4>}</fc>
'''


class SurBox(Group):
    def __init__(self, item: Item, text: str, buff=MED_SMALL_BUFF, color=BLUE, **kwargs):
        sur = SurroundingRect(item, buff=buff, color=color)
        txt = Text(text, font_size=18, color=BLUE)
        txt.points.next_to(sur, UP, aligned_edge=LEFT)
        super().__init__(sur, txt)


class MoreAttr(Template):
    def construct(self) -> None:
        #########################################################

        frame = ImageItem('ShaderProgramAndVertexArray.mp4_20240919_082340.350.jpg', height=5)
        frame_sur = SurroundingRect(frame, buff=0, color=BLUE)
        frame_txt = Text('第5节 你好，三角形', font_size=16)
        frame_txt.points.next_to(frame, UP, buff=SMALL_BUFF)
        frameg = Group(frame, frame_sur, frame_txt)

        hl1 = HighlightRect(Rect([0.35, 1.69, 0], [3.57, 0.17, 0]))
        hl2 = HighlightRect(Rect([-3.41, -0.91, 0], [2.69, -1.8, 0]))

        hl3 = HighlightRect(Rect([1.5, 1.3, 0], [3.52, -0.5, 0]))

        verts = DotCloud(RIGHT * 3, RIGHT * 2, RIGHT * 2.5 + UP * 0.9, color=ORANGE)

        code1 = Text(
            code1_src,
            format=Text.Format.RichText,
            font_size=16
        )

        #########################################################

        self.forward()

        self.prepare(FadeIn(frameg, scale=1.2))

        t = self.aas('1.mp3', '在前面的教程中')
        self.forward_to(t.end + 0.2)

        self.prepare(FadeIn(hl1), duration=1.5)

        t = self.aas('2.mp3', '我们了解了如何填充 VBO')
        self.forward_to(t.end + 0.4)

        self.prepare(Transform(hl1, hl2), at=1.5)

        t = self.aas('3.mp3', '以及如何将着色器程序与 VBO 绑定为一个 VAO')
        self.forward_to(t.end + 0.8)

        t = self.aas('4.mp3', '之前的这个顶点数据指定了三个顶点的位置')

        self.prepare(
            FadeOut(hl2),
            frameg.anim(duration=1.5)
                .points.scale(2).shift(LEFT * 3.95 + DOWN * 1.78),
            duration=t.duration
        )
        self.prepare(FadeIn(verts, scale=0.8), FadeIn(hl3), at=2)

        self.forward_to(t.end + 0.6)

        self.prepare(
            verts.anim.color.set(['#ff0000', '#00ff00', '#0000ff'])
                .r.radius.set(0.08),
            at=1.5
        )

        t = self.aas('5.mp3', '这次，我们同样打算把颜色数据加进顶点数据中')
        self.forward_to(t.end)

        self.play(
            Aligned(
                verts.anim.points.shift(UR * 2 + LEFT * 0.5),
                FadeOut(frameg),
                Write(code1)
            )
        )
        hl3.hide()

        #########################################################

        hl4 = HighlightRect(Rect([-0.19, 0.98, 0], [1.83, -0.46, 0]))
        surbox_vertdata = SurBox(code1, '顶点数据')

        code2 = Text(
            code2_src,
            format=Text.Format.RichText,
            font_size=16
        )
        code2.points.shift(RIGHT * 8)
        surbox_vert = SurBox(code2, '顶点着色器')

        arrow1 = Arrow(code1, code2, color=BLUE)

        sur1 = SurroundingRect(
            code2[3:5],
            color=YELLOW_D,
            fill_alpha=0.15,
            stroke_alpha=0.3,
            depth=10,
            buff=0.03
        )
        sur2 = SurroundingRect(
            code2[4],
            fill_alpha=0.25,
            depth=10,
            buff=0.03
        )
        sur3 = SurroundingRect(
            code2[11],
            fill_alpha=0.1,
            depth=10,
            buff=0.03,
            stroke_radius=0.01
        )

        code3 = Text(
            code3_src,
            format=Text.Format.RichText,
            font_size=16
        )
        code3.points.next_to(code2, buff=LARGE_BUFF)

        surbox_frag = SurBox(code3, '片段着色器')
        arrow2 = Arrow(code2, code3, color=BLUE)

        sur4 = SurroundingRect(
            code3[3],
            fill_alpha=0.1,
            depth=10,
            buff=0.03,
            stroke_radius=0.01
        )

        txt_result = Text('最终输出', font_size=18, color=BLUE)
        txt_result.points.next_to(code3, buff=1.5)
        arrow3 = Arrow(code3, txt_result, color=BLUE)

        #########################################################

        self.prepare(FadeIn(hl4), duration=2)

        t = self.aas('6.mp3', '我们把颜色数据以 3 个 float 值的形式写到 vertices 数组中')
        self.forward_to(t.end + 0.2)
        t = self.aas('7.mp3', '这样把三角形的三个角分别指定为红色、绿色和蓝色')
        self.forward_to(t.end)

        self.play(FadeOut(hl4), FadeIn(surbox_vertdata, at=0.2))

        t = self.aas('8.mp3', '由于现在有更多的数据要发送到顶点着色器')
        self.forward_to(t.end + 0.2)

        self.prepare(
            Write(code2),
            FadeIn(surbox_vert, scale=0.8),
            GrowArrow(arrow1),
            self.camera.anim(duration=1.5).points.shift(RIGHT * 6),
            verts.anim.color.fade(0.5),
            duration=2.6
        )

        t = self.aas('9.mp3', '我们有必要去调整一下顶点着色器')
        self.forward_to(t.end + 0.4)

        self.prepare(
            FadeIn(sur1),
            FadeIn(sur2, at=0.2),
            at=1
        )

        t = self.aas('10.mp3', '使它能够多接受一个颜色值作为输入')
        self.forward_to(t.end + 0.8)
        t = self.aas('11.mp3', '在顶点着色器这里')
        self.forward_to(t.end + 0.2)

        self.play(
            FadeOut(sur1),
            Transform(sur2, sur3, path_arc=40 * DEGREES),
            at=0.5
        )

        t = self.aas('12.mp3', '我们将 `v_color` 直接设置为从顶点数据那里得到的输入颜色')
        self.forward_to(t.end + 0.8)

        self.prepare(
            Write(code3),
            FadeIn(surbox_frag, scale=0.8),
            GrowArrow(arrow2),
            self.camera.anim(duration=1.5).points.shift(RIGHT * 6)
        )

        t = self.aas('13.mp3', '在片段着色器这里', delay=0.5)
        self.forward_to(t.end + 0.3)
        t = self.aas('14.mp3', '我们不再使用 uniform 来传递片段的颜色了')
        self.forward_to(t.end + 0.3)

        self.prepare(
            FadeIn(sur4),
            at=1,
            duration=2
        )

        t = self.aas('15.mp3', '而是使用从顶点着色器传递过来的 `v_color`')
        self.forward_to(t.end)

        self.play(
            GrowArrow(arrow3),
            FadeIn(txt_result, at=0.2)
        )

        self.play(
            FadeOut(Group(sur3, sur4)),
            self.camera.anim(duration=2)
                .points.shift(LEFT * 8 + DOWN).scale(1.2),
            duration=1.5
        )

        t = self.aas('16.mp3', '因为我们添加了另一个顶点属性')
        t = self.aas('17.mp3', '并且更新了 VBO 的内存', delay=t.duration + 0.2)

        self.prepare(
            ShowPassingFlashAround(code2[4]),
            at=1
        )
        self.prepare(
            ShowPassingFlashAround(Rect([-0.11, -0.2, 0], [1.58, 0.84, 0])),
            at=3
        )
        self.forward_to(t.end + 0.4)

        #########################################################

        code4 = Text(
            "<fc #9cdcfe>vao</fc><fc #d4d4d4> = </fc><fc #9cdcfe>ctx</fc><fc #d4d4d4>.</fc><fc #dcdcaa>vertex_array</fc><fc #d4d4d4>(</fc><fc #9cdcfe>prog</fc><fc #d4d4d4>, </fc><fc #9cdcfe>vbo</fc><fc #d4d4d4>, </fc><fc #ce9178>'in_vert'</fc><fc #d4d4d4>, </fc><fc #ce9178>'in_color'</fc><fc #d4d4d4>)</fc>",
            format=Text.Format.RichText,
            font_size=18
        )
        code4.points.next_to(arrow1, DOWN, buff=3)

        psur = partial(
            SurroundingRect,
            stroke_alpha=0,
            fill_alpha=0.3,
            color=WHITE,
            depth=10,
            buff=0.05
        )

        sur1 = psur(code2[3])
        sur2 = psur(code2[3:5])
        sur3 = psur(code1[3][:19])
        sur4 = psur(code1[3][:35])
        sur5 = psur(code1[4][:35])
        sur6 = psur(code1[5][:35])
        Group(sur5, sur6)(VItem).color.set(YELLOW)

        #########################################################

        t = self.aas('18.mp3', '我们必须更改一下 VAO 中关于顶点属性绑定的声明')
        self.forward_to(t.end)

        self.play(Write(code4))

        t = self.aas('19.mp3', '可以发现')
        self.forward_to(t.end)

        self.prepare(
            ShowCreationThenFadeAround(code4[0][45:55]),
            at=1.5
        )

        t = self.aas('20.mp3', '这里我们加了一个对 in_color 属性的绑定')
        self.forward_to(t.end + 0.4)
        t = self.aas('21.mp3', '这表明将顶点数据传递给顶点着色器时')
        self.forward_to(t.end + 0.2)

        self.prepare(
            Create(sur1, at=0.7),
            Create(sur3, at=0.7),
            self.camera.anim.points.scale(0.8).shift(UP * 0.8 + LEFT * 0.4),
        )

        t = self.aas('22.mp3', '首先读取一个位置属性')
        self.forward_to(t.end + 0.4)

        self.prepare(
            Transform(sur1, sur2),
            Transform(sur3, sur4),
            at=0.6,
            duration=1.5
        )

        t = self.aas('23.mp3', '然后还要再读取一个颜色属性')
        self.forward_to(t.end + 0.1)

        self.prepare(
            Indicate(Group(sur2, sur4), scale_factor=1),
            CircleIndicate(Dot(verts.points.get()[0]), scale=1.2),
            verts.anim(duration=0.5).color.set(alpha=[1, 0.5, 0.5]),
            at=0.4
        )

        t = self.aas('24.mp3', '作为一个顶点的输入')
        self.forward_to(t.end + 0.7)
        t = self.aas('25.mp3', '依照这样的方式读取完三个顶点的属性')
        self.forward_to(t.end)

        self.prepare(
            CircleIndicate(Dot(verts.points.get()[1]), scale=1.2),
            verts.anim(duration=0.5).color.set(alpha=[1, 1, 0.5])
        )
        self.play(
            Transform(sur4, sur5, duration=0.5)
        )
        self.play(
            sur5.anim(duration=0.5).color.set(WHITE)
        )

        self.prepare(
            CircleIndicate(Dot(verts.points.get()[2]), scale=1.2),
            verts.anim(duration=0.5).color.set(alpha=1)
        )
        self.play(
            Transform(sur5, sur6, duration=0.5)
        )
        self.play(
            sur6.anim(duration=0.5).color.set(WHITE)
        )

        t = self.aas('26.mp3', '这样顶点着色器就能正确地读取我们的顶点数据')
        self.forward_to(t.end)

        self.play(
            Destruction(sur6),
            Destruction(sur2)
        )
        self.forward()


class MoreAttrSubtitle(SubtitlesTemplate):
    subtitles = [
        ('27.mp3', '运行程序，你应该会看到这样的结果'),
        ('28.mp3', '如果出现了什么问题，你可以参考这节的源代码'),
    ]


class FragInterp(Template):
    def construct(self) -> None:
        #########################################################

        shaders3 = ImageItem('shaders3.png').show()
        verts = DotCloud(
            [1.06, -0.87, 0], [-1.07, -0.85, 0], [0, 0.76, 0],
            color=['#ff0000', '#00ff00', '#0000ff'],
            radius=0.1
        )

        txt_fraginterp = Text('片段插值', font='LXGW WenKai Lite', font_size=30)

        #########################################################

        self.forward()

        t = self.aas('29.mp3', '这个三角形可能与你想象的有点不同')
        self.forward_to(t.end + 0.2)

        self.prepare(FadeOut(shaders3), FadeIn(verts), duration=2)

        t = self.aas('30.mp3', '因为我们只提供了三个颜色')
        self.forward_to(t.end + 0.3)

        self.prepare(FadeOut(verts), FadeIn(shaders3), duration=2)

        t = self.aas('31.mp3', '而不是我们现在看到的大调色板')
        self.forward_to(t.end + 0.5)

        verts.radius.set(0.065)
        self.prepare(
            shaders3.anim.color.fade(0.5),
            FadeIn(verts),
            self.camera.anim.points.scale(0.6)
        )
        self.prepare(
            ShowIncreasingSubsets(txt_fraginterp[0]),
            at=2
        )

        t = self.aas('32.mp3', '这是在片段着色器中进行所谓片段插值的结果')
        self.forward_to(t.end)

        #########################################################

        x1, y1 = -2.18, -1.68
        x2, y2 = 2.17, 1.57
        xbase = x1 + 0.02
        ybase = y1 + 0.02

        hor_lines = Group(
            *[
                Line([x1, y, 0], [x2, y, 0], stroke_radius=0.005)
                for y in np.arange(ybase, y2, 0.1)
            ],
            color=GREY
        )
        ver_lines = Group(
            *[
                Line([x, y1, 0], [x, y2, 0], stroke_radius=0.005)
                for x in np.arange(xbase, x2, 0.1)
            ],
            color=GREY
        )

        #########################################################

        self.play(FadeOut(txt_fraginterp))

        t = self.aas('33.mp3', '当渲染一个三角形时')
        self.forward_to(t.end)

        self.prepare(
            Create(hor_lines, lag_ratio=0.05),
            Create(ver_lines, lag_ratio=0.05, at=0.2),
            duration=0.7,
            at=1.4
        )

        t = self.aas('34.mp3', '光栅化阶段通常会造成比原指定顶点更多的片段', mul=1.2)
        self.forward_to(t.end)

        self.play(
            Group(hor_lines, ver_lines)(VItem).anim.color.fade(0.7),
            duration=0.5
        )
        # self.play(
        #     Destruction(hor_lines, lag_ratio=0.05),
        #     Destruction(ver_lines, lag_ratio=0.05, at=0.2)
        # )

        ###########################################################

        points = verts.points.get()
        orig = points[1]
        v1 = points[2] - orig
        v2 = points[0] - orig

        c_orig = np.array([0, 1, 0])
        c_v1 = np.array([0, -1, 1])
        c_v2 = np.array([1, -1, 0])

        p_tracker = ValueTracker(
            np.sum(points, axis=0) / 3,
            maybe_same_func=lambda a, b: np.all(a == b)
        )

        def dot_updater(dot: Circle, p: UpdaterParams) -> None:
            point = p_tracker.current().data.get()

            vred = points[0] - point
            vgreen = points[1] - point
            vblue = points[2] - point

            all = abs(cross2d(v1, v2)) / 2
            red = abs(cross2d(vgreen, vblue)) / 2 / all
            green = abs(cross2d(vred, vblue)) / 2 / all
            blue = abs(cross2d(vred, vgreen)) / 2 / all

            dot.points.move_to(point)
            dot.fill.set([red, green, blue])

        def arrow_updater(pos: np.ndarray) -> Arrow:
            arrow = Arrow(
                p_tracker.current().data.get(),
                pos,
                max_length_to_tip_length_ratio=1,
                tip_kwargs=dict(
                    back_width=0.1,
                    body_length=0.1
                ),
                buff=0.15,
                color=GREY_A
            )
            return arrow

        def arrows_updater(p: UpdaterParams):
            return Group(*[
                arrow_updater(point)
                for point in points
            ])

        dot = Circle(radius=0.1, stroke_radius=0.01, fill_alpha=1)

        ###########################################################

        t = self.aas('35.mp3', '光栅会根据每个片段相对于三角形形状的相对位置', mul=1.2)

        t = self.aas(
            '36.mp3',
            [
                '插值片段着色器的所有输入变量',
                '（对，所有，无论是颜色还是位置或者是你传递的某个向量）'
            ],
            scale=[1, 0.7],
            delay=4
        )

        dot_updater(dot, None)
        self.play(
            Create(dot),
            FadeIn(arrows_updater(None), show_at_end=False)
        )
        self.prepare(
            DataUpdater(dot, dot_updater),
            ItemUpdater(None, arrows_updater),
            duration=5.5
        )
        self.play(
            p_tracker.anim.data.increment(UP * 0.4 + RIGHT * 0.05),
            duration=1.5
        )
        self.play(
            p_tracker.anim.data.increment(DOWN * 0.8 + LEFT * 0.4),
            duration=1.8
        )
        self.play(
            p_tracker.anim.data.increment(RIGHT * 1 + UP * 0.2),
            duration=2.2
        )
        dot_updater(dot, None)
        self.play(Uncreate(dot), FadeOut(arrows_updater(None)))

        self.prepare(
            *[
                CircleIndicate(Dot(pos))
                for pos in verts.points.get()
            ],
            at=2,
            duration=2
        )

        t = self.aas('37.mp3', '这也就导致了这个三角形的三个顶点是我们设置的三个颜色')
        self.forward_to(t.end + 0.3)

        self.prepare(
            shaders3.anim.color.set(alpha=1),
            FadeOut(verts),
            FadeOut(Group(hor_lines, ver_lines)),
            at=0.4,
            duration=1.6
        )

        t = self.aas('38.mp3', '而中间的部分是这三个颜色的过渡')
        self.forward_to(t.end + 2)


class Notes(Template):
    CONFIG = Config(
        fps=120
    )
    def construct(self) -> None:
        notes = [
            '顶点缓冲对象 <fs 0.8>(Vertex Buffer Object, VBO)</fs>',
            '顶点数组对象 <fs 0.8>(Vertex Array Object, VAO)</fs>',
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
