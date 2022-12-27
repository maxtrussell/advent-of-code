#include <algorithm>
#include <regex>
#include <string>
#include <vector>

#include "../../lib/aoc.cpp"

using namespace std;

bool is_nice1(const string& s) {
  const static regex vowels("(.*[aeiou].*){3,}");
  const static regex two_in_a_row(R"((.)\1)");
  const static regex not_allowed("ab|cd|pq|xy");

  return regex_search(s, vowels) && regex_search(s, two_in_a_row) &&
         !regex_search(s, not_allowed);
}

bool is_nice2(const string& s) {
  const static regex pair_twice(R"((..).*\1)");
  const static regex one_letter_between(R"((.).\1)");

  return regex_search(s, pair_twice) && regex_search(s, one_letter_between);
}

int main(int argc, char *argv[]) {
  const vector<string> lines = aoc::input_lines(argc, argv);
  int part1 = count_if(lines.begin(), lines.end(), is_nice1);
  aoc::output(part1);

  int part2 = count_if(lines.begin(), lines.end(), is_nice2);
  aoc::output(part2);
}
