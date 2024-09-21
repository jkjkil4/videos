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
    str2 = '着色器'


class Intro(Template):
    def construct(self) -> None:
        self.forward()

        #########################################################

        video = Video(
            R'2024\LearnOpenGL-5-HelloTriangle\kdenlive\janim_src\Pipeline1.mp4',
            height=Config.get.frame_height - 3
        ).show()
        sur = SurroundingRect(video, color=WHITE)
        videog = Group(video, sur)

        box1 = SVGItem('box.svg', height=1, color=WHITE)
        box1.points.move_to([-2.04, 0.09, 0])

        box2 = box1.copy()
        box2.points.move_to([2.36, 0.09, 0])

        box3 = box2.copy()
        box3.points.shift(box2.points.box.center - box1.points.box.center)

        arrow12 = Arrow(box1, box2, buff=0.8)
        arrow12txt = arrow12.create_text('着色器')

        arrow23 = Arrow(box2, box3, buff=0.8)
        arrow23txt = arrow23.create_text('着色器')

        tip1 = Text('输入', color=BLUE)
        tip1.points.move_to(box1).shift(UP * 1.8 + LEFT * 0.5)

        arrow1 = Arrow(tip1, box1, color=BLUE)

        tip2 = Text('输出', color=BLUE)
        tip2.points.move_to(box2).shift(UP * 1.8 + RIGHT * 0.5)

        tip2_ = Text('前一个的输出\n后一个的输入', font_size=12, color=BLUE)
        tip2_.points.move_to(tip2)

        arrow2 = Arrow(tip2, box2, color=BLUE)

        circle = Circle(2, color=GREY)
        circle.points.move_to(arrow12txt)

        #########################################################

        video.seek(50)
        # video.start()

        self.play(FadeIn(video), Write(sur))
        self.forward()
        self.play(videog.anim.points.scale(2).shift(UR * 2.6))
        self.forward()
        self.play(
            FadeOut(videog, duration=1.5),
            Create(Group(box1, box2)),
            GrowArrow(arrow12),
            Write(arrow12txt)
        )
        self.forward()
        self.play(
            Write(tip1),
            GrowArrow(arrow1)
        )
        self.forward()
        self.play(Transform(Group(tip1, arrow1), Group(tip2, arrow2), path_arc=-50 * DEGREES))
        self.forward()
        self.play(
            Create(box3),
            GrowArrow(arrow23),
            Write(arrow23txt),
            self.camera.anim.points.shift(RIGHT * 1.5)
        )
        self.play(
            FadeTransform(tip2, tip2_, duration=0.6),
            Indicate(box2, at=0.3)
        )
        self.forward()
        random.seed(114514)
        self.play(
            FadeOut(
                Group(box1, box2, box3, arrow12, arrow23, arrow23txt, arrow2, tip2_)
                    .shuffle(),
                lag_ratio=0.5
            ),
            self.camera.anim.points.move_to(arrow12txt),
            duration=2
        )
        self.forward()
        self.play(FadeIn(circle, scale=0.8))
        self.forward()


code1_src = '''
<fc #569cd6>#version</fc><fc #d4d4d4> version_number</fc>

<fc #569cd6>in</fc><fc #d4d4d4> 类型 输入变量名;</fc>
<fc #569cd6>in</fc><fc #d4d4d4> 类型 输入变量名;</fc>

<fc #569cd6>out</fc><fc #d4d4d4> 类型 输出变量名;</fc>

<fc #569cd6>uniform</fc><fc #d4d4d4> 类型 uniform名;</fc>

<fc #569cd6>void</fc><fc #d4d4d4> main()</fc>
<fc #d4d4d4>{</fc>
    <fc #6a9955>// 处理输入并进行一些图形操作</fc>
<fc #d4d4d4>    ...</fc>
    <fc #6a9955>// 输出处理过的结果到输出变量</fc>
<fc #d4d4d4>    输出变量名 = 经过各种乱七八糟处理后得到的东西;</fc>
<fc #d4d4d4>}</fc>
'''

typ1_src = '''
#let v(body) = {
    set text(fill: rgb("#569cd6"))
    body
}
#let d(body) = {
    set text(size: 0.7em, fill: gray)
    body
}

#set text(font: "Noto Sans S Chinese")

#grid(
    columns: 2,
    gutter: 4pt,
    v[`float`], d[浮点数(小数)],
    v[`double`], d[双精度浮点数],
    v[`int`], d[整数],
    v[`uint`], d[无符号整数],
    v[`bool`], d[条件标记],
)
'''


