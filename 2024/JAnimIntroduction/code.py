# flake8: noqa
import sys

sys.path.append('.')

from janim.imports import *
from utils.template import *


class TitleTl(TitleTemplate):
    str1 = 'JAnim'
    str2 = '编写开源动画引擎的一次尝试'
    str1_font_size = 36


class WhatIsJAnim(SubtitleTemplate2):
    name = '什么是 JAnim'

    def construct(self) -> None:
        super().construct()

        manim = ImageItem('cropped.png', height=2)

        self.forward()

        t = self.aas('1.mp3', '不少人可能听说过 manim，一个数学动画库')

        self.prepare(FadeIn(manim, scale=1.2), at=0.8)

        self.forward_to(t.end + 0.6)

        t = self.aas('3.mp3', '我之前的这几期视频就是用 manim 做的')

        videos = Group(*[ImageItem(f'video{i+1}.png') for i in range(4)])
        videos.points.arrange()

        self.prepare(
            manim.anim(duration=0.5).points.shift(UP),
            FadeIn(
                videos.points.next_to(manim, DOWN).r,
                UP,
                lag_ratio=0.8
            ),
            at=0.5
        )

        self.forward_to(t.end + 1)

        t = self.aas('4.mp3', '但是，manim(gl) 毕竟偏向于是个人项目')

        self.forward_to(t.end + 0.3)

        t = self.aas('5.mp3', '所以在使用的时候经常会遇到不太顺手的地方')

        loading = SVGItem(
            'Loading.svg',
            stroke_radius=0,
            color=WHITE,
        )
        loading.points.scale(1.3)
        loading(VItem).color.fade(0.5)

        self.prepare(
            DataUpdater(
                loading,
                lambda data, p: data(VItem) \
                    .points.rotate(p.alpha * TAU, about_point=ORIGIN).r \
                    .color.fade(1 - there_and_back_with_pause(p.alpha, pause_ratio=0.8)),
                rate_func=linear,
                root_only=False
            ),
            at=1,
            duration=3
        )

        self.forward_to(t.end + 0.5)

        self.play(
            FadeOut(videos, lag_ratio=0.5)
        )

        self.forward(0.3)

        t = self.aas('6.mp3', '于是，对 manim 的源码进行了细致的挖掘后')

        self.forward_to(t.end + 0.2)

        t = self.aas('7.mp3', '我决定编写一个自己的动画库')

        self.forward_to(t.end + 0.2)

        t = self.aas('8.mp3', '便有了 JAnim')

        janim = ImageItem('janim.png', height=1.2)
        janim.points.next_to(manim, DOWN)

        self.prepare(FadeIn(janim), duration=1.5)

        self.forward_to(t.end)

        self.forward(2)


