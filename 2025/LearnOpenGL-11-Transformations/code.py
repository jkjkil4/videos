# flake8: noqa
import sys

sys.path.append('.')

from janim.imports import *

with reloads():
    from utils.template import *
from utils.template import *


class Wiggle(DataUpdater[Points]):
    def __init__(self, item: Points, amount: float = 0.05, times: float = 2, **kwargs):
        super().__init__(
            item, 
            lambda data, p: data.points.shift(math.sin(TAU * times * p.alpha) * amount * RIGHT),
            **kwargs
        )


class Cursor(MarkedItem, SVGItem):
    def __init__(self, **kwargs):
        super().__init__('cursor.svg', height=0.5, **kwargs)
        self.mark.set_points([[-0.12, 0.2, 0]])


class OutlinedDot(Dot):
    def __init__(
        self,
        point=ORIGIN, 
        radius=DEFAULT_DOT_RADIUS,
        stroke_alpha=1,
        fill_color=BLACK,
        **kwargs
    ):
        super().__init__(
            point,
            radius,
            stroke_alpha=stroke_alpha,
            fill_color=fill_color,
            **kwargs
        )


class TL1(Template):
    CONFIG = Config(
        typst_shared_preamble=Template.CONFIG.typst_shared_preamble + t_(
            R'''
            #set math.mat(delim: "[")
            '''
        )
    )

    def construct(self):
        ####################################################

        container = ImageItem('container.jpg', width=2.2, height=2)
        container.save_state()

        rect1 = Rect(stroke_alpha=0, fill_alpha=1, depth=1, color=ORANGE)
        rect1.points.replace(container, stretch=True)
        rect2 = ImageItem('blank.png', width=2.2, height=2, color=[RED, GREEN, GREEN, BLUE], depth=1)
        
        phycenter_dot = Dot(radius=0.06, stroke_alpha=1, stroke_color=BLACK, stroke_radius=0.01, color=ORANGE)

        cursor = Cursor()
        cursor.points.shift([2.24, -4.49, 0.0])

        box = Group(container, phycenter_dot)
        boxc = Group(box, cursor)

        ####################################################

        with self.shows(rect1):
            self.forward()
        with self.shows(rect2):
            self.forward()
        container.show()
        self.forward()
        self.play(FadeIn(phycenter_dot, scale=0.2))
        self.play(Wiggle(phycenter_dot))
        self.play(
            cursor.anim(path_arc=50 * DEGREES)
                .mark.set(ORIGIN)
        )
        self.play(
            boxc.anim.points.shift([-2.21, -0.7, -0.0])
        )
        self.play(
            boxc.anim.points.shift([4.15, 0.54, 0.0])
        )
        self.play(
            cursor.anim.points.shift([1.1, 0.94, 0.0])
        )
        self.play(
            box.update.points.rotate(-40 * DEGREES),
            cursor.anim(path_arc=-40 * DEGREES)
                .points.shift([0.39, -0.92, 0.0])
        )

        ####################################################

        gr = Rect(2.2, 2, color=GREEN_B)
        gr.points.shift(RIGHT * 2)
        gr.save_state()
        gr.points.rotate(-40 * DEGREES).shift([-0.05, -0.16, 0.0])

        grg = Group(container, gr)

        def get_coords():
            points = container.points.get()
            glpoints = points[:, :2] / [Config.get.frame_x_radius, Config.get.frame_y_radius]
            txts = Group[Text]()
            for p, glp, dir in zip(points, glpoints, [UL, DL, UR, DR]):
                txt = Text(f'[{glp[0]:.2f}, {glp[1]:.2f}]', color=GREEN_B, font_size=12)
                txt.points.next_to(p, dir, buff=SMALL_BUFF)
                txts.add(txt)
            return txts

        ####################################################

        self.play(
            FadeOut(Group(phycenter_dot, cursor), duration=0.5),
            container.anim.load_state()
                .points.shift(RIGHT * 2),
            gr.anim.load_state(),
            FadeIn(gr)
        )

        grg.save_state()

        prev_coords = get_coords()
        self.play(Write(prev_coords), duration=1)

        for _ in range(10):
            self.prepare(Destruction(prev_coords), duration=0.1)
            self.forward(0.05)
            grg.points.rotate(-4 * DEGREES)
            new_coords = get_coords()
            self.play(Write(new_coords), duration=0.3)
            prev_coords = new_coords

        self.prepare(Destruction(prev_coords), duration=0.1)
        self.play(
            grg.anim.load_state()
        )
        new_coords = get_coords()
        self.play(Write(new_coords), duration=0.3)

        ####################################################

        txt_mat = TypstMath('mat(gap: #0.8em, column-gap: #1.5em, ,,;,"矩阵？",;,,;)')
        txt_mat.points.shift(LEFT * 3)

        arrow = Arrow(
            txt_mat.points.box.top, 
            grg.points.box.top, 
            path_arc=-PI * 0.7,
            buff=0.7,
            color=ORANGE
        )
        arrow_txt = arrow.create_text('作用“变换”', font_size=18, color=ORANGE)

        ####################################################

        self.play(FadeIn(txt_mat))
        self.play(
            GrowArrow(arrow),
            Write(arrow_txt),
            gr.anim.color.fade(0.5)
        )
        self.play(
            container.update.points.rotate(-40 * DEGREES),
            container.anim.points.scale([1.5, 0.7, 1]),
            container.anim.points.shift([0.64, 0.12, 0.0]),
            lag_ratio=1
        )

        ####################################################

        hl = HighlightRect(txt_mat)

        arrow1 = Arrow(LEFT * 2 + UP * 0.3, RIGHT * 2 + UP * 0.3, color=GREEN)
        arrow2 = Arrow(LEFT * 2 + DOWN * 0.3, RIGHT * 2 + DOWN * 0.3, color=ORANGE)
        arrows = Group(arrow1, arrow2)
        arrows.points.shift(LEFT)

        box = Group(gr, new_coords)
        box.generate_target()
        box.target[0].points.scale(0.5)
        for coord_txt, dir in zip(box.target[1], [UL, DL, UR, DR]):
            coord_txt.points.scale(0.8).next_to(box.target[0], dir, buff=SMALL_BUFF)
        box.target.points.next_to(arrow1, UP)

        txt_mat.generate_target() \
            .points.scale(0.6).next_to(arrow2, DOWN) \
            .r(VItem).color.set(ORANGE)
        
        gpu = SVGItem('gpu.svg')
        gpu.points.next_to(arrows)

        circle = Circle(color=YELLOW)
        circle.points.surround(txt_mat.target)

        new_con = ImageItem('container.jpg', alpha=0.5, depth=1, width=2.2, height=2)

        ####################################################

        self.play(FadeIn(hl))
        self.play(
            FadeOut(Group(container, arrow, arrow_txt)),
            FadeOut(hl),
        )
        self.play(
            GrowArrow(arrow1),
            GrowArrow(arrow2),
            MoveToTarget(box),
            MoveToTarget(txt_mat),
            FadeIn(gpu)
        )
        new_con.points.shift([3.58, 0.02, 0.0])
        self.play(
            AnimGroup(
                ShowPassingFlash(circle.copy()),
                Do(new_con.show),
                lag_ratio=0.8
            ),
            AnimGroup(
                ShowPassingFlash(circle.copy()),
                Do(lambda: new_con.points.rotate(-20 * DEGREES)),
                lag_ratio=0.8
            ),
            AnimGroup(
                ShowPassingFlash(circle.copy()),
                Do(lambda: new_con.points.scale([1.5, 0.8, 1])),
                lag_ratio=0.8
            ),
            lag_ratio=1.2
        )

        ####################################################

        arrow_fast = Arrow(txt_mat, gpu, path_arc=40 * DEGREES)
        arrow_fast_txt = Text('很快！')
        arrow_fast_txt.points.shift([0.83, -1.1, 0.0])

        coordsys = Group(
            RoundedRect(6.6, 3.6, fill_alpha=1, stroke_alpha=0),
            ImageItem('coordinate_systems.png')
                .points.shift(DOWN * 0.07)
                .r
        )

        quest = Text('?', font='Noto Sans S Chinese', font_size=200, fill_alpha=0.3, depth=2)

        ####################################################

        self.play(
            FadeOut(Group(box, arrows, new_con))
        )
        self.play(
            GrowArrow(arrow_fast),
            FadeIn(arrow_fast_txt)
        )
        with self.shows(coordsys):
            self.forward()
        self.play(
            FadeOut(Group(arrow_fast, arrow_fast_txt, gpu)),
            txt_mat.anim.points.to_center().scale(1.5)
        )
        self.play(Write(quest))

    @contextmanager
    def shows(self, item: Item):
        self.show(item)
        yield
        self.hide(item)


