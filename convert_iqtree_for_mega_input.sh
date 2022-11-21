#!/usr/bin/env bash

function usage() {
    echo ""
    echo "convert_iqtree_for_mega_input.sh -- convert iqtree result.treefile for mega realtime input"
    echo ""
    echo "Bugs: any bug should reported to yanpengch@qq.com"
    echo "Date: 2022-11-21"
    echo "Usage:"
    echo "  convert_iqtree_for_mega_input.sh iqtree_result.treefile > out.tree"
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

sed -E 's/\/([0-9.]){2,}//g' $1