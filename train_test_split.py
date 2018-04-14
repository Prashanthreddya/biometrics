import os
from shutil import copyfile

TRAINDIR = 'dataset/train/%d'
TESTDIR = 'dataset/test/%d'
data_path = 'dataset_bk/'

counts = {}
train_count = 0
test_count = 0

def check_dir(path, id):
    path = path % id
    if not os.path.exists(path):
        os.makedirs(path)
    return path

for fname in os.listdir(data_path):
    if fname.endswith('.jpg') and 'back' not in fname:
        id = int(os.path.basename(fname).split('_')[0])
        train_dest = check_dir(TRAINDIR, id)
        test_dest = check_dir(TESTDIR, id)

        fpath_old = os.path.join(data_path, fname)
        fpath_test = os.path.join(test_dest, fname)
        fpath_train = os.path.join(train_dest, fname)



        if id not in counts:
            counts[id] = 1
        else:
            counts[id] += 1

        if counts[id] > 4:
            copyfile(fpath_old, fpath_test)
            test_count += 1
        else:
            copyfile(fpath_old, fpath_train)
            train_count += 1

print "Train count: %d, Test count: %d" % (train_count, test_count)
