#include <fstream>

#include <nlohmann/json.hpp>

#include "../../lib/aoc.cpp"

using json = nlohmann::json;

int dfs(const json& data, int part) {
  int sum = 0;
  if (data.is_object()) {
    for (auto [_, elem] : data.items()) {
      if (part == 2 && elem == "red")
        return 0;
      sum += dfs(elem, part);
    }
  } else if (data.is_array()) {
    for (auto elem : data)
      sum += dfs(elem, part);
  } else if (data.is_number()) {
    sum = data;
  }
  return sum;
}

int main(int argc, char *argv[]) {
  std::ifstream f(argv[1]);
  json data = json::parse(f);
  aoc::output(dfs(data, 1));
  aoc::output(dfs(data, 2));
}
