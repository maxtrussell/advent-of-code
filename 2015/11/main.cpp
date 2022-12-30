#include <string>
#include <unordered_set>
#include <vector>

#include "../../lib/aoc.cpp"

using namespace std;

bool is_valid(const string& password) {
  const static unordered_set<char> forbidden{'i', 'o', 'l'};
  int pairs_found = 0, num_increasing = 1, max_increasing = 0;
  char prev = '\0', prev_pair = '\0';
  for (char x : password) {
    if (forbidden.count(x))
      return false;

    if (x == prev && x != prev_pair) {
      ++pairs_found;
      prev_pair = x;
    }

    if (x == prev + 1)
      ++num_increasing;
    else
      num_increasing = 1;

    max_increasing = max(max_increasing, num_increasing);
    prev = x;
  }
  return pairs_found >= 2 && max_increasing >= 3;
}

string increment_password(const string& old) {
  string incremented = old;
  bool carry = true;
  for (int i = old.size() - 1; i >= 0 && carry; --i) {
    char sum = old[i] + 1;
    if (sum > 'z')
      sum = 'a';
    carry = (sum == 'a');
    incremented[i] = sum;
  }
  return incremented;
}

int main(int argc, char *argv[]) {
  string password = aoc::input_lines(argc, argv)[0];

  // Part 1
  while (!is_valid(password))
    password = increment_password(password);
  aoc::output(password);

  // Part 2
  password = increment_password(password);
  while (!is_valid(password))
    password = increment_password(password);
  aoc::output(password);
}
