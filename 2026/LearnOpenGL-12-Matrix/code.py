# flake8: noqa
import sys

sys.path.append('.')

from janim.imports import *

with reloads():
    from template import *
    from template.audio import seq_play_audio_with_subtitles
from template import *
from template.audio import seq_play_audio_with_subtitles


def colorize_typ(typ: TypstDoc) -> None:
    patterns = [
        ('i', RED),
        ('j', GREEN)
    ]
    for pa, co in patterns:
        if not isinstance(typ, TypstMath):
            pa = f'${pa}$'
        try:
            typ[pa, ...].set(color=co)
        except PatternMismatchError:
            pass


class Cursor(MarkedItem, SVGItem):
    def __init__(self, **kwargs):
        super().__init__('cursor.svg', height=0.5, **kwargs)
        self.mark.set_points([[-0.12, 0.2, 0]])


class SharpDelimTemplate(Template):
    CONFIG = Config(
        typst_shared_preamble=Template.CONFIG.typst_shared_preamble + t_(
            R'''
            #set math.mat(delim: "[")

            #import "@janim/colors:0.0.0": *
            '''
        )
    )


class TLTitle(TitleTemplate):
    str1 = 'Learn OpenGL'
    str2 = '矩阵'


class TL1(SharpDelimTemplate):
    def construct(self):
        seq_play_audio_with_subtitles(
            self,
            [
                { 'file': 'audio_12_1.wav', 'begin': 0, "end": 12, 'delay': 0, 'mul': 1.25 },
                { 'file': 'audio_12_1.wav', 'begin': 12.3, "end": 15.2, 'delay': 0, 'mul': 1.25 },
                { 'file': 'audio_12_1.wav', 'begin': 15.2, "end": 35, 'delay': 0.7, 'mul': 1.25 },
            ]
        )

        ####################################################

        txt = Text('矩阵')
        typ = TypstMath('mat(#box(width: 7em, height: 5em))')

        typ1 = TypstText(
            R'''
            #let bo(body) = {
                set align(horizon)
                box(body, width: 1em, height: 1em)
            }
            #set text(size: 1.5em)
            $
                mat(
                    bo(1), bo(2), bo(3);
                    bo(4), bo(5), bo(6)
                )
            $
            '''
        )

        # typ1.show()
        r1 = SweepRect(Group(typ1[1], typ1[3], typ1[5]))
        r2 = SweepRect(Group(typ1[2], typ1[4], typ1[6]))
        r3 = SweepRect(typ1[1:3])
        r4 = SweepRect(typ1[3:5])
        r5 = SweepRect(typ1[5:7])

        yellowtyp = typ1[1, 3, 5, 2, 4, 6].copy().set(color=YELLOW, depth=-1, glow_alpha=0.5)

        typ2t3 = TypstMath('2 times 3', scale=1.5)
        typ2t3['2'].set(color=RED)
        typ2t3['3'].set(color=GREEN)
        typ2t3.points.next_to(typ1, buff=MED_LARGE_BUFF)

        typi = TypstMath('i = 1 ->')
        typj = TypstMath(R'j = 2 \ arrow.b')

        typij = TypstMath('(i, j)')

        typi2 = TypstMath('i = 2 ->')
        typj2 = TypstMath(R'j = 1 \ arrow.b')

        for t in (typi, typj, typij, typi2, typj2):
            colorize_typ(t)

        typi.points.shift([-1.99, 0.44, 0.0])
        typj.points.shift([0.0, 1.25, 0.0])
        typij.points.shift([-2.24, 1.51, 0.0])
        typi2.points.shift([-2.01, -0.36, -0.0])
        typj2.points.shift([-0.8, 1.26, 0.0])

        ####################################################

        self.forward(4)
        self.play(Write(txt))
        self.forward(2.7)
        self.play(
            txt.anim.color.fade(0.5),
            FadeIn(typ, scale=0.5)
        )
        self.forward(0.2)
        self.play(
            Transform(typ, typ1),
            txt.anim.points.shift(UP * 2),
            duration=0.8
        )

        self.play(
            SweepRect.ins(r1, r2, lag_ratio=0.5),
            SweepRect.outs(r1, r2, lag_ratio=0.5),
            lag_ratio=1,
            duration=1
        )

        self.play(
            SweepRect.ins(r3, r4, r5, lag_ratio=0.5),
            SweepRect.outs(r3, r4, r5, lag_ratio=0.5),
            lag_ratio=1,
            duration=1
        )

        self.forward(0.5)

        self.play(
            ShowSubitemsOneByOne(yellowtyp),
            duration=2
        )

        self.forward(0.6)

        self.play(
            SweepRect.ins(r1, r2, lag_ratio=0.2),
            SweepRect.outs(r1, r2, lag_ratio=0.2),
            lag_ratio=1,
            duration=0.7
        )

        self.play(
            SweepRect.ins(r3, r4, r5, lag_ratio=0.2),
            SweepRect.outs(r3, r4, r5, lag_ratio=0.2),
            lag_ratio=1,
            duration=0.7
        )

        self.play(Write(typ2t3))
        self.forward(3)

        self.play(Write(typij))
        self.forward(1)

        self.play(
            FadeOut(txt),
            Write(typi),
            Write(typj, at=1.2)
        )

        self.play(
            SweepRect.ins(r1, r4)
        )
        self.forward()
        self.play(
            typ2t3.anim.points.scale(0.6).next_to(typij, UP),
            duration=1.6
        )
        self.forward(1.5)

        self.play(
            SweepRect.outs(r1, r4, duration=0.3),
            AnimGroup(
                TransformMatchingDiff(typi, typi2),
                TransformMatchingDiff(typj, typj2),
                duration=1
            ),
            SweepRect.ins(r2, r3, duration=0.4),
            lag_ratio=0.7
        )
        self.forward(2.5)
        self.play(CircleIndicate(typ1[2], rate_func=there_and_back_with_pause), duration=2)

        self.play(FadeOut(Group(typi2, typj2, r2, r3, typ1, typ2t3, typij)))

        self.forward(0.4)


class TL2(SharpDelimTemplate):
    def construct(self):
        seq_play_audio_with_subtitles(
            self,
            [
                { 'file': 'audio_12_1.wav', 'begin': 35, 'end': 55.5, 'mul': 1.25 }
            ]
        )

        ####################################################

        typ1 = TypstText(
            R'''
            #let bo(body) = {
                set align(horizon)
                box(body, width: 1em, height: 1em)
            }
            #set text(size: 1.5em)
            $
                mat(
                    bo(1), bo(2), bo(3);
                    bo(4), bo(5), bo(6)
                )
            $
            '''
        )
        typ1.points.shift(LEFT * 2.5)

        img = ImageItem('container.jpg', height=2)
        img.points.shift(RIGHT * 3)

        def get_xy(x: str, y: str, item: Points, reverse=False):
            typ1 = TypstMath(x, color=RED, scale=1.5, glow_alpha=0.7, glow_color=RED)
            typ1.points.next_to(item, LEFT if reverse else UP, buff=0.4)
            typ2 = TypstMath(y, color=GREEN, scale=1.5, glow_alpha=0.7, glow_color=GREEN)
            typ2.points.next_to(item, UP if reverse else LEFT, buff=0.4)

            return typ1, typ2

        typi, typj = get_xy('i', 'j', typ1, True)
        typx, typy = get_xy('x', 'y', img)

        ####################################################

        self.play(FadeIn(typ1), FadeIn(img))
        self.play(FadeIn(typi, scale=0.5), FadeIn(typj, scale=0.5), lag_ratio=0.5)
        self.forward(0.5)
        self.play(FadeIn(typx, scale=0.5), FadeIn(typy, scale=0.5), lag_ratio=0.5)
        self.forward(2)
        self.play(
            FadeOut(Group(typi, typj, typx, typy, img)),
            typ1.anim.points.to_center()
        )
        self.forward(2)

        ####################################################

        r1 = SweepRect(Group(typ1[1], typ1[3], typ1[5]))
        r2 = SweepRect(Group(typ1[2], typ1[4], typ1[6]))
        r3 = SweepRect(typ1[1:3])
        r4 = SweepRect(typ1[3:5])
        r5 = SweepRect(typ1[5:7])

        ####################################################

        self.play(
            SweepRect.ins(r1, r2, lag_ratio=0.3, duration=0.4),
            SweepRect.outs(r1, r2, lag_ratio=0.3, duration=0.4),
            lag_ratio=1
        )
        self.play(
            SweepRect.ins(r3, r4, r5, lag_ratio=0.3, duration=0.4),
            SweepRect.outs(r3, r4, r5, lag_ratio=0.3, duration=0.4),
            lag_ratio=1
        )
        self.forward(0.5)
        self.play(FadeOut(typ1))
        self.forward(4.5)

        ####################################################

        _p = '#let bb = box(width: 2em, height: 2em)'
        typo1 = TypstMath('mat(bb) plus.minus circle.filled', preamble=_p)
        typo2 = TypstMath('mat(bb) plus.minus mat(bb)', preamble=_p)
        typo3 = TypstMath('mat(bb) dot mat(bb)', preamble=_p)

        typo1.points.shift([-0.92, 1.82, 0.0])
        typo2.points.shift([-2.84, -1.07, -0.0])
        typo3.points.shift([3.19, -1.48, 0.0])

        ####################################################

        self.play(
            FadeIn(typo1, scale=1.5),
            FadeIn(typo2, scale=1.5),
            FadeIn(typo3, scale=1.5),
            lag_ratio=0.3
        )
        self.forward(1.5)
        self.play(FadeOut(Group(typo1, typo2, typo3)))

        self.forward(0.3)


class OpersTypes(Text):
    def __init__(self):
        super().__init__(
            '矩阵与标量计算\n'
            '矩阵与矩阵加减\n'
            '矩阵乘法: 矩阵与向量相乘\n'
            '矩阵乘法: 矩阵与矩阵相乘',
            color=BLUE_A,
            depth=-1000
        )
        self.points.scale(0.8).arrange(DOWN, aligned_edge=LEFT).to_border(UL)
        self.fix_in_frame()


class TL3(SharpDelimTemplate):
    def construct(self):
        seq_play_audio_with_subtitles(
            self,
            [
                { 'file': 'audio_12_2.wav', 'begin': 0, 'end': 9, 'delay': 1.6, 'mul': 1.25 },
            ]
        )

        ####################################################

        opertypes = OpersTypes()

        def get_typ(op: str, digits: int | None = None) -> TypstMath:
            typop = {
                '+': '+',
                '-': '-',
                '*': 'times',
                '/': 'div'
            }[op]
            v = [
                eval(f'{x} {op} 3')
                for x in '1234'
            ]
            if digits is not None:
                v = [
                    round(x, digits)
                    for x in v
                ]
            typ = TypstMath(
                fR'''
                mat(1,2;3,4) {typop} 3
                =
                mat(1 {typop} 3,2 {typop} 3;3 {typop} 3,4 {typop} 3)
                =
                mat({v[0]}, {v[1]}; {v[2]}, {v[3]})
                '''
            )
            for t in typ[f'{typop} 3', ...]:
                t[1:].set(color=GREEN_D)
            return typ

        typ1 = get_typ('+')
        typ2 = get_typ('-')
        typ3 = get_typ('*')
        typ4 = get_typ('/', digits=2)
        for t in (typ2, typ3, typ4):
            t.match_pattern(typ1, '=')

        typ1_parts = Group(
            typ1[0],    # 0: [
            typ1[1:3],  # 1: 1;3
            typ1[3:5],  # 2: 2;4
            typ1[5],    # 3: ]
            typ1[6:8],  # 4: +3
            typ1[8],    # 5: =
            typ1[9],    # 6: [
            Group(typ1[10], typ1[13]),          # 7: 1;3
            Group(typ1[11:13], typ1[14:16]),    # 8: +3
            Group(typ1[16], typ1[19]),          # 9: 2;4
            Group(typ1[17:19], typ1[20:22]),    # 10: +3
            typ1[22],   # 11: ]
            typ1[23:],  # 12: = [...]
        )

        ####################################################

        self.play(Write(opertypes))
        self.play(opertypes[0].anim.color.set(YELLOW))

        self.play(Write(typ1_parts[:5]))
        self.forward(3)
        self.play(
            Write(typ1_parts[5]),
            FadeIn(typ1_parts[6, 11], scale=0.8),
            Transform(typ1_parts[1, 2], typ1_parts[7, 9], hide_src=False, path_arc=-PI / 2),
        )
        self.play(
            Transform(typ1_parts[4], typ1_parts[8, 10], flatten=True, hide_src=False)
        )
        self.play(
            Write(typ1_parts[12])
        )

        for t1, t2 in it.pairwise([typ1, typ2, typ3, typ4]):
            self.play(
                TransformMatchingDiff(t1, t2),
                duration=0.8
            )
            self.forward(0.3)

        self.play(FadeOut(typ4))


