# flake8: noqa
import sys

sys.path.append('.')

from janim.imports import *
from utils.template import *


def get_toprect(**kwargs) -> Rect:
    default_kwargs = dict(
        color=BLACK,
        fill_alpha=1,
        stroke_alpha=0,
        depth=-99,
    )
    toprect = Rect(
        Config.get.frame_width, 1.25,
        **merge_dicts_recursively(default_kwargs, kwargs)
    )
    toprect.points.to_border(UP, buff=0)
    return toprect


class TitleObjTemplate(Template):
    name = ''
    title_kwargs = {}

    def construct(self) -> None:
        self.title = Title(self.name, **self.title_kwargs).fix_in_frame().show()


class TitleTl(TitleTemplate):
    str1 = 'JAnim'
    str2 = '1.0.0 → 1.4.0 更新一览'


class Introduction(Template):
    def construct(self) -> None:
        t = self.aas('1.mp3', 'JAnim 从 1.0.0 到 1.4.0 更新了一些内容')
        self.forward_to(t.end + 0.2)
        t = self.aas('2.mp3', '以下是对这些内容的概览')
        self.forward_to(t.end)

code1 = '''<fc #9cdcfe>t</fc> <fc #d4d4d4>=</fc> <fc #9cdcfe>self</fc><fc #cccccc>.</fc><fc #dcdcaa>play_audio</fc><fc #cccccc>(</fc>
    <fc #4ec9b0>Audio</fc><fc #cccccc>(</fc><fc #ce9178>'107.mp3'</fc><fc #cccccc>),</fc>
    <fc #9cdcfe>begin</fc><fc #d4d4d4>=</fc><fc #b5cea8>0.9</fc><fc #cccccc>,</fc>
    <fc #9cdcfe>end</fc><fc #d4d4d4>=</fc><fc #b5cea8>3.5</fc>
<fc #cccccc>)</fc>
<fc #9cdcfe>self</fc><fc #cccccc>.</fc><fc #dcdcaa>subtitle</fc><fc #cccccc>(</fc><fc #ce9178>'你应该也看到了，可以直接插入音频和字幕'</fc><fc #cccccc>, </fc><fc #9cdcfe>t</fc><fc #cccccc>)</fc>
'''

code2 = '''<fc #9cdcfe>t</fc> <fc #d4d4d4>=</fc> <fc #9cdcfe>self</fc><fc #cccccc>.</fc><fc #dcdcaa>aas</fc><fc #cccccc>(</fc><fc #ce9178>'107.mp3'</fc><fc #cccccc>, </fc><fc #ce9178>'你应该也看到了，可以直接插入音频和字幕'</fc><fc #cccccc>)</fc>'''


