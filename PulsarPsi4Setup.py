def pulsar_psi4_setup(mm):
    mm.load_module("pulsar_psi4","SCF","PSI4_SCF")
    mm.load_module("pulsar_psi4","MP2","PSI4_MP2")
    mm.load_module("pulsar_psi4","CCSD","PSI4_CCSD")
    mm.load_module("pulsar_psi4","CCSD(T)","PSI4_CCSD(T)")
    
