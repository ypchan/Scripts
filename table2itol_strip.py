
'''
table2itol_strip.py -- get strip control file

Author:
    chengyanpeng1992@outlook.com
Bugs: 
    Any bugs should be reported to the above E-mail.
'''
import os
import sys
import gzip
import argparse

colors_lst109 = ["#FFB6C1", "#DC143C", "#FFF0F5", "#DB7093", "#FF69B4", "#FF1493", "#C71585", "#DA70D6", "#D8BFD8", "#EE82EE", "#FF00FF", "#800080", "#BA55D3", "#9400D3", "#4B0082", "#8A2BE2", "#9370DB", "#7B68EE", "#483D8B", "#E6E6FA", "#0000FF", "#191970", "#00008B", "#4169E1", "#6495ED", "#B0C4DE", "#778899", "#1E90FF", "#F0F8FF", "#4682B4", "#87CEFA", "#87CEEB", "#00BFFF", "#5F9EA0", "#E0FFFF", "#AFEEEE", "#00FFFF", "#00CED1", "#2F4F4F", "#008B8B", "#48D1CC", "#20B2AA", "#7FFFD4", "#66CDAA", "#00FA9A", "#00FF7F", "#3CB371", "#2E8B57", "#F0FFF0", "#90EE90", "#8FBC8F", "#32CD32", "#00FF00", "#008000", "#006400", "#7FFF00", "#ADFF2F", "#556B2F", "#9ACD32", "#6B8E23", "#F5F5DC", "#FAFAD2", "#FFFFE0", "#FFFF00", "#808000", "#BDB76B", "#FFFACD", "#F0E68C", "#FFD700", "#FFF8DC", "#DAA520", "#B8860B", "#FDF5E6", "#F5DEB3", "#FFA500", "#FFEFD5", "#FFDEAD", "#FAEBD7", "#D2B48C", "#FFE4C4", "#FF8C00", "#FAF0E6", "#CD853F", "#FFDAB9", "#F4A460", "#D2691E", "#8B4513", "#FFF5EE", "#FFA07A", "#FF7F50", "#FF4500", "#E9967A", "#FF6347", "#FFE4E1", "#FA8072", "#FFFAFA", "#F08080", "#BC8F8F", "#CD5C5C", "#FF0000", "#A52A2A", "#B22222", "#8B0000", "#800000", "#DCDCDC", "#C0C0C0", "#A9A9A9", "#808080", "#000000"]

def parse_args():
    '''Parse command-line arguments.
    '''
    parser = argparse.ArgumentParser(description=__doc__,
                        formatter_class=argparse.RawDescriptionHelpFormatter)
    
    parser.add_argument('mapfile',
                        metavar='<map.txt>',
                        type=str,
                        help='tiptag and corresponding speciestag, without head line')
    
    parser.add_argument('-n', '--datasetname',
                        type=str,
                        default='color strip',
                        help='data set name')

    parser.add_argument('-s', '--separator',
                        default='SPACE',
                        choices=["SPACE","TAB","COMMA"],
                        type=str,
                        help='delimeter in mapfile')

    parser.add_argument('-c', '--colorbranchs',
                        type=str,
                        help='filtered protein file name. default: in_pass.faa.gz')
    
    parser.add_argument('-m', '--margin',
                        type=int,
                        help='protein file that did not pass the filtration. default: in_notpass.faa.gz')
    
    parser.add_argument('-C', '--bordercolor',
                        type=str,
                        default='#000',
                        help='border color')
    
    parser.add_argument('-b', '--borderwidth',
                        type=float,
                        default=1,
                        help='border line width')

    parser.add_argument('-W', '--stripwidth',
                        type=float,
                        default=25,
                        help='strip width')
    
    args = parser.parse_args()

    return args