class TL2(Template):
    def construct(self):
        typ = TypstText(R'向量#h(4em)矩阵', scale=2)
        self.play(Write(typ))
        self.forward()


class TL3(Template):
    def construct(self):
        ####################################################

        axes = Axes(
            (-5, 11),
            (-3, 6),
            axis_config={
                'include_numbers': True
            }
        )
        axes.points.shift([-2.99, -1.12, 0.0])

        typ3d1 = TypstMath('(3,1)')
        typ3d1.points.next_to(axes.c2p(3,1), UR, buff=SMALL_BUFF)
        typ3d1d2 = TypstMath('(3,1,2)')
        typ3d1d2.points.next_to(axes.c2p(3,1), UR, buff=SMALL_BUFF).shift(OUT * 2)

        trpos = ValueTracker([0, 0, 0])
        
        def posg_updater(p=None):
            pos = trpos.current().get_value()
            p = axes.c2p(*pos)
            _DashedLine = partial(DashedLine, color=BLUE, dashed_ratio=0.35, strict_by_length=True)
            group = Group(
                OutlinedDot(p + OUT * pos[2], stroke_color=BLUE, depth=-1),
                # _DashedLine(axes.c2p(), axes.x_axis.n2p(pos[0])),
                _DashedLine(axes.x_axis.n2p(pos[0]), p),
                # _DashedLine(axes.c2p(), axes.y_axis.n2p(pos[1])),
                _DashedLine(axes.y_axis.n2p(pos[1]), p),
            )
            if pos[2] != 0:
                group.add(_DashedLine(axes.c2p(*pos), axes.c2p(*pos) + OUT * pos[2]))
            return group

        posg = posg_updater()

        ####################################################

        self.play(
            Create(axes, lag_ratio=0.05)
        )
        self.play(
            FadeIn(posg, scale=0.8, duration=0.3)
        )
        self.play(
            Aligned(
                Succession(
                    trpos.anim.set_value([3, 0, 0]),
                    trpos.anim.set_value([3, 1, 0]),
                ),
                ItemUpdater(posg, posg_updater)
            )
        )
        self.play(Write(typ3d1))
        self.camera.save_state()
        self.play(
            self.camera.anim.points.set(orientation=Quaternion(0.9, 0.36, 0.09, 0.22))
        )
        self.play(
            trpos.anim.set_value([3, 1, 2]),
            ItemUpdater(posg, posg_updater),
            TransformMatchingDiff(typ3d1, typ3d1d2, duration=1)
        )
        self.play(
            self.camera.anim.load_state(),
            trpos.anim.set_value([3, 1, 0]),
            ItemUpdater(posg, posg_updater),
            TransformMatchingDiff(typ3d1d2, typ3d1, duration=1)
        )

        ####################################################

        frect = FrameRect(**Rect.preset_shadow)

        typ_vecdesc = TypstText(
            R'''
            #set align(center)
            #set page(width: auto)

            #box(inset: 6pt, fill: black, stroke: white, width: 10em)[
                #set align(left)
                $(3,1)$\
                $(3,1,2)$
            ]\
            向量
            '''
        )
        typ_vecdesc.points.to_border(UL)

        vec = Vector([3, 1], color=RED, depth=-2)
        vec.points.shift(axes.c2p())

        vec_txt = vec.create_text('向量', color=RED)

        ####################################################

        self.play(
            FadeIn(frect),
            FadeIn(typ_vecdesc[0], scale=2)
        )
        self.play(
            Write(typ_vecdesc['$(3,1)$'])
        )
        self.play(
            Write(typ_vecdesc['$(3,1,2)$'])
        )
        self.play(
            Write(typ_vecdesc['向量'])
        )
        self.play(
            FadeOut(frect),
            GrowArrow(vec)
        )

        g1 = Group(axes.x_axis, typ3d1[1])
        g1.save_state()
        g2 = Group(axes.y_axis, typ3d1[3])
        g2.save_state()

        def apply_glow(g: Group[VItem]):
            g[0].set(glow_alpha=0.4)
            g[1].set(glow_alpha=0.7)

        self.play(
            g1.anim.do(apply_glow)
        )

        for p1, p2 in it.pairwise([(0,0), (1,0), (2,0), (3,0)]):
            line = Line(axes.c2p(*p1), axes.c2p(*p2), stroke_radius=0.04, color=YELLOW)
            self.play(ShowPassingFlash(line, time_width=0.4))

        self.play(
            g1.anim.load_state(),
            g2.anim.do(apply_glow)
        )

        for p1, p2 in it.pairwise([(3,0), (3,1)]):
            line = Line(axes.c2p(*p1), axes.c2p(*p2), stroke_radius=0.04, color=YELLOW)
            self.play(ShowPassingFlash(line, time_width=0.4))

        self.play(
            g2.anim.load_state()
        )
        self.play(FocusOn(posg[0]))

        self.play(
            FadeOut(Group(posg, typ_vecdesc, axes)),
            Write(vec_txt)
        )

        ####################################################

        cursor = Cursor()
        cursor.points.shift([-1.17, -1.16, 0.0])

        typ3d1.generate_target().points.shift(LEFT * 2 + UP * 0.5)

        txt2d = Text('2 维')
        txt2d.points.next_to(typ3d1.target, buff=MED_LARGE_BUFF)

        typ3d1d2.points.next_to(typ3d1.target, DOWN, buff=MED_LARGE_BUFF, aligned_edge=RIGHT)
        txt3d = Text('3 维')
        txt3d.points.next_to(typ3d1d2, buff=MED_LARGE_BUFF)

        def cursor_scale(**kwargs):
            return cursor.update(rate_func=there_and_back, become_at_end=False, **kwargs) \
                .points.scale(1.4)

        ####################################################

        self.play(
            ShowCreationThenDestructionAround(typ3d1)
        )
        self.play(
            FadeOut(Group(vec, vec_txt)),
            MoveToTarget(typ3d1)
        )
        self.play(
            cursor.anim(path_arc=20 * DEGREES, rate_func=rush_from)
                .points.shift([-0.4, 1.45, 0.0]),
            FadeIn(cursor)
        )
        self.play(
            cursor.anim(path_arc=PI * 0.8)
                .points.shift([0.33, -0.03, 0.0]),
            cursor_scale()
        )
        self.play(Write(txt2d))
        self.play(Write(typ3d1d2))

        self.play(
            cursor.anim(path_arc=20 * DEGREES, rate_func=linear)
                .points.shift([-0.69, -0.84, -0.0]),
            cursor_scale(),
            rate_func=rush_from
        )
        self.play(
            cursor.anim(path_arc=PI * 0.8)
                .points.shift([0.36, -0.01, 0.0]),
            cursor_scale()
        )
        self.play(
            cursor.anim(path_arc=PI * 0.8)
                .points.shift([0.34, 0.0, 0.0]),
            cursor_scale()
        )
        self.play(Write(txt3d))

        self.forward()