class GLSL(SubtitleTemplate2):
    name = 'GLSL'

    def construct(self) -> None:
        super().construct()

        #########################################################

        code1 = Text(
            code1_src,
            format=Text.Format.RichText,
            font_size=16
        )
        random.seed(1145140)
        code1_shuffle = Group(*code1).shuffle()

        sur_config = dict(
            stroke_radius=0.01,
            fill_alpha=0.2,
            color=YELLOW,
            depth=10
        )
        psur = partial(SurroundingRect, **sur_config)

        rect = psur(code1[1])

        hl_uniform = HighlightRect(code1[8])

        #########################################################

        self.play(FadeIn(code1_shuffle, lag_ratio=0.1))
        self.forward()
        self.play(FadeIn(rect))
        self.forward()
        self.play(
            rect.anim.become(psur(code1[3:5]))
        )
        self.forward()
        self.play(
            rect.anim.become(psur(code1[6]))
        )
        self.forward()
        self.play(
            rect.anim.become(psur(code1[8]))
        )
        self.forward()
        self.play(
            rect.anim.become(psur(code1[10:17]))
        )
        self.forward()
        rect_copy = rect.copy().show()
        rect_copy.fill.set(alpha=0)
        rect_copy.stroke.set(alpha=0.4)
        rect_copy.depth.set(1)
        self.play(
            rect.anim.become(psur(code1[12:14]))
        )
        self.forward()
        self.play(
            rect.anim.become(psur(code1[14:16]))
        )
        self.forward()
        self.play(
            FadeOut(rect_copy),
            FadeOut(rect),
            FadeIn(hl_uniform, at=0.5)
        )
        self.forward()
        self.play(FadeOut(hl_uniform))
        self.forward()

        #########################################################

        title = Title('数据类型').fix_in_frame()
        hl_type = boolean_ops.Difference(
            SurroundingRect(code1),
            VItem(
                [-2.69, 1.83, 0], [-2.7, 1.5, 0], [-2.67, 1.2, 0], [-2.66, 0.9, 0], [-2.56, 0.67, 0],
                [-2.39, 0.48, 0], [-2.19, 0.33, 0], [-2.06, 0.12, 0], [-1.91, -0.02, 0], [-1.62, -0.12, 0],
                [-1.43, -0.02, 0], [-1.35, 0.18, 0], [-1.5, 0.43, 0], [-1.7, 0.52, 0], [-1.93, 0.63, 0],
                [-2.05, 0.84, 0], [-2.07, 1.15, 0], [-2.03, 1.5, 0], [-2.07, 1.76, 0], [-2.2, 1.95, 0],
                [-2.57, 1.91, 0]
            ).points.close_path().r,
            **HighlightRect.difference_config_d
        )

        txt_types = TypstText(typ1_src)
        txt_types.points.shift(RIGHT * 3 + UP * 0.6)

        brace = Brace(txt_types, LEFT)

        #########################################################

        self.play(Transform(self.title, title))
        self.title = title
        self.forward()
        self.play(FadeIn(hl_type))
        self.forward()
        self.play(
            Write(brace),
            Write(Group(txt_types[:3], txt_types[5:10], txt_types[13:19], txt_types[25:29], txt_types[34:38])),
            lag_ratio=0.5
        )
        random.seed(1145140)
        self.play(
            Write(
                Group(txt_types[3:5], txt_types[10:13], txt_types[19:25], txt_types[29:34], txt_types[38:]).shuffle(),
                lag_ratio=0.02
            ),
            duration=1
        )
        self.forward()
        self.play(
            self.camera.anim.points.shift(RIGHT * 7),
            FadeOut(code1)
        )
        hl_type.hide()
        self.forward()

        #########################################################

        txt_types_g = Group(txt_types, brace)

        cov_types = SurroundingRect(txt_types_g, **HighlightRect.difference_config_d)

        st_vector = Group(Arrow(DL * 0.8, UR * 0.8), Text('向量'))
        st_matrix = TypstText(
            '#let mattxt = {\n'
            '    set text(font: "Noto Sans S Chinese")\n'
            '    [矩阵]\n'
            '}\n'
            '$ mat(delim: "[", ,,;space,mattxt,space;,,) $'

        )
        stg = Group(st_vector, st_matrix)
        stg.points.arrange(buff=LARGE_BUFF).move_to(self.camera)

        txt_basic = Text('基本类型')
        txt_basic.points.next_to(txt_types_g, UP, buff=0.4)

        #########################################################

        self.play(
            FadeIn(cov_types),
            Write(st_vector, at=0.4),
            Write(st_matrix, at=0.8)
        )
        self.forward()
        self.play(
            FadeOut(cov_types),
            FadeOut(st_matrix),
            FadeOut(st_vector[0]),
            Write(txt_basic),
            st_vector[1].anim.points.shift(UP * 2 + RIGHT),
            self.camera.anim.points.shift(UP)
        )
        self.forward()

        #########################################################

        vec_template = '''
        #let v(body) = {{
            set text(fill: rgb("#569cd6"))
            body
        }}
        #let elem = {elem}
        #let cnt = {cnt}
        #let arr = for _ in range(cnt) {{
            (elem,)
        }}
        #let arr = arr.intersperse($,$)
        $(#for a in arr {{a}})$
        '''
        def template_g(elem: str) -> Group[TypstText]:
            return Group(*[
                TypstText(
                    vec_template
                    .format(elem=elem, cnt=cnt)
                )
                for cnt in range(2, 5)
            ])

        def type_g(t: str):
            return Group(*[
                TypstText(
                    '#set text(fill: rgb("#569cd6"))\n'
                    f'`{t}{cnt}` :'
                )
                for cnt in range(2, 5)
            ])

        circle_g = template_g('circle(fill: aqua, radius: 4pt)')
        circle_g.points.arrange(DOWN, aligned_edge=LEFT) \
            .next_to(st_vector[1], DOWN, aligned_edge=LEFT, buff=0.4)

        type_names = Group(txt_types[:5], txt_types[12:18], txt_types[24:27], txt_types[29:33], txt_types[38:42])
        txt_types.show()

        def create_gvecn(t: str, elem: str):
            g = Group(
                type_g(t),
                template_g(elem)
            )
            g[1].points.arrange(DOWN, aligned_edge=LEFT)
            g.points.next_to_by_indicator(g[1], circle_g.points.box.left, RIGHT, buff=0)
            for a, b in zip(g[0], g[1]):
                a.points.next_to(b, LEFT)
            return g

        vecn = create_gvecn('vec', 'v[`float`]')
        dvecn = create_gvecn('dvec', 'v[`double`]')
        ivecn = create_gvecn('ivec', 'v[`int`]')
        uvecn = create_gvecn('uvec', 'v[`uint`]')
        bvecn = create_gvecn('bvec', 'v[`bool`]')

        udl_vec2 = Underline(vecn[1][0], color=YELLOW)
        udl_vec3 = Underline(vecn[1][1], color=YELLOW)

        #########################################################

        circle_g[0].show()
        self.forward()
        circle_g[1].show()
        self.forward()
        circle_g[2].show()
        self.forward()
        self.play(Indicate(type_names, scale_factor=1.1))
        self.forward()
        self.play(
            Write(vecn[0]),
            Transform(circle_g, vecn[1], at=0.2)
        )
        self.forward()
        self.play(ShowCreationThenDestruction(udl_vec2, time_width=3))
        self.forward()
        self.play(ShowCreationThenDestruction(udl_vec3, time_width=3))
        self.forward()
        self.play(Transform(vecn, dvecn))
        self.forward()
        self.play(Transform(dvecn, ivecn))
        self.forward()
        self.play(Transform(ivecn, uvecn))
        self.forward()
        self.play(Transform(uvecn, bvecn))
        self.forward()
        self.play(
            FadeOut(bvecn),
            FadeIn(vecn, at=0.5)
        )
        self.forward()
        self.play(ShowCreationThenFadeAround(vecn))
        self.forward()

        #########################################################

        cov = boolean_ops.Union(
            Rect([5.09, 2.31, 0], [9.74, 0.3, 0]),
            Rect([1.26, 2.46, 0], [4.59, -0.43, 0]),
            **HighlightRect.difference_config_d
        )

        def get_gletters(letters: str):
            g = Group(*[
                Text(f'.{letter}')
                for letter in letters
            ])
            g.points.arrange(buff=LARGE_BUFF).next_to(vecn, DOWN, buff=LARGE_BUFF)
            return g

        letters = get_gletters('xyzw')
        rgba_letters = get_gletters('rgba')
        stpq_letters = get_gletters('stpq')

        arrows = Group(*[
            Arrow(letter, vecn[1][-1][s])
            for letter, s in zip(letters, [slice(1,6), slice(7,12), slice(13,18), slice(19,24)])
        ])

        #########################################################

        self.play(
            self.camera.anim.points.shift(DOWN),
            FadeIn(cov)
        )
        self.forward()
        self.play(
            Write(letters[0]),
            GrowArrow(arrows[0])
        )
        self.forward()
        self.play(
            *[
                AnimGroup(Write(letters[i]), GrowArrow(arrows[i]))
                for i in range(1, 4)
            ],
            lag_ratio=0.5
        )
        self.forward()
        self.play(
            letters(VItem).anim
                .points.next_to(rgba_letters, DOWN, buff=SMALL_BUFF)
                .r.color.set(GREY_D),
            FadeIn(rgba_letters)
        )
        self.forward()
        self.play(
            Group(letters, rgba_letters)(VItem).anim
                .points.next_to(stpq_letters, DOWN, buff=SMALL_BUFF)
                .r.color.set(GREY_D),
            FadeIn(stpq_letters)
        )
        self.forward()
        self.play(
            Group(letters)(VItem).anim.color.set(WHITE),
            Group(stpq_letters)(VItem).anim.color.set(GREY_D)
        )
        self.forward()


