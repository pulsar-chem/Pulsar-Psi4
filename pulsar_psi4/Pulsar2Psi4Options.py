#A map of pulsar options to Psi4 options
#For the most part PSI4 does not include namespaces in option names, i.e.
#they don't have things like SCF_E_CONVERGENCE, etc.
#there are a few cases where they fail on this, such as determining how the
#2 electron repulsion integrals are built
#
#What we have done here is made a dictionary of Pulsar 2 Psi4 names, first
#sorted by the Psi4 namespace (Global meaning the option is good regardless of
#the method) otherwise there is a dictionary for each namespace protected
#variable
pulsar_2_psi4={"GLOBAL":{ #Global in the sense they are not module specific
   "BASIS_SET":"BASIS",
   "DAMPING_FACTOR":"DAMPING_PERCENTAGE",
   "DENS_TOLERANCE":"D_CONVERGENCE",
   "EGY_TOLERANCE":"E_CONVERGENCE",
   "FITTING_BASIS":"DF_BASIS_SCF",
   "FROZEN_CORE":"FREEZE_CORE",
   "GUESS":"GUESS",
   "JK_BUILD_KEY":"SCF_TYPE",
   "KEY_INITIAL_GUESS":"GUESS",
   "MAX_ITER": "MAXITER",
   "cc_type":"cc_type",
   #"MAX_DERIV":"DERIV" Does Psi4 have this?
   },#End Global
   "FNO-DF-CCSD":{"JK_BUILD_TYPE":"CC_TYPE"},
   "FNO-DF-CCSD(T)":{"JK_BUILD_TYPE":"CC_TYPE"},
}
