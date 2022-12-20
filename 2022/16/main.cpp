#include <algorithm>
#include <future>
#include <queue>
#include <string>
#include <tuple>
#include <unordered_map>
#include <unordered_set>
#include <vector>

#include "../aoc.cpp"

using namespace std;

struct Valve {
  int flow = 0;
  vector<string> children;
};

using Graph = unordered_map<string, Valve>;
using Paths = unordered_map<string, vector<pair<string, int>>>;

vector<pair<string, int>> bfs(const Graph& graph, const string& start) {
  queue<pair<string, int>> queue({{start, 0}});
  unordered_set<string> seen;
  vector<pair<string, int>> paths;
  for (; !queue.empty(); queue.pop()) {
    const auto& [loc, dist] = queue.front();
    Valve valve = graph.at(loc);
    if (valve.flow > 0)
      paths.push_back({loc, dist});

    for (const auto& child : valve.children) {
      if (seen.count(child))
        continue;
      seen.insert(child);
      queue.push({child, dist + 1});
    }
  }
  return paths;
}

// Caching would probably speed this up a bunch.
int dfs(const Graph& graph, const Paths& paths, const string& loc, int time,
        unordered_set<string>& opened) {
  int score = 0;
  Valve valve = graph.at(loc);
  opened.insert(loc);
  for (const auto& [child, dist] : paths.at(loc))
    if (time > dist + 1 && opened.count(child) == 0)
      score = max(score, dfs(graph, paths, child, time - dist - 1, opened));
  opened.erase(loc);

  score += valve.flow * time;
  return score;
}

void get_subsets(const vector<string>& choices, int i, vector<string>& subset,
                 vector<vector<string>>& subsets) {
  subsets.push_back(subset);
  for (auto j = i; j < choices.size(); ++j) {
    subset.push_back(choices[j]);
    get_subsets(choices, j + 1, subset, subsets);
    subset.pop_back();
  }
}

// TODO: Potential library function?
vector<vector<string>> get_subsets(const vector<string>& choices) {
  vector<vector<string>> subsets;
  vector<string> subset;
  get_subsets(choices, 0, subset, subsets);
  return subsets;
}

pair<unordered_set<string>, unordered_set<string>>
get_opened(const vector<string>& all, const vector<string>& subset) {
  unordered_set<string> human(subset.begin(), subset.end());
  unordered_set<string> elephant;
  for (const auto& valve : all)
    if (human.count(valve) == 0)
      elephant.insert(valve);
  return {human, elephant};
}

int main(int argc, char *argv[]) {
  vector<string> lines = aoc::input_lines(argc, argv);

  // Make a graph
  Graph graph;

  // Add all valves
  for (const auto& line : lines) {
    vector<string> tokens = aoc::split(line, " ");
    graph[tokens[1]] = Valve{aoc::read_int(tokens[4])};
  }
  // Add all edges
  for (const auto& line : lines) {
    vector<string> tokens = aoc::split(line, " ");
    for (auto i = 9; i < tokens.size(); ++i)
      graph[tokens[1]].children.push_back(tokens[i].substr(0, 2));
  }

  // Use BFS to pre-calculate distances between all valves with positive flow.
  // Floyd Warshall may be a more efficient implementation.
  Paths paths;
  for (const auto& [start, valve] : graph)
    for (const auto& result : bfs(graph, start))
      paths[start].push_back(result);

  // Part 1
  unordered_set<string> opened;
  aoc::output(dfs(graph, paths, "AA", 30, opened));

  // Part 2
  vector<string> positive_flow_valves;
  for (const auto& [name, valve] : graph)
    if (valve.flow > 0)
      positive_flow_valves.push_back(name);

  int score = 0;
  vector<vector<string>> subsets = get_subsets(positive_flow_valves);
  for (const auto& subset : subsets) {
    // Run a DFS for both human and elephant, giving each only a subset of the
    // valves.
    int curr_score = 0;
    auto [human, elephant] = get_opened(positive_flow_valves, subset);
    curr_score += dfs(graph, paths, "AA", 26, human);
    curr_score += dfs(graph, paths, "AA", 26, elephant);
    score = max(score, curr_score);
  }
  aoc::output(score);
}
