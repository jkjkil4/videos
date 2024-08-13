# flake8: noqa
import sys
import random

sys.path.append('.')

from janim.imports import *

from utils.template import *


class OpenVideoFile(Template):
    def construct(self) -> None:
        self.play_audio(Audio('视频编码2.mp3'), delay=1, end=21)

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
        self.subtitle('这是一个视频文件')
        self.play(FadeIn(file, DOWN, scale=2))
        self.subtitle('双击', duration=0.7, delay=0.2)
        self.play(
            cursor.anim(path_arc=-60 * DEGREES)
                .points.to_center().shift(DR * 0.6 + DOWN * 0.2),
            duration=0.7
        )
        for _ in range(2):
            click()
            self.prepare(
                Flash(cursor.points.box.get(UL), rate_func=rush_from),
                duration=0.1
            )

        video.seek(8.3)
        self.subtitle('视频画面就会出现在屏幕上', duration=1.6)
        self.play(
            FadeIn(video, scale=3, rate_func=rush_from),
            duration=0.5
        )
        self.hide(file, cursor)
        self.forward(1.5)
        video.start()
        self.forward(0.5)

        t = self.subtitle('我们还可以在进度条上点击来跳转进度', duration=2.7)
        self.forward_to(t.end)

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
        ])

        for v in videos:
            v.start(speed=0.5)
        videos[2].start(speed=0.25)
        videos[3].start(speed=0.25)

        #########################################################

        self.subtitle('在这个数字媒体资源丰富的时代', duration=2.3)
        self.forward(2.3)
        self.subtitle('视频画面承载着人类的记忆、情感、知识', duration=3.8)
        self.play(
            Aligned(
                circle.anim.points.scale(17),
                self.camera.anim.points.scale(3),
                FadeIn(
                    videos,
                    lag_ratio=0.5
                )
            ),
            duration=3.8
        )
        self.subtitle('在观看视频之余，我们可能还会好奇', duration=2)
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
            duration=1
        )
        self.subtitle('视频是如何保存到这个文件中的？', duration=2.2, delay=0.5)
        self.forward(1.5)
        file.depth.set(-10)
        self.play(
            Flash(file, color=[PURPLE, PURPLE_A], flash_radius=1, line_length=0.5)
        )
        self.forward(0.7)
        self.subtitle('其中的数据又是如何组织的呢？', duration=2)
        self.forward(2 + 1)


class Title(Template):
    def construct(self) -> None:
        self.play_audio(Audio('视频编码2.mp3'), delay=0.5, begin=21, end=26)

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

        self.subtitle('我们将通过“发明”视频格式的方式', duration=2.5, delay=0.5)
        self.subtitle('来初步认识一下——视频编码', duration=2.2, delay=3)
        self.forward()
        self.prepare(
            Write(g_lines),
            Write(g_lines2),
            at=1,
            duration=2
        )
        self.play(ShowIncreasingSubsets(txt1[0], duration=1.5))
        self.play(DrawBorderThenFill(txt2))
        self.forward(2)


