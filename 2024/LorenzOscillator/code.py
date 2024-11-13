from janim.imports import *


class SubSceneTemplate(Timeline):
    CONFIG = Config(
        output_dir=':/videos',
        pixel_width=Config.get.pixel_width // 2,
        frame_width=Config.get.frame_width / 2
    )


class LorenzOscillatorCurve(SubSceneTemplate):
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
            StepUpdater(curve, updater, become_at_end=False, duration=43),
            Rotating(
                self.camera,
                -TAU * 2,
                axis=UP,
                duration=43
            )
        )


class LorenzOscillatorDotCloud(SubSceneTemplate):
    def construct(self) -> None:
        center = np.array([0.150, 0.196, 25.676])
        radius = 12
        count = 30

        sigma = 10
        rho = 28
        beta = 8 / 3

        dots = DotCloud(
            *[
                center + [x, y, z]
                for x in np.linspace(-radius, radius, count)
                for y in np.linspace(-radius, radius, count)
                for z in np.linspace(-radius, radius, count)
            ],
            color=[BLUE, GREEN]
        ).show()

        def updater(data: DotCloud, p: StepUpdaterParams):
            points = data.points.get()
            x = points[:, [0]]
            y = points[:, [1]]
            z = points[:, [2]]
            dpoints = np.hstack([
                sigma * (y - x),
                x * (rho - z) - y,
                x * y - beta * z
            ])
            data.points.set(points + dpoints * 0.005)

        self.camera.points.scale(10).rotate(-20 * DEGREES, axis=RIGHT)
        self.camera.points.move_to(center)
        self.play(
            StepUpdater(dots, updater, become_at_end=False, duration=41, at=2),
            Rotating(
                self.camera,
                -TAU * 2,
                axis=UP,
                duration=43
            )
        )


class LorenzOscillator(Timeline):
    CONFIG = Config(
        output_dir=':/videos'
    )

    def construct(self) -> None:
        video1 = Video('videos/LorenzOscillatorCurve.mp4')
        video2 = Video('videos/LorenzOscillatorDotCloud.mp4')
        video1.start()
        video2.start()
        group = Group(video1, video2).show()
        group.points.arrange(buff=0)

        txt1 = Text('LorenzOscillatorCurve').show()
        txt1.points.move_to(video1).to_border(UP)

        txt2 = Text('LorenzOscillatorDotCloud').show()
        txt2.points.move_to(video2).to_border(UP)

        g = Group(group, txt1, txt2)
        g.points.shift(DOWN * 0.4)

        self.forward(43)
