#!/bin/bash
#
#SBATCH --comment=mesh_convg
#SBATCH --qos=bfbsm19
#SBATCH --partition=bfbsm_2019

#SBATCH --nodes=3
#SBATCH --sockets-per-node=2
#SBATCH --ntasks-per-node=24
#SBATCH --mem-per-cpu=7000
#SBATCH --job-name=Cond_1-SBES_24M_BP
#SBATCH --output=CY_artery
#SBATCH --time=1000:00:00


#### SLURM 2 node, 24 processor per node Ansys Fluent test to run for 30min.

module purge
module add apps/ansys/2020r1 

# Create our hosts file ala slurm
srun hostname -s |sort -V > $(pwd)/slurmhosts.$SLURM_JOB_ID.txt

time fluent 3ddp -g -t${SLURM_NTASKS} -slurm -pib.infinipath -mpi=ibmmpi -cnf=$(pwd)/slurmhosts.$SLURM_JOB_ID.txt -i SBES_SS.jou
