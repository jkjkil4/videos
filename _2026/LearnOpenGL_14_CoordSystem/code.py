# ruff: noqa
# fmt: off
from __future__ import annotations

import sys

sys.path.append('.')

from janim.imports import *
from janim_url_assets.imports import Iconify

with reloads():
    from template import *
from template import *


class Review(Template):
    def construct(self) -> None:
        ##############################################

        imgs = [ImageItem(f'12_{i}.png', height=2) for i in range(1, 5)]
        imgs[0].points.set_height(4)
        Group(*imgs[1:]).points.arrange()

        surs = [SurroundingRect(item, buff=0, color=WHITE) for item in imgs[1:]]
        all = Group(*imgs[1:], *surs)

        all.generate_target().points.shift(UP * 0.3)

        txts = [Text(text, font_size=16) for text in ('缩放矩阵', '位移矩阵', '旋转矩阵')]
        for txt, sur in zip(txts, all.target[-3:]):
            txt.points.next_to(sur, DOWN, buff=SMALL_BUFF)

        ##############################################

        self.play(FadeIn(imgs[0]))
        self.play(
            FadeOut(imgs[0]),
            AnimGroup(
                *[
                    FadeIn(Group(img, sur))
                    for img, sur in zip(imgs[1:], surs)
                ],
                lag_ratio=0.5
            )
        )
        self.play(
            MoveToTarget(all),
            AnimGroup(
                *[
                    FadeIn(txt)
                    for txt in txts
                ],
                lag_ratio=0.5,
                at=0.4
            )
        )

        ##############################################


class Container3D(Group):
    def __init__(self):
        img = ImageItem('container.jpg', width=2, height=2)
        img.points.shift(OUT)

        imgs = [img]

        for dir in [IN, LEFT, RIGHT, UP, DOWN]:
            img2 = img.copy()
            img2.points.apply_matrix(rotation_between_vectors(OUT, dir))
            imgs.append(img2)

        super().__init__(*imgs)
        self.apply_depth_test()


