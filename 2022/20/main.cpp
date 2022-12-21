#include <string>
#include <vector>

#include "../aoc.cpp"

using namespace std;

void move_element(vector<int64_t>& buf, int64_t buf_index,
                  int64_t index_delta) {
  int64_t dst = aoc::mod(buf_index + index_delta, buf.size() - 1);
  int64_t buf_elem = buf[buf_index];
  buf.erase(buf.begin() + buf_index);
  buf.insert(buf.begin() + dst, buf_elem);
}

int64_t find(const vector<int64_t>& haystack, int64_t needle) {
  return find(haystack.begin(), haystack.end(), needle) - haystack.begin();
}

int64_t get_cords(const vector<int64_t>& seq, const vector<int64_t>& buf) {
  int64_t answer = 0;
  int buf_index = find(seq, 0);
  int offset = find(buf, buf_index);
  for (int64_t i = 1; i <= 3; ++i)
    answer += seq[buf[aoc::mod(offset + i * 1000, buf.size())]];
  return answer;
}

int main(int argc, char *argv[]) {
  vector<int64_t> seq, buf;
  const auto& lines = aoc::input_lines(argc, argv);
  for (auto i = 0; i < lines.size(); ++i) {
    buf.push_back(i);
    seq.push_back(stoi(lines[i]));
  }

  // Part 1
  for (auto i = 0; i < seq.size(); ++i)
    move_element(buf, find(buf, i), seq[i]);
  aoc::output(get_cords(seq, buf));

  // Part 2
  constexpr int64_t key = 811589153;
  buf.clear();
  for (auto i = 0; i < seq.size(); ++i) {
    buf.push_back(i);
    seq[i] *= key;
  }
  for (auto mix = 0; mix < 10; ++mix)
    for (auto i = 0; i < seq.size(); ++i)
      move_element(buf, find(buf, i), seq[i]);
  aoc::output(get_cords(seq, buf));
}
