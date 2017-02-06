import os
import sys

thispath = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,os.path.dirname(thispath))
import psi4.core as psi4
from psi4 import driver
import pulsar as psr
import numpy as np
from Pulsar2Psi4Options import *
from mints2pulsar.molecule import *
from mints2pulsar.wavefunction import *
CheckpointPolicy=psr.CacheData.CheckpointGlobal|psr.CacheData.CheckpointLocal

def make_hash(my_options,order,wfn,opts):
    """Code factorization of the process of making hashes for Psi4 computations.
    Using this function also ensures all hashes are made consistently.
    
    my_options (psr.datastore.OptionMap) : This module's full set of options
    order (int) : Which derivative are we computing?
    wfn (psr.datastore.Wavefunction) : The wavefunction for this system
    opts (list of strings) : The options that actually affect the energy
    """
    option_hash=my_options.hash_values({i for i in opts})
    sys_hash=wfn.system.my_hash()
    return str((order,sys_hash,option_hash))    

def psi4_set_options(my_options,mod_name,wfn):
    for i in my_options.get_keys():
        opt=""
        if mod_name in pulsar_2_psi4 and i in pulsar_2_psi4[mod_name]:
            opt=pulsar_2_psi4[mod_name][i]
        elif i in pulsar_2_psi4["GLOBAL"]:
            opt=pulsar_2_psi4["GLOBAL"][i]
        else: continue
        da_opt=my_options.get(i)
        if i=="BASIS_SET":
            bs_name=wfn.system.as_universe()[0].basis_sets[da_opt].description
            psi4.set_global_option(opt,bs_name)
        else:psi4.set_global_option(opt,da_opt)

def psi4_dryrun(wfn,my_options,cache,comp_hash,psi_variable=None):
    """
    This function mock runs a Psi4 call as if Psi4 obeyed the Pulsar framework
    API fully.  More specifically, it checks the cache for an answer, if it
    finds it, it then returns it, otherwise it skims the Psi variables.
    See [Using the Cache with Psi4](@ref cacheing) for more details.

    NOTE: We don't want, for example, CCSD to have to know that it contains MP2
    and HF because MP2 knows it contains HF.  Instead, we only want CCSD to
    deal with the fact that it contains MP2.  Furthermore, Psi4 needs all
    options set at the begining so each module has to do this through the only
    call it has, i.e. the deriv function, that function ultimately calls this
    function, so this function also has to set the options.  This isn't ideal,
    but the alternative is having every method know all submethods it contains,
    which I like less...
   
    wfn (psr.datastore.wavefunction) : the wavefunction to cache
    my_options (psr.datastore.OptionMap) : the options, in Pulsar format
    cache (psr.datastore.CacheData) : the cache for this module
    comp_hash (string) : the hash of this computation
    psi_variable (string) : the Psi variable Psi4 uses for this energy quantity
    
    NOTE: Only energies work.  To my knowledge Psi4 doesn't support getting say
    the HF component of the MP2 gradient.
    """
    
    out=psr.get_global_output()
    data=cache.get(comp_hash,True)
    if data: return data
    out.debug("Did not use cached value for: "+psi_variable+"\n")
    if psi_variable and psi4.has_variable(psi_variable):
        Egy=psi4.get_variable(psi_variable)
        data=(wfn,[Egy])
        cache.set(comp_hash,data,CheckpointPolicy)
        return cache.get(comp_hash,True)
    return wfn,[]

def psi4_clean():
    """Function to put Psi4 back to a clean state.  In particular deletes
       scratch files and resets Psi variables.  Call as last part of the real
       deriv call to Psi4.
    """
    psi4.clean_variables()
    psi4.clean()
    
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
    my_mol = psr_2_psi4_mol(wfn.system)
    if my_options.get("PRINT") == 0 : psi4.be_quiet()
    

    data=cache.get(comp_hash,True)
    if data: return data
    psr.print_global_debug("Cache miss in: "+method+"\n")
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
    data=(FinalWfn,egy)
    cache.set(comp_hash,data,CheckpointPolicy)
    return FinalWfn,egy
    
