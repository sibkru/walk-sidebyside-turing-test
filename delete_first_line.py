from glob import glob

bvh_files = glob('/home/sib/git/walk-sidebyside-turing-test/bvh/mocap/newMocapBVHs/*.txt')

for file in bvh_files:
    f = open(file, 'r')
    lines = f.readlines()
    f.close()
    lines = lines[1:]
    f = open(file, 'w')
    f.writelines(lines)
    f.close()

