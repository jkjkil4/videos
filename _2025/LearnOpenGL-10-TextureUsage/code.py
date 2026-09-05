# flake8: noqa
import sys

sys.path.append('.')

from janim.imports import *
from PIL import ImageFilter

with reloads():
    from template import *

s1 = '<fs 0.7><c GREY_A>'
s2 = '</c></fs>'

RText = partial(Text, format=Text.Format.RichText)


class TitleTl(TitleTemplate):
    str1 = 'Learn OpenGL'
    str2 = '加载与创建纹理'


class ImgAttrs(Template):
    def construct(self):
        # video = Video(R'kdenlive\video_src\2025-05-19 18-08-22.mp4')
        # video.show().seek(130)

        txt1 = RText('<fc #9cdcfe>img</fc><fc #cccccc>.</fc><fc #9cdcfe>size</fc>')
        txt2 = RText('<fc #9cdcfe>img</fc><fc #cccccc>.</fc><fc #dcdcaa>tobytes</fc><fc #cccccc>()</fc>')
        txt3 = RText('<fc #cccccc>(</fc><fc #b5cea8>1920</fc><fc #cccccc>, </fc><fc #b5cea8>1080</fc><fc #cccccc>)</fc>')
        txt4 = RText('<fc #b5cea8>010100······</fc>')

        for i, char in enumerate(txt4[0]):
            alpha = 1 - i / (len(txt4[0]) - 1)
            char.fill.set(alpha=alpha)

        group = Group(txt1, txt2, txt3, txt4)
        group.points.arrange_in_grid(fill_rows_first=False, aligned_edge=RIGHT, buff=0.7)

        rect = SurroundingRect(group, **Rect.preset_shadow, depth=1, buff=0.4).show()

        self.play(FadeIn(rect))
        self.play(Write(txt1))
        self.play(Write(txt3))
        self.forward()
        self.play(Write(txt2))
        self.play(Write(txt4))
        self.forward()


class TextureParamsHighlight(Template):
    def construct(self):
        # video = Video(R'kdenlive\video_src\2025-05-19 18-08-22.mp4')
        # video.show().seek(170)

        YRect = partial(Rect, color=YELLOW)

        r1 = YRect([-3.73, 1.01, 0], [-2.84, 0.64, 0])
        r2 = YRect([-2.71, 1.02, 0], [-1.48, 0.62, 0])
        r3 = YRect([-1.41, 1.05, 0], [0.37, 0.62, 0])

        hl1 = HighlightRect(r1, buff=0, depth=1)
        hl2 = HighlightRect(r2, buff=0, depth=1)
        hl3 = HighlightRect(r3, buff=0, depth=1)

        self.play(
            FadeIn(hl1), FadeIn(r1),
            duration=0.5
        )
        self.forward()
        self.play(
            FadeOut(hl1), FadeOut(r1),
            FadeIn(hl2), FadeIn(r2),
            duration=0.5
        )
        self.forward()
        self.play(
            FadeOut(hl2), FadeOut(r2),
            FadeIn(hl3), FadeIn(r3),
            duration=0.5
        )
        self.forward()
        self.play(
            FadeOut(hl3), FadeOut(r3),
            duration=0.5
        )


class PillowImageNote(TextDisplayTemplate):
    typ_src = t_(
        R"""
        #set text(font: "Noto Sans S Chinese")
        #set par(justify: true)
        #box(width: 20em)[
            注意，这里我们载入的本身就已经是 `RGB` 形式的图像，刚好对应 `components=3`，因此不用额外的转换；如果你还需要载入其它的，例如带透明度通道的 `.png` `RGBA` 图像，你可以选择对不同的图像配置不同的 components，或者使用 `.convert('RGBA')` 的方式把图像都统一成一种格式
        ]
        """
    )

    def construct(self):
        FrameRect(**Rect.preset_shadow, depth=1).show()
        super().construct()


class VBOChangeFocus(Template):
    def construct(self):
        # video = Video(R'kdenlive\video_src\2025-05-19 18-38-44.mp4')
        # video.show().seek(60)

        self.play(FocusOn([-4.62, -0.8, 0], color=WHITE, alpha=0.5), duration=1.5)


class NewVBODataHighlight(Template):
    def construct(self):
        # video = Video(R'kdenlive\video_src\2025-05-19 18-38-44.mp4')
        # video.show().seek(80)

        rect = Rect([-3.8, -0.3, 0], [-2.61, -1.51, 0], color=YELLOW)
        self.play(
            ShowCreationThenFadeOut(
                rect,
                create_kwargs=dict(
                    auto_close_path=False
                )
            )
        )