class TL4(SharpDelimTemplate):
    def construct(self):
        seq_play_audio_with_subtitles(
            self,
            [
                { 'file': 'audio_12_2.wav', 'begin': 9, 'end': 20, 'delay': 0.2, 'mul': 1.25 },
            ]
        )

        ####################################################

        opertypes = OpersTypes().show()
        opertypes[0].set(color=YELLOW)

        typ = TypstMath(
            R'''
            mat(1, 2; 3, 4) + mat(5, 6; 7, 8)
            =
            mat(1+5, 2+6; 3+7, 4+8)
            =
            mat(6, 8; 10, 12)
            '''
        )
        typ[1, 3, 8, 10, 15, 17, 21, 23, 30, 33].set(color=RED)
        typ[2, 4, 9, 11, 18, 20, 24, 26].set(color=GREEN)
        Group(typ[31:33], typ[34:36]).set(color=GREEN)

        typp = Group(
            typ[0],         #  0: [
            typ[1:3],       #  1:
            typ[3:5],       #  2:
            typ[5],         #  3: ]
            typ[6],         #  4: +
            typ[7],         #  5: [
            typ[8:10],      #  6:
            typ[10:12],     #  7:
            typ[12],        #  8: ]
            typ[13],        #  9: =
            typ[14],        # 10: [
            typ[15, 18],    # 11:
            typ[16, 19],    # 12: ++
            typ[17, 20],    # 13:
            typ[21, 24],    # 14:
            typ[22, 25],    # 15: ++
            typ[23, 26],    # 16:
            typ[27],        # 17: ]
            typ[28],        # 18: =
            typ[29],        # 19: [
            typ[30:33],     # 20:
            typ[33:36],     # 21:
            typ[36],        # 22: ]
        )

        ####################################################

        self.play(
            opertypes[0].anim.set(color=GREY),
            opertypes[1].anim.set(color=YELLOW)
        )
        self.play(
            Write(typp[:10])
        )
        self.forward(2)
        self.play(
            FadeIn(typp[10,17], scale=0.8),
            Transform(typp[1,6,2,7], typp[11,13,14,16], hide_src=False, path_arc=-PI / 2)
        )
        self.play(
            FadeIn(typp[12, 15])
        )
        self.play(
            Write(typp[18:])
        )
        self.forward(2)
        self.play(
            FadeOut(typ)
        )
        self.forward(0.5)


class TL5(SharpDelimTemplate):
    def construct(self):
        seq_play_audio_with_subtitles(
            self,
            [
                { 'file': 'audio_12_3.wav', 'begin': 0, 'end': 21, 'delay': 0, 'mul': 1.25 },
                { 'file': 'audio_12_3.wav', 'begin': 30.2, 'end': 34, 'delay': 0.3, 'mul': 1.25 },
            ]
        )

        ####################################################

        opertypes = OpersTypes().show()
        opertypes[0].set(color=GREY)
        opertypes[1].set(color=YELLOW)

        cursor = Cursor()
        cursor.points.shift([-3.03, 2.13, 0.0])

        ####################################################

        self.play(
            opertypes[1].anim.set(color=GREY)
        )
        self.forward(5.6)
        self.play(
            FadeIn(cursor, UL + UP, rate_func=rush_from)
        )
        self.forward(0.6)
        self.play(
            cursor.anim(path_arc=-PI).points.shift([-0.01, -0.51, -0.0])
        )
        self.forward()
        self.play(
            FadeOut(cursor)
        )
        self.play(
            opertypes[2].anim.set(color=YELLOW)
        )

        ####################################################

        typ1 = TypstMath(
            R'''
            mat(3, 1; 1, 2) dot 4 = mat(12, 4; 4, 8)
            '''
        )
        Group(typ1[1], typ1[3], typ1[10:12], typ1[13]).set(color=RED)
        typ1[2, 4, 12, 14].set(color=GREEN)

        eqidx = typ1.index(typ1['='][0])

        typ2 = TypstMath(
            R'''
            mat(3, 1; 1, 2) vec(1, 1) = "?"
            '''
        )
        typ2.patterns('3', ('1', 1)).set(color=RED)
        typ2.patterns('1', '2').set(color=GREEN)
        typ2.match_pattern(typ1, 'mat(3, 1; 1, 2)')

        hl = HighlightRect(typ1[:6], glow_alpha=0.5)

        ####################################################

        self.play(
            Write(typ1[:eqidx])
        )
        self.play(
            Write(typ1[eqidx:])
        )
        self.forward(3.5)
        self.play(
            Transform(typ1[:6], typ2[:6]),
            FadeOut(typ1[6:]),
            Write(typ2[6:])
        )
        self.forward(4)
        self.play(
            FadeIn(hl)
        )
        self.forward(1.6)
        self.play(
            FadeOut(Group(hl, typ2))
        )

        # self.forward()


def apply_bgshadow(vitem: VItem, radius=0.05, alpha=0.4) -> None:
    vitem.set(stroke_background=True, stroke_radius=radius)
    vitem.stroke.set(BLACK, alpha)


class TL6(SharpDelimTemplate):
    def construct(self):
        seq_play_audio_with_subtitles(
            self,
            [
                { 'file': 'audio_12_3.wav', 'begin': 34, 'end': 137, 'delay': 0.3, 'mul': 1.25 },
            ]
        )

        ####################################################

        opertypes = OpersTypes().show()
        opertypes[:2].set(color=GREY)
        opertypes[2].set(color=YELLOW)

        plane = NumberPlane(faded_line_ratio=0, axis_config={'include_numbers': True}, depth=10)
        lines = plane.background_lines
        numbers = Group(plane.x_axis.numbers, plane.y_axis.numbers)

        vec1 = Vector([1, 0], color=RED_A)
        typ1 = TypstMath('vec(1, 0)', scale=0.7, depth=-1)
        typ1.points.next_to(vec1, UR, buff=0)
        vec2 = Vector([0, 1], color=GREEN_A)
        typ2 = TypstMath('vec(0, 1)', scale=0.7, depth=-1)
        typ2.points.next_to(vec2, UR, buff=0)

        vec3 = Vector([3, 1], color=RED_A, alpha=0.35)
        typ3 = TypstMath('vec(3, 1)', scale=0.7, depth=-1)
        typ3.points.next_to(vec3, UR, buff=0)
        vec4 = Vector([1, 2], color=GREEN_A, alpha=0.35)
        typ4 = TypstMath('vec(1, 2)', scale=0.7, depth=-1)
        typ4.points.next_to(vec4, UR, buff=0)

        for t in (typ1, typ2, typ3, typ4):
            t[1].set(color=RED)
            t[2].set(color=GREEN)

        typm = TypstMath('mat(3, 1; 1, 2)', scale=2)
        typm[1, 3].set(color=RED)
        typm[2, 4].set(color=GREEN)
        typm.points.shift([-5.53, 0.31, 0.0])

        for t in (typm, typ3, typ4):
            apply_bgshadow(t(VItem))

        r1 = SweepRect(typm[1:3], stroke_background=True)
        r2 = SweepRect(typm[3:5], stroke_background=True)

        ####################################################

        self.play(Create(plane, lag_ratio=0.05))
        self.forward(4)
        self.play(
            GrowArrow(vec1),
            GrowArrow(vec2),
            AnimGroup(
                FadeIn(typ1),
                FadeIn(typ2),
                at=0.4
            ),
            duration=3
        )
        self.forward(1.6)
        lines.save_state()
        self.play(
            lines.anim.set(color=YELLOW_D)
        )
        self.forward()
        self.play(
            lines.anim.load_state()
        )
        self.play(
            FadeIn(typm)
        )
        self.forward(2)
        self.play(
            SweepRect.ins(r1, r2, lag_ratio=0.5)
        )
        self.forward(4)
        self.play(
            GrowArrow(vec3),
            GrowArrow(vec4)
        )
        _Transform = partial(Transform, flatten=True, hide_src=False, path_arc=PI / 2, rate_func=ease_inout_quint)
        self.play(
            _Transform(r1, typ3),
            _Transform(r2, typ4),
            lag_ratio=1,
            duration=3
        )
        self.forward(1)

        ####################################################

        plane1 = NumberPlane(faded_line_ratio=0, depth=10)
        plane_orig = plane1.copy().set(alpha=0.25)
        plane2 = plane1.copy()
        plane2.points.apply_matrix([[3, 1], [1, 2]])

        vec3f = vec3.copy().set(alpha=1)
        vec4f = vec4.copy().set(alpha=1)

        g1 = Group(plane1, vec1, vec2).save_state()
        g2 = Group(plane2, vec3f, vec4f).save_state()

        typ1.save_state()
        typ2.save_state()

        typv = TypstMath('vec(1, 1)', scale=1.5)
        typv.points.next_to(typm)
        apply_bgshadow(typv(VItem))

        dot1 = Dot([1, 1, 0])
        dot2 = Dot([4, 3, 0])

        ####################################################

        self.play(
            FadeOut(Group(numbers))
        )
        self.forward(2)
        plane.hide()
        plane1.show()
        self.play(
            Indicate(vec1, scale_factor=1.6),
            Indicate(vec2, scale_factor=1.6),
            duration=2
        )
        self.forward()
        self.play(
            FadeIn(plane_orig, duration=0.5),
            Transform(g1, g2),
            typ1.anim.points.next_to([3, 1, 0], UR, buff=0),
            typ2.anim.points.next_to([1, 2, 0], UR, buff=0),
            FadeOut(typ1),
            FadeOut(typ2),
            duration=6
        )

        self.play(
            Flash(typ3, flash_radius=0.5),
            Flash(typ4, flash_radius=0.5),
        )

        self.forward(0.5)
        self.play(
            FadeOut(plane_orig)
        )
        self.play(
            FadeIn(plane_orig)
        )
        self.forward(6.7)
        self.play(
            ShowCreationThenFadeAround(typm)
        )

        self.play(
            FadeOut(g2),
            FadeIn(g1),
        )
        plane_orig.hide()

        self.forward(2)

        self.play(
            FadeIn(typv),
            duration=2
        )
        self.forward(2)
        self.play(
            Transform(typv, dot1, flatten=True, hide_src=False)
        )
        self.play(
            Flash(dot1, flash_radius=0.4)
        )
        self.play(
            FadeIn(plane_orig, duration=0.5),
            Transform(g1, g2),
            Transform(dot1, dot2),
            duration=2
        )
        self.play(
            Flash(dot2, flash_radius=0.4)
        )

        # self.forward()

        self.play(
            FadeOut(g2),
            FadeOut(dot2),
            FadeIn(g1),
            FadeIn(dot1)
        )
        plane_orig.hide()

        self.forward()

        ####################################################

        tr = ValueTracker({
            'v1': [1, 0],
            'v2': [0, 1]
        })

        def typfj_updater(p=None):
            def stringify(lst: list[float]):
                sfy_x = lambda x: f'{x:.1f}'.replace('.', '&.').removesuffix('.0')

                return ','.join(
                    f'#text({c}, ${sfy_x(x)}$)'
                    for x, c in zip(lst, ['RED', 'GREEN'])
                )

            v = tr.current().get_value()
            v1 = stringify(v['v1'])
            v2 = stringify(v['v2'])

            typfj = TypstMath(
                fR'''
                vec(1,1) = 1 dot vec({v1}) + 1 dot vec({v2})
                '''
            )
            typfj.points.next_to([-4.64, -1.75, 0])
            apply_bgshadow(typfj(VItem))
            return typfj

        typfj = typfj_updater()

        typml = TypstMath('mat(3, 1; 1, 2)')
        typml[1, 3].set(color=RED)
        typml[2, 4].set(color=GREEN)
        typml.points.next_to(typfj, LEFT, buff=SMALL_BUFF)
        apply_bgshadow(typml(VItem))

        typr = TypstMath('= vec(4, 3)')
        typr.points.next_to(typfj, buff=SMALL_BUFF)
        apply_bgshadow(typr(VItem))

        ####################################################

        self.play(
            Write(typfj[:5]),
            Transform(typfj[1], typfj[5], hide_src=False, path_arc=-PI / 2),
            FadeTransform(vec1, typfj[6:11], hide_src=False),
            AnimGroup(
                Write(typfj[11]),
                Transform(typfj[2], typfj[12], hide_src=False, path_arc=PI / 2),
            ),
            FadeTransform(vec2, typfj[13:], hide_src=False),
            lag_ratio=1
        )
        self.forward(0.5)
        self.play(
            FadeIn(plane_orig, duration=0.5),
            Transform(g1, g2),
            Transform(dot1, dot2),
            FadeIn(typml),
            tr.anim.set_value({'v1': [3, 1], 'v2': [1, 2]}),
            ItemUpdater(typfj, typfj_updater),
            duration=4.6
        )
        self.play(
            ShowPassingFlashAround(typfj[5]),
            ShowPassingFlashAround(typfj[12]),
        )
        self.forward(2)
        _Flash = partial(Flash, flash_radius=0.6)
        self.play(
            AnimGroup(
                _Flash(typfj[7:11]),
                _Flash(typ3),
            ),
            Wait(),
            AnimGroup(
                _Flash(typfj[14:]),
                _Flash(typ4),
            ),
            lag_ratio=1
        )
        self.play(
            Write(typr)
        )

        self.forward(2)

        dot1.points.move_to([-1, 2, 0])
        self.play(
            FadeOut(g2),
            FadeOut(dot2),
            FadeOut(Group(typml, typfj, typr, typv)),
            FadeIn(g1),
        )
        plane_orig.hide()
        dot2.points.move_to([-1, 3, 0])

        self.forward()

        ####################################################

        typv = TypstMath('vec(-1, 2)', scale=1.5)
        typv.points.next_to(typm)
        apply_bgshadow(typv(VItem))

        typeq = TypstMath(
            R'''
            mat(3, 1; 1, 2) vec(-1,2)
            =
            (-1) dot vec(3, 1) + 2 dot vec(1, 2)
            =
            vec(-1, 3)
            '''
        )
        typeq[1, 3, 18, 25].set(color=RED)
        typeq[2, 4, 19, 26].set(color=GREEN)
        apply_bgshadow(typeq(VItem))
        typeq.points.shift([-1.5, -1.89, -0.0])

        ####################################################

        self.play(
            Write(typv, duration=1),
            FadeIn(dot1, scale=0.2),
            lag_ratio=0.5
        )
        self.forward(0.6)
        self.play(
            FadeIn(plane_orig, duration=0.5),
            Transform(g1, g2),
            Transform(dot1, dot2),
            Write(typeq[:11]),
            duration=2.5
        )
        self.play(
            Write(typeq[11:21]),
            Write(typeq[21:28]),
            Write(typeq[28:]),
            lag_ratio=1.2
        )
        self.play(
            ShowPassingFlashAround(typeq[29:])
        )
        self.play(
            Flash(dot2, flash_radius=0.4)
        )

        self.forward()
        self.play(
            FadeOut(g2),
            FadeOut(dot2),
            FadeIn(g1),
            FadeOut(Group(typv, typeq))
        )
        plane_orig.hide()

        self.forward()

        self.play(
            FadeIn(plane_orig, duration=0.5),
            Transform(g1, g2),
            duration=4
        )

        self.play(
            FadeOut(Group(g2, plane_orig, typm, vec3, vec4, typ3, typ4, r1, r2))
        )