code2_src = '''
<fc #569cd6>vec2</fc><fc #d4d4d4> someVec;</fc>
<fc #569cd6>vec4</fc><fc #d4d4d4> differentVec = someVec.xyxx;</fc>
<fc #569cd6>vec3</fc><fc #d4d4d4> anotherVec = differentVec.zyw;</fc>
<fc #569cd6>vec4</fc><fc #d4d4d4> otherVec = someVec.xxxx + anotherVec.yxzy;</fc>
'''

code3_src = '''
<fc #569cd6>vec2</fc><fc #d4d4d4> vect = </fc><fc #569cd6>vec2</fc><fc #d4d4d4>(</fc><fc #b5cea8>0.5</fc><fc #d4d4d4>, </fc><fc #b5cea8>0.7</fc><fc #d4d4d4>);</fc>
<fc #569cd6>vec4</fc><fc #d4d4d4> result = </fc><fc #569cd6>vec4</fc><fc #d4d4d4>(vect, </fc><fc #b5cea8>0.0</fc><fc #d4d4d4>, </fc><fc #b5cea8>0.0</fc><fc #d4d4d4>);</fc>
<fc #569cd6>vec4</fc><fc #d4d4d4> otherResult = </fc><fc #569cd6>vec4</fc><fc #d4d4d4>(result.xyz, </fc><fc #b5cea8>1.0</fc><fc #d4d4d4>);</fc>
'''


class Swizzling(Template):
    def construct(self) -> None:
        title = Title('数据类型').show()

        #########################################################

        swizzling = Text(
            f'重组{s1}(Swizzling){s2}',
            format=Text.Format.RichText
        )
        swizzling.points.next_to(title, DOWN, buff=MED_LARGE_BUFF)

        code2 = Text(
            code2_src,
            format=Text.Format.RichText,
            font_size=18
        )
        code2.points.shift(UP * 0.5)
        code3 = Text(
            code3_src,
            format=Text.Format.RichText,
            font_size=18
        )
        code3.points.next_to(code2, DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)

        pudl = partial(
            Underline,
            buff=0.05,
            color=YELLOW
        )

        udls1 = Group(
            pudl(code2[2][28:32]),
            pudl(code2[3][31:34]),
            Group(pudl(code2[4][24:28]), pudl(code2[4][42:46])),
        )

        udls2 = Group(
            pudl(code2[2][:17]),
            pudl(code2[3][:15]),
            Group(pudl(code2[4][:13])),
        )

        udlvect = pudl(code3[2][19:23])
        udlvecta = pudl(code3[2][25:33])
        # udlresultxyz = pudl(code3[3][24:34])
        # udlresultxyza = pudl(code3[3][36:39])

        rect = Rect(
            Config.get.frame_width, 0.2,
            stroke_alpha=0,
            fill_alpha=1,
            fill_color=RED_E
        )
        rect.points.to_border(UP, buff=0)
        rect.points.shift(LEFT * Config.get.frame_width)

        #########################################################

        self.forward()
        self.play(DrawBorderThenFill(swizzling))
        self.forward()
        self.play(Write(code2))
        self.forward()
        self.play(Create(udls1, lag_ratio=0.6))
        self.forward()
        self.play(
            *[
                AnimGroup(
                    Transform(udl1, udl2, hide_src=False),
                    udl1(VItem).anim(duration=0.5).color.fade(0.65)
                )
                for udl1, udl2 in zip(udls1, udls2)
            ],
            lag_ratio=0.6
        )
        self.play(
            udls2(VItem).anim.color.fade(0.5)
        )
        self.forward()
        self.play(Write(code3))
        self.forward()
        self.play(Write(udlvect))
        self.forward()
        self.play(Write(udlvecta))
        self.forward()
        self.play(
            Group(udlvect, udlvecta)(VItem).anim.color.fade(0.65)
        )
        self.forward()

        self.play(
            rect.anim(rate_func=linear)
            .points.shift(RIGHT * Config.get.frame_width),

            duration=2
        )
        self.play(FadeOut(rect))
        self.forward(2)


code4_src = '''
<fc #569cd6>#version</fc> <fc #b5cea8>330</fc><fc #d4d4d4> core</fc>

<fc #569cd6>in 类型</fc><fc #d4d4d4> 变量名1;</fc>

<fc #569cd6>out 类型</fc><fc #d4d4d4> 变量名2;</fc>

<fc #569cd6>void</fc><fc #d4d4d4> main()</fc>
<fc #d4d4d4>{</fc>
<fc #d4d4d4>    ...</fc>
<fc #d4d4d4>}</fc>
'''

code5_src = '''
<fc #569cd6>#version</fc> <fc #b5cea8>330</fc><fc #d4d4d4> core</fc>

<fc #569cd6>in 类型</fc><fc #d4d4d4> 变量名2;</fc>

<fc #569cd6>out vec4</fc><fc #d4d4d4> 变量名3;</fc>

<fc #569cd6>void</fc><fc #d4d4d4> main()</fc>
<fc #d4d4d4>{</fc>
<fc #d4d4d4>    ...</fc>
<fc #d4d4d4>}</fc>
'''

code6_src = '''
<fc #569cd6>#version</fc> <fc #b5cea8>330</fc><fc #d4d4d4> core</fc>

<fc #6a9955>// 从顶点数据得到的输入</fc>
<fc #569cd6>in</fc> <fc #569cd6>vec3</fc><fc #d4d4d4> in_vert;</fc>

<fc #6a9955>// 指定一个传递给片段着色器的输出</fc>
<fc #569cd6>out</fc> <fc #569cd6>vec4</fc><fc #d4d4d4> v_color;</fc>

<fc #569cd6>void</fc><fc #d4d4d4> main()</fc>
<fc #d4d4d4>{</fc>
    <fc #9cdcfe>gl_Position</fc><fc #d4d4d4> = </fc><fc #569cd6>vec4</fc><fc #d4d4d4>(in_vert, </fc><fc #b5cea8>1.0</fc><fc #d4d4d4>);</fc>

    <fc #6a9955>// 把输出变量设置为暗红色</fc>
<fc #d4d4d4>    v_color = </fc><fc #569cd6>vec4</fc><fc #d4d4d4>(</fc><fc #b5cea8>0.5</fc><fc #d4d4d4>, </fc><fc #b5cea8>0.0</fc><fc #d4d4d4>, </fc><fc #b5cea8>0.0</fc><fc #d4d4d4>, </fc><fc #b5cea8>1.0</fc><fc #d4d4d4>);</fc>
<fc #d4d4d4>}</fc>
'''