class SimpleSolution(Template):
    def construct(self) -> None:
        audio = Audio('视频编码2.mp3')
        self.play_audio(audio, delay=1, begin=26, end=57)

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

        txt = Text('玩耍中的同学 →').show()
        txt.points.next_to(frames[0], LEFT)

        #########################################################

        self.forward()
        self.subtitle('我们知道，所谓动态的视频', duration=2)
        self.play(
            self.camera.anim.points.rotate(30 * DEGREES, axis=UP + LEFT * 0.2),
            duration=2
        )
        t = self.subtitle('其实就是将多个图像快速切换', delay=0.5, duration=2.5)
        self.forward()
        self.play(
            *[
                frame.anim.points.shift(i * 0.95 * OUT)
                for i, frame in enumerate(frames)
            ],
            rate_func=rush_from,
            duration=1.5
        )

        self.subtitle('利用“视觉暂留”效应在人眼上形成连续运动的图像',
                      delay=t.end - self.current_time,
                      duration=3.4)

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

        self.subtitle('因此，一个最简单的思路', duration=2.4)
        self.forward(2.4)

        self.subtitle('就是把视频中的每一张画面，也就是每一帧', duration=2.5)
        self.play(
            self.camera.anim.restore(camera_stat),
            frames.anim.become(target),
            duration=1.5
        )
        self.forward()
        self.subtitle('都塞到这个文件中', duration=1.4)
        self.forward(1.5)

        self.subtitle('播放的时候把这些帧逐个拿出来就好了', duration=3)
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
            duration=3
        )
        self.subtitle('这个方法确实简单粗暴', duration=1.8, delay=0.5)
        self.forward(2.5)

        self.subtitle('存储图像对于我们的设备来说是身经百战见得多了', duration=3.5)
        self.play(frames[1:].anim.digest_styles(color=GREY))
        self.forward()
        self.play(frames[1:].anim.digest_styles(color=WHITE))
        self.forward()
        self.subtitle('但视频编码绝对没有这么简单', duration=2.3)
        self.forward(2.3)
        self.subtitle('我们不妨思考一下这个方法会导致什么问题', duration=3)
        self.forward(2.7)


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
            duration=2
        )
        self.play_audio(audio, begin=57, end=76.6)
        self.forward(0.3)
        self.subtitle('一个很严重的问题就是', duration=1.8)
        self.forward(1.8)
        self.subtitle('它会占用非常大的存储空间', duration=2)
        self.forward(2)

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

        self.subtitle('比如一张 1920x1080 像素的普通彩色画面', duration=4)
        self.play(
            FadeOut(frames[1:]),
            Transform(frames[0], frame0_stat),
            duration=1.5
        )
        self.play(
            growline(vline),
            growline(hline, duration=0.75, rate_func=rush_from),
            lag_ratio=0.5
        )
        self.forward(1.5)

        #########################################################

        frame0R = frame0_stat.copy()
        frame0R.digest_styles(color=[1, 0, 0])
        frame0G = frame0_stat.copy()
        frame0G.digest_styles(color=[0, 1, 0])
        frame0B = frame0_stat.copy()
        frame0B.digest_styles(color=[0, 0, 1])

        frame0RGB = Group(frame0R, frame0G, frame0B).show()
        frame0RGB.depth.arrange(10)
        frame0RGB.points.scale(0.25).arrange(DOWN) \
            .next_to(frame0_stat, buff=-0.2)

        #########################################################

        self.subtitle('按照红、绿、蓝三种颜色的存储方式来计算', duration=2.9 )
        self.play(FadeIn(frame0RGB, RIGHT), duration=0.5)

        #########################################################

        typ = Typst('1920 times 1080 times 3 times 8 "bit"')
        txts = Group(
            Text('= 49,766,400 bit'),
            Text('= 6,220,800 B'),
            Text('= 6075 KiB'),
            Text('= 5.93 MiB')
        )
        txts.points.arrange(DOWN, aligned_edge=LEFT)
        # for txt in txts[1:]:
        #     txt.points.align_to(txts[0], LEFT)
        #     txt.points.shift(UP * (txts[0][0].get_mark_orig() - txt[0].get_mark_orig()))
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
            ),
            duration=0.7
        )
        self.play(
            Write(typ[9:11]),
            FadeTransform(frame0RGB, desc2, at=0.5),
            duration=0.7
        )
        self.play(
            Write(typ[11:]),
            FadeIn(desc3, at=0.5),
            duration=0.7
        )
        self.subtitle('需要大约 5.93 MiB', delay=0.7, duration=2)
        self.play(Write(txts[0]))
        for txtp, txt in it.pairwise(txts):
            self.play(
                txtp.anim.color.set(GREY),
                Create(txt),
                lag_ratio=0.5,
                duration=0.4
            )
        self.forward()

        typtxt = Group(typ, txts[-1])
        self.subtitle('对于一个每秒 30 帧的视频来说', duration=2)
        self.play(
            FadeOut(Group(hline, vline, desc1, desc2, desc3, txts[:-1]), duration=0.6),
            typtxt.anim.points.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
                .next_to(frames, UP, aligned_edge=LEFT),
            Transform(frame0_stat, frames[0]),
            FadeIn(frames[1:]),
            duration=0.6
        )

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
        self.subtitle('哪怕持续 1 分钟就需要 10.4 GiB 的空间！', duration=2.4)
        self.play(Write(txt1min)),
        self.forward(0.5)
        self.play(
            GrowArrow(arrow),
            FadeIn(txtGB, scale=0.5, duration=0.6, at=0.4),
            duration=0.5
        )
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
            ),
            duration=1
        )
        self.forward(2)


class CompareToWechat(Template):
    def construct(self) -> None:
        self.play_audio(Audio('视频编码2.mp3'), delay=0.7, begin=76.6, end=87)

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
        self.subtitle('这是什么概念呢？', duration=1.2)
        self.forward(1.2)
        self.subtitle('这意味着每一分钟视频的大小', duration=2.4)
        self.subtitle('约等于 40 个《小而美》安装包', duration=2.6, delay=2.4)
        self.forward(0.5)
        self.play(
            txtGB.anim.become(txtGB_stat),
            Write(bottom, at=0.4),
            info.anim(rate_func=rush_from)
                .points.shift(RIGHT * 6),
            duration=3
        )
        self.forward(1.4)
        self.forward(0.3)
        self.subtitle('这可不行啊，如果是电影这种动辄数小时的视频', duration=3.6)
        self.forward(3.6)
        self.forward()