class NewVBODataNote(Template):
    def construct(self):
        # video = Video(R'kdenlive\video_src\2025-05-19 18-38-44.mp4')
        # video.show().seek(114).start(speed=5)

        p1 = [-3.5, 0.95, 0]
        p2 = [-3.5, 0.54, 0]
        p3 = [-3.5, -0.68, 0]

        SText = partial(Text, font_size=14)

        tip1 = SText('← 声明新的顶点属性')
        tip1.points.next_to(p1, buff=0)
        tip2 = SText('← 将纹理坐标传递给片段着色器')
        tip2.points.next_to(p2, buff=0)

        tip2_arrow = Arrow(
            [-1.38, 0.32, 0], [-2.95, -0.52, 0],
            path_arc=-65 * DEGREES,
            stroke_radius=0.015,
            max_length_to_tip_length_ratio=0.08,
            buff=0.15,
            color=GREY
        )

        tip3 = SText('← 接收从顶点着色器传递过来的纹理坐标')
        tip3.points.next_to(p3, buff=0)

        self.play(Write(tip1))
        self.forward()
        self.play(Write(tip2))
        self.forward()
        self.play(GrowArrow(tip2_arrow))
        self.forward()
        self.play(*map(FadeOut, (tip1, tip2, tip2_arrow)))
        self.forward()
        self.play(Write(tip3))
        self.forward()


class TakeColor(Template):
    def construct(self):
        orig = Image.open(find_file('madeline.png'))
        size = (5, 5)
        kernel = [1] * 25
        blurred = orig.filter(ImageFilter.Kernel(size, kernel, scale=25, offset=0))

        img1 = ImageItem(orig)
        img2 = ImageItem(blurred)
        img = Group(img1, img2)

        img.points.scale(1.5)

        dot = Dot(radius=0.04, fill_color=YELLOW, stroke_color=BLACK, stroke_alpha=1, stroke_radius=0.01)
        dot.points.shift(DL * 0.1)

        txt = Text(
            'v_texcoord',
            font_size=12,
            stroke_color=BLACK,
            stroke_alpha=1,
            stroke_background=True
        )
        txt.points.next_to(dot, UP, buff=SMALL_BUFF)

        path = VItem(
            [-0.1, -0.1, 0], [-0.09, -0.15, 0], [-0.1, -0.21, 0], [-0.1, -0.3, 0], [-0.15, -0.36, 0],
            [-0.24, -0.39, 0], [-0.32, -0.35, 0], [-0.37, -0.29, 0], [-0.37, -0.21, 0], [-0.37, -0.15, 0],
            [-0.35, -0.1, 0], [-0.33, -0.06, 0], [-0.31, -0.02, 0], [-0.29, 0.04, 0], [-0.31, 0.08, 0],
            [-0.37, 0.12, 0], [-0.45, 0.13, 0], [-0.52, 0.12, 0], [-0.56, 0.08, 0], [-0.58, 0.04, 0],
            [-0.58, -0.02, 0], [-0.58, -0.07, 0], [-0.56, -0.11, 0], [-0.55, -0.17, 0], [-0.51, -0.19, 0],
            [-0.43, -0.18, 0], [-0.35, -0.13, 0], [-0.3, -0.08, 0], [-0.27, -0.03, 0], [-0.22, 0.03, 0],
            [-0.16, 0.07, 0], [-0.1, 0.12, 0], [-0.04, 0.15, 0], [0.03, 0.17, 0], [0.11, 0.16, 0],
            [0.17, 0.13, 0], [0.23, 0.13, 0], [0.3, 0.2, 0], [0.33, 0.28, 0], [0.32, 0.34, 0],
            [0.27, 0.32, 0], [0.25, 0.25, 0], [0.25, 0.15, 0], [0.26, 0.08, 0], [0.27, 0.02, 0],
            [0.3, -0.05, 0], [0.28, -0.1, 0], [0.24, -0.15, 0], [0.16, -0.16, 0], [0.1, -0.17, 0],
            [0.05, -0.16, 0], [0, -0.15, 0], [-0.04, -0.14, 0], [-0.08, -0.12, 0], [-0.1, -0.09, 0],
        )

        self.play(
            FadeIn(img1, duration=0.6),
            FadeIn(dot, scale=0.2, duration=0.8, at=0.3),
            Write(txt, at=0.5, duration=0.6)
        )

        def item_updater(p: UpdaterParams):
            pos = dot.current().points.box.center
            plate = Square(0.5, fill_color=img1.point_to_rgba(pos), fill_alpha=1)
            plate.points.shift(RIGHT * 3)
            return Group(plate, Arrow(img1, plate, color=[GREY, WHITE], tip_kwargs=dict(color=WHITE)))

        self.play(
            AnimGroup(
                MoveAlongPath(dot, path),
                Follow(txt, dot, UP, buff=SMALL_BUFF),
                duration=4
            ),
            ItemUpdater(None, item_updater, duration=5),
        )