class TL7(SharpDelimTemplate):
    def construct(self):
        seq_play_audio_with_subtitles(
            self,
            [
                { 'file': 'audio_12_3.wav', 'begin': 137, 'end': 187, 'delay': 0.2, 'mul': 1.25 },
            ]
        )

        ####################################################

        opertypes = OpersTypes().show()
        opertypes[:2].set(color=GREY)
        opertypes[2].set(color=YELLOW)

        typ1 = TypstMath(
            R'''
            mat("?", "?"; "?", "?")
            dot
            mat("?", "?"; "?", "?")
            dot
            vec("?", "?")
            ''',
            scale=1.5
        )
        arrow = Arrow(RIGHT * 2, LEFT * 2, color=YELLOW)
        arrow.points.shift(DOWN * 1.5)

        mat2 = typ1[:13]

        hl1 = HighlightRect(typ1[7:], glow_alpha=0.5)
        hl2 = HighlightRect(typ1, buff=MED_SMALL_BUFF, glow_alpha=0.5)

        hl3 = HighlightRect(mat2, glow_alpha=0.5)

        typ2 = TypstMath('mat(1, 2; 3, 4) dot mat(5, 6; 7, 8)', scale=1.5)
        typ2[1, 3].set(color=RED)
        typ2[2, 4].set(color=GREEN)
        typ2[8:10].set(color=BLUE)
        typ2[10:12].set(color=PURPLE)

        ####################################################

        self.forward(0.3)
        self.play(
            Write(typ1[::-1])
        )
        self.forward(2.7)
        self.play(
            GrowArrow(arrow),
            duration=2
        )
        self.forward(1.5)
        self.play(
            FadeIn(hl1)
        )
        self.forward(3.5)
        self.play(
            hl1.anim.set(fill_alpha=1e-5),
            FadeIn(hl2)
        )
        self.forward(3.5)
        self.play(
            FadeOut(Group(hl1, hl2, arrow)),
        )
        self.forward()
        self.play(
            FadeIn(hl3),
            opertypes[2].anim.set(color=GREY),
            opertypes[3].anim.set(color=YELLOW)
        )
        self.forward(0.5)
        self.play(
            FadeOut(hl3),
            FadeOut(typ1[13:])
        )
        self.play(
            Transform(mat2, typ2)
        )
        self.forward(0.5)

        ####################################################

        r1 = SweepRect(typ2[8:10])
        r2 = SweepRect(typ2[10:12])

        g1 = Group(typ2, r1, r2)

        typ3 = TypstMath(
            R'''
            mat(1,2;3,4) vec(5,7) = vec(19,43)
            wide
            mat(1,2;3,4) vec(6,8) = vec(22,50)
            ''',
            scale=1.2
        )

        typ3[1, 3, 18, 20].set(color=RED)
        typ3[2, 4, 19, 21].set(color=GREEN)
        Group(typ3[7:9], typ3[12:16]).set(color=BLUE)
        Group(typ3[24:26], typ3[29:33]).set(color=PURPLE)

        typ4 = TypstMath(
            R'''
            = mat(19,22;43,50)
            ''',
            scale=1.5
        )
        typ4.patterns('19', '43').set(color=BLUE)
        typ4.patterns('22', '50').set(color=PURPLE)

        ####################################################

        self.play(
            SweepRect.ins(r1, r2, lag_ratio=0.4)
        )
        self.forward(2)
        self.play(
            g1.anim.points.shift(UP * 2)
        )
        typ4.points.next_to(typ2, buff=0.3)
        self.play(
            Transform(typ2[:6], typ3[:6], hide_src=False),
            TransformMatchingDiff(Group(typ2[7:10], typ2[12]).copy(), typ3[6:10], duration=1),
        )
        self.play(
            Write(typ3[10:17])
        )
        self.forward(1)
        self.play(
            Transform(typ2[:6], typ3[17:23], hide_src=False),
            TransformMatchingDiff(Group(typ2[7], typ2[10:]).copy(), typ3[23:27], duration=1)
        )
        self.play(
            Write(typ3[27:])
        )
        self.forward(2)
        self.play(
            Transform(typ3[12:16], typ4[2:6], hide_src=False, path_arc=40 * DEGREES),
            Transform(typ3[29:33], typ4[6:10], hide_src=False, path_arc=40 * DEGREES),
            lag_ratio=0.8,
            duration=2
        )
        self.play(
            FadeIn(Group(typ4[:2], typ4[10]))
        )

        ####################################################

        g24 = Group(typ2, typ4)
        hl = HighlightRect(g24, glow_alpha=0.5)

        matmul1 = TypstMath(
            R'''
            mat(1,2;3,4) dot mat(5,6;7,8)
            =
            mat(19,22;43,50)
            ''',
            scale=1.5
        )
        matmul2 = TypstMath(
            R'''
            mat(5,6;7,8) dot mat(1,2;3,4)
            =
            mat(23,34;31,46)
            ''',
            scale=1.5
        )

        for m in (matmul1, matmul2):
            m['mat(1,2;3,4)'].set(color=YELLOW_A)
            m['mat(5,6;7,8)'].set(color=MAROON_A)

        matmul1.points.shift(UP)
        matmul2.points.shift(DOWN * 1.5)

        ####################################################

        self.play(
            FadeIn(hl)
        )
        self.forward(2)
        self.play(
            FadeOut(hl),
            FadeOut(typ3),
            FadeOut(Group(r1, r2))
        )
        self.play(
            TransformMatchingDiff(g24, matmul1)
        )
        self.forward(1.5)
        self.play(
            Write(matmul2)
        )
        self.forward(2.5)
        self.play(
            FadeOut(Group(matmul1, matmul2))
        )


class TL8(SharpDelimTemplate):
    def construct(self):
        seq_play_audio_with_subtitles(
            self,
            [
                { 'file': 'audio_12_3.wav', 'begin': 187, 'end': 192.4, 'delay': 0.2, 'mul': 1.25 },
                { 'file': 'audio_12_3.wav', 'begin': 192.4, 'end': 197, 'delay': 0.8, 'mul': 1.25 },
            ]
        )

        ####################################################

        opertypes = OpersTypes().show()
        opertypes[:3].set(color=GREY)
        opertypes[3].set(color=YELLOW)

        # plane_orig = NumberPlane((-12, 12), (-12, 12), faded_line_ratio=0)
        plane = NumberPlane((-12, 12), (-12, 12), faded_line_ratio=0).copy()
        v1 = Vector([1, 0], color=RED_A)
        v2 = Vector([0, 1], color=GREEN_A)
        img = ImageItem('meme.png', depth=1, width=2, height=1.5)

        g = Group(plane, v1, v2, img).save_state()

        mat1 = Group(
            TypstMath('mat(0,-1;1,0)', scale=1.5, depth=-10),
            Text('旋转'),
            color=YELLOW_A
        )
        mat2 = Group(
            TypstMath('mat(3,0;0,1)', scale=1.5, depth=-10),
            Text('拉伸'),
            color=MAROON_A
        )
        for m in (mat1, mat2):
            m.points.arrange(DOWN, buff=SMALL_BUFF)
            apply_bgshadow(m(VItem))
        Group(mat1, mat2).points.arrange().to_border(UP)

        def apply_matrix(g: Group[Vector, Any], matrix):
            g.generate_target()
            g.target.points.apply_matrix(matrix)
            for v in g.target[1, 2]:
                new_v = Vector(v.points.get_end(), color=v.stroke.get()[0, :3])
                new_v.points.shift(v.points.get_start())
                v.become(new_v)
            return MoveToTarget(g)

        ####################################################

        self.forward()
        self.play(
            FadeIn(g)
        )
        self.forward()
        self.play(
            apply_matrix(g, [[3,0],[0,1]]),
            FadeIn(mat2, DOWN * 0.5)
        )
        self.play(
            apply_matrix(g, [[0,-1],[1,0]]),
            FadeIn(mat1, DOWN * 0.5)
        )

        self.forward(0.3)

        self.play(
            FadeOut(Group(g, mat1, mat2)),
            duration=0.6
        )
        g.load_state()
        self.hide(mat1, mat2)
        Group(mat2, mat1).points.arrange().to_border(UP)
        self.play(
            FadeIn(g),
            duration=0.6
        )

        self.forward(0.4)

        self.play(
            apply_matrix(g, [[0,-1],[1,0]]),
            FadeIn(mat1, DOWN * 0.5)
        )
        self.play(
            apply_matrix(g, [[3,0],[0,1]]),
            FadeIn(mat2, DOWN * 0.5)
        )
        self.forward(1.4)
        self.play(
            FadeOut(Group(mat1, mat2, g, opertypes))
        )


