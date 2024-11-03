from __future__ import annotations

# flake8: noqa
import random
import sys

from janim.render.base import get_custom_program
from janim.render.texture import get_texture_from_img

sys.path.append('.')

from janim.imports import *

from utils.template import *

s1 = '<fs 0.7><c GREY_A>'
s2 = '</c></fs>'


class SurBox(Group):
    def __init__(self, item: Item, text: str, buff=MED_SMALL_BUFF, color=BLUE, **kwargs):
        sur = SurroundingRect(item, buff=buff, color=color)
        txt = Text(text, font_size=18, color=BLUE)
        txt.points.next_to(sur, DOWN, buff=SMALL_BUFF, aligned_edge=LEFT)
        super().__init__(sur, txt)


class TitleTl(TitleTemplate):
    str1 = 'Learn OpenGL'
    str2 = '纹理'


class Intro(Template):
    def construct(self) -> None:
        #####################################################

        shaders3 = ImageItem('shaders3.png')
        # moderngl = ImageItem('moderngl.png')
        celeste = PixelImageItem('07.png')


        points = [[1.06, -0.87, 0], [-1.07, -0.85, 0], [0, 0.76, 0]]
        colors = ['red', 'lime', 'blue']

        verts = DotCloud(*points)

        circles = Group.from_iterable(
            Circle(0.2, color=c)
                .points.move_to(p)
                .r
            for p, c in zip(points, colors)
        )

        np.random.seed(114514)
        celeste_points = np.array([
            [interpolate(-3.18, 6.53, a1), interpolate(-4, 1.78, a2), 0]
            for a1, a2 in np.random.random((2500, 2))
        ])
        celeste_colors = np.array([
            celeste.point_to_rgba(p)
            for p in celeste_points
        ])
        flags = celeste_colors[:, 3] > 0.9
        # print(flags)

        dots = DotCloud(
            *celeste_points[flags],
            color=celeste_colors[flags][:, :3],
            radius=0.015
        )

        #####################################################

        self.show(verts)
        self.forward()

        self.play(
            *[
                Create(c, auto_close_path=False)
                for c in circles
            ],
            lag_ratio=0.4,
            duration=1
        )
        self.play(
            verts.anim.color.set(colors)
                .r.radius.set(0.1),
            *[
                FadeOut(c, scale=0.5)
                for c in circles
            ]
        )
        self.play(
            FadeOut(verts),
            FadeIn(shaders3)
        )

        def easing1(t: np.ndarray):
            t = np.clip(t, 0, 1)
            return (np.cos(t * PI) + 1) / 2

        def updater1(data: DotCloud, p: UpdaterParams):
            adv = 2
            alpha = np.linspace(1, 2 + adv, data.points.count())
            alpha -= p.alpha * (adv + 2)
            data.color.set(alpha=easing1(alpha))

        self.play(
            FadeOut(shaders3, duration=0.4)
        )

        cam_stat = self.camera.copy()
        self.camera.points.scale(0.1).shift(RIGHT * 4 + DOWN)

        self.play(
            DataUpdater(
                dots,
                updater1,
                become_at_end=False
            )
        )
        self.play(
            self.camera.anim.become(cam_stat),
            duration=2
        )

        ############################################################

        def get_text_by_two_point(text, p1, p2, **kwargs):
            p1, p2 = np.asarray(p1), np.asarray(p2)
            rot = rotation_between_vectors(RIGHT, p2 - p1)
            txt = Text(text, **kwargs)
            txt.points.apply_matrix(rot)
            txt.points.shift(p1 - txt[0].get_mark_orig())
            return txt

        txts_vert = Group.from_iterable(
            get_text_by_two_point(
                '顶点',
                p1, p2,
                font_size=16
            )
            for p1, p2 in [
                ([-2.73, -0.86, 0], [-2.54, -0.43, 0]),
                ([-1.17, 0.29, 0], [-0.83, 0.48, 0]),
                ([0.79, -1.5, 0], [0.97, -1.93, 0]),
                ([2.71, 0, 0], [3.09, 0.29, 0]),
                ([5.18, -0.21, 0], [5.39, -0.64, 0])
            ]
        )

        txts_color = Group.from_iterable(
            get_text_by_two_point(
                '颜色',
                p1, p2,
                font_size=16,
                color=[RED, GREEN, BLUE, RED, GREEN, BLUE]
            )
            for p1, p2 in [
                ([-2.12, -1.78, 0], [-1.54, -1.45, 0]),
                ([-0.41, -0.71, 0], [0.1, -0.88, 0]),
                ([-0.05, -2.91, 0], [0.4, -2.81, 0]),
                ([3.33, -1.57, 0], [3.59, -1.36, 0]),
                ([5.11, -1.62, 0], [5.39, -1.79, 0]),
                ([4.52, -2.93, 0], [4.95, -2.93, 0])
            ]
        )

        txt_texture = Text(f'纹理\n{s1}Texture{s2}', font_size=36, format=Text.Format.RichText)
        txt_texture.points.arrange(DOWN)

        ############################################################

        self.play(
            Write(txts_vert)
        )
        self.play(
            Write(txts_color)
        )
        self.play(
            Uncreate(txts_vert),
            Uncreate(txts_color),
            FadeOut(dots, at=0.4),
            DrawBorderThenFill(txt_texture, at=0.7)
        )

        self.forward()


class Intro2(Template):
    def construct(self) -> None:
        ############################################################

        face1 = Square(
            4,
            fill_color=GREY_B,
            fill_alpha=1
        )
        face1.points.shift(OUT * 2)
        face2 = face1.copy()
        face2.points.rotate(-PI / 2, axis=UP, about_point=ORIGIN)
        face3 = face1.copy()
        face3.points.rotate(PI / 2, axis=RIGHT, about_point=ORIGIN)
        faces = Group(face1, face2, face3)
        face1.depth.set(-1)

        wall = ImageItem('wall.jpg', depth=-1, height=4)

        ############################################################

        self.forward()
        self.play(FadeIn(wall))
        self.play(
            wall.anim.points.shift(OUT * 2)
                .rotate(-PI / 2, axis=UP, about_point=ORIGIN),
            self.camera.anim.points.scale(2)
                .rotate(60 * DEGREES, axis=RIGHT, absolute=True)
                .rotate(-70 * DEGREES, axis=OUT, absolute=True),
            FadeIn(faces)
        )
        self.play(
            self.camera.anim.points.scale(0.25).shift(IN + UP * 0.3)
        )
        self.forward()


typ1_src = '''
#set text(font: "Noto Sans S Chinese")
#set par(first-line-indent: 2em)
#set page(width: 38em)
#par[#box[]]
除了图像以外，纹理也可以被用来储存大量的数据，这些数据可以发送到着色器上，但是这不是我们现在的主题。
'''


class Intro3(TextDisplayTemplate):
    typ_src = typ1_src
    write_duration = 1
    stay_duration = 1.5


class DynamicTriTextureRenderer(ImageItemRenderer):
    def init(self) -> None:
        super().init()
        self.vbo_points.orphan(3 * 3 * 4)
        self.vbo_texcoords.orphan(3 * 2 * 4)

        self.prev_texcoord = None

    def render(self, item: DynamicTriTexture) -> None:
        new_texcoord = item.texcoord._points.data
        new_color = item.color._rgbas.data
        new_points = item.points._points.data

        if new_texcoord is not self.prev_texcoord:
            self.vbo_texcoords.write(new_texcoord[:, :2].tobytes())
            self.prev_texcoord = new_texcoord

        if new_color is not self.prev_color:
            color = resize_with_interpolation(new_color, 4)
            bytes = color.astype('f4').tobytes()

            assert len(bytes) == self.vbo_color.size

            self.vbo_color.write(bytes)
            self.prev_color = new_color

        if new_points is not self.prev_points:
            bytes = new_points.astype('f4').tobytes()

            assert len(bytes) == self.vbo_points.size

            self.vbo_points.write(bytes)
            self.prev_points = new_points

        if self.prev_img is None or item.image.img is not self.prev_img:
            self.texture = get_texture_from_img(item.image.get())
            self.texture.build_mipmaps()
            self.prev_img = item.image.img

        self.prog['image'] = 0
        self.texture.filter = item.image.get_filter()
        self.texture.use(0)
        self.update_fix_in_frame(item, self.prog)
        self.vao.render(mgl.TRIANGLES)


