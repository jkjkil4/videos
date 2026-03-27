# flake8: noqa
import sys

sys.path.append('.')

from janim.imports import *

with reloads():
    from template import *
from template import *


code1_src = R'''
<fc #c586c0>from</fc> <fc #4ec9b0>pyglm</fc> <fc #c586c0>import</fc> <fc #4ec9b0>glm</fc>

<fc #9cdcfe>vec</fc> <fc #d4d4d4>=</fc> <fc #4ec9b0>glm</fc><fc #cccccc>.</fc><fc #4ec9b0>vec4</fc><fc #cccccc>(</fc><fc #b5cea8>1</fc><fc #cccccc>, </fc><fc #b5cea8>0</fc><fc #cccccc>, </fc><fc #b5cea8>0</fc><fc #cccccc>, </fc><fc #b5cea8>1</fc><fc #cccccc>)</fc>

<fc #9cdcfe>trans</fc> <fc #d4d4d4>=</fc> <fc #4ec9b0>glm</fc><fc #cccccc>.</fc><fc #9cdcfe>mat4</fc><fc #cccccc>(</fc><fc #b5cea8>1</fc><fc #cccccc>)</fc>
<fc #9cdcfe>trans</fc> <fc #d4d4d4>=</fc> <fc #4ec9b0>glm</fc><fc #cccccc>.</fc><fc #dcdcaa>translate</fc><fc #cccccc>(</fc><fc #9cdcfe>trans</fc><fc #cccccc>, </fc><fc #4ec9b0>glm</fc><fc #cccccc>.</fc><fc #4ec9b0>vec3</fc><fc #cccccc>(</fc><fc #b5cea8>1</fc><fc #cccccc>, </fc><fc #b5cea8>1</fc><fc #cccccc>, </fc><fc #b5cea8>0</fc><fc #cccccc>))</fc>

<fc #9cdcfe>vec</fc> <fc #d4d4d4>=</fc> <fc #9cdcfe>trans</fc> <fc #dcdcaa>*</fc> <fc #9cdcfe>vec</fc>
<fc #dcdcaa>print</fc><fc #cccccc>(</fc><fc #9cdcfe>vec</fc><fc #cccccc>)</fc>
'''


def get_transplane():
    plane = NumberPlane(faded_line_ratio=0, background_line_style={'alpha': 0.7})
    dot1 = Dot([1, 0, 0])
    dot2 = Dot([2, 1, 0])
    arrow = Arrow(dot1, dot2, color=YELLOW)
    return Group(plane, dot1, dot2, arrow)


class SharpDelimTemplate(Template):
    CONFIG = Config(
        typst_shared_preamble=Template.CONFIG.typst_shared_preamble + t_(
            R'''
            #set math.mat(delim: "[")

            #import "@janim/colors:0.0.0": *
            '''
        )
    )