class TooLarge(Template):
    def construct(self) -> None:
        t = self.play_audio(Audio('视频编码2.mp3'), delay=1, begin=87, end=88.7)

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

        self.subtitle('岂不是得把电脑撑爆', t)
        self.forward_to(t.end)
        self.forward()


class Difference(Template):
    def construct(self) -> None:
        self.play_audio(Audio('视频编码2.mp3'), delay=2, begin=88.7, end=127.2)

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

        self.forward(2.5)
        self.subtitle('为了解决这个问题，我们先来观察一个规律', duration=3)
        self.forward()
        self.play(
            frames.anim(rate_func=rush_from)
                .points.shift(LEFT * Config.get.frame_width + RIGHT * 2.5),
            duration=2
        )
        self.subtitle('对于我们拍摄出来的视频', duration=1.7, delay=0.3)
        self.forward(2)
        self.prepare(
            FadeIn(txt0),
            FadeIn(txt1),
            at=0.8
        )
        self.subtitle('前后连续的两帧之间其实一般不会有太大的变动', duration=3.6)
        self.play(
            Transform(frames[0], frame0),
            Transform(frames[1], frame1),
            FadeOut(frames[2:]),
            duration=1.5
        )
        self.play(
            GrowDoubleArrow(arrow),
            FadeIn(think, duration=2, at=0.2)
        )
        self.forward(0.2)
        self.subtitle('最多也就是在挪动拍摄角度', duration=2)
        self.forward(2)
        self.subtitle('因此我们就可以“偷个懒”', duration=2.3)
        self.forward(2.3)
        self.subtitle('对于后面这一帧', duration=1.3)
        self.subtitle('我们只需要记录和前一帧的“差异”', delay=1.3, duration=2.2)
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
            duration=3
        )
        self.forward(0.5)
        self.subtitle('这种差异算法能保证，对于连续画面而言', duration=3)
        self.play(
            FadeIn(diff),
            txt1.anim.color.set(PURPLE),
            FadeIn(tip),
            duration=1.5
        )
        self.forward(1.5)
        self.subtitle('需要记录的信息量可以大大减小', duration=2.5)


        frame1[0].hide()
        frame1.remove(frame1[0])
        frame1.add(diff, insert=True)
        diff_cpy = diff.copy()
        diff_cpy.points.set(frames[1][0].points.get())
        depth = frames[1][0].depth.get()
        frames[1].remove(frames[1][0])
        frames[1].add(diff_cpy, insert=True)
        frames[1].depth.arrange(depth)

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
        self.subtitle('我们通过这种差异算法记录之后的每一帧的信息', delay=0.5, duration=3.2)
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
                duration=0.05
            )
            frame[0].image.set(diff.image.get())
            t = self.prepare(
                frame.anim.points.shift(DOWN * 0.25),
                duration=0.05
            )

        self.forward(0.2)

        #########################################################

        frame_playback = orig_frames[0].copy()
        frame_playback.points.shift(LEFT * 2)
        frame_playback.depth.set(-100)

        #########################################################

        self.subtitle('在播放的时候，只需要把前一帧作为基础', delay=0.1, duration=3)
        self.play(
            Group(bgl, frames).anim
                .points.rotate(-PI / 2).to_border(RIGHT, buff=LARGE_BUFF)
        )
        self.forward()
        self.play(
            Transform(frames[0], frame_playback)
        )
        self.subtitle('并作用上这个“差异”的因素，也称之为“解码”', delay=0.3, duration=3.7)
        self.subtitle('就可以把后一帧还原出来了', delay=4, duration=2)
        self.subtitle('这样依次往后就可以还原出视频的每一帧', delay=6, duration=3)
        self.forward()

        for i, (diff, orig) in enumerate(zip(frames[1:], orig_frames[1:]), start=2):
            self.play(
                diff[0].anim(rate_func=linear)
                    .points.set(frame_playback[0].points.get()),
                diff[1].anim(rate_func=linear)
                    .points.set(frame_playback[1].points.get()),
                rate_func=rush_into,
                duration=1.5 if i < 4 else 0.15
            )
            diff.hide()
            if i == 18:
                self.play(
                    frames[18:].anim.points.shift(UP * 5),
                    duration=0.6
                )
            frame_playback[0].image.set(orig[0].image.get())

        self.forward(2)