class TL_1(Template):
    def construct(self) -> None:
        ##############################################

        plane = NumberPlane((-4, 4), (-4, 4), faded_line_ratio=1, depth=2)
        plane.points.shift(IN)

        con = Container3D()

        self.camera.points.set(orientation=quat(0.43, -0.19, -0.36, 0.8))

        ##############################################

        self.play(Create(plane, lag_ratio=0.02))
        self.play(
            *[
                FadeIn(item, shift=-item.points.box.center * 0.5)
                for item in con
            ]
        )

        ##############################################

        cam = Camera()
        cam.points.rotate(PI / 2, axis=RIGHT).scale(0.5)
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
        ).apply_depth_test()

        ##############################################
        # self.camera.become(cam)
        
        con.hide()
        self.camera.save_state('orig')
        self.camera.points.shift(DOWN)
        self.camera.save_state()
        self.camera.become(cam)

        self.play(FadeIn(con))
        self.play(
            self.camera.anim.load_state(),
            FadeIn(camitem, at=0.1, duration=0.2)
        )

        ##############################################

        def get_pointto(icon: str, text: str, next_to: Vect):
            svg = Iconify(icon, color=WHITE)
            txt = Text(text, font_size=10)
            arrow = Arrow(ORIGIN, DOWN)
            pointto = Group(svg, txt, arrow)
            pointto.points \
                .arrange(DOWN, buff=SMALL_BUFF) \
                .next_to(next_to, UP)
            pointto.save_state()
            pointto.points.face_to_camera(about_point=next_to)
            return pointto

        ascreen = get_pointto('at-icons/television-flat-screen', '画面', camitem[0].points.box.zenith)

        aeye = get_pointto('akar-icons/eye', '观察点', cam_loc)

        sample_img = ImageItem('sampleframe.png').apply_depth_test()
        sample_img.points \
            .move_to(camitem[0]) \
            .rotate(PI / 2, axis=RIGHT) \
            .set_width(camitem[0].points.box.width)

        ##############################################

        self.play(FadeIn(ascreen), FadeIn(aeye))
        self.play(Indicate(ascreen))

        ##############################################

        def map_to_cam(point: np.ndarray) -> np.ndarray:
            (x, y, depth), = info.map_points_with_depth([point])
            at_cam = info.center + x / 2 * info.horizontal_vect + y / 2 * info.vertical_vect
            return (at_cam - cam_loc) * scale_factor + cam_loc + UP * depth * 0.01

        con2 = con.copy()
        
        arrow = Arrow(UP * 2, DOWN * 3, color=GOLD)

        ##############################################

        self.play(
            GrowArrow(arrow),
            Do(con.hide),
            con2.anim.points.apply_point_fn(map_to_cam),
            FadeIn(sample_img, at=0.3),
        )
        self.play(
            FadeOut(arrow),
            FadeOut(sample_img),
            Do(con2.hide),
            FadeIn(con)
        )
        self.forward()

        ##############################################

        def get_frame_from_points(corners: np.ndarray):
            return Group(
                DotCloud(*corners),
                Group(
                    *[
                        Line(p1, p2, stroke_radius=0.01)
                        for p1, p2 in it.batched(corners, 2)
                    ],
                    *[
                        Line(p1, p2, stroke_radius=0.01)
                        for p1, p2 in it.batched(corners[[0, 2, 1, 3, 4, 6, 5, 7]], 2)
                    ],
                    *[
                        Line(p1, p2, stroke_radius=0.01)
                        for p1, p2 in it.batched(corners[[0, 4, 1, 5, 2, 6, 3, 7]], 2)
                    ],
                )
            )

        con_corners = np.array([
            [x, y, z]
            for x in [-1, 1]
            for y in [-1, 1]
            for z in [-1, 1]
        ])

        con_frame = get_frame_from_points(con_corners)

        def dotline_updater(p=None):
            corner = con_frame.current()[0].points.get()[1]

            dot = DotCloud(corner, color=YELLOW)
            line = Line(corner, cam_loc, color=YELLOW, depth=-1, stroke_radius=0.01).apply_depth_test()
            return Group(dot, line)

        dotline = dotline_updater()

        ##############################################

        camitem[0].set(fill_color=BLUE)
        self.play(
            FadeIn(con_frame[0]),
            Create(con_frame[1], at=0.3)
        )
        self.play(FadeOut(con), plane(VItem).anim.color.fade(0.5))
        self.play(FadeIn(dotline[0]))
        self.play(camitem[0].anim.set(fill_alpha=0.5), Create(dotline[1]))

        ##############################################

        def mapped_updater(p=None):
            cur = con_frame.current()
            points = cur[0].points.get()
            mapped_points = [map_to_cam(point) + DOWN * 0.01 for point in points]

            frame = get_frame_from_points(np.array(mapped_points))
            frame[0].radius.set(0.03)
            return frame

        mapped = mapped_updater()
        self.camera.save_state()

        ##############################################

        con_frame.apply_depth_test().set(depth=1)
        self.play(FadeIn(mapped))
        self.play(
            self.camera.anim(duration=3.5)
                .points.set(orientation=quat(0.58, -0.05, -0.08, 0.81)),
            ascreen.anim(duration=3.5)
                .points.shift(RIGHT * 0.7),
            Aligned(
                AnimGroup(
                    con_frame.update(duration=5).points.rotate(TAU, axis=UR),
                    con_frame.update(at=2, duration=3).points.rotate(TAU, axis=DR + IN),
                ),
                ItemUpdater(mapped, mapped_updater),
                ItemUpdater(dotline, dotline_updater),
                at=0.6,
            )
        )
        self.play(
            self.camera.anim.load_state(), 
            ascreen.anim.points.shift(LEFT * 0.7),
            duration=1.5
        )

        ##############################################

        arrow = Arrow(con_corners[1], mapped[0].points.get()[1], color=YELLOW)
        p1 = Dot([-0.75, 0.5, 0]).fix_in_frame()
        p2 = Dot([1.3, -0.6, 0]).fix_in_frame()

        ##############################################

        self.play(
            GrowArrow(arrow),
            dotline[1].anim.set(alpha=0.5)
        )
        self.play(
            CircleIndicate(p1, rate_func=there_and_back_with_pause, scale=1.3),
        )
        self.play(
            CircleIndicate(p2, rate_func=there_and_back_with_pause, scale=1.3),
        )
        ascreen.load_state()
        con_frame.apply_depth_test(False)
        sample_img.apply_depth_test(False)
        self.play(
            FadeOut(Group(dotline, aeye, arrow)),
            AnimGroup(
                FadeOut(con_frame),
                FadeIn(con),
                FadeOut(mapped),
                camitem[0].anim.set(fill_alpha=0),
                FadeIn(sample_img),
                FadeOut(ascreen[2]),
                self.camera.anim.points
                    .set(orientation=quat(0.5, -0.5, -0.5, 0.5))
                    .shift([-0.07, -1.08, -0.09])
                    .scale(0.8),
                GroupUpdater(
                    ascreen,
                    lambda group, p: group.points.face_to_camera(about_point=camitem[0].points.box.zenith),
                ),
                duration=1.7
            )
        )

        ##############################################

        icon = Iconify('carbon/z-axis', color=WHITE, height=0.4).fix_in_frame()
        txt_from = Text('『世界坐标』').fix_in_frame()
        txt_from.points.shift([-2.12, 2.55, 0])
        icon.points.next_to(txt_from, LEFT)

        txt_to = Text('『标准化设备坐标』').fix_in_frame()
        txt_to.points.shift([2.86, 2.55, 0])

        txt_to2 = Text('『裁剪坐标』').fix_in_frame()
        shift = txt_to2[0].offset_to(txt_to[0])
        txt_to2.points.shift(shift)

        arrow = Arrow(txt_from, txt_to, buff=(0.2, 0.9)).fix_in_frame()

        fr = FrameRect(**Rect.preset_shadow).fix_in_frame()

        img = ImageItem('sampleframe.png', height=2, depth=-10).fix_in_frame()
        img.points.shift([3.26, -0.87, 0])
        sur = SurroundingRect(img, buff=0, color=WHITE, depth=-10).fix_in_frame()
        p4, p2, p1, p3, _ = sur.points.get_anchors()

        curve1 = Polyline(p1, p2, p4, stroke_radius=0.07)
        curve2 = Polyline(p1, p3, p4, stroke_radius=0.07)
        dot1 = Dot(p1)
        dot2 = Dot(p4)

        Group(curve1, curve2, dot1, dot2, color=YELLOW, depth=-20).fix_in_frame()

        red = sur.copy().set(glow_color=RED, glow_alpha=0.5, glow_size=1, depth=-5)

        ##############################################

        self.play(
            FadeIn(icon),
            Write(txt_from),
        )
        self.play(
            GrowArrow(arrow),
            Write(txt_to)
        )
        self.play(
            FadeIn(Group(fr, img, sur)),
        )
        self.play(
            FadeIn(dot1, scale=0.1, hide_at_end=True, duration=0.6),
            AnimGroup(
                ShowPassingFlash(curve1),
                ShowPassingFlash(curve2),
            ),
            FadeOut(dot2, scale=10, duration=0.6),
            lag_ratio=0.8
        )
        self.play(
            FadeIn(red)
        )
        self.forward()
        self.play(
            FadeOut(red),
            FadeOut(Group(fr, img, sur), at=0.4)
        )
        self.play(
            TransformMatchingDiff(txt_to, txt_to2)
        )

        self.forward()


