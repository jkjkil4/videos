# flake8: noqa
import sys
import random

sys.path.append('.')

from janim.imports import *

from utils.template import *


class OpenVideoFile(Template):
    def construct(self) -> None:
        #########################################################

        file = ImageItem('file.png')

        cursor = SVGItem('cursor.svg', height=1)
        cursor.points.shift(RIGHT * Config.get.frame_x_radius + DOWN * Config.get.frame_y_radius + RIGHT)

        def click():
            self.play(
                cursor.anim(rate_func=rush_into)
                    .points.scale(0.8, about_edge=UL),
                duration=0.1
            )
            self.play(
                cursor.anim(rate_func=rush_from)
                    .points.scale(1 / 0.8, about_edge=UL),
                duration=0.1
            )

        video = Video('pb_crop.mp4', height=6)

        #########################################################

        self.forward()
        self.play(FadeIn(file, DOWN, scale=2))
        self.forward()
        self.play(
            cursor.anim(path_arc=-60 * DEGREES)
                .points.to_center().shift(DR * 0.6 + DOWN * 0.2)
        )
        for _ in range(2):
            click()
            self.prepare(
                Flash(cursor.points.box.get(UL), rate_func=rush_from),
                duration=0.1
            )
        self.forward(0.3)

        video.seek(8.3)
        self.play(
            FadeIn(video, scale=3, rate_func=rush_from),
            duration=0.5
        )
        self.hide(file, cursor)
        video.start()
        self.forward(2)

        #########################################################

        circle = Circle(
            depth=100,
            stroke_alpha=0,
            fill_alpha=0.2,
            color=PURPLE
        ).show()

        video_files = [
            (RIGHT * 5, 'R_VID_20240807_172601.mp4'),
            (DL * 5, 'R_VID_20240807_172609.mp4'),
            (LEFT * 4.5 + UP * 4, 'R_VID_20240807_172622.mp4'),
            (DOWN * 9 + RIGHT * 0.5, 'R_VID_20240807_172634.mp4'),
            (UP * 9 + RIGHT * 2, 'R_VID_20240807_172645.mp4'),
            (LEFT * 10 + DOWN * 3, 'R_VID_20240807_172700.mp4'),
            (RIGHT * 10 + DOWN * 7.5, 'R_VID_20240807_172711.mp4'),
            (LEFT * 11 + UP * 5, 'R_VID_20240807_172736.mp4'),
            (RIGHT * 11 + UP * 1.5, 'R_VID_20240807_172745.mp4'),
            (RIGHT * 8 + UP * 9, 'R_VID_20240807_172753.mp4'),
            (LEFT * 5 + UP * 12, 'R_VID_20240807_172802.mp4'),
            (LEFT * 6.5 + DOWN * 13.5, 'R_VID_20240807_172817.mp4'),
            (RIGHT * 6 + DOWN * 10, 'R_VID_20240807_172827.mp4'),
        ]

        random.seed(114514)

        videos = Group(*[
            Video(file, width=4)
                .points.shift(shift).scale(0.2 * random.random() + 0.9).r
            for shift, file in video_files
        ]).show()

        for v in videos:
            v.start(speed=0.5)
        videos[2].start(speed=0.25)
        videos[3].start(speed=0.25)

        #########################################################

        self.play(
            Aligned(
                circle.anim.points.scale(17),
                self.camera.anim.points.scale(3),
                FadeIn(
                    videos,
                    lag_ratio=0.5
                )
            ),
            duration=3
        )
        self.forward()

        #########################################################

        hcircle = circle.copy()
        hcircle.depth.set(-10)
        hcircle.color.set(YELLOW_A, 1)

        #########################################################

        self.play(
            FadeIn(hcircle, rate_func=linear),
            rate_func=rush_into,
            duration=0.3
        )
        self.hide(videos, circle, video)
        self.play(
            hcircle.anim.points.scale(0.02).r.color.set(alpha=0),
            self.camera.anim.points.scale(1 / 3),
            FadeIn(file, at=0.7, duration=0.3),
            duration=0.8
        )
        self.forward()
        file.depth.set(-10)
        self.play(
            Flash(file, color=[PURPLE, PURPLE_A], flash_radius=1, line_length=0.5)
        )
        self.forward()