class DynamicTriTexture(ImageItem):
    renderer_cls = DynamicTriTextureRenderer

    texcoord = CmptInfo(Cmpt_Points[Self])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.points.set([DR, DL, UP]).stretch(1.2, dim=0)
        self.texcoord.set([
            [1.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.5, 1.0, 0.0],
        ])


code1_src = '''
<fc #9cdcfe>tex_coords</fc><fc #d4d4d4> = </fc><fc #4ec9b0>np</fc><fc #d4d4d4>.</fc><fc #dcdcaa>array</fc><fc #d4d4d4>([</fc>
    <fc #b5cea8>0.0</fc><fc #d4d4d4>, </fc><fc #b5cea8>0.0</fc><fc #d4d4d4>,   </fc><fc #6a9955># 左下角</fc>
    <fc #b5cea8>1.0</fc><fc #d4d4d4>, </fc><fc #b5cea8>0.0</fc><fc #d4d4d4>,   </fc><fc #6a9955># 右下角</fc>
    <fc #b5cea8>0.5</fc><fc #d4d4d4>, </fc><fc #b5cea8>1.0</fc>    <fc #6a9955># 上中</fc>
<fc #d4d4d4>], </fc><fc #9cdcfe>dtype</fc><fc #d4d4d4>=</fc><fc #ce9178>'f4'</fc><fc #d4d4d4>)</fc>
'''


class TexCoord(Template):
    def construct(self) -> None:
        ############################################################

        wall = ImageItem('wall.jpg', height=2)
        wall.points.shift(LEFT * 2.4).flip(axis=RIGHT)
        tri_wall = DynamicTriTexture('wall.jpg')

        txt1 = Text('纹理', color=LIGHT_BROWN)
        txt1.points.next_to(wall, DOWN, aligned_edge=LEFT)
        txt2 = Text('三角形', color=LIGHT_BROWN)
        txt2.points.next_to(tri_wall, DOWN, aligned_edge=LEFT) \
            .shift(RIGHT * 2.4)

        ############################################################

        self.forward()
        self.play(FadeIn(tri_wall, scale=2))
        self.play(
            tri_wall.anim.points.shift(RIGHT * 2.4),
            FadeIn(wall),
            AnimGroup(
                Write(txt1),
                Write(txt2),
                at=0.2
            )
        )

        ############################################################

        arrow = Arrow(wall, tri_wall, color=GREY)
        arrow_txt = arrow.create_text(
            f'映射<fs 0.7>(Map)</fs>',
            format=Text.Format.RichText,
            font_size=16,
            color=GREY
        )

        points_l = [
            wall.points.box.get(DR),
            wall.points.box.get(DL),
            wall.points.box.get(UP)
        ]

        top_x = ValueTracker(0.5)

        def tri_l_updater(p: UpdaterParams):
            rect = SurroundingRect(wall, buff=0)
            tri = Polygon(
                wall.points.box.get(DR),
                wall.points.box.get(DL),
                wall.get_orig()
                    + wall.get_horizontal_vect() * top_x.current().data.get()
                    + wall.get_vertical_vect()
            )
            return boolean_ops.Difference(
                rect,
                tri,
                **HighlightRect.difference_config_d
            )

        tri_l = tri_l_updater(None)

        dots_l = Group(
            *[

                Dot(
                    p,
                    fill_color=BLACK,
                    stroke_alpha=1,
                    stroke_radius=0.012,
                    radius=0.07
                )
                for p in points_l
            ],
            depth=-1
        )

        dots_r = Group(
            *[
                Dot(
                    p,
                    fill_color=BLACK,
                    stroke_color=GREY_B,
                    stroke_alpha=1,
                    stroke_radius=0.012,
                    radius=0.07
                )
                for p in tri_wall.points.get()
            ],
            depth=-1
        )

        line1 = VItem(
            [-1.35, -1, 0], [-0.95, -1.06, 0], [-0.5, -1.03, 0], [-0.05, -1.02, 0], [0.45, -0.91, 0],
            [0.96, -0.77, 0], [1.48, -0.59, 0], [2, -0.42, 0], [2.49, -0.31, 0], [3.04, -0.16, 0],
            [3.42, -0.17, 0], [3.69, -0.29, 0], [3.71, -0.55, 0], [3.77, -0.76, 0], [3.66, -1.02, 0],
        )
        line2 = VItem(
            [-3.38, -1.03, 0], [-3.08, -1.33, 0], [-2.71, -1.53, 0], [-2.31, -1.75, 0], [-1.92, -1.86, 0],
            [-1.57, -1.95, 0], [-1.24, -1.93, 0], [-0.86, -1.93, 0],
            [0.1, -1.5, 0], [0.46, -1.31, 0], [0.78, -1.17, 0], [1.05, -1.05, 0], [1.21, -1.02, 0],
        )
        line3 = VItem(
            [-2.38, 0.98, 0], [-2.06, 1.07, 0], [-1.64, 1.1, 0], [-1.19, 1.14, 0], [-0.69, 1.12, 0],
            [0.66, 0.98, 0], [0.98, 0.93, 0], [1.34, 0.89, 0],
            [1.69, 0.9, 0], [2.04, 0.91, 0], [2.38, 1, 0],
        )
        lines = Group(line1, line2, line3, alpha=[1, 0.2])
        line1.color.set(alpha=[1, 0.4, 0.2])
        for line, d1, d2 in zip(lines, dots_l, dots_r):
            line.points.put_start_and_end_on(d1.points.box.center, d2.points.box.center)

        ############################################################

        self.play(
            GrowArrow(arrow),
            DrawBorderThenFill(arrow_txt, at=0.2, duration=1.2)
        )
        self.play(
            Create(dots_r, lag_ratio=0.5)
        )
        self.play(
            Group(arrow, arrow_txt)(VItem).anim(duration=0.6)
                .color.fade(0.5),
            FadeIn(tri_l, duration=0.6),
            Create(dots_l, lag_ratio=0.2)
        )
        self.play(
            Create(lines, lag_ratio=0.2)
        )

        self.play(
            FadeOut(Group(lines, arrow, arrow_txt, tri_wall, txt2, dots_r, dots_l, tri_l)),
            self.camera.anim.points.move_to(wall).scale(0.8),
            txt1.anim(path_arc=-60 * DEGREES)
                .points.shift(UL * 4)
        )

        ############################################################

        box = wall.points.box

        axes = Axes(
            (0, 1.5),
            (0, 1.5),
            unit_size=2,
            axis_config=dict(
                include_tip=True,
                include_numbers=True,
            ),
            x_axis_config=dict(
                numbers_to_exclude=[]
            ),
            depth=-0.5
        )
        axes.points.shift(box.get(DL) - axes.c2p(0, 0))

        x = Typst('x')
        x.points.next_to(axes.x_axis.tip, buff=SMALL_BUFF)

        y = Typst('y')
        y.points.next_to(axes.y_axis.tip, UP, buff=SMALL_BUFF)

        dot1 = Dot(color=YELLOW, radius=0.05, depth=-0.6)
        dot1.points.move_to(box.get(DL))

        dot2 = Dot(color=YELLOW, radius=0.05, depth=-0.6)
        dot2.points.move_to(box.get(UR))

        cline1 = Polyline(box.get(DL), box.get(DR), box.get(UR), stroke_radius=0.05, color=YELLOW, depth=-0.6)
        cline2 = Polyline(box.get(DL), box.get(UL), box.get(UR), stroke_radius=0.05, color=YELLOW, depth=-0.6)

        ############################################################

        self.play(Write(axes, lag_ratio=0.05))

        self.play(
            Write(x),
            Write(y),
            lag_ratio=0.2
        )
        self.play(
            Indicate(
                Group(axes.x_axis.numbers, axes.y_axis.numbers),
                scale_factor=1.05
            )
        )
        self.play(
            FadeIn(dot1, show_at_end=False, duration=0.5, scale=0.1),
            AnimGroup(
                ShowCreationThenDestruction(cline1),
                ShowCreationThenDestruction(cline2)
            ),
            FadeOut(dot2, duration=0.5, scale=10),
            lag_ratio=0.95
        )
        self.play(
            FadeIn(tri_l),
            FadeIn(dots_l),
            Group(self.camera, txt1).anim
                .points.shift(RIGHT * 2)
        )

        self.play(
            Create(line3),
            FadeIn(tri_wall),
            lag_ratio=0.7
        )

        def tri_wall_updater(data: DynamicTriTexture, p: UpdaterParams):
            points = data.texcoord.get().copy()
            points[2, 0] = top_x.current().data.get()
            data.texcoord.set(points)

        def updater_anim(value: float):
            return AnimGroup(
                top_x.anim.data.set(value),
                ItemUpdater(
                    tri_l,
                    tri_l_updater
                ),
                DataUpdater(
                    dots_l[2],
                    lambda data, p: data.points.move_to(
                        wall.get_orig()
                            + wall.get_horizontal_vect() * top_x.current().data.get()
                            + wall.get_vertical_vect()
                    )
                ),
                DataUpdater(
                    line3,
                    lambda data, p: data.points.put_start_and_end_on(
                        dots_l[2].current().points.box.center,
                        dots_r[2].points.box.center
                    )
                ),
                DataUpdater(
                    tri_wall,
                    tri_wall_updater
                )
            )

        self.play(
            updater_anim(0)
        )
        self.play(
            updater_anim(1)
        )
        self.play(
            updater_anim(0.5)
        )
        tri_l.become(tri_l_updater(None))

        self.play(
            CircleIndicate(dots_l[1], rate_func=there_and_back_with_pause),
            CircleIndicate(dots_r[1], rate_func=there_and_back_with_pause),
        )
        self.play(
            CircleIndicate(dots_l[0], rate_func=there_and_back_with_pause),
            CircleIndicate(dots_r[0], rate_func=there_and_back_with_pause),
        )
        self.play(
            CircleIndicate(dots_l[2], rate_func=there_and_back_with_pause),
            CircleIndicate(dots_r[2], rate_func=there_and_back_with_pause),
        )
        self.play(
            FadeOut(txt1)
        )
        self.play(
            self.camera.anim.points.shift(UP * 1.5).scale(1 / 0.8)
        )

        ############################################################

        code1 = Text(
            code1_src,
            font_size=16,
            format=Text.Format.RichText
        )
        code1_sur = SurBox(code1, '数据')
        code1_g = Group(code1, code1_sur)
        code1_g.points.shift(UL * 4)

        glvert = Text('#    #\n#    #', font_size=20)
        glvert_sur = SurBox(glvert, '顶点着色器')
        glvert_g = Group(glvert, glvert_sur)
        glvert_g.points.next_to(code1_g, buff=2)

        glfrag = Text('#    #\n#    #', font_size=20)
        glfrag_sur = SurBox(glfrag, '片段着色器')
        glfrag_g = Group(glfrag, glfrag_sur)
        glfrag_g.points.next_to(glvert_g, buff=2)

        arrow1 = Arrow(code1, glvert, buff=0.5, color=BLUE)
        arrow2 = Arrow(glvert, glfrag, buff=0.5, color=BLUE)

        arrow2_txt = arrow2.create_text('片段插值', font_size=14)

        ############################################################

        self.play(
            Write(code1_g, duration=1.5)
        )
        self.play(
            GrowArrow(arrow1),
            Write(glvert_g, at=0.4)
        )
        self.play(
            FadeIn(arrow2_txt, scale=0.8)
        )
        self.play(
            GrowArrow(arrow2),
            Write(glfrag_g, at=0.4)
        )
        self.forward()


