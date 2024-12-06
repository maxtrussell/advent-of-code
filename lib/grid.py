from typing import Optional


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Point") -> "Point":
        return Point(self.x - other.x, self.y - other.y)

    def __eq__(self, other: "Point") -> bool:
        return self.x == other.x and self.y == other.y

    def __repr__(self) -> str:
        return f"Point<{self.x}, {self.y}>"


class Grid:
    def __init__(self, lines: list[str], diagonal=False):
        self.diagonal = diagonal
        self.grid: list[list[str]] = []
        for line in lines:
            self.grid.append(list(line))

    def get_neighbors(self, p: Point) -> list[Point]:
        adjacents = [Point(x, y) for x, y in [(1, 0), (0, 1), (-1, 0), (0, -1)]]
        diagonals = [Point(x, y) for x, y in [(1, 1), (1, -1), (-1, 1), (-1, -1)]]

        neighbors = [p + n for n in adjacents if self.in_bounds(p + n)]
        if self.diagonal:
            neighbors += [p + n for n in diagonals if self.in_bounds(p + n)]
        return neighbors

    def in_bounds(self, p: Point) -> bool:
        return 0 <= p.y < len(self.grid) and 0 <= p.x < len(self.grid[p.y])

    def get(self, p: Point) -> Optional[str]:
        if self.in_bounds(p):
            return self[p]
        return None

    def __getitem__(self, p: Point) -> str:
        return self.grid[p.y][p.x]

    def __setitem__(self, p: Point, to: str) -> None:
        self.grid[p.y][p.x] = to

    def __iter__(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                yield Point(x, y)

    def __repr__(self) -> str:
        return "\n".join(["".join(row) for row in self.grid])
