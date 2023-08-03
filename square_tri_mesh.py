
import argparse

import numpy as np

def gmsh_header():
    header = '''
$MeshFormat
2.2 0 8
$EndMeshFormat
$PhysicalNames
5
1 2 "periodic_0_l"
1 3 "periodic_1_l"
1 4 "periodic_0_r"
1 5 "periodic_1_r"
2 1 "fluid"
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
    # west
    for i in range(nx-1):
        nele += 1
        # elm-number elm-type reg-phys reg-elem number-of-nodes node-number-list
        n1 = i*nx + 1
        n2 = (i + 1)*nx + 1
        ele += f'{nele} 1 2 2 1 {n1} {n2}\n'

    # east
    for i in range(nx-1):
        nele += 1
        # elm-number elm-type reg-phys reg-elem number-of-nodes node-number-list
        n1 = (i + 1)*nx
        n2 = (i + 2)*nx
        ele += f'{nele} 1 2 4 3 {n1} {n2}\n'

    # south
    for i in range(nx-1):
        nele += 1
        # elm-number elm-type reg-phys reg-elem number-of-nodes node-number-list
        n1 = i + 1
        n2 = i + 2
        ele += f'{nele} 1 2 3 2 {n1} {n2}\n'

    # north
    for i in range(nx-1):
        nele += 1
        # elm-number elm-type reg-phys reg-elem number-of-nodes node-number-list
        n1 = (nx - 1)*nx + i + 1
        n2 = (nx - 1)*nx + i + 2
        ele += f'{nele} 1 2 5 4 {n1} {n2}\n'

    return nele, ele

def gmsh_elements(nx):
    nele, ele = gmsh_boundaries(nx)

    for j in range(nx - 1):
        for i in range(nx - 1):
            nele += 1
            n1 = j*nx + i + 1
            n2 = j*nx + i + 2
            n3 = (j + 1)*nx + i + 1
            ele += f'{nele} 2 2 1 3 {n1} {n2} {n3}\n'
            nele += 1
            n1 = j*nx + i + 2
            n2 = (j + 1)*nx + i + 2
            n3 = (j + 1)*nx + i + 1
            ele += f'{nele} 2 2 1 3 {n1} {n2} {n3}\n'

    return f'$Elements\n{nele}\n' + ele + '$EndElements\n'

def make_mesh(l, x0, nx):
    R = np.linspace(x0, x0 + l, nx)
    X = np.zeros((nx*nx, 3))

    for j,ry in enumerate(R):
        for i,rx in enumerate(R):
            X[j*nx+i,0] = rx
            X[j*nx+i,1] = ry
            X[j*nx+i,2] = 0.

    header = gmsh_header()
    nodes = gmsh_nodes(X)
    ele = gmsh_elements(nx)

    return header + nodes + ele


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Make tri based gmsh of square')
    parser.add_argument('-n', '--nx', dest='nx', type=int)
    parser.add_argument('-l', default=1, dest='l', type=float)
    parser.add_argument('-0', '--x0', default=0, dest='x0', type=float)

    args = parser.parse_args()

    nx = args.nx
    l = args.l
    x0 = args.x0
    msh = make_mesh(l, x0, nx + 1)

    f = open(f'rht_square_nx{nx}.msh', 'w')
    f.write(msh)