class Comparison(SubtitleTemplate2):
    name = '与其它工具的对比'

    def construct(self) -> None:
        super().construct()

        self.forward()

        t = self.aas('9.mp3', '在进行详细的介绍之前')

        self.forward_to(t.end + 0.4)

        t = self.aas('10.mp3', '我会将 JAnim 与其它 “类 manim” 工具进行横向对比')

        self.forward_to(t.end)

        tip = Text('有主观倾向，请自行甄别', font_size=16, color=GREY)
        tip.points.next_to(self.title.txt, aligned_edge=DOWN)

        self.play(Write(tip))

        manimgl = ImageItem('manimgl.png', height=1.5)
        manimce = ImageItem('manimce.png', height=1.5)
        janim = ImageItem('janim.png', height=1.5)

        data: list[tuple[str,
                         list[tuple[ImageItem, str,
                                    str, float, float, float | Iterable[float],
                                    str | Iterable[str]]]]] = [
            (
                '1. 文档', [
                    (manimce, '#1', '11.mp3', 0.8, 4.4, [0.5, 1, 1], '源码包含文档，有专门的文档官网'),
                    (janim, '#2', '12.mp3', 0.6, 3.6, 1, '源码包含文档，有专门的文档官网'),
                    (manimgl, '#3', '13.mp3', 0.6, 4.1, 1, '有文档官网，有 Grant 的代码作为参考')
                ]
            ),
            (
                '2. 社区', [
                    (manimce, '#1', '14.mp3', 0.5, 5.2, [0.6, 1, 1], '拥有健全的 discord 社区，提问之后很快就有人回复'),
                    (manimgl, '#2', '15.mp3', 0.8, 5.0, 1, 'MK 有部分人用，绝大多数都在潜水'),
                    (janim, '#3', '16.mp3', 0.5, 1.9, 1, '只有我在用')
                ]
            ),
            (
                '3. 功能多样性', [
                    (manimce, '#1', '17.mp3', 0.6, 3.1, 1, '有相当多的物件和动画'),
                    (manimgl, '#2', '18.mp3', 0.6, 3.0, 1, '有很多的物件和动画'),
                    (janim, '#3', '19.mp3', 0.7, 2.7, 1, '没几种物件和动画')
                ]
            ),
            (
                '4. Python 版本支持', [
                    (manimgl, '#1', '20.mp3', 0.9, 3.4, 1, '要求 3.7 及以上'),
                    (manimce, '#2', '21.mp3', 0.6, 3.0, 1, '要求 3.8 及以上'),
                    (janim, '#3', '22.mp3', 0.5, 3.0, 1, '3.12 及以上才能用')
                ]
            ),
            (
                '5. 平台支持', [
                    (manimce, '#1', '23.mp3', 0.8, 4.2, [0.5, 0.85, 0.85], '支持 Windows、Linux 和 macOS'),
                    (manimgl, '#1', '24.mp3', 0.7, 4.2, 1, '支持 Windows、Linux 和 macOS'),
                    (janim, '#2', '25.mp3', 0.7, 3.8, 1, '我只能保证在我的电脑上是正常的')
                ]
            ),
            (
                '6. 维护', [
                    (manimce, '#1', '26.mp3', 0.9, 2.7, 1, '社区维护'),
                    (janim, '#2', '27.mp3', 0.5, 1.9, 1, '我来维护'),
                    (manimgl, '#3', '28.mp3', 0.3, 5.8, 1, ['自 2022.4.12 的 1.6.1 版后便没有新的发布包', '（github 上有 Grant 的最新更新，但是已经产生了相当大的差异）'])
                ]
            )
        ]

        manimgl.points.move_to(LEFT * 4)
        janim.points.move_to(RIGHT * 4)

        g = Group(manimgl, manimce, janim)

        texts = [
            Text(text).points.next_to(img, DOWN).r
            for text, img in zip(('manimgl', 'manimce', 'janim'), g)
        ]

        self.play(
            *map(FadeIn, g),
            *map(Write, texts)
        )

        rank_color_map = {
            '#1': YELLOW_D,
            '#2': GREY,
            '#3': LIGHT_BROWN
        }

        for i, (cata, lst) in enumerate(data):
            cata_txt = Text(cata)
            anchor = cata_txt[0].get_mark_orig()
            cata_txt.points.shift(manimgl.points.box.get(UL) + UP * 0.5 - anchor)

            self.play(Write(cata_txt))

            self.forward()

            rank_txts = []

            for img, rank, file, begin, end, mul, subt in lst:
                rank_txt = Text(rank)
                if rank in rank_color_map:
                    rank_txt.color.set(rank_color_map[rank])
                rank_txt.points.next_to(img, DOWN, buff=0.8)
                rank_txt.show()
                rank_txts.append(rank_txt)

                t = self.play_audio(
                    Audio(file).mul(mul),
                    begin=begin,
                    end=end
                )
                self.subtitle(
                    subt,
                    delay=0.8,
                    duration=t.duration - 0.7,
                    scale=1 if isinstance(subt, str) else [1, 0.7],
                )
                self.forward_to(t.end + 0.8)

            self.forward(0.5)

            if i != len(data) - 1:
                cata_txt.hide()
                self.prepare(
                    *map(FadeOut, rank_txts),
                    duration=0.5
                )

        self.play(
            *map(FadeOut, it.chain(g, texts, rank_txts,
                                   [cata_txt, self.title, tip]))
        )

        self.forward()

        t = self.aas('29.mp3', '接下来，我们主要谈 JAnim 功能的优缺点',
                     clip=(0.8, 3.2))

        self.forward_to(t.end + 0.4)

        t = self.aas(
            '30.mp3',
            [
                '因此不涉及入门教程的部分',
                '（你可以在文档中看到目前较为简略的入门教程和样例）'
            ],
            scale=(1, 0.7)
        )

        self.forward_to(t.end + 1)


