from janim.imports import *


class Template(Timeline):
    CONFIG = Config(
        font=['Consolas', 'Noto Sans S Chinese Medium'],
        asset_dir=[
            'assets',
            'audios'
        ],
        output_dir=':/kdenlive/manim_src'
    )


class TitleTemplate(Template):
    str1 = 'Title'
    str2 = 'Topic'
    str1_color = GREY_A
    str2_color = GREY_B
    str1_font_size = 28
    str2_font_size = 32
    background_color = '#222222'

    CONFIG = Config(
        font=['Consolas', 'Noto Sans S Chinese Medium']
    )

    def construct(self) -> None:
        txt1 = Text(self.str1,
                    color=self.str1_color,
                    font_size=self.str1_font_size,
                    format=Text.Format.RichText)
        txt2 = Text(self.str2,
                    color=self.str2_color,
                    font_size=self.str2_font_size,
                    format=Text.Format.RichText)
        txt = Group(txt1, txt2)
        txt.points.arrange(DOWN)

        self.forward(0.1)
        self.play(DrawBorderThenFill(txt))
        self.forward()
        self.play(FadeOut(txt))


class SubtitleTemplate(Template):
    name = 'Subtitle'
    stay_duration = 2

    def construct(self) -> None:
        self.txt = Text(self.name, font_size=32, format=Text.Format.RichText)

        self.txt.show()
        self.forward(self.stay_duration)


class SubtitleTemplate2(SubtitleTemplate):
    stay_duration = 1
    title_kwargs = {}

    def construct(self) -> None:
        super().construct()

        self.title = Title(self.name, **self.title_kwargs)
        self.play(
            Transform(self.txt, self.title.txt),
            FadeIn(self.title.underline, at=0.5, duration=0.5)
        )