class TL4(Template):
    def construct(self):
        
        ####################################################

        self.camera.points.shift([1.93, 2.16, 0.0])

        _NumberPlane = partial(
            NumberPlane,
            axis_config={
                'include_numbers': True
            },
            faded_line_ratio=0,
            background_line_style={
                'alpha': 0.5
            }
        )

        plane = _NumberPlane((-6, 10), (-2, 7)).show()
        large_plane = _NumberPlane((-15, 12), (-5, 16))

        vec1 = Vector([3, 2], color=RED_A)
        txt1 = TypstMath('macron(v) = (3,2)', color=RED_A)
        txt1_3d = TypstMath('macron(v) = (3,2,0)', color=RED_A)
        for txt in (txt1, txt1_3d):
            txt.points.next_to(vec1.points.get_end(), UP, buff=SMALL_BUFF)

        vec2 = Vector([-3, 0], color=GREEN_A)
        txt2 = TypstMath('macron(n) = (-3,0)', color=GREEN_A)
        txt2_3d = TypstMath('macron(n) = (-3,0,0)', color=GREEN_A)
        for txt in (txt2, txt2_3d):
            txt.points.next_to(vec2.points.get_end(), UP, buff=SMALL_BUFF)

        dot11 = SmallDot(ORIGIN, color=YELLOW)
        dot12 = SmallDot(vec1.points.get_end(), color=YELLOW)

        ####################################################

        self.play(
            GrowArrow(vec1),
            Write(txt1),
            GrowArrow(vec2),
            Write(txt2)
        )

        plane.hide()
        large_plane.show()
        self.camera.save_state()
        self.play(
            self.camera.anim
                .points.set(orientation=Quaternion(0.9, 0.39, 0.07, 0.17))
                       .shift([-0.53, -1.63, 0.05]),
            TransformMatchingDiff(txt1, txt1_3d),
            TransformMatchingDiff(txt2, txt2_3d),
        )
        self.play(
            self.camera.anim.load_state(),
            TransformMatchingDiff(txt1_3d, txt1),
            TransformMatchingDiff(txt2_3d, txt2),
        )
        large_plane.hide()
        plane.show()

        self.play(
            ShowPassingFlash(vec1.copy().set(color=YELLOW, depth=-1), time_width=0.3),
            ShowPassingFlash(vec2.copy().set(color=YELLOW, depth=-1), time_width=0.3),
        )

        self.play(
            FadeIn(dot11, scale=0.05, hide_at_end=True),
            ShowPassingFlash(vec1.copy().set(color=YELLOW, depth=-1), time_width=0.3),
            FadeOut(dot12, scale=20, rate_func=rush_from),
            lag_ratio=0.9
        )

        ####################################################

        vec1g = Group(vec1, txt1[3:]).copy()
        vec2g = Group(vec2, txt2[3:]).copy()
        vecsg = Group(vec1, txt1, vec2, txt2)

        ####################################################

        self.play(
            FadeOut(vecsg),
            vec1g.anim.points.shift([1, 3, 0]),
            vec2g.anim.points.shift([6, 3, 0])
        )
        vecsg(VItem).color.fade(0.35)
        self.play(
            FadeIn(vecsg),
        )

        ####################################################

        bvecs = TypstMath('macron(v) = vec(3,2,0) wide macron(n) = vec(-3,0,0)')
        bvecs['macron(v) = vec(3,2,0)'].set(color=RED_A)
        bvecs['macron(n) = vec(-3,0,0)'].set(color=GREEN_A)
        bvecs.points.move_to(self.camera)

        ####################################################

        self.play(
            FadeOut(Group(plane, vec1, vec2, vec1g, vec2g)),
            TransformMatchingDiff(Group(txt1, txt2), bvecs, path_arc=-PI * 0.7)
        )

        self.forward()


class TL5(Template):
    def construct(self):
        ####################################################

        typ = TypstText(
            R'''
            #import "@janim/colors:0.0.0": *
            #set align(center)
            #set text(BLUE_A)

            #let b(label-name, title, body) = [
                #box(
                    table(
                        columns: 1,
                        stroke: BLUE_A,
                        [
                            #set text(size: 0.8em)
                            #box(title) #label(label-name + "-text")
                        ],
                        {
                            set text(size: 0.7em)
                            body
                        }
                    )
                ) #label(label-name)
            ]

            #b("vec-scalar")[
                向量与标量计算
            ][
                #grid(
                    columns: 2,
                    gutter: 10pt,
                    $ macron(v) + x $,
                    $ macron(v) - x $,
                    $ macron(v) times x $,
                    $ macron(v) div x $,
                )
            ]

            #b("vec-inv")[
                向量取反
            ][
                $ -macron(v) $
            ]

            #b("vec-vec")[
                向量加减
            ][
                $ macron(v) + macron(k) $

                $ macron(v) - macron(k) $
            ]

            #b("vec-norm")[
                向量长度
            ][
                $ norm(macron(v)) = sqrt(x^2 + y^2) $
            ]

            #b("vec-vec-mul")[
                向量相乘
            ][
                $ macron(v) dot macron(k) $

                $ macron(v) times macron(k) $
            ]
            '''
        )

        label_names = ['vec-scalar', 'vec-inv', 'vec-vec', 'vec-norm', 'vec-vec-mul']

        title = Title('与向量有关的计算')
        parts = [
            typ.get_label(label_name)
            for label_name in label_names
        ]
        txts = Group.from_iterable(
            typ.get_label(label_name + '-text')
            for label_name in label_names
        )

        parts[0].points.move_to([-2.57, 1.27, 0.0])
        parts[1].points.move_to([1.24, 0.38, 0.0])
        parts[2].points.move_to([-3.91, -1.19, -0.0])
        parts[3].points.move_to([-0.3, -2.03, 0.0])
        parts[4].points.move_to([4.23, -0.79, 0.0])

        fade_items = Group.from_iterable(it.chain(*parts))
        fade_items.remove(*it.chain(*txts))

        ####################################################

        self.play(Write(title))
        self.play(
            *[
                FadeIn(part, scale=1.5, rate_func=rush_from)
                for part in parts
            ],
            lag_ratio=0.4
        )
        self.play(
            FadeOut(title),
            FadeOut(fade_items),
            txts.anim(path_arc=-40 * DEGREES)
                .points.arrange(DOWN, aligned_edge=LEFT).to_border(UL)
        )

        self.forward()


class VecOpersTypes(Text):
    def __init__(self):
        super().__init__(
            '向量与标量计算\n向量取反\n向量加减\n向量长度\n向量相乘', 
            color=BLUE_A,
            depth=-1000
        )
        self.points.scale(0.8).arrange(DOWN, aligned_edge=LEFT).to_border(UL)
        self.fix_in_frame()