class SamplerDesc(Template):
    def construct(self):
        rect = FrameRect(**Rect.preset_shadow, depth=1)
        title = Title('采样器')
        txt = Text('sampler1D\nsampler2D\nsampler3D')
        txt.points.arrange(DOWN)

        self.play(FadeIn(rect), Write(title, at=0.4))
        self.forward()
        self.play(Write(txt[0]))
        self.play(Write(txt[2]))
        self.forward()
        self.play(
            Write(txt[1]),
            txt[0, 2](VItem).anim(duration=0.6).color.set(GREY)
        )
        self.forward()


class SamplerHighlight(Template):
    def construct(self):
        # video = Video(R'kdenlive\video_src\2025-05-19 18-38-44.mp4')
        # video.show().seek(235)

        hl = boolean_ops.Difference(
            FrameRect(),
            boolean_ops.Union(
                Rect([-5.93, -0.9, 0], [-2.01, -1.29, 0]),
                Rect([-4.34, -2.2, 0], [-0.67, -2.51, 0])
            ).points.shift(UP * 0.5).r,
            **Rect.preset_shadow,
        )

        self.play(FadeIn(hl))
        self.forward()
        self.play(FadeOut(hl))

        self.forward()

        YUdl = partial(Underline, color=YELLOW, buff=0)

        ul1 = YUdl(Rect([-3.51, -1.68, 0], [-2.51, -2.02, 0]))
        ul2 = YUdl(Rect([-2.37, -1.68, 0], [-1.36, -2.03, 0]))

        self.play(Create(ul1))
        self.forward()
        self.play(
            Destruction(ul1, rate_func=rush_into),
            Create(ul2, rate_func=rush_from),
            lag_ratio=0.8
        )
        self.forward()
        self.play(Destruction(ul2))


class TextureParams_Sub(Template):
    def construct(self):
        img = ImageItem('madeline.png').show()
        img.points.scale(1.5)

        dot = Dot(radius=0.06, fill_color=BLACK, stroke_color=WHITE, stroke_alpha=1, stroke_radius=0.02)
        dot.points.shift(DR * 0.3)
        dot.show()

        self.play(FadeIn(img), FadeIn(dot))
        self.play(
            self.camera.anim
                .points.rotate(-20 * DEGREES, axis=RIGHT).rotate(-50 * DEGREES, axis=UP),
            dot.anim.points.shift(OUT * 0.8)
        )

        self.forward(10)


class TextureParams(Template):
    def construct(self):
        sub = TextureParams_Sub().build().to_item().show()
        self.forward(2)

        YRect = partial(Rect, color=YELLOW)

        r1 = YRect([-0.84, 1.22, 0], [0.71, -1.4, 0])
        r2 = YRect([0.65, -0.19, 0], [0.98, -0.59, 0])

        self.forward()
        self.play(ShowCreationThenFadeOut(r1, create_kwargs=dict(auto_close_path=False)))
        self.forward(0.3)
        self.play(ShowCreationThenFadeOut(r2, create_kwargs=dict(auto_close_path=False)))
        self.forward()


