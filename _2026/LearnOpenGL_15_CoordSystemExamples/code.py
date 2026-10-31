# ruff: noqa
# fmt: off
from __future__ import annotations

import sys

sys.path.append('.')

from janim.imports import *
from janim_url_assets.imports import Iconify
from template.audio import play_audio_with_subtitles, seq_play_audio_with_subtitles

with reloads():
    from template import *
from template import *


class TLTitle(TitleTemplate):
    str1 = 'Learn OpenGL'
    str2 = '坐标系统示例'


code1_src = R"""
# 模型矩阵 
model = glm.mat4(1)
model = glm.rotate(model, glm.radians(-55.0), glm.vec3(1.0, 0.0, 0.0))

# 观察矩阵 
view = glm.mat4(1)
# 注意，这里朝着我们期望移动的相反方向移动场景
view = glm.translate(view, glm.vec3(0.0, 0.0, -3.0))

# 透视矩阵
projection = glm.mat4(1)
projection = glm.perspective(glm.radians(45.0), screenWidth / screenHeight, 0.1, 100.0)
"""

code2_src = R"""
#version 330 core

in vec3 in_vert;
...
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main()
{
    // 注意乘法要从右向左读
    gl_Position = projection * view * model * vec4(in_vert, 1.0);
}
"""

code3_src = R"""
prog['model'].write(model.to_bytes())
prog['view'].write(view.to_bytes())
prog['projection'].write(projection.to_bytes())
"""

code4_src = R"""
# 顶点数据
vertices = np.array([
#   ----- 位置 -----   - 纹理坐标 -
    -0.5, -0.5, -0.5,  0.0, 0.0,
     0.5, -0.5, -0.5,  1.0, 0.0,
     0.5,  0.5, -0.5,  1.0, 1.0,
     0.5,  0.5, -0.5,  1.0, 1.0,
    -0.5,  0.5, -0.5,  0.0, 1.0,
    -0.5, -0.5, -0.5,  0.0, 0.0,

    -0.5, -0.5,  0.5,  0.0, 0.0,
     0.5, -0.5,  0.5,  1.0, 0.0,
     0.5,  0.5,  0.5,  1.0, 1.0,
     0.5,  0.5,  0.5,  1.0, 1.0,
    -0.5,  0.5,  0.5,  0.0, 1.0,
    -0.5, -0.5,  0.5,  0.0, 0.0,

    -0.5,  0.5,  0.5,  1.0, 0.0,
    -0.5,  0.5, -0.5,  1.0, 1.0,
    -0.5, -0.5, -0.5,  0.0, 1.0,
    -0.5, -0.5, -0.5,  0.0, 1.0,
    -0.5, -0.5,  0.5,  0.0, 0.0,
    -0.5,  0.5,  0.5,  1.0, 0.0,

     0.5,  0.5,  0.5,  1.0, 0.0,
     0.5,  0.5, -0.5,  1.0, 1.0,
     0.5, -0.5, -0.5,  0.0, 1.0,
     0.5, -0.5, -0.5,  0.0, 1.0,
     0.5, -0.5,  0.5,  0.0, 0.0,
     0.5,  0.5,  0.5,  1.0, 0.0,

    -0.5, -0.5, -0.5,  0.0, 1.0,
     0.5, -0.5, -0.5,  1.0, 1.0,
     0.5, -0.5,  0.5,  1.0, 0.0,
     0.5, -0.5,  0.5,  1.0, 0.0,
    -0.5, -0.5,  0.5,  0.0, 0.0,
    -0.5, -0.5, -0.5,  0.0, 1.0,

    -0.5,  0.5, -0.5,  0.0, 1.0,
     0.5,  0.5, -0.5,  1.0, 1.0,
     0.5,  0.5,  0.5,  1.0, 0.0,
     0.5,  0.5,  0.5,  1.0, 0.0,
    -0.5,  0.5,  0.5,  0.0, 0.0,
    -0.5,  0.5, -0.5,  0.0, 1.0,
], dtype='f4')
"""

code5_src = R"""
...
    model = glm.rotate(model, glfw.get_time(), glm.vec3(0.5, 1.0, 0.0))
...
"""