code7_src = '''
<fc #569cd6>#version</fc> <fc #b5cea8>330</fc><fc #d4d4d4> core</fc>

<fc #6a9955>// 从顶点着色器传来的输入变量</fc>
<fc #6a9955>//（名称相同，类型相同）</fc>
<fc #569cd6>in</fc> <fc #569cd6>vec4</fc><fc #d4d4d4> v_color;</fc>

<fc #6a9955>// 最终输出的颜色</fc>
<fc #569cd6>out</fc> <fc #569cd6>vec4</fc><fc #d4d4d4> FragColor;</fc>

<fc #569cd6>void</fc><fc #d4d4d4> main()</fc>
<fc #d4d4d4>{</fc>
<fc #d4d4d4>    FragColor = v_color;</fc>
<fc #d4d4d4>}</fc>
'''

code8_src = '''
<fc #c586c0>import</fc> <fc #4ec9b0>moderngl</fc>

<fc #9cdcfe>ctx</fc><fc #d4d4d4> = </fc><fc #4ec9b0>moderngl</fc><fc #d4d4d4>.</fc><fc #dcdcaa>create_standalone_context</fc><fc #d4d4d4>()</fc>
<fc #dcdcaa>print</fc><fc #d4d4d4>(</fc><fc #9cdcfe>ctx</fc><fc #d4d4d4>.</fc><fc #9cdcfe>info</fc><fc #d4d4d4>[</fc><fc #ce9178>'GL_MAX_VERTEX_ATTRIBS'</fc><fc #d4d4d4>])</fc>
'''


