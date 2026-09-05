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


class Demo0(Timeline):
    def construct(self) -> None:
        Text('TODO').show()
        self.forward()


class Demo1(Timeline):
    def construct(self) -> None:
        circle = Circle(color=[1.0, 0.8, 0.4], glow_color=[1.0, 0.8, 0.4]).show()
        self.forward(0.5)
        self.play(circle.anim.set(glow_alpha=1, glow_size=0.5), duration=0.8)

        effect1 = FrameEffect(
            circle,
            fragment_shader='''
            #version 330 core

            #include "render/includes/blend_color.glsl"

            in vec2 v_texcoord; // 传入的纹理坐标
            out vec4 f_color;   // 输出的颜色

            uniform vec2 JA_FRAME_RADIUS;
            uniform float factor;

            #[JA_FINISH_UP_UNIFORMS]

            void apply(vec2 offset, float alpha) {
                vec2 texcoord = v_texcoord + offset;
                if (texcoord.x < 0.0 || texcoord.x > 1.0) return;
                if (texcoord.y < 0.0 || texcoord.y > 1.0) return;
                vec4 color = frame_texture(texcoord);
                color.a *= alpha;
                f_color = blend_color(color, f_color);
            }

            #define COUNT 2 

            void main()
            {
                f_color = frame_texture(v_texcoord);
                
                vec2 unit = vec2(1.2) / JA_FRAME_RADIUS * factor;
                vec2 unit_x = vec2(unit.x, 0);
                vec2 unit_y = vec2(0, unit.y);

                for (int i = 1; i <= COUNT; i++) {
                    float alpha = float(COUNT - i + 1) / COUNT;
                    alpha *= factor;

                    apply(unit_x * i, alpha);
                    apply(-unit_x * i, alpha);
                    apply(unit_y * i, alpha);
                    apply(-unit_y * i, alpha);
                }

                #[JA_FINISH_UP]
            }
            '''
        ).show()
        
        effect2 = SimpleFrameEffect(
            effect1,
            shader='''
            vec2 uv = v_texcoord;
            float setup = min(time, 0.4) / 0.4;

            float glitchStrength = sin(time * 2.0) * 0.005;
            vec2 offset = vec2(glitchStrength, 0.0);

            float xIndex = floor(uv.x * 8.0);

            float yScale = mix(
                7.0,
                12.0,
                fract(sin(xIndex * 127.1) * 43758.5453)
            );

            float yOffset = fract(sin(xIndex * 311.7) * 43758.5453);

            float xIndexFine = floor(uv.x * 129.0);

            float factor1 = mix(20.0, 60.0, fract(sin(xIndexFine * 157.3) * 43758.5453));
            float factor2 = mix(50.0, 120.0, fract(sin(xIndexFine * 269.7) * 43758.5453));

            float lineY1 = yOffset + 4.0 * time;
            float lineY2 = yOffset + 4.0 * time + 0.1 * sin(time * factor1);
            float lineY3 = yOffset + 4.0 * time + 0.2 * sin(time * factor2);

            vec3 lineNoise = vec3(
                step(0.5, fract(uv.y * yScale + lineY1)),
                step(0.5, fract(uv.y * yScale + lineY2)),
                step(0.5, fract(uv.y * yScale + lineY3))
            );

            float yGlitch1 = (fract(lineY1) - 0.5) * 0.02;
            float yGlitch2 = (fract(lineY2) - 0.5) * 0.02;
            float yGlitch3 = (fract(lineY3) - 0.5) * 0.02;

            vec4 c1 = frame_texture(uv + offset + vec2(0.0, yGlitch1));
            vec4 c2 = frame_texture(uv + vec2(0.0, yGlitch2));
            vec4 c3 = frame_texture(uv - offset + vec2(0.0, yGlitch3));
            vec3 rgb = vec3(c1.r * c1.a, c2.g * c2.a, c3.b * c3.a);
            if (c2.a == 0)
                discard;
            rgb /= c2.a;

            vec4 color = vec4(rgb, c2.a);

            color.rgb *= 0.4 + 0.6 * lineNoise;

            vec4 orig = frame_texture(uv);
            f_color = mix(orig, color, setup);
            ''',
            uniforms=['float time']
        )

        self.play(
            circle.anim.set(glow_alpha=0.5, glow_size=0.8),
            DataUpdater(
                effect1,
                lambda data, p: data.apply_uniforms(factor=p.alpha),
                rate_func=rush_from
            ),
            DataUpdater(
                effect2,
                lambda data, p: data.apply_uniforms(time=p.elapsed),
                duration=FOREVER
            ),
        )
        self.forward(4)


