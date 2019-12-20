from quaternions import *
import torch
from utils import *
import numpy as np
from liegroups.torch import SO3
from sdp_layers import x_from_xxT

def test_rotmat_quat_conversions():
    print('Rotation matrix to quaternion conversions...')
    C1 = SO3.exp(torch.randn(100, 3, dtype=torch.double)).as_matrix()
    C2 = quat_to_rotmat(rotmat_to_quat(C1))
    assert(allclose(C1, C2))
    print('All passed.')
     
def test_rot_angles():
    print('Rotation angles...')
    C1 = SO3.exp(torch.randn(100, 3, dtype=torch.double))
    C2 = SO3.exp(torch.randn(100, 3, dtype=torch.double))

    angles_1 = (C1.dot(C2.inv())).log().norm(dim=1)*(180./np.pi)
    angles_2 = quat_angle_diff(rotmat_to_quat(C1.as_matrix()), rotmat_to_quat(C2.as_matrix()), units='deg', reduce=False)
    angles_3 = rotmat_angle_diff(C1.as_matrix(), C2.as_matrix(), reduce=False)
    assert(allclose(angles_1, angles_2))
    assert(allclose(angles_1, angles_3))
    print('All passed.')

def test_xxT():
    print('Testing x_from_xxT...')
    x = torch.randn(100, 10, dtype=torch.double)
    x[:,-1] = 1.
    X = outer(x, x)
    assert(allclose(x, x_from_xxT(X)))
    print('All passed.')

if __name__=='__main__':
    test_rotmat_quat_conversions()
    test_rot_angles()
    test_xxT()