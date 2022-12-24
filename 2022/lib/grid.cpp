#include <ostream>
#include <vector>

#include "point.cpp"

namespace aoc {
using namespace std;

template <typename T> class Grid {
public:
  Grid(const vector<string>& lines, bool diagonal = false)
      : diagonal_(diagonal) {
    for (const string& line : lines)
      // FIXME: Conditional logic based on T, e.g. call stoi if type is int.
      grid_.push_back(vector<T>(line.begin(), line.end()));
  }

  T operator[](Point p) const { return grid_[p.y][p.x]; }
  T& operator[](Point p) { return grid_[p.y][p.x]; }

  typename vector<vector<T>>::iterator begin() { return grid_.begin(); }
  typename vector<vector<T>>::iterator end() { return grid_.end(); }
  typename vector<vector<T>>::const_iterator begin() const {
    return grid_.cbegin();
  }
  typename vector<vector<T>>::const_iterator end() const {
    return grid_.cend();
  }

  bool in_bounds(Point p) const {
    return 0 <= p.y && p.y < grid_.size() && 0 <= p.x &&
           p.x < grid_[p.y].size();
  }
  vector<Point> get_neighbors(Point p) const {
    const static vector<Point> adjacents{{1, 0}, {0, 1}, {-1, 0}, {0, -1}};
    const static vector<Point> diagonals{{1, 1}, {1, -1}, {-1, 1}, {-1, -1}};

    vector<Point> neighbors;
    for (Point n : adjacents)
      if (in_bounds(p + n))
        neighbors.push_back(p + n);

    if (diagonal_)
      for (Point n : diagonals)
        if (in_bounds(p + n))
          neighbors.push_back(p + n);

    return neighbors;
  }

  int height() const { return grid_.size(); }
  int width() const { return grid_[0].size(); }

  // TODO: This would be better as an iterator.
  vector<Point> get_points() {
    vector<Point> points;
    for (int y = 0; y < grid_.size(); ++y)
      for (int x = 0; x < grid_[y].size(); ++x)
        points.push_back({x, y});
    return points;
  }

private:
  vector<vector<T>> grid_;
  bool diagonal_ = false;
};

template <typename T> ostream& operator<<(ostream& out, const Grid<T>& g) {
  for (const auto& row : g) {
    for (const auto& x : row)
      out << x;
    out << '\n';
  }
  return out;
}

} // namespace aoc