class TextureLocation(Template):
    def construct(self):
        rect = FrameRect(**Rect.preset_shadow)

        self.play(FadeIn(rect))

        locs = TypstText(
            '''
            #grid(
                fill: (x, y) => luma(50%).transparentize(100% * y / 4),
                inset: 6pt,
                ..for i in range(0, 4) {
                    text(fill: white.transparentize(100% * i / 4))[#i]
                }.children
            )
            '''
        )
        loc_zero = locs[4]
        # locs.points.move_to_by_indicator(loc_zero, ORIGIN)

        txt_uniform = RText('<fc #ce9178>ourTexture</fc>', font_size=18)
        txt_pyobj = RText('<fc #9cdcfe>texture</fc>', font_size=18)

        txt_uniform.points.next_to(loc_zero, RIGHT, buff=3.5)
        txt_pyobj.points.next_to(loc_zero, LEFT, buff=3.5)

        arrow_uniform = Arrow(txt_uniform, loc_zero, color=BLUE)
        arrow_pyobj = Arrow(txt_pyobj, loc_zero, color=BLUE)

        bind_uniform = arrow_uniform.create_text(
            "<fc #9cdcfe>prog</fc><fc #cccccc>[</fc><fc #ce9178>'ourTexture'</fc><fc #cccccc>] </fc><fc #d4d4d4>=</fc> <fc #b5cea8>0</fc>",
            format=Text.Format.RichText,
            font_size=14
        )
        bind_pyobj = arrow_pyobj.create_text(
            '<fc #9cdcfe>texture</fc><fc #cccccc>.</fc><fc #dcdcaa>use</fc><fc #cccccc>(</fc><fc #b5cea8>0</fc><fc #cccccc>)</fc>',
            format=Text.Format.RichText,
            font_size=14
        )

        self.play(
            FadeIn(locs, UP, duration=1.2),
            DrawBorderThenFill(txt_uniform, at=0.3, duration=1.1),
            DrawBorderThenFill(txt_pyobj, at=0.3, duration=1.1)
        )

        self.forward()

        self.play(
            GrowArrow(arrow_uniform),
            FadeIn(bind_uniform, at=0.2)
        )

        self.forward()

        self.play(
            GrowArrow(arrow_pyobj),
            FadeIn(bind_pyobj, at=0.2)
        )

        self.forward()

        self.play(
            FocusOn(loc_zero)
        )

        self.forward()

        g = Group(bind_uniform, bind_pyobj)
        g2 = g.copy()
        g2.points.arrange(DOWN, aligned_edge=LEFT).shift(RIGHT * 2)

        self.play(
            FadeOut(Group(txt_uniform, txt_pyobj, arrow_uniform, arrow_pyobj, locs)),
            Transform(g, g2, duration=1.5, path_arc=40 * DEGREES),
            rect.anim(at=0.5)
                .points.replace(SurroundingRect(g2), stretch=True)
        )

        self.forward(2)


code_colorbox = """
<fc #9cdcfe>vertex_shader</fc> <fc #d4d4d4>=</fc> <fc #ce9178>'''</fc>
<fc #ce9178>#version 330 core</fc>

<fc #ce9178>in vec3 in_vert;</fc>
<fc #ce9178>in vec3 in_color;</fc>
<fc #ce9178>in vec2 in_texcoord;</fc>

<fc #ce9178>out vec3 v_color;</fc>
<fc #ce9178>out vec2 v_texcoord;</fc>

<fc #ce9178>void main()</fc>
<fc #ce9178>{</fc>
<fc #ce9178>    gl_Position = vec4(in_vert.x, in_vert.y, in_vert.z, 1.0);</fc>
<fc #ce9178>    v_color = in_color;</fc>
<fc #ce9178>    v_texcoord = in_texcoord;</fc>
<fc #ce9178>}</fc>
<fc #ce9178>'''</fc>

<fc #9cdcfe>fragment_shader</fc> <fc #d4d4d4>=</fc> <fc #ce9178>'''</fc>
<fc #ce9178>#version 330 core</fc>

<fc #ce9178>in vec3 v_color;</fc>
<fc #ce9178>in vec2 v_texcoord;</fc>

<fc #ce9178>uniform sampler2D ourTexture;</fc>

<fc #ce9178>out vec4 FragColor;</fc>

<fc #ce9178>void main()</fc>
<fc #ce9178>{</fc>
<fc #ce9178>    FragColor = texture(ourTexture, v_texcoord) * vec4(v_color, 1.0);</fc>
<fc #ce9178>}</fc>
<fc #ce9178>'''</fc>
"""


class ColorBoxCode(Template):
    def construct(self):
        code = Text(code_colorbox, format=Text.Format.RichText, font_size=12).show()
        code.points.to_border(RIGHT)

        rect = SurroundingRect(code, **Rect.preset_shadow, depth=1).show()
        rect.set(fill_alpha=0.8)

        for i, line in enumerate(code):
            if i not in (5, 8, 14, 22, 31):
                line.color.fade(0.5)


class TextureLocationNote(TextDisplayTemplate):
    typ_src = t_(
        R"""
        #set text(font: "Noto Sans S Chinese")
        #set par(justify: true)
        #import "@janim/colors:0.0.0": *
        #box(width: 25em)[
            在前面，我们向 GLSL 中的纹理 uniform 和 Python 中的纹理对象都绑定了位置 0，这样它们就关联了起来。

            一个纹理的位置值通常称为一个纹理单元(Texture Unit)，纹理单元的主要目的是让我们通过分别绑定不同的位置值，以便在着色器中可以使用多于一个的纹理。

            #box(stroke: BLUE, inset: 4pt)[
                OpenGL 至少保证有 16 个纹理单元供你使用，也就是说你可以使用从 0 到 15 的位置值。
            ]
        ]
        """
    )

    stay_duration=6

    def construct(self):
        FrameRect(**Rect.preset_shadow, depth=1).show()
        super().construct()

        ctx = mgl.create_context()
        texture = ctx.texture((1, 1), 4)
        texture.wr


