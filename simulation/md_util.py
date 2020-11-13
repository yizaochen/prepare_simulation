from os import path
from shutil import copyfile
import re, shutil

def make_mdp(templatefile, i, find_pat, outputfolder):
    """

    """
    step = 50000000  # time step: 0.002 ps; 50000000*0.002 = 100000 ps (100ns)
    inistep = i * step
    newfilename = path.join(outputfolder, f'md{i}.mdp')
    copyfile(templatefile, newfilename)
    print(f'cp {templatefile} {newfilename}')
    with open(newfilename, 'r') as f:
        lines = f.readlines()
    with open(newfilename, 'w') as f:
        for line in lines:
            f.write(re.sub(find_pat, 'init-step       = {0}'.format(str(inistep)), line))