code1 = '''<fc #9cdcfe>circle</fc> <fc #d4d4d4>=</fc> <fc #4ec9b0>Circle</fc><fc #cccccc>(</fc><fc #9cdcfe>color</fc><fc #d4d4d4>=</fc><fc #4fc1ff>BLUE</fc><fc #cccccc>)</fc>
<fc #9cdcfe>square</fc> <fc #d4d4d4>=</fc> <fc #4ec9b0>Square</fc><fc #cccccc>(</fc><fc #9cdcfe>color</fc><fc #d4d4d4>=</fc><fc #4fc1ff>GREEN</fc><fc #cccccc>, </fc><fc #9cdcfe>fill_alpha</fc><fc #d4d4d4>=</fc><fc #b5cea8>0.5</fc><fc #cccccc>)</fc>

<fc #9cdcfe>self</fc><fc #cccccc>.</fc><fc #dcdcaa>play</fc><fc #cccccc>(</fc><fc #4ec9b0>Create</fc><fc #cccccc>(</fc><fc #9cdcfe>circle</fc><fc #cccccc>))</fc>
<fc #9cdcfe>self</fc><fc #cccccc>.</fc><fc #dcdcaa>play</fc><fc #cccccc>(</fc><fc #4ec9b0>Transform</fc><fc #cccccc>(</fc><fc #9cdcfe>circle</fc><fc #cccccc>, </fc><fc #9cdcfe>square</fc><fc #cccccc>))</fc>
<fc #9cdcfe>self</fc><fc #cccccc>.</fc><fc #dcdcaa>play</fc><fc #cccccc>(</fc><fc #4ec9b0>Uncreate</fc><fc #cccccc>(</fc><fc #9cdcfe>square</fc><fc #cccccc>))</fc>'''

code2 = '''<fc #9cdcfe>self</fc><fc #cccccc>.</fc><fc #dcdcaa>play</fc><fc #cccccc>(</fc><fc #4ec9b0>Write</fc><fc #cccccc>(</fc><fc #9cdcfe>txt</fc><fc #cccccc>))</fc>

<fc #9cdcfe>self</fc><fc #cccccc>.</fc><fc #dcdcaa>prepare</fc><fc #cccccc>(</fc>
    <fc #4ec9b0>CircleIndicate</fc><fc #cccccc>(</fc><fc #9cdcfe>txt</fc><fc #cccccc>),</fc>
    <fc #9cdcfe>at</fc><fc #d4d4d4>=</fc><fc #b5cea8>1</fc><fc #cccccc>,</fc>
    <fc #9cdcfe>duration</fc><fc #d4d4d4>=</fc><fc #b5cea8>2</fc>
<fc #cccccc>)</fc>
<fc #9cdcfe>self</fc><fc #cccccc>.</fc><fc #dcdcaa>play</fc><fc #cccccc>(</fc><fc #9cdcfe>txt</fc><fc #cccccc>.</fc><fc #9cdcfe>anim</fc><fc #cccccc>.</fc><fc #9cdcfe>points</fc><fc #cccccc>.</fc><fc #dcdcaa>shift</fc><fc #cccccc>(</fc><fc #4fc1ff>RIGHT</fc><fc #cccccc>), </fc><fc #9cdcfe>duration</fc><fc #d4d4d4>=</fc><fc #b5cea8>2</fc><fc #cccccc>)</fc>
<fc #9cdcfe>self</fc><fc #cccccc>.</fc><fc #dcdcaa>play</fc><fc #cccccc>(</fc><fc #9cdcfe>txt</fc><fc #cccccc>.</fc><fc #9cdcfe>anim</fc><fc #cccccc>.</fc><fc #9cdcfe>points</fc><fc #cccccc>.</fc><fc #dcdcaa>shift</fc><fc #cccccc>(</fc><fc #4fc1ff>LEFT</fc><fc #cccccc>), </fc><fc #9cdcfe>duration</fc><fc #d4d4d4>=</fc><fc #b5cea8>2</fc><fc #cccccc>)</fc>'''