code_twotexture1 = """
<fc #9cdcfe>fragment_shader</fc> <fc #d4d4d4>=</fc> <fc #ce9178>'''</fc>
<fc #ce9178>#version 330 core</fc>

<fc #ce9178>in vec3 v_color;</fc>
<fc #ce9178>in vec2 v_texcoord;</fc>

<fc #ce9178>uniform sampler2D texture1;</fc>
<fc #ce9178>uniform sampler2D texture2;</fc>

<fc #ce9178>out vec4 FragColor;</fc>

<fc #ce9178>void main()</fc>
<fc #ce9178>{</fc>
<fc #ce9178>    FragColor = mix(texture(texture1, v_texcoord), texture(texture2, v_texcoord), 0.2);</fc>
<fc #ce9178>}</fc>
<fc #ce9178>'''</fc>
"""


class TwoTextureCode1(Template):
    def construct(self):
        code = Text(code_twotexture1, format=Text.Format.RichText, font_size=12).show()
        code.points.to_border(UR)

        rect = SurroundingRect(code, **Rect.preset_shadow, depth=1).show()
        rect.set(fill_alpha=0.8)

        for i, line in enumerate(code):
            if i not in (7, 8, 14):
                line.color.fade(0.5)


class GLSLMixParams(Template):
    def construct(self):
        # video = Video(R'kdenlive/video_src/2025-05-19 18-57-18.mp4').show()
        # video.seek(2 * 60 + 30)

        line1 = Line([-3.88, -0.4, 0], [-1.08, -0.4, 0], color=YELLOW)
        line2 = Line([-0.89, -0.4, 0], [1.85, -0.4, 0], color=YELLOW)
        line3 = Line([2.04, -0.4, 0], [2.4, -0.4, 0], color=YELLOW)

        for line in (line1, line2, line3):
            self.play(Create(line))
            self.forward(0.5)


class GLSLMix(Template):
    def construct(self):
        ##############################################################

        rect = FrameRect(**Rect.preset_shadow, depth=1)
        title = Title('mix 函数')

        line = NumberLine((0, 1), include_numbers=True, unit_size=2)
        line.points.shift(UP)

        tracker = ValueTracker(0.2)

        def tip_updater(data: ArrowTip, p=None):
            data.points.next_to(line.n2p(tracker.current().data.get()), UP, buff=SMALL_BUFF)

        tip = ArrowTip(angle=-PI / 2)
        tip_updater(tip)

        def tip_txt_updater(p=None):
            value = tracker.current().data.get()
            txt = Text(f'{value:.2f}', font_size=18)
            txt.points.next_to(tip.current(), UP, buff=SMALL_BUFF)
            return txt

        tip_txt = tip_txt_updater()

        img1 = ImageItem('container.jpg', height=1.5)
        img1.points.next_to(line, LEFT, item_root_only=True, buff=0.35)
        img2 = ImageItem('awesomeface.png', height=1.5)
        img2.points.next_to(line, RIGHT, item_root_only=True, buff=0.35)

        img1b = ImageItem('container.jpg', height=1.5)
        img2b = ImageItem('awesomeface_b.png', height=1.5)
        Group(img1b, img2b).points.next_to(line, DOWN, buff=LARGE_BUFF)

        ##############################################################

        self.play(FadeIn(rect), Write(title), lag_ratio=0.2)
        self.forward()
        self.play(
            FadeIn(line),
            AnimGroup(
                FadeIn(img1, scale=1.2, shift=RIGHT * 0.3, rate_func=rush_from),
                FadeIn(img2, scale=1.2, shift=LEFT * 0.3, rate_func=rush_from),
                at=0.4, duration=0.6
            ),
            FadeIn(Group(tip, tip_txt), DOWN * 0.3, at=0.7, duration=0.6)
        )
        self.forward()
        self.play(
            Aligned(
                Succession(
                    AnimGroup(
                        tracker.anim(duration=0.5).data.set(0),
                        FadeIn(img1b, duration=0.5),
                        lag_ratio=0.6,
                    ),
                    Wait(),
                    AnimGroup(
                        tracker.anim.data.set(1),
                        FadeIn(img2b)
                    ),
                    Wait(),
                    AnimGroup(
                        tracker.anim.data.set(0.2),
                        img2b.anim.color.set(alpha=0.2)
                    )
                ),
                DataUpdater(tip, tip_updater),
                ItemUpdater(tip_txt, tip_txt_updater),
            )
        )
        self.forward()

        ##############################################################