class TL_2(Template):
    def construct(self) -> None:
        ##############################################

        def get_coordbox(img_file: str, icon_name: str, text: str):
            img = ImageItem(img_file, height=2.4)
            icon = Iconify(icon_name, height=0.2, color=WHITE)
            txt = Text(text, font_size=16)

            icontxt = Group(icon, txt, depth=-10)
            icontxt.points.arrange(buff=SMALL_BUFF)

            txtsur = SurroundingRect(icontxt, stroke_alpha=0, fill_alpha=0.5, fill_color=BLUE)
            Group(txtsur, icontxt).points.align_to(img, UL)

            return Group(
                SurroundingRect(img, buff=0, color=BLUE),
                img,
                txtsur,
                icontxt, 
            )

        worldcoord = get_coordbox('worldcoord.png', 'carbon/z-axis', '世界坐标')
        clipcoord = get_coordbox('clipcoord.png', 'at-icons/television-flat-screen', '裁剪坐标')
        
        shader = Shadertoy(readall(find_file('shadertoy-MsdGWn.glsl'))).show()
        alphaeffect = AlphaEffect(shader).show()
        alphaeffect.alpha.set(0)
        center = RectClip(alphaeffect, anchor=ORIGIN, border=True, scale=0.5)
        center.points.set_size(5.4, 3.6)

        group = Group(worldcoord, center, clipcoord)
        group.points.arrange(buff=MED_LARGE_BUFF)

        back = Rect(fill_alpha=1, fill_color=BLACK, stroke_alpha=0, depth=5)
        back.points.replace(center, stretch=True)
        tip_kwargs = {'center_anchor': CenterAnchor.Front}
        arrow = Arrow(worldcoord, clipcoord, buff=0, color=GREY, tip_kwargs=tip_kwargs, depth=10)

        txt = Text('顶点着色器', font_size=18)
        txt.points.next_to(back, UP, buff=SMALL_BUFF)

        hl1 = HighlightRect(worldcoord)
        hl2 = HighlightRect(clipcoord)

        ##############################################

        self.show(worldcoord, clipcoord, arrow)

        self.forward()
        self.play(
            FadeIn(Group(back, center))
        )
        self.play(
            Write(txt)
        )
        self.play(
            Aligned(
                shader.anim_update(),
                Succession(
                    alphaeffect.anim.alpha.set(0.4),
                    Wait(2),
                    alphaeffect.anim.alpha.set(0)
                )
            )
        )
        self.play(FadeIn(hl1))
        self.play(
            FadeOut(hl1),
            FadeIn(hl2),
        )
        self.play(FadeOut(hl2))

        ##############################################

        viewcoord = get_coordbox('viewcoord.png', 'akar-icons/eye', '观察坐标')
        _Arrow = partial(Arrow, tip_kwargs=tip_kwargs, buff=0, color=BLUE)
        arrow1 = _Arrow(worldcoord, viewcoord)
        arrow2 = _Arrow(viewcoord, clipcoord)

        ##############################################

        self.play(
            FadeIn(viewcoord)
        )
        self.play(
            center.anim.set(stroke_alpha=0.5),
            GrowArrow(arrow1),
            GrowArrow(arrow2)
        )

        ##############################################

        txt1 = Text('转\n换')
        txt1.points.move_to(arrow1).shift(RIGHT * 0.2)
        txt2 = Text('转\n换')
        txt2.points.move_to(arrow2).shift(LEFT * 0.2)

        txt11 = Text('观\n察\n矩\n阵')
        txt11.points.move_to(txt1)
        txt22 = Text('投\n影\n矩\n阵')
        txt22.points.move_to(txt2)

        review = Group(
            ImageItem('Review.png'),
            FrameRect(**Rect.preset_shadow),
            Text('矩 阵', font_size=120, fill_alpha=0.5),
            depth=-20
        )

        ##############################################

        self.play(
            Write(txt1),
            Write(txt2)
        )
        self.play(
            Transform(txt1, txt11),
            Transform(txt2, txt22)
        )
        self.play(
            FadeIn(review)
        )
        self.play(
            FadeOut(review)
        )

        self.forward()


