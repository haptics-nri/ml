import csv
import os.path
import shutil

def go():
    with open('../ONE THOUSAND SURFACES - Surfaces.csv', 'rb') as f:
        rdr = csv.reader(f)
        next(rdr)
        for row in rdr:
            if row[8] != '':
                for (flow, col) in [('stickcam', 2), ('optocam', 4), ('biocam', 6)]:
                    if row[col] != '':
                        fname = '../%s/%s/%s/surface.png' % (row[col], flow, row[col+1])
                        if os.path.isfile(fname):
                            print(fname)
                            shutil.copyfile(fname, 'images/%s/%s_%s_%s.png' % (row[8], row[col], flow, row[col+1]))

if __name__ == '__main__':
    go()

