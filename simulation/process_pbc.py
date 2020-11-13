import os
import os.path as path

def process_nopbcgro(GMX, prevdir, mdnum):
    if mdnum == 0:
        refstructure = path.join(prevdir,'order_xtc','{0}.nopbc.gro'.format('npt4'))
    else:
        refstructure = path.join(prevdir,'order_xtc','md{0}.nopbc.gro'.format(str(mdnum-1)))
    inputxtc = path.join(prevdir,'order_xtc','md{0}.xtc'.format(str(mdnum)))
    outputstructure = path.join(prevdir,'order_xtc','md{0}.nopbc.gro'.format(str(mdnum)))
    command = 'echo 0 | {0} trjconv -s {1} -f {2} -pbc nojump -o {3} -dump {4}'.format(GMX,refstructure,inputxtc,outputstructure,str((mdnum+1)*100000))
    print(command)
    os.system(command)


def process_xtc(GMX, prevdir, system, mdnum, atg_num):
    rawdir = path.join(prevdir, 'data', 'raw')
    inputxtc = path.join(prevdir, 'order_xtc','md{0}.xtc'.format(str(mdnum-1))) 
    outputxtc = path.join(rawdir,'{0}.nopbc.{1}.xtc'.format(system,str(mdnum)))
    ndx = path.join(prevdir, 'ndx','{0}.ndx'.format(system))
    if mdnum == 1:
        refstructure = path.join(prevdir, 'order_xtc','npt4.nopbc.gro')
    else:
        refstructure = path.join(prevdir, 'order_xtc','md{0}.nopbc.gro'.format(str(mdnum-2)))
    command = 'echo {0} {0}| {1} trjconv -s {2} -f {3} -pbc nojump -o {4} -center -n {5}'.format(atg_num, GMX,refstructure,inputxtc,outputxtc,ndx)
    print(command)
    os.system(command)


def fitting_xtc(GMX, prevdir, system, mdnum): 
    rawdir = path.join(prevdir, 'data', 'raw')
    grodir = path.join(prevdir, 'data', 'gro')
    fitdir = path.join(prevdir, 'data','fittrj')
    outputxtc = path.join(rawdir,'{0}.nopbc.{1}.xtc'.format(system,str(mdnum)))
    
    fitgro = path.join(grodir,'{0}.npt4.fit.gro'.format(system))
    fitxtc = path.join(fitdir,'{0}.nopbc.{1}.fit.xtc'.format(system,str(mdnum)))
    command = 'echo 0 0| {0} trjconv -fit rot+trans -s {1} -f {2} -o {3}'.format(GMX,fitgro,outputxtc,fitxtc)
    print(command)
    os.system(command)


def extract_trajectory_by_big_interval(GMX, prevdir, system, mdnum): 
    roughdir = path.join(prevdir, 'data','roughtrj','1000')
    fitdir = path.join(prevdir, 'data','fittrj')
    fitxtc = path.join(fitdir,'{0}.nopbc.{1}.fit.xtc'.format(system,str(mdnum)))

    roughxtc = path.join(roughdir,'{0}.nopbc.fit.{1}.1000.xtc'.format(system,str(mdnum)))
    command = '{0} trjcat -f {1} -o {2} -dt 100'.format(GMX,fitxtc,roughxtc)
    print(command)
    os.system(command)

def concatenate_trajectory(GMX, prevdir, system, start, end):
    roughdir = path.join(prevdir, 'data','roughtrj','1000')
    alltrajfiles = ''
    for mdnum in range(start+1, end+2):
        filename = path.join(roughdir, '{0}.nopbc.fit.{1}.1000.xtc'.format(system,str(mdnum)))
        alltrajfiles = alltrajfiles + filename + ' '
    outtraj = path.join(roughdir, '{0}.nopbc.fit.{1}to{2}.1000.xtc'.format(system,str(start+1),str(end+1)))
    command = '{0} trjcat -f {1} -o {2} -dt 100'.format(GMX,alltrajfiles,outtraj)
    print(command)
    os.system(command)
    
