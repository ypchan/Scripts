
#!/usr/bin/env python3
import sys

all_lst = []
with open(sys.argv[1], 'rt') as infh:
    for line in infh:
        if line.startswith('Genus'):
            continue
        line_lst = line.rstip('\n').split('\t')
        accession_num = 3 - line_lst.count('NA')
        line_lst[9] = accession_num
        all_lst.append(line_lst)

all_lst.sort(key=lambda x: (x[0], -x[9]))
for i in all_lst:
    print(i)
sys.exit(0)
