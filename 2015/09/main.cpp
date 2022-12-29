#include <limits>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>

#include "../../lib/aoc.cpp"

using namespace std;

enum class Mode { Shortest, Longest };

struct Route {
  string destination;
  int distance;
};

int dfs(const unordered_map<string, vector<Route>>& routes, const string& curr,
        int dist, int best, unordered_set<string>& seen, Mode mode) {
  seen.insert(curr);
  if (seen.size() == routes.size() ||
      (mode == Mode::Shortest && dist >= best)) {
    seen.erase(curr);
    return dist;
  }

  int distance = best;
  for (const Route& route : routes.at(curr))
    if (seen.count(route.destination) == 0) {
      int child = dfs(routes, route.destination, dist + route.distance, best,
                      seen, mode);
      distance = (mode == Mode::Shortest) ? min(distance, child)
                                          : max(distance, child);
    }
  seen.erase(curr);
  return distance;
}

int main(int argc, char *argv[]) {
  unordered_map<string, vector<Route>> routes;
  for (const string& line : aoc::input_lines(argc, argv)) {
    vector<string> tokens = aoc::split(line, " ");
    const string &a = tokens[0], b = tokens[2];
    int distance = stoi(tokens[4]);
    routes[a].push_back(Route{b, distance});
    routes[b].push_back(Route{a, distance});
  }

  vector<pair<Mode, int>> parts{{Mode::Shortest, numeric_limits<int>::max()},
                                {Mode::Longest, -1}};
  for (auto [mode, best] : parts) {
    for (const auto& [start, _] : routes) {
      unordered_set<string> seen;
      int dist = dfs(routes, start, 0, best, seen, mode);
      best = (mode == Mode::Shortest) ? min(best, dist) : max(best, dist);
    }
    aoc::output(best);
  }
}
