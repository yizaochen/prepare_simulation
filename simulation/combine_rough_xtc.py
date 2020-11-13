import os
import os.path as path

"""
md0.xtc: 0_100ns  ,  md1.xtc: 100_200ns , md2.xtc: 200_300ns
md3.xtc: 300_400ns,  md4.xtc: 400_500ns , md5.xtc: 500_600ns
md6.xtc: 600_700ns,  md7.xtc: 700_800ns ,
"""

GMX = '/home/yizaochen/gromacs-5.1/bin/gmx '

def process_nopbcgro(prevdir, system, suffix, series):
    roughtrj_dir = path.join(prevdir, system, 'data', 'roughtrj', '1000')
    output_dir = path.join(prevdir, system, 'data', 'roughtrj')
    inputfiles = ''
    for filenum in series:
        f = path.join(roughtrj_dir, '3f73+grna+trna+mg.nopbc.fit.{0}.1000.xtc'.format(filenum))
        inputfiles = '{0} {1}'.format(inputfiles, f)
    outputfile = path.join(output_dir, '{0}_{1}.dt100ps.xtc'.format(system, suffix))
    command = '{0} trjcat -f {1} -o {2} -dt 100'.format(GMX, inputfiles, outputfile)
    os.system(command)
    
#-Ad hoc parts------#    
prevdir = '/home/yizaochen/simulation'
system = '3f73+grna+trna+mg'
start = 0   # 0_1 us
end = 4     # 4_5 us
#-------------------#

for i in range(start, end+1):
    suffix = '{0}_{1}us'.format(i, i+1)
    series = range(i*10+1, i*10+11)
    process_nopbcgro(prevdir, system, suffix, series) 
