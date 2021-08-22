#!/bin/bash
#
#SBATCH --comment=mesh_convg
#SBATCH --qos=bfbsm19
#SBATCH --partition=bfbsm_2019

#SBATCH --nodes=8
#SBATCH --sockets-per-node=2
#SBATCH --ntasks-per-node=24
#SBATCH --mem-per-cpu=7500
#SBATCH --job-name=C1_19T_IDDES
#SBATCH --output=C4-IDDES
#SBATCH --time=355:00:00


#### SLURM 2 node, 24 processor per node Ansys Fluent test to run for 30min.
module purge
module add apps/ansys/2021r1

# Create our hosts file ala slurm
srun hostname -s |sort -V > $(pwd)/slurmhosts.$SLURM_JOB_ID.txt

time fluent 3ddp -g -t${SLURM_NTASKS} -slurm -pib.infinipath -mpi=ibmmpi -cflush -platform=intel -cnf=$(pwd)/slurmhosts.$SLURM_JOB_ID.txt -i C1_T_IDDES_19M.jou