if __name__ == '__main__':
    args = parse_args()
    print("DATASET_COLORSTRIP", file=sys.stdout, flush=True)
    print("#lines starting with a hash are comments and ignored during parsing\n#select the separator which is used to delimit the data below (TAB,SPACE or COMMA).This separator must be used throught this file (except in the SEPARATOR line, which uses space).", file=sys.stdout, flush=True)
    
    if args.separator == 'TAB':
        print("SEPARATOR TAB", file=sys.stdout, flush=True)
    else:
        print("#SEPARATOR TAB", file=sys.stdout, flush=True)
    
    if args.separator == 'SPACE':
         print("SEPARATOR SPACE", file=sys.stdout, flush=True)
    else:
        print("#SEPARATOR SPACE", file=sys.stdout, flush=True)
    
    if args.separator == 'COMMA':
         print("SEPARATOR COMMA", file=sys.stdout, flush=True)
    else:
        print("#SEPARATOR COMMA", file=sys.stdout, flush=True)

    print("#label is used in the legend table (can be changed later)", file=sys.stdout, flush=True)
    print(f"DATASET_LABEL {args.datasetname}\n", file=sys.stdout, flush=True)

    print("#dataset color (can be changed later)", file=sys.stdout, flush=True)
    print("COLOR #ff0000\n", file=sys.stdout, flush=True)

    print("#optional settings\n", file=sys.stdout, flush=True)

    print("#all other optional settings can be set or changed later in the web interface (under 'Datasets' tab)", file=sys.stdout, flush=True)
    print(f"COLOR_BRANCHES {args.colorbranches}\n", file=sys.stdout, flush=True)
    
    print("#maximum width", file=sys.stdout, flush=True)
    print(f"STRIP_WIDTH {args.stripwidth}\n", file=sys.stdout, flush=True)

    print("#left margin, used to increase/decrease the spacing to the next dataset. Can be negative, causing datasets to overlap.", file=sys.stdout, flush=True)
    print(f"MARGIN {args.margin}\n", file=sys.stdout, flush=True)

    print("#border width; if set above 0, a black border of specified width (in pixels) will be drawn around the color strip ", file=sys.stdout, flush=True)
    print(f"BORDER_WIDTH {args.borderwidth}", file=sys.stdout, flush=True)

    print(f"BORDER_COLOR {args.bordercolor}\n", file=sys.stdout, flush=True)

    print(f"#show internal values; if set, values associated to internal nodes will be displayed even if these nodes are not collapsed. It could cause overlapping in the dataset display.", file=sys.stdout, flush=True)
    print(f"SHOW_INTERNAL 0\n", file=sys.stdout, flush=True)

    print("#In colored strip charts, each ID is associated to a color. Color can be specified in hexadecimal, RGB or RGBA notation", file=sys.stdout, flush=True)
    print(f"#Internal tree nodes can be specified using IDs directly, or using the 'last common ancestor' method described in iTOL help pages", file=sys.stdout, flush=True)
    print('#Actual data follows after the "DATA" keyword', file=sys.stdout, flush=True)
    
    print(f"DATA", file=sys.stdout, flush=True)
    print(f"#ID1 value1", file=sys.stdout, flush=True)
    print(f"#ID2 value2", file=sys.stdout, flush=True)
    map_fh = open(args.mapfile)
    map_line_lst = map_fh.readlines()
    map_line_lst = [line.rstrip('\n') for line in map_line_lst]
    map_fh.close()
    species_tag = [line.split('\t')[1] for line in map_line_lst]
    
    species_colorrgb_hash = {'Missing':'#FFFFFF'}
    for species_tag in species_tag:
        if species_tag not in species_colorrgb_hash:
            num = len(species_colorrgb_hash)
            if 'Missing' in species_colorrgb_hash:
                num -= 1
            species_colorrgb_hash[species_tag] = colors_lst109[num]

    for line in map_line_lst:
        tip_tag, speceis_tag = line.split('\n')
        tip_color_rgb = species_colorrgb_hash[species_tag]
        if args.delimeter == 'SPACE':
            print(f'{tip_tag} {tip_color_rgb} {species_tag}', file=sys.stdout, flush=True)
        if args.delimeter == 'TAB':
            print(f'{tip_tag}\t{tip_color_rgb}\t{species_tag}', file=sys.stdout, flush=True)
        if args.delimeter == 'COMMA':
            print(f'{tip_tag},{tip_color_rgb},{species_tag}', file=sys.stdout, flush=True)



