class Functions(SubtitleTemplate2):
    name = 'JAnim 有什么功能'

    def construct(self) -> None:
        super().construct()

        t = self.aas('31.mp3', 'JAnim 在很大程度上受到 manim 的启发')

        self.forward_to(t.end + 0.4)

        t = self.aas('32.mp3', '因此，大部分的基础功能',
                     clip=(0.5, 2.2))

        self.forward_to(t.end + 0.3)

        t = self.aas('33.mp3', '例如几何形状插值、文字书写等效果都是足够完善的')

        self.forward_to(t.end)

        circle = Circle(color=BLUE)
        square = Square(color=GREEN, fill_alpha=0.5)

        code1_text = Text(code1, font_size=16, depth=1, format=Text.Format.RichText)
        code1_text.points.next_to(self.title, DOWN, aligned_edge=LEFT)

        self.play(Write(code1_text[:2]))
        self.forward(0.5)

        self.play(Write(code1_text[3]), duration=1)
        self.play(Create(circle))

        self.play(Write(code1_text[4]), duration=1)
        self.play(Transform(circle, square))

        self.play(Write(code1_text[5]), duration=1)
        self.play(Uncreate(square))

        self.forward()
        self.play(FadeOut(code1_text))

        t = self.aas('34.mp3', '并且 JAnim 也解决了 manim 中的一些痛点',
                     mul=1.3)

        self.forward_to(t.end + 1)

        t = self.aas('35.mp3', '在 JAnim 中，你可以使用 depth 指定绘制的优先级，保证层级关系',
                     mul=1.5, clip=(0.6, 5.0))

        circle = Circle(color=RED, depth=0, fill_alpha=0.9)
        circle.points.shift(LEFT * 1.4)

        text0 = Text('depth=<fc #b5cea8>0</fc>', format=Text.Format.RichText)
        text0.points.next_to(circle, LEFT)

        rect = Rect(color=GREEN, depth=1, fill_alpha=0.9)
        rect.points.shift(RIGHT * 0.5).rotate(-20 * DEGREES)

        text1 = Text('depth=<fc #b5cea8>1</fc>', format=Text.Format.RichText)
        text1.points.next_to(rect, RIGHT)

        self.forward()

        self.prepare(
            *[
                CircleIndicate(text,
                               scale=1.2,
                               rate_func=lambda t: there_and_back_with_pause(t, 0.5))
                for text in (text0, text1)
            ],
            at=2,
            duration=2
        )
        self.play(
            FadeIn(Group(circle, text0, text1)),
            DataUpdater(
                rect,
                lambda data, p: data \
                    .color.fade(1 - smooth(min(1, p.alpha * 4))).r \
                    .points.rotate(PI * p.alpha),
                hide_at_begin=False,
                show_at_end=False,
                become_at_end=False,
                rate_func=linear,
                duration=3
            )
        )
        text0.points.next_to(rect, RIGHT)
        text1.points.next_to(circle, LEFT)
        circle.depth.set(1)
        rect.depth.set(0)
        self.play(
            FadeOut(Group(circle, text0, text1), at=3),
            DataUpdater(
                rect,
                lambda data, p: data \
                    .color.fade(1 - smooth(min(1, (1 - p.alpha) * 4))).r \
                    .points.rotate(PI * p.alpha),
                hide_at_begin=False,
                show_at_end=False,
                become_at_end=False,
                rate_func=linear,
                duration=4
            )
        )

        self.forward()

        t = self.aas('36.mp3', '在 JAnim 中，你可以使用 prepare',
                     mul=1.7)

        self.forward_to(t.end + 0.2)

        t = self.aas('37.mp3', '预先设置之后会进行的动画，而不在时间上前进')

        txt = Text('TEXT')
        txt.points.shift(LEFT * 0.5 + DOWN)

        code2_text = Text(code2, font_size=16, format=Text.Format.RichText)
        code2_text.points.next_to(self.title, DOWN, aligned_edge=LEFT)

        anim_label1 = Group(
            Rect(0.9, 0.3, fill_alpha=0.3),
            Text('Write', font_size=16),
            color=np.array(Write.label_color) / 255
        )

        anim_label2 = Group(
            Rect(1.9, 0.3, fill_alpha=0.3),
            Text('CircleIndicate', font_size=16),
            color=np.array(CircleIndicate.label_color) / 255
        )
        anim_label2.points.shift(RIGHT * 2.5)

        anim_label3 = Group(
            Rect(1.9, 0.3, fill_alpha=0.3),
            Text('.anim', font_size=16),
            color=np.array(MethodTransform.label_color) / 255
        )
        anim_label3.points.shift(RIGHT * 1.5 + DOWN * 0.4)

        time_mark = Line(
            UP * 0.2 + LEFT * 0.5,
            DOWN * 0.6 + LEFT * 0.5,
            color=BLUE
        )

        anim_label4 = anim_label3.copy()
        anim_label4.points.shift(RIGHT * 2)

        labels = Group(
            anim_label1, anim_label2,
            anim_label3, anim_label4,
            time_mark
        )
        labels.points.next_to(self.title, DOWN, aligned_edge=RIGHT)

        self.forward(2)

        self.play(
            Write(code2_text[0], duration=1),
            FadeIn(anim_label1),
            FadeIn(time_mark)
        )

        self.play(
            Write(txt),
            time_mark.anim(rate_func=linear).points.shift(RIGHT)
        )

        self.play(
            Write(code2_text[2:7], duration=1),
            FadeIn(anim_label2)
        )
        self.forward()
        self.play(
            Write(code2_text[7], duration=1),
            FadeIn(anim_label3)
        )
        self.prepare(
            CircleIndicate(txt, rate_func=there_and_back_with_pause),
            at=1,
            duration=3
        )
        self.play(
            txt.anim.points.shift(RIGHT),
            time_mark.anim(rate_func=linear).points.shift(RIGHT * 2),
            duration=2
        )
        self.play(
            Write(code2_text[8], duration=1),
            FadeIn(anim_label4)
        )
        self.play(
            txt.anim.points.shift(LEFT),
            time_mark.anim(rate_func=linear).points.shift(RIGHT * 2),
            duration=2
        )

        self.forward(0.5)

        t = self.aas('38.mp3', '这样给了你在这段时间上创建其它动画的机会',
                     mul=[0.6, 1, 1])

        self.forward_to(t.end + 0.5)

        self.play(
            *map(FadeOut, [code2_text, labels, time_mark, txt])
        )

        self.forward()

        t = self.aas('39.mp3', '在 manim 中，许多动画方法会直接改动原物件的属性')

        self.forward_to(t.end + 0.7)

        t = self.aas(
            '40.mp3',
            '''
            #set text(font: ("Consolas", "Noto Sans S Chinese"))
            #stack(dir: ltr)[
                例如 manim 中 Transform(
            ][
                #circle(radius: 0.4em, fill: rgb("#FC6255"), stroke: none)
            ][
                ,
            ][
                #square(size: 0.8em, fill: rgb("#58C4DD"), stroke: none)
            ][
                ) 的运作原理是在动画过程中
            ]
            ''',
            use_typst_text=True
        )

        circle = Circle(color=RED, fill_alpha=1)
        circle.points.shift(LEFT * 2)
        square = Square(color=BLUE, fill_alpha=1)
        square.points.shift(RIGHT * 2)
        square_bg = Square(color=BLUE, stroke_alpha=0, fill_alpha=0.2, depth=1)
        square_bg.points.shift(RIGHT * 2)

        arrow = Arrow(ORIGIN, DOWN, buff=0)
        arrow.points.next_to(circle, UP)
        tip = Text('被改动')
        tip.points.next_to(circle, DOWN)

        self.forward()

        manim = ImageItem('manimgl.png', height=2)
        manim.points.next_to(self.title, DOWN, aligned_edge=LEFT)

        self.play(*map(FadeIn, (circle, square_bg, manim)))
        self.forward_to(t.end + 0.3)

        t = self.aas(
            '41.mp3',
            '''
            #set text(font: ("Consolas", "Noto Sans S Chinese"))
            #stack(dir: ltr, spacing: 2pt)[
                将插值的结果直接设置到
            ][
                #circle(radius: 0.4em, fill: rgb("#FC6255"), stroke: none)
            ][
                对象上，由
            ][
                #circle(radius: 0.4em, fill: rgb("#FC6255"), stroke: none)
            ][
                来呈现插值的效果
            ]
            ''',
            clip=(0.4, 5.9),
            use_typst_text=True
        )

        self.play(
            *[
                item.anim.points.shift(RIGHT * 4)
                for item in (arrow, tip)
            ],
            Transform(circle, square),
            duration=t.duration
        )
        self.forward()

        t = self.aas('42.mp3', 'JAnim 中的动画方法不会改动原物件的属性')

        self.hide(arrow, tip, square, manim)

        circle_bg = Circle(color=RED, stroke_alpha=0, fill_alpha=0.2, depth=1)
        circle_bg.points.shift(LEFT * 2)

        tip = Text('保持\n不变', depth=0.5)
        tip.points.move_to(circle_bg)

        janim = ImageItem('janim.png', height=1)
        janim.points.next_to(self.title, DOWN, aligned_edge=LEFT)

        self.show(circle_bg, tip, circle, janim)

        self.forward_to(t.end + 0.3)

        t = self.aas('43.mp3', '它完全只是在这个区段中显示插值的效果')

        arrow.points.shift(LEFT * 4)
        arrow.show()
        self.play(
            Transform(circle, square),
            duration=t.duration
        )

        self.forward(0.4)

        t = self.aas(
            '44.mp3',
            '''
            #set text(font: ("Consolas", "Noto Sans S Chinese"))
            #stack(dir: ltr, spacing: 2pt)[
                不会对
            ][
                #circle(radius: 0.4em, fill: rgb("#FC6255"), stroke: none)
            ][
                的属性产生影响
            ]
            ''',
            use_typst_text=True
        )

        self.forward_to(t.end + 0.5)

        self.play(
            *map(FadeOut, (janim, circle_bg, square, square_bg, arrow, tip))
        )
        self.forward(0.5)

        t = self.aas('101.mp3', 'JAnim 的预览窗口下方提供了时间轴控件')
        self.forward_to(t.end + 0.3)

        t = self.aas('102.mp3', '你不仅可以前后调整进度')
        self.forward_to(t.end + 0.2)

        t = self.aas('103.mp3', '而且可以看到标注的动画起止时间')
        self.forward_to(t.end + 1)

        t = self.aas('104.mp3', '并且，在 JAnim 中')
        self.forward_to(t.end + 0.2)

        t = self.aas('105.mp3', '可以一键载入新的内容')
        self.forward_to(t.end + 0.5)

        t = self.aas('106.mp3', '而不必关掉窗口再次开启')
        self.forward_to(t.end + 1.5)

        t = self.aas('107.mp3', '你应该也看到了，可以直接插入音频和字幕')
        self.forward_to(t.end + 0.4)

        t = self.aas('108.mp3', '这样你就可以把配音的工作流整合到动画制作中',
                     clip=(0.4, 3.3))
        self.forward_to(t.end + 1.5)


