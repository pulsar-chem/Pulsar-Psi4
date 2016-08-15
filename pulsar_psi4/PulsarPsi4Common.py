import os
import sys
import pulsar as psr
thispath = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,os.path.dirname(thispath))
import psi4
import driver
import numpy as np

CheckpointPolicy=psr.datastore.CacheData.CachePolicy.CheckpointGlobal


pulsar_2_psi4={
   "BASIS_SET":"BASIS",
   "FITTING_BASIS":"DF_BASIS_SCF",
   "MAX_ITER": "MAXITER",
   "EGY_TOLERANCE":"E_CONVERGENCE",
   "DENS_TOLERANCE":"D_CONVERGENCE",
   "KEY_INITIAL_GUESS":"GUESS",
   "DAMPING_FACTOR":"DAMPING_PERCENTAGE",
   "GUESS":"GUESS",
   "FROZEN_CORE":"FREEZE_CORE"
   #"MAX_DERIV":"DERIV" Does Psi4 have this?
}

def psr_2_psi4_mol(PsrMol):
    """Converts the pulsar molecule into a Psi4 molecule
       TODO: Add symmetry
    """
    mol_string="no_com\nno_reorient\nunits bohr\nsymmetry c1\n"\
       +str(int(PsrMol.get_charge()))+" "+str(int(PsrMol.get_multiplicity()))\
       +"\n"
    for atom in PsrMol:
        mol_string+=psr.system.atomic_symbol_from_z(atom.Z)+" "+\
           str(atom[0])+" "+str(atom[1])+" "+str(atom[2])+"\n"
    return psi4.Molecule.create_molecule_from_string(mol_string)

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
        if bf.get_type() == psr.system.ShellType.CartesianGaussian:
            psi4_type=psi4.GaussianType.Cartesian
        shell=psi4.ShellInfo(bf.am(),bf.get_coefs(),bf.get_alphas(),
           psi4_type,counter,nbf,psi4.PrimitiveType.Unnormalized
           )
        counter+=1
        nbf+=bf.n_functions()
        bsvec.push_back(shell)
    return bsvec

def psr_2_psi4_wfn(wfn,key):
    """Converts the pulsar wavefunction to a psi4 wavefunction
       
       wfn : the pulsar wavefunction to convert
       key : the key to the pulsar basis set to associate with this wfn
       
       TODO: Fitting basis sets
    """
    psi4mol=psr_2_psi4_mol(wfn.system)
    psi4bs=psi4.BasisSet()
    psi4bs.build(psi4mol,psr_2_psi4_bs(wfn,key))
    psi4bs.print()
    #return psi4.Wavefunction(psi4mol,psi4bs,options)

def psi4_wfn_2_psr(wfn):
    alpha=psr.math.Spin.alpha;beta=psr.math.Spin.beta
    Da_Spins=[alpha] if (wfn.same_a_b_orbs() and wfn.same_a_b_dens()) else [alpha,beta]
    psi4C={alpha:np.asarray(wfn.Ca()),beta:np.asarray(wfn.Cb())}
    psi4E={alpha:np.asarray(wfn.epsilon_a()),beta:np.asarray(wfn.epsilon_b())}
    psi4D={alpha:np.asarray(wfn.Da()),beta:np.asarray(wfn.Db())}
    PsrWfn=psr.datastore.Wavefunction()
    PsrWfn.epsilon=psr.math.IrrepSpinVectorD()
    PsrWfn.opdm=psr.math.IrrepSpinMatrixD()
    PsrWfn.cmat=psr.math.IrrepSpinMatrixD()
    psrMatrix=psr.math.EigenMatrixImpl;psrVector=psr.math.EigenVectorImpl
    for spin in Da_Spins:
        irrep=psr.math.Irrep.A
        PsrWfn.cmat.set(irrep,spin,psrMatrix(psi4C[spin]))
        PsrWfn.epsilon.set(irrep,spin,psrVector(psi4E[spin]))
        PsrWfn.opdm.set(irrep,spin,psrMatrix(psi4D[spin]))
    return PsrWfn

def make_hash(my_options,order,wfn,opts):
     #Hash input to calculation, return if we know the answer
    option_hash=my_options.hash_values({i for i in opts})
    sys_hash=wfn.system.my_hash()
    return str((order,sys_hash,option_hash))    

def psi4_dryrun(wfn,my_options,cache,comp_hash,psi_variable=None):
    for i in my_options.get_keys():
        if i in pulsar_2_psi4:
           psi4.set_global_option(pulsar_2_psi4[i],my_options.get(i))
    if psi_variable and psi4.has_variable(psi_variable):
        Egy=psi4.get_variable(psi_variable)
        cache.set(comp_hash,(wfn,[Egy]),CheckpointPolicy)
    if cache.count(comp_hash): 
        return cache.get(comp_hash)
    return None
    
def psi4_call(method,deriv,wfn,my_options,cache,comp_hash):
    """ The call to Psi4's Python interface common to all methods.  This is 
        the real call.  All dry runs use psi4_dryrun.
    
        method : the string name Psi4 calls the requested method
        deriv  : the order derivative we want
        wfn    : the Pulsar wavefunction to use
        my_options : the Pulsar OptionMap instance that goes with this
        cache  : the Pulsar DataCache instance for caching deriv and wfn
        comp_hash   : the hash for the computation
        
        TODO: Save energies when higher order derivatives are requested
    """  
    threads=os.getenv("OMP_NUM_THREADS",1)
    print(threads)
    mem=64000000000
    my_mol = psr_2_psi4_mol(wfn.system)
    if my_options.get("PRINT") == 0 : psi4.be_quiet()
    
    dry_values=psi4_dryrun(wfn,my_options,cache,comp_hash)
    if dry_values != None :
        return dry_values
    
    psi4.set_nthread(int(threads))
    psi4.set_memory(mem)
    if(deriv==0):
        egy,psi4_wfn=driver.energy(method,molecule=my_mol,return_wfn=True)
        egy=[egy]
    elif(deriv==1):
        egy,psi4_wfn=driver.gradient(method,molecule=my_mol,return_wfn=True)
    elif(deriv==2):
        egy,psi4_wfn=driver.hessian(method,molecule=my_mol,return_wfn=True)
    else: raise psr.GeneralException("Psi4 doesn't support derivatives > 2")
    egy=np.asarray(egy).flatten().tolist()
    FinalWfn=psi4_wfn_2_psr(psi4_wfn)
    FinalWfn.system=wfn.system
    
    if my_options.get("PRINT") == 0 : psi4.reopen_outfile()
    cache.set(comp_hash,(FinalWfn,egy),CheckpointPolicy)
    psi4.clean()
    return FinalWfn,egy
    