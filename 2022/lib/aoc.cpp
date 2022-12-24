#include <algorithm>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

#include "boost/algorithm/string/classification.hpp"
#include "boost/algorithm/string/split.hpp"
#include <boost/container_hash/hash.hpp>

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

vector<string> split(const string& s, const string& sep) {
  vector<string> tokens;
  boost::split(tokens, s, boost::is_any_of(sep));
  return tokens;
}

int read_int(string::const_iterator& it) {
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

int read_int(const string& line) {
  auto it = line.cbegin();
  return read_int(it);
}

/**
 * An alternative modulo ensuring the return value is positive. Behaves like
 * python's mod.
 */
int64_t mod(int64_t x, int64_t y) { return ((x % y) + y) % y; }

/**
 * Returns the index of the given element or -1 if no match is found.
 */
template <typename Iter, typename Value>
int index_of(Iter begin, Iter end, Value v) {
  auto it = find(begin, end, v);
  if (it == end)
    return -1;
  return it - begin;
}

/**
 * Returns the index of the given element or -1 if no match is found.
 */
template <typename Cont, typename Value> int index_of(const Cont& c, Value v) {
  return index_of(c.begin(), c.end(), v);
}

} // namespace aoc
