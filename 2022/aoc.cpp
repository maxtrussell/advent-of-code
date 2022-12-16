#include <fstream>
#include <iostream>
#include <string>
#include <vector>

namespace aoc {
using namespace std;

vector<string> input_lines(const string &filename) {
  ifstream infile(filename);
  vector<string> lines;
  for (string line; getline(infile, line);)
    lines.push_back(line);
  return lines;
}

template <typename T> void output(T msg) {
  static int part;
  std::cout << "Part " << ++part << ": " << msg << std::endl;
}
} // namespace aoc
