#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

namespace aoc {
using namespace std;

vector<string> input_lines(int argc, char **argv) {
  if (argc < 2)
    throw invalid_argument("Input file is required");
  ifstream ifs(*(++argv));
  if (!ifs)
    throw invalid_argument("Could not open file");
  vector<string> lines;
  for (string line; getline(ifs, line);)
    lines.push_back(move(line));
  return lines;
}

template <typename T> void output(T msg) {
  static int part;
  std::cout << "Part " << ++part << ": " << msg << std::endl;
}
} // namespace aoc