class TL6(Template):
    # CONFIG = Config(
    #     typst_math_preamble=t_(
    #         R'''
    #         #let cr = text.with(red)
    #         #let cg = text.with(green)
    #         #let cb = text.with(blue)
    #         '''
    #     )
    # )

    def construct(self):
        ####################################################

        opertypes = VecOpersTypes().show()

        equations = [
            TypstMath(f'vec(1,2,3) {oper} x = vec(1 {oper} x,2 {oper} x,3 {oper} x)')
            for oper in ['+', '-', 'times', 'div']
        ]
        for eq in equations:
            eq['1', ...].set(color=RED)
            eq['2', ...].set(color=GREEN)
            eq['3', ...].set(color=BLUE)
        for eq in equations[1:]:
            eq.match_pattern(equations[0], 'x =')

        txt1 = Text('向量', color=RED_A)
        txt2 = Text('标量', color=PURPLE_B)
        Group(txt1, txt2).points.arrange(buff=MED_LARGE_BUFF - 0.25).shift([-0.8, 1.11, 0.0])

        def get_parts(eqidx: int):
            eq = equations[eqidx]
            return Group(
                eq[:4],
                eq[4:7],
                eq[7:11],
                eq[11],
                eq[12],
                eq[13],
                eq[14:18],
                Group(eq[18], eq[21], eq[24]),
                Group(eq[19], eq[22], eq[25]),
                Group(eq[20], eq[23], eq[26]),
                eq[27:],
            )
        
        parts = get_parts(0)

        hl = boolean_ops.Union(
            SurroundingRect(parts[3]),
            SurroundingRect(parts[-3]),
            stroke_radius=0.01,
            stroke_alpha=0.5,
            color=YELLOW,
            glow_alpha=0.5
        )

        ####################################################

        self.play(opertypes[0].anim.set(color=YELLOW))
        self.play(Write(txt1))
        self.play(Write(txt2))

        def opin(eqidx: int):
            return FadeIn(equations[eqidx][11], DOWN * 0.3, rate_func=rush_from)
        
        def opout(eqidx: int):
            return FadeOut(equations[eqidx][11], DOWN * 0.3, rate_func=rush_from)

        self.play(FadeIn(parts[:3]))
        self.play(FadeIn(parts[4]))
        self.play(ShowPassingFlashAround(parts[4]))
        self.play(opin(0))
        for i1, i2 in it.pairwise([0, 1, 2, 3]):
            self.play(opout(i1), opin(i2))
        self.play(opout(3))

        self.play(Write(parts[3]))
        self.play(
            Transform(parts[1], parts[-4], path_arc=70 * DEGREES, flatten=True, hide_src=False),
            FadeIn(parts[-5, -1]),
        )
        self.play(
            Transform(parts[3], parts[-3], flatten=True, hide_src=False),
            Transform(parts[4], parts[-2], flatten=True, hide_src=False),
            FadeIn(parts[5], scale=0.5, at=0.5)
        )
        self.play(FadeIn(hl))
        for eq1, eq2 in it.pairwise(equations):
            self.play(
                Transform(eq1, eq2)
            )
        self.play(FadeOut(hl))

        ####################################################

        vec = Vector([2,0.8], color=RED_A)
        vec.points.shift([-2, -1, 0])

        veq = TypstMath('macron(v) times x')
        veq['macron(v)'].set(color=RED_A)
        veq.match_pattern(equations[0], 'x').points.shift(LEFT * 0.15)

        mul1 = TypstMath('macron(v)', color=RED_A)
        mul2 = TypstMath('macron(v) times 2', color=RED_A)
        mul3 = TypstMath('macron(v) times 3', color=RED_A)

        mul1.points.next_to(vec.points.get_end(), UR, buff=SMALL_BUFF)

        veqg = Group(txt1, txt2, veq)
        veqg.generate_target()[-1].points.shift(UP * 0.3)
        veqg.target.points.shift(UP)

        tip = TypstText(
            R'''
            #set page(width: 30em)
            #set text(size: 0.8em, gray)
            注意，数学上是没有向量与标量相加减这种运算的，但是在程序上，比如我们在 Python 里用到的 `numpy` 就对它们有支持。
            '''
        )

        vec1 = Group(vec, mul1)

        ####################################################

        lasteqparts = get_parts(-1)

        self.play(
            FadeOut(lasteqparts[5:]),
            TransformMatchingDiff(lasteqparts[:5], veq)
        )
        self.play(
            MoveToTarget(veqg),
            AnimGroup(
                GrowArrow(vec),
                Write(mul1),
                at=0.5
            )
        )
        vec.save_state()
        vec.generate_target().points.scale(2, about_point=vec.points.get_start()).r.place_tip()
        mul2.points.next_to(vec.target.points.get_end(), UR, buff=SMALL_BUFF)
        self.play(
            MoveToTarget(vec),
            TransformMatchingDiff(mul1, mul2, duration=1)
        )
        vec.generate_target().points.scale(3 / 2, about_point=vec.points.get_start()).r.place_tip()
        mul3.points.next_to(vec.target.points.get_end(), UR, buff=SMALL_BUFF)
        self.play(
            MoveToTarget(vec),
            TransformMatchingDiff(mul2, mul3, duration=1)
        )
        self.play(
            vec.anim.load_state(),
            TransformMatchingDiff(mul3, mul1, duration=1)
        )

        ####################################################

        vpeq = TypstMath('macron(v) + x')
        vpeq['macron(v)'].set(color=RED_A)
        vpeq.match_pattern(veq, 'x')

        ####################################################

        self.play(
            FadeOut(vec1),
            TransformMatchingDiff(veq, vpeq, duration=1),
        )
        self.play(FadeIn(tip))
        self.play(FadeOut(tip))

        ####################################################

        vec1.points.shift([2.43, 0.17, 0.0])
        v = vpeq[:2]
        minus = TypstMath('-')
        minus.points.next_to(v, LEFT, buff=SMALL_BUFF)

        vecm = vec.copy()
        vecm.points.scale(-1, about_point=vecm.points.get_start())
        mulm = TypstMath('- macron(v)')
        mulm['macron(v)'].set(color=RED_A)
        mulm.points.next_to(vecm, DL, buff=SMALL_BUFF)

        typm = TypstMath('- vec(1,2,3) = vec(-1,-2,-3)')
        typm['1', ...].set(color=RED)
        typm['2', ...].set(color=GREEN)
        typm['3', ...].set(color=BLUE)
        tip = TypstText('（或者说，用 $-1$ 数乘该向量）')
        tip.points.next_to(typm['vec(-1,-2,-3)'], DOWN, aligned_edge=LEFT)

        parts = Group(
            typm[0],
            typm[1:5],
            typm[5:8],
            typm[8:12],
            typm[12],
            typm[13:17],
            Group(typm[17], typm[19], typm[21]),
            Group(typm[18], typm[20], typm[22]),
            typm[23:],
        )

        ####################################################

        self.play(
            opertypes[0].anim.set(color=GREY),
            opertypes[1].anim.set(color=YELLOW),
            FadeOut(vpeq[2:]),
            FadeOut(txt2),
            FadeIn(minus, RIGHT * 0.2),
            FadeIn(vec1)
        )
        self.play(
            Transform(vec, vecm, hide_src=False),
            TransformMatchingDiff(mul1.copy(), mulm, duration=1, path_arc=40 * DEGREES),
            vec1(VItem).anim(duration=0.5).color.fade(0.7)
        )
        self.play(
            FadeOut(Group(vec1, vecm, mulm)),
        )
        self.play(
            FadeIn(parts[:4])
        )
        self.play(
            FadeIn(parts[-4, -1]),
            Transform(parts[2], parts[-2], hide_src=False, path_arc=70 * DEGREES)
        )
        self.play(
            Transform(parts[0], parts[-3], flatten=True, hide_src=False),
            FadeIn(parts[-5], scale=0.5, at=0.5)
        )

        ####################################################

        typp = TypstMath(
            'vec(1,2,3) + vec(4,5,6) = vec(1+4,2+5,3+6) = vec(5,7,9)'
        )
        typp['1', ...].set(color=RED)
        typp['2', ...].set(color=GREEN)
        typp['3', ...].set(color=BLUE)
        typp['4', ...].set(color=RED)
        typp['5', (0, 1)].set(color=GREEN)
        typp['6', ...].set(color=BLUE)
        typp['5', 2].set(color=RED)
        typp['7'].set(color=GREEN)
        typp['9'].set(color=BLUE)

        ####################################################

        self.play(
            FadeOut(Group(txt1, minus, v, typm)),
            opertypes[1].anim.color.set(GREY),
            opertypes[2].anim.color.set(YELLOW),
        )

        parts1 = Group(
            typp[:4],
            typp[4:7],
            typp[7:16],
            typp[16:19],
            typp[19:23],
        )

        parts2 = Group(
            typp[23],
            typp[24:28],
            Group(typp[28], typp[31], typp[34]),
            Group(typp[29], typp[32], typp[35]),
            Group(typp[30], typp[33], typp[36]),
            typp[37:41],
        )

        parts3 = Group(
            typp[41],
            typp[42:46],
            typp[46:49],
            typp[49:],
        )

        self.play(
            FadeIn(parts1)
        )
        self.play(
            FadeIn(parts2[0, 1, -1]),
            Transform(parts1[1], parts2[2], hide_src=False, path_arc=70 * DEGREES),
            Transform(parts1[-2], parts2[-2], hide_src=False, path_arc=70 * DEGREES),
        )
        self.play(
            Write(parts2[-3])
        )
        self.play(
            FadeIn(parts3[0, 1, -1]),
        )
        self.play(
            Write(parts3[-2])
        )
        self.play(
            FadeOut(typp)
        )


class TL7(Template):
    def construct(self):
        ####################################################

        opertypes = VecOpersTypes().show()
        opertypes[:2](VItem).color.set(GREY)
        opertypes[2].color.set(YELLOW)
        
        self.camera.points.shift([2, 1.5, 0])

        plane = NumberPlane(
            (-5, 11),
            (-3, 7),
            faded_line_ratio=0,
            axis_config={
                'include_numbers': True
            },
            depth=10
        )

        vec_v = Vector([4,2], color=RED_A)
        typ_v = TypstMath('macron(v) = vec(4,2)', color=RED_A)
        typ_v.points.next_to(vec_v, UR, buff=SMALL_BUFF)
        gv = Group(vec_v, typ_v)

        vec_k = Vector([1,2], color=GREEN_A)
        typ_k = TypstMath('macron(k) = vec(1,2)', color=GREEN_A)
        typ_k.points.next_to(vec_k, UR, buff=SMALL_BUFF)
        gk = Group(vec_k, typ_k)

        _DashedLine = partial(DashedLine, color=YELLOW, dashed_ratio=0.4, depth=5)
        d1 = _DashedLine(plane.c2p(5,4), plane.c2p(5,0))
        d2 = _DashedLine(plane.c2p(5,4), plane.c2p(0,4))

        typ_vk1 = TypstMath('macron(v) + macron(k) = vec(4,2) + vec(1,2)')
        typ_vk2 = TypstMath('macron(v) + macron(k) = vec(5,4)')
        typ_vk1.patterns('macron(v)', '4', ('2', 0)).set(color=RED_A)
        typ_vk1.patterns('macron(k)', '1', ('2', 1)).set(color=GREEN_A)
        typ_vk2.patterns('macron(v)').set(color=RED_A)
        typ_vk2.patterns('macron(k)').set(color=GREEN_A)

        typ_vk1.points.next_to([5,4,0], UP, buff=SMALL_BUFF)
        typ_vk2.points.next_to([5,4,0], UP, buff=SMALL_BUFF)

        vec_vk = Vector([5,4], color=YELLOW)

        ####################################################

        self.play(Create(plane, lag_ratio=0.05))
        self.play(
            GrowArrow(vec_v),
            Write(typ_v),
            GrowArrow(vec_k),
            Write(typ_k),
        )
        self.play(
            gk.anim.points.shift([4, 2, 0]),
            self.camera.anim.points.shift(UR)
        )
        self.play(
            TransformMatchingShapes(Group(typ_v, typ_k), typ_vk1)
        )
        self.play(
            FadeOut(typ_vk1[9:12], scale=0.1),
            Transform(typ_vk1[:7], typ_vk2[:7]),
            Transform(Group(typ_vk1[7], typ_vk1[12]), typ_vk2[7], flatten=True),
            Transform(Group(typ_vk1[8], typ_vk1[13]), typ_vk2[8], flatten=True),
            Transform(typ_vk1[14], typ_vk2[9]),

            GrowArrow(vec_vk),
            Group(vec_v, vec_k)(VItem).anim.color.fade(0.75)
        )
        self.play(
            ShowPassingFlash(d1, time_width=0.8, lag_ratio=0.1),
            ShowPassingFlash(d2, time_width=0.8, lag_ratio=0.1),
            lag_ratio=0.7,
            duration=1
        )

        self.play(
            FadeOut(Group(plane, vec_vk, typ_vk2, vec_v, vec_k))
        )

        self.forward()