class TL1(SharpDelimTemplate):
    def construct(self):
        ####################################################

        img = ImageItem('glm.png', height=1.5)

        glmins = Text('pip install pyglm')

        ####################################################

        self.play(FadeIn(img))
        self.forward()
        self.hide(img)
        self.play(Write(glmins))
        self.play(FadeOut(glmins))

        ####################################################

        code1 = Text(code1_src, format='rich')
        transplane = get_transplane()

        r1 = SweepRect(code1[3])
        r2 = SweepRect(code1[5, 6])
        r3 = SweepRect(code1[8, 9])

        ####################################################

        self.play(Write(code1[1]))
        self.play(
            FadeOut(code1[1]),
            FadeIn(transplane)
        )
        self.forward()
        self.play(
            FadeIn(code1[1]),
            FadeOut(transplane)
        )

        self.play(
            FadeIn(code1[2:])
        )
        self.play(
            r1.anim_in(),
            r2.anim_in(),
            r3.anim_in(),
            lag_ratio=1
        )

        ####################################################

        r4 = SweepRect(code1[3][6:14])

        ud1 = Underline(code1[3][15, 18, 21], color=YELLOW)
        ud2 = Underline(code1[3][24], color=YELLOW)

        typ1 = TypstMath('#[`vec`] = vec(1,0,0,1)', scale=0.5)
        typ1.points.shift([0.97, 1, 0.0])

        r5 = SweepRect(code1[5][8:16])

        typ2 = TypstMath('#[`trans`] = mat(1,0,0,0;0,1,0,0;0,0,1,0;0,0,0,1)', scale=0.5)
        typ2.points.shift([-0.2, 0.12, 0.0])

        typ3 = TypstMath('#[`trans`] = mat(1,0,0,0;0,1,0,0;0,0,1,0;0,0,0,1) mat(1,0,0,1;0,1,0,1;0,0,1,0;0,0,0,1)', scale=0.5)
        typ3.points.shift([1.92, -1.1, 0.0])
        typ4 = TypstMath('#[`trans`] = mat(1,0,0,1;0,1,0,1;0,0,1,0;0,0,0,1)')
        typ4.match_pattern(typ3, '#[`trans`]')

        for t in (typ3, typ4):
            t['mat(1,0,0,1;0,1,0,1;0,0,1,0;0,0,0,1)'].set(color=BLUE)

        r6 = SweepRect(code1[6][38, 41, 44], color=BLUE_A)
        r7 = SweepRect(typ3[55:58], color=BLUE_A)
        r8 = SweepRect(code1[6][8:21])

        typ5 = TypstMath('#[`vec`] = mat(1,0,0,1;0,1,0,1;0,0,1,0;0,0,0,1) vec(1,0,0,1)', scale=0.6)
        typ5['mat(1,0,0,1;0,1,0,1;0,0,1,0;0,0,0,1)'].set(color=BLUE)
        typ5.points.shift([-0.19, -1.36, -0.0])

        typ6 = TypstMath('#[`vec`] = vec(2,1,0,1)')
        typ6.match_pattern(typ5, '#[`vec`]')

        result = Group(
            tmp := ImageItem('QQ20260318-190146.png', height=3.5),
            SurroundingRect(tmp, buff=0)
        )

        hl = HighlightRect(Rect([-3.89, -1.7, 0], [3.71, -1.38, 0]), buff=0, fill_alpha=0.75)
        dark = FrameRect(fill_alpha=1, color=BLACK)

        ####################################################

        self.play(
            FadeOut(Group(r1, r2, r3)),
            r4.anim_in()
        )
        self.play(
            Create(ud1)
        )
        self.play(
            Create(ud2, duration=0.3),
            Indicate(code1[3][24])
        )
        self.play(
            FadeIn(typ1),
            FadeOut(Group(ud1, ud2))
        )
        self.play(
            r5.anim_in()
        )
        self.play(
            FadeIn(typ2)
        )
        self.play(
            TransformMatchingDiff(typ2, typ3),
            r8.anim_in()
        )
        self.play(
            SweepRect.ins(r6, r7)
        )
        self.play(
            SweepRect.outs(r6, r7, duration=0.6),
            TransformMatchingDiff(typ3, typ4),
        )
        self.play(
            Transform(typ1[:4], typ5[:4]),
            TransformMatchingDiff(Group(typ4, typ1[4:]), typ5[4:], duration=1),
        )
        self.play(
            Transform(typ5[:4], typ6[:4]),
            FadeTransform(typ5[4:], typ6[4:]),
        )
        self.play(
            FadeIn(result)
        )
        self.play(
            FadeIn(hl)
        )
        self.forward()
        self.play(
            FadeIn(dark)
        )

        self.forward()


def SmileCon(width=3, height=2.5, **kwargs):
    return Group(
        ImageItem('container.jpg', width=width, height=height),
        ImageItem('awesomeface_b.png', width=width, height=height, alpha=0.2),
        **kwargs
    )


code2_src = R'''
<fc #9cdcfe>trans</fc> <fc #d4d4d4>=</fc> <fc #4ec9b0>glm</fc><fc #cccccc>.</fc><fc #9cdcfe>mat4</fc><fc #cccccc>(</fc><fc #b5cea8>1</fc><fc #cccccc>)</fc>
<fc #9cdcfe>trans</fc> <fc #d4d4d4>=</fc> <fc #4ec9b0>glm</fc><fc #cccccc>.</fc><fc #dcdcaa>rotate</fc><fc #cccccc>(</fc><fc #9cdcfe>trans</fc><fc #cccccc>, </fc><fc #4ec9b0>glm</fc><fc #cccccc>.</fc><fc #dcdcaa>radians</fc><fc #cccccc>(</fc><fc #b5cea8>90</fc><fc #cccccc>), </fc><fc #4ec9b0>glm</fc><fc #cccccc>.</fc><fc #4ec9b0>vec3</fc><fc #cccccc>(</fc><fc #b5cea8>0</fc><fc #cccccc>, </fc><fc #b5cea8>0</fc><fc #cccccc>, </fc><fc #b5cea8>1</fc><fc #cccccc>))</fc>
<fc #9cdcfe>trans</fc> <fc #d4d4d4>=</fc> <fc #4ec9b0>glm</fc><fc #cccccc>.</fc><fc #dcdcaa>scale</fc><fc #cccccc>(</fc><fc #9cdcfe>trans</fc><fc #cccccc>, </fc><fc #4ec9b0>glm</fc><fc #cccccc>.</fc><fc #4ec9b0>vec3</fc><fc #cccccc>(</fc><fc #b5cea8>0.5</fc><fc #cccccc>, </fc><fc #b5cea8>0.5</fc><fc #cccccc>, </fc><fc #b5cea8>0.5</fc><fc #cccccc>))</fc>
'''

