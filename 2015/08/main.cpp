#include <string>
#include <vector>

#include "../../lib/aoc.cpp"

using namespace std;

int eat_escape(string::const_iterator& it) {
  char next = *(it + 1);
  int code = (next == 'x') ? 4 : 2;
  it += code - 1;
  return code;
}

int main(int argc, char *argv[]) {
  int total_code = 0, total_string = 0;
  int escaped_total = 0;
  for (const string& line : aoc::input_lines(argc, argv)) {
    int code = 2, str = 0, escaped = 6;
    for (auto it = line.begin() + 1; it != line.end() - 1; ++it) {
      if (*it == '\\') {
        int new_code = eat_escape(it);
        code += new_code;
        escaped += new_code;
        escaped += (new_code == 4) ? 1 : 2;
      } else {
        ++code;
        ++escaped;
      }
      ++str;
    }

    total_code += code;
    total_string += str;
    escaped_total += escaped;
  }
  aoc::output(total_code - total_string);
  aoc::output(escaped_total - total_code);
}