class TextureLocation2(Template):
    def construct(self):
        # video = Video(R'kdenlive/video_src/2025-05-19 18-57-18.mp4').show()
        # video.seek(6 * 60 + 25)

        rect = HighlightRect(Rect([-5.9, 0.9, 0], [-3.71, -0.49, 0]), buff=0).show()

        locs = TypstText(
            '''
            #grid(
                fill: (x, y) => luma(50%).transparentize(100% * y / 4),
                inset: 6pt,
                ..for i in range(0, 4) {
                    text(fill: white.transparentize(100% * i / 4))[#i]
                }.children
            )
            '''
        ).show()
        locs.points.shift(UR * 2)
        loc_zero = locs[4]
        loc_one = locs[5]
        # locs.points.move_to_by_indicator(loc_zero, ORIGIN)

        txt_uniform1 = RText('<fc #ce9178>texture1</fc>', font_size=18).show()
        txt_pyobj1 = RText('<fc #9cdcfe>texture1</fc>', font_size=18).show()

        txt_uniform1.points.next_to(loc_zero, RIGHT, buff=2.7)
        txt_pyobj1.points.next_to(loc_zero, LEFT, buff=2.7)

        arrow_uniform1 = Arrow(txt_uniform1, loc_zero, color=BLUE).show()
        arrow_pyobj1 = Arrow(txt_pyobj1, loc_zero, color=BLUE).show()

        bind_uniform1 = arrow_uniform1.create_text(
            "<fc #9cdcfe>prog</fc><fc #cccccc>[</fc><fc #ce9178>'texture1'</fc><fc #cccccc>] </fc><fc #d4d4d4>=</fc> <fc #b5cea8>0</fc>",
            format=Text.Format.RichText,
            font_size=10,
            buff=SMALL_BUFF
        ).show()
        bind_pyobj1 = arrow_pyobj1.create_text(
            '<fc #9cdcfe>texture1</fc><fc #cccccc>.</fc><fc #dcdcaa>use</fc><fc #cccccc>(</fc><fc #b5cea8>0</fc><fc #cccccc>)</fc>',
            format=Text.Format.RichText,
            font_size=10,
            buff=SMALL_BUFF
        ).show()

        txt_uniform2 = RText('<fc #ce9178>texture2</fc>', font_size=18)
        txt_pyobj2 = RText('<fc #9cdcfe>texture2</fc>', font_size=18)

        txt_uniform2.points.next_to(loc_one, RIGHT, buff=2.7)
        txt_pyobj2.points.next_to(loc_one, LEFT, buff=2.7)

        arrow_uniform2 = Arrow(txt_uniform2, loc_one, color=BLUE)
        arrow_pyobj2 = Arrow(txt_pyobj2, loc_one, color=BLUE)

        bind_uniform2 = arrow_uniform2.create_text(
            "<fc #9cdcfe>prog</fc><fc #cccccc>[</fc><fc #ce9178>'texture2'</fc><fc #cccccc>] </fc><fc #d4d4d4>=</fc> <fc #b5cea8>1</fc>",
            format=Text.Format.RichText,
            font_size=10,
            buff=SMALL_BUFF
        )
        bind_pyobj2 = arrow_pyobj2.create_text(
            '<fc #9cdcfe>texture2</fc><fc #cccccc>.</fc><fc #dcdcaa>use</fc><fc #cccccc>(</fc><fc #b5cea8>1</fc><fc #cccccc>)</fc>',
            format=Text.Format.RichText,
            font_size=10,
            buff=SMALL_BUFF
        )

        self.forward()
        self.play(*map(FadeIn, (txt_uniform2, txt_pyobj2, arrow_uniform2, arrow_pyobj2, bind_uniform2, bind_pyobj2)))
        self.forward()


