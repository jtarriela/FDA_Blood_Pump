#!/bin/bash
#
#SBATCH --comment=mesh_convg
#SBATCH --qos=bfbsm19
#SBATCH --partition=bfbsm_2019

#SBATCH --nodes=5
#SBATCH --sockets-per-node=2
#SBATCH --ntasks-per-node=24
#SBATCH --mem-per-cpu=7500
#SBATCH --job-name=C4_19
#SBATCH --output=CY_artery
#SBATCH --time=355:00:00


#### SLURM 2 node, 24 processor per node Ansys Fluent test to run for 30min.

module purge
module add apps/ansys/2020r1 

# Create our hosts file ala slurm
srun hostname -s |sort -V > $(pwd)/slurmhosts.$SLURM_JOB_ID.txt

time fluent 3ddp -g -t${SLURM_NTASKS} -slurm -pib.infinipath -mpi=ibmmpi -cnf=$(pwd)/slurmhosts.$SLURM_JOB_ID.txt -i C4_SS_SBES_19M.jou
