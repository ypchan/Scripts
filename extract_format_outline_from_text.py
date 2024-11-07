#!/usr/bin/env python3
'''
extract_format_outline_from_text.py
'''

import sys

in_text = sys.argv[1]

out_lst = ['', '', '', '', '', '', '']

print(f'Phylum\tSubphylum\tClass\tSubclass\tOrder\tFamily\tGenus',
      file=sys.stdout, flush=True)

with open(in_text, 'rt') as infh:
    for line in infh:
        line = line.rstrip('\n')

        # skip blank line
        if not line:
            continue

        # skip page line
        if line.isnumeric():
            continue

        line_lst = line.split()
        rank_name = line_lst[0]

        if rank_name.endswith('mycota'):
            phylum = rank_name
            out_lst[0] = phylum
            if line.endswith('order incertae sedis') or line.endswith('orders incertae sedis'):
                subpylum = 'incertae sedis'
                class_name = 'incertae sedis'
                subclass = 'incertae sedis'
                out_lst[1] = subpylum
                out_lst[2] = class_name
                out_lst[3] = subclass

            if line.endswith('families incertae sedis') or line.endswith('family incertae sedis'):
                subpylum = 'incertae sedis'
                class_name = 'incertae sedis'
                subclass = 'incertae sedis'
                order = 'incertae sedis'
                out_lst[1] = subpylum
                out_lst[2] = class_name
                out_lst[3] = subclass
                out_lst[4] = order

            if line.endswith('genera incertae sedis') or line.endswith('genus incertae sedis'):
                subpylum = 'incertae sedis'
                class_name = 'incertae sedis'
                subclass = 'incertae sedis'
                order = 'incertae sedis'
                family = 'incertae sedis'
                out_lst[1] = subpylum
                out_lst[2] = class_name
                out_lst[3] = subclass
                out_lst[4] = order
                out_lst[5] = family

            continue

        if rank_name.endswith('mycotina'):
            subpylum = rank_name
            out_lst[1] = subpylum

            # order incertae sedis
            if line.endswith('order incertae sedis') or line.endswith('orders incertae sedis'):
                class_name = 'incertae sedis'
                subclass = 'incertae sedis'
                out_lst[2] = class_name
                out_lst[3] = subclass

            if line.endswith('families incertae sedis') or line.endswith('family incertae sedis'):
                class_name = 'incertae sedis'
                subclass = 'incertae sedis'
                order = 'incertae sedis'
                out_lst[2] = class_name
                out_lst[3] = subclass
                out_lst[4] = order

            if line.endswith('genera incertae sedis') or line.endswith('genus incertae sedis'):
                class_name = 'incertae sedis'
                subclass = 'incertae sedis'
                order = 'incertae sedis'
                family = 'incertae sedis'
                out_lst[2] = class_name
                out_lst[3] = subclass
                out_lst[4] = order
                out_lst[5] = family

            continue

        if rank_name.endswith('mycetes'):
            class_name = rank_name
            out_lst[2] = class_name

            # order incertae sedis
            if line.endswith('order incertae sedis') or line.endswith('orders incertae sedis'):
                subclass = 'incertae sedis'
                out_lst[3] = subclass

            if line.endswith('families incertae sedis') or line.endswith('family incertae sedis'):
                subclass = 'incertae sedis'
                order = 'incertae sedis'
                out_lst[3] = subclass
                out_lst[4] = order

            if line.endswith('genera incertae sedis') or line.endswith('genus incertae sedis'):
                subclass = 'incertae sedis'
                order = 'incertae sedis'
                family = 'incertae sedis'
                out_lst[3] = subclass
                out_lst[4] = order
                out_lst[5] = family

            continue

        if rank_name.endswith('mycetidae'):
            subclass = rank_name
            out_lst[3] = subclass

            if line.endswith('families incertae sedis') or line.endswith('family incertae sedis'):
                order = 'incertae sedis'
                out_lst[4] = order

            if line.endswith('genera incertae sedis') or line.endswith('genus incertae sedis'):
                order = 'incertae sedis'
                family = 'incertae sedis'
                out_lst[4] = order
                out_lst[5] = family

            continue

        if rank_name.endswith('ales'):
            order = rank_name
            out_lst[4] = order
            if line.endswith('genera incertae sedis') or line.endswith('genus incertae sedis'):
                family = 'incertae sedis'
                out_lst[5] = family
            continue

        if rank_name.endswith('aceae'):
            family = rank_name
            out_lst[5] = family
            continue

        genus_name = rank_name
        out_lst[6] = genus_name
        print('\t'.join(out_lst), file=sys.stdout, flush=True)
    sys.exit(0)
