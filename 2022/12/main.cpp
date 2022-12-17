#include <algorithm>
#include <deque>
#include <iostream>
#include <limits>
#include <ostream>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>

#include "../aoc.cpp"

using namespace std;
using Grid = vector<vector<char>>;

struct Point {
  int x = 0, y = 0;

  char get_height(const Grid &grid) {
    char height = grid[y][x];
    if (height == 'S')
      height = 'a';
    if (height == 'E')
      height = 'z';
    return height;
  }
};

ostream &operator<<(ostream &out, const Point &p) {
  return out << "Point{x: " << p.x << ", y: " << p.y << "}";
}

Point operator+(const Point &a, const Point &b) {
  return Point{a.x + b.x, a.y + b.y};
}

bool operator==(const Point &a, const Point &b) {
  return a.x == b.x && a.y == b.y;
}

bool operator!=(const Point &a, const Point &b) { return !(a == b); }

template <> struct std::hash<Point> {
  size_t operator()(const Point &p) const noexcept {
    size_t hash_x = hash<int>{}(p.x);
    size_t hash_y = hash<int>{}(p.y);
    return hash_x ^ (hash_y << 1);
  }
};

bool can_travel(const Grid &grid, Point src, Point dst) {
  return src.get_height(grid) - dst.get_height(grid) <= 1;
}

bool in_bounds(const Grid &grid, Point p) {
  return p.x >= 0 && p.y >= 0 && p.x < grid[0].size() && p.y < grid.size();
}

vector<Point> get_neighbors(const Grid &grid, Point pos,
                            const unordered_set<Point> &seen) {
  vector<Point> neighbors;
  vector<Point> deltas = {{0, 1}, {1, 0}, {0, -1}, {-1, 0}};
  for (Point delta : deltas) {
    Point n = pos + delta;
    if (!in_bounds(grid, n))
      continue;
    bool travelable = can_travel(grid, pos, n);
    bool already_seen = seen.find(n) != seen.end();
    if (travelable && !already_seen)
      neighbors.push_back(n);
  }
  return neighbors;
}

void bfs(const Grid &grid, Point start, vector<vector<int>> &step_grid) {
  deque<pair<Point, int>> queue{{start, 0}};
  unordered_set<Point> seen({start});
  for (auto p = queue.front(); !queue.empty();
       queue.pop_front(), p = queue.front()) {
    auto [pos, steps] = p;
    step_grid[pos.y][pos.x] = steps;
    for (Point neighbor : get_neighbors(grid, pos, seen)) {
      seen.insert(neighbor);
      queue.push_back({neighbor, steps + 1});
    }
  }
}

int main(int argc, char *argv[]) {
  // Parse input
  Grid grid;
  Point start, end;
  vector<vector<int>> step_grid;
  vector<Point> starts;
  vector<string> lines = aoc::input_lines(argc, argv);
  for (auto y = 0; y < lines.size(); ++y) {
    vector<char> row;
    for (auto x = 0; x < lines[y].size(); ++x) {
      row.push_back(lines[y][x]);
      switch (lines[y][x]) {
      case 'S':
        start = Point{x, y};
      case 'a':
        starts.push_back(Point{x, y});
        break;
      case 'E':
        end = Point{x, y};
      }
    }
    step_grid.push_back(vector<int>(row.size()));
    grid.push_back(move(row));
  }

  bfs(grid, end, step_grid);
  int shortest = numeric_limits<int>::max();
  for (auto start : starts) {
    int tile = grid[start.y][start.x];
    int steps = step_grid[start.y][start.x];
    if ((tile == 'a' || tile == 'S') && steps != 0)
      shortest = min(shortest, steps);
  }

  aoc::output(step_grid[start.y][start.x]);
  aoc::output(shortest);
}
