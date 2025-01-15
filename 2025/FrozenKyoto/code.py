import random
from janim.imports import *


class TextBox(Group[VItem]):
    def __init__(
        self,
        text: str,
        font_size: float,
        box_width: float,
        box_color: JAnimColor
    ):
        sq1 = Square(
            box_width,
            stroke_alpha=0,
            fill_alpha=1,
            fill_color='#0e2c45'
        )
        sq1.points.shift(DR * 0.08)
        sq2 = Square(
            box_width,
            stroke_alpha=0,
            fill_alpha=1,
            fill_color=box_color
        )
        stroke = boolean_ops.Union(sq1, sq2)
        sq3 = Square(
            box_width * 0.8,
            stroke_radius=0.01,
            stroke_color=GREY_A
        )
        txt = Text(text, font_size=font_size, font=['新蒂文徵明體', 'KaiTi'])
        super().__init__(sq1, sq2, stroke, sq3, txt)


class GothicTextBox(Group[VItem]):
    seed_generator = random.Random(114514)

    def __init__(
        self,
        text: str,
        font_size: float,
        box_color: JAnimColor,
        box_buff: float | Margins,
        *,
        post_fn: Callable[[Text], None] = lambda x: None
    ):
        txt = Text(text, font_size=font_size, font='DFPHSGothic-W9')
        post_fn(txt)
        sq1 = SurroundingRect(
            txt,
            buff=box_buff,
            stroke_alpha=0,
            fill_alpha=1,
            fill_color='#0e2c45'
        )
        sq1.points.shift(DR * 0.09)
        sq2 = SurroundingRect(
            txt,
            buff=box_buff,
            stroke_alpha=0,
            fill_alpha=1,
            fill_color=box_color
        )
        stroke = boolean_ops.Union(sq1, sq2)
        super().__init__(sq1, sq2, stroke, txt)
        self.depth.arrange()

    def get_anim(
        self,
        *,
        stretch_dim: int = 0,
        stretch_duration: float = 1,
        txt_duration: float = 0.85,
        seed: int | float | str | bytes | bytearray | None = None,
        **kwargs
    ):
        if seed is None:
            seed = self.seed_generator.random()

        rng = random.Random(seed)

        stat1 = self[:3].copy()
        self[:3].points.stretch(0, dim=stretch_dim, about_point=self[1].points.box.center)

        stat2 = self[3].copy()
        for char in self[3].walk_descendants(TextChar):
            char.points.shift([rng.random() * 5 - 2.5, rng.random() * 5 - 2.5, 0])
            char.points.rotate(rng.random() * 90 * DEGREES - 45 * DEGREES)
            char.color.set(alpha=0)

        return AnimGroup(
            self[:3].anim(rate_func=cubic_out, duration=stretch_duration).become(stat1),
            self[3].anim(rate_func=expo_out, duration=txt_duration).become(stat2),
            **kwargs
        )


class TextBoxGroup(Group[Group[TextBox]]):
    def __init__(
        self,
        text: str,
        box_colors: Sequence[JAnimColor],
        buff: float,
        font_size: int,
        box_width: float
    ):
        lines = text.split('\n')

        def next_color() -> Generator[JAnimColor, None, None]:
            yield from box_colors
            while True:
                yield box_colors[-1]

        iter = next_color()
        super().__init__(
            *[
                Group.from_iterable(
                    TextBox(char, font_size, box_width, next(iter))
                    for char in line
                ).points.arrange(buff=buff).r
                for line in lines
            ]
        )
        self.points.arrange(DOWN, buff=buff)

    def get_anim(
        self,
        *,
        direction_fn: Callable[[int], Vect] = lambda i: DOWN,
        **kwargs
    ):
        return AnimGroup(
            *[
                AnimGroup(
                    GrowFromPoint(
                        box[:3],
                        box[0].points.box.center,
                        duration=0.4,
                        rate_func=sine_out
                    ),
                    GrowFromPoint(
                        box[3],
                        box[0].points.box.center,
                        duration=0.4,
                        at=0.075,
                        rate_func=sine_out
                    ),
                    FadeIn(
                        box[4],
                        direction_fn(i),
                        duration=0.4,
                        at=0.15,
                        rate_func=sine_out
                    )
                )
                for i, box in enumerate(it.chain(*self.children))
            ],
            **kwargs
        )


