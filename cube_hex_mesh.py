
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
    for i1 in range(nx-1):
        for i2 in range(nx-1):
            # i=0
            nele += 1
            n = [(i1 + 0)*nx*nx + (i2 + 0)*nx + 1, (i1 + 0)*nx*nx + (i2 + 1)*nx + 1,
                 (i1 + 1)*nx*nx + (i2 + 1)*nx + 1, (i1 + 1)*nx*nx + (i2 + 0)*nx + 1]
            # Id Type NumTags PhysGrp ElemGrp IndexList
            n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
            ele += f'{nele} 3 2 2 2 {n_str}\n'

            # i=nx-1
            nele += 1
            n = [(i1 + 0)*nx*nx + (i2 + 0)*nx + nx, (i1 + 0)*nx*nx + (i2 + 1)*nx + nx,
                 (i1 + 1)*nx*nx + (i2 + 1)*nx + nx, (i1 + 1)*nx*nx + (i2 + 0)*nx + nx]
            # Id Type NumTags PhysGrp ElemGrp IndexList
            n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
            ele += f'{nele} 3 2 5 5 {n_str}\n'

            # j=0
            nele += 1
            n = [(i1 + 0)*nx*nx + i2 + 1, (i1 + 0)*nx*nx + i2 + 2,
                 (i1 + 1)*nx*nx + i2 + 2, (i1 + 1)*nx*nx + i2 + 1]
            # Id Type NumTags PhysGrp ElemGrp IndexList
            n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
            ele += f'{nele} 3 2 3 3 {n_str}\n'

            # j=nx-1
            nele += 1
            n = [(i1 + 0)*nx*nx + (nx - 1)*nx + i2 + 1, (i1 + 0)*nx*nx + (nx - 1)*nx + i2 + 2,
                 (i1 + 1)*nx*nx + (nx - 1)*nx + i2 + 2, (i1 + 1)*nx*nx + (nx - 1)*nx + i2 + 1]
            # Id Type NumTags PhysGrp ElemGrp IndexList
            n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
            ele += f'{nele} 3 2 6 6 {n_str}\n'

            # k=0
            nele += 1
            n = [(i1 + 0)*nx + i2 + 1, (i1 + 1)*nx + i2 + 1,
                 (i1 + 1)*nx + i2 + 2, (i1 + 0)*nx + i2 + 2]
            # Id Type NumTags PhysGrp ElemGrp IndexList
            n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
            ele += f'{nele} 3 2 4 4 {n_str}\n'

            # k=nx-1
            nele += 1
            n = [(nx - 1)*nx*nx + (i1 + 0)*nx + i2 + 1, (nx - 1)*nx*nx + (i1 + 1)*nx + i2 + 1,
                 (nx - 1)*nx*nx + (i1 + 1)*nx + i2 + 2, (nx - 1)*nx*nx + (i1 + 0)*nx + i2 + 2]
            # Id Type NumTags PhysGrp ElemGrp IndexList
            n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
            ele += f'{nele} 3 2 7 7 {n_str}\n'
    
    return nele, ele

def gmsh_elements(nx):
    nele, ele = gmsh_boundaries(nx)

    # elm-number elm-type number-of-tags < tag > … node-number-list
    for k in range(nx - 1):
        for j in range(nx - 1):
            for i in range(nx - 1):
                nele += 1
                n = [k*nx*nx + j*nx + i + 1, k*nx*nx + j*nx + i + 2, 
                     k*nx*nx + (j + 1)*nx + i + 2, k*nx*nx + (j + 1)*nx + i + 1,
                     (k + 1)*nx*nx + j*nx + i + 1, (k + 1)*nx*nx + j*nx + i + 2,
                     (k + 1)*nx*nx + (j + 1)*nx + i + 2, (k + 1)*nx*nx + (j + 1)*nx + i + 1]
                n_str = ' '.join('{ni}'.format(ni=ni) for ni in n)
                ele += f'{nele} 5 2 1 1 {n_str} \n'

    return f'$Elements\n{nele}\n' + ele + '$EndElements\n'

def make_mesh(l, x0, nx):
    R = np.linspace(x0, x0 + l, nx)
    X = np.zeros((nx*nx*nx, 3))

    for k, rz in enumerate(R):
        for j, ry in enumerate(R):
            for i, rx in enumerate(R):
                X[k*nx*nx + j*nx + i,0] = rx
                X[k*nx*nx + j*nx + i,1] = ry
                X[k*nx*nx + j*nx + i,2] = rz
    
    header = gmsh_header()
    nodes = gmsh_nodes(X)
    ele = gmsh_elements(nx)

    return header + nodes + ele


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Make hex based gmsh of cube')
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
