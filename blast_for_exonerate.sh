#!/usr/bin/env bash

<<COMMENT
AUTHOR: chenyanpeng1992@outlook.com
DATE  : 2020-09-13
COMMENT

function usage {
cat << EOF

$(basename $0) -- A shell script to run blast for exonerate genome annotation.

SYNOPSIS:
    $(basename $0) -p|--program <tblastn|blastn> 
                   -g|--genome <fasta(.gz)>
                   -e|--evidence <est.fna|prot.faa> 

OPTION:
    -h|--help                          print help message and exit
    -i|--in_sra_aspera  <sra_aspera>   input ENA SRA aspera url, required. Example: fasp.sra.ebi.ac.uk:/vol1/srr/SRR106/023/SRR10641223"
    -o|--out_dirname    <dirname>      output direname, optional. [Default: `pwd`]

BUGS:
    Any bugs in fastqInfo should be reported to chenyanpeng1992@outlook.com

EOF
}

# parse command-line arguments
PARSED_ARGUMENTS=$(getopt -a -n ascp.sh -o hi:o: --long help,in_sra_url:,out_dirname: -- "$@")
VALID_ARGUMENTS=$?

if [ "$VALID_ARGUMENTS" != "0" ]
then
    usage
fi

eval set -- "$PARSED_ARGUMENTS"

while :
do
    case "$1" in
        -h | --help)
            usage
            exit 2 ;;
        -i | --in_sra_aspera)
            SRA_ASPERA=$2
            shift 2 ;;
        -o | --out_dirname)
            DIRNAME=$2
            shift 2 ;;
        --)
            # -- means the end of the arguments; drop this, and break out of the while loop
            shift
            break ;;
        *)
            # If invalid options were passed, then getopt should have reported an error,
            # which we checked as VALID_ARGUMENTS when getopt was called...
            echo "Unknown option: $1"
               usage ;;
    esac
done

if [[ ! $SRA_ASPERA ]]
then
    echo "[ERROR] no input. The argument: -i|--in_sra_url is required."
    usage
    exit 2
fi

if [[ ! $DIRNAME ]]
then
    DIRNAME="./"
fi

function ascp {
    echo "$ASCP -i $ASPERA_KEY -v -k 1 -T -l 400m --mode=recv era-fasp@$SRA_ASPERA $DIRNAME"
    echo ""
    $ASCP \
    -i $ASPERA_KEY \
    -v \
    -k 1 \
    -T \
    -l 400m \
    --mode=recv \
    -P 33001 \
    era-fasp@$SRA_ASPERA \
    $DIRNAME
    return 0
}

ascp