class FrozenKyoto(Timeline):
    CONFIG = Config(
        background_color=Color('#462f49')
    )

    def construct(self):
        video_path = R'D:\Documents\you-get\向着将要永远封冻的京都，一起去吧。.mp4'
        seek = 100

        audio = Audio(
            video_path,
            begin=seek
        ).fade_in(0.5)
        self.play_audio(audio)

        video = Video(
            video_path,
            width=Config.get.frame_width,
            alpha=1
        ).fix_in_frame().show()
        video.points.scale(0.3, about_edge=DR)
        video.seek(seek)
        video.start()

        g1 = TextBoxGroup(
            '平安時代に',
            ('#686489', '#007d9a', '#982547', '#da7238', '#5f974b'),
            0.2,
            135,
            1.95
        )
        g1.points.shift(RIGHT * 3.8 + UP * 2.7)
        g1[0][1].points.shift(DOWN * 1)
        for i, box in enumerate(g1[0][2:]):
            box.points.next_to(g1[0][i], DOWN, buff=0.2)

        g2 = GothicTextBox(
            'いらっしゃいませんか？',
            38,
            '#3c5e6e',
            0.1
        )
        g2.points.shift(RIGHT * 5.3 + DOWN * 2.9)

        g3 = TextBoxGroup(
            '九百五十\n年前に',
            ('#543f70', '#206666', '#273f7f', '#204d7e', '#ab354e', '#1045e0', '#b35148'),
            0.05,
            100,
            1.5
        )
        g3.points.shift(RIGHT * 12.2 + UP * 1.9)

        g4 = GothicTextBox(
            '造\nら\nれ\nた',
            46,
            '#1b9bd1',
            Margins(0.05, 0.3, 0.05, 0.3)
        )
        g4.points.shift(RIGHT * 12.1 + DOWN * 1.65)

        g5 = TextBoxGroup(
            '此処には',
            ('#0c9e68',),
            0.03,
            40,
            0.74
        )
        g5.points.shift(RIGHT * 16.02 + DOWN * 0.5)

        g6 = TextBoxGroup(
            '絵に描いた様な',
            ('#013d7d',),
            0.03,
            40,
            0.71
        )
        g6.points.shift(RIGHT * 16.03 + DOWN * 1.44)

        g7 = GothicTextBox(
            '春がありました',
            38,
            '#ae3170',
            Margins(0.2, 0.1, 0.2, 0.1)
        )
        g7.points.shift(RIGHT * 16.05 + DOWN * 2.3)

        g8 = GothicTextBox(
            '絵\nを\n描\nく\n様\nに',
            40,
            '#aba73b',
            Margins(0.1, 0.2, 0.1, 0.2),
            post_fn=lambda txt: txt.arrange_in_lines(base_buff=0.7)
        )
        g8.points.shift(RIGHT * 22 + UP * 1.6)

        g9 = GothicTextBox(
            '桜\nの\n木\nを\n一\n本\n一\n本',
            40,
            '#c64d69',
            Margins(0.1, 0.2, 0.1, 0.2),
            post_fn=lambda txt: txt.arrange_in_lines(base_buff=0.7)
        )
        g9.points.shift(RIGHT * 21 + DOWN * 0.3)

        g10 = GothicTextBox(
            '植\nえ\nて\nい\nっ\nた\nの\nで\nす',
            40,
            '#0092d3',
            Margins(0.1, 0.2, 0.1, 0.2),
            post_fn=lambda txt: txt.arrange_in_lines(base_buff=0.7)
        )
        g10.points.shift(RIGHT * 20 + DOWN * 2.15)

        g11 = TextBoxGroup(
            '一日たっぷり',
            ('#97b633', '#e0c2a4', '#dc714a', '#296bd8', '#5a273f', '#3b5a6b'),
            0.03,
            44,
            0.71
        )
        g11.points.shift(RIGHT * 25.3 + UP * 2.8)

        def post_fn(txt: Text):
            for i, char in enumerate(txt[0]):
                char.points.shift(LEFT * 0.03 * i)

        g12 = GothicTextBox(
            'こういう場所に連れてきてあげたい',
            28,
            '#b13452',
            Margins(0.05, 0.15, 0.05, 0.15),
            post_fn=post_fn
        )
        g12.points.shift(RIGHT * 26.6 + UP * 1.95)

        g13 = GothicTextBox(
            'と、おもいます。',
            28,
            '#b13452',
            Margins(0.2, 0.15, 0.2, 0.15),
            post_fn=post_fn
        )
        g13.points.shift(RIGHT * 30.2 + UP * 1.1)

        g14 = TextBoxGroup(
            '今',
            ('#395769',),
            0.2,
            135,
            1.95
        )
        g14.points.shift(RIGHT * 30.2 + DOWN * 0.5)

        g15 = TextBoxGroup(
            'この国も',
            ('#ba9b3a', '#6023d2', '#9d2b5a', '#a92777'),
            0.03,
            44,
            0.71
        )
        g15.points.shift(RIGHT * 33.75 + DOWN * 0.7)

        g16 = GothicTextBox(
            '大変な事になって来ているようですが',
            28,
            '#032c4d',
            Margins(0.1, 0.15, 0.1, 0.15),
            post_fn=post_fn
        )
        g16.points.shift(RIGHT * 40.55 + UP * 2.8)

        g17 = TextBoxGroup(
            '一つの\n時代は',
            ('#9bb933', '#a96c36', '#97233b', '#0049d1', '#4325ce', '#a926bd'),
            0.05,
            90,
            1.45
        )
        g17.points.shift(RIGHT * 43 + DOWN * 0.4)

        def post_fn(txt: Text):
            for i, char in enumerate(txt[0]):
                char.points.shift(RIGHT * 0.15 * i)

        g18 = GothicTextBox(
            'いうなれば',
            70,
            '#002546',
            Margins(0.45, 0.05, 0.45, 0.05),
            post_fn=post_fn
        )
        g18.points.shift(RIGHT * 42.8 + DOWN * 2.6)

        g19 = TextBoxGroup(
            '沙羅双樹の花の色',
            ('#84778c', '#aeb92a', '#9e3c4e', '#0254de', '#0ab22b', '#032c4c', '#053949', '#261d3d'),
            0,
            78,
            1.18
        )
        for box in g19[0]:
            box.points.to_center()
        g19.points.shift(RIGHT * 50.77)
        g19[0][0].points.shift(LEFT * 2.4 + UP * 1.8)
        g19[0][4].points.shift(RIGHT * 2.4 + UP * 1.8)
        g19[0][1].points.shift(LEFT * 1.2 + UP * 2.5)
        g19[0][3].points.shift(RIGHT * 1.2 + UP * 2.5)
        g19[0][2].points.shift(UP * 3)
        g19[0][5].points.shift(LEFT * 1.7 + DOWN * 0.5)
        g19[0][7].points.shift(RIGHT * 1.7 + DOWN * 0.5)
        g19[0][6].points.shift(DOWN * 1.6)

        g20 = GothicTextBox(
            '知る人ぞ知る',
            54,
            '#1f2d38',
            Margins(1, 0.05, 1, 0.05)
        )
        g20.points.shift(RIGHT * 51.2 + DOWN * 2.9)

        def post_fn(txt: Text):
            for i, char in enumerate(txt[0]):
                char.points.shift(RIGHT * 0.065 * i)

        g21 = GothicTextBox(
            '歴史を潜り抜けて',
            50,
            '#01274a',
            Margins(0.2, 0.05, 0.2, 0.05),
            post_fn=post_fn
        )
        g21.points.shift(RIGHT * 57 + UP * 2.95)

        g22 = TextBoxGroup(
            '今も',
            ('#902f51', '#063b63'),
            0.03,
            140,
            2.24
        )
        g22.points.shift(RIGHT * 57 + UP * 0.9)

        g23 = GothicTextBox(
            '\n'.join('京都は此処で待っています'),
            34,
            '#0093dd',   # #d1ae47
            Margins(0.2, 0.1, 0.2, 0.1),
            post_fn=lambda txt: txt.arrange_in_lines(base_buff=0.54)
        )
        g23.points.shift(RIGHT * 61.4 + DOWN * 2.53)

        def post_fn(txt: Text):
            for i, char in enumerate(txt[0]):
                char.points.shift(LEFT * 0.02 * i)

        g24 = GothicTextBox(
            '私は昔に向かって歩いています',
            34,
            '#d1ae47',
            Margins(0, 0.15, 0, 0.15),
            post_fn=post_fn
        ).show()
        g24.points.shift(RIGHT * 65.8 + DOWN * 3.1)

        self.forward(2)

        self.prepare(
            g1.get_anim(at=0.25, lag_ratio=0.4),
            g2.get_anim(at=1.3, lag_ratio=0.1),
            g3.get_anim(at=2.1, lag_ratio=0.42, direction_fn=lambda i: DOWN if i % 2 == 0 else UP),
            g4.get_anim(at=3.4, lag_ratio=0.3, stretch_dim=1, stretch_duration=0.4, txt_duration=0.7),
            g5.get_anim(at=4.2, lag_ratio=0.2),
            g6.get_anim(at=4.6, lag_ratio=0.25),
            g7.get_anim(at=5.7, lag_ratio=0.2, stretch_duration=0.6),
            g8.get_anim(at=6.4, lag_ratio=0.2, stretch_dim=1),
            g9.get_anim(at=7, lag_ratio=0.3, stretch_dim=1),
            g10.get_anim(at=8.6, lag_ratio=0.3, stretch_dim=1),
            g11.get_anim(at=9.1, lag_ratio=0.28),
            g12.get_anim(at=9.7, lag_ratio=0.25, stretch_duration=2, txt_duration=1.4),
            g13.get_anim(at=12, lag_ratio=0.2),
            g14.get_anim(at=12.5, lag_ratio=0.2),
            g15.get_anim(at=12.9, lag_ratio=0.17),
            g16.get_anim(at=13.7, lag_ratio=0.3, stretch_duration=2, txt_duration=2),
            g17.get_anim(at=15.8, lag_ratio=0.2, direction_fn=lambda i: DOWN if i % 2 == 0 else UP),
            g18.get_anim(at=16.6, stretch_duration=0.6, txt_duration=1),
            g19.get_anim(at=17.3, lag_ratio=0.27),
            g20.get_anim(at=18.7, lag_ratio=0.4, txt_duration=0.6),
            g21.get_anim(at=19.8, lag_ratio=0.3),
            g22.get_anim(at=20.9, lag_ratio=0.2, duration=0.7),
            g23.get_anim(at=21.3, lag_ratio=0.4, stretch_dim=1),
            g24.get_anim(at=22.7, lag_ratio=0.4),
        )

        self.timeout(6.4, Group(g1, g2).hide)
        self.timeout(9.2, Group(g3, g4).hide)
        self.timeout(10.5, Group(g5, g6, g7).hide)
        self.timeout(11.9, Group(g8, g9, g10).hide)
        self.timeout(14.6, Group(g11, g12).hide)
        self.timeout(16.9, Group(g13, g14, g15).hide)
        self.timeout(20.1, g16.hide)
        self.timeout(21.4, Group(g17, g18).hide)
        self.timeout(24.6, Group(g19, g20).hide)

        speed = 2.55
        duration = 26

        self.play(
            self.camera.anim(rate_func=linear)
                .points.shift(RIGHT * duration * speed),
            duration=duration
        )