class _Demo2Sub(Timeline):
    def __init__(self, shape_type: str, background_color: JAnimColor):
        super().__init__()
        self.shape_type = shape_type
        self.background_color = background_color

    def construct(self):
        if self.shape_type == 'smooth':
            axes = ThreeDAxes((-8, 8), (-8, 8), (-8, 8)).apply_depth_test()
            self.prepare(FadeIn(axes, at=1))

        background = FrameRect(fill_alpha=1, fill_color=self.background_color, stroke_alpha=0, depth=100)
        background.fix_in_frame()
        self.prepare(FadeIn(background, at=1.5, duration=3))

        self.camera.save_state()

        for shape, duration, time_adv in zip(
            [Torus(2, 1), Cylinder(2, 4), Sphere(radius=3)],
            [2.6, 0.5, 3],
            [0, 2.6, 3.1],
        ):
            item = shape.into(self.shape_type).show()
            item.save_state()
            self.prepare(
                Do(lambda: item.set(color=BLUE_D), at=duration - 0.2),
                Do(item.load_state, at=duration - 0.1),
                Do(lambda: item.set(color=BLUE_D), at=duration - 0.05),
            )
            self.play(self.RotatingCamera(time_adv), duration=duration)
            self.camera.load_state()
            item.hide()
        
    def RotatingCamera(self, time_adv: float):
        return AnimGroup(
            DataUpdater(
                self.camera,
                lambda data, p: data.points.rotate(PI / 2 * (time_adv + p.elapsed), axis=RIGHT),
                rate_func=linear
            ),
            DataUpdater(
                self.camera,
                lambda data, p: data.points.rotate(PI / 2 * (time_adv + p.elapsed), axis=OUT),
                rate_func=linear
            ),
        )


class Demo2(Timeline):
    def construct(self):
        subs = [
            _Demo2Sub(type, color).build().to_item()
            for type, color in zip(
                ['checker', 'wire', 'smooth', 'dots'],
                ['#000022', '#000033', '#000033', '#000022']
            )
        ]
        subs[0].show()

        effects = [
            RectClip(sub, anchor=ORIGIN)
            for sub in subs
        ]
        effects[0].show().depth.set(-1)
        
        dirs = [UL, UR, DL, DR]

        self.forward()
        for sub, effect, dir in zip(subs, effects, dirs):
            self.show(sub, effect)
            self.prepare(
                effect.anim
                    .points.scale(0.5).to_border(dir, buff=0)
                    .r.transform.set(scale=0.5)
            )

        self.forward_to(subs[0].duration)


class Demo3(Timeline):
    def construct(self) -> None:
        shader = Shadertoy(
            """
            // Originates from https://www.shadertoy.com/view/lsX3W4

            // This shader computes the distance to the Mandelbrot Set for everypixel, and colorizes
            // it accordingly.
            // 
            // Z -> Z²+c, Z0 = 0. 
            // therefore Z' -> 2·Z·Z' + 1
            //
            // The Hubbard-Douady potential G(c) is G(c) = log Z/2^n
            // G'(c) = Z'/Z/2^n
            //
            // So the distance is |G(c)|/|G'(c)| = |Z|·log|Z|/|Z'|
            //
            // More info:
            // https://iquilezles.org/articles/distancefractals


            float distanceToMandelbrot( in vec2 c )
            {
                // iterate
                float di =  1.0;
                vec2 z  = vec2(0.0);
                float m2 = 0.0;
                vec2 dz = vec2(0.0);
                for( int i=0; i<300; i++ )
                {
                    if( m2>1024.0 ) { di=0.0; break; }

                    // Z' -> 2·Z·Z' + 1
                    dz = 2.0*vec2(z.x*dz.x-z.y*dz.y, z.x*dz.y + z.y*dz.x) + vec2(1.0,0.0);
                        
                    // Z -> Z² + c			
                    z = vec2( z.x*z.x - z.y*z.y, 2.0*z.x*z.y ) + c;
                        
                    m2 = dot(z,z);
                }

                // distance	
                // d(c) = |Z|·log|Z|/|Z'|
                float d = 0.5*sqrt(dot(z,z)/dot(dz,dz))*log(dot(z,z));
                //if( di>0.5 ) d=0.0;
                
                return d;
            }

            void mainImage( out vec4 fragColor, in vec2 fragCoord )
            {
                vec2 p = (2.0*fragCoord-iResolution.xy)/iResolution.y;

                // animation	
                float tz = -0.1 + 0.25 * iTime;
                float zoo = pow( 0.5, 13.0*tz );
                vec2 c = vec2(-0.05,.6805) + p*zoo;

                // distance to Mandelbrot
                float d = distanceToMandelbrot(c);
                
                // do some soft coloring based on distance
                d = clamp( pow(4.0*d/zoo,0.2), 0.0, 1.0 );
                //d =pow(d,.1);
                //d = 1.0-1.0/(1.0+1000.0*d);
                
                
                vec3 col = vec3(d);
                
                fragColor = vec4( col, 1.0 );
            }
            """
        )
        self.prepare(
            shader.create_updater(duration=FOREVER)
        )
        self.forward(8)


