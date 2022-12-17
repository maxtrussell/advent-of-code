#include "../aoc.cpp"

using namespace std;

char normalize(char move) { return move > 'C' ? move - ('X' - 'A') : move; }
int score_move(char move) { return move - 'A' + 1; }

char get_move(char opp, char me) {
  if (me == 'B')
    return opp;
  int delta = me == 'A' ? -1 : 1;
  return ((opp - 'A' + delta + 3) % 3) + 'A';
}

int result(char a, char b) {
  int diff = (b - a + 3) % 3;
  if (diff == 0)
    return 3;
  else if (diff == 1)
    return 6;
  return 0;
}

int main(int argc, char *argv[]) {
  int part1 = 0, part2 = 0;
  for (const auto &line : aoc::input_lines(argc, argv)) {
    char opp = line[0];
    char me = normalize(line[2]);
    part1 += score_move(me) + result(opp, me);
    me = get_move(opp, me);
    part2 += score_move(me) + result(opp, me);
  }
  aoc::output(part1);
  aoc::output(part2);
}
