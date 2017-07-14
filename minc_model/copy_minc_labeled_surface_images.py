import csv
import os
import os.path
import shutil
import re
from contextlib import contextmanager

# from http://stackoverflow.com/a/24176022/1114328
@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)

def go():
    datadir = '/x/alexburka'
    with open('ONE THOUSAND SURFACES - Surfaces.csv', 'rb') as r:
        with cd('minc_model'):
            with open('images/props_w.txt', 'w+') as pw, open('images/props_h.txt', 'w+') as ph, open('images/props_r.txt', 'w+') as pr, open('images/props_ss.txt', 'w+') as pss, open('images/props_so.txt', 'w+') as pso, open('images/props_sb.txt', 'w+') as psb:
                rdr = csv.reader(r)
                next(rdr)
                for row in rdr:
                    if row[8] != '' and 'HaTT' in row[9]:
                        for (flow, col, ps) in [('stickcam', 2, pss), ('optocam', 4, pso), ('biocam', 6, psb)]:
                            if row[col] != '':
                                fname = '%s/%s/%s/%s/surface.png' % (datadir, row[col], flow, row[col+1])
                                if os.path.isfile(fname):
                                    print(fname)
                                    new_fname = 'images/%s/%s_%s_%s.png' % (row[8], row[col], flow, row[col+1])
                                    shutil.copyfile(fname, new_fname)
                                    flow = '%s/%s/%s/%s/%s.flow' % (datadir, row[col], flow, row[col+1], flow)
                                    with open(flow) as f:
                                        lines = f.readlines()
                                        warm = [line for line in lines if 'warm' in line]
                                        hard = [line for line in lines if 'hard' in line]
                                        rough = [line for line in lines if 'rough' in line]
                                        slippery = [line for line in lines if 'slippery' in line]
                                        if len(warm) == 1:
                                            pw.write('%s %s\n' % (new_fname, re.split(r'[\[\]]', warm[0])[1]))
                                        if len(hard) == 1:
                                            ph.write('%s %s\n' % (new_fname, re.split(r'[\[\]]', hard[0])[1]))
                                        if len(rough) == 1:
                                            pr.write('%s %s\n' % (new_fname, re.split(r'[\[\]]', rough[0])[1]))
                                        ps.write('%s %s\n' % (new_fname, re.split(r'[\[\]]', slippery[0])[1]))
                            
if __name__ == '__main__':
    go()