class TL9(SharpDelimTemplate):
    def construct(self):
        seq_play_audio_with_subtitles(
            self,
            [
                { 'file': 'audio_12_3.wav', 'begin': 198, 'end': 225, 'delay': 0, 'mul': 1.25 },
                { 'file': 'audio_12_4.wav', 'begin': 0, 'end': 10, 'delay': 0.2, 'mul': 1.25 },
            ]
        )

        ####################################################

        txt = Text("“变换”", font_size=60)
        txt.points.shift(UP * 1)

        mat1 = Group(
            TypstMath('mat(0,-1;1,0)', scale=1.5, depth=-10),
            Text('旋转'),
            color=YELLOW_A
        )
        mat2 = Group(
            TypstMath('mat(3,0;0,1)', scale=1.5, depth=-10),
            Text('拉伸'),
            color=MAROON_A
        )
        other = Text('......')

        g = Group(mat1, mat2, other)
        g.points.arrange(buff=LARGE_BUFF * 2).shift(DOWN)

        for m in (mat1, mat2):
            m.points.arrange(DOWN, buff=SMALL_BUFF, center=False)

        ####################################################

        self.forward(6)
        self.play(
            Write(txt, duration=2)
        )
        self.play(
            FadeIn(g),
            duration=3
        )
        self.forward()

        self.play(
            FadeOut(Group(txt, g)),
            duration=3
        )
        self.forward(5)

        ####################################################

        computer = SVGItem('computer.svg', alpha=0.5)

        ####################################################

        self.play(Write(computer), duration=3)
        self.forward(4)

        self.play(
            FadeOut(computer),
            FadeIn(g),
            duration=2
        )
        self.forward(3)
        self.play(
            FadeOut(g),
            duration=2
        )

        self.forward(3.5)


class MatTypes(Group):
    def __init__(self):
        _Text = partial(Text, font_size=18)
        super().__init__(
            _Text('单位矩阵'),
            _Text('缩放矩阵'),
            _Text('位移矩阵'),
            _Text('旋转矩阵'),
            color=GREY,
            depth=-50
        )
        self.fix_in_frame()
        self.points.arrange(buff=LARGE_BUFF * 1.6).to_border(UP)
        apply_bgshadow(self(VItem), radius=0.02, alpha=1)


class Pause(Succession):
    def __init__(self, duration: float):
        rect0 = Rect(Config.get.frame_width, 0.2, color=RED_E, fill_alpha=1, stroke_alpha=0)
        rect0.points.to_border(UP, buff=0)
        rect = rect0.copy()
        rect.points.stretch(0, dim=0, about_edge=LEFT)

        super().__init__(
            AnimGroup(
                rect.anim(rate_func=linear, duration=duration).become(rect0),
                FadeIn(rect, duration=0.5),
            ),
            FadeOut(rect, duration=0.5)
        )


class TL10(SharpDelimTemplate):
    def construct(self):
        seq_play_audio_with_subtitles(
            self,
            [
                { 'file': 'audio_12_4.wav', 'begin': 11, 'end': 27.7, 'delay': 1, 'mul': 1.25 },
                { 'file': 'audio_12_4.wav', 'begin': 32.2, 'end': 46.4, 'delay': 0, 'mul': 1.25 },
            ]
        )

        ####################################################

        mattypes = MatTypes().show()

        mat1 = TypstMath('mat(1, 0; 0, 1)', scale=2)
        mat1[1, 3].set(color=RED)
        mat1[2, 4].set(color=GREEN)
        apply_bgshadow(mat1(VItem), 0.02)

        line = Line(
            mat1['1', 0].points.box.center, mat1['1', 1].points.box.center,
            buff=-0.5,
            depth=1,
            stroke_radius=0.3,
            stroke_color=YELLOW,
            stroke_alpha=0.5
        )

        g = Group(mat1, line)

        ####################################################

        self.forward(2)
        self.play(mattypes[0].anim.set(fill_color=YELLOW))
        self.play(FocusOn(mattypes[0]))
        self.play(Write(mat1, stroke_color=WHITE))
        self.play(
            Create(line, duration=0.5),
            FadeIn(line, duration=0.25),
            duration=1
        )
        self.forward(0.5)
        self.play(
            g.anim.points.shift(LEFT * 4),
            FadeOut(line),
        )

        ####################################################

        plane = NumberPlane(faded_line_ratio=0)
        vec1 = Vector([1,0], color=RED_A)
        vec2 = Vector([0,1], color=GREEN_A)

        r1 = SweepRect(mat1[1:3])
        r2 = SweepRect(mat1[3:5])

        ####################################################

        self.play(
            FadeIn(plane)
        )
        self.play(
            SweepRect.ins(r1, r2)
        )
        self.forward(0.6)
        self.play(
            FadeTransform(r1, vec1, path_arc=PI / 2),
            FadeTransform(r2, vec2, path_arc=PI / 2),
            lag_ratio=1
        )
        self.forward(3)
        self.play(
            ApplyWave(vec1),
            # Wait(1.2),
            ApplyWave(vec2),
            lag_ratio=1
        )
        self.forward(0.7)

        ####################################################

        mat2 = TypstMath(
            R'''
            mat(1,0,0,0;0,1,0,0;0,0,1,0;0,0,0,1)
            vec(1,2,3,4)
            =
            vec(1 dot 1, 1 dot 2, 1 dot 3, 1 dot 4)
            =
            vec(1,2,3,4)
            ''',
            scale=1.3
        )
        mat2[5, 9, 13, 17, 52].set(color=RED)
        mat2[6, 10, 14, 18, 55].set(color=GREEN)
        mat2[7, 11, 15, 19, 58].set(color=BLUE)
        mat2[8, 12, 16, 20, 61].set(color=MAROON)

        txt = TypstText(
            R'''
            #set page(width: 34em)
            你可能会奇怪一个没变换的变换矩阵有什么用？单位矩阵通常是生成其他变换矩阵的起点，如果我们深挖线性代数，这还是一个对证明定理、解线性方程非常有用的矩阵。
            '''
        )

        ####################################################

        self.play(
            FadeOut(Group(plane, mat1, vec1, vec2)),
            FadeIn(mat2[:26])
        )
        self.forward(1.4)
        self.play(
            Write(mat2[26:])
        )
        self.play(
            ShowCreationThenDestructionAround(mat2[26:44]),
            ShowCreationThenDestructionAround(mat2[72:]),
        )
        self.forward(4.6)

        self.play(mat2(VItem).anim.color.fade(0.75), Write(txt))
        self.play(Pause(4))
        self.play(
            FadeOut(Group(txt, mat2))
        )

        self.forward()


class TL11(SharpDelimTemplate):
    def construct(self):
        seq_play_audio_with_subtitles(
            self,
            [
                { 'file': 'audio_12_4.wav', 'begin': 49.3, 'end': 64, 'delay': 2.5, 'mul': 1.25 },
                { 'file': 'audio_12_4.wav', 'begin': 64, 'end': 76.4, 'delay': 2.5, 'mul': 1.25 },
            ]
        )

        ####################################################

        mattypes = MatTypes().show()
        mattypes[0].set(fill_color=YELLOW)

        plane_orig = NumberPlane(faded_line_ratio=0, depth=10)
        plane_orig(VItem).color.fade(0.65).set(GREY)
        plane = NumberPlane(y_range=[-8, 8], faded_line_ratio=0, depth=10, background_line_style={'alpha': 0.7})

        def get_mat(a: int, b: int):
            mat = TypstMatrix(
                [
                    [f'{a:.1f}'.removesuffix('.0'), 0],
                    [0, f'{b:.1f}'.removesuffix('.0')]
                ],
                scale=1.8,
                label=True
            )
            e1 = mat.get_element(0, 0).set(color=RED)
            e2 = mat.get_element(0, 1).set(color=RED)
            e3 = mat.get_element(1, 0).set(color=GREEN)
            e4 = mat.get_element(1, 1).set(color=GREEN)
            mat.points.shift(LEFT * 3.5)
            apply_bgshadow(mat(VItem))
            rs = Group(
                SweepRect(Group(e1, e3)),
                SweepRect(Group(e2, e4))
            )
            return Group(mat, rs)

        mat1, rs1 = g1 = get_mat(1, 1)

        vec1 = Vector([1,0], color=RED_A)
        vec2 = Vector([0,1], color=GREEN_A)

        vec1.generate_target().points.update_by_attrs(end=[2, 0, 0]).r.place_tip()
        vec2.generate_target().points.update_by_attrs(end=[0, 0.7, 0]).r.place_tip()

        g = Group(plane, vec1, vec2)
        g.save_state()

        ####################################################

        self.play(
            mattypes[0].anim.set(fill_color=GREY),
            mattypes[1].anim.set(fill_color=YELLOW),
            FocusOn(mattypes[1], duration=1.5)
        )
        self.play(
            Write(mat1, stroke_color=WHITE),
            FadeIn(plane)
        )
        self.play(
            AnimGroup(
                GrowArrow(vec1),
                GrowArrow(vec2),
            ),
            SweepRect.ins(*rs1),
            lag_ratio=0.3
        )
        self.forward(2)
        plane_orig.show()
        self.play(
            ItemUpdater(g1, lambda p: get_mat(1 + 1 * p.alpha, 1)),
            plane.anim.points.stretch(2, dim=0),
            MoveToTarget(vec1)
        )
        self.play(
            ItemUpdater(g1, lambda p: get_mat(2, 1 - 0.3 * p.alpha)),
            plane.anim.points.stretch(0.7, dim=1),
            MoveToTarget(vec2)
        )
        self.play(
            Flash(mat1, flash_radius=1.5, line_length=0.5)
        )
        self.forward(5.5)

        g1.hide()
        mat1, rs1 = g1 = get_mat(2, 0.7)
        g1.show()
        _CircleIndicate = partial(CircleIndicate, rate_func=there_and_back_with_pause)
        self.play(
            _CircleIndicate(mat1.get_element(0, 0), buff=0.5),
            _CircleIndicate(vec1.tip),
            duration=2
        )
        self.play(
            _CircleIndicate(mat1.get_element(1, 1)),
            _CircleIndicate(vec2.tip),
            duration=2
        )

        g_ = g.copy()
        g.save_state('transformed')
        g.hide().load_state()
        g1_ = g1.copy()
        g1.hide()
        g1.become(get_mat(1, 1))
        self.play(
            FadeOut(g_, duration=0.5),
            FadeIn(g),
            FadeOut(g1_, duration=0.5),
            FadeIn(g1),
            duration=1.6
        )

        self.forward()

        ####################################################

        vec3 = Vector([2,3], color=WHITE, glow_alpha=0.5, glow_color=WHITE).show()
        vec3_orig = vec3.copy().set(glow_alpha=0, alpha=0.3, depth=20)
        vec4 = Vector([4, 2.1], color=WHITE, glow_alpha=0.5, glow_color=WHITE)

        typ3 = TypstMath('vec(2,3)')
        typ3['2'].set(color=RED)
        typ3['3'].set(color=GREEN)
        typ3.points.next_to(vec3.points.get_end(), DR, buff=0)
        typ4 = TypstMath('vec(4,2.1)')
        typ4['4'].set(color=RED)
        typ4['2.1'].set(color=GREEN)
        typ4.points.next_to(vec4.points.get_end(), DR, buff=0)

        ####################################################

        self.play(
            GrowArrow(vec3),
            FadeIn(typ3),
            duration=2
        )
        self.forward(2)
        vec3_orig.show()
        self.play(
            ItemUpdater(g1, lambda p: get_mat(1 + 1 * p.alpha, 1 - 0.3 * p.alpha)),
            g.anim.load_state('transformed'),
            Transform(vec3, vec4),
            FadeTransform(typ3, typ4, hide_src=False),
            typ3(VItem).anim(duration=0.3).color.fade(0.7),
            duration=2.5
        )
        self.forward(4)

        self.play(
            FadeOut(Group(g, plane_orig, vec3_orig, vec4, typ3, typ4, g1))
        )


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
        self.points.scale(0.8)
        self.apply_distance_sort()


