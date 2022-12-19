#include <algorithm>
#include <cstdint>
#include <functional>
#include <optional>
#include <regex>
#include <string>
#include <unordered_set>
#include <vector>

#include "../aoc.cpp"

using namespace std;

struct Point {
  int x = 0, y = 0;
};

template <> struct std::hash<Point> {
  size_t operator()(const Point &p) const noexcept { return p.x * 1000 + p.y; }
};

using Grid = unordered_set<Point>;

ostream &operator<<(ostream &out, const Point &p) {
  return out << "Point{x: " << p.x << ", y: " << p.y << "}";
}

Point operator+(const Point &a, const Point &b) {
  return Point{a.x + b.x, a.y + b.y};
}

Point operator-(const Point &a, const Point &b) {
  return Point{a.x - b.x, a.y - b.y};
}

bool operator==(const Point &a, const Point &b) {
  return a.x == b.x && a.y == b.y;
}

bool operator!=(const Point &a, const Point &b) { return !(a == b); }

bool le(const Point &a, const Point &b, const Point &delta) {
  return delta.x != 0 ? a.x <= b.x : a.y <= b.y;
}

void add_rock(Grid &grid, const string &line) {
  // Parse all points using regex
  vector<Point> points;
  const static regex pattern(R"((\d+),(\d+))");
  sregex_iterator it(line.begin(), line.end(), pattern);
  for (; it != sregex_iterator(); ++it) {
    Point p{stoi((*it)[1]), stoi((*it)[2])};
    points.push_back(p);
  }

  for (auto i = 0; i < points.size() - 1; ++i) {
    vector<Point> line{points[i], points[i + 1]};
    Point diff = points[i + 1] - points[i];
    Point delta = diff.x != 0 ? Point{1, 0} : Point{0, 1};
    sort(line.begin(), line.end(),
         [delta](Point a, Point b) { return le(a, b, delta); });
    for (Point p = line[0]; le(p, line[1], delta); p = p + delta) {
      grid.insert(p);
    }
  }
}

Point get_next_pos(const Grid &grid, Point curr, int floor) {
  static vector<Point> deltas{{0, 1}, {-1, 1}, {1, 1}};
  for (Point delta : deltas) {
    if ((curr + delta).y >= floor)
      continue;
    if (grid.count(curr + delta) == 0)
      return curr + delta;
  }
  return curr;
}

bool simulate(Grid &grid, int bound, int floor) {
  Point curr{500, 0};
  Point next = get_next_pos(grid, curr, floor);
  while (next != curr) {
    curr = next;
    next = get_next_pos(grid, curr, floor);
    if (next.y >= bound)
      return false;
  }
  grid.insert(curr);
  return true;
}

int main(int argc, char *argv[]) {
  Grid grid;
  for (const auto &line : aoc::input_lines(argc, argv))
    add_rock(grid, line);

  Point bound = *min_element(grid.begin(), grid.end(),
                             [](Point a, Point b) { return a.y > b.y; });
  int floor = bound.y + 2;
  Grid grid1 = grid;
  int part1 = 0;
  while (simulate(grid1, bound.y, floor)) {
    ++part1;
  }

  int part2 = 0;
  while (simulate(grid, floor, floor)) {
    ++part2;
    if (grid.count(Point{500, 0}) == 1)
      break;
  }
  aoc::output(part1);
  aoc::output(part2);
}
