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
   'MP2':make_psi4_entry('MP2'),
   'CCSD':make_psi4_entry('CCSD'),
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

#Because of how Psi4 works need to forward
CorrelationOptions={
  "PRINT":(OptionType.Int,1,False,None,"The printing level for Psi4"),
  "FROZEN_CORE":(OptionType.String,"TRUE",False,None,"Are we freezing the core?"),
  "cc_type":(OptionType.String,"DF",False,None,"Are we using density fitting?")
}


minfo['MP2']['options']=CorrelationOptions
minfo['CCSD']['options']=CorrelationOptions
minfo['CCSD(T)']['options']=CorrelationOptions

