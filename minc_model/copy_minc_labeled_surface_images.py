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
            with open('images/props.csv', 'wb+') as w:
                rdr = csv.reader(r)
                wtr = csv.DictWriter(w, fieldnames=['ID', 'ImageStick', 'ImageOpto', 'ImageBio', 'Warmness', 'Hardness', 'Roughness', 'SlipperinessStick', 'SlipperinessOpto', 'SlipperinessBio'])
                wtr.writeheader()
                idx = 1
                next(rdr)
                for row in rdr:
                    if row[8] != '' and 'HaTT' in row[9]:
                        props = {}
                        for (flow, col, eff) in [('stickcam', 2, 'Stick'), ('optocam', 4, 'Opto'), ('biocam', 6, 'Bio')]:
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
                                            props['Warmness'] = re.split(r'[\[\]]', warm[0])[1]
                                        if len(hard) == 1:
                                            props['Hardness'] = re.split(r'[\[\]]', hard[0])[1]
                                        if len(rough) == 1:
                                            props['Roughness'] = re.split(r'[\[\]]', rough[0])[1]
                                        props['Slipperiness%s' % eff] = re.split(r'[\[\]]', slippery[0])[1]
                                        props['Image%s' % eff] = new_fname
                        if 'SlipperinessStick' in props and 'SlipperinessOpto' in props and 'SlipperinessBio' in props:
                            props['ID'] = idx
                            idx = idx + 1
                            wtr.writerow(props)

if __name__ == '__main__':
    go()

