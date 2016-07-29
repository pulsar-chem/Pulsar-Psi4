from pulsar.datastore import OptionType
from pulsar.datastore.OptionValidators import *

def make_psi4_entry(MethName):
    return {
      "type" : "python_module",
      "base" : "EnergyMethod",
      "version" : "0.1a",
      "authors"     : ["Psi4 authors"],
      "refs"        : [""],
      "description" : "Computes a "+MethName+" derivative"}

minfo = {
   'SCF':make_psi4_entry('SCF'),
   'SCF_DRY':make_psi4_entry('SCF_DRY'),
   'MP2':make_psi4_entry('MP2'),
   'MP2_DRY':make_psi4_entry('MP2_DRY'),
   'CCSD':make_psi4_entry('CCSD'),
   'CCSD_DRY':make_psi4_entry('CCSD_DRY'),
   'CCSD(T)':make_psi4_entry('CCSD(T)')
}

minfo['SCF']['options']={
   "PRINT":(OptionType.Int,1,False,None,"The printing level for Psi4"),
   "MAX_ITER":(OptionType.Int,100,False,None,
         'Maximum number of iterations HF may use'),
   "EGY_TOLERANCE":(OptionType.Float,1.0e-6,False,None,
         "The convergence criteria for the energy"),
   "DENS_TOLERANCE":(OptionType.Float,1.0e-6,False,None,
          "The convergence criteria for the density"),
   "KEY_INITIAL_GUESS":(OptionType.String,"SAD",False,None,
          "The manner in which the first density is generated"),
   "DAMPING_FACTOR":(OptionType.Float,0.0,False,None,
           "The amount of the previous density to mix in"),
   "GUESS":(OptionType.String,"SAD",False,None,"How to form the initial density"),
   "MAX_DERIV":(OptionType.Int,2,False,None,'Max analytic derivative')
}
minfo['SCF_DRY']['options']=minfo['SCF']['options']

CorrOptions={
  "PRINT":(OptionType.Int,1,False,None,"The printing level for Psi4"),
  "FROZEN_CORE":(OptionType.String,"TRUE",False,None,"Are we freezing the core?"),
}

CCOptions={  
   "cc_type":(OptionType.String,"DF",False,None,"Are we using density fitting?"),
}


minfo['MP2']['options']=CorrOptions.copy()
minfo['MP2']['options']["SCF_KEY"]=(OptionType.String,"PSI4_SCF_DRY",False,None,"The SCF module providing the reference")

minfo['MP2_DRY']['options']=minfo['MP2']['options']

minfo['CCSD']['options']=CorrOptions.copy()
minfo['CCSD']['options'].update(CCOptions)
minfo['CCSD']['options']["MP2_KEY"]=(OptionType.String,"PSI4_MP2_DRY",False,None,"The MP2 module used to generate the initial T2 amplitudes")
minfo['CCSD_DRY']['options']=minfo['CCSD']['options']
  
  
minfo['CCSD(T)']['options']=CorrOptions.copy()
minfo['CCSD(T)']['options'].update(CCOptions)
minfo['CCSD(T)']['options']["CCSD_KEY"]=(OptionType.String,"PSI4_CCSD_DRY",False,None,"The CCSD module used to generate the T1 and T2 amplitudes")

