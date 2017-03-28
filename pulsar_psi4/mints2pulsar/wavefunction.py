from mints2pulsar.molecule import *
from mints2pulsar.basisset import *
import numpy as np

def psr_2_psi4_wfn(wfn,key):
    """Converts the pulsar wavefunction to a psi4 wavefunction
       
       wfn : the pulsar wavefunction to convert
       key : the key to the pulsar basis set to associate with this wfn
       
       TODO: Fitting basis sets
    """
    psi4mol=psr_2_psi4_mol(wfn.system)
    psi4bs=psr_2_psi4_bs(wfn,psi4mol,key)
    return psi4.Wavefunction(psi4mol,psi4bs)

def psi4_wfn_2_psr(wfn):
    alpha,beta=psr.Spin.alpha,psr.Spin.beta
    Da_Spins=[alpha] if (wfn.same_a_b_orbs() and wfn.same_a_b_dens()) else [alpha,beta]
    psi4C={alpha:np.asarray(wfn.Ca()),beta:np.asarray(wfn.Cb())}
    psi4E={alpha:np.asarray(wfn.epsilon_a()),beta:np.asarray(wfn.epsilon_b())}
    psi4D={alpha:np.asarray(wfn.Da()),beta:np.asarray(wfn.Db())}
    PsrWfn=psr.Wavefunction()
    PsrWfn.epsilon=psr.BlockedEigenVector()
    PsrWfn.opdm,PsrWfn.cmat=psr.BlockedEigenMatrix(),psr.BlockedEigenMatrix()
    psrMatrix,psrVector=psr.EigenMatrixImpl,psr.EigenVectorImpl
    for spin in Da_Spins:
        irrep=psr.Irrep.A
        PsrWfn.cmat.set(irrep,spin,psrMatrix(psi4C[spin]))
        PsrWfn.epsilon.set(irrep,spin,psrVector(psi4E[spin]))
        PsrWfn.opdm.set(irrep,spin,psrMatrix(psi4D[spin]))
    return PsrWfn