class TexSettings(Template):
    def construct(self) -> None:
        boxes = Group.from_iterable(
            Group(
                Rect(3, 0.7),
                Text(text)
            )
            for text in [
                '纹理环绕方式',
                '纹理过滤',
                '多级渐远纹理'
            ]
        ).show()
        boxes.points.arrange(DOWN)

        stat = boxes.copy()

        self.forward()
        for box in boxes:
            self.play(
                box(VItem).anim.color.set(YELLOW),
                Group.from_iterable(
                    b for b in boxes if b is not box
                )(VItem)
                    .anim.color.fade(0.5),
                duration=0.6
            )
            self.forward()
            self.play(
                boxes.anim.become(stat),
                duration=0.6
            )
        self.forward()



class CustomImgRenderer(ImageItemRenderer):
    shader_path = ''

    def init(self) -> None:
        assert self.shader_path
        self.prog = get_custom_program(self.shader_path)

        self.ctx = self.data_ctx.get().ctx
        self.vbo_points = self.ctx.buffer(reserve=4 * 3 * 4)
        self.vbo_color = self.ctx.buffer(reserve=4 * 4 * 4)
        self.vbo_texcoords = self.ctx.buffer(
            data=np.array([
                [-2.0, -2.0],     # 左上
                [-2.0, 3.0],     # 左下
                [3.0, -2.0],     # 右上
                [3.0, 3.0]      # 右下
            ], dtype='f4')
        )

        self.vao = self.ctx.vertex_array(self.prog, [
            (self.vbo_points, '3f', 'in_point'),
            (self.vbo_color, '4f', 'in_color'),
            (self.vbo_texcoords, '2f', 'in_texcoord')
        ])

        self.prev_points = None
        self.prev_color = None
        self.prev_img = None


class ImgRepeatRenderer(CustomImgRenderer):
    shader_path = 'shaders/image_repeat'


class ImgMirroredRepeatRenderer(CustomImgRenderer):
    shader_path = 'shaders/image_mirrored_repeat'


class ImgClampRenderer(CustomImgRenderer):
    shader_path = 'shaders/image_clamp'


class ImgBorderRenderer(CustomImgRenderer):
    shader_path = 'shaders/image_border'


class DynamicTriTextureRenderer2(DynamicTriTextureRenderer):
    def init(self) -> None:
        self.prog = get_custom_program('shaders/image_repeat')

        self.ctx = self.data_ctx.get().ctx
        self.vbo_points = self.ctx.buffer(reserve=3 * 3 * 4)
        self.vbo_color = self.ctx.buffer(reserve=4 * 4 * 4)
        self.vbo_texcoords = self.ctx.buffer(reserve=3 * 2 * 4)

        self.vao = self.ctx.vertex_array(self.prog, [
            (self.vbo_points, '3f', 'in_point'),
            (self.vbo_color, '4f', 'in_color'),
            (self.vbo_texcoords, '2f', 'in_texcoord')
        ])

        self.prev_points = None
        self.prev_color = None
        self.prev_img = None

        self.prev_texcoord = None


code2_src = '''
<fc #9cdcfe>img</fc><fc #d4d4d4> = </fc><fc #4ec9b0>Image</fc><fc #d4d4d4>.</fc><fc #dcdcaa>open</fc><fc #d4d4d4>(</fc><fc #ce9178>'container.jpg'</fc><fc #d4d4d4>)</fc>
<fc #9cdcfe>texture</fc><fc #d4d4d4> = </fc><fc #9cdcfe>ctx</fc><fc #d4d4d4>.</fc><fc #dcdcaa>texture</fc><fc #d4d4d4>(</fc><fc #9cdcfe>img</fc><fc #d4d4d4>.</fc><fc #9cdcfe>size</fc><fc #d4d4d4>, </fc><fc #9cdcfe>components</fc><fc #d4d4d4>=</fc><fc #b5cea8>3</fc><fc #d4d4d4>, </fc><fc #9cdcfe>data</fc><fc #d4d4d4>=</fc><fc #9cdcfe>img</fc><fc #d4d4d4>.</fc><fc #dcdcaa>tobytes</fc><fc #d4d4d4>())</fc>

<fc #9cdcfe>texture</fc><fc #d4d4d4>.</fc><fc #9cdcfe>repeat_x</fc><fc #d4d4d4> = </fc><fc #569cd6>True</fc>
<fc #9cdcfe>texture</fc><fc #d4d4d4>.</fc><fc #9cdcfe>repeat_y</fc><fc #d4d4d4> = </fc><fc #569cd6>True</fc>
'''

