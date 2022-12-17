#include <algorithm>
#include <string>
#include <unordered_set>
#include <utility>
#include <vector>

#include "../aoc.cpp"

using namespace std;
using Bag = unordered_set<char>;

int get_priority(char x) {
  if (x < 'a')
    return x - 'A' + 27;
  return x - 'a' + 1;
}

char intersect(const vector<Bag> &bags) {
  for (char x : bags[0])
    if (all_of(bags.begin() + 1, bags.end(),
               [x](const Bag &b) { return b.find(x) != b.end(); }))
      return x;
  __builtin_unreachable();
}

int main(int argc, char *argv[]) {
  vector<Bag> bags;
  int part1 = 0, part2 = 0;
  for (const string &line : aoc::input_lines(argc, argv)) {
    int m = line.length() / 2;
    Bag l(line.begin(), line.begin() + m);
    Bag r(line.begin() + m, line.end());
    part1 += get_priority(intersect({move(l), move(r)}));

    bags.push_back({line.begin(), line.end()});
    if (bags.size() == 3) {
      part2 += get_priority(intersect(bags));
      bags.clear();
    }
  }
  aoc::output(part1);
  aoc::output(part2);
}