code3_src = R"""
<fc #6a9955># 导入需要的库</fc>
<fc #c586c0>import</fc> <fc #4ec9b0>glfw</fc>
<fc #c586c0>import</fc> <fc #4ec9b0>moderngl</fc> <fc #c586c0>as</fc> <fc #4ec9b0>mgl</fc>
<fc #c586c0>import</fc> <fc #4ec9b0>numpy</fc> <fc #c586c0>as</fc> <fc #4ec9b0>np</fc>
<fc #c586c0>from</fc> <fc #4ec9b0>PIL</fc> <fc #c586c0>import</fc> <fc #4ec9b0>Image</fc>
<fc #c586c0>from</fc> <fc #4ec9b0>pyglm</fc> <fc #c586c0>import</fc> <fc #4ec9b0>glm</fc>

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
<fc #9cdcfe>vertex_shader</fc> <fc #d4d4d4>=</fc> <fc #ce9178>'''</fc>
<fc #ce9178>#version 330 core</fc>

<fc #ce9178>in vec3 in_vert;</fc>
<fc #ce9178>in vec2 in_texcoord;</fc>

<fc #ce9178>out vec2 v_texcoord;</fc>

<fc #ce9178>uniform mat4 transform;</fc>

<fc #ce9178>void main()</fc>
<fc #ce9178>{</fc>
<fc #ce9178>    gl_Position = transform * vec4(in_vert, 1.0);</fc>
<fc #ce9178>    v_texcoord = in_texcoord;</fc>
<fc #ce9178>}</fc>
<fc #ce9178>'''</fc>

<fc #9cdcfe>fragment_shader</fc> <fc #d4d4d4>=</fc> <fc #ce9178>'''</fc>
<fc #ce9178>#version 330 core</fc>

<fc #ce9178>in vec2 v_texcoord;</fc>

<fc #ce9178>uniform sampler2D texture1;</fc>
<fc #ce9178>uniform sampler2D texture2;</fc>

<fc #ce9178>out vec4 FragColor;</fc>

<fc #ce9178>void main()</fc>
<fc #ce9178>{</fc>
<fc #ce9178>    FragColor = mix(texture(texture1, v_texcoord), texture(texture2, v_texcoord), 0.2);</fc>
<fc #ce9178>}</fc>
<fc #ce9178>'''</fc>

<fc #9cdcfe>prog</fc> <fc #d4d4d4>=</fc> <fc #9cdcfe>ctx</fc><fc #cccccc>.</fc><fc #dcdcaa>program</fc><fc #cccccc>(</fc><fc #9cdcfe>vertex_shader</fc><fc #cccccc>, </fc><fc #9cdcfe>fragment_shader</fc><fc #cccccc>)</fc>

<fc #6a9955># 顶点数据</fc>
<fc #9cdcfe>vertices</fc> <fc #d4d4d4>=</fc> <fc #4ec9b0>np</fc><fc #cccccc>.</fc><fc #dcdcaa>array</fc><fc #cccccc>([</fc>
<fc #6a9955>#   ----- 位置 -----   - 纹理坐标 -</fc>
     <fc #b5cea8>0.5</fc><fc #cccccc>,  </fc><fc #b5cea8>0.5</fc><fc #cccccc>, </fc><fc #b5cea8>0.0</fc><fc #cccccc>,  </fc><fc #b5cea8>1.0</fc><fc #cccccc>, </fc><fc #b5cea8>1.0</fc><fc #cccccc>,   </fc><fc #6a9955># 右上</fc>
     <fc #b5cea8>0.5</fc><fc #cccccc>, </fc><fc #d4d4d4>-</fc><fc #b5cea8>0.5</fc><fc #cccccc>, </fc><fc #b5cea8>0.0</fc><fc #cccccc>,  </fc><fc #b5cea8>1.0</fc><fc #cccccc>, </fc><fc #b5cea8>0.0</fc><fc #cccccc>,   </fc><fc #6a9955># 右下</fc>
    <fc #d4d4d4>-</fc><fc #b5cea8>0.5</fc><fc #cccccc>, </fc><fc #d4d4d4>-</fc><fc #b5cea8>0.5</fc><fc #cccccc>, </fc><fc #b5cea8>0.0</fc><fc #cccccc>,  </fc><fc #b5cea8>0.0</fc><fc #cccccc>, </fc><fc #b5cea8>0.0</fc><fc #cccccc>,   </fc><fc #6a9955># 左下</fc>
    <fc #d4d4d4>-</fc><fc #b5cea8>0.5</fc><fc #cccccc>,  </fc><fc #b5cea8>0.5</fc><fc #cccccc>, </fc><fc #b5cea8>0.0</fc><fc #cccccc>,  </fc><fc #b5cea8>0.0</fc><fc #cccccc>, </fc><fc #b5cea8>1.0</fc>    <fc #6a9955># 左上</fc>
<fc #cccccc>], </fc><fc #9cdcfe>dtype</fc><fc #d4d4d4>=</fc><fc #ce9178>'f4'</fc><fc #cccccc>)</fc>

<fc #9cdcfe>vbo</fc> <fc #d4d4d4>=</fc> <fc #9cdcfe>ctx</fc><fc #cccccc>.</fc><fc #dcdcaa>buffer</fc><fc #cccccc>(</fc><fc #9cdcfe>vertices</fc><fc #cccccc>.</fc><fc #dcdcaa>tobytes</fc><fc #cccccc>())</fc>

<fc #9cdcfe>indices</fc> <fc #d4d4d4>=</fc> <fc #4ec9b0>np</fc><fc #cccccc>.</fc><fc #dcdcaa>array</fc><fc #cccccc>([</fc>
    <fc #b5cea8>0</fc><fc #cccccc>, </fc><fc #b5cea8>1</fc><fc #cccccc>, </fc><fc #b5cea8>3</fc><fc #cccccc>,    </fc><fc #6a9955># 第一个三角形</fc>
    <fc #b5cea8>1</fc><fc #cccccc>, </fc><fc #b5cea8>2</fc><fc #cccccc>, </fc><fc #b5cea8>3</fc>     <fc #6a9955># 第二个三角形</fc>
<fc #cccccc>], </fc><fc #9cdcfe>dtype</fc><fc #d4d4d4>=</fc><fc #ce9178>'i4'</fc><fc #cccccc>)</fc>

<fc #9cdcfe>ibo</fc> <fc #d4d4d4>=</fc> <fc #9cdcfe>ctx</fc><fc #cccccc>.</fc><fc #dcdcaa>buffer</fc><fc #cccccc>(</fc><fc #9cdcfe>indices</fc><fc #cccccc>.</fc><fc #dcdcaa>tobytes</fc><fc #cccccc>())</fc>

<fc #6a9955># 顶点数组对象</fc>
<fc #9cdcfe>vao</fc> <fc #d4d4d4>=</fc> <fc #9cdcfe>ctx</fc><fc #cccccc>.</fc><fc #dcdcaa>vertex_array</fc><fc #cccccc>(</fc><fc #9cdcfe>prog</fc><fc #cccccc>, </fc><fc #9cdcfe>vbo</fc><fc #cccccc>, </fc><fc #ce9178>'in_vert'</fc><fc #cccccc>, </fc><fc #ce9178>'in_texcoord'</fc><fc #cccccc>, </fc><fc #9cdcfe>index_buffer</fc><fc #d4d4d4>=</fc><fc #9cdcfe>ibo</fc><fc #cccccc>)</fc>

<fc #6a9955># 纹理</fc>
<fc #9cdcfe>img</fc> <fc #d4d4d4>=</fc> <fc #4ec9b0>Image</fc><fc #cccccc>.</fc><fc #dcdcaa>open</fc><fc #cccccc>(</fc><fc #ce9178>'container.jpg'</fc><fc #cccccc>).</fc><fc #dcdcaa>transpose</fc><fc #cccccc>(</fc><fc #4ec9b0>Image</fc><fc #cccccc>.FLIP_TOP_BOTTOM)</fc>
<fc #9cdcfe>texture1</fc> <fc #d4d4d4>=</fc> <fc #9cdcfe>ctx</fc><fc #cccccc>.</fc><fc #dcdcaa>texture</fc><fc #cccccc>(</fc><fc #9cdcfe>img</fc><fc #cccccc>.</fc><fc #9cdcfe>size</fc><fc #cccccc>, </fc><fc #9cdcfe>components</fc><fc #d4d4d4>=</fc><fc #b5cea8>3</fc><fc #cccccc>, </fc><fc #9cdcfe>data</fc><fc #d4d4d4>=</fc><fc #9cdcfe>img</fc><fc #cccccc>.</fc><fc #dcdcaa>tobytes</fc><fc #cccccc>())</fc>
<fc #9cdcfe>img</fc> <fc #d4d4d4>=</fc> <fc #4ec9b0>Image</fc><fc #cccccc>.</fc><fc #dcdcaa>open</fc><fc #cccccc>(</fc><fc #ce9178>'awesomeface.png'</fc><fc #cccccc>).</fc><fc #dcdcaa>transpose</fc><fc #cccccc>(</fc><fc #4ec9b0>Image</fc><fc #cccccc>.FLIP_TOP_BOTTOM)</fc>
<fc #9cdcfe>texture2</fc> <fc #d4d4d4>=</fc> <fc #9cdcfe>ctx</fc><fc #cccccc>.</fc><fc #dcdcaa>texture</fc><fc #cccccc>(</fc><fc #9cdcfe>img</fc><fc #cccccc>.</fc><fc #9cdcfe>size</fc><fc #cccccc>, </fc><fc #9cdcfe>components</fc><fc #d4d4d4>=</fc><fc #b5cea8>4</fc><fc #cccccc>, </fc><fc #9cdcfe>data</fc><fc #d4d4d4>=</fc><fc #9cdcfe>img</fc><fc #cccccc>.</fc><fc #dcdcaa>tobytes</fc><fc #cccccc>())</fc>

<fc #6a9955># 绑定纹理</fc>
<fc #9cdcfe>prog</fc><fc #cccccc>[</fc><fc #ce9178>'texture1'</fc><fc #cccccc>] </fc><fc #d4d4d4>=</fc> <fc #b5cea8>0</fc>
<fc #9cdcfe>prog</fc><fc #cccccc>[</fc><fc #ce9178>'texture2'</fc><fc #cccccc>] </fc><fc #d4d4d4>=</fc> <fc #b5cea8>1</fc>
<fc #9cdcfe>texture1</fc><fc #cccccc>.</fc><fc #dcdcaa>use</fc><fc #cccccc>(</fc><fc #b5cea8>0</fc><fc #cccccc>)</fc>
<fc #9cdcfe>texture2</fc><fc #cccccc>.</fc><fc #dcdcaa>use</fc><fc #cccccc>(</fc><fc #b5cea8>1</fc><fc #cccccc>)</fc>

<fc #6a9955># 矩阵</fc>
<fc #9cdcfe>trans</fc> <fc #d4d4d4>=</fc> <fc #4ec9b0>glm</fc><fc #cccccc>.</fc><fc #9cdcfe>mat4</fc><fc #cccccc>(</fc><fc #b5cea8>1</fc><fc #cccccc>)</fc>
<fc #9cdcfe>trans</fc> <fc #d4d4d4>=</fc> <fc #4ec9b0>glm</fc><fc #cccccc>.</fc><fc #dcdcaa>rotate</fc><fc #cccccc>(</fc><fc #9cdcfe>trans</fc><fc #cccccc>, </fc><fc #4ec9b0>glm</fc><fc #cccccc>.</fc><fc #dcdcaa>radians</fc><fc #cccccc>(</fc><fc #b5cea8>90</fc><fc #cccccc>), </fc><fc #4ec9b0>glm</fc><fc #cccccc>.</fc><fc #4ec9b0>vec3</fc><fc #cccccc>(</fc><fc #b5cea8>0</fc><fc #cccccc>, </fc><fc #b5cea8>0</fc><fc #cccccc>, </fc><fc #b5cea8>1</fc><fc #cccccc>))</fc>
<fc #9cdcfe>trans</fc> <fc #d4d4d4>=</fc> <fc #4ec9b0>glm</fc><fc #cccccc>.</fc><fc #dcdcaa>scale</fc><fc #cccccc>(</fc><fc #9cdcfe>trans</fc><fc #cccccc>, </fc><fc #4ec9b0>glm</fc><fc #cccccc>.</fc><fc #4ec9b0>vec3</fc><fc #cccccc>(</fc><fc #b5cea8>0.5</fc><fc #cccccc>, </fc><fc #b5cea8>0.5</fc><fc #cccccc>, </fc><fc #b5cea8>0.5</fc><fc #cccccc>))</fc>

<fc #9cdcfe>prog</fc><fc #cccccc>[</fc><fc #ce9178>'transform'</fc><fc #cccccc>].</fc><fc #dcdcaa>write</fc><fc #cccccc>(</fc><fc #9cdcfe>trans</fc><fc #cccccc>.</fc><fc #dcdcaa>to_bytes</fc><fc #cccccc>())</fc>

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
"""


