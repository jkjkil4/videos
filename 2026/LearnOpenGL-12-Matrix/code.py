# flake8: noqa
import sys

sys.path.append('.')

from janim.imports import *

with reloads():
    from utils.template import *
from utils.template import *


class SweepRect(SurroundingRect):
    def __init__(self, *items: Points, direction=..., **kwargs):
        super().__init__(
            Group(*items),
            **merge_dicts_recursively(
                Rect.preset_highlight_fill,
                {
                    'fill_alpha': 0.25
                }
            ),
            depth=1,
            **kwargs
        )

        if direction is ...:
            w, h = self.points.box.size
            direction = RIGHT if w > h else DOWN

        self.direction = np.array(direction)
        self.dim = np.where(self.direction != 0)[0][0]

    def anim_in(self, rate_func=rush_from, **kwargs):
        return DataUpdater(
            self,
            lambda data, p: data.points.stretch(p.alpha, dim=self.dim, about_edge=-self.direction),
            rate_func=rate_func,
            become_at_end=False,
            **kwargs,
            name='SweepRect in'
        )
    
    def anim_out(self, rate_func=rush_into, **kwargs):
        return DataUpdater(
            self,
            lambda data, p: data.points.stretch(1 - p.alpha, dim=self.dim, about_edge=self.direction),
            rate_func=rate_func,
            hide_at_end=True,
            become_at_end=False,
            **kwargs,
            name='SweepRect out'
        )
    
    def ins(*rects: SweepRect, **kwargs):
        return AnimGroup(
            *[rect.anim_in() for rect in rects],
            **kwargs
        )
    
    def outs(*rects: SweepRect, **kwargs):
        return AnimGroup(
            *[rect.anim_out() for rect in rects],
            **kwargs
        )
    

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


class TL1(SharpDelimTemplate):
    def construct(self):
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

        self.play(Write(txt))
        self.play(
            txt.anim.color.fade(0.5),
            FadeIn(typ, scale=0.5)
        )
        self.play(
            Transform(typ, typ1),
            txt.anim.points.shift(UP * 2)
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
            duration=1.4
        )

        self.play(
            ShowSubitemsOneByOne(yellowtyp)
        )

        self.play(
            SweepRect.ins(r1, r2, lag_ratio=0.2),
            SweepRect.outs(r1, r2, lag_ratio=0.2),
            lag_ratio=1,
            duration=0.5
        )

        self.play(
            SweepRect.ins(r3, r4, r5, lag_ratio=0.2),
            SweepRect.outs(r3, r4, r5, lag_ratio=0.2),
            lag_ratio=1,
            duration=0.5
        )

        self.play(Write(typ2t3))

        self.play(Write(typij))

        self.play(
            FadeOut(txt),
            Write(typi),
            Write(typj, at=0.4)
        )

        self.play(
            SweepRect.ins(r1, r4)
        )
        self.play(
            typ2t3.anim.points.scale(0.6).next_to(typij, UP)
        )

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
        self.play(CircleIndicate(typ1[2]))

        self.play(FadeOut(Group(typi2, typj2, r2, r3, typ1, typ2t3, typij)))

        self.forward()


class TL2(SharpDelimTemplate):
    def construct(self):
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
        self.play(FadeIn(typx, scale=0.5), FadeIn(typy, scale=0.5), lag_ratio=0.5)
        self.play(
            FadeOut(Group(typi, typj, typx, typy, img)),
            typ1.anim.points.to_center()
        )

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
        self.play(FadeOut(typ1))

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
        self.play(FadeOut(Group(typo1, typo2, typo3)))

        self.forward()


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
                TransformMatchingDiff(t1, t2)
            )

        self.play(FadeOut(typ4))
        
        self.forward()


class TL4(SharpDelimTemplate):
    def construct(self):
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
        self.play(
            FadeOut(typ)
        )


class TL5(SharpDelimTemplate):
    def construct(self):
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
        self.play(
            FadeIn(cursor, UL + UP, rate_func=rush_from)
        )
        self.play(
            cursor.anim(path_arc=-PI).points.shift([-0.01, -0.51, -0.0])
        )
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
        self.play(
            Transform(typ1[:6], typ2[:6]),
            FadeOut(typ1[6:]),
            Write(typ2[6:])
        )
        self.play(
            FadeIn(hl)
        )
        self.play(
            FadeOut(Group(hl, typ2))
        )

        self.forward()


def apply_bgshadow(vitem: VItem, radius=0.05, alpha=0.4) -> None:
    vitem.set(stroke_background=True, stroke_radius=radius)
    vitem.stroke.set(BLACK, alpha)