class Example1(Template):
    def construct(self) -> None:
        ##############################################

        # plane = NumberPlane((-4, 4), (-4, 4), faded_line_ratio=1)
        axes = ThreeDAxes((-4, 4), (-4, 4), (-3, 3), axis_config={'include_tip': True})
        labels = axes.get_axis_labels(rotate_xy=False)
        labels[-1].points.rotate(PI, about_point=ORIGIN)

        face = ImageItem('container.jpg', height=2)

        cam = Camera()
        cam.points.scale(0.5)
        info = cam.points.info

        cam_loc = info.camera_location
        cam_corners = [
            info.center + xs / 2 * info.horizontal_vect + ys / 2 * info.vertical_vect
            for xs in [-1, 1]
            for ys in [-1, 1]
        ]
        scale_factor = 0.4
        cam_corners = [
            (cam_corners[i] - cam_loc) * scale_factor + cam_loc
            for i in (0, 1, 3, 2)
        ]

        camitem = Group(
            Polygon(*cam_corners),
            Group.from_iterable(
                (DashedLine(cam_loc, corner)
                for corner in cam_corners),
                color=GREY_B
            ),
        )
        camitem.save_state()
        camitem.points.shift(-info.camera_location)

        Group(axes, face, camitem).apply_depth_test()

        code1 = Text(code1_src, font_size=14, render='pixel').fix_in_frame()
        code1.points.to_border(UL)

        parts = [code1[1:4], code1[5:9], code1[10:13]]

        ##############################################

        self.play(
            FadeIn(Group(axes, labels), duration=2),
            self.camera.anim(at=0.7, duration=1.5)
                .points.set(orientation=quat(0.44, -0.2, -0.36, 0.8)),
        )

        self.play(
            FadeIn(face)
        )

        self.play(
            face.update.points.rotate(-55 * DEGREES, axis=RIGHT),
            FadeIn(parts[0])
        )

        ##############################################

        arrow = Arrow(DL * 2, UL * 2, color=YELLOW).fix_in_frame()

        ##############################################

        self.play(
            FadeIn(camitem)
        )
        self.play(
            FadeIn(arrow),
            camitem.anim.load_state(),
        )

        self.play(
            Rotate(arrow, PI),
        )
        self.play(
            Group(camitem, face).anim.points.shift(-info.camera_location),
            FadeIn(parts[1]),
            FadeOut(arrow, at=0.4, duration=0.6)
        )

        self.play(
            FadeIn(parts[2])
        )

        ##############################################

        _Udl = lambda item: Underline(item, color=YELLOW).fix_in_frame()
        ul1 = _Udl(code1[12][75:78])
        ul2 = _Udl(code1[12][80:85])
        ul3 = _Udl(code1[12][29:46])

        ##############################################

        self.play(
            ShowCreationThenDestruction(ul1),
            ShowCreationThenDestruction(ul2),
            ShowCreationThenDestruction(ul3),
            lag_ratio=0.6
        )

        self.play(
            FadeOut(camitem, duration=0.6),
            self.camera.anim.points.reset().shift(-info.camera_location)
        )

        ##############################################

        def txtbox(text: str):
            txt = Text(text, depth=-5, color=BLUE)
            box = SurroundingRect(txt, depth=-2, fill_alpha=0.3, fill_color=BLUE_E, stroke_alpha=0)
            return Group(txt, box).fix_in_frame()

        txt1 = txtbox('模型矩阵')
        txt2 = txtbox('观察矩阵')
        txt3 = txtbox('透视矩阵')

        txts = Group(txt1, txt2, txt3)
        txts.points.arrange(DOWN, aligned_edge=LEFT).to_border(UL)

        ##############################################

        self.play(
            FadeTransform(parts[0], txt1),
            FadeTransform(parts[1], txt2),
            FadeTransform(parts[2], txt3),
            lag_ratio=0.5
        )

        ##############################################

        fr = FrameRect(**Rect.preset_shadow)

        code2 = Text(code2_src, depth=-5, font_size=18).fix_in_frame()

        ##############################################

        part = code2[12][46:]
        part.save_state()
        part.points.next_to(code2[12][:17], buff=SMALL_BUFF)

        self.play(
            FadeIn(fr)
        )
        self.play(
            Write(Group(code2[1:5], code2[9:11], code2[12][:17], code2[12][46:], code2[13])),
        )
        self.play(
            FadeIn(code2[5:9]),
            *[
                txt.anim(path_arc=50 * DEGREES).points.scale(0.7).next_to(line, LEFT, buff=SMALL_BUFF)
                for txt, line in zip(txts, code2[5:9])
            ]
        )
        self.play(
            part.anim.load_state()
        )
        self.play(
            Write(Group(*code2[12].children[17:46][::-1])),
            FadeIn(code2[11], duration=2),
        )

        ##############################################

        code2.generate_target()
        code2.target.points.scale(0.7).to_border(UL).shift(DOWN * 0.4)

        _Sur = partial(SurroundingRect, color=BLUE, fill_alpha=0.25)
        sur2 = _Sur(code2.target, depth=-4).fix_in_frame()

        code3 = Text(code3_src, depth=-5, font_size=18).fix_in_frame()
        code3.points.scale(0.7).next_to(code2.target, DOWN, aligned_edge=LEFT, buff=MED_LARGE_BUFF + 0.4)

        sur3 = _Sur(code3, depth=-4).fix_in_frame()

        txt2 = Text('顶点着色器', font_size=20).fix_in_frame()
        txt2.points.next_to(sur2, UP, aligned_edge=LEFT, buff=SMALL_BUFF).shift(RIGHT * 0.1)

        txt3 = Text('Python').fix_in_frame()
        txt3.points.next_to(sur3, UP, aligned_edge=LEFT, buff=SMALL_BUFF).shift(RIGHT * 0.1)

        ##############################################

        self.play(
            FadeOut(txts, UL),
            MoveToTarget(code2),
            Create(sur2, auto_close_path=False),
            FadeIn(txt2)
        )

        self.play(
            FadeIn(txt3),
            Create(sur3, auto_close_path=False),
            Write(code3)
        )

        self.play(
            FadeOut(Group(txt2, txt3, code2, code3, sur2, sur3, fr))
        )

        self.forward()