class TL2(SharpDelimTemplate):
    def construct(self):
        ####################################################

        sc = SmileCon().show()
        code2 = Text(code2_src, format='rich')

        ####################################################

        self.play(
            sc.anim.points.scale(0.5)
        )
        self.play(
            sc.update.points.rotate(PI / 2).scale([3/2.5, 2.5/3, 1])
        )
        self.play(
            FadeOut(sc),
            Write(code2)
        )

        ####################################################

        idmat = 'mat(1,0,0,0;0,1,0,0;0,0,1,0;0,0,0,1)'
        rotmat = 'mat(0,-1,0,0;1,0,0,0;0,0,1,0;0,0,0,1)'
        scalemat = 'mat(0.5,0,0,0;0,0.5,0,0;0,0,0.5,0;0,0,0,1)'

        _TypstMath = partial(TypstMath, scale=0.5)
        typ1 = _TypstMath(f'#[`trans`] = {idmat}')
        typ2 = _TypstMath(f'#[`trans`] = {idmat} {rotmat}')
        typ3 = _TypstMath(f'#[`trans`] = {idmat} {rotmat} {scalemat}')
        typ4 = _TypstMath(f'#[`trans`] = {rotmat} {scalemat}')
        for t in (typ1, typ2, typ3, typ4):
            try:
                t[rotmat].set(color=PURPLE)
                t[scalemat].set(color=MAROON)
            except PatternMismatchError:
                pass
        typ1.points.shift([-2.8, 1.02, 0.0])
        typ2.points.shift([1.06, 0.58, 0.0])
        typ3.points.shift([0.12, -1.1, 0.0])
        typ4.points.shift(DOWN * 1.5)

        arrow = Arrow(RIGHT * 1.5, LEFT * 1.5, color=YELLOW)
        arrow.points.next_to(typ4, DOWN, buff=SMALL_BUFF)

        r1 = SweepRect(code2[2][8:18], color=PURPLE, alpha=0.5)
        r2 = SweepRect(code2[3][8:17], color=MAROON, alpha=0.5)

        part1 = Group(code2[2][5], code2[2][7], code2[2][25:41], code2[2][42], code2[2][54], code2[2][57])
        part2 = Group(code2[2][43:60])
        part3 = Group(code2[3][25:48])
        for p in (part1, part2, part3):
            p.save_state()

        txt1 = Text('旋转角度<fs 0.75>(转成弧度制)</fs>', format='rich', font_size=18)
        txt1.points.next_to(part1, UP, buff=SMALL_BUFF)
        txt2 = Text('旋转轴', font_size=18)
        txt2.points.next_to(part2, UP, buff=SMALL_BUFF)
        txt3 = Text('各个方向的缩放倍率', font_size=18)
        txt3.points.next_to(part3, DOWN, buff=SMALL_BUFF)

        ####################################################

        self.play(
            r1.anim_in()
        )
        self.play(
            r2.anim_in()
        )
        self.play(
            FadeIn(typ1)
        )
        self.play(
            TransformMatchingDiff(typ1, typ2)
        )
        self.play(
            FadeOut(typ2, duration=0.6),
            Write(txt1),
            part1.anim.set(color=RED)
        )
        self.play(
            Write(txt2),
            part2.anim.set(color=RED)
        )
        self.play(
            part1.anim.load_state(),
            part2.anim.load_state(),
            FadeOut(Group(txt1, txt2)),
            FadeIn(typ2)
        )
        self.play(
            TransformMatchingDiff(typ2, typ3),
        )
        self.play(
            FadeOut(typ3, duration=0.6),
            Write(txt3),
            part3.anim.set(color=RED)
        )
        self.play(
            part3.anim.load_state(),
            FadeOut(txt3),
            FadeIn(typ3)
        )
        self.play(
            TransformMatchingDiff(typ3, typ4)
        )
        self.play(
            GrowArrow(arrow)
        )

        ####################################################

        part1 = typ4[33:]
        part2 = typ4[6:33]

        typ5 = TypstMath('#[`trans`] = mat(0,-0.5,0,0;0.5,0,0,0;0,0,0.5,0;0,0,0,1)')
        # typ5.match_pattern(typ4, '#[`trans`]')

        ####################################################

        self.play(
            ShowCreationThenFadeAround(part1)
        )
        self.play(
            ShowCreationThenFadeAround(part2)
        )
        self.play(
            TransformMatchingDiff(typ4, typ5),
            FadeOut(Group(code2, arrow, r1, r2))
        )

        ####################################################

        txt4 = Text('着色器')
        txt4.points.shift(DOWN * 1.5)
        typ5.generate_target().points.shift(UP * 1.5)

        arrow = Arrow(typ5.target, txt4, color=YELLOW)
        arrow_txt = arrow.create_text('?', color=YELLOW)

        arrow.generate_target().points.put_start_and_end_on(UP * 5, UP)
        txt4.generate_target() \
            .points.next_to(arrow.target, DOWN, buff=SMALL_BUFF) \
            .r.color.set(BLUE)

        frame = Rect(6, 1.5, color=BLUE)
        frame.points.next_to(txt4.target, DOWN, buff=SMALL_BUFF)

        ####################################################

        self.play(
            MoveToTarget(typ5),
            Write(txt4),
            GrowArrow(arrow)
        )
        self.play(
            FadeIn(arrow_txt)
        )
        self.play(
            FadeOut(arrow_txt, duration=0.3),
            FadeOut(typ5, UP * 4),
            MoveToTarget(arrow),
            MoveToTarget(txt4),
            Create(frame, auto_close_path=False, at=0.6),
        )

        ####################################################

        def gettxt(type: str) -> Text:
            txt = Text(f'<fc #569cd6>uniform</fc> <fc #569cd6>{type}</fc><fc #cccccc> xxx;</fc>', format='rich')
            txt.points.next_to(frame.points.box.left)
            return txt

        txtut1 = Text('向量类型')
        txtut2 = Text('矩阵类型')

        for t in (txtut1, txtut2):
            t.points.next_to(frame, LEFT)

        vec2 = gettxt('vec2')
        vec3 = gettxt('vec3')
        vec4 = gettxt('vec4')

        mat2 = gettxt('mat2')
        mat3 = gettxt('mat3')
        mat4 = gettxt('mat4')

        r = SweepRect(mat4[0][8:12])

        ####################################################

        def Rep(a, b):
            return AnimGroup(
                FadeOut(a, UP * 0.5),
                FadeIn(b, UP * 0.5)
            )

        self.play(
            Write(txtut1),
            FadeIn(vec2)
        )
        self.play(
            Rep(vec2, vec3)
        )
        self.play(
            Rep(vec3, vec4)
        )
        self.forward()
        self.play(
            AnimGroup(
                FadeOut(txtut1),
                FadeOut(vec4),
            ),
            AnimGroup(
                Write(txtut2),
                FadeIn(mat2),
            ),
            lag_ratio=0.5
        )
        self.play(
            Rep(mat2, mat3)
        )
        self.play(
            Rep(mat3, mat4)
        )
        self.play(
            r.anim_in(),
            r.anim_out(),
            lag_ratio=1
        )
        self.play(
            FadeOut(Group(txtut2, mat4, frame, txt4, arrow))
        )

        ####################################################

        code3 = Text(code3_src, format='rich', font_size=16)
        code3.points.to_border(UP)

        excepts = [42, 46, 102, 103, 104, 105, 106, 107]

        ins = code3[:]
        ins.remove(*ins[excepts])

        self.camera.save_state()
        self.camera.points.shift(UP * 2)

        ####################################################

        self.play(
            FadeIn(ins[:30]),
            self.camera.anim.load_state(),
            duration=1.6
        )
        ins[30:].show()
        self.play(
            self.camera.anim.points.shift(DOWN * 8.2),
            duration=2
        )
        self.play(
            FadeIn(code3[42])
        )
        self.play(
            FadeIn(code3[46])
        )
        self.play(
            ShowCreationThenFadeAround(code3[46][18:27])
        )
        self.play(
            self.camera.anim.points.shift(DOWN * 19.8),
            duration=2
        )
        self.play(
            FadeIn(code3[102:106])
        )
        self.play(
            Write(code3[107])
        )

        self.forward()


