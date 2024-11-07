#!/usr/bin/env bash
#!/usr/bin/env bash

function usage() {
    echo ""
    echo "stat_gene_length.sh -- get gene length from gff3 files"
    echo ""
    echo "Bugs: any bug should reported to yanpengch@qq.com"
    echo "Date: 2022-11-25"
    echo "Usage:"
    echo "  stat_gene_length.sh -i gff3 > length.lst"
    echo ""
}
version=1.0

# check input
if [[ $# == 0 ]];then
    usage
    exit 0
fi
   
if [[ $1 =~ "-h" ]];then
    usage
    exit 0
fi

while [[ "$1" =~ ^- && ! "$1" == "--" ]]; do case $1 in
  -v | --version )
    echo "$version"
    exit
    ;;
  -i | --input )
    shift; INPUT_GFF3=$1
    ;;
esac; shift; done
if [[ "$1" == '--' ]]; then shift; fi

awk -F '\t' '$3=="gene" {print FILENAME"\t"$9"\t"$5-$4+1}' INPUT_GFF3 | sed 's/ID=/\t/;s/;/\t/'