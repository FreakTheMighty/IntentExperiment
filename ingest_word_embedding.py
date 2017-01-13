import sys
import h5py
import hashlib
import numpy as np
f = h5py.File("data/word_embeddint.hdf5", "w")

for p in sys.argv[1:]:
    with open(p) as word_file:
        for text_line in word_file:
            line = text_line.split()
            key = line[0]
            vec = np.array(map(lambda e: float(e), line[1:]))
            normalized = hashlib.md5(key).hexdigest()
            #import pdb; pdb.set_trace();
            print key, normalized
            f.create_dataset(normalized, data=vec)
    f.close();