code4_src = R'''
<fc #6a9955># 渲染循环</fc>
<fc #c586c0>while</fc> <fc #569cd6>not</fc> <fc #4ec9b0>glfw</fc><fc #cccccc>.</fc><fc #dcdcaa>window_should_close</fc><fc #cccccc>(</fc><fc #9cdcfe>window</fc><fc #cccccc>):</fc>
    <fc #6a9955># 输入</fc>
    <fc #dcdcaa>process_input</fc><fc #cccccc>(</fc><fc #9cdcfe>window</fc><fc #cccccc>)</fc>

    <fc #6a9955># 矩阵</fc>
    <fc #9cdcfe>trans</fc> <fc #d4d4d4>=</fc> <fc #4ec9b0>glm</fc><fc #cccccc>.</fc><fc #9cdcfe>mat4</fc><fc #cccccc>(</fc><fc #b5cea8>1</fc><fc #cccccc>)</fc>
    <fc #9cdcfe>trans</fc> <fc #d4d4d4>=</fc> <fc #4ec9b0>glm</fc><fc #cccccc>.</fc><fc #dcdcaa>translate</fc><fc #cccccc>(</fc><fc #9cdcfe>trans</fc><fc #cccccc>, </fc><fc #4ec9b0>glm</fc><fc #cccccc>.</fc><fc #4ec9b0>vec3</fc><fc #cccccc>(</fc><fc #b5cea8>0.5</fc><fc #cccccc>, </fc><fc #d4d4d4>-</fc><fc #b5cea8>0.5</fc><fc #cccccc>, </fc><fc #b5cea8>0</fc><fc #cccccc>))</fc>
    <fc #9cdcfe>trans</fc> <fc #d4d4d4>=</fc> <fc #4ec9b0>glm</fc><fc #cccccc>.</fc><fc #dcdcaa>rotate</fc><fc #cccccc>(</fc><fc #9cdcfe>trans</fc><fc #cccccc>, </fc><fc #4ec9b0>glfw</fc><fc #cccccc>.</fc><fc #dcdcaa>get_time</fc><fc #cccccc>(), </fc><fc #4ec9b0>glm</fc><fc #cccccc>.</fc><fc #4ec9b0>vec3</fc><fc #cccccc>(</fc><fc #b5cea8>0</fc><fc #cccccc>, </fc><fc #b5cea8>0</fc><fc #cccccc>, </fc><fc #b5cea8>1</fc><fc #cccccc>))</fc>
    <fc #9cdcfe>prog</fc><fc #cccccc>[</fc><fc #ce9178>'transform'</fc><fc #cccccc>].</fc><fc #dcdcaa>write</fc><fc #cccccc>(</fc><fc #9cdcfe>trans</fc><fc #cccccc>.</fc><fc #dcdcaa>to_bytes</fc><fc #cccccc>())</fc>

    <fc #6a9955># 渲染指令</fc>
    <fc #9cdcfe>ctx</fc><fc #cccccc>.</fc><fc #dcdcaa>clear</fc><fc #cccccc>(</fc><fc #b5cea8>0.2</fc><fc #cccccc>, </fc><fc #b5cea8>0.3</fc><fc #cccccc>, </fc><fc #b5cea8>0.3</fc><fc #cccccc>)</fc>
    <fc #9cdcfe>vao</fc><fc #cccccc>.</fc><fc #dcdcaa>render</fc><fc #cccccc>(</fc><fc #4ec9b0>mgl</fc><fc #cccccc>.</fc><fc #9cdcfe>TRIANGLES</fc><fc #cccccc>)</fc>

    <fc #6a9955># 处理事件、交换缓冲</fc>
    <fc #4ec9b0>glfw</fc><fc #cccccc>.</fc><fc #dcdcaa>poll_events</fc><fc #cccccc>()</fc>
    <fc #4ec9b0>glfw</fc><fc #cccccc>.</fc><fc #dcdcaa>swap_buffers</fc><fc #cccccc>(</fc><fc #9cdcfe>window</fc><fc #cccccc>)</fc>
'''