class TL_3(Template):
    def construct(self) -> None:
        ##############################################

        plane = NumberPlane((-4, 4), (-4, 4), faded_line_ratio=1, depth=2)
        plane.points.shift(IN)

        axes = ThreeDAxes(
            (-4, 4), (-4, 4), (-6, 4),
            axis_config={
                'include_tip': True,
            }
        ).apply_depth_test()

        labels = axes.get_axis_labels('x', 'y', 'z')
        Group(axes, labels).points.rotate(PI / 2, about_point=ORIGIN, axis=RIGHT)
        labels[1].points.shift(IN).scale(-1)

        con = Container3D()

        self.camera.points.set(orientation=quat(0.43, -0.19, -0.36, 0.8))

        cam = Camera()
        cam.points.set(orientation=quat(0.49, 0.24, 0.37, 0.75)).scale(0.5)
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
            Polygon(*cam_corners, fill_alpha=0.3, fill_color=BLUE),
            Group.from_iterable(
                (DashedLine(cam_loc, corner)
                for corner in cam_corners),
                color=GREY_B
            ),
        ).apply_depth_test()

        # eye = Group(
        #     Iconify('akar-icons/eye', color=WHITE),
        #     Text('观察点', font_size=10),
        #     Arrow(ORIGIN, DOWN),
        # )
        # eye.points.arrange(DOWN, buff=SMALL_BUFF).next_to(ORIGIN, UP, buff=SMALL_BUFF)

        ##############################################

        # self.show(camitem, plane, con)
        # self.hide(plane)
        # self.show(axes, eye)
        #
        # offset = -camitem.points.box.get_y(DOWN)
        # Group(camitem, con).points.shift(UP * offset)
        # self.camera.points.set(orientation=quat(0.43, -0.19, -0.36, 0.81))
        # self.camera.points.shift([-1.14, 1.43, 0.15])
        # eye.points.face_to_camera(about_point=ORIGIN, rotate=-30 * DEGREES)
        # self.forward()

        self.show(camitem, plane, con)

        self.camera.points.rotate(-20 * DEGREES)
        self.prepare(
            DataUpdater(
                self.camera,
                lambda data, p: data.points.rotate(5 * DEGREES * p.elapsed),
                duration=FOREVER
            )
        )

        ##############################################

        def get_coordname(icon_name: str, text: str):
            icon = Iconify(icon_name, height=0.2, color=WHITE)
            txt = Text(text, font_size=16)

            icontxt = Group(icon, txt)
            icontxt.points.arrange(buff=SMALL_BUFF)

            sur = SurroundingRect(icontxt, buff=(0.4, 0.1, 0.4, 0.1), fill_alpha=0.5, fill_color=BLUE, stroke_alpha=0)
            group = Group(sur, icontxt, depth=-20).fix_in_frame()
            group.points.to_border(UP)
            return group

        worldcoord = get_coordname('carbon/z-axis', '世界坐标')
        viewcoord = get_coordname('akar-icons/eye', '观察坐标')
        clipcoord = get_coordname('at-icons/television-flat-screen', '裁剪坐标')

        ##############################################

        self.show(worldcoord)
        
        ##############################################

        arrow = Arrow(info.camera_location, info.camera_location * 0.3, tip_kwargs={'center_anchor': CenterAnchor.Back}, color=BLUE).apply_depth_test()

        fr = normalize(-info.camera_axis)
        right = normalize(info.horizontal_vect)
        up = normalize(info.vertical_vect)
        mat_T = np.vstack([right, fr, up])

        ##############################################

        self.forward()

        self.play(
            FocusOn(Dot([3.34, 1.48, 0]).fix_in_frame()),
        )
        self.play(
            GrowArrow(arrow)
        )

        axes.save_state()
        axes.points.apply_matrix(mat_T.T).shift(info.camera_location)
        self.play(
            Group(camitem, con, arrow, plane).anim.points.shift(-info.camera_location).apply_matrix(mat_T),
            axes.anim(show_at_begin=False).load_state(),
            FadeOut(plane),
            FadeIn(axes, at=0.5, duration=0.5),
            Transform(worldcoord, viewcoord),
            FadeOut(arrow, at=0.7, duration=0.3),
            duration=3
        )
        cam.points.set(orientation=quat(1.0, 0.0, 0.0, 1.0)).shift(-cam.points.info.camera_location)

        ##############################################

        eye = Group(
            Iconify('akar-icons/eye', color=WHITE),
            Text('观察点', font_size=10, stroke_alpha=0.5, stroke_color=BLACK),
            Arrow(ORIGIN, DOWN),
        )
        eye.points.arrange(DOWN, buff=SMALL_BUFF).next_to(ORIGIN, UP, buff=SMALL_BUFF)
        
        ##############################################

        self.prepare(
            GroupUpdater(
                eye,
                lambda group, p: group.points.face_to_camera(about_point=ORIGIN),
                duration=FOREVER
            )
        )

        self.play(FadeIn(eye), FadeIn(labels))

        self.play(
            # 将 Group(camitem, eye) 的所有颜色都 mix YELLOW
            GroupUpdater(
                Group(camitem, eye),
                lambda group, p: group(VItem).color.mix(YELLOW, p.alpha),
                rate_func=there_and_back_with_pause,
                become_at_end=False
            ),
            # 但是 "观察点" 文字的 stroke 不要，抵消一下
            GroupUpdater(
                eye[1],
                lambda group, p: group.set(stroke_color=BLACK),
                become_at_end=False
            )
        )
        self.play(
            FocusOn(viewcoord)
        )

        ##############################################

        quest = Text('?', font_size=80)
        quest.points.rotate(PI / 2, axis=RIGHT).move_to(camitem[0])

        ##############################################

        self.play(
            Aligned(
                Succession(
                    FadeIn(quest),
                    Wait(),
                    FadeOut(quest),
                ),
                DataUpdater(camitem[0], lambda data, p: data.color.mix(YELLOW, p.alpha), rate_func=there_and_back_with_pause)
            )
        )

        ##############################################

        p1, p2, p3, p4, _ = camitem[0].points.get_anchors()
        p11, p22, p33, p44, _ = camitem[0].points.get_anchors() + UP * 6

        def get_proj_area(p1, p2, p3, p4, p11, p22, p33, p44):
            return Group(
                Polygon(p4, p44, p11, p1),
                Polygon(p3, p33, p44, p4),
                Polygon(p2, p22, p33, p3),
                Polygon(p1, p11, p22, p2),
                fill_alpha=0.5,
                fill_color=YELLOW,
                stroke_alpha=0,
                depth=-10
            )

        orth_area = get_proj_area(p1, p2, p3, p4, p11, p22, p33, p44)
        orth_area.generate_target()
        orth_area.points.stretch(0, dim=1, about_edge=DOWN)

        think = ImageItem('think.jpg', height=1.2).apply_depth_test()
        think.points.rotate(PI / 2, axis=RIGHT).shift(UP * 3)

        ##############################################

        camitem.set(depth=-1)
        self.play(
            FadeOut(eye),
            FadeOut(camitem[1]),
            self.camera.anim.points
                .set(orientation=quat(0.52, -0.16, -0.25, 0.8))
                .shift([0.0, 2.83, 0.06]),
            duration=2,
        )
        self.play(
            MoveToTarget(orth_area)
        )
        self.play(
            orth_area(VItem).anim.color.fade(0.7),
            FadeOut(con)
        )
        self.play(
            FadeIn(think)
        )

        ##############################################

        def get_proj_updater(points_fn, map_fn):
            def proj_updater(p=None):
                points = points_fn()
                mapped_points = [map_fn(point) for point in points]
                return Group(
                    DotCloud(*points, radius=0.03),
                    Group.from_iterable(
                        Line(p1, p2, stroke_radius=0.01)
                        for p1, p2 in zip(points, mapped_points)
                    ),
                    DotCloud(*mapped_points, radius=0.03),
                )
            
            return proj_updater

        def map_point_orth(point: np.ndarray):
            x, _, z = point
            y = camitem[0].points.box.get_y()
            return [x, y, z]

        orth_proj_updater = get_proj_updater(lambda: think.current().points.get()[[0, 1, 3, 2]], map_point_orth)
        orth_proj = orth_proj_updater()

        mapped_think_kwargs = dict(fill_color=GREY, fill_alpha=0.5, stroke_radius=0.015, depth=-1)
        mapped_think = Polygon(*orth_proj[-1].points.get(), **mapped_think_kwargs)

        ##############################################

        self.play(
            FadeIn(orth_proj[0]),
            AnimGroup(
                Create(orth_proj[1]),
            ),
            AnimGroup(
                FadeIn(orth_proj[2]),
                Create(mapped_think, auto_close_path=False)
            ),
            lag_ratio=1
        )
        self.play(
            think.anim.points.shift(UP * 4.2),
            ItemUpdater(orth_proj, orth_proj_updater),
            duration=3
        )

        ##############################################

        typ1 = TypstMath('(x,y,z)', depth=-20)
        typ1.points.rotate(PI / 2, axis=RIGHT).next_to(orth_proj[0], LEFT + OUT, buff=SMALL_BUFF)
        typ2 = TypstMath("(x',y')", depth=-20)
        typ2.points.rotate(PI / 2, axis=RIGHT).next_to(orth_proj[2], LEFT + OUT, buff=SMALL_BUFF)

        typ1.set(stroke_background=True)
        typ2.set(stroke_background=True, stroke_color=BLACK, stroke_alpha=0.5)

        ##############################################

        self.play(
            Write(typ1)
        )
        self.play(
            TransformMatchingDiff(typ1.copy(), typ2)
        )

        ##############################################

        def get_projbox(img_file: str, text: str):
            img = ImageItem(img_file, width=3, depth=-90)
            txt = Text(text, font_size=16, depth=-100)

            txtsur = SurroundingRect(txt, stroke_alpha=0, fill_alpha=0.5, fill_color=BLUE, depth=-90)
            Group(txtsur, txt).points.align_to(img, UL)

            return Group(
                SurroundingRect(img, buff=0, color=BLUE, depth=-90),
                img,
                txtsur,
                txt, 
            ).fix_in_frame()

        orthbox = get_projbox('Orth.png', '正射投影')
        orthbox.points.to_border(UL)

        shadow = FrameRect(**Rect.preset_shadow)
        shadow.set(fill_alpha=1)
        road = ImageItem('road.jpg')
        g = Group(shadow, road, depth=-100).fix_in_frame()

        ##############################################

        self.play(
            FadeIn(orthbox, DOWN)
        )
        self.play(
            FadeIn(g)
        )
        self.hide(orth_proj, typ1, typ2, orth_area, mapped_think, think)
        self.show(camitem[1], con)
        think.points.shift(DOWN * 4.2)
        self.play(
            FadeOut(g)
        )

        ##############################################

        p11, p22, p33, p44, _ = camitem[0].points.get_anchors() * 4

        pers_area = get_proj_area(p1, p2, p3, p4, p11, p22, p33, p44)

        info = cam.points.info
        cam_loc = info.camera_location

        def map_point_pers(point: np.ndarray):
            (x, y), = info.map_points([point])
            at_cam = info.center + x / 2 * info.horizontal_vect + y / 2 * info.vertical_vect
            return (at_cam - cam_loc) * scale_factor + cam_loc

        pers_proj_updater = get_proj_updater(lambda: think.current().points.get()[[0, 1, 3, 2]], map_point_pers)
        pers_proj = pers_proj_updater()

        def mapped_think_updater(p=None):
            points = think.current().points.get()[[0, 1, 3, 2]]
            mapped_points = [map_point_pers(point) for point in points]
            return Polygon(*mapped_points, **mapped_think_kwargs)

        mapped_think = mapped_think_updater()

        ##############################################

        self.play(
            Transform(get_proj_area(p1, p2, p3, p4, p1, p2, p3, p4), pers_area)
        )
        self.play(
            FadeOut(con),
            pers_area(VItem).anim.color.fade(0.7)
        )
        self.play(
            FadeIn(think)
        )

        self.play(
            FadeIn(pers_proj[0]),
            AnimGroup(
                Create(pers_proj[1]),
            ),
            AnimGroup(
                FadeIn(pers_proj[2]),
                Create(mapped_think, auto_close_path=False)
            ),
            lag_ratio=1
        )
        self.play(
            think.anim.points.shift(UP * 4.2),
            ItemUpdater(pers_proj, pers_proj_updater),
            ItemUpdater(mapped_think, mapped_think_updater),
            duration=3
        )
        self.play(
            Indicate(mapped_think, scale_factor=1),
            duration=2
        )

        ##############################################

        persbox = get_projbox('Pers.png', '透视投影')
        persbox.points.to_border(UR)
        
        shadow = FrameRect(**Rect.preset_shadow, depth=-85).fix_in_frame()
        boxes = Group(orthbox, persbox)

        ##############################################

        self.play(
            FadeIn(persbox, DOWN)
        )
        self.forward()
        self.play(
            FadeIn(shadow),
            boxes.anim.points.scale(1.5).arrange()
        )
        self.forward()
        self.play(
            FadeOut(orthbox, LEFT * 2),
            persbox.anim.points.to_center(),
            duration=2
        )
        self.play(
            FadeOut(shadow),
            FadeOut(persbox),
            think.anim.points.shift(DOWN * 3.2),
            ItemUpdater(pers_proj, pers_proj_updater),
            ItemUpdater(mapped_think, mapped_think_updater)
        )

        ##############################################

        _Plane = partial(Polygon, fill_alpha=0.5, stroke_alpha=0, fill_color=BLUE)
        plane1 = _Plane(p1, p2, p3, p4)
        plane2 = _Plane(p11, p22, p33, p44)

        txt = Text('平截头体', color=YELLOW, font_size=40).fix_in_frame()
        txt.points.shift([2.5, 1, 0])

        ##############################################

        self.camera.save_state()
        self.play(
            self.camera.anim.points
                .set(orientation=quat(0.33, -0.07, -0.21, 0.92))
                .scale(1.48)
                .shift([0.05, 0.67, 0.0])
        )
        self.play(
            FadeIn(plane1, scale=0.25),
            FadeOut(plane1, scale=4),
            lag_ratio=1,
        )
        self.play(
            FadeIn(plane2, scale=0.8),
            FadeOut(plane2, scale=1 / 0.8),
            lag_ratio=1,
        )
        self.play(
            Write(txt)
        )
        self.play(
            FadeOut(txt),
            self.camera.anim.load_state(),
            FadeOut(think),
            FadeOut(pers_proj),
            FadeOut(mapped_think),
            duration=2
        )

        ##############################################

        axes2 = axes.copy()
        labels2 = labels.copy()

        shift = camitem[0].points.box.center - axes2.get_origin()
        Group(axes2.z_axis, labels2[2]).points.scale(-1, about_point=axes2.get_origin())
        Group(axes2, labels2).points.shift(shift)
        axes2.z_axis.points.pointwise_become_partial(axes2.z_axis, 0.3, 1)
        removed_ticks = axes2.z_axis.ticks[:3].hide()
        axes2.z_axis.ticks.remove(*removed_ticks)

        p1234 = np.array([LEFT + IN, LEFT + OUT, RIGHT + OUT, RIGHT + IN]) + camitem[0].points.box.center
        clip_area = get_proj_area(*(p1234 + DOWN), *(p1234 + UP))

        ##############################################

        self.play(
            AnimGroup(
                Destruction(Group(axes, labels)),
                FadeOut(camitem),
            ),
            Create(Group(axes2, labels2)),
            AnimGroup(
                Transform(pers_area, clip_area),
                Transform(viewcoord, clipcoord),
                duration=2,
            ),
            lag_ratio=0.4
        )
        self.play(
            Transform(clip_area, pers_area),
            Transform(clipcoord, viewcoord),
        )
        self.play(
            Transform(pers_area, clip_area),
            Transform(viewcoord, clipcoord),
        )

        ##############################################

        shadow = FrameRect(**Rect.preset_shadow)
        how = Text('How?', font_size=120)
        g = Group(shadow, how, depth=-100).fix_in_frame()

        ##############################################

        self.play(
            FadeIn(g),
        )

        self.forward()