class Midway(Template):
    def construct(self) -> None:
        self.play_audio(Audio('视频编码2.mp3'), delay=1 , begin=127.8, end=138.5)

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
        self.subtitle('至此，通过对比前后差异', delay=0.2, duration=1.8)
        self.play(
            FadeIn(bgl1),
            frames.anim(rate_func=rush_from).points.shift(vect),
            duration=1.5
        )
        self.subtitle('我们将那些占用巨大的原始画面', delay=1, duration=2)
        self.forward(2)
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
        self.subtitle('变成了第一张原始画面以及随后的多个“差异”数据', duration=3.5)
        self.play(
            Indicate(
                diff_frames[0][1],
                at=0.5,
                duration=1
            ),
        )
        self.forward(1.5)
        self.prepare(
            *[
                Indicate(frame[1], color=PURPLE, scale_factor=1)
                for frame in diff_frames[1:]
            ],
            duration=1
        )
        self.forward(0.5)
        self.subtitle('大幅度减小了存储占用', duration=2.2)
        self.forward(3)


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

        self.play_audio(Audio('视频编码2.mp3'), delay=1, begin=139.3, end=145.3)
        self.forward()
        self.subtitle('那么，难道我们的方案就是“只存第一张，后面全靠算”吗？', duration=4)
        self.forward(4)
        self.subtitle('这种方案存在明显的问题', duration=2)
        self.forward(2)
        self.forward()


class Limitation(Template):
    def construct(self) -> None:
        self.play_audio(Audio('视频编码2.mp3'), delay=1, begin=145.3, end=161.4)

        #########################################################

        video = Video('celeste-playback.mp4', width=Config.get.frame_width * 0.75)

        arrow = Arrow(RIGHT * 4 + DOWN * 1.4, LEFT * 4 + DOWN * 1.4, color=YELLOW)

        bi = ImageItem('bi.jpg', height=Config.get.frame_height)

        #########################################################

        self.forward()
        self.subtitle('还记得我们开头说过的', duration=1.9)
        self.subtitle('“可以点击进度条进行跳转”吗？', delay=1.9, duration=2)
        video.seek(3.9)
        self.play(FadeIn(video, scale=1.5))
        self.play(
            video.anim.points.scale(3, about_edge=DOWN).shift(LEFT * 5)
        )
        video.start()
        self.forward(0.5)
        self.play(
            video.anim.points.shift(RIGHT * 5)
        )
        video.stop()
        self.play(
            video.anim.points.shift(RIGHT * 6),
            duration=0.7
        )
        # self.forward(0.2)
        # self.play(
        #     video.anim.points.shift(LEFT * 7),
        #     duration=0.5
        # )
        # self.forward(0.2)
        # self.play(
        #     video.anim.points.shift(LEFT * 7)
        # )
        # self.forward(0.4)
        # video.stop()
        self.subtitle('试想一下', duration=1)
        self.forward()
        self.subtitle('如果后面的每一帧都是依赖前一帧', duration=2.5)
        self.play(GrowArrow(arrow), duration=2.5)
        self.forward(0.5)
        self.subtitle('那如果我们只是想跳转到电影结尾回顾一下结局', duration=3.3)
        self.forward(3.3)
        self.forward(0.3)
        self.subtitle('鼠标确实只需轻轻一拖就可以了', duration=2.5)
        self.play(FocusOn(arrow.points.get_start() + DOWN * 0.5))
        self.forward(0.5)
        self.subtitle('而电脑要考虑的就很多了', duration=1.7)
        self.forward(1.7)
        self.play_audio(Audio('bi.mp3', begin=0.5, end=1).fade_out(0.07))
        bi.show()
        self.forward(0.5)


class ComputeAll(Template):
    def construct(self) -> None:
        self.play_audio(Audio('视频编码2.mp3'), begin=161.4, end=169.4)

        #########################################################

        fire = ImageItem('fire.jpg', alpha=0.3, width=Config.get.frame_width)
        video = Video('2024-04-26 22-44-23.mp4', width=Config.get.frame_width * 0.5)
        video.points.scale(1 / 100)

        random.seed(114514)

        line = Line(6 * LEFT, 6 * RIGHT, color=PURPLE_E)
        unstable_arrow = Arrow(color=PURPLE_A)
        unstable_arrow.points.set_as_corners([
            RIGHT * x + UP * (rush_into(y / 3) * 3 * (random.random() * 2 - 1))
            for x, y in zip(np.linspace(-6, 6, 65), np.linspace(0, 3, 65))
        ])
        unstable_arrow.points.make_smooth(root_only=True)
        unstable_arrow.place_tip()

        #########################################################

        video.start(speed=180)

        self.subtitle('他得把整个视频从头算一遍', duration=2.5)
        self.subtitle('这也太坑了吧！', delay=2.5, duration=1.2)
        self.play(
            FadeIn(fire),
            video.anim.points.scale(100),
            rate_func=linear,
            duration=3
        )
        self.play(
            video.anim.color.set([1, 0.5, 0])
        )
        self.subtitle('并且，对于有损压缩的画面', duration=2.2)
        self.subtitle('误差会随着解码而累积', delay=2.2, duration=1.9)
        self.forward()
        self.play(
            video.anim(duration=0.4).points.scale(0.5),
            Create(line),
            GrowArrow(unstable_arrow),
            duration=3
        )
        self.forward(0.3)


