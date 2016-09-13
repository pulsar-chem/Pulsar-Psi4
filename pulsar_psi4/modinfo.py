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
   'DF-SCF':make_psi4_entry('DF-SCF'),
   'DF-MP2':make_psi4_entry('DF-MP2'),
   'FNO-DF-CCSD':make_psi4_entry('FNO-DF-CCSD'),
   'FNO-DF-CCSD(T)':make_psi4_entry('FNO-DF-CCSD(T)')
}

minfo['DF-SCF']['options']={
   "IS_DRY":(OptionType.Bool,False,False,None,"Will this computation really run?"),
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

CorrOptions={
   "IS_DRY":(OptionType.Bool,False,False,None,"Will this computation really run?"),
  "PRINT":(OptionType.Int,1,False,None,"The printing level for Psi4"),
  "FROZEN_CORE":(OptionType.String,"TRUE",False,None,"Are we freezing the core?"),
}

CCOptions={  
   "cc_type":(OptionType.String,"DF",False,None,"Are we using density fitting?"),
}

minfo['DF-MP2']['options']=CorrOptions.copy()
minfo['DF-MP2']['options']["SCF_KEY"]=(OptionType.String,"PSI4_SCF",False,None,"The SCF module providing the reference")

minfo['FNO-DF-CCSD']['options']=CorrOptions.copy()
minfo['FNO-DF-CCSD']['options'].update(CCOptions)
minfo['FNO-DF-CCSD']['options']["MP2_KEY"]=(OptionType.String,"PSI4_MP2",False,None,"The MP2 module used to generate the initial T2 amplitudes")
  
  
minfo['FNO-DF-CCSD(T)']['options']=CorrOptions.copy()
minfo['FNO-DF-CCSD(T)']['options'].update(CCOptions)
minfo['FNO-DF-CCSD(T)']['options']["CCSD_KEY"]=(OptionType.String,"PSI4_CCSD",False,None,"The CCSD module used to generate the T1 and T2 amplitudes")

