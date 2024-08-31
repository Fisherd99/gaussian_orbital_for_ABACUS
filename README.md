# Gaussian orbital for ABACUS 
## About  
**ABACUS** (Atomic-orbital Based Ab-initio Computation at UStc) supports NAO(numerical atomic orbital) as calculation basis, which is in format of ORB file. So far, NAOs are only obtained through optimazation based on jY basis. This repository supplies gaussian orbitals in ORB format, which may be needed for benchmark with other softwares.

## How to use
1. Just assign the .orb file to ABACUS directly. They are converted from `aims/species_defaults/non-standard/gaussian_tight_770` and `cp2k/data/BASIS_MOLOPT`.

**NOTICE**: to use them, one should modify function `to_numerical_orbital_lm` in ABACUS source file `module_basis/module_nao/numerical_radial.cpp` as following
``` c++
void NumericalRadial::to_numerical_orbital_lm(Numerical_Orbital_Lm& orbital_lm, const int nk_legacy, const double lcao_dk) const
{
#ifdef __DEBUG
    assert(rgrid_);
    assert(rgrid_[0] == 0.0);
    assert(is_uniform(nr_, rgrid_, 1e-14));

    // Numerical_Orbital_Lm does not support extra exponent in the real space value
    assert(pr_ == 0);
#endif

    double dr = rgrid_[1] - rgrid_[0];
    double* rab = new double[nr_];
    std::fill(rab, rab + nr_, dr);

    //orbital_lm.set_orbital_info(symbol_, itype_, l_, izeta_, std::min(nr_, ircut_+1), rab, rgrid_,
    orbital_lm.set_orbital_info(symbol_, itype_, l_, izeta_, nr_, rab, rgrid_,
            Numerical_Orbital_Lm::Psi_Type::Psi, rvalue_, nk_legacy, lcao_dk,
            0.001 /* dr_uniform */, PARAM.inp.out_element_info, true, GlobalV::CAL_FORCE);
    delete[] rab;
}
```
Otherwise, the absolute value less than 1e-15 in gaussian orbital will cause different `rcut` and break down the calculation.

2. The script `xxx2abacus_gaussian.py` can generate arbitrary gaussian ORB file converted from xxx format. So far, xxx can be FHI-aims and CP2K. To use this, one can download gaussian orbital file in [basis exchange](https://www.basissetexchange.org/) and run command
```
python xxx2abacus_gaussian.py <inputfile> <outputfile> <rcut> [basis_label]
```
For example, in folder `aug-cc-pVTZ-14au`, run
```
python ../aims2abacus_gaussian.py 01_H_default 01H_augccpVTZ_14au 14
```
will generate `01H_augccpVTZ_14.orb` and `01H_augccpVTZ_14.png`.

And in folder `MOLOPT-TZVP-14au`, run
```
python ../cp2k2abacus_gaussian.py 01_H_default 01H_MOLOPT-TZVP_14au 14 MOLOPT-GTH
```
where `MOLOPT-GTH` is used to address in which line the script begins to read. The default value is `MOLOPT` if this parameter is not given.

3. The script `check_norm.py` can check whether each radial orbital is normalized. 

4. The script `convert.sh` can run a batch of `xxx2abacus_gaussian.py`.