class Desc_ShorthandForAudio(TitleObjTemplate):
    name = '对 self.play_audio 和 self.subtitle 的简写'
    title_kwargs = dict(
        depth=-100
    )

    def construct(self) -> None:
        super().construct()

        get_toprect().show()

        self.forward(0.8)

        t = self.aas('3.mp3', '可以发现，比如在之前演示视频的这里')

        img1 = ImageItem('audio_subtitle_old.png', height=5)

        codetxt1 = Text(code1, format=Text.Format.RichText)
        codetxt1.points.scale(0.53).shift(LEFT * 2.6 + DOWN * 0.18)

        lineno = Group(*[
            Text(str(i + 1), font_size=12)
            .points.next_to(line.get_mark_orig(), LEFT).shift(UP * 0.05)
            .r
            for i, line in enumerate(codetxt1)
            if i < 6
        ])

        self.play(
            FadeIn(img1)
        )
        self.play(
            img1.anim.points.scale(3).shift(DR * 1.5 + DOWN * 0.9)
        )
        self.prepare(
            FadeOut(img1),
            FadeIn(codetxt1)
        )
        self.forward_to(t.end)

        t = self.aas('4.mp3', '需要使用 6 行代码才能播放带有字幕的音频')

        self.prepare(Write(lineno), at=0.5)
        self.forward_to(t.end + 0.3)

        t = self.aas('5.mp3', '现在我将它整合为了一行代码')

        codetxt2 = Text(code2, format=Text.Format.RichText)
        codetxt2.points.scale(0.5).next_to(codetxt1, DOWN, aligned_edge=LEFT, buff=MED_LARGE_BUFF)

        self.play(Write(codetxt2), duration=1, at=0.6)
        self.forward_to(t.end)
        self.play(ShowCreationThenDestructionAround(codetxt2))
        self.forward(0.5)

        t = self.aas('6.mp3', '这行代码会自动识别音频前后的空白区段，裁剪出中间的有效区段')

        chart_rect = Rect(3, 2)
        chart_rect.points.shift(RIGHT * 3)
        dl = chart_rect.points.box.get(DL)
        right = chart_rect.points.box.get(DR) - dl
        up = chart_rect.points.box.get(UL) - dl

        graph = VItem(fill_alpha=0.5)
        graph.points.set_as_corners([
            dl + right * x + up * y
            for x, y in [
                (0, 0),
                (0.2, 0),
                (0.25, 0.5),
                (0.3, 0.8),
                (0.35, 0.6),
                (0.5, 0.3),
                (0.55, 0.6),
                (0.6, 0.2),
                (0.65, 0.65),
                (0.7, 0),
                (1, 0)
            ]
        ]).close_path()

        p = dl + 0.2 * right
        line1 = Line(p + DOWN * 0.2, p + up + UP * 0.2, color=YELLOW)
        p = dl + 0.7 * right
        line2 = Line(p + DOWN * 0.2, p + up + UP * 0.2, color=YELLOW)

        clip_rect = Rect(
            line1.points.get_start(),
            line2.points.get_end(),
            color=YELLOW,
            fill_alpha=0.3,
            stroke_alpha=0
        )

        self.prepare(FadeIn(graph))
        self.prepare(
            FadeIn(line1, right * 0.2),
            FadeIn(line2, right * -0.3),
            at=1.5
        )
        self.prepare(FadeIn(clip_rect), at=3)
        self.forward_to(t.end + 1)


class Desc_IndicateSections(TitleObjTemplate):
    name = '对于较长的音频，预览时提示两侧没有显示完全'

    def construct(self) -> None:
        super().construct()
        self.forward()

        imgs = Group(
            ImageItem('indicate1.png', height=3),
            Arrow(),
            ImageItem('indicate2.png', height=3)
        )
        imgs.points.arrange()

        t = self.aas('7.mp3', '例如这个音频只预览了 0~8s')

        self.prepare(FadeIn(imgs[0], scale=1.2), at=0.5)
        self.forward_to(t.end + 0.4)

        t = self.aas('8.mp3', '右边添加了渐变，提示存在未显示的部分')

        self.play(
            GrowArrow(imgs[1]),
            FadeIn(imgs[2], scale=1.2, at=0.3, rate_func=rush_from)
        )
        self.forward_to(t.end + 1)


class Desc_FontTable1(TitleObjTemplate):
    name = '字体列表'
    title_kwargs = dict(
        depth=-100
    )

    def construct(self) -> None:
        super().construct()

        get_toprect(fill_alpha=0.5).show()
        self.forward(0.1)


class Desc_FontTable2(SubtitlesTemplate):
    subtitles = [
        ('101.mp3', '你可以在该列表中搜索可用的字体')
    ]


class Desc_PausePoint1(TitleObjTemplate):
    name = '暂停点 Pause Point'

    def construct(self) -> None:
        super().construct()
        self.forward()


class Desc_PausePoint2(SubtitlesTemplate):
    subtitles = [
        ('9.mp3', '添加了 self.pause_point 用来标记暂停点'),
        ('10.mp3', '并且可以使用 Ctrl+Z 快速移动到前一个暂停点，Ctrl+C 快速移动到后一个'),
        ('11.mp3', '这样可以更方便地控制动画的播放区间')
    ]


class PausePointExample(Timeline):
    CONFIG = Config(
        font='LXGW WenKai Lite'
    )
    def construct(self) -> None:
        txt1 = Text('第一节 42号混凝土')

        self.play(Write(txt1))
        self.pause_point()
        txt1.hide()

        txt2 = Text('第二节 意大利面')

        self.play(FadeIn(txt2, scale=1.2))
        self.pause_point()
        txt2.hide()

        txt3 = Text('第三节 高速运转的机械')

        self.play(DrawBorderThenFill(txt3), duration=1)


