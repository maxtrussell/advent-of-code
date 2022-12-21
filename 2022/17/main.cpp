#include <array>
#include <boost/container_hash/hash.hpp>
#include <boost/container_hash/hash_fwd.hpp>
#include <cstdlib>
#include <limits>
#include <sstream>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

#include "../aoc.cpp"

using namespace std;
using Grid = vector<unordered_set<int>>;

struct CycleData {
  int64_t i = 0;
  int64_t height = 0;
  int64_t seen = 0;
};

const vector<vector<aoc::Point>> rocks = {
    // ####
    {{0, 0}, {1, 0}, {2, 0}, {3, 0}},
    // .#.
    // ###
    // .#.
    {{1, 0}, {0, 1}, {1, 1}, {2, 1}, {1, 2}},
    // ..#
    // ..#
    // ###
    {{2, 2}, {2, 1}, {0, 0}, {1, 0}, {2, 0}},
    // #
    // #
    // #
    // #
    {{0, 0}, {0, 1}, {0, 2}, {0, 3}},
    // ##
    // ##
    {{0, 0}, {0, 1}, {1, 0}, {1, 1}}};

bool collision_check(const Grid& grid, aoc::Point pos,
                     const vector<aoc::Point>& rock) {
  for (const aoc::Point& rp : rock) {
    aoc::Point p = pos + rp;
    if (p.x < 0 || p.x > 6 || p.y <= 0 || grid[p.x].count(p.y) > 0)
      return true;
  }
  return false;
}

void drop_rock(Grid& grid, int i, int& jet_index, int64_t& highest,
               const string& dirs) {
  const vector<aoc::Point>& rock = rocks[i % rocks.size()];
  aoc::Point pos{2, static_cast<int>(highest + 4)};
  aoc::Point dy{0, -1};

  // Drop the rock
  bool done = false;
  for (auto j = 0; !done; ++j) {
    jet_index = (jet_index + 1) % dirs.length();
    int dir = dirs[jet_index] == '<' ? -1 : 1;
    aoc::Point dx{dir, 0};

    for (aoc::Point delta : {dx, dy}) {
      bool collided = collision_check(grid, pos + delta, rock);
      if (!collided)
        pos += delta;
      done = (collided && delta == dy);
    }
  }

  // Update the map
  for (aoc::Point rp : rock) {
    aoc::Point p = pos + rp;
    grid[p.x].insert(p.y);
    highest = max(highest, (int64_t)p.y);
  }
}

size_t state_hash(int rock_index, int jet_index) {
  size_t seed = 0;
  boost::hash_combine(seed, rock_index);
  boost::hash_combine(seed, jet_index);
  return seed;
}

int main(int argc, char *argv[]) {
  const string dirs = aoc::input_lines(argc, argv)[0];
  Grid grid;
  for (auto i = 0; i < 7; ++i)
    grid.push_back(unordered_set<int>{});

  constexpr int64_t num_rocks = 1'000'000'000'000;
  int64_t highest = 0;
  int jet_index = -1;
  int64_t skipped_height = 0, skipped_rocks = 0;
  bool have_skipped = false;
  unordered_map<size_t, CycleData> seen_states;
  int64_t i = 0;
  while (i + skipped_rocks < num_rocks) {
    drop_rock(grid, i, jet_index, highest, dirs);
    if (i == 2021)
      aoc::output(highest);

    size_t state = state_hash(i % rocks.size(), jet_index);
    int64_t seen = 1;
    if (seen_states.count(state)) {
      CycleData cycle_data = seen_states.at(state);
      seen = cycle_data.seen + 1;
      if (seen >= 2 && !have_skipped && i >= 2021) {
        // We've seen enough to know a cycle
        // Advance as far as possible based on cycles
        int64_t cycle_height = highest - cycle_data.height;
        int64_t cycle_length = i - cycle_data.i;
        int64_t cycles_to_skip = (num_rocks - i) / cycle_length;
        skipped_height = cycles_to_skip * cycle_height;
        skipped_rocks = cycles_to_skip * cycle_length;
        have_skipped = true;
      }
    }
    seen_states[state] = {i, highest, seen};
    ++i;
  }
  aoc::output(highest + skipped_height);
}