code3_src = '''
<fc #d4d4d4>.</fc><fc #9cdcfe>repeat_x</fc><fc #d4d4d4> = </fc><fc #569cd6>False</fc>
<fc #d4d4d4>.</fc><fc #9cdcfe>repeat_y</fc><fc #d4d4d4> = </fc><fc #569cd6>False</fc>
'''


class TexRepeat(Template):
    def construct(self) -> None:
        ############################################################

        mdl = PixelImageItem('madeline.png', height=4)

        mdl1 = mdl.copy()
        mdl1.depth.set(1)
        mdl1.points.scale(5)
        # mdl1.color.fade(0.6)
        mdl1.renderer_cls = ImgRepeatRenderer

        mdl2 = mdl1.copy()
        mdl2.renderer_cls = ImgMirroredRepeatRenderer

        mdl3 = mdl1.copy()
        mdl3.renderer_cls = ImgClampRenderer

        mdl4 = mdl1.copy()
        mdl4.renderer_cls = ImgBorderRenderer

        mdl5 = mdl1.copy()
        mdl5.renderer_cls = ImageItemRenderer

        plane = NumberPlane(
            (-2, 4),
            (-2, 2),
            unit_size=4,
            axis_config=dict(
                include_numbers=True,
            ),
            y_axis_config=dict(
                numbers_to_exclude=[0]
            ),
            faded_line_ratio=2,
            depth=-0.5
        )
        lines = Group(plane.faded_lines, plane.background_lines)
        plane.points.shift(mdl.points.box.get(DL) - plane.c2p(0, 0))

        ques = Text('?', font_size=60, font='LXGW WenKai Lite')

        quesg = Group.from_iterable(
            ques.copy()
                .points.shift(v * 3.5)
                .r
            for v in [
                LEFT, RIGHT, UP, DOWN,
                UL, UR, DL, DR
            ]
        )

        txts = Group.from_iterable(
            Text(
                text,
                stroke_background=True,
                stroke_color=BLACK,
                stroke_alpha=1,
                stroke_radius=0.04,
                font_size=30,
            )
            for text in [
                'GL_REPEAT',
                'GL_MIRRORED_REPEAT',
                'GL_CLAMP_TO_EDGE',
                'GL_CLAMP_TO_BORDER'
            ]
        )

        ############################################################

        self.forward()

        self.play(
            FadeIn(mdl, scale=1.2),
            FadeIn(Group(*plane.get_axes()))
        )
        self.play(
            DrawBorderThenFill(quesg, duration=1.5),
            self.camera.anim.points.scale(1.2)
        )

        ############################################################

        r1 = HighlightRect(
            Rect(DL * 2, UR * 2),
            self.camera,
            fill_alpha=0.7
        )
        r2 = HighlightRect(
            Rect(DR * 2 + RIGHT * 4, UL * 2 + RIGHT * 4),
            self.camera,
            fill_alpha=0.7
        )

        ############################################################

        self.play(
            FadeOut(quesg, duration=0.6),
            FadeIn(mdl1),
            FadeIn(txts[0], UP),
            FadeIn(lines)
        )
        # self.play(
        #    mdl1.anim.color.set(alpha=1)
        # )
        # self.play(
        #    mdl1.anim.color.set(alpha=0.4)
        # )
        self.play(
            FadeTransform(mdl1, mdl2),
            FadeOut(txts[0], UP),
            FadeIn(txts[1], UP)
        )
        self.play(
            FadeIn(r1)
        )
        self.play(
            Transform(r1, r2)
        )
        self.play(
            FadeOut(r2)
        )
        self.play(
            FadeTransform(mdl2, mdl3),
            FadeOut(txts[1], UP),
            FadeIn(txts[2], UP),
            FadeOut(lines)
        )
        self.play(
            FadeTransform(mdl3, mdl4),
            FadeOut(txts[2], UP),
            FadeIn(txts[3], UP)
        )
        self.play(
            FadeOut(txts[3], scale=0.8, duration=0.3),
            FadeIn(txts[0], scale=0.5),
            FadeTransform(mdl4, mdl1),
            FadeIn(lines)
        )

        ############################################################

        tri_mdl = DynamicTriTexture('madeline.png')
        tri_mdl.renderer_cls = DynamicTriTextureRenderer2
        tri_mdl.points.shift(RIGHT * 7).scale(1.6)
        tri_mdl.texcoord.set([
            [1.0, 1.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.5, 0.0, 0.0]
        ])

        right_x = ValueTracker(1.0)

        def tri_l_updater(p: UpdaterParams):
            rect = SurroundingRect(mdl, buff=0)
            tri = Polygon(
                mdl.get_orig()
                    + mdl.get_horizontal_vect() * right_x.current().data.get()
                    + mdl.get_vertical_vect(),
                mdl.points.box.get(DL),
                mdl.points.box.get(UP),
            )
            return Group(
                boolean_ops.Difference(
                    rect,
                    tri,
                    **HighlightRect.difference_config_d
                ),
                boolean_ops.Difference(
                    tri,
                    rect,
                    fill_alpha=0.3,
                    color=WHITE,
                    stroke_alpha=0
                )
            )

        tri_l = tri_l_updater(None)

        dot = Dot(
            fill_color=BLACK,
            stroke_alpha=1,
            stroke_radius=0.02,
            radius=0.1,
            depth=-2
        )

        def dot_updater(data: Dot, p: UpdaterParams):
            data.points.move_to(
                mdl.get_orig()
                    + mdl.get_horizontal_vect() * right_x.current().data.get()
                    + mdl.get_vertical_vect()
            )

        dot_updater(dot, None)

        line = VItem(
            [2.28, -2.48, 0], [3.04, -2.87, 0], [3.75, -3.02, 0], [4.44, -3.15, 0], [5.09, -3.08, 0],
            [5.8, -2.99, 0], [6.4, -2.81, 0], [6.93, -2.67, 0], [7.31, -2.5, 0], [7.71, -2.34, 0],
            [8.01, -2.15, 0],
            alpha=[1, 0.2]
        )

        def line_updater(data: VItem, p: UpdaterParams):
            data.points.put_start_and_end_on(
                dot.current().points.box.center,
                tri_mdl.points.get()[0]
            )

        line_updater(line, None)

        def tri_updater(data: DynamicTriTexture, p: UpdaterParams):
            points = data.texcoord.get().copy()
            points[0, 0] = right_x.current().data.get()
            data.texcoord.set(points)

        ############################################################

        self.play(
            Group(*plane.get_axes())(VItem)
                .anim.color.set(GREY),
            FadeOut(Group(lines, mdl1)),
            txts[0].anim.points
                .next_to(mdl, DOWN, aligned_edge=LEFT).scale(0.9),
            self.camera.anim.points.shift(RIGHT * 3),
            FadeIn(tri_mdl),
            FadeIn(tri_l),
            FadeIn(dot, at=0.3),
            Create(line, at=0.6)
        )
        self.play(
            right_x.anim.data.set(1.7),
            ItemUpdater(
                tri_l,
                tri_l_updater
            ),
            DataUpdater(
                dot,
                dot_updater
            ),
            DataUpdater(
                tri_mdl,
                tri_updater
            ),
            DataUpdater(
                line,
                line_updater
            ),
            duration=2
        )
        self.play(
            CircleIndicate(Dot([8.1, -0.41, 0]), buff=MED_LARGE_BUFF, rate_func=there_and_back_with_pause),
            CircleIndicate(Dot([2.38, -0.37, 0]), buff=MED_LARGE_BUFF, rate_func=there_and_back_with_pause),
            duration=1.5
        )

        ###########################################################

        wrappings = Group.from_iterable(
            Group(
                ImageItem(f'texture_wrapping{i}.png', height=3),
                Text(text, font_size=18)
            ).points.arrange(DOWN, buff=SMALL_BUFF).r
            for i, text in enumerate([
                'GL_REPEAT',
                'GL_MIRRORED_REPEAT',
                'GL_CLAMP_TO_EDGE',
                'GL_CLAMP_TO_BORDER'
            ], start=1)
        )
        wrappings(VItem).set_stroke_background()
        wrappings.points.arrange().move_to(self.camera).shift(UP * 1.5)

        code2 = Text(
            code2_src,
            font_size=20,
            format=Text.Format.RichText
        )
        code2.points.next_to(wrappings, DOWN, buff=LARGE_BUFF)

        repeat_g = Group(
            code2[4][7:],
            code2[5][7:]
        )

        code3 = Text(
            code3_src,
            font_size=20,
            format=Text.Format.RichText
        )
        code3.points.next_to(wrappings[2], DOWN, buff=MED_LARGE_BUFF)

        code4 = Text(
            '<fc #9cdcfe>ctx</fc><fc #d4d4d4>.</fc><fc #dcdcaa>sampler</fc>',
            font_size=20,
            format=Text.Format.RichText
        )
        code4.points.next_to(wrappings[3], DOWN, buff=MED_LARGE_BUFF)

        cross = SVGItem('cross.svg', height=1)
        cross.points.next_to(wrappings[1], DOWN, buff=MED_LARGE_BUFF)

        ###########################################################

        self.play(
            FadeOut(Group(*plane.get_axes(), mdl, tri_mdl, dot, line, tri_l)),
            Transform(txts[0], wrappings[0][1]),
            FadeIn(wrappings[0][0], at=0.4),
            FadeIn(wrappings[1:], at=0.4)
        )
        self.play(
            Write(code2)
        )
        self.play(
            code2[:3](VItem).anim.color.fade(0.7),
            ShowPassingFlashAround(code2[4:], at=0.5)
        )
        self.play(
            FadeOut(code2[:3], duration=0.4),
            FadeOut(code2[4][:7], duration=0.4),
            FadeOut(code2[5][:7], duration=0.4),
            repeat_g.anim.points.next_to(wrappings[0], DOWN, buff=MED_LARGE_BUFF)
        )
        self.play(
            FadeTransform(
                repeat_g,
                Group.from_iterable(Group(*line) for line in code3[1:-1]),
                hide_src=False,
                path_arc=40 * DEGREES
            )
        )
        self.play(
            ShowCreationThenDestructionAround(Group(wrappings[2], code3))
        )
        self.play(
            FadeIn(code4, UP)
        )
        self.play(
            FadeIn(cross, scale=0.8)
        )

        self.forward()


