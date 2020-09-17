#!/usr/bin/env bash
###!/bin/bash -l
### declare job name
###PBS -N job_name
##
### request queue for this job
###PBS -q batch
##
### request a total 64 processors fotr this job (2 nodes and 32 processors per node)
###PBS -l nodes=1:ppn=32
##
###PBS -j oe
##
###PBS -V
##
### run time
###PBS -l walltime=120:00:00
##
##cd $PBS_O_WORKDIR
##source activate orthofinder
##
### define some variables
##logname=
##jobname=
##
### job log
##echo "Run ${job_name}" | tee ${logname}.log
##echo "" | tee -a ${logname}.log
##
### count nodes
##NP=$(cat $PBS_NODEFILE | wc -l)
##
##echo "------------------------------------------------" | tee -a ${logname}.log
##echo "Jobid :" ${PBS_JOBID%.mgr} | tee -a ${logname}.log
##echo "Queue :" $PBS_QUEUE | tee -a ${logname}.log
##echo "Nodes :" $PBS_O_HOST | tee -a ${logname}.log
##echo "CPUs  :" $NP | tee -a ${logname}.log
##echo "------------------------------------------------" | tee -a ${logname}.log
##echo "" | tee -a ${logname}.log
##
### start time
##echo $(date) | tee -a ${logname}.log
##
### program block
### example:
### orthofinder -f Sordariomycetes_protein_sets 2>&1 | tee -a ${logname}.log
##
### end time
##echo $(date) | tee -a ${logname}.log
#
grep '^##' $0 | sed 's/##//'
