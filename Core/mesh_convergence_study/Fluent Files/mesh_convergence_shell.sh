#!/bin/bash
#
#SBATCH --comment=mesh_convg
#SBATCH --qos=bfbsm19
#SBATCH --partition=bfbsm_2019

#SBATCH --nodes=1
#SBATCH --sockets-per-node=2
#SBATCH --ntasks-per-node=16
#SBATCH --mem-per-cpu=5000
#SBATCH --job-name=crse
#SBATCH --output=CY_artery
#SBATCH --time=74:00:00


#### SLURM 2 node, 24 processor per node Ansys Fluent test to run for 30min.

module purge
module add apps/ansys/2020r1 

# Create our hosts file ala slurm
srun hostname -s |sort -V > $(pwd)/slurmhosts.$SLURM_JOB_ID.txt

time fluent 3ddp -g -t${SLURM_NTASKS} -ssh -pib.infinipath -mpi=intel -cnf=$(pwd)/slurmhosts.$SLURM_JOB_ID.txt -i mesh_convergence_tui_v_21_1.jou