code5_src = '''
<fc #4ec9b0>mgl</fc><fc #d4d4d4>.</fc><fc #9cdcfe>NEAREST</fc>
<fc #4ec9b0>mgl</fc><fc #d4d4d4>.</fc><fc #9cdcfe>LINEAR</fc>
'''


class TexFilter(Template):
    def construct(self) -> None:
        ############################################################

        crow02 = PixelImageItem('crow02.png', height=2)

        axes = Axes(
            (0, 1.5),
            (0, 1.5),
            unit_size=2,
            axis_config=dict(
                include_tip=True,
                include_numbers=True,
            ),
            x_axis_config=dict(
                numbers_to_exclude=[]
            ),
            depth=-0.5
        )
        axes.points.shift(crow02.points.box.get(DL) - axes.c2p(0, 0))

        path = VItem(
            [-0.48, -0.28, 0], [-0.35, -0.41, 0], [-0.24, -0.4, 0], [-0.15, -0.33, 0], [-0.07, -0.24, 0],
            [0.06, -0.23, 0], [0.1, -0.31, 0], [0.03, -0.44, 0], [-0.05, -0.55, 0], [-0.02, -0.61, 0],
            [0.09, -0.55, 0], [0.17, -0.47, 0], [0.21, -0.34, 0], [0.22, -0.25, 0], [0.14, -0.16, 0],
        )

        dot = Dot(
            path.points.get_start(),
            fill_color=BLACK,
            stroke_alpha=1,
            stroke_radius=0.012,
            radius=0.07,
            depth=-1
        )

        ############################################################

        self.forward()
        self.play(
            FadeIn(crow02, scale=1.2),
            Write(axes, lag_ratio=0.05),
            FadeIn(dot, scale=0.5, at=0.6)
        )
        self.play(
            MoveAlongPath(dot, path)
        )

        ############################################################

        def current_pixel_pos() -> tuple[float, float]:
            pos = dot.current().points.box.center
            return crow02.point_to_pixel(pos)

        def pixel_updater(data: Rect, p: UpdaterParams):
            pixel_pos = current_pixel_pos()
            data.points.next_to(crow02.pixel_to_point(*pixel_pos), DR, buff=0)

        pixel = Rect(
            crow02.pixel_to_point(0, 0),
            crow02.pixel_to_point(1, 1),
            stroke_radius=0.002,
            color=YELLOW
        )
        pixel_updater(pixel, None)

        ############################################################

        self.play(
            self.camera.anim.points.move_to(dot).scale(0.2).shift(RIGHT * 0.5 + DOWN * 0.25),
            dot.anim.points.scale(0.2)
                .r.radius.set(0.002),
            FadeIn(pixel, scale=0.1)
        )

        ############################################################

        fr = FrameRect(self.camera, **HighlightRect.difference_config_d, depth=-10)

        methods = Text(
            code5_src,
            font_size=8,
            format=Text.Format.RichText,
            depth=-20
        )
        methods.points.arrange(DOWN).move_to(self.camera)

        ############################################################

        self.play(
            FadeIn(fr)
        )
        self.play(
            FadeIn(methods)
        )
        self.play(
            FadeOut(fr),
            FadeOut(methods[2]),
            methods[1].anim.points.scale(0.5).shift(UL * 0.4 + LEFT * 0.4)
        )

        ############################################################

        def large_pixel_updater(data: Square, p: UpdaterParams):
            pixel_pos = current_pixel_pos()
            data.fill.set(crow02.pixel_to_rgba(*pixel_pos)[:3])

        large_pixel = Square(
            0.5,
            stroke_radius=0.005,
            fill_alpha=1,
            color=YELLOW_E,
            depth=-1
        )
        large_pixel.points.next_to(self.camera)
        large_pixel_updater(large_pixel, None)

        def line_updater(data: Line, p: UpdaterParams):
            box = pixel.current().points.box
            y = clip(large_pixel.points.box.y,
                     box.get_y(DOWN),
                     box.get_y(UP))
            data.points.put_start_and_end_on(
                [box.get_x(RIGHT), y, 0],
                large_pixel.points.box.left
            )

        line = Line(color=[YELLOW, YELLOW_E], stroke_radius=[0.002, 0.005])
        line_updater(line, None)

        path = VItem(
            [0.14, -0.16, 0], [0.24, -0.12, 0], [0.27, -0.13, 0], [0.27, -0.16, 0], [0.23, -0.23, 0],
            [0.21, -0.29, 0], [0.16, -0.33, 0], [0.1, -0.38, 0], [0.05, -0.36, 0], [0.03, -0.3, 0],
            [0.05, -0.22, 0], [0.07, -0.17, 0], [0.14, -0.16, 0],
        )

        ############################################################

        self.play(
            Create(line),
            DrawBorderThenFill(large_pixel, duration=1.5)
        )
        self.play(
            MoveAlongPath(dot, path, rate_func=linear),
            DataUpdater(
                pixel,
                pixel_updater
            ),
            DataUpdater(
                large_pixel,
                large_pixel_updater
            ),
            DataUpdater(
                line,
                line_updater
            ),
            duration=4
        )

        ############################################################

        light = ImageItem('light.png', height=0.3)
        light.points.move_to(dot)

        def line_updater(data: Line, p: UpdaterParams):
            data.points.put_start_and_end_on(
                dot.current().points.box.center,
                large_pixel.points.box.left
            )

        def large_pixel_updater(data: Square, p: UpdaterParams):
            pos = dot.current().points.box.center
            x, y = crow02.point_to_pixel(pos)
            x += 0.5
            y += 0.5
            d = (-2, -1, 0, 1, 2)
            points = [
                (
                    crow02.pixel_to_point(x + dx, y + dy),
                    get_norm(crow02.pixel_to_point(x + dx, y + dy) - pos)
                )
                for dx, dy in it.product(d, d)
                if crow02.pixel_to_rgba(int(x + dx), int(y + dy))[-1] > 0.5
            ]
            points.sort(key=lambda p: p[1])

            weights = [
                math.exp(-600 * p[1]**2)
                for p in points
            ]

            total = sum(weights)

            color = np.sum(
                [
                    w * crow02.point_to_rgba(p[0])[:3]
                    for p, w in zip(points, weights)
                ],
                axis=0
            ) / total

            data.fill.set(color)

        def light_updater(data: ImageItem, p: UpdaterParams):
            data.points.move_to(dot.current())

        methods[2].points.move_to(methods[1]).scale(0.5)

        ############################################################

        self.play(
            FadeOut(pixel),
            FadeIn(light),
            line.anim.do(partial(line_updater, p=None)),
            large_pixel.anim.do(partial(large_pixel_updater, p=None)),
            FadeOut(methods[1], scale=0.8, duration=0.4),
            FadeIn(methods[2], scale=0.3)
        )
        self.play(
            MoveAlongPath(dot, path, rate_func=linear),

            DataUpdater(
                large_pixel,
                large_pixel_updater
            ),
            DataUpdater(
                line,
                line_updater
            ),
            DataUpdater(
                light,
                light_updater
            ),
            duration=4
        )
        self.play(
            FadeOut(Group(crow02, light, dot, line, large_pixel,
                          methods[2], axes))
        )

        self.forward()


