#include <algorithm>
#include <iterator>
#include <string>
#include <unordered_map>
#include <vector>

#include "../aoc.cpp"

using namespace std;

//     +---+---+
//     | 0 | 1 |
//     +---+---+
//     | 2 |
// +---+---+
// | 4 | 3 |
// +---+---+
// | 5 |
// +---+

enum Direction { Right, Down, Left, Up };
enum class Navigation { Flat, Cube };
const vector<aoc::Point> Deltas = {{1, 0}, {0, 1}, {-1, 0}, {0, -1}};

constexpr int F = 50;
// constexpr int F = 4;  // Used for testing with mini.txt
vector<aoc::Rect> Faces{
    aoc::Rect(aoc::Point{F, 0}, F, F),     // Face 0
    aoc::Rect(aoc::Point{2 * F, 0}, F, F), // Face 1
    aoc::Rect(aoc::Point{F, F}, F, F),     // Face 2
    aoc::Rect(aoc::Point{F, 2 * F}, F, F), // Face 3
    aoc::Rect(aoc::Point{0, 2 * F}, F, F), // Face 4
    aoc::Rect(aoc::Point{0, 3 * F}, F, F)  // Face 5
};
vector<vector<pair<int, int>>> FaceLinks{
    {{1, Right}, {2, Down}, {4, Right}, {5, Right}}, // Face 0
    {{3, Left}, {2, Left}, {0, Left}, {5, Up}},      // Face 1
    {{1, Up}, {3, Down}, {4, Down}, {0, Up}},        // Face 2
    {{1, Left}, {5, Left}, {4, Left}, {2, Up}},      // Face 3
    {{3, Right}, {5, Down}, {0, Right}, {2, Right}}, // Face 4
    {{3, Up}, {1, Down}, {0, Down}, {4, Up}}         // Face 5
};

// {x flips, y flips, rots}
vector<vector<tuple<int, int, int>>> RotsAndFlipsRequired{
    {{-1, -1, -1}, {-1, -1, -1}, {0, 1, 0}, {0, 1, 3}}, // Face 0
    {{0, 1, 0}, {0, 1, 3}, {-1, -1, -1}, {1, 0, 2}},    // Face 1
    {{1, 0, 1}, {-1, -1, -1}, {1, 0, 1}, {-1, -1, -1}}, // Face 2
    {{0, 1, 0}, {0, 1, 3}, {-1, -1, -1}, {-1, -1, -1}}, // Face 3
    {{-1, -1, -1}, {-1, -1, -1}, {0, 1, 0}, {0, 1, 3}}, // Face 4
    {{1, 0, 1}, {1, 0, 2}, {1, 0, 1}, {-1, -1, -1}}     // Face 5
};

struct Move {
  int turn = 0;
  int delta = 0;

  Move(int dist) : delta(dist) {}
  Move(int dir, int dist) : delta(dist) { turn = dir == 'R' ? 1 : -1; }
};

struct Cursor {
  aoc::Point pos;
  int dir = 0;
  Navigation mode = Navigation::Flat;
};

int get_face(aoc::Point p) {
  for (int face = 0; face < Faces.size(); ++face) {
    aoc::Rect rect = Faces[face];
    if (rect.contains(p))
      return face;
  }
  assert(false && "unreachable");
}

/**
 * Rotate a point about the face of a n sized cube.
 */
aoc::Point rotate(const aoc::Point p, int times, int n) {
  aoc::Point rotated = p;
  for (int i = 0; i < times; ++i) {
    int x1 = (n - 1) - rotated.y;
    int y1 = rotated.x;
    rotated = aoc::Point{x1, y1};
  }
  return rotated;
}

// Perform a x/y flip on an n-sized square.
int flip(int x, int n) { return (n - 1) - x; }

void cube_wrap(const vector<vector<char>>& graph, const Cursor& cursor,
               aoc::Point& next, int& next_dir) {
  int curr_face = get_face(cursor.pos);

  auto n = FaceLinks[curr_face][cursor.dir];
  int next_face = n.first;
  next_dir = n.second;

  // We have the next face we now need to rotate+translate our point.
  aoc::Point relative = cursor.pos - Faces[curr_face].min_;

  auto [xflip, yflip, rots] = RotsAndFlipsRequired[curr_face][cursor.dir];
  assert(xflip != -1 && yflip != -1 && rots != -1);

  // Do the rotation(s). A point relative to the face is requried.
  relative = rotate(relative, rots, F);

  // Do the flips
  if (xflip)
    relative.x = flip(relative.x, F);
  if (yflip)
    relative.y = flip(relative.y, F);

  // Do the translation to the next face
  next = relative + Faces[next_face].min_;
}

bool need_wrap(const vector<vector<char>>& graph, aoc::Point p) {
  bool out_of_bounds =
      p.y < 0 || p.y >= graph.size() || p.x < 0 || p.x >= graph[p.y].size();
  return out_of_bounds || graph[p.y][p.x] == ' ';
}

void do_wrap(const vector<vector<char>>& graph, aoc::Point& p, Cursor& cursor) {
  p.y = aoc::mod(p.y, graph.size());
  p.x = aoc::mod(p.x, graph[p.y].size());
  while (graph[p.y][p.x] == ' ') {
    p += Deltas[cursor.dir];
    p.y = aoc::mod(p.y, graph.size());
    p.x = aoc::mod(p.x, graph[p.y].size());
  }
}

void do_move(const vector<vector<char>>& graph, Cursor& cursor, Move move) {
  for (int i = 0; i < move.delta; ++i) {
    aoc::Point next = cursor.pos + Deltas[cursor.dir];
    int next_dir = cursor.dir;
    if (need_wrap(graph, next)) {
      if (cursor.mode == Navigation::Cube)
        cube_wrap(graph, cursor, next, next_dir);
      else
        do_wrap(graph, next, cursor);
    }

    if (graph[next.y][next.x] == '#')
      break;

    cursor.pos = next;
    cursor.dir = next_dir;
  }
  cursor.dir = aoc::mod(cursor.dir + move.turn, 4);
}

int main(int argc, char *argv[]) {
  vector<vector<char>> graph;
  vector<string> lines = aoc::input_lines(argc, argv);
  vector<Move> moves;
  bool parsed_map = false;
  for (size_t i = 0; i < lines.size(); ++i) {
    if (!lines[i].length()) {
      parsed_map = true;
      continue;
    }

    if (!parsed_map) {
      vector<char> row(lines[i].begin(), lines[i].end());
      graph.push_back(move(row));
    } else {
      auto it = lines[i].cbegin();
      int delta = aoc::read_int(it);
      while (it != lines[i].end()) {
        char turn = *it++;
        moves.push_back(Move(turn, delta));
        delta = aoc::read_int(it);
      }
      moves.push_back(Move(delta));
    }
  }

  // Get starting position
  int x = aoc::index_of(graph[0], '.');
  aoc::Point start{x, 0};

  for (Navigation mode : {Navigation::Flat, Navigation::Cube}) {
    Cursor cursor{start, Right, mode};
    for (Move m : moves)
      do_move(graph, cursor, m);

    int ans = 1000 * (cursor.pos.y + 1) + 4 * (cursor.pos.x + 1) + cursor.dir;
    aoc::output(ans);
  }
}
