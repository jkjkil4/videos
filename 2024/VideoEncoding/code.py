# flake8: noqa
import sys

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

        rect = boolean_ops.Difference(
            FrameRect(),
            Rect(2, 1)
                .points.shift(DOWN * 1.8 + RIGHT * 0.55).r,
            stroke_alpha=0,
            fill_alpha=0.5,
            fill_color=BLACK
        )

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
        video.start()
        self.forward(1.5)
        video.stop()
        self.play(
            video.anim.points.scale(3, about_edge=DOWN)
        )
        self.play(FadeIn(rect))
        self.forward()
        self.play(FadeOut(rect))
        cursor.hide()
        self.play(
            video.anim.points.scale(1 / 3, about_edge=DOWN).shift(RIGHT * 3),
            file.anim.points.shift(LEFT * 3)
        )
        self.forward()

        #########################################################

        arrow = DoubleArrow(file, video, color=PURPLE)
        rect2 = FrameRect(
            stroke_alpha=0,
            fill_alpha=0.5,
            fill_color=BLACK
        )
        invent = SVGItem('invent.svg', height=3)

        #########################################################

        self.play(GrowDoubleArrow(arrow))
        self.forward()
        self.play(
            FadeIn(rect2),
            DrawBorderThenFill(invent, at=0.5)
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


typ1_src = '''
#{
    set text(fill: gray, size: 0.7em)
    [
        (yuv420p)
    ]
}
#v(-0.5em)
$1920 times 1080 times 1.5 = 3110400$
'''


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

        #########################################################

        frame0_stat.points.scale(0.8).shift(LEFT * 2)

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

        typ1 = TypstDoc(typ1_src)
        txt = Text('2.97 MB')
        typtxt = Group(typ1, txt)
        typtxt.points.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        typtxt.points.next_to(frame0_stat, aligned_edge=UP)

        frames.points.scale(1.2, about_edge=LEFT).shift(DOWN * 0.6)

        #########################################################

        self.play(
            FadeIn(typ1[:9]),
            Write(typ1[9:])
        )
        self.forward()
        self.play(FadeIn(txt, scale=0.5))
        self.forward()
        self.play(
            FadeOut(Group(hline, vline), duration=0.6),
            typtxt.anim.points.align_to(frames, LEFT),
            Transform(frame0_stat, frames[0]),
            FadeIn(frames[1:])
        )
        self.forward()

        #########################################################

        txt30fps = Text('每秒 30 张')
        txt30fps.points.next_to(txt, buff=LARGE_BUFF)

        txt1min = Text('1 分钟')
        txt1min.points.next_to(txt30fps, buff=MED_LARGE_BUFF)

        arrow = Arrow(ORIGIN, RIGHT * 5.7, color=GREY, depth=1)
        arrow.points.next_to(txt)

        txtGB = Text('5.2 GB')
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


class TooLarge(Template):
    def construct(self) -> None:
        #########################################################

        bg = Group(
            Circle(5),
            Circle(3),
            stroke_alpha=0,
            fill_alpha=0.3,
            fill_color=PURPLE_E,
            depth=100
        ).show()

        txtGB = Text('5.2 GB', font_size=60).show()
        qq = SVGItem('QQ.svg', height=1)
        txt_cnt = Text('x28', font_size=40)

        bottom = Group(qq, txt_cnt)
        bottom.points.arrange()

        group = Group(txtGB, bottom)
        group.points.arrange(DOWN, buff=LARGE_BUFF).shift(UP * 0.1)

        tip = Text('（对于 186MB 的 PC 安装包而言）', font_size=12, color=GREY)
        tip.points.next_to(bottom, DOWN)

        txtGB_stat = txtGB.copy()
        txtGB.points.to_center()

        #########################################################

        self.forward()
        self.play(
            txtGB.anim.become(txtGB_stat),
            Write(bottom, at=0.4),
            FadeIn(tip, at=0.9, duration=0.5)
        )
        self.forward()


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

        txt0 = Text('前一张', color=PURPLE_E, depth=-20)
        txt0.points.next_to(frame0.points.box.get(DL), UR, buff=SMALL_BUFF)
        txt1 = Text('后一张', color=PURPLE_E, depth=-10)
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