limits_typ = '''
#set text(font: ("Consolas", "Noto Sans S Chinese"), size: 7pt)
#set par(justify: true)
#set page(width: 550pt)

- JAnim 目前拥有的组件相对较少，一些功能不太完善。可能要等我有特定的需求后，你才能在 JAnim 看到对应的更新。

- #{[
  有一些语法会更啰嗦，比如：

  #table(
    columns: 2,
    inset: 4pt,
    gutter: 2pt,
    fill: (x, y) => {
      if y == 0 {
        blue.lighten(20%)
      } else {
        none
      }
    },
    [manim], [janim],

    `.apply_points_function(...)`, `.points.apply_points_fn(...)`,
    `.next_to(...)`, `.points.next_to(...)`,
    `.set_color(...)`, `.color.set(...)`,
    `.set_stroke(...)`, `.stroke.set(...)`,
    `.set_fill(...)`, `.fill.set(...)`,
  )
  也就是要显式的写出“是在对哪个部分操作，是坐标数据，还是颜色数据？”，不过从另一个角度来看，这种显式语法也许是一种优点？
]}

- 不支持按步模拟，也就是没有提供“根据前一帧的内容决定后一帧”的功能，之后可能会支持。

- JAnim 目前只支持单声道音频（多声道的会先转换）。

- 我并没有对比过，但是我觉得 JAnim 的渲染效率更低。并且我觉得我写渲染器写得很草率，如果你去看这部分的源码应该就能感受到这一点。

- JAnim 没有足够的项目积累，有些潜在的问题需要进行更多的动画开发才能逐步发现。
'''