class TL12(SharpDelimTemplate):
    def construct(self):
        seq_play_audio_with_subtitles(
            self,
            [
                { 'file': 'audio_12_4.wav', 'begin': 76.4, 'end': 89, 'delay': 0, 'mul': 1.25 },
                { 'file': 'audio_12_4.wav', 'begin': 90.2, 'end': 101, 'delay': 1.5, 'mul': 1.25 },
                { 'file': 'audio_12_4.wav', 'begin': 101, 'end': 112, 'delay': 0.5, 'mul': 1.25 },
            ]
        )

        ####################################################

        mattypes = MatTypes().show()
        mattypes[1].set(fill_color=YELLOW)

        def get_mat(a: int, b: int):
            mat = TypstMatrix(
                [
                    [f'{a:.1f}'.removesuffix('.0'), 0],
                    [0, f'{b:.1f}'.removesuffix('.0')]
                ],
                gap='0.75em',
                scale=1.8,
                label=True
            )
            mat.get_element(0, 0).set(color=RED)
            mat.get_element(0, 1).set(color=RED)
            mat.get_element(1, 0).set(color=GREEN)
            mat.get_element(1, 1).set(color=GREEN)
            return mat

        mat1 = get_mat(2, 0.7)
        mat2 = get_mat(3, 3)

        mat1.points.shift(LEFT * 2)
        mat2.points.shift(RIGHT * 2)

        txt1 = Text('不均匀缩放')
        txt1.points.next_to(mat1, DOWN)

        txt2 = Text('均匀缩放')
        txt2.points.next_to(mat2, DOWN)

        ####################################################

        self.play(
            Write(mat1)
        )
        self.play(
            Write(mat2)
        )
        self.play(
            Write(txt1)
        )
        self.play(
            ShowPassingFlashAround(mat1.get_element(0, 0), time_width=0.65),
            ShowPassingFlashAround(mat1.get_element(1, 1), time_width=0.65),
            duration=2.5
        )
        self.forward()
        self.play(
            ShowPassingFlashAround(mat2.get_element(0, 0), time_width=0.65),
            ShowPassingFlashAround(mat2.get_element(1, 1), time_width=0.65),
        )
        self.forward(0.4)
        self.play(
            Write(txt2)
        )
        self.forward(0.3)

        self.play(
            FadeOut(Group(mat1, mat2, txt1, txt2)),
            duration=0.7
        )

        ####################################################

        eq = TypstMath(
            R'''
            mat(S_1,0,0,0;0,S_2,0,0;0,0,S_3,0;0,0,0,1)
            dot
            vec(x,y,z,1)
            =
            vec(S_1 dot x, S_2 dot y, S_3 dot z, 1)
            ''',
            depth=-10,
            # scale=0.9
        ).fix_in_frame()
        Group(eq[5:7], eq[10], eq[15], eq[20], eq[56:58]).set(color=RED)
        Group(eq[7], eq[11:13], eq[16], eq[21], eq[60:62]).set(color=GREEN)
        Group(eq[8], eq[13], eq[17:19], eq[22], eq[64:66]).set(color=BLUE)
        eq[9, 14, 19, 23].set(color=MAROON)
        eq.points.shift(RIGHT)

        eqparts = Group(
            eq[:29],
            eq[29],
            eq[30:48],
            eq[48],
            eq[49:],
        )

        rs = Group(
            SweepRect(eq[5:9]),
            SweepRect(eq[10:14]),
            SweepRect(eq[15:19]),
        ).fix_in_frame()
        rs[-1].points.stretch(0.94, dim=1, about_edge=UP)

        plane = NumberPlane(
            (-7.5, 7.5),
            (-7.5, 7.5),
            faded_line_ratio=0,
            background_line_style={'alpha': 0.7}
        ).apply_depth_test()

        con3d = Container3D().apply_depth_test()

        ####################################################

        self.play(Write(eqparts[0]))
        apply_bgshadow(eq[5:24](VItem))
        self.forward(0.5)
        self.play(
            Aligned(
                eq.anim(show_at_begin=False).points.shift(LEFT * 4.75),
                FadeIn(plane),
                FadeIn(con3d),
                self.camera.anim.points.set(orientation=Quaternion(0.87, 0.4, 0.13, 0.27)),
                rs.anim(show_at_begin=False).points.shift(LEFT * 4.75),
                Succession(
                    Wait(),
                    SweepRect.ins(*rs, lag_ratio=0.3, duration=0.8)
                ),
            ),
            duration=2
        )

        ####################################################

        vec1 = Vector([3, 0], color=RED_A)
        vec2 = Vector([0, 3], color=GREEN_A)
        vec3 = Vector([0, 0, 3], color=BLUE_A)
        vecs = Group(vec1, vec2, vec3).apply_depth_test()
        vecs.points.shift(OUT * 2e-2)

        typ1 = TypstMath('S_1', color=RED)
        typ2 = TypstMath('S_2', color=GREEN)
        typ3 = TypstMath('S_3', color=BLUE)
        typs = Group(typ1, typ2, typ3)
        for v, t in zip(vecs, typs):
            t.points.scale(1.2).next_to(v.points.get_end(), UR, buff=0)
            apply_bgshadow(t(VItem))
            t.points.face_to_camera()

        ####################################################

        self.play(
            *map(GrowArrow, vecs),
            FadeIn(typs),
            duration=2
        )
        self.prepare(
            Destruction(plane),
            at=0.8
        )
        self.forward(2)
        apply_bgshadow(eq[37:41](VItem))
        apply_bgshadow(eq[56:69](VItem))
        self.play(
            FadeIn(eqparts[1, 2]),
        )
        self.forward(3)
        self.play(
            Write(eqparts[3]),
            FadeIn(eqparts[4]),
            lag_ratio=0.4
        )
        self.forward(0.7)

        ####################################################

        # ts1 = TransformableFrameClip(rs, eq).show()
        ts1 = Group(rs, eq)
        ts2 = TransformableFrameClip(con3d, vecs, typs).show()

        ####################################################

        self.play(
            # Destruction(plane, rate_func=rush_into, duration=0.6),
            ts1.anim.points.shift(RIGHT),
            ts2.anim.clip.set(x_offset=0.15, y_offset=-0.1),
            duration=1.6
        )

        ####################################################

        hl = boolean_ops.Difference(
            FrameRect(),
            boolean_ops.Union(
                SurroundingRect(eq[20:24]),
                SurroundingRect(eq[9, 14, 19]),
                SurroundingRect(eq[40]),
                SurroundingRect(eq[68]),
            ),
            **Rect.preset_shadow,
            depth=-20
        ).fix_in_frame()
        hl.set(fill_alpha=0.7)

        fr = FrameRect(fill_alpha=1, stroke_alpha=0, color=BLACK, depth=-30).fix_in_frame()

        ####################################################

        self.forward(0.8)
        self.play(
            ShowCreationThenFadeAround(eq[23]),
            ShowCreationThenFadeAround(eq[40]),
            ShowCreationThenFadeAround(eq[68]),
        )
        self.forward(3)
        self.play(
            rs(VItem).anim.color.fade(0.5),
            FadeIn(hl),
            duration=2
        )
        self.forward(2)
        self.play(
            FadeIn(fr)
        )

        self.forward(0.3)


class TL13(SharpDelimTemplate):
    def construct(self):
        seq_play_audio_with_subtitles(
            self,
            [
                { 'file': 'audio_12_4.wav', 'begin': 112, 'end': 127, 'delay': 0, 'mul': 1.25 },
            ]
        )

        ####################################################

        mattypes = MatTypes().show()
        mattypes[1].set(fill_color=YELLOW)

        plane = NumberPlane(
            faded_line_ratio=0,
            background_line_style={'alpha': 0.7}
        )

        typplus = TypstMath('"" + vec(2,1)')
        typplus['2'].set(color=RED)
        typplus['1'].set(color=GREEN)
        typplus.points.shift([2.13, 1.06, 0.0])

        dot1 = Dot([1,1,0])
        dot2 = Dot([3,2,0])

        arrow = Arrow(dot1, dot2, color=BLUE)

        typ1 = TypstMath('vec(x,y) + vec(2,1) = vec(x+2,y+1)')
        typ1[6, 13].set(color=RED)
        typ1[7, 16].set(color=GREEN)

        typ2 = TypstMath(
            R'''
            mat(#box(width: 4em, height: 4em, align(horizon)[?]))
            dot
            vec(#box(width: 1em, height: 4em, align(horizon)[?]))
            =
            vec(#box(width: 1em, height: 4em, align(horizon)[?]))
            '''
        )

        txt1 = Text('直接使用向量加法')
        txt1.points.next_to(LEFT * 2.5, LEFT)
        txt2 = Text('使用矩阵')
        txt2.points.next_to(LEFT * 2.5, LEFT)

        g1 = Group(typ1, txt1)
        g2 = Group(typ2, txt2)
        g2.points.shift(DOWN)

        ####################################################

        self.play(
            mattypes[1].anim.set(fill_color=GREY),
            mattypes[2].anim.set(fill_color=YELLOW),
            FocusOn(mattypes[2], duration=1.6)
        )

        self.play(
            FadeIn(plane)
        )

        self.play(
            FadeIn(dot1, scale=0.2)
        )
        self.play(
            GrowArrow(arrow),
            Write(typplus),
            duration=1.3
        )

        self.play(
            Transform(dot1, dot2, hide_src=False),
            dot1.anim(duration=0.3).color.fade(0.7),
            duration=2
        )
        self.forward()

        self.play(
            FadeOut(Group(plane, dot1, dot2, arrow, typplus)),
            Write(typ1)
        )
        self.play(Write(txt1))
        self.forward(2)
        self.play(
            g1.anim.points.shift(UP),
            FadeIn(g2),
            duration=2
        )

        self.play(
            FadeOut(Group(g1, g2))
        )