class TexFilter2(Template):
    def construct(self) -> None:
        ############################################################

        filterings = Group(
            *[
                Group(
                    PixelImageItem(f'texture_filtering{i}.png', height=3.2),
                    Text(text)
                ).points.arrange(DOWN, buff=SMALL_BUFF).r
                for i, text in enumerate(
                    [
                        'mgl.NEAREST',
                        'mgl.LINEAR'
                    ],
                    start=1
                )
            ]
        )
        filterings.points.arrange()

        hl1 = Rect([0, 2.05, 0], [3.45, -2.18, 0], **HighlightRect.difference_config_d)
        hl2 = Rect([-3.51, 2.18, 0], [-0.06, -2.14, 0], **HighlightRect.difference_config_d)

        ############################################################

        self.forward()

        self.play(
            FadeIn(filterings, scale=1.2, lag_ratio=0.02)
        )
        self.play(
            FadeIn(hl1)
        )
        self.play(
            FadeOut(hl1),
            FadeIn(hl2)
        )
        self.play(
            FadeOut(hl2)
        )

        self.forward()


class TexFilter3(Template):
    def construct(self) -> None:
        ########################################################

        wall = ImageItem('wall.jpg', height=3)
        wall.points.to_border(LEFT).shift(RIGHT)

        txt_kwargs = dict(
            stroke_background=True,
            stroke_alpha=1,
            stroke_color=BLACK
        )

        txt = Text('原图', **txt_kwargs)
        txt.points.move_to(wall)

        wall1 = wall.copy()
        wall1.image.set(min_mag_filter=(mgl.NEAREST_MIPMAP_NEAREST, mgl.NEAREST))
        wall1.points.shift(RIGHT * 6 + UP * 3).scale(0.6, about_edge=DL)

        wall2 = wall.copy()
        wall2.image.set(min_mag_filter=(mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR))
        wall2.points.shift(RIGHT * 6 + DOWN * 1).scale(1.5, about_edge=UL)

        txt1 = Text('缩小', **txt_kwargs)
        txt1.points.move_to(wall1)

        txt2 = Text('放大', **txt_kwargs)
        txt2.points.move_to(wall2)

        arrow1 = Arrow(wall, wall1)
        arrow2 = Arrow(wall, wall2)

        atxt1 = arrow1.create_text('<fc #4ec9b0>mgl</fc><fc #d4d4d4>.</fc><fc #9cdcfe>NEAREST</fc>',
                                   format=Text.Format.RichText)
        atxt2 = arrow2.create_text('<fc #4ec9b0>mgl</fc><fc #d4d4d4>.</fc><fc #9cdcfe>LINEAR</fc>',
                                   format=Text.Format.RichText,
                                   under=True)

        ########################################################

        self.show(wall, txt)
        self.forward()
        self.play(
            FadeIn(wall1),
            Write(txt1)
        )
        self.play(
            GrowArrow(arrow1),
            Write(atxt1)
        )
        self.play(
            FadeIn(wall2),
            Write(txt2)
        )
        self.play(
            GrowArrow(arrow2),
            Write(atxt2)
        )

        ########################################################

        code = Text(
            '<fc #9cdcfe>texture</fc><fc #d4d4d4>.</fc><fc #9cdcfe>filter</fc><fc #d4d4d4> = (</fc><fc #4ec9b0>mgl</fc><fc #d4d4d4>.</fc><fc #9cdcfe>NEAREST</fc><fc #d4d4d4>, </fc><fc #4ec9b0>mgl</fc><fc #d4d4d4>.</fc><fc #9cdcfe>LINEAR</fc><fc #d4d4d4>)</fc>',
            format=Text.Format.RichText
        )

        ########################################################

        self.play(
            Transform(atxt1[0][:], code[0][18:29]),
            Transform(atxt2[0][:], code[0][31:41]),
            FadeIn(code[0][:18]),
            FadeIn(code[0][29:31]),
            FadeIn(code[0][41:]),
            FadeOut(Group(wall, wall1, wall2, arrow1, arrow2, txt, txt1, txt2))
        )
        self.play(
            ShowCreationThenDestruction(Underline(code[0][18:29], color=YELLOW))
        )
        self.play(
            ShowCreationThenDestruction(Underline(code[0][31:41], color=YELLOW))
        )
        self.forward()


class TexMipmap(Template):
    def construct(self) -> None:
        ###########################################################

        cam_orig = self.camera.copy()

        plane = NumberPlane(
            (-4, 5), (-4, 7),
            unit_size=1.5,
            faded_line_ratio=2
        )

        self.camera.anim.points \
            .rotate(75 * DEGREES, axis=RIGHT) \
            .rotate(20 * DEGREES, absolute=True)

        face1 = ImageItem('container.jpg', height=2)
        cube = Group(
            face1,
            *[
                face1.copy()
                    .points.apply_matrix(rotation_between_vectors(IN, v))
                           .shift(v + OUT)
                    .r
                for v in [LEFT, UP, RIGHT, DOWN, OUT]
            ]
        )
        cubes = cube * 6
        cubes.points.arrange_by_offset(DOWN * 7 + LEFT, center=False).set_y(14).set_x(-0.5)
        for i, cube in enumerate(reversed(cubes)):
            cube.points.shift(RIGHT * i**2 / 7)
        cubes.depth.arrange()

        rect1 = Rect([3.9, 2.6, 0], [4.68, 1.7, 0], color=YELLOW).fix_in_frame()
        rect2 = Rect([-5.8, 2, 0], [-3.1, -1.4, 0], color=YELLOW).fix_in_frame()
        hl1 = HighlightRect(rect1, buff=0).fix_in_frame()
        hl2 = HighlightRect(rect2, buff=0).fix_in_frame()

        cam_stat = self.camera.copy()

        ###########################################################

        self.forward()

        self.play(
            Write(plane, lag_ratio=0.05),
            FadeIn(cubes, at=1.2)
        )
        self.play(
            FadeIn(hl1),
            ShowCreationThenDestruction(rect1, duration=2)
        )
        self.play(
            FadeOut(hl1),
            FadeIn(hl2),
            ShowCreationThenDestruction(rect2, duration=2)
        )
        self.play(
            FadeOut(hl2)
        )
        self.play(
            FadeIn(hl1)
        )

        self.forward()


