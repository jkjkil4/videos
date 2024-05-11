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
    background_color = '#222222'

    CONFIG = Config(
        font=['Consolas', 'Noto Sans S Chinese Medium']
    )

    def construct(self) -> None:
        txt1 = Text(self.str1, color=self.str1_color, font_size=28, format=Text.Format.RichText)
        txt2 = Text(self.str2, color=self.str2_color, font_size=32, format=Text.Format.RichText)
        txt = Group(txt1, txt2)
        txt.points.arrange(DOWN)

        self.forward(0.1)
        self.play(DrawBorderThenFill(txt))
        self.forward()
        self.play(FadeOut(txt))


class SubtitleTemplate(Template):
    name = 'Subtitle'

    def construct(self) -> None:
        txt = Text(self.name, font_size=32, format=Text.Format.RichText)

        txt.show()
        self.forward(2)