code_removecolor1 = """
<fc #9cdcfe>vertices</fc> <fc #d4d4d4>=</fc> <fc #4ec9b0>np</fc><fc #cccccc>.</fc><fc #dcdcaa>array</fc><fc #cccccc>([</fc>
<fc #6a9955>#   ----- 位置 -----  ---- 颜色 ----   - 纹理坐标 -</fc>
     <fc #b5cea8>0.5</fc><fc #cccccc>,  </fc><fc #b5cea8>0.5</fc><fc #cccccc>, </fc><fc #b5cea8>0.0</fc><fc #cccccc>,  </fc><fc #b5cea8>1.0</fc><fc #cccccc>, </fc><fc #b5cea8>0.0</fc><fc #cccccc>, </fc><fc #b5cea8>0.0</fc><fc #cccccc>,  </fc><fc #b5cea8>1.0</fc><fc #cccccc>, </fc><fc #b5cea8>1.0</fc><fc #cccccc>,   </fc><fc #6a9955># 右上</fc>
     <fc #b5cea8>0.5</fc><fc #cccccc>, </fc><fc #d4d4d4>-</fc><fc #b5cea8>0.5</fc><fc #cccccc>, </fc><fc #b5cea8>0.0</fc><fc #cccccc>,  </fc><fc #b5cea8>0.0</fc><fc #cccccc>, </fc><fc #b5cea8>1.0</fc><fc #cccccc>, </fc><fc #b5cea8>0.0</fc><fc #cccccc>,  </fc><fc #b5cea8>1.0</fc><fc #cccccc>, </fc><fc #b5cea8>0.0</fc><fc #cccccc>,   </fc><fc #6a9955># 右下</fc>
    <fc #d4d4d4>-</fc><fc #b5cea8>0.5</fc><fc #cccccc>, </fc><fc #d4d4d4>-</fc><fc #b5cea8>0.5</fc><fc #cccccc>, </fc><fc #b5cea8>0.0</fc><fc #cccccc>,  </fc><fc #b5cea8>0.0</fc><fc #cccccc>, </fc><fc #b5cea8>0.0</fc><fc #cccccc>, </fc><fc #b5cea8>1.0</fc><fc #cccccc>,  </fc><fc #b5cea8>0.0</fc><fc #cccccc>, </fc><fc #b5cea8>0.0</fc><fc #cccccc>,   </fc><fc #6a9955># 左下</fc>
    <fc #d4d4d4>-</fc><fc #b5cea8>0.5</fc><fc #cccccc>,  </fc><fc #b5cea8>0.5</fc><fc #cccccc>, </fc><fc #b5cea8>0.0</fc><fc #cccccc>,  </fc><fc #b5cea8>1.0</fc><fc #cccccc>, </fc><fc #b5cea8>1.0</fc><fc #cccccc>, </fc><fc #b5cea8>0.0</fc><fc #cccccc>,  </fc><fc #b5cea8>0.0</fc><fc #cccccc>, </fc><fc #b5cea8>1.0</fc>    <fc #6a9955># 左上</fc>
<fc #cccccc>], </fc><fc #9cdcfe>dtype</fc><fc #d4d4d4>=</fc><fc #ce9178>'f4'</fc><fc #cccccc>)</fc>
"""

code_removecolor2 = """
<fc #9cdcfe>vertex_shader</fc> <fc #d4d4d4>=</fc> <fc #ce9178>'''</fc>
<fc #ce9178>#version 330 core</fc>

<fc #ce9178>in vec3 in_vert;</fc>
<fc #ce9178>in vec3 in_color;</fc>
<fc #ce9178>in vec2 in_texcoord;</fc>

<fc #ce9178>out vec3 v_color;</fc>
<fc #ce9178>out vec2 v_texcoord;</fc>

<fc #ce9178>void main()</fc>
<fc #ce9178>{</fc>
<fc #ce9178>    gl_Position = vec4(in_vert.x, in_vert.y, in_vert.z, 1.0);</fc>
<fc #ce9178>    v_color = in_color;</fc>
<fc #ce9178>    v_texcoord = in_texcoord;</fc>
<fc #ce9178>}</fc>
<fc #ce9178>'''</fc>

<fc #9cdcfe>fragment_shader</fc> <fc #d4d4d4>=</fc> <fc #ce9178>'''</fc>
<fc #ce9178>#version 330 core</fc>

<fc #ce9178>in vec3 v_color;</fc>
<fc #ce9178>in vec2 v_texcoord;</fc>

<fc #ce9178>uniform sampler2D texture1;</fc>
<fc #ce9178>uniform sampler2D texture2;</fc>

<fc #ce9178>out vec4 FragColor;</fc>

<fc #ce9178>void main()</fc>
<fc #ce9178>{</fc>
<fc #ce9178>    FragColor = mix(texture(texture1, v_texcoord), texture(texture2, v_texcoord), 0.2);</fc>
<fc #ce9178>}</fc>
<fc #ce9178>'''</fc>
"""