class TL14(SharpDelimTemplate):
    def construct(self):
        seq_play_audio_with_subtitles(
            self,
            [
                { 'file': 'audio_12_4.wav', 'begin': 128, 'end': 165, 'delay': 0.3, 'mul': 1.25 },
                { 'file': 'audio_12_4.wav', 'begin': 165, 'end': 194, 'delay': 3.4, 'mul': 1.25 },
            ]
        )

        ####################################################

        mattypes = MatTypes().show()
        mattypes[2].set(fill_color=YELLOW)

        mat1 = TypstText(
            R'''
            #let dc = circle(radius: 0.65em, fill: white.transparentize(50%))
            $
                mat(
                    gap: #1em,
                    ..#range(4).map(
                        row => range(4).map(
                            col => [#box[#dc] #label("box" + str(row) + "-" + str(col))]
                        )
                    )
                )
            $
            '''
        )

        def getels(lst: list[tuple[int, int, str, JAnimColor]]):
            a = Group()
            b = Group()
            for row, col, typ_str, c in lst:
                label = mat1.get_label(f'box{row}-{col}')
                a.add(label)

                typ = TypstMath(typ_str, color=c, scale=1.4)
                typ.points.move_to(label).shift(DOWN * 0.06 + RIGHT * 0.03)
                b.add(typ)

            return a, b

        els1, typs1 = getels([
            [0, 0, 'S_1', RED],
            [1, 1, 'S_2', GREEN],
            [2, 2, 'S_3', BLUE]
        ])

        els2, typs2 = getels([
            [0, 3, 'T_x', RED],
            [1, 3, 'T_y', GREEN],
            [2, 3, 'T_z', BLUE]
        ])

        txt1 = TypstText('缩放 $->$', scale=1.3)
        txt1.points.shift([-3, 1.45, 0.0])

        txt2 = TypstText('$<-$ 位移', scale=1.3)
        txt2.points.shift([3, 1.45, 0.0])

        r1 = SweepRect(typs2)

        ####################################################

        self.play(
            FadeIn(mat1)
        )
        self.forward(2.5)
        self.play(
            FadeOut(els1),
            FadeIn(typs1),
            FadeIn(txt1)
        )
        self.forward(3)
        self.play(
            FadeIn(els1),
            FadeOut(typs1),
            FadeOut(txt1)
        )
        self.forward(5)
        self.play(
            FadeOut(els2),
            FadeIn(typs2),
            FadeIn(txt2)
        )
        self.forward(0.5)
        self.play(
            r1.anim_in()
        )
        self.forward(4.6)

        ####################################################

        mat2 = TypstMath(
            R'''
            mat(1, 0, 0, T_x; 0, 1, 0, T_y; 0, 0, 1, T_z; 0, 0, 0, 1)
            dot
            vec(x,y,z,1)
            ''',
            scale=1.3
        )
        Group(mat2[5], mat2[9], mat2[13], mat2[17:19]).set(color=RED)
        Group(mat2[6], mat2[10], mat2[14], mat2[19:21]).set(color=GREEN)
        Group(mat2[7], mat2[11], mat2[15], mat2[21:23]).set(color=BLUE)
        mat2[8, 12, 16, 23].set(color=MAROON)
        mat2parts = Group(
            mat2[:29],
            mat2[29],
            mat2[30:],
        )

        line = Line(
            mat2[5].points.box.center,
            mat2[23].points.box.center,
            buff=-0.2,
            stroke_radius=0.2,
            stroke_alpha=0.3,
            stroke_color=YELLOW,
            depth=10
        )
        r2 = SweepRect(mat2[17:23])

        ####################################################

        fadeouts = Group(*mat1, typs2, txt2, r1)
        fadeouts.remove(*els2.descendants())

        self.play(
            FadeOut(fadeouts),
            Write(mat2parts[0]),
            duration=3.5
        )
        self.forward(2)
        self.play(
            Create(line),
            FadeIn(line, duration=0.3)
        )
        self.forward(1.5)
        self.play(
            FadeOut(line, duration=0.6),
            r2.anim_in()
        )
        self.forward()
        self.play(
            FadeOut(r2),
            Write(mat2parts[1:])
        )
        self.forward(0.5)

        ####################################################

        mat3 = TypstText(
            R'''
            #let sd = $#h(-0.1em) dot #h(0.1em)$
            $
                vec(1,0,0,0) sd x
                +
                vec(0,1,0,0) sd y
                +
                vec(0,0,1,0) sd z
                +
                vec(T_x, T_y, T_z, 1) sd 1
            $
            '''
        )
        Group(mat3[7], mat3[28], mat3[49], mat3[70:72]).set(color=RED)
        Group(mat3[8], mat3[29], mat3[50], mat3[72:74]).set(color=GREEN)
        Group(mat3[9], mat3[30], mat3[51], mat3[74:76]).set(color=BLUE)
        mat3[10, 31, 52, 76].set(color=MAROON)

        mat4 = TypstMath(
            R'''
            vec(x,0,0,0)
            +
            vec(0,y,0,0)
            +
            vec(0,0,z,0)
            +
            vec(T_x, T_y, T_z, 1)
            '''
        )
        Group(mat4[26], mat4[45], mat4[64:66]).set(color=RED)
        Group(mat4[8], mat4[46], mat4[66:68]).set(color=GREEN)
        Group(mat4[9], mat4[28], mat4[68:70]).set(color=BLUE)
        mat4[10, 29, 48].set(color=MAROON)

        mat5 = TypstMath(
            R'''
            vec(x + T_x, y + T_y, z + T_z, 1)
            '''
        )
        mat5['T_x'].set(color=RED)
        mat5['T_y'].set(color=GREEN)
        mat5['T_z'].set(color=BLUE)

        ####################################################

        ignores = Group(*mat2[:5], *mat2[24:29], *mat2[30:37], *mat2[41:])
        src = mat2[:]
        src.remove(*ignores)

        self.play(
            FadeOut(ignores, duration=0.5),
            TransformMatchingShapes(src, mat3)
        )
        self.play(
            TransformMatchingDiff(mat3, mat4)
        )

        ignores = Group(*mat4[11:18], *mat4[19:26], *mat4[30:37], *mat4[38:45], *mat4[49:56], *mat4[57:64])
        src = mat4[:]
        src.remove(*ignores)

        self.play(
            FadeOut(ignores, duration=0.5),
            TransformMatchingShapes(src, mat5)
        )

        mat2.points.scale(1/1.3).shift(LEFT * 1)
        mat5.generate_target().points.shift(RIGHT * 2)
        eq = TypstMath('=')
        eq.points.move_to((mat2.points.box.right + mat5.target.points.box.left) * 0.5)
        self.play(
            AnimGroup(
                FadeIn(mat2),
                MoveToTarget(mat5),
            ),
            Write(eq),
            lag_ratio=0.6
        )

        ####################################################

        hl = HighlightRect(Group(mat5[8:11], mat5[12:15], mat5[16:19]), glow_alpha=0.5)

        r1 = SurroundingRect(mat2[5:24], glow_alpha=0.4)
        r2 = SurroundingRect(Group(mat2[5:8], mat2[9:12], mat2[13:16]), glow_alpha=0.4)
        r3 = SurroundingRect(mat2[17:23], stroke_alpha=0, fill_alpha=0.5, depth=10, color=RED)

        ####################################################

        self.play(
            FadeIn(hl)
        )
        self.forward(2)
        self.play(
            FadeOut(hl)
        )
        self.forward(1.5)
        self.play(
            FadeIn(r1)
        )
        self.forward(2.5)
        self.play(
            Transform(r1, r2)
        )
        self.forward()
        self.play(
            FadeIn(r3)
        )
        self.forward()
        self.play(
            FadeOut(r3),
            Transform(r2, r1),
            duration=2
        )
        self.forward(5)
        self.play(
            FadeOut(r1)
        )
        self.forward(3)
        self.play(
            FadeOut(Group(mat2, mat5, eq))
        )

        self.forward(4)


def Tick(**kwargs):
    return VItem(
        [-0.77, 1.58, 0], [-0.77, 1.58, 0], [-0.76, 1.58, 0], [-0.75, 1.57, 0], [-0.75, 1.57, 0],
        [-0.75, 1.57, 0], [-0.73, 1.54, 0], [-0.71, 1.53, 0], [-0.71, 1.53, 0], [-0.7, 1.53, 0],
        [-0.63, 1.6, 0], [-0.58, 1.65, 0], [-0.43, 1.77, 0],
        **kwargs
    )


class TL15(SharpDelimTemplate):
    def construct(self):
        seq_play_audio_with_subtitles(
            self,
            [
                { 'file': 'audio_12_5.wav', 'begin': 0, 'end': 46.6, 'delay': 1, 'mul': 1.25 },
            ]
        )

        ####################################################

        mattypes = MatTypes().show()
        mattypes[2].set(fill_color=YELLOW)

        tick1 = Tick(color=GREEN_B, depth=-100)
        tick2 = Tick(color=GREEN_B, depth=-100)
        tick3 = Tick(color=GREEN_B, depth=-100)

        tick1.points.shift([-3.1, 1.64, 0.0])
        tick2.points.shift([-0.49, 1.64, 0.0])
        tick3.points.shift([2.12, 1.64, 0.0])

        txt = Text('简单介绍', font_size=48, color=GREY_A)

        ####################################################

        self.play(
            mattypes[2].anim.set(fill_color=GREY),
            mattypes[3].anim.set(fill_color=YELLOW),
            # FocusOn(mattypes[3], duration=1.5)
        )
        self.forward(1)

        self.play(
            Create(tick1, rate_func=rush_from),
            Create(tick2, rate_func=rush_from),
            Create(tick3, rate_func=rush_from),
            lag_ratio=1.5
        )
        self.forward()
        self.play(
            FocusOn(mattypes[-1]),
            ShowCreationThenFadeAround(mattypes[-1])
        )
        self.play(
            FadeOut(Group(tick1, tick2, tick3))
        )
        self.forward(5)
        self.play(
            Write(txt, duration=2)
        )
        self.forward()
        self.play(
            FadeOut(txt, duration=2)
        )

        ####################################################

        con3d = Container3D().apply_depth_test().apply_distance_sort(False)

        def con3d_updater(data, p=None):
            deg = degtr.current().get_value()
            data.points.rotate(deg, about_point=ORIGIN)

        degtr = ValueTracker(0)

        def lines_updater(p=None, at3d=False):
            deg = degtr.current().get_value()
            line1 = Line(ORIGIN, RIGHT * 1.5, color=BLUE, stroke_radius=0.015)
            line2 = line1.copy()
            line2.points.rotate(deg, about_point=ORIGIN)

            g = Group(
                line1, line2
            )

            try:
                angle = Angle(line1, line2, color=BLUE)
                g.add(angle)
                txt = Text('旋转角度', font_size=12)
                txt.points.scale(min(1, deg / (20 * DEGREES)))
                p = angle.points.pfp(0.5)
                txt.points.next_to(p, buff=0.1)
                if at3d:
                    txt.points.face_to_camera(about_point=p, inverse=True, rotate=PI)
                g.add(txt)
            except PointError:
                pass

            g.points.shift(OUT * 0.802)
            return g

        lines = lines_updater()

        line_axis = DashedLine(ORIGIN, OUT * 5, color=BLUE).apply_depth_test()
        arrow_axis = Arrow(DOWN * 0.3 + OUT * 1.8, UP * 0.3 + OUT * 1.8, path_arc=PI, buff=0).apply_distance_sort()
        arrow_axis.points.rotate(-20 * DEGREES, about_point=ORIGIN)

        txt_axis = Text('旋\n转\n轴', font_size=12).fix_in_frame()
        txt_axis.points.shift([0.3, 2, 0])

        def Updaters(at3d=False):
            return AnimGroup(
                ItemUpdater(lines, partial(lines_updater, at3d=at3d)),
                DataUpdater(con3d if at3d else con3d[0], con3d_updater, root_only=False)
            )

        ####################################################

        self.play(
            FadeIn(con3d[0])
        )

        self.play(
            Create(lines[0])
        )
        self.forward(2)
        self.play(
            Aligned(
                Succession(
                    degtr.anim.set_value(50 * DEGREES),
                    degtr.anim(rate_func=ease_inout_quint).set_value(20 * DEGREES),
                    degtr.anim(duration=0.5).set_value(0 * DEGREES),
                ),
                Updaters()
            ),
            duration=6
        )
        self.forward()
        con3d.show()
        self.play(
            self.camera.anim.points.set(orientation=Quaternion(0.88, 0.35, 0.12, 0.3)),
            Create(line_axis, lag_ratio=0.9),
        )
        self.forward(3)
        self.play(
            GrowArrow(arrow_axis),
            FadeIn(txt_axis),
            degtr.anim.set_value(35 * DEGREES),
            Updaters(True),
            duration=2
        )
        self.play(
            Indicate(lines[-1])
        )
        self.play(
            Indicate(txt_axis)
        )
        self.forward(0.5)
        con3d.points.rotate(-35 * DEGREES)
        self.play(
            degtr.anim.set_value(140 * DEGREES),
            Updaters(True),
            duration=8
        )
        self.play(
            FadeOut(Group(con3d, lines, line_axis, arrow_axis, txt_axis))
        )
        self.forward(0.5)