class RealSolution(Template):
    def construct(self) -> None:
        self.play_audio(Audio('视频编码2.mp3'), begin=169.5, end=203.2)

        #########################################################

        bgl = Rect(
            Config.get.frame_width * 2, 2,
            stroke_alpha=0,
            fill_alpha=0.5,
            fill_color=PURPLE_E,
            depth=1000
        )

        diff = ImageItem('diff.jpg', height=Config.get.frame_height - 2)

        frames = Group(*[
            Group(
                frame,
                SurroundingRect(frame, color=WHITE, buff=0, stroke_radius=0.01),
                depth=i
            )
            for i, frame in enumerate([
                VideoFrame('example.mp4', 0, height=Config.get.frame_height - 2),
                *(diff * 120)
            ])
        ])

        for frame in frames:
            frame.points.to_center().scale(0.3)
            frame.points.apply_point_fn(
                lambda p: p + p[0] * 0.6 * DOWN
            )
        frames.points.arrange(buff=-0.85).shift(RIGHT * 5)

        origframes = frames[::30]
        origframes_exf = origframes[1:]

        #########################################################

        self.subtitle('因此，实际的方案是每隔一些画面就插入一个“原始画面”', duration=4.3)
        self.show(bgl, frames)

        self.forward()
        self.play(
            origframes_exf.anim.points.shift(UP),
            self.camera.anim.points.shift(RIGHT * 4)
        )
        self.forward(1.6)

        for i, frame in enumerate(origframes_exf, start=1):
            frame[0].image.set(VideoFrame('example.mp4', i).image.get())
            frame.points.scale(1.2)

        self.play(
            *[
                frame.anim(rate_func=rush_from)
                    .points.scale(1 / 1.2)
                for frame in origframes_exf
            ],
            duration=0.3
        )

        self.forward(1.2)
        self.subtitle('比如这个视频', duration=1)
        self.forward()

        #########################################################

        y = frames[30].points.box.get_y(DOWN)

        def get_start_and_end(i: int):
            f1 = frames[i * 30]
            f2 = frames[i * 30 + 29]
            b1 = f1.points.box
            b2 = f2.points.box
            return (
                [b1.get_x(RIGHT), y, 0],
                [b2.get_x(RIGHT), y, 0]
            )

        arrows = Group(*[
            DoubleArrow(
                *get_start_and_end(i),
                buff=0,
                color=YELLOW,
                tip_kwargs=dict(
                    center_anchor=CenterAnchor.Front
                )
            )
            for i in range(4)
        ]).show()

        txts = Text(
            '30 帧',
            color=YELLOW,
            stroke_alpha=1,
            stroke_color=BLACK,
            stroke_background=True
        ) * len(arrows)
        for arrow, txt in zip(arrows, txts):
            txt.points.next_to(arrow, DOWN, buff=0)

        #########################################################

        self.subtitle('每30帧就有一个原始画面', duration=1.4)
        self.play(
            *[
                GrowArrow(arrow)
                for arrow in arrows
            ],
            *[
                Write(txt)
                for txt in txts
            ]
        )

        self.forward()

        ########################################################

        arrow = Group(
            Text('跳转'),
            Arrow(ORIGIN, DOWN),
            color=PURPLE
        )
        arrow.points.arrange(DOWN, buff=SMALL_BUFF)
        arrow.points.next_to(frames[72], UP, buff=0)

        arrow_actually = Group(
            Text('跳转（实际上）'),
            Arrow(ORIGIN, DOWN),
            color=PURPLE_A
        )
        arrow_actually.points.arrange(DOWN, buff=SMALL_BUFF)
        arrow_actually.points.next_to(frames[60], UP, buff=0)

        tgt = frames[60][0]

        frame72_stat = frames[72].copy()

        frames_stat = frames.copy()

        ########################################################

        self.subtitle('这样在跳转的时候就不必从头计算了', delay=0.3, duration=3)
        self.play(
            FadeIn(arrow, DOWN, rate_func=rush_from),
            duration=0.6
        )
        self.play(
            Group(arrow, frames[72])
                .anim.points.shift(UP * 0.5),
            duration=0.4
        )
        self.forward()

        for frame in frames[61:72]:
            frame[0].image.set(tgt.image.get())
            frame.points.scale(1.1)
            self.play(
                frame.anim.points.scale(1 / 1.1),
                duration=0.1,
                rate_func=rush_from
            )

        frames[72][0].image.set(VideoFrame('example.mp4', 2.4).image.get())
        frames[72].points.scale(1.2)
        self.play(
            frames[72].anim.points.scale(1 / 1.2),
            duration=0.2,
            rate_func=rush_from
        )
        self.forward()

        to_diff_lst = []

        def to_diff(frame: Group[ImageItem | SurroundingRect]):
            to_diff_lst.append(frame)
            frame[0].image.set(diff.image.get())
            return frame

        self.subtitle('由于大多数播放器选择从最近的原始画面开始放', duration=3.3)
        self.play(
            Aligned(
                Transform(arrow, arrow_actually, hide_src=False),
                arrow(VItem).anim.color.set(PURPLE_E),
                AnimGroup(
                    FadeTransform(frames[72], frame72_stat),
                    *[
                        FadeTransform(
                            frame,
                            to_diff(frame.copy())
                        )
                        for frame in reversed(frames[61:72])
                    ],
                    lag_ratio=0.2
                ),
                duration=1.5
            )
        )
        self.forward()

        ########################################################

        exv = Video('pb_crop.mp4', height=6)
        exv.seek(8.9)
        exv.points.move_to(self.camera).scale(3, about_edge=DOWN).shift(UP)

        rect = boolean_ops.Difference(
            FrameRect(),
            Rect(1.8, 0.7)
                .points.shift(DR * 0.55 + DOWN * 0.2)
                .r,
            stroke_alpha=0,
            fill_alpha=0.5,
            fill_color=BLACK
        )
        rect.points.move_to(self.camera)

        ########################################################

        exv.start()
        self.play(FadeIn(exv), duration=0.3)
        self.forward(0.7)
        self.subtitle('这也造成了跳转时总会差那么一点', duration=2.1)
        exv.stop()
        self.forward(0.3)
        self.play(FadeIn(rect), duration=0.3)
        self.forward()
        self.play(
            FadeOut(Group(rect, exv)),
            FadeOut(Group(arrow, arrow_actually,
                          arrows, txts)),
            duration=0.6
        )

        ########################################################

        itxt = Text(
            'I 帧 <fs 0.7><fa 0.5>(Intra-coded Frame)</fa></fs>',
            color=YELLOW,
            format=Text.Format.RichText
        )
        itxt.points.next_to(frames[30], UP, aligned_edge=LEFT)

        ptxt = Text(
            'P 帧 <fs 0.7><fa 0.5>(Predicted Frame)</fa></fs>',
            color=PURPLE,
            format=Text.Format.RichText
        )
        ptxt.points.next_to(frames[40], DOWN, aligned_edge=LEFT)

        ########################################################

        self.subtitle('用专业语言来说', delay=0.3, duration=1.2)
        self.subtitle('这个原始画面叫做“I帧”', delay=1.5, duration=2)
        self.forward()
        self.play(
            Write(itxt),
            AnimGroup(
                *[
                    frame[1].anim.color.set(YELLOW)
                        .r.radius.set(0.03)
                    for frame in origframes
                ],
                lag_ratio=0.5,
                duration=2
            )
        )
        self.subtitle('在前一张画面基础上计算的帧叫做“P帧”', delay=0.7, duration=3)
        self.forward()

        for f, fs in zip(frames[61:73], frames_stat[61:73]):
            f.become(fs)
            f.show()
        frame72_stat.hide()
        for f in to_diff_lst:
            f.hide()

        self.play(
            Write(ptxt),
            AnimGroup(
                *[
                    frame[1].anim.color.set(PURPLE)
                        .r.radius.set(0.02)
                    for i, frame in enumerate(frames)
                    if i % 30 != 0
                ],
                lag_ratio=0.02,
                duration=2
            )
        )
        self.forward(0.5)
        self.subtitle('这样的一个分段叫做GOP', delay=0.3, duration=2)
        self.play(
            Group(itxt, frames[30])
                .anim.points.shift(DOWN),
            frames[:30].anim.points.shift(LEFT * 2),
            frames[60::30].anim.points.shift(RIGHT * 2 + DOWN),
            Group(frames[61:90], frames[91:120])
                .anim.points.shift(RIGHT * 2),
            duration=0.6
        )

        ########################################################

        rect = SurroundingRect(
            Group(itxt, ptxt, frames[30:60]),
            buff=Margins(0.5, 0.5, 0.5, 0.9),
            stroke_color=BLUE,
            fill_color=BLACK,
            fill_alpha=0.5
        )

        gop = Group(
            Text('GOP', font_size=36, color=BLUE),
            Text('(Group of Pictures)', font_size=18, color=BLUE_E)
        )
        gop.points.arrange(DOWN, buff=SMALL_BUFF)
        gop.points.move_to(rect)

        btxt = Text(
            'B 帧 <fs 0.6><fa 0.5>(Bidirectional Predicted Frame)</fa></fs>',
            color=MAROON,
            format=Text.Format.RichText
        )
        btxt.points.next_to(ptxt, DOWN, aligned_edge=LEFT)

        ########################################################

        self.play(
            FadeIn(rect),
            Write(gop)
        )
        self.forward(0.6)
        self.subtitle('其实，基于类似的原理', duration=1.6)
        self.forward(1.6)
        self.subtitle('还有同时根据前面画面和后面画面计算的“B帧”', duration=3)
        self.forward()
        self.play(
            Write(btxt)
        )
        self.subtitle('这里我们就不作展开了', duration=1.3)
        self.forward(1.3)
        self.forward(2)