class InputAndOutput(SubtitleTemplate2):
    name = '输入与输出'

    def construct(self) -> None:
        super().construct()
        self.title.fix_in_frame()

        #########################################################

        def get_code_block(name: str, code: str):
            rect = Rect(5, 4.2, color=BLUE)

            nametxt = Text(name, font_size=14, color=BLUE)
            nametxt.points.next_to(rect, DOWN, aligned_edge=LEFT)

            txt = Text(code, format=Text.Format.RichText, font_size=14)
            txt.points.next_to(rect.points.box.get(UL), DR)

            return Group(rect, nametxt, txt)

        code4_block = get_code_block('顶点着色器', code4_src)
        code5_block = get_code_block('片段着色器', code5_src)
        code6_block = get_code_block('顶点着色器', code6_src)
        code7_block = get_code_block('片段着色器', code7_src)

        vert_block = Group(code4_block, code6_block)
        frag_block = Group(code5_block, code7_block)

        blocks = Group(vert_block, frag_block)
        blocks.points.arrange()

        ra = VItem(stroke_alpha=0, fill_alpha=0.6, color=GREY_E, depth=1)
        ra.points.set_as_corners([RIGHT, UP, UL, ORIGIN, DL, DOWN, RIGHT])

        ras = ra * 10
        ras.points.arrange(buff=-0.3).set_y(code4_block[0].points.box.y)

        cov = Rect([-5.24, 2.46, 0], [5.26, -2.56, 0], **HighlightRect.difference_config_d)
        inout = Text('in & out', font_size=60, color='#569cd6')

        txt_vertdata = Text(
            f'顶点数据\n{s1}Vertex Data{s2}',
            format=Text.Format.RichText,
        )
        txt_vertdata.points.arrange(DOWN, buff=SMALL_BUFF)
        txt_vertdata.points.next_to(code4_block, LEFT, buff=LARGE_BUFF) \
            .shift(UP * 1.5)

        arrow1 = Arrow(txt_vertdata, code4_block[-1][3])

        fr = FrameRect(**HighlightRect.difference_config_d).fix_in_frame()
        ch5 = ImageItem('ShaderProgramAndVertexArray.mp4_20240919_082340.350.jpg', height=5).fix_in_frame()
        ch5_sur = SurroundingRect(ch5, buff=0, color=WHITE).fix_in_frame()
        ch5_title = Text('第5节 你好，三角形').fix_in_frame()
        ch5_title.points.next_to(ch5, UP, buff=SMALL_BUFF)
        ch5g = Group(fr, ch5, ch5_sur, ch5_title)

        vertattr_sur = SurroundingRect(code4_block[-1][3][6:10], color=GOLD, buff=0.05)
        vertattr_txt = Text(
            f'顶点属性\n<fs 0.7>Vertex Attribute</fs>',
            font_size=16,
            format=Text.Format.RichText,
            color=GOLD
        )
        vertattr_txt.arrange_in_lines(buff=-0.05)
        vertattr_txt.points.next_to(code4_block[-1][3])

        tip_cpp_opengl = TypstText(
            '''
            #set text(font: "Noto Sans S Chinese", size: 0.5em, fill: gray)
            在 C++ 传递 OpenGL 顶点属性可能更倾向于使用类似于 `layout (location = 0)`  的标识符，\\
            但是这里我们使用 ModernGL 推荐的方式
            '''
        ).fix_in_frame()
        tip_cpp_opengl.points.to_border(UL, buff=SMALL_BUFF)
        # tip_cpp_opengl.show()

        fr = FrameRect(**HighlightRect.difference_config_d).fix_in_frame()
        code8 = Text(
            code8_src,
            format=Text.Format.RichText,
            font_size=20,
            depth=-1
        ).fix_in_frame()
        code8_sur = SurroundingRect(code8, color=WHITE, fill_alpha=1, fill_color=BLACK, buff=MED_SMALL_BUFF).fix_in_frame()
        code8g = Group(fr, code8, code8_sur)

        cam_stat = self.camera.copy()

        #########################################################

        # self.show(code4_block, code5_block)
        self.play(
            AnimGroup(
                FadeIn(Group(code4_block[:2]), scale=0.95),
                FadeIn(
                    Group(code4_block[2][1], code4_block[2][7:]),
                    at=0.2
                )
            ),
            AnimGroup(
                FadeIn(Group(code5_block[:2]), scale=0.95),
                FadeIn(
                    Group(code5_block[2][1], code5_block[2][7:]),
                    at=0.2
                )
            ),
            lag_ratio=0.3
        )
        self.forward()
        self.play(
            Indicate(code4_block[0], scale_factor=1, rate_func=there_and_back_with_pause),
            Indicate(code5_block[0], scale_factor=1, rate_func=there_and_back_with_pause)
        )
        self.forward()
        self.play(FadeIn(ras))
        self.forward()
        self.play(FadeIn(cov), Write(inout, at=0.3))
        self.forward()
        self.play(
            FadeOut(inout),
            FadeOut(cov),
            self.camera.anim(duration=1.5)
                .points.move_to(code4_block).scale(0.7),
            Write(code4_block[-1][3], at=0.5)
        )
        self.forward()
        self.play(
            self.camera.anim.points.shift(LEFT),
            DrawBorderThenFill(txt_vertdata),
            GrowArrow(arrow1, at=0.3)
        )
        self.forward()
        self.play(
            FadeIn(ch5g)
        )
        self.forward()
        self.play(
            FadeOut(ch5g)
        )
        self.forward()
        self.timeout(0.5, tip_cpp_opengl.show)
        self.play(
            Create(vertattr_sur, auto_close_path=False),
            DrawBorderThenFill(vertattr_txt, duration=1, at=0.3, stroke_radius=0.005)
        )
        self.forward()
        self.play(FadeIn(code8g))
        self.forward()
        self.play(FadeOut(Group(code8g, tip_cpp_opengl, vertattr_sur, vertattr_txt)))
        self.forward()
        self.play(
            self.camera.anim.points.shift(RIGHT * 7),
            duration=2
        )
        self.forward()
        self.play(Write(code5_block[-1][5]))
        self.forward()

        #########################################################

        txt_fragcolor = Text('最终输出的颜色', font_size=20)
        for char, color in zip(txt_fragcolor[0],
                         resize_with_interpolation(Cmpt_Rgbas.format_colors([RED, GREEN, BLUE]),
                                                   len(txt_fragcolor[0]))):
            char.color.set(color)

        txt_fragcolor.points.next_to(code5_block, buff=MED_LARGE_BUFF) \
            .set_y(code5_block[-1][5].points.box.y)

        arrow2 = Arrow(code5_block[-1][5], txt_fragcolor)

        #########################################################

        self.play(
            Write(txt_fragcolor),
            GrowArrow(arrow2, at=0.3)
        )
        self.forward()
        self.play(
            Indicate(code5_block[-1][5][9:13])
        )
        self.forward()
        self.play(
            self.camera.anim.become(cam_stat).points.scale(1.2)
        )
        self.forward()
        self.play(Indicate(ras[:3], scale_factor=1.03))
        self.forward()
        self.play(Indicate(ras[7:], scale_factor=1.03))
        self.forward()
        self.play(
            self.camera.anim.become(cam_stat),
            Indicate(ras[3:7], scale_factor=1.03, color=GOLD, duration=2),
        )
        self.forward()

        #########################################################

        udl1 = Group(
            Underline(code4_block[-1][5][4:6]),
            Underline(code5_block[-1][3][3:5]),
            color=YELLOW
        )
        udl2 = Group(
            Underline(code4_block[-1][5][7:11]),
            Underline(code5_block[-1][3][6:10]),
            color=YELLOW
        )

        arrow3 = Arrow(color=YELLOW)
        arrow3.points.set([
            [-3, 1.04, 0], [-2.78, 1.03, 0], [-2.48, 1.04, 0], [-2.15, 1.03, 0], [-1.81, 1.07, 0],
            [-1.5, 1.18, 0], [-1.28, 1.3, 0], [-1.11, 1.37, 0], [-1.02, 1.41, 0], [-0.94, 1.45, 0],
            [-0.81, 1.48, 0], [-0.62, 1.54, 0], [-0.41, 1.57, 0], [-0.25, 1.59, 0], [-0.11, 1.57, 0],
            [0.05, 1.57, 0], [0.22, 1.57, 0]
        ])
        arrow3.points.shift(DL * 0.05)
        arrow3.place_tip()

        #########################################################

        self.play(
            Write(code4_block[-1][5])
        )
        self.forward()
        self.play(
            Write(code5_block[-1][3])
        )
        self.forward()
        self.play(
            ShowCreationThenDestruction(udl1)
        )
        self.forward(0.2)
        self.play(
            ShowCreationThenDestruction(udl2)
        )
        self.forward()
        self.play(GrowArrow(arrow3))
        self.forward()
        self.play(
            FadeOut(Group(txt_vertdata, arrow1, txt_fragcolor, arrow2, arrow3)),
            FadeTransform(code4_block, code6_block),
            FadeTransform(code5_block, code7_block)
        )
        self.forward()

        #########################################################

        hl_swi = HighlightRect(code6_block[-1][11][18:36])

        udl1 = Underline(code6_block[-1][7], color=YELLOW, buff=0.05)
        udl2 = Underline(code7_block[-1][5], color=YELLOW, buff=0.05)

        arrow = Arrow(color=YELLOW)
        arrow.points.set([
            [-2.81, 0.52, 0], [-2.55, 0.51, 0], [-2.26, 0.56, 0], [-1.94, 0.6, 0], [-1.65, 0.69, 0],
            [-1.42, 0.76, 0], [-1.22, 0.85, 0], [-0.98, 0.96, 0], [-0.7, 1.04, 0], [-0.38, 1.1, 0],
            [-0.11, 1.11, 0], [0.12, 1.13, 0], [0.2, 1.11, 0]
        ])
        arrow.points.shift(DOWN * 0.05)
        arrow.place_tip()

        psur = partial(
            SurroundingRect,
            buff=0.05,
            stroke_alpha=0.6
        )

        sur1 = psur(code6_block[-1][14])
        sur2 = psur(code7_block[-1][12])

        #########################################################

        self.play(FadeIn(hl_swi))
        self.forward()
        self.play(FadeOut(hl_swi))
        self.forward()
        self.play(
            Create(udl1),
            Create(udl2, at=1.5),
        )
        self.forward()
        self.play(GrowArrow(arrow))
        self.forward()
        self.play(FocusOn(code6_block[-1][7][9:16]))
        self.forward()
        self.play(FadeIn(sur1))
        self.forward()
        self.play(FadeIn(sur2))
        self.forward(2)


class Uniform1(SubtitleTemplate2):
    name = 'Uniform'

    def construct(self) -> None:
        super().construct()
        self.title.fix_in_frame()
        self.forward()

        #########################################################

        pipeline = ImageItem('pipeline.png').show()
        arrow = Arrow(UL * 2.2, UL * 1.2, color=YELLOW)
        # arrow2 = Arrow(UR * 2.2 + RIGHT, UR * 1.2 + RIGHT, color=YELLOW)
        # arrow3 = Arrow(DR * 2.2 + RIGHT, DR * 1.2 + RIGHT, color=YELLOW)
        # arrow4 = Arrow(DL * 2.2, DL * 1.2, color=YELLOW)
        # arrows = Group(arrow1, arrow2, arrow3, arrow4)

        #########################################################

        # self.play(
        #     *[
        #         Transform(a, b, path_arc=-40 * DEGREES)
        #         for a, b in it.pairwise(arrows)
        #     ],
        #     lag_ratio=1
        # )
        self.play(FadeIn(pipeline, scale=1.2))
        self.forward()
        self.play(Rotate(arrow, about_point=RIGHT * 0.5, angle=-280 * DEGREES))
        self.forward()

        #########################################################

        def create_g(text: str):
            g = Group(
                Rect(
                    1.2, 0.4,
                    fill_alpha=1,
                    fill_color=GOLD_E,
                    stroke_color=GOLD
                ),
                Text(text)
            )
            g.points.next_to(arrow, DL)
            return g

        g1 = create_g('1.322')
        g2 = create_g('0.721')

        arrow_line = VItem(*arrow.points.get(), stroke_radius=0.04)

        #########################################################

        self.play(FadeIn(g1, DR))
        self.forward()
        self.play(
            *[
                ShowPassingFlash(arrow_line, time_width=0.2, rate_func=linear, duration=0.5)
                for _ in range(5)
            ],
            lag_ratio=0.4
        )
        self.play(FadeIn(g2, DR), FadeOut(g1, DR))
        self.play(
            *[
                ShowPassingFlash(arrow_line, time_width=0.2, rate_func=linear, duration=0.5)
                for _ in range(5)
            ],
            lag_ratio=0.4
        )
        self.forward()

        self.play(FadeOut(Group(g2, arrow, pipeline)))
        self.forward()


