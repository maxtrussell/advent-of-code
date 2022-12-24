#include <algorithm>
#include <limits>
#include <string>
#include <string_view>
#include <unordered_map>
#include <unordered_set>
#include <vector>

#include "../lib/aoc.cpp"
#include "../lib/point.cpp"

using namespace std;

constexpr char Elf = '#';
const vector<string> Cardinals = {"north", "south", "west", "east"};
const vector<aoc::Point> Proposals = {{0, -1}, {0, 1}, {-1, 0}, {1, 0}};
const unordered_map<string, unordered_set<aoc::Point>> Dirs{
    {"north", {{0, -1}, {1, -1}, {-1, -1}}}, // N, NE, or NW
    {"south", {{0, 1}, {1, 1}, {-1, 1}}},    // S, SE, or SW
    {"west", {{-1, -1}, {-1, 0}, {-1, 1}}},  // W, WE, or WW
    {"east", {{1, -1}, {1, 0}, {1, 1}}}      // E, SE, or NE
};

class Grid {
public:
  Grid(const vector<string>& lines) {
    for (int y = 0; y < lines.size(); ++y)
      for (int x = 0; x < lines[y].length(); ++x)
        if (lines[y][x] == Elf)
          grid.insert({x, y});
  }
  inline bool contains(aoc::Point p) const { return grid.count(p) != 0; }
  void move(aoc::Point from, aoc::Point to) {
    assert(grid.count(to) == 0);
    grid.insert(to);
    grid.erase(from);
  }
  inline void insert(aoc::Point p) { grid.insert(p); }
  inline void erase(aoc::Point p) { grid.erase(p); }
  aoc::Rect get_bounds() {
    int max_x, max_y, min_x, min_y;
    max_x = max_y = numeric_limits<int>::min();
    min_x = min_y = numeric_limits<int>::max();
    for (auto elf : grid) {
      max_x = max(max_x, elf.x);
      max_y = max(max_y, elf.y);
      min_x = min(min_x, elf.x);
      min_y = min(min_y, elf.y);
    }
    return {{min_x, min_y}, {max_x, max_y}};
  }
  unordered_set<aoc::Point>::iterator begin() { return grid.begin(); }
  unordered_set<aoc::Point>::iterator end() { return grid.end(); }
  void print() {
    aoc::Rect bounds = get_bounds();
    for (int y = bounds.min_.y; y <= bounds.max_.y; ++y) {
      for (int x = bounds.min_.x; x <= bounds.max_.x; ++x)
        cout << (contains({x, y}) ? Elf : '.');
      cout << '\n';
    }
  }
  inline int count_empty_tiles() { return get_bounds().area() - grid.size(); }

private:
  unordered_set<aoc::Point> grid;
};

vector<aoc::Point> get_neighbors(const Grid& grid, aoc::Point p) {
  const static vector<aoc::Point> deltas = {{-1, -1}, {-1, 0}, {0, -1}, {-1, 1},
                                            {1, -1},  {1, 0},  {0, 1},  {1, 1}};
  vector<aoc::Point> neighbors;
  for (aoc::Point delta : deltas)
    neighbors.push_back(p + delta);
  return neighbors;
}

unordered_map<aoc::Point, vector<aoc::Point>> generate_proposals(Grid& grid,
                                                                 int round) {
  unordered_map<aoc::Point, vector<aoc::Point>> proposals;
  for (aoc::Point elf : grid) {
    vector<aoc::Point> neighbors = get_neighbors(grid, elf);
    if (none_of(neighbors.begin(), neighbors.end(),
                [&grid](aoc::Point n) { return grid.contains(n); }))
      continue;

    for (int i = 0; i < 4; ++i) {
      int index = aoc::mod((i + round), 4);
      const string& dir = Cardinals[index];
      if (none_of(neighbors.begin(), neighbors.end(),
                  [&grid, &dir, &elf](aoc::Point nei) {
                    return grid.contains(nei) &&
                           Dirs.at(dir).count(nei - elf) > 0;
                  })) {
        proposals[Proposals[index] + elf].push_back(elf);
        break;
      }
    }
  }
  return proposals;
}

bool move_elves(
    Grid& grid,
    const unordered_map<aoc::Point, vector<aoc::Point>>& proposals) {
  bool moved = false;
  for (const auto& [p, proposers] : proposals) {
    if (proposers.size() > 1)
      continue;
    moved = true;
    grid.move(proposers[0], p);
  }
  return moved;
}

int main(int argc, char *argv[]) {
  Grid grid(aoc::input_lines(argc, argv));
  bool moved = true;
  int i = 0;
  for (; moved; ++i) {
    if (i == 10)
      aoc::output(grid.count_empty_tiles());
    auto proposals = generate_proposals(grid, i);
    moved = move_elves(grid, proposals);
  }
  aoc::output(i);
}