class Desc_FixInFrame(TitleObjTemplate):
    name = '将物件固定在屏幕上'

    def construct(self) -> None:
        super().construct()
        self.title.fix_in_frame(False)

        g1 = Group(
            s := Square(fill_alpha=0.5, color=BLUE),
            Group(
                Text('Not fixed in frame'),
                Vector(DOWN * 0.3)
            )
            .points.arrange(DOWN, buff=SMALL_BUFF)
            .next_to(s, UP, buff=SMALL_BUFF).r
        )

        g2 = Group(
            s := Square(fill_alpha=0.5, color=BLUE),
            Group(
                Text('Fixed in frame'),
                Vector(DOWN * 0.3)
            )
            .points.arrange(DOWN, buff=SMALL_BUFF)
            .next_to(s, UP, buff=SMALL_BUFF).r
        ).fix_in_frame()

        g = Group(g1, g2).show()
        g.points.arrange(buff=LARGE_BUFF)

        self.forward()

        t = self.aas('12.mp3', '固定在屏幕上的物件不会随摄像机的移动改变在屏幕上的位置')

        self.prepare(
            self.camera.anim
            .points.rotate(70 * DEGREES, axis=RIGHT),
            at=2
        )
        t2 = self.prepare(
            self.camera.anim
            .points.rotate(-90 * DEGREES, axis=DR),
            at=3
        )

        self.forward_to(max(t.end, t2.end))


class Desc_Editor1(TitleObjTemplate):
    name = '编辑框'

    def construct(self) -> None:
        super().construct()
        self.forward()


class Desc_Editor2(SubtitlesTemplate):
    subtitles = [
        ('13.mp3', '在窗口下方添加了一个输入框，可以快速切换预览的内容')
    ]


code3 = '''<fc #4ec9b0>DataUpdater</fc><fc #cccccc>(</fc>
    <fc #9cdcfe>text</fc><fc #cccccc>,</fc>
    <fc #569cd6>lambda</fc> <fc #9cdcfe>data</fc><fc #cccccc>, </fc><fc #9cdcfe>p</fc><fc #cccccc>:
        </fc><fc #9cdcfe>data</fc><fc #cccccc>.</fc><fc #9cdcfe>points</fc><fc #cccccc>.</fc><fc #dcdcaa>next_to</fc><fc #cccccc>(</fc><fc #9cdcfe>dot</fc><fc #cccccc>.</fc><fc #dcdcaa>current</fc><fc #cccccc>(), </fc><fc #4fc1ff>DOWN</fc><fc #cccccc>),</fc>
    <fc #9cdcfe>root_only</fc><fc #d4d4d4>=</fc><fc #569cd6>False</fc>
<fc #cccccc>)</fc>
'''

code4 = '''<fc #4ec9b0>GroupUpdater</fc><fc #cccccc>(</fc>
    <fc #9cdcfe>text</fc><fc #cccccc>,</fc>
    <fc #569cd6>lambda</fc> <fc #9cdcfe>text</fc><fc #cccccc>, </fc><fc #9cdcfe>p</fc><fc #cccccc>:</fc>
        <fc #9cdcfe>text</fc><fc #cccccc>.</fc><fc #9cdcfe>points</fc><fc #cccccc>.</fc><fc #dcdcaa>next_to</fc><fc #cccccc>(</fc><fc #9cdcfe>dot</fc><fc #cccccc>.</fc><fc #dcdcaa>current</fc><fc #cccccc>(), </fc><fc #4fc1ff>DOWN</fc><fc #cccccc>)</fc>
<fc #cccccc>)</fc>
'''


