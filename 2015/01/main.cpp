#include <algorithm>
#include <string>
#include <vector>

#include "../../lib/aoc.cpp"

using namespace std;

int main(int argc, char *argv[]) {
  const string line = aoc::input_lines(argc, argv)[0];
  int floors = 0;
  int basement = 0;
  for (int i = 0; i < line.size(); ++i) {
    floors += (line[i] == '(' ? 1 : -1);
    if (floors == -1 && !basement)
      basement = i + 1;
  }
  aoc::output(floors);
  aoc::output(basement);
}
