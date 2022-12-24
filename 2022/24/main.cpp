#include <queue>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>

#include <boost/container_hash/hash.hpp>

#include "../lib/aoc.cpp"
#include "../lib/grid.cpp"

using namespace std;
using Blizzards = unordered_map<aoc::Point, vector<aoc::Point>>;

const unordered_map<char, aoc::Point> Deltas = {
    {'>', {1, 0}}, {'v', {0, 1}}, {'<', {-1, 0}}, {'^', {0, -1}}};

struct State {
  int step = 0;
  aoc::Point pos{};
};

bool operator==(const State& a, const State& b) {
  return a.step == b.step && a.pos == b.pos;
}

template <> struct std::hash<State> {
  size_t operator()(const State& s) const noexcept {
    size_t hash = 0;
    boost::hash_combine(hash, s.step);
    boost::hash_combine(hash, s.pos.x);
    boost::hash_combine(hash, s.pos.y);
    return hash;
  }
};

Blizzards update_blizzards(const aoc::Grid<char>& grid,
                           const Blizzards& blizzards) {
  Blizzards updated;
  for (auto [pos, deltas] : blizzards) {
    for (aoc::Point d : deltas) {
      aoc::Point next = pos + d;
      if (!grid.in_bounds(next + d)) {
        next.y = aoc::mod(next.y + d.y, grid.height()) + d.y;
        next.x = aoc::mod(next.x + d.x, grid.width()) + d.x;
      }
      updated[next].push_back(d);
    }
  }
  return updated;
}

vector<aoc::Point> get_moves(const aoc::Grid<char>& grid, aoc::Point pos,
                             const Blizzards& blizzards) {
  // You can move in any direction
  vector<aoc::Point> pot_neighbors = grid.get_neighbors(pos);
  // or you can wait in place
  pot_neighbors.push_back(pos);
  // but you cannot move into a wall or blizzard.
  vector<aoc::Point> neighbors;
  for (aoc::Point n : pot_neighbors)
    if (grid[n] != '#' && blizzards.count(n) == 0)
      neighbors.push_back(n);

  return neighbors;
}

pair<int, Blizzards> bfs(const aoc::Grid<char>& grid, aoc::Point start,
                         aoc::Point end, Blizzards& blizzards,
                         unordered_set<State> cache) {
  queue<pair<aoc::Point, int>> q;
  q.push({start, 0});
  int prev_steps = -1;
  while (!q.empty()) {
    auto [pos, steps] = q.front();
    q.pop();

    // Blizzards are cyclical, so blizzard state is the lcm of the blizzard
    // cycle.
    int blizzard_state =
        aoc::mod(steps, (grid.height() - 2) * (grid.width() - 2));
    if (cache.count({blizzard_state, pos}) > 0)
      continue;
    cache.insert({blizzard_state, pos});

    // Blizzards move first
    if (steps > prev_steps)
      blizzards = update_blizzards(grid, blizzards);
    prev_steps = steps;

    if (pos == end)
      return {steps, blizzards};

    for (aoc::Point nei : get_moves(grid, pos, blizzards))
      q.push({nei, steps + 1});
  }
  assert(false && "unreachable");
}

int main(int argc, char *argv[]) {
  aoc::Grid<char> grid(aoc::input_lines(argc, argv));
  // FIXME: I don't actually need to track the blizzards, could just use time +
  // lcm.
  unordered_map<aoc::Point, vector<aoc::Point>> blizzards;
  for (aoc::Point p : grid.get_points())
    if (grid[p] != '#' && grid[p] != '.')
      blizzards[p].push_back(Deltas.at(grid[p]));

  aoc::Point start = {1, 0}, end = {grid.width() - 2, grid.height() - 1};
  int steps = 0;
  for (auto [s, e] : vector<pair<aoc::Point, aoc::Point>>{
           {start, end}, {end, start}, {start, end}}) {
    unordered_set<State> cache;
    auto result = bfs(grid, s, e, blizzards, cache);
    steps += result.first;
    blizzards = result.second;
    if (s == start && e == end)
      aoc::output(steps);
  }
}
