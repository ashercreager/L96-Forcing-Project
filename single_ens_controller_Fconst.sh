#!/bin/bash
#SBATCH --cluster=pitzer
#SBATCH --time=1:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=31
#SBATCH --job-name=pickles
#SBATCH --account=PAS2635
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=creager.52@osu.edu

export Fvals=$(seq -f "%.1f" 6.1 0.1 9.0)

for F in $Fvals
do
  echo "$F"
  python single_ens_controller_Fconst.py "$F" > "${F}_log" &
done
wait