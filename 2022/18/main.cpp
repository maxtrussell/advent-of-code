#include <string>
#include <unordered_set>
#include <vector>

#include "../aoc.cpp"

using namespace std;

struct Point {
  int x = 0;
  int y = 0;
  int z = 0;
};

struct BoundingBox {
  int min_x = 0, min_y = 0, min_z = 0;
  int max_x = 0, max_y = 0, max_z = 0;

  bool contains(Point p) const {
    return min_x <= p.x && min_y <= p.y && min_z <= p.z && max_x >= p.x &&
           max_y >= p.y && max_z >= p.z;
  }
};

using Graph = unordered_set<Point>;

Point operator+(const Point& a, const Point& b) {
  return {a.x + b.x, a.y + b.y, a.z + b.z};
}

bool operator==(const Point& a, const Point& b) {
  return a.x == b.x && a.y == b.y && a.z == b.z;
}

template <> struct std::hash<Point> {
  size_t operator()(const Point& p) const noexcept {
    size_t hash = 0;
    boost::hash_combine(hash, p.x);
    boost::hash_combine(hash, p.y);
    boost::hash_combine(hash, p.z);
    return hash;
  }
};

vector<Point> get_sides(Point pos) {
  const static vector<Point> deltas = {{1, 0, 0},  {-1, 0, 0}, {0, 1, 0},
                                       {0, -1, 0}, {0, 0, 1},  {0, 0, -1}};
  vector<Point> sides;
  for (const Point& delta : deltas)
    sides.push_back(pos + delta);
  return sides;
}

int dfs(const Graph& graph, Point pos, unordered_set<Point>& seen,
        const BoundingBox& box) {
  seen.insert(pos);
  int faces = 0;
  for (const Point& side : get_sides(pos)) {
    if (graph.count(side))
      faces += 1;
    else if (!seen.count(side) && box.contains(side))
      faces += dfs(graph, side, seen, box);
  }
  return faces;
}

int main(int argc, char *argv[]) {
  Graph graph;
  for (auto const& line : aoc::input_lines(argc, argv)) {
    auto it = line.begin();
    graph.insert({aoc::read_int(line, it), aoc::read_int(line, it),
                  aoc::read_int(line, it)});
  }

  // Part 1
  int faces = graph.size() * 6;
  for (Point p : graph)
    for (Point s : get_sides(p))
      faces -= graph.count(s);
  aoc::output(faces);

  // Part 2
  // Get bounding box and flood fill the air to count exposed faces
  int max_x = 0, max_y = 0, max_z = 0;
  for (Point p : graph) {
    max_x = max(max_x, p.x);
    max_y = max(max_y, p.y);
    max_z = max(max_z, p.z);
  }
  BoundingBox box{-1, -1, -1, max_x + 1, max_y + 1, max_z + 1};
  unordered_set<Point> seen;
  aoc::output(dfs(graph, {-1, -1}, seen, box));
}
