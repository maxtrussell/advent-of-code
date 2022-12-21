#include <cassert>
#include <string>
#include <unordered_map>
#include <vector>

#include "../aoc.cpp"

using namespace std;

struct TreeNode {
  string name;
  char op;
  int64_t value = 0;
  pair<string, string> children;

  int64_t get_value(const unordered_map<string, TreeNode>& edges) const {
    if (op == '\0')
      return value;

    auto [child_a, child_b] = children;
    int64_t a = edges.at(child_a).get_value(edges);
    int64_t b = edges.at(child_b).get_value(edges);
    switch (op) {
    case '+':
      return a + b;
    case '-':
      return a - b;
    case '*':
      return a * b;
    case '/':
      return a / b;
    case '=':
      return a == b;
    }
    assert(false && "unreachable");
  }

  int64_t solve_for_human(const unordered_map<string, TreeNode>& edges) const {
    const auto& [hchild, child] = find_human_child(edges);
    int64_t solve_for = child.get_value(edges);
    return hchild.solve(edges, solve_for);
  }

  int64_t solve(const unordered_map<string, TreeNode>& edges,
                int64_t solve_for) const {
    if (name == "humn")
      return solve_for;

    const auto& [hchild, child] = find_human_child(edges);
    int64_t b = child.get_value(edges);
    bool human_is_rhs = (hchild.name == children.second);
    switch (op) {
    case '+':
      solve_for -= b;
      break;
    case '-':
      if (human_is_rhs)
        solve_for = b - solve_for;
      else
        solve_for += b;
      break;
    case '*':
      solve_for /= b;
      break;
    case '/':
      if (human_is_rhs)
        solve_for = b / solve_for;
      else
        solve_for *= b;
      break;
    }
    return hchild.solve(edges, solve_for);
  }

  pair<TreeNode, TreeNode>
  find_human_child(const unordered_map<string, TreeNode>& edges) const {
    string hchild, child;
    if (edges.at(children.first).has_human(edges)) {
      hchild = children.first;
      child = children.second;
    } else {
      hchild = children.second;
      child = children.first;
    }
    return {edges.at(hchild), edges.at(child)};
  }

  bool has_human(const unordered_map<string, TreeNode>& edges) const {
    if (op == '\0')
      return name == "humn";

    auto [child_a, child_b] = children;
    return edges.at(child_a).has_human(edges) ||
           edges.at(child_b).has_human(edges);
  }
};

int main(int argc, char *argv[]) {
  unordered_map<string, TreeNode> edges;
  for (const string& line : aoc::input_lines(argc, argv)) {
    string name(line.begin(), line.begin() + 4);
    if (isdigit(line.at(6))) {
      auto x = static_cast<int64_t>(aoc::read_int(line));
      edges[name] = {name, '\0', x};
    } else {
      pair<string, string> children;
      children.first = string(line.begin() + 6, line.begin() + 10);
      children.second = string(line.begin() + 13, line.begin() + 17);
      char op = line.at(11);
      edges[name] = {name, op, 0, children};
    }
  }

  // Part 1
  aoc::output(edges["root"].get_value(edges));

  // Part 2
  int64_t ans = edges["root"].solve_for_human(edges);
  aoc::output(ans);
}
