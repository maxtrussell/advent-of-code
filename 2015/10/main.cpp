#include <string>
#include <vector>

#include "../../lib/aoc.cpp"

using namespace std;

pair<int, int> rle(vector<int>::const_iterator& it,
                   const vector<int>::const_iterator end) {
  int orig = *it;
  int i = 1;
  while (*(it + i) == orig && it + i != end)
    ++i;
  it += i;
  return {orig, i};
}

vector<int> look_and_say(const vector<int>& orig) {
  vector<int> next;
  auto it = orig.cbegin();
  auto end = orig.cend();
  while (it != end) {
    auto [x, n] = rle(it, end);
    next.push_back(n);
    next.push_back(x);
  }
  return next;
}

int main(int argc, char *argv[]) {
  string line = aoc::input_lines(argc, argv)[0];
  vector<int> vals;
  for (char x : line)
    vals.push_back(x - '0');

  for (int i = 0; i < 50; ++i) {
    if (i == 40)
      aoc::output(vals.size());
    vals = look_and_say(vals);
  }
  aoc::output(vals.size());
}
