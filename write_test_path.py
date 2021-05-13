# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
import ProcessMVNX
import numpy as np
import ProcessMVNX.bvh_import as bvh
from numpy import cos, sin
import matplotlib.pyplot as plt
from transforms3d import euler

from functools import partial

hom_unit = np.array([[0, 0, 0, 1]]).T


def Yrot(a):
    return np.array([[cos(a), 0, sin(a)], [0, 1, 0], [-sin(a), 0, cos(a)]])


def Xrot(a):
    return np.array([[1, 0, 0], [0, cos(a), -sin(a)], [0, sin(a), cos(a)]])


def Zrot(a):
    return np.array([[cos(a), -sin(a), 0], [sin(a), cos(a), 0], [0, 0, 1]])


def rotation_matrix(angles):
    angles = angles * np.pi / 180
    z, x, y = angles[0], angles[1], angles[2]
    R = np.eye(4)
    R[:3, :3] = Zrot(z).dot(Xrot(x).dot(Yrot(y)))
    return R


def translation_matrix(v):
    T = np.eye(4)
    T[:3, 3] = v.flatten()
    return T


def pair_list(skel_node, cumlist=[]):
    if not skel_node.children:
        return cumlist
    else:
        for child in skel_node.children:
            cumlist = cumlist + pair_list(child, cumlist)[1:]
            cumlist.append(
                (skel_node.name, child.name)
            )
    return cumlist



class MotionProcesser:
    def __init__(self, skeleton, motion):
        self.motion = motion
        self.joint_idx = {s.name: slice((j + 1) * 3, (j + 2) * 3) for j, s in enumerate(skeleton)}

    def add_offset(self, segment, cumdict, t):
        """
        This method converts joint angles to positions.
        returns dictionary `cumdict` with all positions.
        """
        pose = self.motion[t]
        if segment.parent:
            parent = segment.parent.name
            joint = segment.name
            Mprev, pos = cumdict[parent]

            v = segment.offset[:, None]
            R = rotation_matrix(pose[self.joint_idx[joint]])
            T = translation_matrix(v)
            M = T.dot(R)

            M = Mprev.dot(M)
            position = M.dot(hom_unit)[:3]
            cumdict[joint] = (M, position)
        else:
            v = pose[:3]
            R = rotation_matrix(pose[self.joint_idx["pelvis"]])
            T = translation_matrix(v)
            M = T.dot(R)
            position = M.dot(hom_unit)[:3]
            cumdict["pelvis"] = (M, position)

        if segment.end_site is not None:
            return cumdict

        for child in segment.children:
            cumdict = {**cumdict, **self.add_offset(child, cumdict, t)}
        return cumdict


all_joints = [
    "pelvis",
    "pelvis_right_femur",
    "right_femur_tibia",
    "right_tibia_foot",
    "pelvis_left_femur",
    "left_femur_tibia",
    "left_tibia_foot",
    "pelvis_spine1",
    "spine1",
    "spine2",
    "neck",
    "right_manubrium",
    "right_clavicle",
    "right_humerus",
    "right_radius",
    "left_manubrium",
    "left_clavicle",
    "left_humerus",
    "left_radius",
]

round3 = partial(round, ndigits=3)
scale = lambda x: x / 10
process = lambda x: str(round3(scale(x)))

def convert_bvh(fn_in, fn_out='path.txt'):
    skeleton = bvh.parse_bvh(bvh.read_file(fn_in))
    skdict = {s.name: s for s in skeleton}
    pairs = pair_list(skeleton[0])
    pairs += [
        ('right_femur_tibia', 'right_tibia_foot'),
        ('pelvis_right_femur', 'right_femur_tibia')
    ]
    pairs = set(pairs)
    pairs.remove(('spine1', 'right_manubrium'))
    pairs.remove(('spine1', 'left_manubrium'))

    joints, pelvis = bvh.read_bvh_motion(fn_in)
    '''for j in range(len(joints)):
        for i in range(0,9):
            joints[j][i] = joints[j][i+9] '''
    motion = np.concatenate((pelvis, joints), axis=1)

    mp = MotionProcesser(skeleton, motion)

    lst = []
    for t in range(len(motion)):
        cd = mp.add_offset(skeleton[0], {}, t)
        # Positions of all joints in one big list
        c3d = np.array([cd[k][1][:3].T for k in all_joints]).flatten()
        # 96 entries: 
        c3d = np.array([
            np.concatenate((cd[a][1][:3].T, cd[b][1][:3].T), axis=1)
            for a, b in pairs
        ]).flatten()
        lst.append(c3d)
    P = np.array(lst)

    # write GL-LINES specific data format
    s = "" # TODO: use dictionary `pairs` to write header for *-lines.txt files"

    # "pelvis-x;pelvis-y;pelvis-z;pelvis_right_femur-x;pelvis_right_femux-y;..."
    header_list = []
    for start, end in pairs:
        for point in [start, end]:
            for coord in ["x", "y", "z"]:
                header_list.append(str(point) + '-' + coord)
    s = ";".join(header_list) + '\n'

    for line in P:
        for _ in range(1):
            s += ";".join(map(process, list(line)))
            s = s + "\n"
    with open(fn_out, "w") as fo:
        fo.write(s)


if __name__ == '__main__':
    from glob import glob
    import os
    bvh_files = glob('/home/sib/git/walk-sidebyside-turing-test/bvh/mocap/newMocapBVHs/*.bvh')
    fn =  "bvh/mocap.bvh"
    out_fn = fn.split('.')[0]+'-lines-attention-check.txt'
    for i in range(len(bvh_files)):
        out_fn = '/home/sib/git/walk-sidebyside-turing-test/bvh/mocap/newMocapBVHs/clip' + str(i) + '.txt'
        convert_bvh(bvh_files[i], out_fn)
    """ for fn in glob('bvh/generated/*/*.bvh'):
        out_fn = fn.split('.')[0]+'-lines.txt'
        if recompute:
            print('reconverting', out_fn)
            convert_bvh(fn, out_fn)
        elif os.path.exists(out_fn):
            print(out_fn.split('/')[-2], 'exists, skipping.', end=' ')
        else:
            print('converting', out_fn)
            convert_bvh(fn, out_fn) """