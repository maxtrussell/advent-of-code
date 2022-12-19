#include <algorithm>
#include <cctype>
#include <cstdint>
#include <cstdlib>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

#include "../aoc.cpp"

using namespace std;

struct Point {
  int x = 0, y = 0;
};

template <> struct std::hash<Point> {
  size_t operator()(const Point &p) const noexcept {
    return hash<int>()(p.x) ^ hash<int>()(p.y);
  }
};

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

int distance(Point a, Point b) {
  Point delta = a - b;
  return abs(delta.x) + abs(delta.y);
}

int read_int(const string &line, string::const_iterator &it) {
  while (!isdigit(*it) && *it != '-') {
    ++it;
  }
  string buf;
  while (isdigit(*it) || *it == '-') {
    buf += *it;
    ++it;
  }
  return stoi(buf);
}

void add_points_on_row(Point sensor, int radius, int row,
                       unordered_set<Point> &blocked) {
  int offset = abs(sensor.y - row);
  int start = sensor.x - radius + offset;
  int end = sensor.x + radius - offset;
  for (auto i = start; i < end; ++i)
    blocked.insert(Point{i, row});
}

pair<int, int> y_intercepts(Point p) { return {p.y + p.x, p.y - p.x}; }

int main(int argc, char *argv[]) {
  vector<pair<Point, int>> sensors;
  for (const auto &line : aoc::input_lines(argc, argv)) {
    auto it = line.begin();
    Point sensor{read_int(line, it), read_int(line, it)};
    Point beacon{read_int(line, it), read_int(line, it)};
    sensors.push_back(make_pair(sensor, distance(sensor, beacon)));
  }

  constexpr int row = 2'000'000;
  // constexpr int row = 10;
  constexpr int upper_bound = 4'000'000;
  // constexpr int upper_bound = 20;

  // Part 1
  // It would probably be a lot faster to keep a ordered list of ranges.
  // But that's more work.
  unordered_set<Point> blocked;
  for (auto [sensor, dist] : sensors)
    add_points_on_row(sensor, dist, row, blocked);
  aoc::output(blocked.size());

  // Part 2
  unordered_set<int> vertex_set;
  for (auto [p, r] : sensors) {
    Point left{p.x - r - 1, p.y};
    auto [l1, l2] = y_intercepts(left);
    vertex_set.insert(l1);
    vertex_set.insert(l2);

    Point right{p.x + r + 1, p.y};
    auto [r1, r2] = y_intercepts(left);
    vertex_set.insert(r1);
    vertex_set.insert(r2);
  }
  vector<int> vertices(vertex_set.begin(), vertex_set.end());
  unordered_set<Point> candidates;
  for (auto i = 0; i < vertices.size(); ++i) {
    for (auto j = i + 1; j < vertices.size(); ++j) {
      int y = (vertices[i] + vertices[j]) / 2;
      int x = abs(vertices[i] - y);
      if (y >= 0 && y <= upper_bound && x <= upper_bound)
        candidates.insert(Point{x, y});
    }
  }

  Point part2;
  for (auto p : candidates) {
    if (all_of(sensors.begin(), sensors.end(), [p](auto s) {
          auto [sensor, r] = s;
          return distance(p, sensor) > r;
        })) {
      part2 = p;
      break;
    }
  }
  aoc::output(part2.x * int64_t(4'000'000) + part2.y);
}