class Ball(Dot):
    speed = CustomData()

    def __init__(self, radius: float):
        super().__init__(radius=radius, color=BLUE)
        self.speed.set(ORIGIN)

class _Demo4(Timeline):
    def construct(self):
        # 有关配置
        left = -6
        right = 6
        bottom = -6
        top = 6

        radius = 0.25
        ball_count = 60

        # 容器边框
        # Polygon([left, top, 0], [left, bottom, 0], [right, bottom, 0], [right, top, 0], fill_alpha=0.2).show()
        # 内部的球
        balls = Ball(radius) * ball_count

        def sample_spd():
            return rng.choice([-1, 1]) * rng.uniform(2, 5)

        # 生成互不重叠的初始位置
        positions = []
        rng = np.random.default_rng(1234)
        for ball in balls:
            # 初始位置
            while True:
                pos = np.array([
                    rng.uniform(left + radius, right - radius),
                    rng.uniform(bottom + radius, top - radius),
                    0,
                ])
                if all(np.linalg.norm(pos - other) >= 2 * radius for other in positions):
                    break
            ball.points.move_to(pos)
            positions.append(pos)

            # 初始速度
            ball.speed.set(
                np.array([sample_spd(), sample_spd(), 0])
            )

        def updater(group: Group[Ball], p) -> None:
            dt = p.dt

            # 1. 根据速度移动
            for ball in group:
                ball.points.shift(ball.speed.get() * dt)

            # 2. 与容器边界碰撞
            for ball in group:
                pos = ball.points.box.center
                speed = ball.speed.get().copy()

                if pos[0] - radius < left:
                    ball.points.set_x(left + radius)
                    speed[0] = abs(speed[0])

                elif pos[0] + radius > right:
                    ball.points.set_x(right - radius)
                    speed[0] = -abs(speed[0])

                if pos[1] - radius < bottom:
                    ball.points.set_y(bottom + radius)
                    speed[1] = abs(speed[1])

                elif pos[1] + radius > top:
                    ball.points.set_y(top - radius)
                    speed[1] = -abs(speed[1])

                ball.speed.set(speed)

            # 3. 小球之间的完全弹性碰撞
            for i in range(len(group)):
                for j in range(i + 1, len(group)):
                    ball1 = group[i]
                    ball2 = group[j]

                    p1 = ball1.points.box.center
                    p2 = ball2.points.box.center

                    delta = p2 - p1
                    dist = np.linalg.norm(delta)

                    min_dist = 2 * radius

                    if dist >= min_dist:
                        continue

                    # 两个球存在重合时，给出碰撞方向
                    if dist < 1e-8:
                        normal = np.array([1.0, 0.0, 0.0])
                        dist = 0.0
                    else:
                        normal = delta / dist

                    v1 = ball1.speed.get()
                    v2 = ball2.speed.get()

                    # 相对速度
                    relative_velocity = v2 - v1
                    velocity_along_normal = np.dot(relative_velocity, normal)
                    # 只有相互靠近时才处理碰撞
                    if velocity_along_normal < 0:
                        # 相同质量的完全弹性碰撞
                        impulse = velocity_along_normal * normal
                        ball1.speed.set(v1 + impulse)
                        ball2.speed.set(v2 - impulse)

                    # 消除两个球之间的重叠
                    overlap = min_dist - dist
                    if overlap > 0:
                        correction = normal * (overlap / 2)
                        ball1.points.shift(-correction)
                        ball2.points.shift(correction)

        self.play(
            GroupStepUpdater(balls, updater, become_at_end=False),
            duration=6,
        )