code9_src = '''
<fc #569cd6>#version</fc> <fc #b5cea8>330</fc><fc #d4d4d4> core</fc>

<fc #569cd6>uniform</fc> <fc #569cd6>vec4</fc><fc #d4d4d4> ourColor;   </fc><fc #6a9955>// 在 Python 代码中设定这个变量</fc>

<fc #569cd6>out</fc> <fc #569cd6>vec4</fc><fc #d4d4d4> FragColor;</fc>

<fc #569cd6>void</fc><fc #d4d4d4> main()</fc>
<fc #d4d4d4>{</fc>
<fc #d4d4d4>    FragColor = ourColor;</fc>
<fc #d4d4d4>}</fc>
'''

code10_src = '''<fc #9cdcfe>prog</fc><fc #d4d4d4>[</fc><fc #ce9178>'ourColor'</fc><fc #d4d4d4>] = (</fc><fc #b5cea8>0.5</fc><fc #d4d4d4>, </fc><fc #b5cea8>0.0</fc><fc #d4d4d4>, </fc><fc #b5cea8>0.0</fc><fc #d4d4d4>, </fc><fc #b5cea8>1.0</fc><fc #d4d4d4>)</fc>'''

code11_src = '''
<fc #9cdcfe>time_value</fc><fc #d4d4d4> = </fc><fc #4ec9b0>glfw</fc><fc #d4d4d4>.</fc><fc #dcdcaa>get_time</fc><fc #d4d4d4>()</fc>
<fc #9cdcfe>green_value</fc><fc #d4d4d4> = (</fc><fc #4ec9b0>math</fc><fc #d4d4d4>.</fc><fc #dcdcaa>sin</fc><fc #d4d4d4>(</fc><fc #9cdcfe>time_value</fc><fc #d4d4d4>) / </fc><fc #b5cea8>2.0</fc><fc #d4d4d4>) + </fc><fc #b5cea8>0.5</fc>
<fc #9cdcfe>prog</fc><fc #d4d4d4>[</fc><fc #ce9178>'ourColor'</fc><fc #d4d4d4>] = (</fc><fc #b5cea8>0.0</fc><fc #d4d4d4>, </fc><fc #9cdcfe>green_value</fc><fc #d4d4d4>, </fc><fc #b5cea8>0.0</fc><fc #d4d4d4>, </fc><fc #b5cea8>1.0</fc><fc #d4d4d4>)</fc>
'''

