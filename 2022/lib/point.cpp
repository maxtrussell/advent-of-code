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

struct Point {
  int x = 0, y = 0;

  /**
   * Returns a point rotated clockwise about 0,0.
   */
  Point rotate() { return {y, -x}; }

  /**
   * Returns a point rotated clockwise n times about 0,0.
   */
  Point rotate(int n) {
    Point rotated;
    for (int i = 0; i < n; ++i)
      rotated = rotate();
    return rotated;
  };

  Point rotate_about(Point center);
  Point rotate_about(Point center, int n);
};

ostream& operator<<(ostream& out, const Point& p) {
  return out << "Point{x: " << p.x << ", y: " << p.y << "}";
}

Point operator+(const Point& a, const Point& b) {
  return Point{a.x + b.x, a.y + b.y};
}

void operator+=(Point& a, const Point& b) {
  a.x += b.x;
  a.y += b.y;
}

Point operator-(const Point& a, const Point& b) {
  return Point{a.x - b.x, a.y - b.y};
}

bool operator>(const Point& a, const Point& b) {
  return a.x > b.x && a.y > b.y;
}

bool operator>=(const Point& a, const Point& b) {
  return a.x >= b.x && a.y >= b.y;
}

bool operator<(const Point& a, const Point& b) {
  return a.x < b.x && a.y < b.y;
}

bool operator<=(const Point& a, const Point& b) {
  return a.x <= b.x && a.y <= b.y;
}

bool operator==(const Point& a, const Point& b) {
  return a.x == b.x && a.y == b.y;
}

bool operator!=(const Point& a, const Point& b) { return !(a == b); }

Point Point::rotate_about(Point center) {
  Point relative = *this - center;
  relative = relative.rotate();
  return relative + center;
}

Point Point::rotate_about(Point center, int n) {
  Point rotated;
  for (int i = 0; i < n; ++i)
    rotated = rotated.rotate_about(center);
  return rotated;
}

struct Rect {
  Point min_;
  Point max_;

  Rect(Point min, Point max) : min_(min), max_(max) {}
  Rect(Point min, int width, int height) : min_(min) {
    max_ = min + Point{width - 1, height - 1};
  }
  int area() { return (max_.x - min_.x + 1) * (max_.y - min_.y + 1); }
  bool contains(Point p) const { return min_ <= p && p <= max_; }
};

} // namespace aoc

template <> struct std::hash<aoc::Point> {
  size_t operator()(const aoc::Point& p) const noexcept {
    size_t hash = 0;
    boost::hash_combine(hash, p.x);
    boost::hash_combine(hash, p.y);
    return hash;
  }
};
