#!/bin/bash

scontrol show nodes | awk '
BEGIN { OFS="\t" }
/NodeName=/ {
    split($1, a, "=")
    node="NodeName=" a[2]
    next
}
{
    for (i=1; i<=NF; i++) {
        if ($i ~ /CPUAlloc=/) {
            split($i, a, "=")
            cpu_alloc="CPUAlloc=" a[2]
        } else if ($i ~ /CPUTot=/) {
            split($i, a, "=")
            cpu_tot="CPUTot=" a[2]
        } else if ($i ~ /CPULoad=/) {
            split($i, a, "=")
            cpu_load="CPULoad=" a[2]
        }
    }
    print node, cpu_alloc, cpu_tot, cpu_load
}
'

