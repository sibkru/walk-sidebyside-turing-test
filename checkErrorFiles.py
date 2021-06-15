# Script prints ELBOs auf all dyn lvm error.pkl Files to ensure they have an ELBO
from glob import glob
import pickle
import numpy
for fn in glob('bvh/generated/*-dyn(*)-lvm(*)*/errors.pkl'):
    print(fn)
    with open(fn, "rb") as f:
        u = pickle._Unpickler(f)
        u.encoding = 'latin1'
        p = u.load()
        print(p["ELBO"])
