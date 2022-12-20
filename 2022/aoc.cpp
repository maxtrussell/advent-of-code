#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

#include "boost/algorithm/string/classification.hpp"
#include "boost/algorithm/string/split.hpp"

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

vector<string> split(const string &s, const string &sep) {
  vector<string> tokens;
  boost::split(tokens, s, boost::is_any_of(sep));
  return tokens;
}

int read_int(const string &line, string::const_iterator &it) {
  while (!isdigit(*it) && *it != '-') {
    ++it;
  }
  string buf;
  while (isdigit(*it) || *it == '-') {
    buf += *it;
    ++it;
  }
  return stoi(buf);
}

int read_int(const string &line) {
  auto it = line.cbegin();
  return read_int(line, it);
}

struct Point {
  int x = 0, y = 0;
};

ostream &operator<<(ostream &out, const Point &p) {
  return out << "Point{x: " << p.x << ", y: " << p.y << "}";
}

Point operator+(const Point &a, const Point &b) {
  return Point{a.x + b.x, a.y + b.y};
}

Point operator-(const Point &a, const Point &b) {
  return Point{a.x - b.x, a.y - b.y};
}

bool operator==(const Point &a, const Point &b) {
  return a.x == b.x && a.y == b.y;
}

bool operator!=(const Point &a, const Point &b) { return !(a == b); }

} // namespace aoc

template <> struct std::hash<aoc::Point> {
  size_t operator()(const aoc::Point &p) const noexcept {
    hash<int> hash_int;
    return hash_int(p.x) ^ hash_int(p.y);
  }
};
