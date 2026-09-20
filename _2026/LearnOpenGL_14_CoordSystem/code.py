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
                .next_to(next_to, UP) \
                .face_to_camera(about_point=next_to)
            return pointto

        ascreen = get_pointto('at-icons/television-flat-screen', '画面', camitem[0].points.box.zenith)

        aeye = get_pointto('akar-icons/eye', '观察点', cam_loc)

        sample_frame = ImageItem('sampleframe.png').apply_depth_test()
        sample_frame.points \
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
            FadeIn(sample_frame, at=0.3),
        )
        self.play(
            FadeOut(arrow),
            FadeOut(sample_frame),
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
        con_group = Group(con, con_frame)

        def dotline_updater(p=None):
            corner = con_frame.current()[0].points.get()[1]

            dot = DotCloud(corner, color=YELLOW)
            line = Line(corner, cam_loc, color=YELLOW, depth=-1, stroke_radius=0.01).apply_depth_test()
            return Group(dot, line)

        dotline = dotline_updater()

        ##############################################

        camitem[0].set(fill_color=BLUE)
        self.play(Create(con_frame))
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
            )
        )
        self.forward()