class TexMipmap2(Template):
    def construct(self) -> None:
        ###########################################################

        frame = ImageItem('TexMipmap.png').show()

        tex = Group(
            img := ImageItem('container.jpg'),
            SurroundingRect(img, buff=0, color=GOLD),

            rect := Rect(
                0.8, 0.4,
                fill_alpha=1,
                color=GOLD
            ).points.align_to(img, UL).r,

            Text('纹理', font_size=16)
                .points.move_to(rect).r
        )
        tex.points.shift(LEFT)

        ur_orig = np.array([4.02, 2.42, 0])
        ur_h = [4.6, 2.4, 0] - ur_orig
        ur_v = [3.96, 1.9, 0] - ur_orig

        u_tr = ValueTracker(0.4)
        v_tr = ValueTracker(0.6)

        def dl_updater(p=None):
            w, h = tex[0].image.img.size
            u = u_tr.current().data.get()
            v = v_tr.current().data.get()

            rect = Rect(
                tex[0].pixel_to_point(w * clip(u - 0.1, 0, 1),
                                      h * clip(v - 0.1, 0, 1)),
                tex[0].pixel_to_point(w * clip(u + 0.1, 0, 1),
                                      h * clip(v + 0.1, 0, 1)),
                fill_alpha=0.2
            )
            return rect

        dl = dl_updater()

        def line_updater(p=None):
            w, h = tex[0].image.img.size
            u = u_tr.current().data.get()
            v = v_tr.current().data.get()

            return Arrow(
                tex[0].pixel_to_point(w * clip(u + 0.1, 0, 1),
                                    h * clip(v - 0.1, 0, 1)),
                ur_orig + u * ur_h + v * ur_v,
                buff=0
            )

        line = line_updater()

        container_bad = ImageItem('container.jpg', height=3)
        container_bad.image.set(min_mag_filter=(mgl.NEAREST, mgl.LINEAR))
        container_bad.points.next_to(tex, buff=LARGE_BUFF)

        ###########################################################

        self.forward()

        self.play(
            FadeIn(tex[0], duration=0.7),
            Write(tex[1:])
        )
        self.play(
            Write(dl),
            Write(line)
        )
        self.play(
            u_tr.anim.data.set(0.7),
            v_tr.anim.data.set(0.2),
            ItemUpdater(dl, dl_updater),
            ItemUpdater(line, line_updater)
        )
        self.play(
            u_tr.anim.data.set(0.2),
            v_tr.anim.data.set(0.6),
            ItemUpdater(dl, dl_updater),
            ItemUpdater(line, line_updater)
        )
        self.play(
            u_tr.anim.data.set(0.7),
            v_tr.anim.data.set(0.7),
            ItemUpdater(dl, dl_updater),
            ItemUpdater(line, line_updater)
        )
        line.hide()
        line = line_updater()
        self.play(
            FadeOut(Group(line, dl)),
            FadeIn(container_bad)
        )
        self.play(
            container_bad.anim(rate_func=rush_from).points.scale(0.05),
            duration=3
        )
        self.play(
            FadeOut(Group(frame, container_bad))
        )

        ###########################################################

        txt_mipmap = Text('多\n级\n渐\n远\n纹\n理')
        txt_mipmap.points.to_border(UL, buff=LARGE_BUFF)
        txt_line = Line(ORIGIN, DOWN * 5)
        txt_line.points.next_to(txt_mipmap, buff=SMALL_BUFF, aligned_edge=UP)

        txt_mipmap_g = Group(txt_mipmap, txt_line, color=GOLD)

        img = tex[0]
        imgs1 = img * 8
        imgs1.points.scale(0.53).arrange(DOWN) \
            .next_to(txt_line, buff=MED_LARGE_BUFF, aligned_edge=UP)

        imgs2 = imgs1.copy()

        for img1, img2 in it.pairwise(imgs2):
            img2.points.set_width(img1.points.box.width / 2)
            img2.points.next_to(img1, DOWN, aligned_edge=LEFT)

        container = ImageItem('container.jpg')
        container.image.set(min_mag_filter=(mgl.LINEAR_MIPMAP_NEAREST, mgl.LINEAR))

        def redsur_updater(p=None):
            width = container.current().points.box.width

            use = None
            for img in imgs2:
                if img.points.box.width < width:
                    use = img
                    break

            assert use is not None

            return SurroundingRect(
                use,
                buff=0,
                color=RED
            )

        ###########################################################

        self.play(
            TransformMatchingShapes(tex[-1], txt_mipmap),
            FadeTransform(tex[1], txt_line, duration=2),
            FadeOut(tex[2])
        )
        self.play(
            Transform(Group(img), imgs1)
        )
        self.play(
            Transform(imgs1, imgs2)
        )
        self.show(container)

        self.prepare(
            ItemUpdater(None, redsur_updater),
            duration=5
        )

        self.forward()
        self.play(
            container.anim(rate_func=rush_from).points.scale(0.025),
            duration=4
        )
        redsur = redsur_updater().show()

        ###########################################################

        imgs3 = imgs2.copy()
        imgs3[1:].points.arrange(DOWN, buff=0, aligned_edge=LEFT)
        Group(imgs3[0], imgs3[1:]).points.arrange(buff=0)

        cover = Rect(
            [-6.32, 3.21, 0], [-3.03, -3.06, 0],
            **HighlightRect.difference_config_d
        )

        txt_mipmaps = Text(
            '<fc #9cdcfe>texture</fc><fc #d4d4d4>.</fc><fc #dcdcaa>build_mipmaps</fc><fc #d4d4d4>()</fc>',
            font_size=16,
            format=Text.Format.RichText
        )
        txt_mipmaps.points.next_to(imgs3, DOWN)

        ###########################################################

        self.play(
            FadeOut(redsur, duration=0.4),
            FadeOut(container, duration=0.4),
            Transform(imgs2, imgs3, path_arc=60 * DEGREES),
            FadeIn(cover, at=0.6, duration=0.3),
            FadeIn(imgs2, at=0.7, duration=0.5)
        )
        self.play(
            Write(txt_mipmaps)
        )

        ###########################################################

        height1 = imgs2[1].points.box.height + 0.05
        height2 = imgs2[1].points.box.height - 0.05
        container.points.set_height(height1)

        ###########################################################

        redsur = redsur_updater()
        self.play(
            FadeOut(Group(txt_mipmaps, cover, imgs3)),
            FadeIn(container),
            FadeIn(redsur)
        )
        self.prepare(
            ItemUpdater(
                redsur,
                redsur_updater
            ),
            duration=3
        )
        for _ in range(3):
            self.play(
                container.anim(duration=0.3).points.set_height(height2)
            )
            self.forward(0.2)
            self.play(
                container.anim(duration=0.3).points.set_height(height1)
            )
            self.forward(0.2)

        ###########################################################

        lmn = Text(
            '<fc #4ec9b0>mgl</fc><fc #d4d4d4>.</fc><fc #9cdcfe>LINEAR_MIPMAP_NEAREST</fc>',
            font_size=16,
            format=Text.Format.RichText
        )
        lmn.points.next_to(container, DOWN)

        lmn_part = lmn[0][:10].copy()
        lmn_part.points.next_to(container, DOWN)

        pbg = partial(
            SurroundingRect,
            buff=SMALL_BUFF / 2,
            stroke_alpha=0,
            fill_alpha=0.7,
            depth=10
        )

        bg1 = pbg(lmn[0][4:10], color=PURPLE)
        bg2 = pbg(Group(lmn[0][11:17], lmn[0][18:25]), color=MAROON)

        txt1 = Text('纹理内', font_size=12, color=PURPLE)
        txt1.points.next_to(bg1, DOWN, buff=MED_LARGE_BUFF)
        txt2 = Text('多级渐远纹理间', font_size=12, color=MAROON)
        txt2.points.next_to(bg2, DOWN, buff=MED_LARGE_BUFF)

        arrow1 = Arrow(txt1, bg1, buff=0.1, color=PURPLE)
        arrow2 = Arrow(txt2, bg2, buff=0.1, color=MAROON)

        ###########################################################

        self.play(
            Write(lmn_part)
        )
        self.play(
            Transform(lmn_part, lmn[0][:10]),
            FadeIn(lmn[0][10:], LEFT)
        )
        self.play(
            FadeIn(bg1, duration=0.7),
            GrowDoubleArrow(arrow1, start_ratio=1, at=0.5, duration=0.4, rate_func=rush_from),
            FadeIn(txt1, DOWN * 0.2, 1.2, at=0.3, duration=0.6),
        )
        self.play(
            FadeIn(bg2, duration=0.7),
            GrowDoubleArrow(arrow2, start_ratio=1, at=0.5, duration=0.4, rate_func=rush_from),
            FadeIn(txt2, DOWN * 0.2, 1.2, at=0.3, duration=0.6),
        )

        ###########################################################

        lml = Text(
            '<fc #4ec9b0>mgl</fc><fc #d4d4d4>.</fc><fc #9cdcfe>LINEAR_MIPMAP_LINEAR</fc>',
            font_size=16,
            format=Text.Format.RichText
        )
        lml.points.move_to_by_indicator(lml[0][10], lmn[0][10])

        container.image.set(min_mag_filter=(mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR))

        ###########################################################

        self.play(
            Destruction(lmn[0][18:], lag_ratio=0.2),
            Create(lml[0][18:], lag_ratio=0.2, at=0.3)
        )

        self.prepare(
            ItemUpdater(
                redsur,
                redsur_updater
            ),
            duration=2
        )
        for _ in range(2):
            self.play(
                container.anim(duration=0.3).points.set_height(height2)
            )
            self.forward(0.2)
            self.play(
                container.anim(duration=0.3).points.set_height(height1)
            )
            self.forward(0.2)

        self.forward()