class TL8(Template):
    def construct(self):
        ####################################################

        opertypes = VecOpersTypes().show()
        opertypes[:2](VItem).color.set(GREY)
        opertypes[2].color.set(YELLOW)

        typ = TypstMath(
            R'''
            vec(1,2,3)
            -
            vec(4,5,6)
            =
            vec(1+(-4), 2+(-5), 3+(-6)) 
            =
            vec(-3,-3,-3)
            '''
        ).fix_in_frame()
        typ.patterns(('1', ...), '4', '-4', ('-3', 0)).set(color=RED)
        typ.patterns(('2', ...), '5', '-5', ('-3', 1)).set(color=GREEN)
        typ.patterns(('3', (0, 1)), '6', '-6', ('-3', 2)).set(color=BLUE)

        ####################################################

        parts = Group(typ[:23], typ[23], typ[24:50], typ[50], typ[51:])

        self.play(
            SpinInFromNothing(parts[0], path_arc=40 * DEGREES),
            Write(parts[1]),
            SpinInFromNothing(parts[2], path_arc=40 * DEGREES),
            Write(parts[3]),
            SpinInFromNothing(parts[4], path_arc=40 * DEGREES),
            lag_ratio=1.2
        )
        self.play(Destruction(typ))

        ####################################################

        self.camera.points.shift([2, 1.5, 0])

        plane = NumberPlane(
            (-7, 11),
            (-4, 7),
            faded_line_ratio=0,
            axis_config={
                'include_numbers': True
            },
            depth=10
        )

        vec_w = Vector([0.5, 3.5], color=GREEN_A)
        typ_w = TypstMath('macron(w) = vec(0.5, 3.5)', color=GREEN_A)
        typ_w.points.next_to(vec_w, UR, buff=SMALL_BUFF)
        gw = Group(vec_w, typ_w)

        vec_v = Vector([3, 2], color=RED_A)
        typ_v = TypstMath('macron(v) = vec(3, 2)', color=RED_A)
        typ_v.points.next_to(vec_v, UR, buff=SMALL_BUFF)
        gv = Group(vec_v, typ_v)

        typ_nv = TypstMath('"" -macron(v) = -vec(3, 2)', color=RED_A)
        typ_nv.points.next_to(vec_v, UR, buff=SMALL_BUFF)
        typ_nv.match_pattern(typ_v, 'v')

        vec_res = Vector([-2.5, 1.5], color=YELLOW)
        vec_res.points.shift([3,2,0])

        g = Group(vec_w, vec_v)

        typ = TypstMath(
            R'''
            macron(w) - macron(v)
            =
            vec(0.5, 3.5) - vec(3, 2)
            '''
        )
        typ.patterns('macron(w)', 'vec(0.5,3.5)').set(color=GREEN_A)
        typ.patterns('macron(v)', 'vec(3,2)').set(color=RED_A)
        typ.points.next_to(vec_res.points.get_end(), UP, buff=SMALL_BUFF)
        typbg = SurroundingRect(typ, depth=1, **Rect.preset_shadow)

        typp = TypstMath(
            R'''
            macron(w) - macron(v)
            =
            vec(-2.5, 1.5)
            '''
        )
        typp['macron(w)'].set(color=GREEN_A)
        typp['macron(v)'].set(color=RED_A)
        typp.match_pattern(typ, '=')
        typpbg = SurroundingRect(typp, depth=1, **Rect.preset_shadow)

        typg = Group(typ_w, typ_nv)

        ####################################################

        self.play(
            FadeIn(plane),
            FadeIn(gw),
            FadeIn(gv),
        )

        self.play(
            vec_v.anim.points.scale(-1),
            TransformMatchingDiff(typ_v, typ_nv, duration=1),
            Flash(typ_nv[0], at=0.5)
        )

        self.play(
            GrowArrow(vec_res),
            g(VItem).anim.color.fade(0.5),
            TransformMatchingShapes(typg, typ),
            FadeIn(typbg, at=0.5),
        )

        self.play(
            Transform(typbg, typpbg),
            TransformMatchingDiff(typ, typp)
        )

        self.play(
            plane.anim.points.shift([3,2,0]),
            self.camera.anim.points.shift(UR * 1.4)
        )

        ####################################################

        _DashedLine = partial(DashedLine, color=YELLOW, dashed_ratio=0.4, depth=5)
        d1 = _DashedLine(plane.c2p(-2.5,1.5), plane.c2p(-2.5,0))
        d2 = _DashedLine(plane.c2p(-2.5,1.5), plane.c2p(0,1.5))

        ####################################################

        self.play(
            ShowPassingFlash(d1, time_width=0.8, lag_ratio=0.1),
            ShowPassingFlash(d2, time_width=0.8, lag_ratio=0.1),
            lag_ratio=0.7,
            duration=1
        )

        self.play(
            FadeOut(Group(typp, vec_res, vec_w, vec_v, plane))
        )


class TL9(Template):
    def construct(self):
        ####################################################

        opertypes = VecOpersTypes().show()
        opertypes[:2](VItem).color.set(GREY)
        opertypes[2].color.set(YELLOW)

        plane = NumberPlane(
            (-7, 12),
            (-4, 9),
            faded_line_ratio=0,
            axis_config={
                'include_numbers': True
            },
            depth=10
        )
        self.camera.points.shift([2, 1.5, 0])

        vec = Vector([4,2], color=RED_A)
        typ = TypstMath('macron(v) = vec(4,2)')
        typ['macron(v)'].set(color=RED_A)
        typ['4'].set(color=RED)
        typ['2'].set(color=GREEN)
        typ.points.next_to(vec, UR, buff=SMALL_BUFF)

        ####################################################

        self.play(
            opertypes[2].anim.set(color=GREY),
            opertypes[3].anim.set(color=YELLOW)
        )

        self.play(
            Create(plane, lag_ratio=0.5)
        )
        self.play(
            GrowArrow(vec),
            Write(typ)
        )

        ####################################################

        def pline(p1, p2, **kwargs):
            return Line(plane.c2p(*p1), plane.c2p(*p2), **kwargs)
        
        xline = pline((0,0), (4,0), color=RED)
        yline = pline((4,0), (4,2), color=GREEN)

        poly = Polygon(plane.c2p(0,0), plane.c2p(4,0), plane.c2p(4,2), color=YELLOW)

        gg = TypstMath('norm(macron(v)) = sqrt(4^2 + 2^2) = sqrt(16 + 4) = sqrt(20) approx 4.47')
        gg.points.shift([3.88, 3.49, 0.0])
        gg['macron(v)'].set(color=RED_A)
        gg.patterns('4', '16').set(color=RED)
        gg.patterns('2', ('4', 1)).set(color=GREEN)

        txt = Text('<c RED_A>向量</c>的长度    <c GREY><fs 0.7>使用勾股定理即可</fs></c>', format='rich')
        txt.points.next_to(gg, UP, aligned_edge=LEFT, buff=SMALL_BUFF * 1.5)
        
        ggbg = SurroundingRect(Group(gg, txt), depth=5, **Rect.preset_shadow)

        ####################################################

        self.play(
            Transform(typ['4'][0], xline, hide_src=False, path_arc=-PI * 0.6),
            Transform(typ['2'][0], yline, hide_src=False, path_arc=-PI * 0.6),
            lag_ratio=0.5
        )
        self.play(
            ShowPassingFlash(poly)
        )
        self.play(
            FadeIn(ggbg),
            Write(txt[0][:5]),
            FadeIn(txt[0][5:]),
            FadeIn(gg[:4])
        )
        self.play(Write(gg[4:]))

        ####################################################

        vec3d = Vector([4, 2, 3], color=RED_A)

        typ3d = TypstMath('macron(v) = vec(4,2,3)')
        for pa, co in zip(['macron(v)', '4', '2', '3'], [RED_A, RED, GREEN, BLUE]):
            typ3d[pa].set(color=co)
        typ3d.points.next_to(vec3d.points.get_end(), DR, buff=SMALL_BUFF)

        comp3d = TypstMath('norm(macron(v)) = sqrt(4^2 + 2^2 + 3^2) = sqrt(29)')
        comp3d['macron(v)'].set(color=RED_A)
        comp3d['4'].set(color=RED)
        comp3d['2'].set(color=GREEN)
        comp3d['3'].set(color=BLUE)
        comp3d.fix_in_frame()
        comp3d.points.shift([1.59, 2.11, 0])

        shadow = pline((0,0), (4,2), color=RED_A, alpha=0.25)

        dl = DashedLine(plane.c2p(4,2), plane.c2p(4,2) + OUT * 3, color=BLUE)

        self.camera.save_state()

        ####################################################

        self.play(
            FadeOut(Group(ggbg, gg, txt)),
            self.camera.anim
                .points.set(orientation=Quaternion(0.97, 0.25, 0.01, 0.02)) \
                        .shift([0.91, 1, -0.27]),
            Transform(vec, vec3d),
            Group(plane.background_lines, plane.faded_lines)(VItem).anim
                .color.fade(0.5),
            FadeIn(shadow),
            TransformMatchingDiff(typ, typ3d, duration=1),
            Create(dl, lag_ratio=1.2)
        )

        self.play(Write(comp3d))

        self.play(
            *[
                FadeOut(item, root_only=True)
                for item in self.visible_items()
                if item not in opertypes.descendants()
            ]
        )

        self.forward()