class TL16(SharpDelimTemplate):
    def construct(self):
        seq_play_audio_with_subtitles(
            self,
            [
                { 'file': 'audio_12_5.wav', 'begin': 46.6, 'end': 61, 'delay': 0, 'mul': 1.25 },
            ]
        )

        ####################################################

        mattypes = MatTypes().show()
        mattypes[3].set(fill_color=YELLOW)

        plane = NumberPlane(faded_line_ratio=0)
        plane(VItem).color.fade(0.5)

        vec_orig = Vector([2,1], color=BLUE_A)
        vec = vec_orig.copy().set(depth=-1)
        vec_orig.color.fade(0.5)

        def angle_updater(p: UpdaterParams | None = None):
            try:
                angle = Angle(vec_orig, vec.current(), color=BLUE)
                typ = TypstMath('theta', color=BLUE)
                typ.points.next_to(angle.points.pfp(0.5), UR, buff=0.05)
                return Group(angle, typ)
            except PointError:
                return Group()

        angle = angle_updater()

        typ = TypstMath('cos theta wide sin theta', scale=2.5)
        typ['theta', ...].set(color=BLUE)
        typ.points.shift([0.0, -1.26, 0.0])

        ####################################################

        self.forward(0.7)
        self.play(
            FadeIn(plane),
            GrowArrow(vec),
            duration=2
        )
        self.forward(2)
        vec_orig.show()
        self.play(
            vec.update.points.rotate(50 * DEGREES, about_point=ORIGIN),
            ItemUpdater(angle, angle_updater),
            duration=2
        )
        self.forward(3.5)
        self.play(
            Write(typ),
            duration=1.5
        )

        self.forward(2)

        self.play(
            FadeOut(Group(plane, vec_orig, vec, angle, typ))
        )


class TL17(SharpDelimTemplate):
    def construct(self):
        seq_play_audio_with_subtitles(
            self,
            [
                { 'file': 'audio_12_5.wav', 'begin': 61, 'end': 115.3, 'delay': 0, 'mul': 1.25 },
                { 'file': 'audio_12_5.wav', 'begin': 115.3, 'end': 171, 'delay': 1, 'mul': 1.25 },
                { 'file': 'audio_12_5.wav', 'begin': 173.5, 'end': 185, 'delay': 5, 'mul': 1.25 },
            ]
        )

        ####################################################

        mattypes = MatTypes().show()
        mattypes[3].set(fill_color=YELLOW)

        typ1 = TypstText(
            R'''
            #let dot = box(circle(radius: 0.5em, fill: white.transparentize(50%)), baseline: 20%)
            $
                mat(
                    gap: #0.35em,
                    dot, dot, dot, 0;
                    dot, dot, dot, 0;
                    dot, dot, dot, 0;
                    0, 0, 0, 1;
                )
            $
            '''
        )

        hl = HighlightRect(Group(typ1[5:8], typ1[9:12], typ1[13:16]), glow_alpha=0.5)

        typ2 = TypstText(
            R'''
            #let ss(body) = {
                set text(size: 0.8em)
                body
            }
            #box[$
                mat(
                    1, 0, 0, 0;
                    0, cos theta, -sin theta, 0;
                    0, sin theta, cos theta, 0;
                    0, 0, 0, 1;
                )
                vec(x, y, z, 1)
                =
                vec(
                    x,
                    ss(cos theta dot y - sin theta dot z),
                    ss(sin theta dot y + cos theta dot z),
                    1
                )
            $] <eq1>

            #box[$
                mat(
                    cos theta, 0, sin theta, 0;
                    0, 1, 0, 0;
                    -sin theta, 0, cos theta, 0;
                    0, 0, 0, 1;
                )
                vec(x, y, z, 1)
                =
                vec(
                    ss(cos theta dot x + sin theta dot z),
                    y,
                    ss(-sin theta dot x + cos theta dot z),
                    1
                )
            $] <eq2>

            #box[$
                mat(
                    cos theta, -sin theta, 0, 0;
                    sin theta, cos theta, 0, 0;
                    0, 0, 1, 0;
                    0, 0, 0, 1;
                )
                vec(x, y, z, 1)
                =
                vec(
                    ss(cos theta dot x - sin theta dot y),
                    ss(sin theta dot x + cos theta dot y),
                    z,
                    1
                )
            $] <eq3>
            ''',
        )
        Group(typ2[5], typ2[9], typ2[19], typ2[30], typ2[105:109], typ2[116], typ2[120:124], typ2[130], typ2[165:169], typ2[172:176], typ2[206:210], typ2[216:221], typ2[227], typ2[231], typ2[266:270], typ2[273:277]).set(color=RED)
        Group(typ2[6], typ2[10:14], typ2[20:25], typ2[31], typ2[66:70], typ2[73:77], typ2[109], typ2[117], typ2[124], typ2[131], typ2[210:214], typ2[221:225], typ2[228], typ2[232], typ2[279:283], typ2[286:290]).set(color=GREEN)
        Group(typ2[7], typ2[14:18], typ2[25:29], typ2[32], typ2[79:83], typ2[86:90], typ2[110:115], typ2[118], typ2[125:129], typ2[132], typ2[179:184], typ2[187:191], typ2[214], typ2[225], typ2[229], typ2[233]).set(color=BLUE)
        typ2[8, 18, 29, 33, 115, 119, 129, 133, 215, 226, 230, 234].set(color=MAROON)

        parts = Group(
            typ2.get_label('eq1'),
            typ2.get_label('eq2'),
            typ2.get_label('eq3'),
        )
        for part in parts:
            part.points.to_center()

        r1 = SurroundingRect(parts[2][:57])
        r2 = SurroundingRect(parts[2][58:])

        ####################################################

        self.forward(2)
        self.play(
            FadeIn(typ1),
            duration=3
        )
        self.forward(12)
        self.play(
            FadeIn(hl),
            duration=2
        )
        self.forward(4)
        self.play(
            FadeOut(hl)
        )
        self.forward(5.5)
        self.play(
            FadeOut(typ1),
            FadeIn(parts[2])
        )
        self.forward(2)
        self.play(
            Create(r1, auto_close_path=False),
        )
        self.forward(2)
        self.play(
            Transform(r1, r2)
        )
        self.forward()
        self.play(
            FadeOut(r2)
        )
        self.forward(0.5)
        self.play(
            Aligned(
                WiggleOutThenIn(parts[2][91], scale=2),
                DataUpdater(
                    parts[2][91],
                    lambda data, p: data.fill.mix(YELLOW, p.alpha),
                    rate_func=there_and_back
                ),
                duration=2.5
            )
        )
        self.forward(2)

        ####################################################

        _Rect = partial(Rect, color=YELLOW, depth=10, fill_alpha=0.2, stroke_alpha=0)
        r1 = _Rect([-3.48, 0.04, 0], [-0.64, 0.89, 0])
        r2 = _Rect([-3.47, -0.9, 0], [-1.4, 0.88, 0])
        r3 = _Rect([0.9, -0.01, 0], [3.43, 0.83, 0])
        rs = Group(r1, r2, r3)

        txt0 = TypstText('绕 $x$ 轴旋转 $theta$', scale=0.7)
        txt1 = TypstText('绕 $y$ 轴旋转 $theta$', scale=0.7)
        txt2 = TypstText('绕 $z$ 轴旋转 $theta$', scale=0.7)

        ####################################################

        self.play(
            FadeIn(rs)
        )
        self.forward()
        self.play(
            Group(rs, parts[2]).anim.points.scale(0.55).to_border(UR).shift(DOWN),
            FadeOut(rs),
        )
        txt2.points.next_to(parts[2], DOWN, buff=SMALL_BUFF)
        self.play(
            FadeIn(txt2)
        )
        self.forward()

        ####################################################

        r1 = _Rect([-3.47, -0.38, 0], [-0.63, 0.43, 0])
        r2 = _Rect([-3.05, -0.92, 0], [-1.05, 0.91, 0])
        r3 = _Rect([0.89, -0.41, 0], [3.44, 0.42, 0])
        rs = Group(r1, r2, r3)

        ####################################################

        self.play(
            FadeIn(parts[0])
        )
        self.forward()
        self.play(
            FadeIn(rs)
        )
        self.forward(2)
        self.play(
            Group(rs, parts[0]).anim.points.scale(0.55).to_border(UL).shift(DOWN),
            FadeOut(rs),
            # duration=0.6
        )
        txt0.points.next_to(parts[0], DOWN, buff=SMALL_BUFF)
        self.play(
            FadeIn(txt0),
            # duration=0.6
        )

        self.play(
            FadeIn(parts[1])
        )
        self.play(
            parts[1].anim.points.scale(0.55).to_border(UP).shift(DOWN),
        )
        txt1.points.next_to(parts[1], DOWN, buff=SMALL_BUFF)
        self.play(
            FadeIn(txt1)
        )
        self.forward(17.5)

        ####################################################

        typ3 = TypstMath(
            R'''
            mat(
                cos theta_2, 0, sin theta_2, 0;
                0, 1, 0, 0;
                -sin theta_2, 0, cos theta_2, 0;
                0, 0, 0, 1;
            )
            mat(
                1, 0, 0, 0;
                0, cos theta_1, -sin theta_1, 0;
                0, sin theta_1, cos theta_1, 0;
                0, 0, 0, 1;
            )
            vec(x,y,z,1)
            '''
        )
        typ3.points.shift(DOWN * 0.5)
        Group(typ3[5:10], typ3[18], typ3[22:27], typ3[34], typ3[48], typ3[52], typ3[64], typ3[77]).set(color=RED)
        Group(typ3[10], typ3[19], typ3[27], typ3[35], typ3[49], typ3[53:58], typ3[65:71], typ3[78]).set(color=GREEN)
        Group(typ3[11:17], typ3[20], typ3[28:33], typ3[36], typ3[50], typ3[58:63], typ3[71:76], typ3[79]).set(color=BLUE)
        typ3[17, 21, 33, 37, 51, 63, 76, 80].set(color=MAROON)

        alphaeff = AlphaEffect(typ2, txt0, txt1, txt2).show()

        ####################################################

        self.play(
            Aligned(
                FadeIn(typ3[86:]),
                TransformMatchingDiff(parts[0][:39].copy(), typ3[43:86], path_arc=80 * DEGREES),
            )
        )
        self.play(
            TransformMatchingDiff(parts[1][:39].copy(), typ3[:43], path_arc=50 * DEGREES),
        )
        self.forward(9.5)
        self.play(
            FadeOut(typ3),
            alphaeff.anim.alpha.set(0.5)
        )
        self.forward(4)

        ####################################################

        tl = TL17_Sub1().build().to_item(keep_last_frame=True).show()
        tlalpha = AlphaEffect(tl).show()
        tlalpha.alpha.set(0)

        ####################################################

        self.play(
            tlalpha.anim.alpha.set(1)
        )
        self.forward(4)
        self.play(
            tlalpha.anim.alpha.set(0)
        )
        tlalpha.hide()
        tl.hide()
        self.forward(3.5)

        ####################################################

        typ4 = TypstMath(
            R'''
            mat(
                gap: #0.75em,
                cos theta + R_x^2 (1 - cos theta),
                R_x R_y (1 - cos theta) - R_z sin theta,
                R_x R_z (1 - cos theta) + R_y sin theta,
                0;

                R_y R_x (1 - cos theta) + R_z sin theta,
                cos theta + R_y^2 (1 - cos theta),
                R_y R_z (1 - cos theta) - R_x sin theta,
                0;

                R_z R_x (1 - cos theta) - R_y sin theta,
                R_z R_y (1 - cos theta) + R_x sin theta,
                cos theta + R_z^2 (1 - cos theta),
                0;

                0, 0, 0, 1;
            )
            ''',
            scale=0.9
        )
        typ4.points.shift(DOWN * 0.2)
        typ4.patterns(('R_x', ...), 'R_x^2').set(color=RED)
        typ4.patterns(('R_y', ...), 'R_y^2').set(color=GREEN)
        typ4.patterns(('R_z', ...), 'R_z^2').set(color=BLUE)
        typ4['""^2', ...].set(color=WHITE)

        txt41 = TypstText('绕任意轴 $(R_x, R_y, R_z)$ 旋转')
        txt41.points.next_to(typ4, DOWN, buff=SMALL_BUFF)
        txt41['$R_x$', ...].set(color=RED)
        txt41['$R_y$', ...].set(color=GREEN)
        txt41['$R_z$', ...].set(color=BLUE)

        txt42 = TypstMath('(R_x^2 + R_y^2 + R_z^2 = 1)', scale=0.7)
        txt42(VItem).color.fade(0.5)
        txt42.points.next_to(txt41, DOWN, buff=SMALL_BUFF)
        txt42['R_x^2'].set(color=RED)
        txt42['R_y^2'].set(color=GREEN)
        txt42['R_z^2'].set(color=BLUE)
        txt42['""^2', ...].set(color=WHITE)

        g4 = Group(typ4, txt41, txt42)

        tip = TypstText(
            R'''
            #set page(width: 34em)
            #set text(size: 0.8em)
            #set par(first-line-indent: (amount: 2em, all: true))
            即使这样一个矩阵也不能完全解决万向节死锁问题（尽管会极大地避免）。
            避免万向节死锁的真正解决方案是使用四元数(Quaternion)，它不仅更安全，而且计算会更有效率。
            '''
        )

        tip.points.shift(DOWN)

        ####################################################

        self.show(g4)
        self.forward(5.5)

        self.play(
            FadeOut(Group(typ2, txt0, txt1, txt2)),
            g4.anim.points.scale(0.65).to_border(UP).shift(DOWN),
            duration=2
        )
        self.play(
            Write(tip)
        )
        self.play(
            Pause(3)
        )
        self.play(
            FadeOut(tip)
        )

        self.forward(6)

        self.play(
            FadeOut(Group(mattypes, g4))
        )
        self.forward(2.5)


