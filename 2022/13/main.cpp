#include <algorithm>
#include <cctype>
#include <initializer_list>
#include <regex>
#include <string>
#include <variant>
#include <vector>

#include "../aoc.cpp"

using namespace std;

enum class Result { RIGHT, EQUAL, WRONG };

class Packet {
public:
  Packet(int value) : value_(value) {}
  Packet(vector<Packet> children) : children_(children) {}

  bool is_int() const { return value_ != -1; }
  int as_int() const { return value_; }
  vector<Packet> as_list() const {
    if (value_ == -1)
      return children_;
    return {value_};
  }

private:
  vector<Packet> children_;
  int value_ = -1;
};

Result validate(const Packet &a, const Packet &b) {
  Packet left = a, right = b;
  // Both are integers
  if (left.is_int() && right.is_int()) {
    int l = left.as_int(), r = right.as_int();
    if (l == r)
      return Result::EQUAL;
    return l < r ? Result::RIGHT : Result::WRONG;
  }

  // Both are lists
  vector<Packet> l = left.as_list(), r = right.as_list();
  for (auto i = 0; i < l.size() && i < r.size(); ++i)
    if (Result res = validate(l[i], r[i]); res != Result::EQUAL)
      return res;

  if (l.size() == r.size())
    return Result::EQUAL;
  return l.size() < r.size() ? Result::RIGHT : Result::WRONG;
}

bool operator<(const Packet &a, const Packet &b) {
  return validate(a, b) == Result::RIGHT;
}

bool operator==(const Packet &a, const Packet &b) {
  return validate(a, b) == Result::EQUAL;
}

bool operator<=(const Packet &a, const Packet &b) {
  Result res = validate(a, b);
  return res == Result::EQUAL || res == Result::RIGHT;
}

int read_number(const string &line, string::const_iterator &it) {
  string s;
  while (isdigit(*it))
    s += *it++;
  return stoi(s);
}

// Recursively parse packets
Packet parse(const string &line, string::const_iterator &it) {
  vector<Packet> children;
  while (true) {
    if (*it == '[') {
      it++;
      children.push_back(parse(line, it));
    } else if (*it == ']') {
      it++;
      return Packet(children);
    } else if (isdigit(*it)) {
      int x = read_number(line, it);
      children.push_back(Packet(x));
    } else
      it++;
  }
}

Packet parse(const string &line) {
  auto it = line.begin();
  it++;
  return parse(line, it);
}

int main(int argc, char *argv[]) {
  vector<string> lines = aoc::input_lines(argc, argv);
  Packet div1 = parse("[[2]]"), div2 = parse("[[6]]");
  vector<Packet> all_packets{div1, div2};

  // Part 1
  int part1 = 0;
  for (auto i = 0; i < lines.size() - 1; i += 3) {
    Packet left = parse(lines[i]), right = parse(lines[i + 1]);
    all_packets.push_back(left);
    all_packets.push_back(right);
    if (left <= right)
      part1 += (i / 3) + 1;
  }
  aoc::output(part1);

  // Part 2
  int part2 = 1;
  sort(all_packets.begin(), all_packets.end());
  for (auto target : {div1, div2}) {
    auto it = find(all_packets.begin(), all_packets.end(), target);
    part2 *= it - all_packets.begin() + 1;
  }
  aoc::output(part2);
}