class Title(Template):
    def construct(self) -> None:
        txt1 = Text('视频是如何存储在你的设备里的')
        txt2 = Text('视频编码简述', font_size=80)
        g = Group(txt1, txt2)
        g.points.arrange(DOWN, aligned_edge=LEFT)

        def get_lines(count: int, length: float, color: JAnimColor) -> Group[Line]:
            lines = Line(ORIGIN, length * RIGHT, color=color) * count
            lines.points.arrange(DOWN)
            return lines

        lines1 = get_lines(3, 4, PURPLE)
        lines2 = get_lines(3, 3, PURPLE_E)
        g_lines = Group(lines1, lines2)
        g_lines.points.arrange(DOWN, aligned_edge=LEFT).to_border(UL, buff=0).shift(DOWN * 0.5)

        g_lines2 = g_lines.copy()
        g_lines2.points.rotate(PI).to_border(DR, buff=0).shift(UP * 0.5)

        self.forward()
        self.prepare(
            Write(g_lines),
            Write(g_lines2),
            at=1,
            duration=2
        )
        self.play(ShowIncreasingSubsets(txt1[0], duration=1.5))
        self.play(DrawBorderThenFill(txt2))
        self.forward()




class SimpleSolution(Template):
    def construct(self) -> None:
        #########################################################

        camera_stat = self.camera.store()

        frames = Group(*[
            Group(
                v := VideoFrame(
                    'example.mp4',
                    t,
                    height=Config.get.frame_height - 2,
                ),
                SurroundingRect(v, color=WHITE, buff=0),
                depth=t
            ).points.shift(i * IN).r
            for i, t in enumerate(np.linspace(0, 3, 30, endpoint=False))
        ]).show()

        txt = Text('玩耍中的舍友 →').show()
        txt.points.next_to(frames[0], LEFT)

        #########################################################

        self.forward()
        self.play(
            self.camera.anim.points.rotate(30 * DEGREES, axis=UP + LEFT * 0.2)
        )
        self.forward()
        self.play(
            *[
                frame.anim.points.shift(i * 0.95 * OUT)
                for i, frame in enumerate(frames)
            ],
            rate_func=rush_from
        )

        for frame in frames[:-1]:
            frame.hide()
            self.forward(0.1)

        self.forward()

        target = frames.copy()
        for frame in target:
            frame.points.to_center().scale(0.3)
            frame.points.apply_point_fn(
                lambda p: p + p[0] * 0.6 * DOWN
            )
        target.points.arrange(buff=-0.65)

        self.prepare(FadeOut(txt, duration=0.5))
        for frame in reversed(frames[:-1]):
            frame.show()
            self.forward(0.02)

        frame0_stat = frames[0].copy()

        self.play(
            self.camera.anim.restore(camera_stat),
            frames.anim.become(target)
        )
        self.forward()
        self.play(
            *[
                DataUpdater(
                    frame,
                    lambda data, p: data.points.shift(UP * there_and_back(p.alpha)),
                    become_at_end=False,
                    root_only=False
                )
                for frame in frames
            ],
            lag_ratio=0.1,
            duration=2
        )
        self.forward()

        self.play(frames[1:].anim.digest_styles(color=GREY))
        self.forward()
        self.play(frames[1:].anim.digest_styles(color=WHITE))
        self.forward(2)

        self.play(
            ItemUpdater(
                None,
                lambda p: Sector(radius=9,
                                 start_angle=PI / 2,
                                 angle=-(1 - p.alpha) * TAU,
                                 stroke_alpha=0,
                                 fill_alpha=rush_from(p.alpha * 6) * 0.5 if p.alpha < 1/6 else 0.5,
                                 color=PURPLE,
                                 depth=100),
                rate_func=linear
            ),
            duration=3
        )
        self.forward()

        #########################################################

        frame0_stat.points.scale(0.8).shift(LEFT * 2)
        # frame0_stat[0].image.set(min_mag_filter=(mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR))

        width = frame0_stat.points.box.width
        height = frame0_stat.points.box.height
        woffset = RIGHT * width / 2
        hoffset = DOWN * height / 2

        hline = Group(
            g := Group(
                Line(-woffset + DOWN * 0.2, -woffset + UP * 0.2),
                DoubleArrow(-woffset, woffset),
                Line(woffset + DOWN * 0.2, woffset + UP * 0.2)
            ),
            Text('1080').points.next_to(g[1], UP, buff=SMALL_BUFF).r
        )
        hline.points.next_to(frame0_stat, UP, buff=SMALL_BUFF)

        vline = Group(
            g := Group(
                Line(-hoffset + LEFT * 0.2, -hoffset + RIGHT * 0.2),
                DoubleArrow(-hoffset, hoffset),
                Line(hoffset + LEFT * 0.2, hoffset + RIGHT * 0.2)
            ),
            Text('1920').points.rotate(PI / 2).next_to(g[1], LEFT, buff=SMALL_BUFF).r
        )
        vline.points.next_to(frame0_stat, LEFT, buff=SMALL_BUFF)

        def growline(line, **kwargs):
            direction = normalize(line[0][1].points.start_direction)
            return AnimGroup(
                GrowDoubleArrow(line[0][1]),
                FadeIn(line[0][0], -direction, at=0.3, duration=0.7),
                FadeIn(line[0][2], direction, at=0.3, duration=0.7),
                Write(line[1], at=0.2, duration=0.8),
                **kwargs
            )

        #########################################################

        self.play(
            FadeOut(frames[1:]),
            Transform(frames[0], frame0_stat)
        )
        self.play(
            growline(vline),
            growline(hline, duration=0.75, rate_func=rush_from),
            lag_ratio=0.5
        )
        self.forward()

        #########################################################

        frame0R = frame0_stat.copy()
        frame0R.digest_styles(color=RED)
        frame0G = frame0_stat.copy()
        frame0G.digest_styles(color=GREEN)
        frame0B = frame0_stat.copy()
        frame0B.digest_styles(color=BLUE)

        frame0RGB = Group(frame0R, frame0G, frame0B).show()
        frame0RGB.depth.arrange(10)
        frame0RGB.points.scale(0.25).arrange(DOWN) \
            .next_to(frame0_stat, buff=-0.2)

        #########################################################

        self.play(FadeIn(frame0RGB, RIGHT))
        self.forward()

        #########################################################

        typ = Typst('1920 times 1080 times 3 times 8 "bit"')
        txts = Group(
            Text('= 49,766,400 bit'),
            Text('= 6,220,800 B'),
            Text('= 6075 KiB'),
            Text('= 5.93 MiB')
        )
        for txt in txts[1:]:
            txt.points.align_to(txts[0], LEFT)
            txt.points.shift(UP * (txts[0][0].get_mark_orig() - txt[0].get_mark_orig()))
        typtxt = Group(typ, txts)
        typtxt.points.arrange(DOWN, buff=LARGE_BUFF, aligned_edge=LEFT)
        typtxt.points.next_to(frame0_stat, aligned_edge=UP, buff=LARGE_BUFF)
        typtxt.points.shift(DOWN * 0.2)

        frames.points.scale(1.2, about_edge=LEFT).shift(DOWN * 0.6)

        desc1 = Text('像素尺寸', font_size=16, color=PURPLE_B)
        desc1.points.next_to(typ[:9], DOWN)

        desc2 = Text(
            '[<c RED>R</c><c GREEN>G</c><c BLUE>B</c>]',
            font_size=16,
            color=PURPLE_B,
            format=Text.Format.RichText
        )
        desc2.points.next_to(typ[9:11], DOWN)

        desc3 = Text('每种颜色使用\n8bit 二进制位的空间存储', font_size=16, color=PURPLE_B)
        desc3.points.next_to(typ[12:], DOWN, aligned_edge=LEFT)

        #########################################################

        self.play(
            Write(typ[:9]),
            Transform(
                Group(hline[1], vline[1]),
                Group(desc1),
                hide_src=False,
                path_arc=50 * DEGREES,
                at=0.5
            )
        )
        self.forward()
        self.play(
            Write(typ[9:11]),
            FadeTransform(frame0RGB, desc2, at=0.5)
        )
        self.forward()
        self.play(
            Write(typ[11:]),
            FadeIn(desc3, at=0.5),
        )
        self.forward()
        self.play(Write(txts[0]))
        self.forward()
        for txtp, txt in it.pairwise(txts):
            self.play(
                Uncreate(txtp),
                Create(txt),
                lag_ratio=0.5,
                duration=0.4
            )
        self.forward()

        typtxt = Group(typ, txts[-1])
        self.play(
            FadeOut(Group(hline, vline, desc1, desc2, desc3), duration=0.6),
            typtxt.anim.points.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
                .next_to(frames, UP, aligned_edge=LEFT),
            Transform(frame0_stat, frames[0]),
            FadeIn(frames[1:])
        )
        self.forward()

        #########################################################

        txt30fps = Text('每秒 30 帧')
        txt30fps.points.next_to(txt, buff=LARGE_BUFF)

        txt1min = Text('1 分钟')
        txt1min.points.next_to(txt30fps, buff=MED_LARGE_BUFF)

        arrow = Arrow(ORIGIN, RIGHT * 5.7, color=GREY, depth=1)
        arrow.points.next_to(txt)

        txtGB = Text('10.4 GiB')
        txtGB.points.next_to(arrow)

        #########################################################

        self.play(Write(txt30fps)),
        self.forward(0.5)
        self.play(Write(txt1min)),
        self.forward()
        self.play(
            GrowArrow(arrow),
            FadeIn(txtGB, scale=0.5, duration=0.6, at=0.4),
        )
        self.forward(0.5)
        self.play(
            ShowCreationThenFadeAround(
                txtGB,
                surrounding_rect_config=dict(
                    color=PURPLE
                )
            ),
            AnimGroup(
                *[
                    DataUpdater(
                        frame,
                        lambda data, p: data.points.shift(UP * 0.2 * there_and_back(p.alpha)),
                        become_at_end=False,
                        root_only=False
                    )
                    for frame in frames
                ],
                lag_ratio=0.1,
                duration=2
            )
        )
        self.forward(2)