typ2_src = R'''
#set page(fill: none)
#let center-box(body) = context {
  box(move(body, dy: measure(body).height / 2 - 0.5em))
}

#{
  show raw: set text(fill: rgb("#4ec9b0"))
  `mgl`
}.#center-box(
  box(
    fill: rgb("#9A72AC").transparentize(30%),
    inset: 2pt,
    width: 6.8em
  )[
    #set par(spacing: -0.3em)
    #set text(fill: rgb("#9cdcfe"))
    `NEAREST` \
    #set align(center)
    #move(dx: 3pt, dy: 2pt, text(fill: white)[\/]) \
    #set align(right)
    `LINEAR`
  ]
)`_`#center-box(
  box(
    fill: rgb("#C55F73").transparentize(30%),
    inset: 2pt,
    width: 13.6em
  )[
    #set par(spacing: -0.3em)
    #set text(fill: rgb("#9cdcfe"))
    `MIPMAP_NEAREST` \
    #set align(center)
    #move(dx: 2.5pt, dy: 2pt, text(fill: white)[\/]) \
    #set align(right)
    `MIPMAP_LINEAR`
  ]
)
'''

typ3_src = R'''
#{{
    show raw: set text(rgb("#4ec9b0"))
    `mgl`
}}.#{{
    set text(rgb("#9cdcfe"))
    highlight(
        fill: rgb("#9A72AC").transparentize(40%),
        extent: 1pt,
    )[`{}`]
    `_`
    highlight(
        fill: rgb("#C55F73").transparentize(40%),
        extent: 1pt,
    )[`{}`]
}}
'''

typ4_src = '''
#set text(font: "Noto Sans S Chinese", size: 0.8em, fill: luma(40%))
#set page(width: 44em)
#set par(first-line-indent: 2em)
#par(box())
一个常见的错误是，将放大过滤的选项设置为多级渐远纹理的选项之一。这样没有任何效果，因为多级渐远纹理主要是使用在纹理被缩小的情况下的，纹理放大不会使用多级渐远纹理。
'''


class TexMipmap3(Template):
    def construct(self) -> None:
        ##########################################################

        typ2 = TypstText(typ2_src)
        typ2.points.to_border(UP, buff=LARGE_BUFF)
        typ2.show()

        typs = Group(*[
            TypstText(typ3_src.format(a, f'MIPMAP_{b}'))
            for a, b in it.product(
                ('NEAREST', 'LINEAR'),
                ('NEAREST', 'LINEAR')
            )
        ])
        descs = Group(*[
            Text(text,
                 font_size=16,
                 format=Text.Format.RichText)
            for text in [
                '使用<c PURPLE>邻近插值</c>进行纹理内的采样；\n使用最<c MAROON>邻近</c>的多级渐远纹理级别',
                '使用<c PURPLE>线性插值</c>进行纹理内的采样；\n使用最<c MAROON>邻近</c>的多级渐远纹理级别',
                '使用<c PURPLE>邻近插值</c>进行纹理内的采样；\n在两个多级渐远纹理之间进行<c MAROON>线性插值</c>',
                '使用<c PURPLE>线性插值</c>进行纹理内的采样；\n在两个多级渐远纹理之间使用<c MAROON>线性插值</c>'
            ]
        ])

        typdescs = Group(*typs, *descs)
        typdescs.points.arrange_in_grid(4, aligned_edge=LEFT, v_buff=MED_LARGE_BUFF, fill_rows_first=False)
        # typdescs.show()

        setfilter1 = Text(
            '<fc #9cdcfe>texture</fc><fc #d4d4d4>.</fc><fc #9cdcfe>filter</fc><fc #d4d4d4> = (</fc><fc #4ec9b0>mgl</fc><fc #9cdcfe>.LINEAR, </fc><fc #4ec9b0>mgl</fc><fc #d4d4d4>.</fc><fc #9cdcfe>LINEAR</fc><fc #d4d4d4>)</fc>',
            format=Text.Format.RichText,
            font_size=16
        )
        setfilter1.points.next_to(typdescs, DOWN, buff=MED_LARGE_BUFF)

        setfilter2 = Text(
            '<fc #9cdcfe>texture</fc><fc #d4d4d4>.</fc><fc #9cdcfe>filter</fc><fc #d4d4d4> = (</fc><fc #4ec9b0>mgl</fc><fc #d4d4d4>.</fc><fc #9cdcfe>LINEAR_MIPMAP_LINEAR</fc><fc #d4d4d4>, </fc><fc #4ec9b0>mgl</fc><fc #d4d4d4>.</fc><fc #9cdcfe>LINEAR</fc><fc #d4d4d4>)</fc>',
            format=Text.Format.RichText,
            font_size=16
        )
        setfilter2.points.next_to(setfilter1, DOWN)

        setfilter3 = Text(
            '<fc #9cdcfe>texture</fc><fc #d4d4d4>.</fc><fc #9cdcfe>filter</fc><fc #d4d4d4> = (</fc><fc #4ec9b0>mgl</fc><fc #d4d4d4>.</fc><fc #9cdcfe>LINEAR_MIPMAP_LINEAR</fc><fc #d4d4d4>, </fc><fc #4ec9b0>mgl</fc><fc #d4d4d4>.</fc><fc #9cdcfe>LINEAR</fc><fc #d4d4d4>)</fc>',
            format=Text.Format.RichText,
            font_size=16
        )
        setfilter3.points.shift(UP * 1)

        typ4 = TypstDoc(typ4_src)
        typ4.points.next_to(setfilter3, DOWN, buff=MED_LARGE_BUFF)

        ##########################################################

        self.play(Write(typ2))

        self.forward(0.5)

        for typ, desc, (part1, part2) in zip(
            typs,
            descs,
            it.product(
                [typ2[5:12], typ2[13:19]],
                [typ2[21:35], typ2[36:49]]
            )
        ):
            rect1 = SurroundingRect(part1)
            rect2 = SurroundingRect(part2)
            self.show(rect1, rect2, typ, desc)
            self.forward(0.7)
            self.hide(rect1, rect2)

        self.play(
            Write(setfilter1, duration=1.3)
        )
        self.play(
            setfilter1.anim(duration=0.4).color.fade(0.5),
            Write(setfilter2, duration=1.3)
        )
        self.play(
            FadeOut(Group(typ2, typdescs, setfilter1), duration=0.8),
            Transform(setfilter2, setfilter3, duration=1.3)
        )
        self.play(
            FadeIn(typ4)
        )


if __name__ == '__main__':
    anim = TexFilter()


# if __name__ == '__main__':
#     anim = TexMipmap().build()
#     anim.anim_on(9.5)
#     anim.capture().save('2024/LearnOpenGL-9-Texture/assets/TexMipmap.png')