class Demo4(Timeline):
    def construct(self) -> None:
        tl = _Demo4().build().to_item().show()

        effect = SimpleFrameEffect(
            tl,
            shader="""
            f_color = frame_texture(v_texcoord);
            
            vec2 frame_pos = (v_texcoord - 0.5) * 2 * JA_FRAME_RADIUS;
            float factor = (5.0 - length(frame_pos)) / 5.0;

            f_color.a *= factor;
            """,
            uniforms=[
                'vec2 JA_FRAME_RADIUS',
            ]
        ).show()

        self.forward(tl.duration)


class Demo5(Timeline):
    def construct(self) -> None:
        center = np.array([0.150, 0.196, 25.676])

        curve = VItem([3.051522, 1.582542, 15.62388], glow_alpha=0.5)
        curve.set(color=[BLUE_E, BLUE_A], stroke_radius=0.1)

        sigma = 10
        rho = 28
        beta = 8 / 3

        def updater(data: VItem, p: StepUpdaterParams):
            point = data.points.get()[-1].copy()
            for _ in range(20):
                x, y, z = point
                dp = np.array([
                    sigma * (y - x),
                    x * (rho - z) - y,
                    x * y - beta * z
                ])
                point += dp * 0.001
            data.points.add_as_corners([point]).make_approximately_smooth()

        self.camera.points.scale(10).rotate(-20 * DEGREES, axis=RIGHT)
        self.camera.points.move_to(center)
        self.play(
            StepUpdater(curve, updater, step=0.008, become_at_end=False, duration=6),
            Rotating(
                self.camera,
                -TAU * 2,
                axis=UP,
                duration=6
            )
        )


class Demo6(Timeline):
    def construct(self) -> None:
        typ = TypstText(
            """
            #import "@preview/physica:0.9.8": *
            #let evd = evaluated

            #let di = $1 - y_(n+1)$
            #let uv = $sum_(i=1)^n x_i^2$

            $
                g^(-1) (x) = ((2x_1) / (uv + 1), (2x_2) / (uv + 1), dots.c, (2x_n) / (uv + 1), (uv - 1) / (uv + 1))

                wide

                evd(pdv(,x^i))_p
                =
                (dif phi_p)^(-1)
                (evd(pdv(,x^i))_(phi(p)))
                =
                dif (phi^(-1))_(phi(p))
                (evd(pdv(,x^i))_(phi(p)))

                wide

                evd(pdv(,x^i))_p f 
                = 
                evd(pdv(,x^i))_(phi(p)) (f compose phi^(-1))
                =
                pdv(hat(f),x^i) (hat(p))

                wide 

                gamma' (t_0)
                =
                dif gamma (evd(dv(,t))_(t_0)) 
                in
                T_(gamma(t_0)) M
            $
            """,
            scale=3.4
        ).show()
        typ_gray = typ.copy() * 3
        typ_gray.set(color=GREY_D, depth=1)
        typ_gray.points.arrange(buff=MED_LARGE_BUFF)
        typ_gray.points.shift(RIGHT * 12 + UP * 1.3)
        typ.points.shift(DOWN * 0.4)

        self.camera.points.move_to(typ.points.box.left + RIGHT * 8, coor_mask=(1, 0, 0))
        self.play(
            self.camera.anim(rate_func=linear)
                .points.move_to(typ.points.box.right + LEFT * 8, coor_mask=(1, 0, 0)),
            typ_gray.anim.points.shift(LEFT * 24),
            duration=5
        )


@dataclass
class Rod:
    length: float
    start_angle: float
    rot_speed: float

    children: list[Rod]


