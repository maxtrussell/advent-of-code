#include <string>
#include <unordered_set>
#include <vector>

#include "../../lib/aoc.cpp"
#include "../../lib/point.cpp"

using namespace std;

int main(int argc, char *argv[]) {
  const string line = aoc::input_lines(argc, argv)[0];
  unordered_set<aoc::Point> houses1, houses2;
  aoc::Point pos{0, 0}, santa{0, 0}, robot{0, 0};
  houses1.insert(santa);
  houses2.insert(santa);
  for (int i = 0; i < line.length(); ++i) {
    aoc::Point delta;
    if (line[i] == '<')
      delta = {-1, 0};
    else if (line[i] == '>')
      delta = {1, 0};
    else if (line[i] == '^')
      delta = {0, -1};
    else
      delta = {0, 1};

    pos += delta;
    houses1.insert(pos);
    aoc::Point& part2 = (i % 2 == 0) ? santa : robot;
    part2 += delta;
    houses2.insert(part2);
  }
  aoc::output(houses1.size());
  aoc::output(houses2.size());
}