class Compress(Template):
    def construct(self) -> None:
        self.play_audio(Audio('视频编码2.mp3'), delay=0.3, begin=203.3, end=215)

        ########################################################

        box = Square(0.5, stroke_alpha=0, fill_alpha=1, color=GOLD)

        boxes = box * 12
        boxes.points.arrange_in_grid(n_rows=4, buff=SMALL_BUFF)

        boxgroup = Group(
            SurroundingRect(boxes, buff=0, stroke_alpha=0, fill_alpha=0.2, fill_color=GOLD_E, depth=10),
            boxes
        )

        boxgroups = boxgroup * 8
        boxgroups.points.arrange(buff=SMALL_BUFF).shift(RIGHT * 2)

        allboxes = Group(*[
            box
            for boxgroup in boxgroups[1:]
            for box in boxgroup[1]
        ])
        random.seed(114514)
        allboxes.shuffle()

        allsur = Group(*[
            boxgroup[0]
            for boxgroup in boxgroups[1:]
        ])

        clip = len(allboxes) * 4 // 5

        uncreate_boxes = allboxes[:clip]
        stay_boxes = allboxes[clip:]
        stay_boxes_sorted = Group(
            *sorted(stay_boxes,
                    key=lambda box: box.points.box.x)
        )
        stay_boxes_sorted_target = stay_boxes_sorted.copy()
        stay_boxes_sorted_target.points \
            .arrange_in_grid(n_rows=4, buff=SMALL_BUFF, fill_rows_first=False) \
            .next_to(boxgroups[0], buff=SMALL_BUFF)
        stay_boxes_sorted_target(VItem).color.set(PURPLE)

        ########################################################

        self.forward()
        self.subtitle('利用这套思路', duration=1.1)
        self.subtitle('我们可以在保持观感基本不变的情况下将视频数据量极大地压缩', delay=1.1, duration=4.7)
        self.play(
            *[
                AnimGroup(
                    FadeIn(boxgroup[0], scale=0.7, rate_func=rush_from),
                    Write(boxgroup[1])
                )
                for boxgroup in boxgroups
            ],
            lag_ratio=0.4,
            duration=3
        )
        self.play(
            Uncreate(uncreate_boxes, lag_ratio=0.1),
            stay_boxes(VItem).anim.color.set(PURPLE),
            allsur(VItem).anim.color.set(PURPLE_E),
            duration=2
        )
        self.play(Transform(stay_boxes_sorted, stay_boxes_sorted_target))

        self.subtitle('从而使视频无论是本地存储', duration=2)
        self.forward()

        ########################################################

        g = Group(boxgroups[0][1], stay_boxes_sorted_target)
        gsur = Group(*[
            boxgroup[0]
            for boxgroup in boxgroups
        ])

        computer = ImageItem('computer.png')
        computer.points.move_to(g)

        internet = Group(
            Circle(
                0.6,
                stroke_alpha=0,
                fill_alpha=1,
                fill_color=BLACK
            ),
            ImageItem('internet.png', height=1.2)
        )
        dst = get_norm(internet.points.box.center - computer.points.box.center)

        computers = Group(
            computer,
            *[
                computer.copy()
                    .points.move_to(dst * (RIGHT * math.cos(radian) + UP * math.sin(radian)))
                    .r
                for i in range(-2, 3)
                for radian in [i * 60 * DEGREES]
            ]
        )

        lines = Group(
            *[
                Line(internet, computer)
                for computer in computers
            ],
            color=PURPLE_E,
        )
        lines_copy = lines.copy()
        lines_copy(VItem).color.set(PURPLE_A)
        lines_copy.depth.arrange(-1)

        line1 = lines_copy[0].copy()
        line1.points.reverse()

        ########################################################

        self.play(
            FadeOut(gsur),
            FadeTransform(g, computer)
        )
        self.subtitle('还是通过网络大规模传播都成为了可能', duration=2.8)
        self.forward(0.2)
        self.play(
            FadeIn(internet),
            FadeIn(computers[1:], scale=0.8, about_point=ORIGIN),
            Create(lines)
        )
        self.prepare(
            *[
                ShowPassingFlash(line1, time_width=0.3, rate_func=linear)
                for _ in range(4)
            ],
            lag_ratio=0.7,
            duration=0.5
        )
        self.forward(0.3)
        self.play(
            *[
                ShowPassingFlash(lines_copy[1:], time_width=0.3, rate_func=linear)
                for _ in range(6)
            ],
            lag_ratio=0.7,
            duration=1
        )
        self.forward()