class CompareToWechat(Template):
    def construct(self) -> None:
        #########################################################

        bg = Group(
            Circle(6, color='#1e1322', depth=100),
            Circle(3, color='#33213a', depth=5),
            stroke_alpha=0,
            fill_alpha=1
        ).show()

        txtGB = Text('10.4 GiB', font_size=56).show()
        wechat = SVGItem('wechat-fill.svg', height=1)
        txt_cnt = Text('x40', font_size=40)

        bottom = Group(wechat, txt_cnt)
        bottom.points.arrange()

        group = Group(txtGB, bottom)
        group.points.arrange(DOWN, buff=LARGE_BUFF).shift(DOWN * 0.2)

        txtGB_stat = txtGB.copy()
        txtGB.points.to_center()

        info = ImageItem('wechat-info.png', height=2, depth=100).show()

        Group(bg, txtGB, txtGB_stat, wechat, txt_cnt, bottom, info) \
            .points.shift(LEFT * 3)

        #########################################################

        self.forward()
        self.play(
            txtGB.anim.become(txtGB_stat),
            Write(bottom, at=0.4),
            info.anim(rate_func=rush_from)
                .points.shift(RIGHT * 6)
        )
        self.forward()


class TooLarge(Template):
    def construct(self) -> None:
        c = Circle(
            3,
            stroke_alpha=0,
            fill_alpha=0.3,
            fill_color=PURPLE_E
        ).show()
        g = Group(
            ImageItem('computer.png'),
            Text(': 请打开麦克风交流')
        ).show()
        g.points.arrange()