code12_src = '''
<fc #6a9955># 导入需要的库</fc>
<fc #c586c0>import</fc> <fc #4ec9b0>math</fc>

<fc #c586c0>import</fc> <fc #4ec9b0>glfw</fc>
<fc #c586c0>import</fc> <fc #4ec9b0>moderngl</fc> <fc #c586c0>as</fc> <fc #4ec9b0>mgl</fc>
<fc #c586c0>import</fc> <fc #4ec9b0>numpy</fc> <fc #c586c0>as</fc> <fc #4ec9b0>np</fc>

<fc #6a9955># 初始化 GLFW</fc>
<fc #c586c0>if</fc> <fc #569cd6>not</fc> <fc #4ec9b0>glfw</fc><fc #d4d4d4>.</fc><fc #dcdcaa>init</fc><fc #d4d4d4>():</fc>
    <fc #c586c0>raise</fc> <fc #4ec9b0>Exception</fc><fc #d4d4d4>(</fc><fc #ce9178>'GLFW出错'</fc><fc #d4d4d4>)</fc>

<fc #6a9955># 创建窗口</fc>
<fc #9cdcfe>window</fc><fc #d4d4d4> = </fc><fc #4ec9b0>glfw</fc><fc #d4d4d4>.</fc><fc #dcdcaa>create_window</fc><fc #d4d4d4>(</fc><fc #b5cea8>800</fc><fc #d4d4d4>, </fc><fc #b5cea8>600</fc><fc #d4d4d4>, </fc><fc #ce9178>'LearnOpenGL'</fc><fc #d4d4d4>, </fc><fc #569cd6>None</fc><fc #d4d4d4>, </fc><fc #569cd6>None</fc><fc #d4d4d4>)</fc>
<fc #c586c0>if</fc> <fc #569cd6>not</fc> <fc #9cdcfe>window</fc><fc #d4d4d4>:</fc>
    <fc #4ec9b0>glfw</fc><fc #d4d4d4>.</fc><fc #dcdcaa>terminate</fc><fc #d4d4d4>()</fc>
    <fc #c586c0>raise</fc> <fc #4ec9b0>Exception</fc><fc #d4d4d4>(</fc><fc #ce9178>'window出错'</fc><fc #d4d4d4>)</fc>

<fc #6a9955># 获得上下文</fc>
<fc #4ec9b0>glfw</fc><fc #d4d4d4>.</fc><fc #dcdcaa>make_context_current</fc><fc #d4d4d4>(</fc><fc #9cdcfe>window</fc><fc #d4d4d4>)</fc>
<fc #9cdcfe>ctx</fc><fc #d4d4d4> = </fc><fc #4ec9b0>mgl</fc><fc #d4d4d4>.</fc><fc #dcdcaa>create_context</fc><fc #d4d4d4>()</fc>

<fc #6a9955># 视口</fc>
<fc #569cd6>def</fc> <fc #dcdcaa>framebuffer_size_callback</fc><fc #d4d4d4>(</fc><fc #9cdcfe>window</fc><fc #d4d4d4>, </fc><fc #9cdcfe>width</fc><fc #d4d4d4>, </fc><fc #9cdcfe>height</fc><fc #d4d4d4>):</fc>
    <fc #9cdcfe>ctx</fc><fc #d4d4d4>.</fc><fc #9cdcfe>viewport</fc><fc #d4d4d4> = (</fc><fc #b5cea8>0</fc><fc #d4d4d4>, </fc><fc #b5cea8>0</fc><fc #d4d4d4>, </fc><fc #9cdcfe>width</fc><fc #d4d4d4>, </fc><fc #9cdcfe>height</fc><fc #d4d4d4>)</fc>

<fc #4ec9b0>glfw</fc><fc #d4d4d4>.</fc><fc #dcdcaa>set_framebuffer_size_callback</fc><fc #d4d4d4>(</fc><fc #9cdcfe>window</fc><fc #d4d4d4>, </fc><fc #dcdcaa>framebuffer_size_callback</fc><fc #d4d4d4>)</fc>

<fc #6a9955># 处理输入</fc>
<fc #569cd6>def</fc> <fc #dcdcaa>process_input</fc><fc #d4d4d4>(</fc><fc #9cdcfe>window</fc><fc #d4d4d4>):</fc>
    <fc #c586c0>if</fc> <fc #4ec9b0>glfw</fc><fc #d4d4d4>.</fc><fc #dcdcaa>get_key</fc><fc #d4d4d4>(</fc><fc #9cdcfe>window</fc><fc #d4d4d4>, </fc><fc #4ec9b0>glfw</fc><fc #d4d4d4>.</fc><fc #9cdcfe>KEY_ESCAPE</fc><fc #d4d4d4>) == </fc><fc #4ec9b0>glfw</fc><fc #d4d4d4>.</fc><fc #9cdcfe>PRESS</fc><fc #d4d4d4>:</fc>
        <fc #4ec9b0>glfw</fc><fc #d4d4d4>.</fc><fc #dcdcaa>set_window_should_close</fc><fc #d4d4d4>(</fc><fc #9cdcfe>window</fc><fc #d4d4d4>, </fc><fc #569cd6>True</fc><fc #d4d4d4>)</fc>

<fc #6a9955># 着色器程序</fc>
<fc #9cdcfe>vertex_shader</fc><fc #d4d4d4> = </fc><fc #ce9178>\'''</fc>
<fc #ce9178>#version 330 core</fc>

<fc #ce9178>in vec3 in_vert;</fc>

<fc #ce9178>void main()</fc>
<fc #ce9178>{</fc>
<fc #ce9178>    gl_Position = vec4(in_vert, 1.0);</fc>
<fc #ce9178>}</fc>
<fc #ce9178>\'''</fc>

<fc #9cdcfe>fragment_shader</fc><fc #d4d4d4> = </fc><fc #ce9178>\'''</fc>
<fc #ce9178>#version 330 core</fc>

<fc #ce9178>uniform vec4 ourColor;   // 在OpenGL程序代码中设定这个变量</fc>

<fc #ce9178>out vec4 FragColor;</fc>

<fc #ce9178>void main()</fc>
<fc #ce9178>{</fc>
<fc #ce9178>    FragColor = ourColor;</fc>
<fc #ce9178>}</fc>
<fc #ce9178>\'''</fc>

<fc #9cdcfe>prog</fc><fc #d4d4d4> = </fc><fc #9cdcfe>ctx</fc><fc #d4d4d4>.</fc><fc #dcdcaa>program</fc><fc #d4d4d4>(</fc><fc #9cdcfe>vertex_shader</fc><fc #d4d4d4>, </fc><fc #9cdcfe>fragment_shader</fc><fc #d4d4d4>)</fc>

<fc #6a9955># 顶点数据</fc>
<fc #9cdcfe>vertices</fc><fc #d4d4d4> = </fc><fc #4ec9b0>np</fc><fc #d4d4d4>.</fc><fc #dcdcaa>array</fc><fc #d4d4d4>([</fc>
<fc #d4d4d4>    -</fc><fc #b5cea8>0.5</fc><fc #d4d4d4>, -</fc><fc #b5cea8>0.5</fc><fc #d4d4d4>, </fc><fc #b5cea8>0.0</fc><fc #d4d4d4>,</fc>
     <fc #b5cea8>0.5</fc><fc #d4d4d4>, -</fc><fc #b5cea8>0.5</fc><fc #d4d4d4>, </fc><fc #b5cea8>0.0</fc><fc #d4d4d4>,</fc>
     <fc #b5cea8>0.0</fc><fc #d4d4d4>,  </fc><fc #b5cea8>0.5</fc><fc #d4d4d4>, </fc><fc #b5cea8>0.0</fc>
<fc #d4d4d4>], </fc><fc #9cdcfe>dtype</fc><fc #d4d4d4>=</fc><fc #ce9178>'f4'</fc><fc #d4d4d4>)</fc>

<fc #9cdcfe>vbo</fc><fc #d4d4d4> = </fc><fc #9cdcfe>ctx</fc><fc #d4d4d4>.</fc><fc #dcdcaa>buffer</fc><fc #d4d4d4>(</fc><fc #9cdcfe>vertices</fc><fc #d4d4d4>.</fc><fc #dcdcaa>tobytes</fc><fc #d4d4d4>())</fc>

<fc #6a9955># 顶点数组对象</fc>
<fc #9cdcfe>vao</fc><fc #d4d4d4> = </fc><fc #9cdcfe>ctx</fc><fc #d4d4d4>.</fc><fc #dcdcaa>vertex_array</fc><fc #d4d4d4>(</fc><fc #9cdcfe>prog</fc><fc #d4d4d4>, </fc><fc #9cdcfe>vbo</fc><fc #d4d4d4>, </fc><fc #ce9178>'in_vert'</fc><fc #d4d4d4>)</fc>

<fc #6a9955># 渲染循环</fc>
<fc #c586c0>while</fc> <fc #569cd6>not</fc> <fc #4ec9b0>glfw</fc><fc #d4d4d4>.</fc><fc #dcdcaa>window_should_close</fc><fc #d4d4d4>(</fc><fc #9cdcfe>window</fc><fc #d4d4d4>):</fc>
    <fc #6a9955># 输入</fc>
    <fc #dcdcaa>process_input</fc><fc #d4d4d4>(</fc><fc #9cdcfe>window</fc><fc #d4d4d4>)</fc>

    <fc #6a9955># 渲染指令</fc>
    <fc #9cdcfe>ctx</fc><fc #d4d4d4>.</fc><fc #dcdcaa>clear</fc><fc #d4d4d4>(</fc><fc #b5cea8>0.2</fc><fc #d4d4d4>, </fc><fc #b5cea8>0.3</fc><fc #d4d4d4>, </fc><fc #b5cea8>0.3</fc><fc #d4d4d4>)</fc>

    <fc #9cdcfe>time_value</fc><fc #d4d4d4> = </fc><fc #4ec9b0>glfw</fc><fc #d4d4d4>.</fc><fc #dcdcaa>get_time</fc><fc #d4d4d4>()</fc>
    <fc #9cdcfe>green_value</fc><fc #d4d4d4> = (</fc><fc #4ec9b0>math</fc><fc #d4d4d4>.</fc><fc #dcdcaa>sin</fc><fc #d4d4d4>(</fc><fc #9cdcfe>time_value</fc><fc #d4d4d4>) / </fc><fc #b5cea8>2.0</fc><fc #d4d4d4>) + </fc><fc #b5cea8>0.5</fc>
    <fc #9cdcfe>prog</fc><fc #d4d4d4>[</fc><fc #ce9178>'ourColor'</fc><fc #d4d4d4>] = (</fc><fc #b5cea8>0.0</fc><fc #d4d4d4>, </fc><fc #9cdcfe>green_value</fc><fc #d4d4d4>, </fc><fc #b5cea8>0.0</fc><fc #d4d4d4>, </fc><fc #b5cea8>1.0</fc><fc #d4d4d4>)</fc>
    <fc #9cdcfe>vao</fc><fc #d4d4d4>.</fc><fc #dcdcaa>render</fc><fc #d4d4d4>(</fc><fc #4ec9b0>mgl</fc><fc #d4d4d4>.</fc><fc #9cdcfe>TRIANGLES</fc><fc #d4d4d4>)</fc>

    <fc #6a9955># 处理事件、交换缓冲</fc>
    <fc #4ec9b0>glfw</fc><fc #d4d4d4>.</fc><fc #dcdcaa>poll_events</fc><fc #d4d4d4>()</fc>
    <fc #4ec9b0>glfw</fc><fc #d4d4d4>.</fc><fc #dcdcaa>swap_buffers</fc><fc #d4d4d4>(</fc><fc #9cdcfe>window</fc><fc #d4d4d4>)</fc>

<fc #6a9955># 终止 GLFW</fc>
<fc #4ec9b0>glfw</fc><fc #d4d4d4>.</fc><fc #dcdcaa>terminate</fc><fc #d4d4d4>()</fc>
'''


