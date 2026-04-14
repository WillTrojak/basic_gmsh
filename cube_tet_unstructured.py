import argparse
from math import pi


def make_geo(l, x0, n):
    lc = l / n

    return f"""\
// Unstructured tet mesh of a cube [{x0}, {x0 + l}]^3
// Periodic in x, y, and z for PyFR

L = {l};
x0 = {x0};
lc = {lc};

// Points
Point(1) = {{x0, x0, x0, lc}};
Point(2) = {{x0 + L, x0, x0, lc}};
Point(3) = {{x0 + L, x0 + L, x0, lc}};
Point(4) = {{x0, x0 + L, x0, lc}};
Point(5) = {{x0, x0, x0 + L, lc}};
Point(6) = {{x0 + L, x0, x0 + L, lc}};
Point(7) = {{x0 + L, x0 + L, x0 + L, lc}};
Point(8) = {{x0, x0 + L, x0 + L, lc}};

// Lines (bottom face)
Line(1) = {{1, 2}};
Line(2) = {{2, 3}};
Line(3) = {{3, 4}};
Line(4) = {{4, 1}};

// Lines (top face)
Line(5) = {{5, 6}};
Line(6) = {{6, 7}};
Line(7) = {{7, 8}};
Line(8) = {{8, 5}};

// Vertical lines
Line(9)  = {{1, 5}};
Line(10) = {{2, 6}};
Line(11) = {{3, 7}};
Line(12) = {{4, 8}};

// Surfaces
Curve Loop(1) = {{1, 2, 3, 4}};
Plane Surface(1) = {{1}};

Curve Loop(2) = {{5, 6, 7, 8}};
Plane Surface(2) = {{2}};

Curve Loop(3) = {{1, 10, -5, -9}};
Plane Surface(3) = {{3}};

Curve Loop(4) = {{3, 12, -7, -11}};
Plane Surface(4) = {{4}};

Curve Loop(5) = {{4, 9, -8, -12}};
Plane Surface(5) = {{5}};

Curve Loop(6) = {{2, 11, -6, -10}};
Plane Surface(6) = {{6}};

// Volume
Surface Loop(1) = {{1, 2, 3, 4, 5, 6}};
Volume(1) = {{1}};

// Physical groups for PyFR
Physical Surface("periodic_0_l") = {{5}};
Physical Surface("periodic_0_r") = {{6}};
Physical Surface("periodic_1_l") = {{3}};
Physical Surface("periodic_1_r") = {{4}};
Physical Surface("periodic_2_l") = {{1}};
Physical Surface("periodic_2_r") = {{2}};
Physical Volume("fluid") = {{1}};

// Periodicity
Periodic Surface {{6}} = {{5}} Translate {{L, 0, 0}};
Periodic Surface {{4}} = {{3}} Translate {{0, L, 0}};
Periodic Surface {{2}} = {{1}} Translate {{0, 0, L}};
"""


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a Gmsh .geo file for an unstructured tet cube mesh"
    )
    parser.add_argument("-n", "--nx", required=True, type=int)
    parser.add_argument("-l", default=2 * pi, type=float)
    parser.add_argument("-0", "--x0", default=0, type=float)
    parser.add_argument("-q", "--quiet", action="store_true")

    args = parser.parse_args()

    geo = make_geo(args.l, args.x0, args.nx)

    filename = f"cube_tet_nx{args.nx}.geo"
    with open(filename, "w") as f:
        f.write(geo)

    if not args.quiet:
        print(f"Wrote: {filename}\n"
              f"Now run:\ngmsh -3 -optimize -format msh22 -order 0 {filename}")