class Difference(Template):
    def construct(self) -> None:
        #########################################################

        bgl = Rect(
            Config.get.frame_width * 2, 2,
            stroke_alpha=0,
            fill_alpha=0.5,
            fill_color=PURPLE_E,
            depth=1000
        ).show()

        frames = Group(*[
            Group(
                v := VideoFrame(
                    'example.mp4',
                    t,
                    height=Config.get.frame_height - 2,
                ),
                SurroundingRect(v, color=WHITE, buff=0),
                depth=t
            ).points.shift(i * IN).r
            for i, t in enumerate(np.linspace(0, 3, 30, endpoint=False))
        ]).show()

        orig_frames = frames.copy()

        frame0 = frames[0].copy()
        frame0[0].depth.set(-20)
        frame0[1].color.set(PURPLE).r.depth.set(-21)
        frame1 = frames[1].copy()
        frame1[1].color.set(PURPLE).r.depth.set(-10)
        arrow = DoubleArrow(ORIGIN, RIGHT * 3, color=PURPLE)

        comp = Group(frame0, arrow, frame1)
        comp.points.arrange()

        txt0 = Text('前一帧', color=PURPLE_E, depth=-20)
        txt0.points.next_to(frame0.points.box.get(DL), UR, buff=SMALL_BUFF)
        txt1 = Text('后一帧', color=PURPLE_E, depth=-10)
        txt1.points.next_to(frame1.points.box.get(DL), UR, buff=SMALL_BUFF)

        think = ImageItem('think.png', width=1.5)
        think.points.next_to(arrow, UP)

        for frame in frames:
            frame.points.to_center().scale(0.3)
            frame.points.apply_point_fn(
                lambda p: p + p[0] * 0.6 * DOWN
            )
        frames.points.arrange(buff=-0.65).shift(RIGHT * Config.get.frame_width)

        diff = ImageItem('diff.jpg')
        diff.points.replace(frame1)

        tip = Text('这里仅作示意，不代表实际“差异算法”的效果', font_size=12, color=GREY)
        tip.points.next_to(frame1, UP, aligned_edge=LEFT)

        #########################################################

        self.forward()
        self.play(
            frames.anim(rate_func=rush_from)
                .points.shift(LEFT * Config.get.frame_width + RIGHT * 2.5),
            duration=0.7
        )
        self.forward()
        self.prepare(
            FadeIn(txt0),
            FadeIn(txt1),
            at=1
        )
        self.play(
            Transform(frames[0], frame0),
            Transform(frames[1], frame1),
            FadeOut(frames[2:]),
            duration=1.5
        )
        self.forward()
        self.play(
            GrowDoubleArrow(arrow),
            FadeIn(think, duration=3, at=0.5)
        )
        self.forward()
        self.play(
            *[
                ShowPassingFlash(
                    VItem(
                        *points,
                        points[0],
                        color=YELLOW,
                        depth=-20
                    ),
                    rate_func=linear
                )
                for i in range(4)
                for points in [np.roll(frame1[1].points.get()[:-1], i * 2, axis=0)]
            ],
            duration=1.5
        )
        self.forward()
        self.play(
            FadeIn(diff),
            txt1.anim.color.set(PURPLE),
            FadeIn(tip)
        )

        frame1[0].hide()
        frame1.remove(frame1[0])
        frame1.add(diff, insert=True)
        diff_cpy = diff.copy()
        diff_cpy.points.set(frames[1][0].points.get())
        depth = frames[1][0].depth.get()
        frames[1].remove(frames[1][0])
        frames[1].add(diff_cpy, insert=True)
        frames[1].depth.arrange(depth)

        self.forward()
        self.play(
            Indicate(
                diff,
                scale_factor=1,
                color=[3, 3, 3],
                rate_func=there_and_back_with_pause
            ),
            duration=1.5
        )
        self.forward()
        self.play(
            FadeOut(
                Group(think, arrow, tip, txt0, txt1)
            ),
            Transform(frame0, frames[0]),
            Transform(frame1, frames[1]),
            FadeIn(frames[2:])
        )
        self.forward()

        for frame in frames[2:]:
            self.play(
                frame.anim.points.shift(UP * 0.25),
                duration=0.1
            )
            frame[0].image.set(diff.image.get())
            t = self.prepare(
                frame.anim.points.shift(DOWN * 0.25),
                duration=0.1
            )

        self.forward()

        #########################################################

        frame_playback = orig_frames[0].copy()
        frame_playback.points.shift(LEFT * 2)
        frame_playback.depth.set(-100)

        #########################################################

        self.play(
            Group(bgl, frames).anim
                .points.rotate(-PI / 2).to_border(RIGHT, buff=LARGE_BUFF)
        )
        self.forward()
        self.play(
            Transform(frames[0], frame_playback)
        )
        self.forward()

        for i, (diff, orig) in enumerate(zip(frames[1:], orig_frames[1:]), start=2):
            self.play(
                diff[0].anim(rate_func=linear)
                    .points.set(frame_playback[0].points.get()),
                diff[1].anim(rate_func=linear)
                    .points.set(frame_playback[1].points.get()),
                rate_func=rush_into,
                duration=1 if i < 4 else 0.15
            )
            diff.hide()
            if i == 18:
                self.play(
                    frames[18:].anim.points.shift(UP * 5),
                    duration=0.6
                )
            frame_playback[0].image.set(orig[0].image.get())

        self.forward()