class End(Template):
    CONFIG = Config(
        output_dir=':/assets'   # 因为这是被 MetaEnd 使用的，所以输出到 ':/assets'
    )

    def construct(self) -> None:
        t = self.play_audio(Audio('视频编码2.mp3'), delay=1, begin=215)

        txt1 = Text('这里提及的思路', color=PURPLE_A)
        txt2 = Text('视频编码', font_size=500, color=BLUE)
        txt2.points.shift(UP * 12 + RIGHT * 2)
        rect = Rect(
            60, 60,
            color=BLUE,
            fill_alpha=0.3,
            stroke_radius=0.2,
            depth=1
        )
        rect.points.move_to(txt2)

        txt2.show()
        self.forward()
        self.subtitle('然而，这里提及的思路', duration=1.6)
        self.subtitle('仅仅是视频编码的冰山一角', delay=1.6, duration=2)
        self.play(Write(txt1))
        self.play(
            self.camera.anim.points.scale(10).move_to(txt2),
            FadeIn(rect),
            duration=3
        )
        self.subtitle('它的学问不止于此', duration=1.3)
        self.forward(1.5)
        self.subtitle('我们能刷到这个视频', duration=1.4)
        self.forward(1.5)
        self.subtitle('还需要感谢视频编码技术的发展与完善', duration=2.7)
        self.forward_to(t.end + 1)


