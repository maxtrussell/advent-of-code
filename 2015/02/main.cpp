#include <string>
#include <vector>

#include "../../lib/aoc.cpp"

using namespace std;

struct Box {
  int length = 0, width = 0, height = 0;

  int get_paper() {
    const vector<pair<int, int>> faces{
        {length, width}, {length, height}, {width, height}};

    int paper = 0;
    int smallest_face = length * width * height;
    for (auto [d1, d2] : faces) {
      smallest_face = min(smallest_face, d1 * d2);
      paper += 2 * d1 * d2;
    }
    return paper + smallest_face;
  }

  int get_ribbon() {
    vector<int> sides{length, width, height};
    sort(sides.begin(), sides.end());
    return (sides[0] * 2) + (sides[1] * 2) + length * width * height;
  }
};

int main(int argc, char *argv[]) {
  int paper = 0, ribbon = 0;
  for (const string& line : aoc::input_lines(argc, argv)) {
    auto it = line.begin();
    Box box{aoc::read_int(it), aoc::read_int(it), aoc::read_int(it)};
    paper += box.get_paper();
    ribbon += box.get_ribbon();
  }
  aoc::output(paper);
  aoc::output(ribbon);
}