class Example2(Template):
    def construct(self) -> None:
        ##############################################

        code4 = Text(code4_src, render='pixel', font_size=18)
        code4.points.next_to(Config.get.bottom, DOWN).to_border(LEFT)
        code4.generate_target().points.next_to(Config.get.bottom, UP, buff=1, coor_mask=(0,1,0))

        txt = Group(
            Rect(Config.get.frame_width, 1.5)
                .stroke.set(alpha=0)
                .r.fill.set(GREY_E, 1)
                .r,
            Text('代码见简介', font_size=30)
        )

        ##############################################

        self.play(
            MoveToTarget(code4)
        )
        self.play(
            FadeIn(txt[0]),
            Write(txt[1])
        )

        ##############################################

        code4.generate_target().points.shift(UP * 3)
        code5 = Text(code5_src, font_size=18)
        code5.points.next_to(code4.target, DOWN, aligned_edge=LEFT, buff=1)

        ##############################################

        self.play(
            FadeOut(txt)
        )
        self.play(
            MoveToTarget(code4),
            Write(code5),
            lag_ratio=0.8
        )
        ul = Underline(code5[2][30:45], color=YELLOW)
        self.play(
            ShowCreationThenDestruction(ul)
        )

        self.forward()


class RenderCovering(Template):
    def construct(self) -> None:
        square1 = Square().show()
        square1.points.shift(OUT)
        square2 = square1.copy().show()
        square2.points.shift(IN * 2)

        lines = Group.from_iterable(
            Line(p1, p2)
            for p1, p2 in zip(square1.points.get_anchors()[:-1], square2.points.get_anchors()[:-1])
        ).show()

        g = Group(square1, square2, lines)

        img1 = Group(ImageItem('container.jpg'), ImageItem('awesomeface_b.png', alpha=0.2))
        img1.points.set_height(2)
        img1.points.shift(OUT)
        
        img2 = img1.copy()
        img2.depth.arrange()
        img2.points.shift(IN * 2)

        self.camera.points.set(orientation=quat(-0.01, -0.14, 0.23, 0.96))

        self.play(
            Create(g, auto_close_path=False)
        )
        self.play(
            FadeIn(img1)
        )
        self.play(
            FadeIn(img2)
        )


class IndicateDepthTest(Template):
    def construct(self) -> None:
        pass