class TL17_Sub1(SharpDelimTemplate):
    def construct(self):
        con3d = Container3D().apply_depth_test().show()
        con3d(ImageItem).color.fade(0.2)
        base = np.array([0.662, 0.2, 0.7222])
        axis = DashedLine(base * -4, base * 4, color=BLUE_A, dashed_ratio=0.4).apply_depth_test().show()
        # self.camera.points.set(orientation=Quaternion(0.8, 0.3, -0.05, 0.52))
        # self.camera.points.shift([-0.52, 0.49, 0.46])
        self.camera.points.set(orientation=Quaternion(0.92, 0.32, 0.08, 0.23))

        typ = TypstMath('hat(n) = vec(0.662, 0.2, 0.7222)', depth=-20).fix_in_frame().show()
        typ['hat(n)'].set(color=YELLOW)
        typ.points.shift([2.58, 0.37, 0])

        self.forward()


class TL18(SharpDelimTemplate):
    def construct(self):
        seq_play_audio_with_subtitles(
            self,
            [
                { 'file': 'audio_12_6.wav', 'begin': 0, 'end': 15.2, 'delay': 0, 'mul': 1.25 },
            ]
        )

        ####################################################

        typ1 = TypstText(
            R'''
            #let bo(body) = box(width: 4em, height: 3em, align(horizon, body))
            #let bm(n) = $mat(#bo[矩阵 $#n$])$
            $
                bm(n)
                bm(text(size: #0.7em, n-1))
                dots.c
                bm(2)
                bm(1)
            $
            '''
        )

        typ2 = TypstMath(
            R'''
            mat(
                #box(width: 4em, height: 3em, align(horizon)[单个矩阵])
            )
            '''
        )

        ####################################################

        self.forward()
        self.play(Write(typ1[::-1]))
        self.forward(4)
        self.play(
            Transform(typ1, typ2)
        )
        self.forward(2)

        typ1.show()
        typ1.points.shift(UP * 0.3)
        alphaeff = AlphaEffect(typ1)
        alphaeff.alpha.set(0)

        self.play(
            alphaeff.anim.alpha.set(0.35),
            typ2.anim.points.shift(DOWN  * 0.3)
        )

        self.forward(4.6)


class TL19(SharpDelimTemplate):
    def construct(self):
        seq_play_audio_with_subtitles(
            self,
            [
                { 'file': 'audio_12_6.wav', 'begin': 15.5, 'end': 78.2, 'delay': 0, 'mul': 1.25 },
            ]
        )

        ####################################################

        typ1 = TypstText(
            R'''
            缩放两倍：
            #box(baseline: 40%)[$
                mat(2,0,0,0;0,2,0,0;0,0,2,0;0,0,0,1)
            $]
            ''',
            color=YELLOW_A
        )

        typ2 = TypstText(
            R'''
            位移 $vec(1,2,3)$ 个单位：
            #box(baseline: 40%)[$
                mat(1,0,0,1;0,1,0,2;0,0,1,3;0,0,0,1)
            $]
            ''',
            color=PURPLE_A
        )
        g1 = Group(typ1, typ2)
        g1.points.arrange(buff=LARGE_BUFF).to_border(UP)

        part1 = typ1[5:].copy()
        part2 = typ2[11:].copy()

        vec1 = TypstMath('vec(x,y,z,1)')

        g2 = Group(part2, part1, vec1)
        g2.points.arrange()

        arrow = Arrow(RIGHT * 2, LEFT * 2, color=YELLOW)
        arrow.points.next_to(g2, DOWN)

        vec2 = TypstMath('vec(2x,2y,2z,1)')
        vec2.points.move_to(vec1)
        vec2.generate_target().points.next_to(part2)

        vec3 = TypstMath('vec(2x+1,2y+2,2z+3,1)')
        vec3.points.move_to(vec2.target)

        ####################################################

        self.forward(2.7)
        self.show(typ1)
        self.forward(2)
        self.show(typ2)
        self.forward(3)

        self.play(
            FadeIn(vec1)
        )
        self.forward(2)
        self.play(
            Transform(typ1[5:], part1, hide_src=False, path_arc=60 * DEGREES)
        )
        self.forward(1.2)
        self.play(
            Transform(typ2[11:], part2, hide_src=False, path_arc=60 * DEGREES),
            duration=1.3
        )
        self.forward(4.5)
        self.play(
            GrowArrow(arrow),
            duration=2
        )
        self.forward(1.5)
        self.play(
            TransformMatchingDiff(g2[1, 2], vec2)
        )
        self.forward(2)
        self.play(
            MoveToTarget(vec2)
        )
        self.play(
            TransformMatchingDiff(Group(part2, vec2), vec3)
        )
        self.forward(3.5)
        self.play(
            vec3.anim.points.to_border(LEFT, buff=LARGE_BUFF),
            FadeOut(arrow)
        )
        self.forward(6)

        ####################################################

        g12 = Group(typ1, typ2)
        g12.generate_target()
        for item, dir in zip(g12.target, [UR, UL]):
            item.points.scale(0.6, about_edge=dir)

        prefix_str = '缩放两倍然后位移 $vec(1,2,3)$ 个单位：'

        typ3 = TypstText(
            fR'''
            {prefix_str}
            #box(baseline: 40%)[$
                mat(1,0,0,1;0,1,0,2;0,0,1,3;0,0,0,1)
                mat(2,0,0,0;0,2,0,0;0,0,2,0;0,0,0,1)
            $]
            '''
        )
        typ3.points.next_to(g12.target, DOWN, buff=SMALL_BUFF).shift(UP * 0.3)
        typ3['$ mat(1,0,0,1;0,1,0,2;0,0,1,3;0,0,0,1) $'].set(color=PURPLE_A)
        typ3['$ mat(2,0,0,0;0,2,0,0;0,0,2,0;0,0,0,1) $'].set(color=YELLOW_A)

        typ3part2 = typ3[17:43]
        typ3part1 = typ3[43:]

        typ4 = TypstText(
            fR'''
            {prefix_str}
            #box(baseline: 40%)[$
                mat(2,0,0,1;0,2,0,2;0,0,2,3;0,0,0,1)
            $]
            '''
        )
        typ4.match_pattern(typ3, prefix_str)

        for t in (typ3, typ4):
            prefix = t[prefix_str]
            prefix.set(color=YELLOW_A)
            cnt = len(prefix)
            for i, item in enumerate(prefix):
                item.color.mix(PURPLE_A, i / (cnt - 1))

        ####################################################

        self.play(
            MoveToTarget(g12),
            Write(typ3[prefix_str])
        )
        self.forward(0.5)
        self.play(
            Transform(typ1[5:], typ3part1, hide_src=False),
            Transform(typ2[11:], typ3part2, hide_src=False, duration=0.7),
            lag_ratio=0.8
        )
        self.forward(0.7)
        self.play(
            # Transform(typ3[prefix_str], typ4[prefix_str]),
            TransformMatchingDiff(typ3, typ4),
            FadeOut(g12, UP, at=0.5),
            duration=1.4
        )
        self.play(
            typ4.anim.points.shift(UP)
        )

        ####################################################

        typ5 = TypstMath(
            R'''
            mat(2,0,0,1;0,2,0,2;0,0,2,3;0,0,0,1)
            vec(x,y,z,1)
            '''
        )
        typ5parts = Group(typ5[:26], typ5[26:])

        typ6 = TypstMath('vec(2x+1,2y+2,2z+3,1)')

        ####################################################

        self.play(
            FadeIn(typ5parts[1]),
            Transform(typ4[17:], typ5parts[0], hide_src=False, path_arc=30 * DEGREES),
            lag_ratio=0.6
        )
        self.forward(2)
        self.play(
            TransformMatchingDiff(typ5, typ6)
        )
        self.forward()

        ####################################################

        g = Group(vec3, typ6)
        eq = TypstMath('=')
        eq.points.shift(LEFT * 2)

        ####################################################

        self.play(
            g.anim.points.arrange(buff=LARGE_BUFF),
            Write(eq),
            eq.update.points.shift(RIGHT * 2),
            duration=2
        )
        self.forward(6)

        self.play(
            FadeOut(Group(g, eq, typ4))
        )

        self.forward()


class TL20(SharpDelimTemplate):
    def construct(self):
        seq_play_audio_with_subtitles(
            self,
            [
                { 'file': 'audio_12_6.wav', 'begin': 79, 'end': 103, 'delay': 0, 'mul': 1.25 },
            ]
        )

        ####################################################

        plane = NumberPlane(faded_line_ratio=1)

        container = ImageItem('container.jpg', height=1.6)

        vec1 = Vector([2, 1])
        vec2 = Vector([6, 1.5], color=RED, glow_alpha=0.6, glow_color=RED)

        ####################################################

        self.forward(1.5)
        self.play(
            FadeIn(Group(plane, container)),
            duration=3
        )
        self.forward(4.5)
        self.play(
            container.anim(rate_func=ease_inout_quint).points.shift(RIGHT * 2 + UP),
            GrowArrow(vec1, rate_func=ease_inout_quint)
        )
        self.play(
            Group(Group(plane, container)).anim.points.scale([3, 1.5, 1]),
            Transform(vec1, vec2)
        )
        self.forward(4)
        self.play(
            FadeOut(Group(plane, container, vec2))
        )

        self.forward(8)


class All(AboveTimelines):
    excludes = [TL17_Sub1]
