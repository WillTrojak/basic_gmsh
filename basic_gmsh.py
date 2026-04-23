import argparse

from cube_hex_mesh import make_mesh as make_hex
from cube_tet_mesh import make_mesh as make_tet
from cube_pyr_mesh import make_mesh as make_pyr
from cube_pri_mesh import make_mesh as make_pri
from square_tri_mesh import make_mesh as make_tri
from square_quad_mesh import make_mesh as make_quad

elements = {
    'hex': ('cube', make_hex),
    'tet': ('cube', make_tet),
    'pyr': ('cube', make_pyr),
    'pri': ('cube', make_pri),
    'tri': ('square', make_tri),
    'quad': ('square', make_quad),
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a gmsh mesh')
    parser.add_argument('-e', '--element', required=True,
                        choices=elements.keys())
    parser.add_argument('-n', '--nx', required=True, dest='nx', type=int)
    parser.add_argument('-l', default=1, dest='l', type=float)
    parser.add_argument('-0', '--x0', default=0, dest='x0', type=float)

    args = parser.parse_args()

    shape, make = elements[args.element]
    msh = make(args.l, args.x0, args.nx + 1)

    fname = f'{shape}_{args.element}_nx{args.nx}.msh'
    with open(fname, 'w') as f:
        f.write(msh)
