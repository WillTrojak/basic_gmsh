
import argparse
from math import pi

import numpy as np

def gmsh_header():
    header = '''
$MeshFormat
2.2 0 8
$EndMeshFormat
$PhysicalNames
7
3 1 "fluid"
2 2 "periodic_0_l"
2 3 "periodic_1_l"
2 4 "periodic_2_l"
2 5 "periodic_0_r"
2 6 "periodic_1_r"
2 7 "periodic_2_r"
$EndPhysicalNames
'''
    return header

def gmsh_nodes(X):
    data = f'$Nodes\n{len(X)}\n'
    for i,x in enumerate(X):
        data += f'{i+1} ' + ' '.join(str(z) for z in x) + '\n'
    data += '$EndNodes\n'
    return data

def gmsh_boundaries(nx, nele = 0):
    ele = ''

    ind = lambda i, j, k: grid_i(nx, nx, i, j, k)
    for i1 in range(nx-1):
        for i2 in range(nx-1):
            # WEST 1: i=0
            nele += 1
            n = [ind(0, i2+0, i1+0),
                 ind(0, i2+1, i1+0),
                 ind(0, i2+0, i1+1)]
            # Id Type NumTags PhysGrp ElemGrp IndexList
            n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
            ele += f'{nele} 2 2 2 2 {n_str}\n'

            # WEST 2: i=0
            nele += 1
            n = [ind(0, i2+0, i1+1),
                 ind(0, i2+1, i1+0),
                 ind(0, i2+1, i1+1)]
            # Id Type NumTags PhysGrp ElemGrp IndexList
            n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
            ele += f'{nele} 2 2 2 2 {n_str}\n'

            # EAST 1: i=nx-1
            nele += 1
            n = [ind(nx-1, i2+0, i1+0),
                 ind(nx-1, i2+0, i1+1),
                 ind(nx-1, i2+1, i1+0)]
            # Id Type NumTags PhysGrp ElemGrp IndexList
            n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
            ele += f'{nele} 2 2 5 5 {n_str}\n'

            # EAST 2: i=nx-1
            nele += 1
            n = [ind(nx-1, i2+0, i1+1),
                 ind(nx-1, i2+1, i1+1),
                 ind(nx-1, i2+1, i1+0)]
            # Id Type NumTags PhysGrp ElemGrp IndexList
            n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
            ele += f'{nele} 2 2 5 5 {n_str}\n'

            # SOUTH 1: j=0
            nele += 1
            n = [ind(i2+0, 0, i1+0),
                 ind(i2+0, 0, i1+1),
                 ind(i2+1, 0, i1+0)]
            # Id Type NumTags PhysGrp ElemGrp IndexList
            n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
            ele += f'{nele} 2 2 3 3 {n_str}\n'

            # SOUTH 2: j=0
            nele += 1
            n = [ind(i2+1, 0, i1+0),
                 ind(i2+0, 0, i1+1),
                 ind(i2+1, 0, i1+1)]
            # Id Type NumTags PhysGrp ElemGrp IndexList
            n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
            ele += f'{nele} 2 2 3 3 {n_str}\n'

            # NORTH 1: j=nx-1
            nele += 1
            n = [ind(i2+0, nx-1, i1+0),
                 ind(i2+1, nx-1, i1+0),
                 ind(i2+0, nx-1, i1+1)]
            # Id Type NumTags PhysGrp ElemGrp IndexList
            n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
            ele += f'{nele} 2 2 6 6 {n_str}\n'

            # NORTH 2: j=nx-1
            nele += 1
            n = [ind(i2+1, nx-1, i1+0),
                 ind(i2+1, nx-1, i1+1),
                 ind(i2+0, nx-1, i1+1)]
            # Id Type NumTags PhysGrp ElemGrp IndexList
            n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
            ele += f'{nele} 2 2 6 6 {n_str}\n'

            # BOTTOM 1: k=0
            nele += 1
            n = [ind(i2+0, i1+0, 0),
                 ind(i2+1, i1+0, 0),
                 ind(i2+0, i1+1, 0)]
            # Id Type NumTags PhysGrp ElemGrp IndexList
            n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
            ele += f'{nele} 2 2 4 4 {n_str}\n'

            # BOTTOM 2: k=0
            nele += 1
            n = [ind(i2+1, i1+0, 0),
                 ind(i2+1, i1+1, 0),
                 ind(i2+0, i1+1, 0)]
            # Id Type NumTags PhysGrp ElemGrp IndexList
            n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
            ele += f'{nele} 2 2 4 4 {n_str}\n'

            # TOP 1: k=nx-1
            nele += 1
            n = [ind(i2+0, i1+0, nx-1),
                 ind(i2+0, i1+1, nx-1),
                 ind(i2+1, i1+0, nx-1)]
            # Id Type NumTags PhysGrp ElemGrp IndexList
            n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
            ele += f'{nele} 2 2 7 7 {n_str}\n'

            # TOP 2: k=nx-1
            nele += 1
            n = [ind(i2+1, i1+0, nx-1),
                 ind(i2+0, i1+1, nx-1),
                 ind(i2+1, i1+1, nx-1)]
            # Id Type NumTags PhysGrp ElemGrp IndexList
            n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
            ele += f'{nele} 2 2 7 7 {n_str}\n'

    return nele, ele