class TL3(SharpDelimTemplate):
    def construct(self):
        ####################################################

        con = SmileCon(width=2, height=2)

        ####################################################

        self.prepare(
            GroupUpdater(
                con,
                lambda group, p: group.points.rotate(p.elapsed),
                duration=FOREVER
            )
        )
        self.play(
            FadeIn(con)
        )
        self.prepare(
            GroupUpdater(
                con,
                lambda group, p: group.points.shift(min(1, smooth(p.elapsed)) * (DOWN + RIGHT * 2)),
                duration=FOREVER
            )
        )

        self.forward(2)

        self.play(FadeOut(con))

        ####################################################

        code4 = Text(code4_src, format='rich', font_size=18)

        ins = code4[:]
        ins.remove(*code4[6:11])

        rect = DashedVItem(SurroundingRect(code4[6:11], buff=0.2), 50)
        hl = SurroundingRect(code4[6:11], buff=0.2, stroke_alpha=0, fill_alpha=0.25, depth=10)

        # code4.show()
        r1 = SweepRect(code4[9][12:22], color=PURPLE, alpha=0.5)
        r2 = SweepRect(code4[8][12:25], color=GOLD_E, alpha=0.5)

        ####################################################

        self.play(
            FadeIn(ins)
        )
        self.play(
            Create(rect, lag_ratio=1)
        )
        self.play(
            FadeIn(code4[6:11])
        )
        v = code4[9][30:45](VItem)
        v.glow.set(size=0.04)
        self.play(
            v.anim.glow.set(alpha=1)
        )
        self.play(
            FadeIn(hl)
        )
        self.play(
            FadeOut(hl)
        )
        self.play(
            r1.anim_in()
        )
        self.play(
            r2.anim_in()
        )

        self.forward()