class TL6(SharpDelimTemplate):
    def construct(self):
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
        self.play(
            GrowArrow(vec1),
            GrowArrow(vec2),
            AnimGroup(
                FadeIn(typ1),
                FadeIn(typ2),
                at=0.4
            )
        )
        lines.save_state()
        self.play(
            lines.anim.set(color=YELLOW_D)
        )
        self.play(
            lines.anim.load_state()
        )
        self.play(
            FadeIn(typm)
        )
        self.play(
            SweepRect.ins(r1, r2, lag_ratio=0.5)
        )
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
        self.play()

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
        plane.hide()
        plane1.show()
        self.play(
            FadeIn(plane_orig, duration=0.5),
            Transform(g1, g2),
            typ1.anim.points.next_to([3, 1, 0], UR, buff=0),
            typ2.anim.points.next_to([1, 2, 0], UR, buff=0),
            FadeOut(typ1),
            FadeOut(typ2)
        )

        self.play(
            Flash(typ3, flash_radius=0.5),
            Flash(typ4, flash_radius=0.5),
        )

        self.forward()

        self.play(
            FadeOut(g2),
            FadeIn(g1),
        )
        plane_orig.hide()

        self.forward()

        self.play(
            FadeIn(typv)
        )
        self.play(
            Transform(typv, dot1, flatten=True, hide_src=False)
        )
        self.play(
            Flash(dot1, flash_radius=0.4)
        )
        self.play(
            FadeIn(plane_orig, duration=0.5),
            Transform(g1, g2),
            Transform(dot1, dot2)
        )
        self.play(
            Flash(dot2, flash_radius=0.4)
        )

        self.forward()

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
        self.play(
            FadeIn(plane_orig, duration=0.5),
            Transform(g1, g2),
            Transform(dot1, dot2),
            FadeIn(typml),
            tr.anim.set_value({'v1': [3, 1], 'v2': [1, 2]}),
            ItemUpdater(typfj, typfj_updater),
            duration=5
        )
        _Flash = partial(Flash, flash_radius=0.6)
        self.play(
            AnimGroup(
                _Flash(typfj[7:11]),
                _Flash(typ3),
            ),
            AnimGroup(
                _Flash(typfj[14:]),
                _Flash(typ4),
            ),
            lag_ratio=1
        )
        self.play(
            ShowPassingFlashAround(typfj[5]),
            ShowPassingFlashAround(typfj[12]),
        )
        self.play(
            Write(typr)
        )

        self.forward()

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
        self.play(
            FadeIn(plane_orig, duration=0.5),
            Transform(g1, g2),
            Transform(dot1, dot2),
            Write(typeq[:11])
        )
        self.play(
            Write(typeq[11:21]),
            Write(typeq[21:28]),
            Write(typeq[28:]),
            lag_ratio=1
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

        self.forward()


class TL7(SharpDelimTemplate):
    def construct(self):
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

        self.play(
            Write(typ1[::-1])
        )
        self.play(
            GrowArrow(arrow)
        )
        self.play(
            FadeIn(hl1)
        )
        self.play(
            hl1.anim.set(fill_alpha=1e-5),
            FadeIn(hl2)
        )
        self.play(
            FadeOut(Group(hl1, hl2, arrow)),
        )
        self.play(
            FadeIn(hl3),
            opertypes[2].anim.set(color=GREY),
            opertypes[3].anim.set(color=YELLOW)
        )
        self.play(
            FadeOut(hl3),
            FadeOut(typ1[13:])
        )
        self.play(
            Transform(mat2, typ2)
        )

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
        self.play(
            Transform(typ2[:6], typ3[17:23], hide_src=False),
            TransformMatchingDiff(Group(typ2[7], typ2[10:]).copy(), typ3[23:27], duration=1)
        )
        self.play(
            Write(typ3[27:])
        )
        self.play(
            Transform(typ3[12:16], typ4[2:6], hide_src=False, path_arc=40 * DEGREES),
            Transform(typ3[29:33], typ4[6:10], hide_src=False, path_arc=40 * DEGREES),
            lag_ratio=0.8
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
        self.play(
            FadeOut(hl),
            FadeOut(typ3),
            FadeOut(Group(r1, r2))
        )
        self.play(
            TransformMatchingDiff(g24, matmul1)
        )
        self.play(
            Write(matmul2)
        )
        self.play(
            FadeOut(Group(matmul1, matmul2))
        )

        self.forward()


class TL8(SharpDelimTemplate):
    def construct(self):
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

        self.play(
            FadeIn(g)
        )
        self.play(
            apply_matrix(g, [[3,0],[0,1]]),
            FadeIn(mat2, DOWN * 0.5)
        )
        self.play(
            apply_matrix(g, [[0,-1],[1,0]]),
            FadeIn(mat1, DOWN * 0.5)
        )
        
        self.forward()

        self.play(
            FadeOut(Group(g, mat1, mat2))
        )
        g.load_state()
        self.hide(mat1, mat2)
        Group(mat2, mat1).points.arrange().to_border(UP)
        self.play(
            FadeIn(g)
        )

        self.forward()

        self.play(
            apply_matrix(g, [[0,-1],[1,0]]),
            FadeIn(mat1, DOWN * 0.5)
        )
        self.play(
            apply_matrix(g, [[3,0],[0,1]]),
            FadeIn(mat2, DOWN * 0.5)
        )
        self.play(
            FadeOut(Group(mat1, mat2, g, opertypes))
        )

        self.forward()


class TL9(SharpDelimTemplate):
    def construct(self):
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

        self.play(
            Write(txt, duration=2)
        )
        self.play(
            FadeIn(g)
        )

        self.play(
            FadeOut(Group(txt, g))
        )

        ####################################################

        computer = SVGItem('computer.svg', alpha=0.5)

        ####################################################

        self.play(Write(computer))

        self.play(
            FadeOut(computer),
            FadeIn(g)
        )
        self.play(
            FadeOut(g)
        )

        self.forward()


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

        self.play(mattypes[0].anim.set(fill_color=YELLOW))
        self.play(Write(mat1, stroke_color=WHITE))
        self.play(
            Create(line, duration=0.5),
            FadeIn(line, duration=0.25),
        )
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
        self.play(
            FadeTransform(r1, vec1, path_arc=PI / 2),
            FadeTransform(r2, vec2, path_arc=PI / 2),
            lag_ratio=1
        )
        self.play(
            ApplyWave(vec1),
            ApplyWave(vec2),
            lag_ratio=1
        )

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
        self.play(
            Write(mat2[26:])
        )
        self.play(
            ShowCreationThenDestructionAround(mat2[26:44]),
            ShowCreationThenDestructionAround(mat2[72:]),
        )

        self.play(mat2(VItem).anim.color.fade(0.75), Write(txt))
        self.play(Pause(4))
        self.play(
            FadeOut(Group(txt, mat2))
        )

        self.forward()


class TL11(SharpDelimTemplate):
    def construct(self):
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
            mattypes[1].anim.set(fill_color=YELLOW)
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

        g1.hide()
        mat1, rs1 = g1 = get_mat(2, 0.7)
        g1.show()
        _CircleIndicate = partial(CircleIndicate, rate_func=there_and_back_with_pause)
        self.play(
            _CircleIndicate(mat1.get_element(0, 0), buff=0.5),
            _CircleIndicate(vec1.tip)
        )
        self.play(
            _CircleIndicate(mat1.get_element(1, 1)),
            _CircleIndicate(vec2.tip)
        )

        self.forward()

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
            FadeIn(g1)
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
            FadeIn(typ3)
        )
        vec3_orig.show()
        self.play(
            ItemUpdater(g1, lambda p: get_mat(1 + 1 * p.alpha, 1 - 0.3 * p.alpha)),
            g.anim.load_state('transformed'),
            Transform(vec3, vec4),
            FadeTransform(typ3, typ4, hide_src=False),
            typ3(VItem).anim(duration=0.3).color.fade(0.7)
        )

        self.play(
            FadeOut(Group(g, plane_orig, vec3_orig, vec4, typ3, typ4, g1))
        )

        self.forward()


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
            ShowPassingFlashAround(mat1.get_element(0, 0), time_width=0.65),
            ShowPassingFlashAround(mat1.get_element(1, 1), time_width=0.65),
        )
        self.play(
            Write(txt1)
        )
        self.play(
            ShowPassingFlashAround(mat2.get_element(0, 0), time_width=0.65),
            ShowPassingFlashAround(mat2.get_element(1, 1), time_width=0.65),
        )
        self.play(
            Write(txt2)
        )

        self.play(
            FadeOut(Group(mat1, mat2, txt1, txt2))
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
            )
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
            *map(GrowArrow, vecs)
        )
        self.play(
            FadeIn(typs)
        )
        apply_bgshadow(eq[37:41](VItem))
        apply_bgshadow(eq[56:69](VItem))
        self.play(FadeIn(eqparts[1, 2]))
        self.play(
            Write(eqparts[3]),
            FadeIn(eqparts[4]),
            lag_ratio=0.4
        )

        ####################################################

        # ts1 = TransformableFrameClip(rs, eq).show()
        ts1 = Group(rs, eq)
        ts2 = TransformableFrameClip(con3d, vecs, typs).show()

        ####################################################

        self.play(
            Destruction(plane, rate_func=rush_into, duration=0.6),
            ts1.anim.points.shift(RIGHT),
            ts2.anim.clip.set(x_offset=0.15, y_offset=-0.1)
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

        self.play(
            ShowCreationThenFadeAround(eq[23]),
            ShowCreationThenFadeAround(eq[40]),
            ShowCreationThenFadeAround(eq[68]),
        )
        self.play(
            rs(VItem).anim.color.fade(0.5),
            FadeIn(hl)
        )
        self.play(
            FadeIn(fr)
        )

        self.forward()


class TL13(SharpDelimTemplate):
    def construct(self):
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
            mattypes[2].anim.set(fill_color=YELLOW)
        )

        self.play(
            FadeIn(plane)
        )

        self.play(
            FadeIn(dot1, scale=0.2)
        )
        self.play(
            GrowArrow(arrow),
            Write(typplus)
        )
        
        self.play(
            Transform(dot1, dot2, hide_src=False),
            dot1.anim(duration=0.3).color.fade(0.7)
        )

        self.play(
            FadeOut(Group(plane, dot1, dot2, arrow, typplus)),
            Write(typ1)
        )
        self.play(Write(txt1))
        self.play(
            g1.anim.points.shift(UP),
            FadeIn(g2)
        )

        self.play(
            FadeOut(Group(g1, g2))
        )

        self.forward()


class All(AboveTimelines):
    pass
