#!/bin/bash
#SBATCH --cluster=pitzer
#SBATCH --time=1:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=39
#SBATCH --job-name=L96ForcingProject
#SBATCH --account=PAS2635
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=creager.52@osu.edu

export Fvals=$(seq -f "%.1f" 5.0 0.1 5.5)

for F in $Fvals
do
  echo "$F"
  python Fconst_super_ens.py "$F" > "${F}_log" &
done
wait