class TL_4(Template):
    def construct(self) -> None:
        ##############################################

        _Text = partial(Text, font_size=60)
        txt1 = _Text('投影矩阵')
        txt2 = _Text('透视除法')
        txts = Group(txt1, txt2)
        txts.points.arrange(buff=LARGE_BUFF)

        ##############################################

        self.forward()

        self.play(
            Write(txt1)
        )
        self.play(
            Write(txt2)
        )

        ##############################################

        mat = TypstMatrix(
            [
                [
                    Circle(0.25, fill_alpha=0.5, stroke_alpha=0)
                    for j in range(4)
                ]
                for i in range(4)
            ]
        ).show()
        mat(VItem).color.fade(0.5)

        vec1 = TypstMath('vec(x, y, z, 1)', scale=1.5)
        eq = TypstMath('=', scale=1.5)
        vec2 = TypstMath("vec(x', y', z', w')", scale=1.5)

        for sym, color in zip(['x', 'y', 'z'], [RED, GREEN, BLUE]):
            vec1[sym].set(color=color)
            vec2[sym + "'"].set(color=color)

        typs = Group(mat, vec1, eq, vec2)
        typs.points.arrange(buff=SMALL_BUFF)

        arrow = Arrow(vec1[10], vec2[13], path_arc=PI / 2, color=YELLOW)

        ##############################################

        self.play(
            FadeOut(txt2),
            txt1.anim.points.scale(0.6).move_to(mat),
            FadeIn(mat)
        )
        self.play(
            FadeIn(vec1)
        )
        self.play(
            Write(eq),
            FadeIn(vec2),
            lag_ratio=0.3
        )
        self.play(
            GrowArrow(arrow),
            ShowCreationThenDestructionAround(vec2[13:15]),
            lag_ratio=0.8
        )
        self.play(
            FadeOut(arrow)
        )

        ##############################################

        ref = ImageItem('PerspectiveRef.png', depth=10)
        vec2bg = SurroundingRect(vec2, **Rect.preset_shadow, depth=5)

        vec2group = Group(vec2bg, vec2)

        vec2_1 = TypstMath("vec(x' slash w', y' slash w', z' slash w', 1)")
        for sym, color in zip('xyz', [RED, GREEN, BLUE]):
            vec2_1[sym + "'"].set(color=color)
        vec2bg_1 = SurroundingRect(vec2_1, **Rect.preset_shadow, depth=5)

        vec2group_1 = Group(vec2bg_1, vec2_1)

        ##############################################

        self.play(
            FadeIn(ref),
            FadeOut(Group(txt1, mat, vec1, eq)),
            vec2group.anim.points.scale(0.6).shift([-4.31, 1.48, 0.0]),
            FadeIn(vec2bg),
        )
        vec2group_1.points.move_to(vec2)
        self.play(
            Transform(vec2bg, vec2bg_1, duration=2),
            TransformMatchingDiff(vec2, vec2_1)
        )
        txt2.points.scale(0.6)
        txt2.points.shift([-6.27, 1.56, 0.0])
        self.play(
            Write(txt2)
        )
        self.play(
            ShowCreationThenFadeAround(vec2_1[22])
        )
        self.play(
            ShowCreationThenFadeAround(Group(vec2_1[10:12], vec2_1[15:17], vec2_1[20:22]))
        )

        ##############################################

        ref2 = ImageItem('ClipRef.png', depth=10)

        coord1 = TypstMath('(-1.0, -1.0, -1.0)')
        coord2 = TypstMath('(1.0, 1.0, 1.0)')

        ##############################################

        self.play(
            FadeIn(ref2),
            FadeOut(Group(txt2, vec2group_1))
        )
        coord1.points.shift([1.41, -2.5, 0.0])
        coord2.points.shift([1.51, 1.4, 0.0])
        self.play(
            Write(coord1, duration=1),
            Write(coord2, duration=1),
            lag_ratio=0.4
        )

        self.forward()