class RemoveColorCode(MOVTemplate):
    def construct(self):
        code1 = Text(code_removecolor1, format=Text.Format.RichText, font_size=10)
        code1.points.to_border(UR)

        code2 = Text(code_removecolor2, format=Text.Format.RichText, font_size=10)
        code2.points.to_border(UR)

        pyline = Text(
            "<fc #9cdcfe>vao</fc> <fc #d4d4d4>=</fc> <fc #9cdcfe>ctx</fc><fc #cccccc>.</fc><fc #dcdcaa>vertex_array</fc><fc #cccccc>(</fc><fc #9cdcfe>prog</fc><fc #cccccc>, </fc><fc #9cdcfe>vbo</fc><fc #cccccc>, </fc><fc #ce9178>'in_vert'</fc><fc #cccccc>, </fc><fc #ce9178>'in_color'</fc><fc #cccccc>, </fc><fc #ce9178>'in_texcoord'</fc><fc #cccccc>, </fc><fc #9cdcfe>index_buffer</fc><fc #d4d4d4>=</fc><fc #9cdcfe>ibo</fc><fc #cccccc>)</fc>",
            format=Text.Format.RichText,
            font_size=12
        )
        pyline.points.to_border(UR)

        rect1 = SurroundingRect(code1, **Rect.preset_shadow, depth=1)
        rect1.set(fill_alpha=0.8, stroke_alpha=1, stroke_color=WHITE)

        rect2 = SurroundingRect(code2, **Rect.preset_shadow, depth=1)
        rect2.set(fill_alpha=0.8, stroke_alpha=1, stroke_color=WHITE)

        rect3 = SurroundingRect(pyline, **Rect.preset_shadow, depth=1)
        rect3.set(fill_alpha=0.8, stroke_alpha=1, stroke_color=WHITE)

        def del_line(item: Points):
            return Line(
                item.points.box.left,
                item.points.box.right,
                color=YELLOW,
                stroke_radius=0.01,
                alpha=0.8
            )

        del_line1 = Group(
            del_line(code1[2][20:32]),
            *[del_line(code1[i][22:36]) for i in range(3, 7)]
        )

        del_line2 = Group.from_iterable(del_line(code2[i]) for i in (5, 8, 14, 22))

        del_line3 = del_line(pyline[0][45:55])

        self.show(code1, rect1, del_line1)
        self.forward()
        self.hide_all()
        self.show(code2, rect2, del_line2)
        self.forward()
        self.hide_all()
        self.show(pyline, rect3, del_line3)
        self.forward()


class ImageAndOpenGLCoords(MOVTemplate):
    def construct(self):
        txt_img = Text('图像')
        txt_opengl = Text('OpenGL')

        class ColoredAxes(Axes):
            def __init__(self, *, inverse_y=False, **kwargs):
                super().__init__(
                    (0, 1.5), (0, -1.5) if inverse_y else (0, 1.5),
                    axis_config=dict(
                        include_tip=True,
                        include_ticks=False,
                    ),
                    **kwargs
                )
                self.x_axis.set(color=RED)
                self.y_axis.set(color=GREEN)

                self.x_label = TypstMath('x', color=RED)
                self.x_label.points.next_to(self.x_axis, RIGHT)

                self.y_label = TypstMath('y', color=GREEN)
                self.y_label.points.next_to(self.y_axis, DOWN if inverse_y else UP)

                self.add(self.x_label, self.y_label)

        axes_img = ColoredAxes(inverse_y=True)
        axes_opengl = ColoredAxes()

        img = ImageItem('awesomeface_b.png', height=2, depth=1)

        g_img = Group(txt_img, axes_img)
        g_img.points.arrange(RIGHT)

        g_opengl = Group(txt_opengl, axes_opengl)
        g_opengl.points.arrange(RIGHT)

        line = DashedLine(ORIGIN, RIGHT * g_opengl.points.box.width)

        g = Group(g_img, line, g_opengl)
        g.points.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=RIGHT)\
            .to_border(RIGHT, buff=LARGE_BUFF)

        rect = SurroundingRect(
            g,
            **Rect.preset_shadow,
            depth=2,
            buff=0.5
        )

        img.points.next_to(axes_img.c2p(), DR, buff=0)

        self.play(
            FadeIn(rect),
            AnimGroup(
                FadeIn(axes_img, scale=0.8),
                FadeIn(axes_opengl, scale=0.8),
                Write(txt_img, at=0.5, duration=1),
                Write(txt_opengl, at=0.5, duration=1)
            ),
            lag_ratio=0.5
        )
        self.play(FadeIn(img, scale=1.2, rate_func=rush_from))

        self.forward()

        self.play(
            CircleIndicate(Dot(axes_opengl.c2p()), buff=0.05, scale=6, rate_func=there_and_back_with_pause),
            duration=3
        )

        self.forward()

        self.play(
            CircleIndicate(Dot(axes_img.c2p()), buff=0.05, scale=6, rate_func=there_and_back_with_pause),
            duration=3
        )

        self.forward()

        center = (
            axes_img.c2p() +
            axes_opengl.c2p()
        ) / 2

        self.play(
            Rotate(img, PI, axis=RIGHT, about_point=center)
        )

        self.forward()

        self.play(
            Rotate(img, -PI, axis=RIGHT, about_point=center),
            duration=0.7
        )

        self.forward()

        self.play(
            Rotate(img, PI, axis=RIGHT)
        )

        self.forward()

        self.play(
            Rotate(img, PI, axis=RIGHT, about_point=center)
        )

        self.forward()
