import pulsar as psr
OT_Bool,OT_Int,OT_Float,OT_String=psr.OptionType.Bool,psr.OptionType.Int,\
                                  psr.OptionType.Float,psr.OptionType.String

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
   "BASIS_SET":(OT_String,"PRIMARY",False,None,"The key for the basis set"),
   "IS_DRY":(OT_Bool,False,False,None,"Will this computation really run?"),
   "PRINT":(OT_Int,1,False,None,"The printing level for Psi4"),
   "JK_BUILD_KEY":(OT_String,"DF",False,None,"The key for the JK builder"),
   "MAX_ITER":(OT_Int,100,False,None,
         'Maximum number of iterations HF may use'),
   "EGY_TOLERANCE":(OT_Float,1.0e-6,False,None,
         "The convergence criteria for the energy"),
   "DENS_TOLERANCE":(OT_Float,1.0e-6,False,None,
          "The convergence criteria for the density"),
   "KEY_INITIAL_GUESS":(OT_String,"SAD",False,None,
          "The manner in which the first density is generated"),
   "DAMPING_FACTOR":(OT_Float,0.0,False,None,
           "The amount of the previous density to mix in"),
   "GUESS":(OT_String,"SAD",False,None,"How to form the initial density"),
   "MAX_DERIV":(OT_Int,2,False,None,'Max analytic derivative')
}

CorrOptions={
  "BASIS_SET":(OT_String,"PRIMARY",False,None,"The key for the basis set"),
  "IS_DRY":(OT_Bool,False,False,None,"Will this computation really run?"),
  "PRINT":(OT_Int,1,False,None,"The printing level for Psi4"),
  "FROZEN_CORE":(OT_String,"TRUE",False,None,"Are we freezing the core?"),
  "MAX_DERIV":(OT_Int,2,False,None,'Max analytic derivative'),
  "JK_BUILD_KEY":(OT_String,"DF",False,None,"The key for the JK builder")
}


minfo['DF-MP2']['options']=CorrOptions.copy()
minfo['DF-MP2']['options']["SCF_KEY"]=(
    OT_String,"PSI4_DF_SCF",False,None,"The SCF module providing the reference")

minfo['FNO-DF-CCSD']['options']=CorrOptions.copy()
minfo['FNO-DF-CCSD']['options']["MP2_KEY"]=(
    OT_String,"PSI4_DF_MP2",False,None,"The MP2 module used to generate the "\
                  "initial T2 amplitudes")
  
  
minfo['FNO-DF-CCSD(T)']['options']=CorrOptions.copy()
minfo['FNO-DF-CCSD(T)']['options']["CCSD_KEY"]=(OT_String,"PSI4_DF_FNO_CCSD",False,
    None,"The CCSD module used to generate the T1 and T2 amplitudes")

