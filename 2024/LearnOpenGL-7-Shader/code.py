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
        #########################################################

        video = Video(
            R'2024\LearnOpenGL-5-HelloTriangle\kdenlive\janim_src\Pipeline1.mp4',
            height=Config.get.frame_height - 3
        )
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

        self.forward()

        video.seek(50)
        self.prepare(
            FadeIn(video),
            Write(sur),
            at=0.3
        )
        self.prepare(
            videog.anim.points.scale(2).shift(UR * 2.6),
            at=1.3
        )

        t = self.aas('1.mp3', '在“你好，三角形”这节的教程中提到')
        self.forward_to(t.end + 0.2)

        self.prepare(
            FadeOut(videog, duration=1.5),
            Create(Group(box1, box2)),
            GrowArrow(arrow12),
            Write(arrow12txt),
            at=0.4
        )

        t = self.aas('2.mp3', f'着色器{s1}(Shader){s2}是运行在 GPU 上的小程序',
                     format=Text.Format.RichText)
        self.forward_to(t.end + 0.4)
        t = self.aas('3.mp3', '这些小程序作为图形渲染管线的某个特定部分而运行')
        self.forward_to(t.end + 0.5)
        t = self.aas('4.mp3', '从基本意义上来说')
        self.forward_to(t.end + 0.2)

        self.prepare(
            Write(tip1),
            GrowArrow(arrow1),
            at=0.5
        )
        self.prepare(
            Transform(
                Group(tip1, arrow1),
                Group(tip2, arrow2),
                path_arc=-50 * DEGREES
            ),
            at=1.6
        )

        t = self.aas('5.mp3', '着色器只是一种把输入转化为输出的程序')
        self.forward_to(t.end + 0.6)
        t = self.aas('6.mp3', '着色器也是一种非常独立的程序')
        self.forward_to(t.end + 0.2)

        self.prepare(
            Create(box3),
            GrowArrow(arrow23),
            Write(arrow23txt),
            self.camera.anim.points.shift(RIGHT * 1.5),
            at=0.3
        )

        t = self.aas('7.mp3', '因为它们之间不能相互通信')
        self.forward_to(t.end + 0.4)

        self.prepare(
            FadeTransform(tip2, tip2_, duration=0.6),
            Indicate(box2, at=0.8),
            at=0.8
        )

        t = self.aas('8.mp3', '它们之间唯一的沟通只有通过输入和输出')
        self.forward_to(t.end + 0.6)

        random.seed(114514)
        self.prepare(
            FadeOut(
                Group(box1, box2, box3, arrow12, arrow23, arrow23txt, arrow2, tip2_)
                    .shuffle(),
                lag_ratio=0.5
            ),
            self.camera.anim.points.move_to(arrow12txt),
            duration=3.5,
            at=0.5
        )

        t = self.aas('9.mp3', '前面的教程里我们简要地触及了一点着色器的皮毛')
        self.forward_to(t.end + 0.2)
        t = self.aas('10.mp3', '并了解了如何恰当地使用它们')
        self.forward_to(t.end + 0.4)

        self.prepare(
            FadeIn(circle, scale=0.8),
            at=0.4,
            duration=2
        )

        t = self.aas('11.mp3', '现在我们会用一种更加广泛的形式详细解释着色器')
        self.forward_to(t.end + 0.2)
        t = self.aas('12.mp3', '特别是 OpenGL 着色器语言，也就是 GLSL')
        self.forward_to(t.end + 1)



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

        self.prepare(
            FadeIn(code1_shuffle, lag_ratio=0.1),
            at=0.6,
            duration=3
        )

        t = self.aas('13.mp3', '着色器是使用一种类似C语言')
        self.forward_to(t.end + 0.2)
        t = self.aas('14.mp3', '叫作 GLSL 的语言写成的')
        self.forward_to(t.end + 0.6)
        t = self.aas('15.mp3', 'GLSL 是为图形计算量身定制的')
        self.forward_to(t.end + 0.2)

        t = self.aas('16.mp3', '它包含一些针对向量和矩阵操作的有用特性')
        self.forward_to(t.end + 1)

        self.prepare(
            FadeIn(rect),
            at=0.5
        )

        t = self.aas('17.mp3', '着色器的开头总是要声明版本')
        self.forward_to(t.end + 0.4)

        self.prepare(
            rect.anim.become(psur(code1[3:5])),
            at=0.2,
            duration=0.7
        )
        self.prepare(
            rect.anim.become(psur(code1[6])),
            at=1
        )

        t = self.aas('18.mp3', '接着是输入变量和输出变量')
        self.forward_to(t.end + 0.5)

        self.prepare(
            rect.anim.become(psur(code1[8])),
            at=0.1,
            duration=0.5
        )
        self.prepare(
            rect.anim.become(psur(code1[10:17])),
            at=0.8
        )

        t = self.aas('19.mp3', '以及 uniform 和 main 函数')
        self.forward_to(t.end + 1)
        t = self.aas('20.mp3', '每个着色器的入口点都是 main 函数')
        self.forward_to(t.end + 0.4)

        rect_copy = rect.copy().show()
        rect_copy.fill.set(alpha=0)
        rect_copy.stroke.set(alpha=0.4)
        rect_copy.depth.set(1)
        self.prepare(
            rect.anim.become(psur(code1[12:14])),
            at=0.3
        )

        t = self.aas('21.mp3', '在这个函数中我们处理所有的输入变量')
        self.forward_to(t.end + 0.2)

        self.prepare(
            rect.anim.become(psur(code1[14:16])),
            at=0.2
        )

        t = self.aas('22.mp3', '并将结果输出到输出变量中')
        self.forward_to(t.end + 0.7)

        self.prepare(
            FadeOut(rect_copy),
            FadeOut(rect),
            FadeIn(hl_uniform, at=0.5),
            at=0.3
        )

        t = self.aas('23.mp3', '如果你不知道什么是 uniform 也不用担心')
        self.forward_to(t.end + 0.2)
        t = self.aas('24.mp3', '我们后面会进行讲解')
        self.forward_to(t.end)

        self.play(FadeOut(hl_uniform))

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

        t = self.aas('25.mp3', '和其它编程语言一样')
        self.forward_to(t.end + 0.3)

        self.prepare(
            FadeIn(hl_type),
            at=0.4
        )

        t = self.aas('26.mp3', 'GLSL 有数据类型来指定变量的种类')
        self.forward_to(t.end + 0.5)

        self.prepare(
            Write(brace),
            Write(Group(txt_types[:5], txt_types[12:18], txt_types[24:27], txt_types[29:33], txt_types[38:42])),
            lag_ratio=0.5,
            at=2
        )
        random.seed(1145140)
        self.prepare(
            Write(
                Group(txt_types[5:12], txt_types[18:24], txt_types[27:29], txt_types[33:38], txt_types[42:]).shuffle(),
                lag_ratio=0.02
            ),
            duration=1,
            at=4
        )

        t = self.aas('27.mp3', 'GLSL 中包含 C 等其它语言大部分的基础数据类型：float、double、int、uint 和 bool')
        self.forward_to(t.end)

        self.play(
            self.camera.anim.points.shift(RIGHT * 7),
            FadeOut(code1)
        )
        hl_type.hide()


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

        t = self.aas('28.mp3', 'GLSL 也有两种容器类型')
        self.forward_to(t.end + 0.2)
        t = self.aas('29.mp3', '它们会在这个教程中使用很多')
        self.forward_to(t.end + 0.4)

        self.prepare(
            FadeIn(cov_types),
            Write(st_vector, at=0.4),
            Write(st_matrix, at=0.8)
        )

        t = self.aas('30.mp3', '分别是向量(Vector)和矩阵(Matrix)')
        self.forward_to(t.end + 0.7)

        t = self.aas('31.mp3', '其中矩阵我们会在之后的教程里再讨论')
        self.forward_to(t.end + 0.3)

        self.prepare(
            FadeOut(cov_types),
            FadeOut(st_matrix),
            FadeOut(st_vector[0]),
            Write(txt_basic),
            st_vector[1].anim.points.shift(UP * 2 + RIGHT),
            self.camera.anim.points.shift(UP),
            at=0.8,
            duration=2
        )

        t = self.aas('32.mp3', '现在我们先介绍一下 GLSL 中的向量类型')
        self.forward_to(t.end + 1)

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

        t = self.aas('33.mp3', 'GLSL 中的向量')
        self.forward_to(t.end + 0.1)

        self.prepare(
            *[
                Create(sub)
                for sub in circle_g
            ],
            lag_ratio=0.4,
            at=0.8
        )

        t = self.aas('34.mp3', '是一个可以包含 2、3 或者 4 个分量的容器')
        self.forward_to(t.end + 0.4)

        self.prepare(
            Indicate(type_names, scale_factor=1.1),
            at=1.3
        )

        t = self.aas('35.mp3', '分量的类型可以是前面默认基础类型的任意一个')
        self.forward_to(t.end + 0.6)
        t = self.aas('36.mp3', '比如我们在之前绘制三角形的时候提到的')
        self.forward_to(t.end + 0.3)

        self.prepare(
            Write(vecn[0]),
            Transform(circle_g, vecn[1], at=0.2),
            at=0.4
        )

        t = self.aas('37.mp3', 'vecn 就是包含 n 个 float（浮点数）分量的向量')
        self.forward_to(t.end + 0.4)

        self.prepare(
            ShowCreationThenDestruction(udl_vec2, time_width=3),
            at=0.5
        )

        t = self.aas('38.mp3', '例如 vec2 就是包含 2 个浮点数分量')
        self.forward_to(t.end + 0.2)

        self.prepare(
            ShowCreationThenDestruction(udl_vec3, time_width=3),
            at=0.4
        )

        t = self.aas('39.mp3', 'vec3 就是包含 3 个')
        self.forward_to(t.end + 0.7)

        self.prepare(
            Transform(vecn, dvecn, at=0.6, duration=0.5),
            Transform(dvecn, ivecn, at=1.9, duration=0.5),
            Transform(ivecn, uvecn, at=3.2, duration=0.5),
            Transform(uvecn, bvecn, at=4.2, duration=0.5),
        )

        t = self.aas('40.mp3', '同样的，还有 dvecn、ivecn、uvecn 和 bvecn')
        self.forward_to(t.end)
        t = self.aas('41.mp3', '分别对应不同数据类型的向量')
        self.forward_to(t.end + 0.4)
        t = self.aas('42.mp3', '根据需要使用即可')
        self.forward_to(t.end + 0.7)
        t = self.aas('43.mp3', '但是这些类型的向量中')
        self.forward_to(t.end + 0.2)

        self.prepare(
            AnimGroup(
                FadeOut(bvecn),
                FadeIn(vecn, at=0.5)
            ),
            ShowCreationThenFadeAround(vecn),
            at=0.9,
            lag_ratio=1
        )

        t = self.aas('44.mp3', '我们最常用到的还是包含浮点数类型的 vecn')
        self.forward_to(t.end + 1.4)

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
        self.prepare(
            Write(letters[0]),
            GrowArrow(arrows[0]),
            at=1.3
        )

        t = self.aas('45.mp3', '一个向量的分量可以通过 vec.x 这种方式获取')
        self.forward_to(t.end + 0.7)

        t = self.aas('46.mp3', '这里 x 是指这个向量的第一个分量')
        self.forward_to(t.end + 0.5)

        self.prepare(
            *[
                AnimGroup(Write(letters[i]), GrowArrow(arrows[i]))
                for i in range(1, 4)
            ],
            lag_ratio=0.5,
            at=1.2
        )

        t = self.aas('47.mp3', '你可以分别使用 .x、.y、.z 和 .w')
        self.forward_to(t.end + 0.2)
        t = self.aas('48.mp3', '来获取它的第 1、2、3、4 个分量')
        self.forward_to(t.end + 0.6)

        self.prepare(
            letters(VItem).anim
                .points.next_to(rgba_letters, DOWN, buff=SMALL_BUFF)
                .r.color.set(GREY_D),
            FadeIn(rgba_letters),
            at=1.7
        )

        t = self.aas('49.mp3', 'GLSL 也允许你对颜色使用 rgba')
        self.forward_to(t.end + 0.2)

        self.prepare(
            Group(letters, rgba_letters)(VItem).anim
                .points.next_to(stpq_letters, DOWN, buff=SMALL_BUFF)
                .r.color.set(GREY_D),
            FadeIn(stpq_letters),
            at=1
        )

        t = self.aas('50.mp3', '或是对纹理坐标使用 stpq 访问相同的分量')
        self.forward_to(t.end + 0.6)
        t = self.aas('51.mp3', '无论你使用 xyzw、rgba 还是 stpq 获取分量')
        self.forward_to(t.end + 0.2)
        t = self.aas('52.mp3', '它们在本质上是没有区别的')
        self.forward_to(t.end + 0.3)

        self.prepare(
            Group(letters)(VItem).anim.color.set(WHITE),
            Group(stpq_letters)(VItem).anim.color.set(GREY_D),
            at=0.4
        )

        t = self.aas('53.mp3', '你可以把它们看成是一种别名')
        self.forward_to(t.end + 1)


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

        t = self.aas('54.mp3', '向量这一数据类型也允许一些有趣而灵活的分量选择方式', mul=1.2)
        self.forward_to(t.end + 0.2)

        self.prepare(DrawBorderThenFill(swizzling))

        t = self.aas('55.mp3', '叫做重组(Swizzling)')
        self.forward_to(t.end + 0.6)

        self.prepare(Write(code2), at=0.5)

        t = self.aas('56.mp3', '重组允许这样的语法：')
        self.forward_to(t.end + 1.5)

        self.prepare(
            Create(udls1, lag_ratio=0.6),
            at=1
        )

        t = self.aas('57.mp3', '你可以使用上面 4 个字母任意组合')
        self.forward_to(t.end + 0.2)

        self.prepare(
            *[
                AnimGroup(
                    Transform(udl1, udl2, hide_src=False, duration=0.8),
                    udl1(VItem).anim(duration=0.5).color.fade(0.65)
                )
                for udl1, udl2 in zip(udls1, udls2)
            ],
            lag_ratio=0.6,
            at=0.2
        )

        t = self.aas('58.mp3', '来创建一个同类型的新向量')
        self.forward_to(t.end)

        self.play(
            udls2(VItem).anim.color.fade(0.5)
        )

        self.prepare(
            Write(code3),
            at=0.2
        )

        t = self.aas('59.mp3', '并且也可以把一个向量作为一个参数')
        self.forward_to(t.end + 0.2)
        t = self.aas('60.mp3', '传给不同的向量构造函数，以减少需求参数的数量')
        self.forward_to(t.end + 0.8)
        t = self.aas('61.mp3', '比如说下面这段第二行 result 向量的构造')
        self.forward_to(t.end + 0.8)

        self.prepare(
            Write(udlvect),
            at=0.1
        )

        t = self.aas('62.mp3', 'vect 本身已经是一个 vec2 向量了')
        self.forward_to(t.end + 0.3)

        self.prepare(
            Write(udlvecta),
            at=0.8
        )

        t = self.aas('63.mp3', '所以我们只需要再填入两个分量')
        self.forward_to(t.end + 0.2)

        self.prepare(
            Group(udlvect, udlvecta)(VItem).anim.color.fade(0.65),
            at=1.3
        )

        t = self.aas('64.mp3', '就可以完成 `vec4` 向量的构造')
        self.forward_to(t.end + 0.6)
        t = self.aas('65.mp3', '必要的话你可以暂停来观察一下这几行代码是如何起作用的')
        self.forward_to(t.end)

        self.play(
            rect.anim(rate_func=linear)
            .points.shift(RIGHT * Config.get.frame_width),

            duration=2
        )
        self.play(FadeOut(rect))

        t = self.aas('66.mp3', '向量是一种灵活的数据类型')
        self.forward_to(t.end + 0.3)
        t = self.aas('67.mp3', '我们可以把它用在各种输入和输出上')
        self.forward_to(t.end + 0.6)
        t = self.aas('68.mp3', '在教程中你也可以看到很多新颖的管理向量的例子')
        self.forward_to(t.end + 1)


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

        self.prepare(
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
            lag_ratio=0.3,
            at=0.2
        )

        t = self.aas('69.mp3', '虽然着色器是各自独立的小程序')
        self.forward_to(t.end + 0.2)

        self.prepare(
            Indicate(code4_block[0], scale_factor=1, rate_func=there_and_back_with_pause),
            Indicate(code5_block[0], scale_factor=1, rate_func=there_and_back_with_pause),
            at=0.7
        )

        t = self.aas('70.mp3', '但是它们都是一个整体的一部分')
        self.forward_to(t.end + 0.6)
        t = self.aas('71.mp3', '出于这样的原因')
        self.forward_to(t.end + 0.2)

        self.prepare(
            FadeIn(ras),
            at=0.7
        )

        t = self.aas('72.mp3', '我们希望每个着色器都有输入和输出')
        self.forward_to(t.end + 0.4)
        t = self.aas('73.mp3', '这样才能进行数据交流和传递')
        self.forward_to(t.end + 0.8)

        self.prepare(
            FadeIn(cov),
            Write(inout, at=0.3),
            at=0.3
        )

        t = self.aas('74.mp3', 'GLSL 定义了 in 和 out 关键字专门来实现这个目的')
        self.forward_to(t.end + 0.4)
        t = self.aas('75.mp3', '每个着色器使用这两个关键字设定输入和输出')
        self.forward_to(t.end + 1)

        self.prepare(
            FadeOut(inout),
            FadeOut(cov),
            self.camera.anim(duration=1.5)
                .points.move_to(code4_block).scale(0.7),
            Write(code4_block[-1][3], at=0.5),
            at=0.5
        )

        t = self.aas('76.mp3', '顶点着色器应当接收的是一种特殊形式的输入')
        self.forward_to(t.end + 0.1)
        t = self.aas('77.mp3', '否则就会效率低下')
        self.forward_to(t.end + 0.4)
        t = self.aas('78.mp3', '它的特殊之处在于')
        self.forward_to(t.end + 0.3)

        self.prepare(
            self.camera.anim.points.shift(LEFT),
            DrawBorderThenFill(txt_vertdata),
            GrowArrow(arrow1, at=0.3),
            at=0.2
        )

        t = self.aas('79.mp3', '它从顶点数据中直接接收输入')
        self.forward_to(t.end + 0.2)

        self.prepare(
            FadeIn(ch5g),
            at=1
        )

        t = self.aas('80.mp3', '就像之前我们使用 in_vert 来绑定顶点数据和顶点着色器的输入一样')
        self.forward_to(t.end)

        self.play(
            FadeOut(ch5g)
        )
        self.timeout(1.7, tip_cpp_opengl.show)
        self.prepare(
            Create(vertattr_sur, auto_close_path=False),
            DrawBorderThenFill(vertattr_txt, duration=1, at=0.3, stroke_radius=0.005),
            at=1.2
        )

        t = self.aas('81.mp3', f'顶点着色器的每个输入变量也叫顶点属性{s1}(Vertex Attribute){s2}',
                     format=Text.Format.RichText)
        self.forward_to(t.end + 0.7)
        t = self.aas('82.mp3', '我们能声明的顶点属性是有上限的')
        self.forward_to(t.end + 0.2)
        t = self.aas('83.mp3', '它一般由硬件来决定')
        self.forward_to(t.end + 0.5)
        t = self.aas('84.mp3', 'OpenGL 确保至少有 16 个包含 4 分量的顶点属性可用')
        self.forward_to(t.end + 0.3)
        t = self.aas('85.mp3', '但是有些硬件或许允许更多的顶点属性')
        self.forward_to(t.end + 0.3)
        t = self.aas('86.mp3', '你可以查询 GL_MAX_VERTEX_ATTRIBS 来获取具体的上限')
        self.forward_to(t.end)

        self.play(FadeIn(code8g))

        t = self.aas('87.mp3', '直接运行这一小段代码')
        self.forward_to(t.end + 0.2)
        t = self.aas('88.mp3', '通常情况下它至少会返回 16 个')
        self.forward_to(t.end + 0.3)
        t = self.aas('89.mp3', '大部分情况下够用了')
        self.forward_to(t.end)

        self.play(FadeOut(Group(code8g, tip_cpp_opengl, vertattr_sur, vertattr_txt)))

        self.prepare(
            self.camera.anim.points.shift(RIGHT * 7),
            duration=2,
        )

        t = self.aas('90.mp3', '另一个例外是片段着色器')
        self.forward_to(t.end)

        self.play(Write(code5_block[-1][5]))

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

        self.prepare(
            Write(txt_fragcolor),
            GrowArrow(arrow2, at=0.3),
            at=0.5
        )
        self.prepare(
            Indicate(code5_block[-1][5][9:13]),
            at=2
        )

        t = self.aas('91.mp3', '它需要一个 vec4 颜色输出变量')
        self.forward_to(t.end + 0.4)

        t = self.aas('92.mp3', '因为片段着色器需要生成一个最终输出的颜色', mul=1.2)
        self.forward_to(t.end + 0.7)
        t = self.aas('93.mp3', '嗯，只要这个变量是一个 vec4 类型的就行了')
        self.forward_to(t.end + 0.2)
        t = self.aas('94.mp3', '命名无所谓')
        self.forward_to(t.end + 0.6)
        t = self.aas('95.mp3', '如果你在片段着色器没有定义输出颜色')
        self.forward_to(t.end + 0.2)
        t = self.aas('96.mp3', 'OpenGL 会把你的物体渲染为黑色（或白色）', mul=1.2)
        self.forward_to(t.end + 1)

        t = self.aas('97.mp3', '这两个过程是输入和输出中的例外情况')

        self.prepare(
            self.camera.anim.become(cam_stat).points.scale(1.2),
            duration=t.duration
        )

        self.forward_to(t.end + 0.3)

        self.prepare(
            Indicate(ras[:3], scale_factor=1.03),
            at=1.3
        )

        t = self.aas('98.mp3', '他们是渲染管线从外部获取输入')
        self.forward_to(t.end + 0.4)

        self.prepare(
            Indicate(ras[7:], scale_factor=1.03),
            at=0.8
        )

        t = self.aas('99.mp3', '以及将结果传递出去的过程')
        self.forward_to(t.end + 0.8)

        self.prepare(
            self.camera.anim.become(cam_stat),
            Indicate(ras[3:7], scale_factor=1.03, color=GOLD, duration=2),
            at=1
        )

        t = self.aas('100.mp3', '当我们打算从一个着色器向另一个着色器发送数据时')
        self.forward_to(t.end + 0.4)

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

        self.prepare(
            Write(code4_block[-1][5]),
            at=1.2
        )

        t = self.aas('101.mp3', '我们必须在发送方着色器中声明一个输出')
        self.forward_to(t.end + 0.2)

        self.prepare(
            Write(code5_block[-1][3]),
            at=1.2
        )

        t = self.aas('102.mp3', '在接收方着色器中声明一个类似的输入')
        self.forward_to(t.end + 0.4)

        self.prepare(
            ShowCreationThenDestruction(udl1, at=0.2),
            ShowCreationThenDestruction(udl2, at=0.7)
        )

        t = self.aas('103.mp3', '当类型和名字都一样的时候')
        self.forward_to(t.end + 0.2)

        self.prepare(
            GrowArrow(arrow3),
            at=0.6
        )

        t = self.aas('104.mp3', 'OpenGL 就会把两个变量链接到一起')
        self.forward_to(t.end + 0.3)
        t = self.aas('105.mp3', '它们之间就能发送数据了')
        self.forward_to(t.end + 1)
        t = self.aas('106.mp3', '为了展示这具体是如何工作的')
        self.forward_to(t.end + 0.3)

        self.prepare(
            FadeOut(Group(txt_vertdata, arrow1, txt_fragcolor, arrow2, arrow3)),
            FadeTransform(code4_block, code6_block),
            FadeTransform(code5_block, code7_block),
            at=1.5
        )

        t = self.aas('107.mp3', '我们会稍微改动一下《你好，三角形》那节的着色器')
        self.forward_to(t.end + 0.4)

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

        t = self.aas('108.mp3', '让顶点着色器为片段着色器决定颜色')
        self.forward_to(t.end + 1)

        self.play(FadeIn(hl_swi), at=0.5)

        t = self.aas('109.mp3', '因为前面介绍了“重组语法”')
        self.forward_to(t.end + 0.2)

        self.prepare(
            ShowCreationThenDestruction(
                Underline(code6_block[-1][11][23:30], color=YELLOW)
            ),
            at=1,
            duration=3
        )

        t = self.aas('110.mp3', '所以这里我们把一个 vec3 作为 vec4 构造器的参数')
        self.forward_to(t.end + 0.4)
        t = self.aas('111.mp3', '这样就会比之前更简洁')
        self.forward_to(t.end)

        self.play(FadeOut(hl_swi))
        self.prepare(
            Create(udl1),
            Create(udl2, at=5),
            at=2
        )

        t = self.aas('112.mp3', '你可以看到我们在顶点着色器中声明了一个 v_color 作为 vec4 输出')
        self.forward_to(t.end + 0.5)
        t = self.aas('113.mp3', '并在片段着色器中声明了一个类似的 v_color')
        self.forward_to(t.end + 0.4)
        t = self.aas('114.mp3', '由于它们名字相同且类型相同')
        self.forward_to(t.end + 0.3)

        self.prepare(GrowArrow(arrow), at=0.9)

        t = self.aas('115.mp3', '片段着色器中的`v_color 就和顶点着色器中的 v_color 链接了')
        self.forward_to(t.end + 0.8)

        self.prepare(FocusOn(code6_block[-1][7][9:16]), at=0.4)

        t = self.aas('116.mp3', '这里的命名是随意的')
        self.forward_to(t.end + 0.2)
        t = self.aas('117.mp3', '只是我习惯把“顶点(<c YELLOW>V</c>ertex)着色器传递出去的东西”加上 `v_` 的前缀',
                     format=Text.Format.RichText)
        self.forward_to(t.end + 0.8)

        self.prepare(FadeIn(sur1), at=2)

        t = self.aas('118.mp3', '由于我们在顶点着色器中将颜色设置为暗红色')
        self.forward_to(t.end + 0.2)

        self.prepare(FadeIn(sur2), at=0.7)

        t = self.aas('119.mp3', '最终的片段也是暗红色的')
        self.forward_to(t.end + 2)


