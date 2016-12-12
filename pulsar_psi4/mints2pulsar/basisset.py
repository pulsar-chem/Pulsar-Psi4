import psi4.core as psi4
import pulsar as psr

def psr_2_psi4_bs(wfn,bs_key):
    """Converts the pulsar basis into a vector of shells needed to make Psi4
       basis
       
       wfn : the pulsar wavefunction to convert
       bs_key : the key for the pulsar basis to use
    """
    PsrBS=wfn.system.get_basis_set(bs_key)
    bsvec=psi4.BSVec()
    counter=0;nbf=0
    for bf in PsrBs:
        psi4_type=psi4.GaussianType.Pure
        if bf.get_type() == psr.ShellType.CartesianGaussian:
            psi4_type=psi4.GaussianType.Cartesian
        shell=psi4.ShellInfo(bf.am(),bf.get_coefs(),bf.get_alphas(),
           psi4_type,counter,nbf,psi4.PrimitiveType.Unnormalized
           )
        counter+=1
        nbf+=bf.n_functions()
        bsvec.push_back(shell)
    return bsvec