class Limits(SubtitleTemplate2):
    name = '目前的局限性'

    CONFIG = Config(
        # preview_fps=5
    )

    def construct(self) -> None:
        super().construct()

        self.forward()

        typ = TypstDoc(limits_typ)
        typ(VItem).stroke.set(alpha=None) \
            .r.points.shift(DOWN)

        self.play(Write(typ))
        self.forward(5)
        self.play(FadeOut(self.title), FadeOut(typ))


class Examples(Template):
    def construct(self) -> None:
        t = self.aas('201.mp3', '虽然说目前没有足够的项目积累',
                     clip=None)

        self.forward_to(t.end + 1)

        t = self.aas('202.mp3', '但是也有一些可供参考的实例',
                     clip=None)

        self.forward_to(t.end + 1)

        t = self.aas('203.mp3', '我也整了点活',
                     clip=None)

        self.forward_to(t.end + 1)

        t = self.aas('204.mp3', '以上就是对 JAnim 特性的介绍，如果你有兴趣，欢迎来提 issue 和 PR',
                     clip=None)

        self.forward_to(t.end + 1)

        txt = Group(
            *[
                Text(line)
                for line in (
                    '（见简介）',
                    'github: https://github.com/jkjkil4/JAnim',
                    'gitee: https://gitee.com/jkjkil4/JAnim',
                    '文档: janim.rtfd.io',
                    'QQ群: 970174336'
                )
            ]
        ).show()
        txt.points.arrange(DOWN)

        self.forward(2)

        txt.hide()
        self.forward()