class InputAndOutputSubtitle(SubtitlesTemplate2):
    subtitles = [
        ('120.mp3', '所以我们运行程序就会有这样的结果', 0.3, {}),
        ('123.mp3', '这样我们成功地从顶点着色器向片段着色器发送了数据', 0.8, dict(mul=1.2)),
        ('121.mp3', '这一部分的代码放在这个链接里了', 0.2, {}),
        ('122.mp3', '有什么问题的话可以参考', 1, {}),
        ('124.mp3', '让我们更上一层楼', 0.2, {}),
        ('125.mp3', '看看能否从应用程序中直接给片段着色器发送一个颜色！', 2, {}),
    ]


class Uniform1(SubtitleTemplate2):
    name = 'Uniform'

    def construct(self) -> None:
        super().construct()
        self.title.fix_in_frame()

        #########################################################

        pipeline = ImageItem('pipeline.png')
        arrow = Arrow(UL * 2.2, UL * 1.2, color=YELLOW)
        # arrow2 = Arrow(UR * 2.2 + RIGHT, UR * 1.2 + RIGHT, color=YELLOW)
        # arrow3 = Arrow(DR * 2.2 + RIGHT, DR * 1.2 + RIGHT, color=YELLOW)
        # arrow4 = Arrow(DL * 2.2, DL * 1.2, color=YELLOW)
        # arrows = Group(arrow1, arrow2, arrow3, arrow4)

        #########################################################

        t = self.aas('126.mp3', 'Uniform 是另一种从我们的应用程序')
        self.forward_to(t.end)
        t = self.aas('127.mp3', '在 CPU 上传递数据到 GPU 上的着色器的方式')
        self.forward_to(t.end + 0.3)
        t = self.aas('128.mp3', '但 uniform 和顶点数据有些不同')
        self.forward_to(t.end + 0.6)

        self.prepare(FadeIn(pipeline, scale=1.2), at=0.5, duration=2)

        t = self.aas('129.mp3', '首先，uniform 是全局的')
        self.forward_to(t.end + 0.3)

        self.prepare(
            Rotate(arrow, about_point=RIGHT * 0.5, angle=-280 * DEGREES),
            duration=3
        )

        t = self.aas('130.mp3', '它可以被着色器程序的任意着色器阶段访问')
        self.forward_to(t.end + 0.6)

        # self.play(
        #     *[
        #         Transform(a, b, path_arc=-40 * DEGREES)
        #         for a, b in it.pairwise(arrows)
        #     ],
        #     lag_ratio=1
        # )

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

        self.prepare(FadeIn(g1, DR), at=0.6)

        t = self.aas('131.mp3', '其次，无论你把 uniform 值设置成什么')
        self.forward_to(t.end)

        self.prepare(
            *[
                ShowPassingFlash(arrow_line, time_width=0.2, rate_func=linear, duration=0.5)
                for _ in range(5)
            ],
            lag_ratio=0.4,
            at=0.5
        )

        t = self.aas('132.mp3', 'uniform 会一直保存他们的数据')
        self.forward_to(t.end)

        self.prepare(FadeIn(g2, DR), FadeOut(g1, DR), at=0.4)

        t = self.aas('133.mp3', '直到它们被重置或更新')
        self.forward_to(t.end)

        self.play(
            *[
                ShowPassingFlash(arrow_line, time_width=0.2, rate_func=linear, duration=0.5)
                for _ in range(5)
            ],
            lag_ratio=0.4
        )
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

        tip = Text(
            '如果你声明了一个 uniform 却在 GLSL 代码中没用过，编译器会静默移除这个变量，导致最后编译出的版本中并不会包含它，\n'
            '这可能导致几个非常麻烦的错误，记住这点！',
            font_size=12,
            color=GREY
        )
        tip.points.next_to(title, DOWN, aligned_edge=LEFT)

        ########################################################

        t = self.aas('134.mp3', '要在 GLSL 中声明 uniform')
        self.forward_to(t.end + 0.3)

        self.prepare(Write(uniform_decl1[0][:7]), at=1.5)

        t = self.aas('135.mp3', '我们只需在着色器中使用 `uniform` 关键字')
        self.forward_to(t.end)

        self.timeout(0.5, uniform_decl1.show)

        t = self.aas('136.mp3', '并带上类型和名称')
        self.forward_to(t.end)

        self.play(
            TransformInSegments(
                uniform_decl1[0], [(0,7),(8,10),(11,14)],
                uniform_decl2[0], [(0,7),(8,12),(13,22)]
            )
        )

        t = self.aas('137.mp3', '这样我们就可以在着色器中使用新声明的 uniform')
        self.forward_to(t.end + 0.4)

        t = self.aas('138.mp3', '我们这次来试着通过 uniform 设置三角形的颜色')

        self.prepare(
            Transform(uniform_decl2[0][:], code9[3][:22]),
            FadeIn(Group(*[
                line[22:]
                if line is code9[3]
                else line

                for line in code9
            ])),
            duration=t.duration
        )

        self.forward_to(t.end + 0.6)

        self.prepare(FadeIn(uniform_sur), at=1)

        t = self.aas('139.mp3', '我们在片段着色器中声明了一个 uniform vec4 的 ourColor')
        self.forward_to(t.end + 0.1)

        self.show(tip)
        self.prepare(Transform(uniform_sur, fragcolor_sur), at=0.4)

        t = self.aas('140.mp3', '并把片段着色器的输出颜色设置为 uniform 值的内容')
        self.forward_to(t.end)
        self.play(FadeOut(fragcolor_sur), FadeOut(tip))

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

        t = self.aas('141.mp3', '因为 uniform 是全局变量')
        self.forward_to(t.end + 0.4)
        t = self.aas('142.mp3', '我们可以在任何着色器中定义它们')
        self.forward_to(t.end + 0.2)
        t = self.aas('143.mp3', '而无需通过顶点着色器作为中介传递过来')
        self.forward_to(t.end + 0.6)
        t = self.aas('144.mp3', '由于这里我们的顶点着色器用不到这个 uniform')
        self.forward_to(t.end + 0.2)
        t = self.aas('145.mp3', '所以我们不在那里定义它')
        self.forward_to(t.end + 0.3)
        t = self.aas('146.mp3', '只在片段着色器这里定义')
        self.forward_to(t.end)

        self.play(
            FadeOut(fadeout, duration=0.2),
            code9.anim.points.shift(shift),
            FadeIn(fragg, RIGHT * 1.3, at=0.6, duration=0.4, rate_func=rush_from)
        )

        t = self.aas('147.mp3', '这个 uniform 现在还是空的')
        self.forward_to(t.end + 0.3)
        t = self.aas('148.mp3', '我们还没有给他添加任何数据')
        self.forward_to(t.end + 0.6)

        self.prepare(
            FadeIn(pyg),
            Write(code10),
            at=0.5
        )

        t = self.aas('149.mp3', '我们在 Python 代码中这样就可以设置着色器程序的 uniform 值了')
        self.forward_to(t.end + 0.2)

        t = self.aas('150.mp3', '这和前面一样，会显示一个暗红色的三角形')
        self.forward_to(t.end + 0.6)
        t = self.aas('151.mp3', '为了让它有趣一点')
        self.forward_to(t.end + 0.2)

        self.prepare(
            Transform(code10[:], code11[1:-1]),
            duration=2
        )

        t = self.aas('152.mp3', '现在我们让它随着时间改变颜色')
        self.forward_to(t.end + 0.8)

        self.prepare(FadeIn(gettime_sur), duration=2)

        t = self.aas('153.mp3', '我们通过 glfw.get_time() 获取运行的秒数')
        self.forward_to(t.end + 0.3)

        self.prepare(
            Transform(gettime_sur, sin_sur),
            code11[1][:10](VItem).anim.set_stroke_background()
                .stroke.set(YELLOW_E, 1)
                .r.radius.set(0.01),
            code11[2][24:34](VItem).anim.set_stroke_background()
                .stroke.set(YELLOW_E, 1)
                .r.radius.set(0.01),
            duration=2
        )

        t = self.aas('154.mp3', '然后我们使用 `sin` 函数让绿色在 0.0 到 1.0 之间改变')
        self.forward_to(t.end + 0.3)

        self.prepare(
            Transform(sin_sur, grv_sur),
            code11[2][:11](VItem).anim.set_stroke_background()
                .stroke.set(GREEN_E, 1)
                .r.radius.set(0.01),
            code11[3][25:36](VItem).anim.set_stroke_background()
                .stroke.set(GREEN_E, 1)
                .r.radius.set(0.01),
            duration=2
        )

        t = self.aas('155.mp3', '并且将其传递给叫作 `ourColor` 的 uniform')
        self.forward_to(t.end)

        self.play(FadeOut(grv_sur))

        t = self.aas('156.mp3', '我们把这段放进渲染循环中')

        self.prepare(
            FadeOut(Group(pysur, pytxt, fragsur, fragtxt, code9, title)),
            AnimGroup(
                FadeTransform(code11[1:-1], code12[80:83]),
                FadeIn(code12[:80]),
                FadeIn(code12[83:]),
                duration=t.duration
            )
        )

        self.forward_to(t.end)
        t = self.aas('157.mp3', '就可以在每一次迭代中更新这个 uniform')
        self.forward_to(t.end + 0.3)
        t = self.aas('158.mp3', '这样就会使得这个三角形动态地改变颜色')
        self.forward_to(t.end + 0.7)

        t = self.aas('159.mp3', '这里使用了 math.sin')

        self.prepare(
            self.camera.anim.points.shift(UP * 20),
            duration=t.duration
        )

        self.forward_to(t.end + 0.3)

        self.prepare(
            ShowCreationThenFadeAround(code12[2]),
            at=0.7,
            duration=2
        )

        t = self.aas('160.mp3', '记得在文件开头导入一下 math 库')
        self.forward_to(t.end + 0.4)
        t = self.aas('161.mp3', '这是自带的，不用另外安装')
        self.forward_to(t.end)

        self.play(self.camera.anim.points.shift(DOWN * 20))

        self.prepare(
            ShowCreationThenFadeAround(code12[80:83]),
            at=0.3
        )

        t = self.aas('162.mp3', '在绘制三角形前更新 uniform 的值')
        self.forward_to(t.end + 2)


class Uniform2Subtitle(SubtitlesTemplate):
    subtitles = [
        ('163.mp3', '如果你正确更新了'),
        ('164.mp3', '你会看到你的三角形逐渐由绿变黑再变回绿色'),
        ('165.mp3', '如果你在哪遇到了问题'),
        ('166.mp3', '可以参考一下这节的源码'),
    ]

