import os

modelpath = os.path.join(os.path.expanduser('~'), 'Documents', 'testing')

directory = 'project1'

fullpath = os.path.join(modelpath, directory)

os.mkdir(fullpath)

files = [os.path.join(fullpath, 'test.record'), os.path.join(fullpath, 'train.record'), os.path.join(fullpath, 'results.h5')]

for i in files:
    with open(i, 'w'): pass
