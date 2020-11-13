import os
import os.path as path

rootdir = '/home/yizaochen/simulation/hAgo/arna+arna'
GMX = '/home/yizaochen/gromacs-5.1/bin/gmx '
system_name = 'arna+arna'
na_type = 'RNA'
switch = {1: False, 2: False, 3: False, 4: False, 5: False,
          6: True}   # Regulate

fname_list = ['nvt1', 'nvt2', 'npt1', 'npt2', 'npt3', 'npt4']

#1. Ouput Only DNA Traj
if switch[1]:
    refstruc = path.join(rootdir , 'order_xtc', 'npt4.nopbc.gro')
    ndx = path.join(rootdir, 'ndx', 'arna+arna.ndx')
    for fname in fname_list:
        traj_in = path.join(rootdir, '{0}.trr'.format(fname))
        traj_out = path.join(rootdir, 'equil', '{0}.na.xtc'.format(fname))
        cmd = 'echo 11 11|{0} trjconv -s {1} -f {2} -o {3} -center -pbc nojump -n {4}'.format(GMX, refstruc, traj_in, traj_out, ndx)
        os.system(cmd)

#2. Combine Equilibrium Traj
if switch[2]:
    traj_out = path.join(rootdir, 'equil', 'equil.combine.xtc')
    cmd = '{0} trjcat -f '.format(GMX)
    for fname in fname_list:
        traj_in = path.join(rootdir, 'equil', '{0}.na.xtc'.format(fname))
        cmd = '{0} {1}'.format(cmd,traj_in)
    cmd = '{0} -o {1}'.format(cmd, traj_out)
    os.system(cmd)

#3. Best Fit 
if switch[3]:
    refstruc = path.join(rootdir , 'data', 'gro', 'arna+arna.npt4.fit.gro') 
    traj_in = path.join(rootdir, 'equil', 'equil.combine.xtc')
    traj_out = path.join(rootdir, 'data', 'fittrj', 'arna+arna.nopbc.equil.fit.xtc')
    cmd = 'echo 0 0 | {0} trjconv -s {1} -f {2} -o {3} -fit rot+trans'.format(GMX, refstruc, traj_in, traj_out)
    os.system(cmd)

#4. Change Time
if switch[4]:
    rmsddir = path.join(rootdir , 'data', 'rmsd') 
    if not path.isdir(rmsddir):
        os.mkdir(rmsddir)
        print("{0} is created!".format(rmsddir))
    traj_in_1 = path.join(rootdir, 'data', 'fittrj', 'arna+arna.nopbc.equil.fit.xtc')
    traj_in_2 = path.join(rootdir, 'data', 'roughtrj', '1000', '{0}.nopbc.fit.1to10.xtc'.format(system_name))
    traj_out  = path.join(rmsddir, '{0}.equil+1000ns.dt1ns.xtc'.format(system_name))
    tempfile = path.join(rootdir, 'temp.txt')
    f = open(tempfile, 'w')
    f.write('0\n5100\n')
    f.close()
    cmd = '{0} trjcat -f {1} {2} -o {3} -dt 1000 -settime < {4}'.format(GMX, traj_in_1, traj_in_2, traj_out, tempfile)
    os.system(cmd)
    os.remove(tempfile)

#5. Make Index
if switch[5]:
    stru_in = path.join(rootdir, 'data', 'gro', '{0}.npt4.fit.pdb'.format(system_name))
    index_out = path.join(rootdir, 'ndx', 'r5_15.ndx')
    tempfile = path.join(rootdir, 'temp.txt')
    f = open(tempfile, 'w')
    f.write('r 5-15\nq\n')
    f.close()
    cmd = '{0} make_ndx -f {1} -o {2} < {3}'.format(GMX, stru_in, index_out, tempfile)
    os.system(cmd)
    os.remove(tempfile)

#6. RMSD FIT
if switch[6]:
    if na_type == 'DNA':
        refstru_a = '/home/yizaochen/simulation/hAgo/refgro/add_r5_15.gro' 
        refstru_b = '/home/yizaochen/simulation/hAgo/refgro/bdd_r5_15.gro'
    else:
        refstru_a = '/home/yizaochen/simulation/hAgo/refgro/arr_r5_15.gro' 
        refstru_b = '/home/yizaochen/simulation/hAgo/refgro/brr_r5_15.gro'
    trajin = path.join(rootdir, 'data', 'rmsd', '{0}.r5_15.xtc'.format(system_name))
    xvg_out_a = path.join(rootdir, 'data', 'rmsd', '{0}.rmsd.a.xvg'.format(system_name))
    xvg_out_b = path.join(rootdir, 'data', 'rmsd', '{0}.rmsd.b.xvg'.format(system_name))
    cmd = '{0} rms -s {1} -f {2} -o {3} -tu ns -fit rot+trans'.format(GMX, refstru_a, trajin, xvg_out_a)
    os.system(cmd)
    cmd = '{0} rms -s {1} -f {2} -o {3}  -tu ns -fit rot+trans'.format(GMX, refstru_b, trajin, xvg_out_b)
    os.system(cmd)
 
