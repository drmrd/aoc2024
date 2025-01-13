# Advent of Code 2024 in Pure Python
This repository includes solutions to all twenty-five Advent of Code 2024
puzzles written in Python. To make things interesting, I elected to (a) not use
any third-party packages to solve problems while (b) building out a few shared
data structures and path-finding algorithms that could be re-used throughout the
month. This proved to be a fun challenge that largely boiled down to
implementing simple vectors, creating graph data structures with a heavy nod to
NetworkX's API (or at least my memory of NetworkX's API), and variants of A*
and Dijkstra algorithms. This led to code that was reasonably performany,
readable, and for the most part well-tested.

The only direct dependencies are
- [advent-of-code-data](https://github.com/wimglenn/advent-of-code-data) to
  fetch and cache puzzle inputs and
- [pygame](https://github.com/pygame/pygame) to create a basic visualized on
  that one day in mid-December when my nieces asked me what I was working on.
- [tqdm](https://github.com/tqdm/tqdm) for progress bars on a few sluggish
  solutions (and its [stub package](https://pypi.org/project/types-tqdm/).
- Standard testing and SCA fare (pytest, mypy, and hypothesis).