class TL10(Template):
    def construct(self):
        ####################################################

        opertypes = VecOpersTypes().show()
        opertypes[:3](VItem).color.set(GREY)
        opertypes[3].color.set(YELLOW)

        plane = NumberPlane(
            faded_line_ratio=0,
            axis_config={
                'include_numbers': True
            },
            depth=10
        )
        plane(VItem).color.fade(0.6)

        vec = Vector(color=RED_A)
        vec.points.rotate(30 * DEGREES, about_point=ORIGIN)
        
        ####################################################

        _Rotate = partial(Rotate, about_point=ORIGIN, rate_func=ease_inout_quart)

        self.play(GrowArrow(vec, rate_func=rush_from))
        self.play(
            _Rotate(vec, 40 * DEGREES)
        )
        self.play(
            _Rotate(vec, -200 * DEGREES)
        )
        self.play(
            _Rotate(vec, 80 * DEGREES)
        )
        self.play(
            FadeIn(plane),
            _Rotate(vec, 50 * DEGREES)
        )

        ####################################################

        brace = Brace(vec, buff=SMALL_BUFF * 0.5).show()
        bracetxt = brace.points.create_text('1')

        g = Group(vec, brace, bracetxt)

        desc = Text('单位向量', font_size=30, color=YELLOW).fix_in_frame()
        desc.points.shift(UP * 3)

        ####################################################

        self.play(
            Write(desc),
            Write(Group(brace, bracetxt))
        )
        self.play(
            _Rotate(g, 70 * DEGREES)
        )
        self.play(
            _Rotate(g, -20 * DEGREES)
        )

        self.play(FadeOut(g))

        ####################################################

        tr_vec = ValueTracker([3.7, 2.1, 0])

        def curval():
            return tr_vec.current().get_value()

        def vec_updater(p=None, normalized=False, alpha=1, color=RED_A):
            value = curval()
            if normalized:
                value = normalize(value)
            vec = Vector(value, color=color)
            vec.color.fade(1-alpha)
            return vec
        
        tvec_updater = partial(vec_updater, alpha=0.4)
        nvec_updater = partial(vec_updater, normalized=True, color=YELLOW)

        vec = vec_updater()
        nvec = nvec_updater()

        typ1 = TypstMath('macron(v)', color=RED_A)
        typ2 = TypstMath('hat(n) = macron(v) / norm(macron(v))')
        typ2['hat(n)'].set(color=YELLOW)
        typ2['macron(v)', ...].set(color=RED_A)

        typ1.points.next_to(vec, UR, buff=SMALL_BUFF)
        typ2.points.next_to(nvec.points.get_end(), RIGHT, buff=SMALL_BUFF)

        def FollowArrow(item, arrow, normal=False):
            def updater(group, p):
                value = curval()
                dir = np.sign(value)
                if dir[0] == 0:
                    dir[0] = 0
                if not normal:
                    dir[1] = 1
                else:
                    dir[1] = 0
                    value = normalize(value)
                group.points.next_to(value, dir, buff=SMALL_BUFF)
            return GroupUpdater(item, updater)
        
        cursor = Cursor(depth=-10)
        cursor.mark.set(curval())

        def Holding():
            return ItemUpdater(
                None,
                lambda p: Dot(curval(), color=YELLOW, fill_alpha=0.5, glow_alpha=0.5, depth=-5)
            )
        
        def CursorFollow():
            return GroupUpdater(
                cursor,
                lambda group, p: group.mark.set(curval())
            )
        
        def Updaters():
            return AnimGroup(
                Holding(),
                CursorFollow(),
                ItemUpdater(vec, tvec_updater),
                ItemUpdater(nvec, nvec_updater),
                FollowArrow(typ1, vec),
                FollowArrow(typ2, nvec, normal=True)
            )

        ####################################################

        self.play(
            GrowArrow(vec),
            Write(typ1)
        )
        self.play(
            Transform(vec, nvec, hide_src=False),
            vec.anim.color.fade(0.6),
            Transform(typ1, typ2, hide_src=False, path_arc=-50 * DEGREES)
        )
        self.play(
            FadeIn(cursor, UL * 0.3 + UP * 0.2)
        )
        self.play(
            ShowCreationThenDestructionAround(typ2[:2])
        )
        self.play(
            tr_vec.anim.set_value([2, -2.4, 0]),
            Updaters()
        )
        self.play(
            tr_vec.anim.set_value([-3.4, -1.3, 0]),
            Updaters()
        )
        self.play(
            tr_vec.anim(rate_func=rush_into).set_value([-1.4, 2, 0]),
            Updaters()
        )
        self.play(
            tr_vec.anim(rate_func=rush_from).set_value([3.7, 2.1, 0]),
            Updaters()
        )
        self.play(FadeOut(cursor))

        ####################################################

        arrow = Arrow(typ1, nvec.points.get_end(), max_length_to_tip_length_ratio=0.03, path_arc=PI * 0.6)
        arrowtxt = arrow.create_text('标准化<fs 0.5>(或单位化)</fs>', font_size=18, format='rich')

        line = Line(ORIGIN, np.array(curval()) * 2, color=YELLOW)

        ####################################################

        self.camera.save_state()

        self.play(
            GrowArrow(arrow),
            Write(arrowtxt)
        )
        self.play(
            self.camera.anim
                .points.scale(0.58)
                       .shift([1.02, 0.43, 0.0]),
            FadeOut(desc)
        )
        self.play(
            FadeOut(Group(arrow, arrowtxt, vec, typ1))
        )
        self.play(
            ShowPassingFlash(line, rate_func=rush_into, time_width=0.4, duration=0.6)
        )

        self.play(
            *[
                FadeOut(item, root_only=True)
                for item in self.visible_items()
                if item not in opertypes.descendants()
            ]
        )

        self.forward()


def colorize_vec(typ: TypstDoc) -> None:
    patterns = [
        ('macron(v)', RED_A),
        ('macron(k)', GREEN_A)
    ]
    for pa, co in patterns:
        if not isinstance(typ, TypstMath):
            pa = f'${pa}$'
        try:
            typ[pa, ...].set(color=co)
        except PatternMismatchError:
            pass


def Tick(**kwargs):
    return VItem(
        [-0.77, 1.58, 0], [-0.77, 1.58, 0], [-0.76, 1.58, 0], [-0.75, 1.57, 0], [-0.75, 1.57, 0],
        [-0.75, 1.57, 0], [-0.73, 1.54, 0], [-0.71, 1.53, 0], [-0.71, 1.53, 0], [-0.7, 1.53, 0],
        [-0.63, 1.6, 0], [-0.58, 1.65, 0], [-0.43, 1.77, 0],
        **kwargs
    )