class Uniform2(Template):
    def construct(self) -> None:
        title = Title('Uniform').show()

        ########################################################

        uniform_decl1 = Text(
            '<fc #569cd6>uniform</fc> <fc #569cd6>类型</fc><fc #d4d4d4> 名称;</fc>',
            format=Text.Format.RichText
        )
        uniform_decl2 = Text(
            '<fc #569cd6>uniform</fc> <fc #569cd6>vec4</fc><fc #d4d4d4> ourColor;</fc>',
            format=Text.Format.RichText
        )

        code9 = Text(
            code9_src,
            format=Text.Format.RichText,
            font_size=16
        )

        sur_config = dict(
            stroke_radius=0.01,
            fill_alpha=0.2,
            color=YELLOW,
            depth=10
        )
        psur = partial(SurroundingRect, **sur_config)

        uniform_sur = psur(code9[3][:22])

        fragcolor_sur = psur(code9[9])

        ########################################################

        self.forward()
        self.play(Write(uniform_decl1[0][:7]))
        self.forward()
        uniform_decl1.show()
        self.forward()
        self.play(
            TransformInSegments(
                uniform_decl1[0], [(0,7),(8,10),(11,14)],
                uniform_decl2[0], [(0,7),(8,12),(13,22)]
            )
        )
        self.forward()
        # self.show(code9)
        self.play(
            Transform(uniform_decl2[0][:], code9[3][:22]),
            FadeIn(Group(*[
                line[22:]
                if line is code9[3]
                else line

                for line in code9
            ]))
        )
        self.forward()
        self.play(FadeIn(uniform_sur))
        self.forward()
        self.play(Transform(uniform_sur, fragcolor_sur))
        self.forward()
        fadeout = code9[3][22:]
        code9[3].remove(*code9[3][22:])

        ########################################################

        glslsur = partial(
            SurroundingRect,
            color=BLUE,
            buff=0.2
        )
        shift = RIGHT * 5

        fragsur = glslsur(code9)
        fragsur.points.shift(shift)
        fragtxt = Text('片段着色器', color=BLUE, font_size=18)
        fragtxt.points.next_to(fragsur, DOWN, aligned_edge=LEFT, buff=SMALL_BUFF)
        fragg = Group(fragsur, fragtxt)

        pysur = Rect(6, fragsur.points.box.height, color=BLUE)
        pysur.points.shift(LEFT * 2.3)
        pytxt = Text('Python', color=BLUE, font_size=18)
        pytxt.points.next_to(pysur, DOWN, aligned_edge=LEFT, buff=SMALL_BUFF)
        pyg = Group(pysur, pytxt)

        code10 = Text(
            code10_src,
            format=Text.Format.RichText,
            font_size=16
        )
        code11 = Text(
            code11_src,
            format=Text.Format.RichText,
            font_size=14
        )

        Group(code10, code11).points.move_to(pysur)

        sur_config = dict(
            stroke_radius=0.01,
            fill_alpha=0.2,
            color=YELLOW,
            buff=0.05,
            depth=10
        )
        psur = partial(SurroundingRect, **sur_config)

        gettime_sur = psur(code11[1][13:])
        sin_sur = psur(code11[2][14:])
        grv_sur = psur(code11[3][19:])

        code12 = Text(
            code12_src,
            format=Text.Format.RichText,
            font_size=16
        )
        code12.points.shift(UP * 10)

        ########################################################

        self.play(
            FadeOut(fadeout, duration=0.2),
            FadeOut(fragcolor_sur, duration=0.2),
            code9.anim.points.shift(shift),
            FadeIn(fragg, RIGHT * 1.3, at=0.6, duration=0.4, rate_func=rush_from)
        )
        self.forward()
        self.play(
            FadeIn(pyg),
            Write(code10)
        )
        self.forward()
        self.play(
            Transform(code10[:], code11[1:-1])
        )
        self.forward()
        self.play(FadeIn(gettime_sur))
        self.forward()
        self.play(
            Transform(gettime_sur, sin_sur),
            code11[1][:10](VItem).anim.set_stroke_background() \
                .stroke.set(YELLOW_E, 1),
            code11[2][24:34](VItem).anim.set_stroke_background() \
                .stroke.set(YELLOW_E, 1)
        )
        self.forward()
        self.play(
            Transform(sin_sur, grv_sur),
            code11[2][:11](VItem).anim.set_stroke_background() \
                .stroke.set(GREEN_E, 1),
            code11[3][25:36](VItem).anim.set_stroke_background() \
                .stroke.set(GREEN_E, 1)
        )
        self.forward()
        self.play(FadeOut(grv_sur))
        self.forward()
        self.play(
            FadeOut(Group(pysur, pytxt, fragsur, fragtxt, code9, title))
        )
        self.forward()
        self.play(
            FadeTransform(code11[1:-1], code12[80:83]),
            FadeIn(code12[:80]),
            FadeIn(code12[83:])
        )
        self.forward()
        self.play(self.camera.anim.points.shift(UP * 20))
        self.forward()
        self.play(ShowCreationThenFadeAround(code12[2]))
        self.forward()
        self.play(self.camera.anim.points.shift(DOWN * 20))
        self.forward()
        self.play(ShowCreationThenFadeAround(code12[80:83]))
        self.forward()