class Desc_GroupUpdater(TitleObjTemplate):
    name = 'GroupUpdater'

    def construct(self) -> None:
        super().construct()

        self.forward()

        codetxt3 = Text(code3, font_size=12, format=Text.Format.RichText)
        codetxt3.points.next_to(self.title, DOWN, aligned_edge=LEFT) \
            .shift(RIGHT * 0.3)

        dot = Dot()
        dot.points.shift(LEFT * 3 + UP)

        text = Text('ry')

        t = self.aas('14.mp3', '这是 DataUpdater 的效果')
        self.prepare(
            Succession(
                Write(codetxt3, duration=1),
                Wait(0.2),
                AnimGroup(
                    dot.anim.points.shift(DOWN * 2),
                    DataUpdater(
                        text,
                        lambda data, p, dot=dot:
                            data.points.next_to(dot.current(), DOWN),
                        root_only=False
                    )
                )
            )
        )

        self.forward_to(t.end + 1)

        codetxt4 = Text(code4, font_size=12, format=Text.Format.RichText)
        codetxt4.points.next_to(self.title, DOWN).align_to(RIGHT * 0.3, LEFT)

        dot = Dot()
        dot.points.shift(RIGHT * 3 + UP)

        text = Text('ry')

        t = self.aas('15.mp3', '这是 GroupUpdater 的效果')
        self.prepare(
            Succession(
                Write(codetxt4, duration=1),
                Wait(0.2),
                AnimGroup(
                    dot.anim.points.shift(DOWN * 2),
                    GroupUpdater(
                        text,
                        lambda text, p, dot=dot:
                            text.points.next_to(dot.current(), DOWN)
                    )
                )
            )
        )

        self.forward_to(t.end + 1)

        t = self.aas('16.mp3', '对比一下')

        self.forward_to(t.end + 0.3)

        t = self.aas('17.mp3', 'DataUpdater 分别地对每个子物件进行操作')

        rect = Rect(self.title.points.box.width / 2 - 0.4, 5.7, color=YELLOW)
        rect.points.shift(LEFT * 3.1)

        self.prepare(Create(rect, auto_close_path=False))

        self.forward_to(t.end + 0.2)

        t = self.aas('18.mp3', '因此在 DataUpdater 中使用 “next_to” 会使子物件挤在一起')

        self.forward_to(t.end + 0.4)

        t = self.aas('19.mp3', '不同的是')

        self.prepare(
            rect.anim.points.shift(RIGHT * 6.1)
        )

        self.forward_to(t.end + 0.3)

        t = self.aas('20.mp3', 'GroupUpdater 是对整体进行操作')

        self.forward_to(t.end + 0.25)

        t = self.aas('21.mp3', '因此在 GroupUpdater 中使用 “next_to” 会得到正确的结果')

        self.forward_to(t.end + 1)

        self.play(
            rect.anim.points.stretch(0.23, dim=1, about_edge=UP),
            self.camera.anim.points.move_to(rect).scale(0.55).shift(DOWN * 0.5)
        )

        follow = Group(
            Typst('=>'),
            Text(
                '<fc #4ec9b0>Follow</fc><fc #cccccc>(</fc><fc #9cdcfe>text</fc><fc #cccccc>, </fc><fc #9cdcfe>dot</fc><fc #cccccc>, </fc><fc #4fc1ff>DOWN</fc><fc #cccccc>)</fc>',
                font_size=12,
                format=Text.Format.RichText
            )
        )
        follow.points.arrange().next_to(rect, DOWN, aligned_edge=LEFT)

        t = self.aas('22.mp3', '并且我将 GroupUpdater 和 next_to 封装为了 Follow')

        self.prepare(
            FadeIn(follow[0], RIGHT),
            Write(follow[1], at=0.5),
            at=t.end - 1 - self.current_time,
            duration=1
        )

        self.forward_to(t.end + 0.2)

        t = self.aas('23.mp3', '作为一种简写')

        self.forward_to(t.end + 1)


class Desc_Other1(TitleObjTemplate):
    name = '杂项'
    def construct(self) -> None:
        super().construct()
        self.forward()

        t = self.aas(
            '24.mp3',
            '''
            #set text(font: ("Consolas", "Noto Sans S Chinese"))
            还有一些其它新增的#text("（从 manim 抄来的）", size: 0.7em)动画功能
            ''',
            use_typst_text=True
        )

        self.forward_to(t.end)
        self.forward()


'''
Homotopy ComplexHomotopy
MoveAlongPath
ApplyWave WiggleOutThenIn
Wait
'''