class MetaEnd(Template):
    def construct(self) -> None:
        ########################################################

        camera_stat = self.camera.store()

        bg = FrameRect(
            stroke_alpha=0,
            fill_alpha=1,
            fill_color=WHITE
        ).show()

        b_like = SVGItem('b-like.svg', height=0.4, color='#61666d')
        b_coin = SVGItem('b-coin.svg', height=0.4, color='#61666d')
        b_fav = SVGItem('b-fav.svg', height=0.4, color='#61666d')

        b_acts = Group(b_like, b_coin, b_fav).show()
        b_acts.points.arrange(buff=LARGE_BUFF).to_border(DL, buff=LARGE_BUFF)

        video = Video('End.mp4')
        video.points.scale(0.55).next_to(b_acts, UP, buff=0.35, aligned_edge=LEFT)
        audio = Audio('End.mp3', end=10.8)

        txt = Text('视频是如何存储在你的设备里的 – 视频编码简述', font_size=18, color=BLACK).show()
        txt.points.next_to(video, UP, buff=0.35, aligned_edge=LEFT)

        self.camera.points.move_to(video).scale(video.points.box.width / bg.points.box.width)

        ########################################################

        self.play_audio(audio)
        video.show().start()

        self.forward(6.4)
        self.play(
            self.camera.anim.restore(camera_stat),
            duration=2
        )

        ########################################################

        circles = Circle(0.3, color=BLUE_D) * 3
        for c, b in zip(circles, b_acts):
            c.points.reverse().rotate(PI / 2)
            c.points.move_to(b)

        ########################################################

        self.prepare(
            Create(circles, auto_close_path=False),
            at=1.4 + 0.5
        )

        self.forward_to(audio.duration() + 0.5)
        for b in b_acts:
            b.points.scale(1.2)
            b(VItem).color.set(BLUE_D)
        self.play(
            *[
                b.anim(duration=0.2).points.scale(1 / 1.2)
                for b in b_acts
            ],
            *[
                FadeOut(c, scale=1.2, duration=0.1)
                for c in circles
            ],
        )
        self.forward()
