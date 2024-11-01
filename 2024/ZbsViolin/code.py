# flake8: noqa
import sys

sys.path.append('.')

from janim.imports import *

from utils.template import *


class ZbsViolin(Template):
    def construct(self) -> None:
        t = self.play_audio(Audio('video.mp4'))
        video = Video('video.mp4', height=Config.get.frame_height)
        video.show().start()
        video.points.shift(UP * 2)

        imgs = [
            ImageItem(f'{i}.png', width=Config.get.frame_width)
                .points.to_border(DOWN, 0)
                .r
            for i in range(1, 7)
        ]
        imgs[0].show()
        times_list = [
            [1.6, 3.5],
            [3.5, 5.1, 6.9, 8.5, 10.2],
            [10.2, 11.9, 13.5, 15.0, 17.0, 18.4],
            [18.4, 20, 21.1, 22.6, 24.6, 25.7, 26.6],
            [26.6, 28.1, 29.6, 31.1, 32.4, 33.2, 35.2],
            [35.2, 37.8, 40.1, 41]
        ]
        corners_list = [
            [2.72, 6.88],
            [-6.89, -2.9, 0.32, 3.56, 6.82],
            [-6.75, -3.08, -0.26, 2.4, 4.93, 6.74],
            [-6.78, -3.95, -2.14, 1.24, 4.42, 5.44, 6.78],
            [-6.78, -3.63, -1.67, 0.23, 2.12, 4.13, 6.72],
            [-6.88, -1.02, 0.3, 2.33]
        ]
        for img, times, corners in zip(imgs, times_list, corners_list):
            self.schedule(times[0], img.show)
            self.schedule(times[-1], img.hide)
            y1 = img.points.box.get_y(UP)
            y2 = img.points.box.get_y(DOWN)
            for (t1, c1), (t2, c2) in it.pairwise(zip(times, corners)):
                rect = Rect([c1, y1, 0], [c2, y2, 0],
                            stroke_alpha=0,
                            fill_alpha=0.2,
                            color=YELLOW)
                self.schedule(t1, rect.show)
                self.schedule(t2, rect.hide)

        self.forward_to(round(t.end, 1))
