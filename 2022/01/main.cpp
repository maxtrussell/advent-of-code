#include <algorithm>
#include <numeric>
#include <string>
#include <vector>

#include "../aoc.cpp"

using namespace std;

int main(int argc, char *argv[]) {
  vector<string> lines = aoc::input_lines(argc, argv);
  vector<int> elves;
  int elf = 0;
  for (const auto &line : lines) {
    if (line == "") {
      elves.push_back(elf);
      elf = 0;
    } else
      elf += stoi(line);
  }
  elves.push_back(elf);
  sort(elves.begin(), elves.end(), [](int a, int b) { return a > b; });
  aoc::output(elves[0]);
  aoc::output(elves[0] + elves[1] + elves[2]);
}
