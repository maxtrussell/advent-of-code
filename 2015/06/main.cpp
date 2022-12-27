#include <algorithm>
#include <string>
#include <vector>

#include "../../lib/aoc.cpp"
#include "../../lib/point.cpp"

using namespace std;

struct Instruction {
  aoc::Point start, end;
  string action;
};

void do_instruction(vector<vector<int>>& lights, const Instruction& inst) {
  for (int y = inst.start.y; y <= inst.end.y; ++y) {
    for (int x = inst.start.x; x <= inst.end.x; ++x) {
      if (inst.action == "on")
        lights[y][x] += 1;
      else if (inst.action == "off")
        lights[y][x] = max(0, lights[y][x] - 1);
      else
        lights[y][x] += 2; // This breaks part1
                           // lights[y][x] = !lights[y][x];
    }
  }
}

int main(int argc, char *argv[]) {
  vector<Instruction> instructions;
  for (const string& line : aoc::input_lines(argc, argv)) {
    vector<string> tokens = aoc::split(line, " ");
    auto it = line.begin();
    instructions.push_back({{aoc::read_int(it), aoc::read_int(it)},
                            {aoc::read_int(it), aoc::read_int(it)},
                            tokens[1]});
  };

  vector<vector<int>> lights(1000, vector<int>(1000, 0));
  for (const auto& inst : instructions)
    do_instruction(lights, inst);

  int64_t on = 0, brightness = 0;
  for (int y = 0; y < 1000; ++y) {
    for (int x = 0; x < 1000; ++x) {
      if (lights[y][x] > 0)
        ++on;
      brightness += lights[y][x];
    }
  }
  aoc::output(on);
  aoc::output(brightness);
}
