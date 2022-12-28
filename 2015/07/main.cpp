#include <algorithm>
#include <cctype>
#include <memory>
#include <optional>
#include <string>
#include <unordered_map>
#include <vector>

#include "../../lib/aoc.cpp"

using namespace std;

class TreeNode {
public:
  virtual ~TreeNode() = default;
  virtual uint16_t
  get_value(const unordered_map<string, unique_ptr<TreeNode>>& tree,
            unordered_map<string, uint16_t>& cache) const = 0;
};

// Wrapper function for debug and caching.
uint16_t get_node_val(const unordered_map<string, unique_ptr<TreeNode>>& tree,
                      unordered_map<string, uint16_t>& cache,
                      const string& name) {
  if (!cache.count(name))
    cache[name] = tree.at(name)->get_value(tree, cache);
  return cache.at(name);
}

class UnaryNode : public TreeNode {
public:
  UnaryNode(string the_op, string the_child) : op(the_op), child(the_child) {}

  uint16_t get_value(const unordered_map<string, unique_ptr<TreeNode>>& tree,
                     unordered_map<string, uint16_t>& cache) const {
    uint16_t child_val = get_node_val(tree, cache, child);
    if (op == "NOT")
      return ~child_val;
    else if (op == "REF")
      return child_val;
    assert(false && "unreachable");
  }

private:
  string op;
  string child;
};

class BinaryNode : public TreeNode {
public:
  BinaryNode(string the_op, string left, string right)
      : op(the_op), left_child(left), right_child(right) {}

  uint16_t get_value(const unordered_map<string, unique_ptr<TreeNode>>& tree,
                     unordered_map<string, uint16_t>& cache) const {
    uint16_t left_val = get_node_val(tree, cache, left_child);
    uint16_t right_val = get_node_val(tree, cache, right_child);
    if (op == "AND") {
      return left_val & right_val;
    } else if (op == "OR") {
      return left_val | right_val;
    } else if (op == "LSHIFT") {
      return left_val << right_val;
    } else if (op == "RSHIFT") {
      return left_val >> right_val;
    }
    assert(false && "unreachable");
  }

private:
  string op;
  string left_child;
  string right_child;
};

class ValueNode : public TreeNode {
public:
  ValueNode(uint16_t val) : value(val) {}
  void set_value(uint16_t val) { value = val; }

  uint16_t get_value(const unordered_map<string, unique_ptr<TreeNode>>&,
                     unordered_map<string, uint16_t>&) const {
    return value;
  }

private:
  uint16_t value;
};

bool is_number(const string& s) {
  for (char c : s)
    if (!isdigit(c))
      return false;
  return true;
}

int main(int argc, char **argv) {
  unordered_map<string, unique_ptr<TreeNode>> tree;
  for (const string& line : aoc::input_lines(argc, argv)) {
    vector<string> tokens = aoc::split(line, " ");
    if (tokens.size() == 5) {
      // Binary node
      const string& left = tokens[0];
      const string& op = tokens[1];
      const string& right = tokens[2];
      const string& name = tokens[4];

      // If right hand side is a number, insert a corresponding value node.
      if (is_number(right))
        tree[right] = make_unique<ValueNode>(stoi(right));

      tree[name] = make_unique<BinaryNode>(op, left, right);
    } else if (tokens[0] == "NOT") {
      tree[tokens[3]] = make_unique<UnaryNode>(tokens[0], tokens[1]);
    } else if (is_number(tokens[0])) {
      tree[tokens[2]] = make_unique<ValueNode>(stoi(tokens[0]));
    } else {
      // Reference node, e.g. x -> y
      tree[tokens[2]] = make_unique<UnaryNode>("REF", tokens[0]);
    }
  }

  // Part 1
  unordered_map<string, uint16_t> cache;
  uint16_t part1 = get_node_val(tree, cache, "a");
  aoc::output(part1);

  // Part 2
  cache.clear();
  tree["b"] = make_unique<ValueNode>(part1);
  aoc::output(get_node_val(tree, cache, "a"));
}
