import lib.aoc as aoc
from lib.grid import Point

from copy import deepcopy
from itertools import combinations


class Line:
    def __init__(self, a: Point, b: Point):
        if a.x == b.x:
            self.vertical = True
            self.pos = a.x
            self.start, self.end = (p.y for p in sorted([a, b], key=lambda p: p.y))
        elif a.y == b.y:
            self.vertical = False  # horizontal
            self.pos = a.y
            self.start, self.end = (p.x for p in sorted([a, b], key=lambda p: p.x))

    def contains(self, l: "Line", d: int) -> bool:
        if self.vertical != l.vertical:
            return False
        if (d > 0 and l.pos > self.pos) or (d < 0 and l.pos < self.pos):
            return False
        return l.start >= self.start and l.end <= self.end

    def intersects(self, l: "Line", d: int) -> bool:
        if self.vertical != l.vertical:
            return False
        if (d > 0 and l.pos > self.pos) or (d < 0 and l.pos < self.pos):
            return False
        midpoint = (l.end + l.start) / 2
        return self.start <= midpoint <= self.end

    def supercedes(self, l: "Line") -> bool:
        if self.vertical != l.vertical:
            return False
        if self.pos != l.pos:
            return False
        midpoint = (l.end + l.start) / 2
        return self.start <= midpoint <= self.end

    def __repr__(self) -> str:
        return f"Line<{self.vertical=}, {self.pos=}, {self.start=}, {self.end=}>"


def merge_lines(lines: list[Line]) -> list[Line]:
    did_merge = True
    while did_merge:
        did_merge = False
        for i in range(len(lines) - 1):
            # Do they overlap?
            a, b = lines[i], lines[i + 1]
            if b.start > a.end:
                continue
            # They overlap!
            a.end = max(a.end, b.end)
            del lines[i + 1]
            did_merge = True
            break

    return lines


def rect_area(a, b):
    width = abs(a.x - b.x) + 1
    height = abs(a.y - b.y) + 1
    return width * height


def only_red_green(a, b):
    corners = [a, Point(a.x, b.y), b, Point(b.x, a.y)]
    for a, b in zip(corners, corners[1:] + [corners[0]]):
        curr = Line(a, b)
        lines = v_lines if curr.vertical else h_lines

        # Collect all segments above and below curr
        above, below = [], []
        for l in lines:
            if l.pos >= curr.pos:
                above.append(l)
            if l.pos <= curr.pos:
                below.append(l)

        # Pre merge, count number of intersections.
        if not any(l.supercedes(curr) for l in lines):
            intersects_above = sum(l.intersects(curr, 1) for l in above)
            if intersects_above % 2 != 1:
                return False

            intersects_below = sum(l.intersects(curr, -1) for l in below)
            if intersects_below % 2 != 1:
                return False

        merged_above = merge_lines(deepcopy(above))
        merged_below = merge_lines(deepcopy(below))
        if not any(l.contains(curr, 1) for l in merged_above):
            return False
        if not any(l.contains(curr, -1) for l in merged_below):
            return False
    return True


points = []
for line in aoc.input_lines():
    x, y = [int(n) for n in line.split(",")]
    points.append(Point(x, y))

h_lines, v_lines = [], []
for a, b in zip(points, points[1:] + [points[0]]):
    l = Line(a, b)
    if l.vertical:
        v_lines.append(l)
    else:
        h_lines.append(l)

h_lines.sort(key=lambda l: l.start)
v_lines.sort(key=lambda l: l.start)

rects = list(
    sorted(combinations(points, 2), key=lambda p: rect_area(p[0], p[1]), reverse=True)
)

aoc.output(rect_area(rects[0][0], rects[0][1]))
a, b = next((a, b) for a, b in rects if only_red_green(a, b))
aoc.output(rect_area(a, b))