class SpecialThanks(SubtitleTemplate2):
    CONFIG = Config(
        font='LXGW WenKai Lite'
    )
    name = '特别鸣谢'

    def construct(self) -> None:
        super().construct()

        self.forward()

        content1 = Group(
            Text('Grant Sanderson (3Blue1Brown)'),
            ImageItem('3b1b.png'),
            Text('JAnim 大量借鉴自他开发的 manim', font_size=20)
        )
        content2 = Group(
            Text('manim-kindergarten 群友'),
            ImageItem('mk.png')
        )
        content3 = Group(
            Text('凡人忆拾'),
            ImageItem('yishi.png'),
            Text(
                '在他的 manim3 发布之前，JAnim 更偏向于是对 manim 的复刻，\n'
                '虽然提供了对增量动画的支持，但是仍无法自由地控制时间进度。\n'
                '\n'
                '在 manim3 发布后，我下定决心进行了大重构，形成了现在的架构。',
                font_size=20
            )
        )

        refactor = ImageItem('refactor.png')
        refactor.points.shift(DOWN * 0.3)

        rect = boolean_ops.Difference(
            SurroundingRect(refactor),
            Rect(UP * 3, DOWN * 3 + RIGHT * 0.8),
            stroke_alpha=0,
            fill_alpha=0.6,
            fill_color=BLACK
        )

        for content in (content1, content2, content3):
            content.points.arrange(DOWN, aligned_edge=LEFT) \
                .next_to(self.title, DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)

        self.play(
            Succession(
                DrawBorderThenFill(content1[0]),
                FadeIn(content1[1]),
                Write(content1[2])
            )
        )
        self.forward()
        self.play(FadeOut(content1))
        self.play(
            Succession(
                DrawBorderThenFill(content2[0]),
                FadeIn(content2[1])
            )
        )
        self.forward()
        self.play(FadeOut(content2))
        self.forward()
        self.play(
            Succession(
                DrawBorderThenFill(content3[0]),
                FadeIn(content3[1]),
                Write(content3[2], duration=4)
            )
        )
        self.forward(2)
        self.play(FadeOut(content3), FadeIn(refactor))
        self.play(FadeIn(rect))
        self.forward(2)
        self.play(FadeOut(rect), FadeOut(refactor))
        self.forward()
