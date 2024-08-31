# A batch shell script to convert the Gaussian orbital to the format for Abacus
basisname=MOLOPT-TZV2PX
basis_label=TZV2PX-MOLOPT
rcut=14
#pyscript=../aims2abacus_gaussian.py
pyscript=../cp2k2abacus_gaussian.py

cd MOLOPT-TZV2PX-${rcut}au
python $pyscript 01_H_default 01H_${basisname}_${rcut}au $rcut $basis_label
#python $pyscript 03_Li_default 03Li_${basisname}_${rcut}au $rcut
python $pyscript 06_C_default 06C_${basisname}_${rcut}au $rcut $basis_label
python $pyscript 07_N_default 07N_${basisname}_${rcut}au $rcut $basis_label
python $pyscript 08_O_default 08O_${basisname}_${rcut}au $rcut $basis_label
#python $pyscript 11_Na_default 11Na_${basisname}_${rcut}au $rcut