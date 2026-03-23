from bisect import bisect_left, bisect_right


class CutRangeCollection:
    def __init__(self) -> None:
        self._boundaries: list[float] = []

    def clear(self) -> None:
        self._boundaries = []

    def has_ranges(self) -> bool:
        return bool(self._boundaries)

    def get_boundaries(self) -> list[float]:
        return [*self._boundaries]

    def modify(self, start: float, end: float, is_cut_selection: bool) -> bool:
        start, end = sorted((start, end))
        if start == end:
            return False

        left = bisect_left(self._boundaries, start)
        right = bisect_right(self._boundaries, end)

        orig_left_is_cut = left % 2 == 1
        orig_right_is_cut = right % 2 == 1

        if orig_left_is_cut and orig_right_is_cut:
            if is_cut_selection:
                self._boundaries = [*self._boundaries[:left], *self._boundaries[right:]]
            else:
                self._boundaries = [*self._boundaries[:left], start, end, *self._boundaries[right:]]
        elif not orig_left_is_cut and orig_right_is_cut:
            if is_cut_selection:
                self._boundaries = [*self._boundaries[:left], start, *self._boundaries[right:]]
            else:
                self._boundaries = [*self._boundaries[:left], end, *self._boundaries[right:]]
        elif orig_left_is_cut and not orig_right_is_cut:
            if is_cut_selection:
                self._boundaries = [*self._boundaries[:left], end, *self._boundaries[right:]]
            else:
                self._boundaries = [*self._boundaries[:left], start, *self._boundaries[right:]]
        else:
            if is_cut_selection:
                self._boundaries = [*self._boundaries[:left], start, end, *self._boundaries[right:]]
            else:
                self._boundaries = [*self._boundaries[:left], *self._boundaries[right:]]

        return True

    def get_ranges(self) -> list[tuple[float, float]]:
        ranges: list[tuple[float, float]] = []
        for i in range(len(self._boundaries) // 2):
            ranges.append((self._boundaries[i * 2], self._boundaries[i * 2 + 1]))
        return ranges