class Demo7(Timeline):
    def construct(self) -> None:
        rods = [
            Rod(0.3, 0, 3, []),
            Rod(0.5, 0, 3.5, []),
            Rod(
                1.5, 0, 5,
                [
                    Rod(0.2, 0, 30, []),
                    Rod(0.2, PI / 2, 30, [])
                ]
            ),
            Rod(1.7, PI / 2, 5, []),
            Rod(1.9, PI / 2, 5, []),
            Rod(
                2.1, 0, 3,
                [
                    Rod(0.2, i * PI / 9, 18, [])
                    for i in range(10)
                ]
            ),
            Rod(2.5, PI / 2, 3, []),
            Rod(2.8, PI / 3, 2.5, [Rod(0.3, 0, 15, [])]),
            Rod(
                3.0, PI / 3, 2.5,
                [
                    Rod(0.3, 0, 15, []),
                    Rod(0.3, PI, 15, []),
                ]
            ),
            Rod(3.5, 0, 2, []),
            Rod(
                3.55, 0, 2,
                [
                    Rod(0.05, 0, 40, []),
                    Rod(0.05, PI, 40, []),
                ]
            ),
            Rod(3.6, 0, 2, []),
            Rod(3.7, 0, 2, []),
        ]

        def parse_rod(rod: Rod, parent_line: Line | None):
            line = Line(
                ORIGIN, RIGHT * rod.length, 
                color=GREY, 
                stroke_radius=0.006,
                depth=1
            ).show()
            self.prepare(
                DataUpdater(
                    line,
                    lambda data, p: data.points.rotate(
                        rod.start_angle + rod.rot_speed * p.elapsed,
                        about_point=ORIGIN
                    ),
                    duration=FOREVER
                )
            )
            if parent_line is not None:
                self.prepare(
                    DataUpdater(
                        line,
                        lambda data, p: data.points.shift(
                            parent_line.current().points.get_end()
                        ),
                        duration=FOREVER
                    )
                )
            if rod.children:
                for child in rod.children:
                    parse_rod(child, line)
            else:
                tracer = VItem(
                    color=BLUE_A, 
                    alpha=[0, 1], 
                    stroke_radius=0.006,
                    glow_alpha=0.1,
                    glow_color=BLUE_D,
                ).show()
                
                def tracer_updater(data: VItem, p: StepUpdaterParams) -> None:
                    new_pos = line.current().points.get_end()
                    data.points.add_as_corners([new_pos])
                    points = data.points.get()
                    if len(points) >= 7 and cross2d(points[0], points[-1]) > 0 and cross2d(points[0], points[-5]) < 0:
                        data.points.set(points[2:])

                self.prepare(
                    StepUpdater(tracer, tracer_updater, duration=FOREVER, skip_null_items=False),
                    DataUpdater(tracer, lambda data, p: data.points.make_smooth(approx=True), duration=FOREVER, skip_null_items=False),
                )

        for rod in rods:
            parse_rod(rod, None)
        self.forward(6)


