#include <algorithm>
#include <string>
#include <unordered_map>
#include <vector>

#include "../aoc.cpp"

using namespace std;

enum Material { Ore, Clay, Obsidian, Geode };

using Blueprint = vector<array<int, 4>>;

struct Inventory {
  array<int, 4> drones{1, 0, 0, 0};
  array<int, 4> resources{0, 0, 0, 0};
};

using Cache = unordered_map<pair<Inventory, int>, int>;

bool operator==(const pair<Inventory, int>& a, const pair<Inventory, int>& b) {
  const auto& [a_inv, a_time] = a;
  const auto& [b_inv, b_time] = b;
  return a_inv.drones == b_inv.drones && a_inv.resources == b_inv.resources &&
         a_time == b_time;
}

template <> struct std::hash<pair<Inventory, int>> {
  size_t operator()(const pair<Inventory, int>& p) const noexcept {
    size_t hash = 0;
    const auto& [inv, time] = p;
    boost::hash_combine(hash, inv.drones[0]);
    boost::hash_combine(hash, inv.drones[1]);
    boost::hash_combine(hash, inv.drones[2]);
    boost::hash_combine(hash, inv.drones[3]);
    boost::hash_combine(hash, inv.resources[0]);
    boost::hash_combine(hash, inv.resources[1]);
    boost::hash_combine(hash, inv.resources[2]);
    boost::hash_combine(hash, inv.resources[3]);
    boost::hash_combine(hash, time);
    return hash;
  }
};

array<int, 4> operator+(const array<int, 4>& a, const array<int, 4>& b) {
  return {a[0] + b[0], a[1] + b[1], a[2] + b[2], a[3] + b[3]};
}
array<int, 4> operator*(const array<int, 4>& a, int b) {
  return {a[0] * b, a[1] * b, a[2] * b, a[3] * b};
}
array<int, 4> operator-(const array<int, 4>& a, const array<int, 4>& b) {
  return {a[0] - b[0], a[1] - b[1], a[2] - b[2], a[3] - b[3]};
}

void operator+=(array<int, 4>& a, const array<int, 4>& b) { a = a + b; }
void operator-=(array<int, 4>& a, const array<int, 4>& b) { a = a - b; }

bool operator>=(const array<int, 4>& a, const array<int, 4>& b) {
  return a[0] >= b[0] && a[1] >= b[1] && a[2] >= b[2] && a[3] >= b[3];
}

int most_possible(const Inventory& inv, int time) {
  int geodes = inv.resources[Geode] + inv.drones[Geode] * time;
  // Produce geodes non stop
  geodes += ((time * time + time) / 2);
  return geodes;
}

// Depth first search
int max_geodes(const Blueprint& bp, int time, Inventory& inv, Cache& cache,
               int& best) {
  if (time <= 0 || most_possible(inv, time) <= best)
    return 0;

  int most_geodes = 0;
  const auto& cache_key = make_pair(inv, time);
  if (cache.count(cache_key))
    return cache.at(cache_key);

  // Make purchases if possible
  Inventory old = inv;
  for (auto mat = 3; mat >= 0; --mat) {
    if (inv.resources >= bp[mat]) {
      inv.resources += inv.drones - bp[mat];
      ++inv.drones[mat];
      most_geodes =
          max(most_geodes, max_geodes(bp, time - 1, inv, cache, best));
      inv = old;
    }
  }

  // Mine for a minute
  inv.resources += inv.drones;
  --time;

  // Branch one more time, post-mining
  most_geodes = max(most_geodes, max_geodes(bp, time, inv, cache, best));

  most_geodes = max(most_geodes, inv.resources[Geode]);
  cache[cache_key] = most_geodes;
  best = max(best, most_geodes);
  return most_geodes;
}

int main(int argc, char *argv[]) {
  vector<Blueprint> blueprints;
  for (const string& line : aoc::input_lines(argc, argv)) {
    Blueprint blueprint;
    auto it = line.begin();
    aoc::read_int(line, it);                              // blueprint number
    blueprint.push_back({aoc::read_int(line, it), 0, 0}); // ore robot
    blueprint.push_back({aoc::read_int(line, it), 0, 0}); // clay robot
    blueprint.push_back({aoc::read_int(line, it), aoc::read_int(line, it),
                         0}); // obsidian robot
    blueprint.push_back(
        {aoc::read_int(line, it), 0, aoc::read_int(line, it)}); // geode robot
    blueprints.push_back(move(blueprint));
  }

  // Part 1
  int part1 = 0;
  int time = 24;
  for (auto i = 0; i < blueprints.size(); ++i) {
    Inventory inv{};
    Cache cache{};
    int best = 0;
    int geodes = max_geodes(blueprints[i], time, inv, cache, best);
    part1 += geodes * (i + 1);
  }
  aoc::output(part1);

  // Part 2
  time = 32;
  int part2 = 1;
  for (auto i = 0; i < 3; ++i) {
    Inventory inv{};
    Cache cache{};
    int best = 0;
    int geodes = max_geodes(blueprints[i], time, inv, cache, best);
    part2 *= geodes;
  }
  aoc::output(part2);
}