class TL11(Template):
    def construct(self):
        ####################################################

        opertypes = VecOpersTypes().show()
        opertypes[:3](VItem).color.set(GREY)
        opertypes[3].color.set(YELLOW)

        typ1 = TypstMath('vec(1,2,3)')
        typ2 = TypstMath('vec(5,6,7)')
        typ12 = TypstMath('vec(5,12,21)')
        for pa, co in zip(['1', '2', '3'], [RED, GREEN, BLUE]):
            typ1[pa].set(color=co)
        for pa, co in zip(['5', '6', '7'], [RED, GREEN, BLUE]):
            typ2[pa].set(color=co)
        for pa, co in zip(['5', '12', '21'], [RED, GREEN, BLUE]):
            typ12[pa].set(color=co)

        txtt = Text('乘')

        g12 = Group(typ1, typ2)
        g12.points.arrange(buff=MED_LARGE_BUFF * 1.5)

        np.random.seed(114514015)
        quest = Text('?', font='Noto Sans S Chinese', font_size=64, depth=1, fill_alpha=0.5)
        quests = quest * 5
        for q in quests:
            q.points.shift(np.random.random((1,3)) * 3 - 1.5)
            q.points.scale(np.random.rand() * 0.3 + 0.7)

        multypes = TypstText(
            R'''
            #import "@preview/fletcher:0.5.8": diagram, node, edge
            #set text(size: 0.8em)
            
            #diagram(
                edge-stroke: white,
                spacing: (1em, 0.2em),
                // debug: 2,
                node-inset: 2pt,
                node((1,1))[
                    #show: box.with(width: 6em)
                    #set align(left)
                    点乘 $macron(v) dot macron(k)$
                ],
                node((1,2))[
                    #show: box.with(width: 6em)
                    #set align(left)
                    叉乘 $macron(v) times macron(k)$
                ],
                edge((0,0), "d,r"),
                edge((0,0), "dd,r"),
            )
            '''
        ).fix_in_frame()
        colorize_vec(multypes)
        multypes_parts = [
            multypes[:6],
            multypes[7:14],
            multypes[15:],
        ]
        multypes.points.next_to(opertypes, DOWN, aligned_edge=LEFT, buff=SMALL_BUFF).shift(RIGHT * 0.1)

        type1 = multypes_parts[1].copy()
        type2 = multypes_parts[2].copy()

        types = Group(type1, type2)
        types.points.scale(1.5).arrange(DOWN, buff=MED_LARGE_BUFF).to_center()

        ####################################################

        self.play(
            opertypes[3].anim.set(color=GREY),
            opertypes[4].anim.set(color=YELLOW)
        )

        self.play(
            FadeIn(typ1, RIGHT),
            FadeIn(typ2, LEFT)
        )
        self.play(Write(txtt))
        self.play(
            FadeOut(txtt),
            FadeTransform(Group(typ1, typ2), typ12),
            FadeIn(quests, scale=0.7, lag_ratio=0.4, rate_func=linear)
        )
        self.play(
            FadeOut(Group(quests, typ12))
        )

        self.play(
            Write(type1)
        )
        self.play(
            Write(type2)
        )
        self.play(
            Transform(type1, multypes_parts[1]),
            Transform(type2, multypes_parts[2]),
            FadeIn(multypes_parts[0]),
            duration=1.6
        )

        ####################################################

        plane = NumberPlane(
            faded_line_ratio=0,
            axis_config={
                'include_numbers': True
            },
            depth=10
        )

        typ = TypstMath(
            'macron(v) dot macron(k) = norm(macron(v)) dot norm(macron(k)) dot cos theta',
            depth=-5
        ).fix_in_frame()
        colorize_vec(typ)
        parts = [
            typ[6:10],
            typ[11:15],
            typ[16:],
        ]

        typ.generate_target().points.to_border(UP)
        typbg = SurroundingRect(typ.target, depth=-4, **Rect.preset_shadow).fix_in_frame()

        vec_v = Vector([3,1], color=RED_A)
        vec_k = Vector([1,2], color=GREEN_A)

        angle = Angle(vec_v, vec_k)
        angle_txt = TypstMath('theta')
        angle_txt.points.next_to(angle, UR, buff=0)
        angg = Group(angle, angle_txt)

        def Squeezed(*anims: Animation, factor: float):
            if len(anims) == 1:
                anim = anims[0]
            else:
                anim = AnimGroup(*anims)
            anim.scale_range(1 - factor)
            wait = factor / 2
            return Succession(
                Wait(wait),
                anim,
                Wait(wait)
            )
        
        def FlashArrow(arrow: Arrow):
            return ShowPassingFlash(
                arrow.copy().set(color=YELLOW, depth=-1, stroke_radius=0.04),
                time_width=0.5
            )
        
        _CircleIndicate = partial(CircleIndicate, circle_kwargs={ 'depth': -20 })

        ####################################################
        
        self.play(Write(typ[:5]))
        self.play(Write(typ[5:]))
        self.play(
            FadeIn(typbg),
            MoveToTarget(typ),
            FadeIn(plane)
        )
        self.play(
            GrowArrow(vec_v),
            GrowArrow(vec_k),
            lag_ratio=0.5
        )

        self.play(
            _CircleIndicate(parts[0]),
            Squeezed(FlashArrow(vec_v), factor=0.5),
            duration=2
        )
        self.play(
            _CircleIndicate(parts[1]),
            Squeezed(FlashArrow(vec_k), factor=0.5),
            duration=2
        )
        self.play(
            _CircleIndicate(parts[2]),
            Squeezed(
                Create(angle),
                Write(angle_txt),
                factor=0.5
            ),
            duration=2
        )

        self.camera.save_state()

        self.play(
            self.camera.anim.points.scale(0.5),
            FadeOut(plane.x_axis.numbers),
            FadeOut(plane.y_axis.numbers),
            plane.background_lines(VItem).anim.color.fade(0.5),
            duration=2
        )
        self.play(
            vec_v.anim.points.scale(1 / vec_v.points.length, about_point=ORIGIN).r.place_tip(),
            vec_k.anim.points.scale(1 / vec_k.points.length, about_point=ORIGIN).r.place_tip(),
            angg(VItem).anim.points.scale(0.7, scale_stroke_radius=True, about_point=ORIGIN),
        )

        ####################################################

        typnorm = TypstMath(R'& norm(macron(v)) = 1 \ & norm(macron(k)) = 1', depth=-20).fix_in_frame()
        typnorm.points.shift([2.93, 1.84, 0])
        colorize_vec(typnorm)

        nparts = [
            typnorm[5],
            typnorm[11],
        ]

        typsim1 = TypstMath('macron(v) dot macron(k) = 1 dot 1 dot cos theta', depth=-20)
        typsim2 = TypstMath('macron(v) dot macron(k) = cos theta', depth=-20)
        for t in (typsim1, typsim2):
            colorize_vec(t)
            t.fix_in_frame()
            t.match_pattern(typ, '=')

        cursor = Cursor().fix_in_frame()
        cursor.points.shift([0.89, 0.49, 0.0])

        tick1 = Tick(depth=-25, stroke_radius=0.04, color=YELLOW).fix_in_frame()
        tick2 = Tick(depth=-25, stroke_radius=0.04, color=YELLOW).fix_in_frame()
        tick1.points.shift([-0.75, 1.65, 0]).scale(1.5)
        tick2.points.shift([0.52, 1.65, 0]).scale(1.5)

        ####################################################

        self.play(
            Write(typnorm),
        )
        self.play(
            nparts[0].copy().anim(hide_at_end=True).points.move_to(parts[0]),
            nparts[1].copy().anim(hide_at_end=True).points.move_to(parts[1]),
            FadeOut(typnorm)
        )
        self.play(
            TransformMatchingDiff(typ, typsim1)
        )
        self.play(
            TransformMatchingDiff(typsim1, typsim2)
        )
        self.play(
            FadeIn(cursor, LEFT + UP * 2),
        )
        self.play(
            Create(tick1)
        )
        self.play(
            Create(tick2)
        )
        self.play(
            FadeOut(Group(tick1, tick2, cursor))
        )

        ####################################################

        def angle_updater(p=None):
            vec1 = vec_v.current()
            vec2 = vec_k.current()
            dot = np.dot(vec1.points.vector, vec2.points.vector)
            if abs(dot) < 0.02:
                angle = RightAngle(vec1, vec2, length=0.25 * 0.7)
            else:
                angle = Angle(vec1, vec2, radius=0.4 * 0.7)
            angle.radius.scale(0.7)
            return angle

        def cosval_updater(p=None):
            v1 = vec_v.current().points.vector
            v2 = vec_k.current().points.vector
            dot = np.dot(v1, v2)
            typ = TypstMath(f'= {dot:.2f}', color=YELLOW, depth=-20).fix_in_frame()
            typ.match_pattern(typsim2, '=')
            typ.points.next_to(typsim2, buff=SMALL_BUFF, coor_mask=(1, 0, 0))
            return typ
        
        cosval = cosval_updater()

        def Updaters():
            return AnimGroup(
                ItemUpdater(cosval, cosval_updater),
                ItemUpdater(angle, angle_updater),
                GroupUpdater(
                    angle_txt, 
                    lambda data, p: data.points.next_to(angle_updater().points.pfp(0.5), UR, buff=0.07)
                )
            )

        ####################################################

        self.play(
            FocusOn(angle_txt, duration=1.5),
            Write(cosval),
            lag_ratio=0.6
        )
        self.play(
            vec_k.update.points.rotate(45 * DEGREES, about_point=ORIGIN),
            Updaters()
        )
        self.play(
            *[
                ShowPassingFlash(
                    angle.copy().set(color=YELLOW, depth=-20, stroke_radius=0.03),
                    time_width=0.4,
                    rate_func=linear,
                    duration=0.6
                )
                for _ in range(3)
            ],
            lag_ratio=0.8
        )
        self.play(
            ShowPassingFlashAround(
                cosval, 
                surrounding_rect_config={ 'depth': -20 },
                time_width=0.5
            )
        )

        ####################################################

        sur = SurroundingRect(cosval, depth=-20).fix_in_frame()
        sur.points.stretch(1.3, dim=0, about_edge=LEFT)

        def bgcosval_updater(p=None):
            v1 = vec_v.current().points.vector
            v2 = vec_k.current().points.vector
            dot = np.dot(v1, v2)
            typ = TypstMath(f'{dot:.2f}', scale=3, color=YELLOW, depth=2, fill_alpha=0.25)
            typ.points.move_to_by_indicator(typ['.'], [-0.1, -0.3, 0])
            return typ
        
        bgcosval = bgcosval_updater()
        
        def Updaters2():
            return AnimGroup(
                Updaters(),
                ItemUpdater(bgcosval, bgcosval_updater)
            )

        ####################################################

        self.play(FadeIn(sur))

        self.play(
            vec_k.update.points.rotate(-PI / 2 + 1e-3, about_point=ORIGIN),
            Updaters2(),
            duration=2
        )
        self.play(
            vec_k.update.points.rotate(PI - 2e-3, about_point=ORIGIN),
            Updaters2(),
            duration=7
        )
        self.play(
            vec_k.update.points.rotate(-(PI - 2e-3), about_point=ORIGIN),
            Updaters2(),
            duration=3
        )
        self.play(
            vec_k.update.points.rotate(PI - 2e-3, about_point=ORIGIN),
            Updaters2(),
            duration=3
        )
        
        for axis in plane.get_axes():
            axis.remove(axis.numbers)
        self.play(
            FadeOut(Group(cosval, bgcosval, vec_v, vec_k, plane, angle, angle_txt, sur))
        )
        self.camera.load_state()

        ####################################################

        typ0 = TypstMath('macron(v) dot macron(k)')
        colorize_vec(typ0)

        typ1 = TypstMath('vec(0.6, -0.8, 0) dot vec(0, 1, 0) =')
        typ1.match_pattern(typ0, 'dot', 2, 0)
        typ1.patterns('0.6', ('0', 3)).set(color=RED)
        typ1.patterns('-0.8', '1').set(color=GREEN)
        typ1['0', (2, 4)].set(color=BLUE)

        typ0.points.scale(2, about_point=typ0['dot'].points.box.center)

        ####################################################

        self.play(Write(typ0))
        self.play(
            FadeTransform(typ0[:2], typ1[:16]),
            Transform(typ0[2], typ1[16]),
            FadeTransform(typ0[3:], typ1[17:-1]),
        )
        self.play(
            typ1.anim(show_at_begin=False).points.shift(LEFT * 1)
        )

        ####################################################

        typ2 = TypstMath('= vec(delim: #none, 0.6 times 0, -0.8 times 1, 0 times 0)')
        typ2.match_pattern(typ1, '=')
        typ2['0.6 times 0'].set(color=RED)
        typ2['-0.8 times 1'].set(color=GREEN)
        typ2['0 times 0'].set(color=BLUE)

        ####################################################

        typ1_parts = Group(
            typ1[4:7],
            Group(typ1[7:9], typ1[10]),
            typ1[11],
            typ1[21],
            typ1[22],
            typ1[23],
        )

        typ2_parts = [
            typ2[1:6],
            typ2[6:12],
            typ2[12:],
        ]

        _TsMatchingDiff = partial(
            TransformMatchingDiff,
            path_arc=-PI * 0.3,
            match=lambda item1, item2, p, **kwargs: Transform(item1, item2, **kwargs, hide_src=False)
        )

        self.play(Write(typ1[-1]))
        self.play(
            _TsMatchingDiff(typ1_parts[0, 3], typ2_parts[0], path_arc=-PI * 0.3),
            _TsMatchingDiff(typ1_parts[1, 4], typ2_parts[1], path_arc=-PI * 0.3),
            _TsMatchingDiff(typ1_parts[2, 5], typ2_parts[2], path_arc=-PI * 0.3),
        )

        ####################################################

        typ3 = TypstMath('= 0.6 times 0 + (-0.8) times 1 + 0 times 0')
        typ3.match_pattern(typ2, '=')
        typ3['0.6 times 0'].set(color=RED)
        typ3['(-0.8) times 1'].set(color=GREEN)
        typ3['0 times 0'].set(color=BLUE)

        typ4 = TypstMath('= -0.8')
        typ4.match_pattern(typ3, '=')
        typ4.points.shift(DOWN * 0.5)

        typeq = typ4.copy().set(depth=-20)
        typeq.points.next_to(typsim2, buff=SMALL_BUFF)

        hint = Text('（你可以自行验证它们的长度都是1）', font_size=16, color=GREY_D)
        hint.points.next_to(typ1, DOWN, aligned_edge=LEFT)

        typtheta = TypstText('进一步算出 $theta approx 143.1 degree$')
        typtheta.points.shift([0.56, 2.56, 0.0])

        ####################################################

        self.play(
            TransformMatchingDiff(typ2[1:], typ3[1:], path_arc=PI / 2)
        )
        self.play(
            Write(typ4)
        )
        self.play(
            FadeOut(typ3[1:]),
            FadeOut(typ1[-1]),
            typ4.anim.points.shift(UP * 0.5)
        )
        
        self.play(
            Create(tick1)
        )

        tick2.points.shift(DOWN * 0.2)
        self.play(
            FadeIn(hint),
            Create(tick2)
        )
        self.play(
            Write(typeq)
        )

        self.play(Write(typtheta))

        self.play(FadeOut(Group(tick1, tick2, typsim2, typeq, typtheta, typ1[:-1], typ4, hint, typbg)))

        ####################################################

        plane = NumberPlane((-5, 5), (-5, 5), faded_line_ratio=0, background_line_style={ 'alpha': 0.5 })

        vec1 = Vector(np.array([2, 1, 1.5]) * 0.7, color=RED_A)
        vec2 = Vector([0, 1.5], color=GREEN_A)
        vec3 = Vector(np.cross(vec1.points.vector, vec2.points.vector), color=BLUE_A, glow_alpha=0.5, glow_color=BLUE_A)

        typ1 = TypstMath('macron(v)', color=RED_A)
        typ2 = TypstMath('macron(k)', color=GREEN_A)
        typ3 = TypstMath('macron(v) times macron(k)', color=BLUE_A)
        colorize_vec(typ3)

        typ1.points.next_to(vec1.points.end, UR, buff=SMALL_BUFF)
        typ2.points.next_to(vec2.points.end, UR, buff=SMALL_BUFF)
        typ3.points.next_to(vec3.points.end, UR, buff=SMALL_BUFF)

        _BgRect = partial(SurroundingRect, **Rect.preset_shadow)

        typ1 = Group(_BgRect(typ1), typ1)
        typ2 = Group(_BgRect(typ2), typ2)
        typ3 = Group(_BgRect(typ3), typ3)

        def FaceToCamera(**kwargs):
            return AnimGroup(
                GroupUpdater(
                    typ1, 
                    lambda group, p: group.points.face_to_camera(about_point=vec1.points.end),
                    **kwargs
                ),
                GroupUpdater(
                    typ2, 
                    lambda group, p: group.points.face_to_camera(about_point=vec2.points.end),
                    **kwargs
                ),
                GroupUpdater(
                    typ3, 
                    lambda group, p: group.points.face_to_camera(about_point=vec3.points.end),
                    **kwargs
                ),
            )

        ####################################################

        self.play(
            FadeIn(plane),
            GrowArrow(vec1),
            GrowArrow(vec2),
            self.camera.anim.points.set(orientation=Quaternion(0.87, 0.36, 0.12, 0.29))
        )

        self.prepare(
            DataUpdater(
                self.camera,
                lambda data, p: data.points.rotate(p.elapsed * 0.1),
                duration=FOREVER
            ),
            FaceToCamera(duration=FOREVER)
        )
        self.play(
            GrowArrow(vec3)
        )

        self.forward()