class Midway(Template):
    def construct(self) -> None:
        #########################################################

        bgl1 = Rect(
            Config.get.frame_width * 2, 2,
            stroke_alpha=0,
            fill_alpha=0.5,
            fill_color=PURPLE_E,
            depth=1000
        )

        diff = ImageItem('diff.jpg')

        frames = Group(*[
            Group(
                v := VideoFrame(
                    'example.mp4',
                    t,
                    height=Config.get.frame_height - 2,
                ),
                SurroundingRect(v, color=WHITE, buff=0),
                depth=t
            ).points.shift(i * IN).r
            for i, t in enumerate(np.linspace(0, 3, 30, endpoint=False))
        ])

        for frame in frames:
            frame.points.to_center().scale(0.3)
            frame.points.apply_point_fn(
                lambda p: p + p[0] * 0.6 * DOWN
            )
        frames.points.arrange(buff=-0.65).shift(RIGHT * 2.2)

        diff_frames = frames.copy()
        for frame in diff_frames[1:]:
            frame[0].image.set(diff.image.get())

        for frame in diff_frames:
            frame.depth.arrange(frame.depth.get() - 0.01)

        vect = LEFT * 12
        frames.points.shift(-vect)

        arrow = DoubleArrow(LEFT * 0.4, RIGHT * 0.4, path_arc=-PI)
        arrow.points.next_to(frames, UP, aligned_edge=LEFT, buff=SMALL_BUFF)
        arrow.points.shift(vect)

        #########################################################

        self.forward()
        self.play(
            FadeIn(bgl1),
            frames.anim(rate_func=rush_from).points.shift(vect),
            duration=1.5
        )
        self.play(
            FadeIn(arrow),
            duration=0.3
        )
        self.play(
            arrow.anim(rate_func=linear)
                .points.shift(-vect),
            ShowIncreasingSubsets(diff_frames),
            rate_func=rush_into
        )
        self.forward()


class Question(Template):
    def construct(self) -> None:
        Circle(
            2,
            stroke_alpha=0,
            fill_color=PURPLE_E,
            fill_alpha=0.5,
            stroke_radius=0.1
        ).show()
        Circle(
            6,
            color=PURPLE_E,
            stroke_alpha=0.4
        ).show()
        Text('?', font='Noto Sans S Chinese Medium', font_size=80).show()