def gmsh_elements(nx):
    nele, ele = gmsh_boundaries(nx)
    moff = nx*nx*nx

    ind = lambda i, j, k: grid_i(nx, nx, i, j, k)
    mind = lambda i, j, k: moff + grid_i(nx-1, nx-1, i, j, k)

    # elm-number elm-type number-of-tags < tag > … node-number-list
    for k in range(nx - 1):
        for j in range(nx - 1):
            for i in range(nx - 1):
                # Bottom 1
                nele += 1
                n = [ind(i+0, j+0, k+0),
                     ind(i+1, j+0, k+0),
                     ind(i+0, j+1, k+0),
                     mind(i, j, k)]
                n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                ele += f'{nele} 4 2 1 1 {n_str} \n'

                # Bottom 2
                nele += 1
                n = [ind(i+1, j+0, k+0),
                     ind(i+1, j+1, k+0),
                     ind(i+0, j+1, k+0),
                     mind(i, j, k)]
                n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                ele += f'{nele} 4 2 1 1 {n_str} \n'

                # Top 1
                nele += 1
                n = [ind(i+0, j+0, k+1),
                     ind(i+0, j+1, k+1),
                     ind(i+1, j+0, k+1),
                     mind(i, j, k)]
                n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                ele += f'{nele} 4 2 1 1 {n_str} \n'

                # Top 2
                nele += 1
                n = [ind(i+1, j+0, k+1),
                     ind(i+0, j+1, k+1),
                     ind(i+1, j+1, k+1),
                     mind(i, j, k)]
                n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                ele += f'{nele} 4 2 1 1 {n_str} \n'

                # East 1
                nele += 1
                n = [ind(i+1, j+0, k+0),
                     ind(i+1, j+0, k+1),
                     ind(i+1, j+1, k+0),
                     mind(i, j, k)]
                n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                ele += f'{nele} 4 2 1 1 {n_str} \n'

                # East 2
                nele += 1
                n = [ind(i+1, j+0, k+1),
                     ind(i+1, j+1, k+1),
                     ind(i+1, j+1, k+0),
                     mind(i, j, k)]
                n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                ele += f'{nele} 4 2 1 1 {n_str} \n'

                # West 1
                nele += 1
                n = [ind(i+0, j+0, k+0),
                     ind(i+0, j+1, k+0),
                     ind(i+0, j+0, k+1),
                     mind(i, j, k)]
                n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                ele += f'{nele} 4 2 1 1 {n_str} \n'

                # West 2
                nele += 1
                n = [ind(i+0, j+0, k+1),
                     ind(i+0, j+1, k+0),
                     ind(i+0, j+1, k+1),
                     mind(i, j, k)]
                n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                ele += f'{nele} 4 2 1 1 {n_str} \n'

                # South 1
                nele += 1
                n = [ind(i+0, j+0, k+0),
                     ind(i+0, j+0, k+1),
                     ind(i+1, j+0, k+0),
                     mind(i, j, k)]
                n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                ele += f'{nele} 4 2 1 1 {n_str} \n'

                # South 2
                nele += 1
                n = [ind(i+1, j+0, k+0),
                     ind(i+0, j+0, k+1),
                     ind(i+1, j+0, k+1),
                     mind(i, j, k)]
                n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                ele += f'{nele} 4 2 1 1 {n_str} \n'

                # North 1
                nele += 1
                n = [ind(i+0, j+1, k+0),
                     ind(i+1, j+1, k+0),
                     ind(i+0, j+1, k+1),
                     mind(i, j, k)]
                n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                ele += f'{nele} 4 2 1 1 {n_str} \n'

                # North 2
                nele += 1
                n = [ind(i+1, j+1, k+0),
                     ind(i+1, j+1, k+1),
                     ind(i+0, j+1, k+1),
                     mind(i, j, k)]
                n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                ele += f'{nele} 4 2 1 1 {n_str} \n'

    return f'$Elements\n{nele}\n' + ele + '$EndElements\n'

def grid_i(nx, ny, i, j, k):
    return k*nx*ny + j*nx + i + 1

def make_mesh(l, x0, nx):
    R = np.linspace(x0, x0 + l, nx)
    dx = R[1] - R[0]
    M = np.linspace(x0 + 0.5*dx, x0 + l - 0.5*dx, nx-1)
    X = np.zeros((nx*nx*nx + (nx-1)*(nx-1)*(nx-1), 3))

    i = 0
    for rz in R:
        for ry in R:
            for rx in R:
                X[i,:] = [rx, ry, rz]
                i += 1

    for mz in M:
        for my in M:
            for mx in M:
                X[i,:] = [mx, my, mz]
                i += 1

    header = gmsh_header()
    nodes = gmsh_nodes(X)
    ele = gmsh_elements(nx)

    return header + nodes + ele


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Make tet based gmsh of cube')
    parser.add_argument('-n', '--nx', dest='nx', type=int)
    parser.add_argument('-l', default=1, dest='l', type=float)
    parser.add_argument('-0', '--x0', default=0, dest='x0', type=float)

    args = parser.parse_args()

    nx = args.nx
    l = args.l
    x0 = args.x0
    msh = make_mesh(l, x0, nx + 1)

    f = open(f'cube_nx{nx}.msh', 'w')
    f.write(msh)


