def pulsar_psi4_setup(mm):
    """Function that loads all modules within the Psi4 supermodule
    
       The super module's name is pulsar_psi4.  All modules are then loaded
       with key's PSI4_<MODULE_TYPE>.  If a dry version is available for that
       module, i.e. it is a submodule of another module, the above rules apply
       but have _DRY appended to the key and module type.
       
       mm (psr.modulemanager.ModuleManger) : The modulemanager we are using
    """
    mm.load_module("pulsar_psi4","DF-SCF","PSI4_SCF")
    mm.load_module("pulsar_psi4","DF-MP2","PSI4_MP2")
    mm.load_module("pulsar_psi4","FNO-DF-CCSD","PSI4_CCSD")
    mm.load_module("pulsar_psi4","FNO-DF-CCSD(T)","PSI4_CCSD(T)")
    