class Demo8(Timeline):
    def construct(self) -> None:
        radius = 20
    
        # 给无穷远处打补丁的填充色
        outer = boolean_ops.Difference(
            Square(1000),
            Square(2 * radius - 5),
            fill_alpha=1,
            fill_color=BLUE_D,
            stroke_alpha=0,
        )
        outer.points.insert_n_curves(150)
    
        # 复平面
        plane = NumberPlane(
            (-radius, radius, 0.8), 
            (-radius, radius, 0.8), 
            faded_line_ratio=0
        ).show()
        plane.points.prepare_for_nonlinear_transform(150)
    
        # =====
        # 让水平线/竖直线的采样精度，两端稀疏，中间密集，因为外侧的坐标会被变换到一起，而内侧的坐标会被极端向外拉伸，需要更高的精度来模拟
        # 当然，直接增加 prepare_for_nonlinear_transform 的精度也是可以的，但是会更慢
        def coord_transform(x: float, a: float = radius, k: float = 4.0) -> float:
            return a * math.atanh(math.tanh(k) * x / a) / k
    
        bg_lines = plane.background_lines
        x_lines = bg_lines[:len(bg_lines) // 2]
        y_lines = bg_lines[len(bg_lines) // 2:]
        Group(x_lines, plane.x_axis).points.apply_complex_fn(lambda z: coord_transform(z.real) + z.imag * 1j)
        Group(y_lines, plane.y_axis).points.apply_complex_fn(lambda z: z.real + coord_transform(z.imag) * 1j)
        # =====
    
        # z -> 1/z 的过渡函数，采用 复平面 -> 变换到单位球 -> 旋转单位球 -> 变换回复平面的策略
        def complex_fn(z: complex, alpha: float) -> complex:
            x = z.real
            y = z.imag
            r2 = x * x + y * y
    
            # 复平面 -> 单位球
            X = 2 * x / (1 + r2)
            Y = -2 * y / (1 + r2)
            Z = (r2 - 1) / (1 + r2)
    
            # 绕 X 轴旋转 alpha * pi
            theta = alpha * math.pi
            cos_theta = math.cos(theta)
            sin_theta = math.sin(theta)
    
            X_new = X
            Y_new = cos_theta * Y - sin_theta * Z
            Z_new = sin_theta * Y + cos_theta * Z
    
            # 映射到的无穷远点直接放到屏幕左边
            # 因为只有横向连线才会出现无穷远点
            # 放在左边是合适的，刚好能和线重合
            if 1 - Z_new == 0:
                return -50  
    
            # 单位球 -> 复平面
            return complex(
                X_new / (1 - Z_new),
                -Y_new / (1 - Z_new),
            )
    
        self.forward(0.5)
        self.play(
            GroupUpdater(
                Group(plane, outer),
                lambda group, p: group.points.apply_complex_fn(
                    lambda z: complex_fn(z, p.alpha)
                ),
                show_at_begin=False,  # 因为我们不想让 outer 一开始就出现，会露馅
                duration=4,
            ),
            Do(outer.show, at=1),
        )
        self.forward(0.5)


class DemosDemonstration(Demo1):
    def construct(self):
        demos_cls = [Demo1, Demo2, Demo3, Demo4, Demo5, Demo6, Demo7, Demo8]
        scales = [1, 0.7, 1, 1, 1, 1, 1, 1]

        for demo_cls, scale in zip(demos_cls, scales):
            if demo_cls is Demo3:
                txt = Text('Originates from https://www.shadertoy.com/view/lsX3W4', font_size=16, depth=-1)
                txt.points.to_border(DL)
                txt.set(stroke_alpha=1, stroke_color=BLACK)
                self.prepare(FadeIn(txt), FadeOut(txt, at=4))

            demo = demo_cls().build().to_item(keep_last_frame=True)
            clip = RectClip(demo, anchor=ORIGIN, border=True, scale=scale)
            clip.points.set_size(3, 3)
            self.prepare(
                # 动画分为两大并行的部分
                Aligned(
                    # 1. 第一部分
                    # 持续旋转(DataUpdater) 以及 显示/隐藏(Do)
                    Succession(
                        Do(Group(demo, clip).show),
                        DataUpdater(
                            clip,
                            lambda data, p: data.points.rotate(80 * DEGREES * p.elapsed),
                        ),
                        Do(Group(demo, clip).hide),
                    ),
                    # 2. 第二部分
                    # 向左进入(update) 以及 缩放(DataUpdater) 以及 向左离开(update)
                    # 使用 offset-0.5 使得各个动画之间有一定重叠，减少生硬感
                    Succession(
                        clip.update(become_at_end=False, rate_func=lambda t: rush_into(1 - t))
                            .points.shift(RIGHT * 9.5),
                        DataUpdater(
                            clip,
                            lambda data, p: data.points.scale(1 + 2 * p.alpha),
                            become_at_end=False,
                            rate_func=there_and_back_with_pause,
                            duration=3,
                        ),
                        clip.update(rate_func=rush_into)
                            .points.shift(LEFT * 9.5),
                        offset=-0.5
                    ),
                ),
                duration=4.7,
            )
            self.forward(4.35)

        self.forward(0.5)


class JAnimDemosDemonstration(Template):
    def construct(self) -> None:
        txt = Text('以下画面均直接使用 JAnim 渲染生成', color=GREY_B)

        self.forward(0.5)
        self.play(FadeIn(txt, duration=2))
        self.forward()
        self.play(FadeOut(txt))

        icon = Iconify("boxicons:headphone", height=2, color=GREY_B)

        self.play(FadeIn(icon))
        self.forward()
        self.play(FadeOut(icon))

        audio_file = '/home/jkjkil/Documents/Z.A.T.O. SOUNDTRACK/24. Tightrope.mp3'
        audio_duration = 43.4
        fade_out = 2
        audio_t = self.play_audio(
            Audio(audio_file, end=audio_duration).fade_out(fade_out), 
            delay=0.3
        )
    
        demos = DemosDemonstration().build().to_item().show()
        self.forward(demos.duration)
        demos.hide()
        # self.forward(35.3)

        txt1 = Text('JAnim', font_size=80)
        txt2 = Text(
            '程序化动画引擎\n<fs 0.7>Programmatic Animation Engine</fs>',
            format='rich',
            font_size=60,
            fill_alpha=0.3,
            depth=1
        )
        txt2.points.arrange(DOWN)

        txt1.show()
        self.forward(0.5)
        self.play(
            DrawBorderThenFill(txt2, duration=1.9)
        )
        self.forward(2)
        self.hide(txt1, txt2)

        txt = Text(
            """
            更多内容请阅读文档：janim.rtfd.io

            QQ 群：970174336 欢迎提问
            """
        ).show()
        self.forward_to(audio_t.end + 0.2)