from janim.cli import get_module_from_file
m12 = get_module_from_file('2026/LearnOpenGL-12-Matrix/code.py')


class TL4(m12.TL18):
    skip_aws = True


class TL5(SharpDelimTemplate):
    def construct(self):
        ####################################################

        gr = Rect(2.2, 2, color=GREEN_B)
        gr.points.shift(RIGHT * 2)
        # gr.save_state()

        def get_coords():
            points = gr.points.get()
            glpoints = points[::2, :2] / [Config.get.frame_x_radius, Config.get.frame_y_radius]
            txts = Group[Text]()
            for glp, dir in zip(glpoints, [UR, UL, DL, DR]):
                txt = Text(f'[{glp[0]:.2f}, {glp[1]:.2f}]', color=GREEN_B, font_size=12)
                txt.points.next_to(gr, dir, buff=SMALL_BUFF)
                txts.add(txt)
            return txts

        new_coords = get_coords()

        txt_mat = TypstMath('mat(gap: #0.8em, column-gap: #1.5em, ,,;,"矩阵？",;,,;)')
        txt_mat.points.shift(LEFT * 3)

        #####

        arrow1 = Arrow(LEFT * 2 + UP * 0.3, RIGHT * 2 + UP * 0.3, color=GREEN)
        arrow2 = Arrow(LEFT * 2 + DOWN * 0.3, RIGHT * 2 + DOWN * 0.3, color=ORANGE)
        arrows = Group(arrow1, arrow2)
        arrows.points.shift(LEFT)

        box = Group(gr, new_coords)
        box.generate_target()
        box.target[0].points.scale(0.5)
        for coord_txt, dir in zip(box.target[1], [UR, UL, DL, DR]):
            coord_txt.points.scale(0.8).next_to(box.target[0], dir, buff=SMALL_BUFF)
        box.target.points.next_to(arrow1, UP)

        txt_mat.generate_target() \
            .points.scale(0.6).next_to(arrow2, DOWN) \
            .r(VItem).color.set(ORANGE)

        gpu = SVGItem('gpu.svg')
        gpu.points.next_to(arrows)

        circle = Circle(color=YELLOW)
        circle.points.surround(txt_mat.target)

        new_con = ImageItem('container.jpg', alpha=0.5, depth=1, width=2.2, height=2)

        ####################################################

        self.forward()

        self.play(
            FadeIn(txt_mat),
            FadeIn(gr),
            FadeIn(new_coords)
        )

        self.play(
            GrowArrow(arrow1),
            GrowArrow(arrow2),
            MoveToTarget(box),
            MoveToTarget(txt_mat),
            FadeIn(gpu)
        )
        new_con.points.shift([3.58, 0.02, 0.0])
        self.play(
            AnimGroup(
                ShowPassingFlash(circle.copy()),
                Do(new_con.show),
                lag_ratio=0.8
            ),
            AnimGroup(
                ShowPassingFlash(circle.copy()),
                Do(lambda: new_con.points.rotate(-20 * DEGREES)),
                lag_ratio=0.8
            ),
            AnimGroup(
                ShowPassingFlash(circle.copy()),
                Do(lambda: new_con.points.scale([1.5, 0.8, 1])),
                lag_ratio=0.8
            ),
            lag_ratio=1.2
        )

        self.forward()


class TL6(SharpDelimTemplate):
    def construct(self):
        img = ImageItem('coordinate_systems.png')
        rect = SurroundingRect(img, depth=1, fill_alpha=1, fill_color=WHITE).round_corners(0.15)

        g = Group(rect, img).show()

        self.forward()


class All(Template, AboveTimelines):
    pass