class TL_5(Template):
    def construct(self) -> None:
        ##############################################

        plane = NumberPlane((-4, 4), (-4, 4), faded_line_ratio=1, depth=2)
        plane.points.shift(IN)

        axes = ThreeDAxes(
            (-4, 4), (-4, 4), (-6, 4),
            axis_config={
                'include_tip': True,
            }
        ).apply_depth_test()

        labels = axes.get_axis_labels('x', 'y', 'z')
        Group(axes, labels).points.rotate(PI / 2, about_point=ORIGIN, axis=RIGHT)
        labels[1].points.shift(IN).scale(-1)

        con = Container3D()

        self.camera.points.set(orientation=quat(0.43, -0.19, -0.36, 0.8))

        cam = Camera()
        cam.points.set(orientation=quat(0.49, 0.24, 0.37, 0.75)).scale(0.5)
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
            Polygon(*cam_corners, fill_alpha=0.3, fill_color=BLUE),
            Group.from_iterable(
                (DashedLine(cam_loc, corner)
                for corner in cam_corners),
                color=GREY_B
            ),
        ).apply_depth_test()

        ##############################################

        self.show(camitem, plane, con)

        self.camera.points.rotate(-20 * DEGREES)
        self.prepare(
            DataUpdater(
                self.camera,
                lambda data, p: data.points.rotate(5 * DEGREES * p.elapsed),
                duration=FOREVER
            )
        )

        ##############################################

        def get_coordname(icon_name: str, text: str):
            icon = Iconify(icon_name, height=0.2, color=WHITE)
            txt = Text(text, font_size=16)

            icontxt = Group(icon, txt)
            icontxt.points.arrange(buff=SMALL_BUFF)

            sur = SurroundingRect(icontxt, buff=(0.4, 0.1, 0.4, 0.1), fill_alpha=0.5, fill_color=BLUE, stroke_alpha=0)
            group = Group(sur, icontxt, depth=-20).fix_in_frame()
            return group

        worldcoord = get_coordname('carbon/z-axis', '世界坐标')
        viewcoord = get_coordname('akar-icons/eye', '观察坐标')
        clipcoord = get_coordname('at-icons/television-flat-screen', '裁剪坐标')

        coords = Group(worldcoord, viewcoord, clipcoord)
        coords.points.arrange().to_border(UP)
        coords.save_state()

        ##############################################

        def generate_state(idx: int, name: str):
            offset = coords[idx].points.box.get_x()
            coords.points.shift([-offset, 0, 0])

            indices = [0, 1, 2]
            indices.remove(idx)
            coords[indices](VItem).color.fade(0.5)
            
            coords.save_state(name)

        generate_state(0, 'world')
        coords.load_state()
        generate_state(1, 'view')
        coords.load_state()
        generate_state(2, 'clip')

        coords.load_state('world')

        self.show(coords)
        
        ##############################################

        arrow = Arrow(info.camera_location, info.camera_location * 0.3, tip_kwargs={'center_anchor': CenterAnchor.Back}, color=BLUE).apply_depth_test()

        fr = normalize(-info.camera_axis)
        right = normalize(info.horizontal_vect)
        up = normalize(info.vertical_vect)
        mat_T = np.vstack([right, fr, up])

        ##############################################

        self.forward()

        self.play(
            GrowArrow(arrow)
        )

        axes.save_state()
        axes.points.apply_matrix(mat_T.T).shift(info.camera_location)
        self.play(
            Group(camitem, con, arrow, plane).anim.points.shift(-info.camera_location).apply_matrix(mat_T),
            axes.anim(show_at_begin=False).load_state(),
            FadeOut(plane),
            FadeIn(axes, at=0.5, duration=0.5),
            coords.anim.load_state('view'),
            FadeOut(arrow, at=0.7, duration=0.3),
            duration=3
        )
        cam.points.set(orientation=quat(1.0, 0.0, 0.0, 1.0)).shift(-cam.points.info.camera_location)
        self.play(
            FadeIn(labels)
        )

        ##############################################

        p1, p2, p3, p4, _ = camitem[0].points.get_anchors()
        p11, p22, p33, p44, _ = camitem[0].points.get_anchors() * 4

        def get_proj_area(p1, p2, p3, p4, p11, p22, p33, p44):
            return Group(
                Polygon(p4, p44, p11, p1),
                Polygon(p3, p33, p44, p4),
                Polygon(p2, p22, p33, p3),
                Polygon(p1, p11, p22, p2),
                fill_alpha=0.5,
                fill_color=YELLOW,
                stroke_alpha=0,
                depth=-10
            )

        pers_area = get_proj_area(p1, p2, p3, p4, p11, p22, p33, p44)

        ##############################################

        self.play(
            self.camera.anim.points
                .set(orientation=quat(0.52, -0.16, -0.25, 0.8))
                .shift([0.0, 2.83, 0.06]),
            duration=2,
        )
        self.play(
            Transform(get_proj_area(p1, p2, p3, p4, p1, p2, p3, p4), pers_area)
        )

        ##############################################

        axes2 = axes.copy()
        labels2 = labels.copy()

        shift = camitem[0].points.box.center - axes2.get_origin()
        Group(axes2.z_axis, labels2[2]).points.scale(-1, about_point=axes2.get_origin())
        Group(axes2, labels2).points.shift(shift)
        axes2.z_axis.points.pointwise_become_partial(axes2.z_axis, 0.3, 1)
        removed_ticks = axes2.z_axis.ticks[:3].hide()
        axes2.z_axis.ticks.remove(*removed_ticks)

        def map_point_to_clip_approx(point: np.ndarray):
            x, y, z = point
            y1 = p1[1]
            y2 = p11[1]
            
            y_ratio = (y - y1) / (y2 - y1)
            p111 = p1 * (1 - y_ratio) + p11 * y_ratio
            p222 = p2 * (1 - y_ratio) + p22 * y_ratio
            p444 = p4 * (1 - y_ratio) + p44 * y_ratio
            
            x_ratio = (x - p111[0]) / (p444[0] - p111[0])
            z_ratio = (z - p111[2]) / (p222[2] - p111[2])

            return [
                -1 + 2 * x_ratio,
                -1 + 2 * y_ratio + y1,
                -1 + 2 * z_ratio,
            ]

        tip = Text('* 仅供演示，箱子坐标存在略微误差', font_size=14, color=GREY).fix_in_frame()
        tip.points.to_border(DL)

        ##############################################

        self.play(
            AnimGroup(
                Destruction(Group(axes, labels)),
                FadeOut(camitem),
            ),
            Create(Group(axes2, labels2)),
            AnimGroup(
                Group(con, pers_area).anim.points.apply_point_fn(map_point_to_clip_approx),
                coords.anim.load_state('clip'),
                duration=2,
            ),
            lag_ratio=0.4
        )
        self.play(
            self.camera.anim.points
                .set(fov=10, orientation=quat(1.0, 0.0, 0.0, 1.0)),
        )
        self.play(
            FadeIn(tip),
            Group(con, pers_area, axes2, labels2).anim.points.stretch(1.7, dim=0, about_point=ORIGIN),
        )
        self.forward()

        ##############################################

        shadow = FrameRect(**Rect.preset_shadow, depth=-100).fix_in_frame()
        code1 = Text('gl_Position = projection * view * vec4(in_point, 1.0);', depth=-100).fix_in_frame()

        ##############################################

        self.play(
            FadeOut(tip),
            FadeIn(shadow),
            Write(code1)
        )

        self.forward()
