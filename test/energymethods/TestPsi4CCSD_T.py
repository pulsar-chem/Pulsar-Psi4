import pulsar as psr
import pulsar_psi4 as psr4

correct_energy=-76.273740284068
scf_corr_egy=-76.0414279550684569
mp2_corr_egy=-76.260764556606
mp3_corr_egy=-76.265524879741
ccsd_corr_egy=-76.268534035737
correct_grad=[0.00031057995481974883, 0.0006456409547574079, 0.011757658755370302,
              0.0067916083168123075, 0.0010965967413910217, -0.00613982532982517,
              -0.007102188271632036, -0.0017422376961489922, -0.005617833425544473]



def Run(mm):
        tester = psr.PyTester("Testing Pulsar/Psi4 CCSD(T) Interface")
        mm.load_module("pulsar_psi4","DF-SCF","PSI4_SCF")
        mm.load_module("pulsar_psi4","DF-MP2","PSI4_MP2")
        mm.load_module("pulsar_psi4","FNO-DF-CCSD","PSI4_CCSD")
        mm.load_module("pulsar_psi4","FNO-DF-CCSD(T)","PSI4_CCSD(T)")
        mm.change_option("PSI4_CCSD(T)","BASIS_SET","aug-cc-pvdz")
        mm.change_option("PSI4_CCSD(T)","PRINT",0)#Set to 1+ to see all the output
        mol=psr.make_system("""
        0 1
        O    1.2361419   1.0137761  -0.0612424
        H    0.5104418   0.8944555   0.5514190
        H    1.9926927   1.1973129   0.4956931
        """)
    
        wfn=psr.Wavefunction()
        wfn.system=mol
        MyMod=mm.get_module("PSI4_CCSD(T)",0)
        MyMP2Mod=mm.get_module("PSI4_MP2",0)
        MySCFMod=mm.get_module("PSI4_SCF",0)
    
        NewWfn,Egy=MyMod.deriv(0,wfn)
        tester.test_double("Psi4's CCSD(T) via deriv(0)",Egy[0],correct_energy)
        NewWfn,Egy=MyMP2Mod.deriv(0,wfn)
        tester.test_double("Psi4's CCSD(T)'s MP2 via deriv(0)",Egy[0],mp2_corr_egy)
        NewWfn,Egy=MyMP2Mod.deriv(0,wfn)
        tester.test_double("Psi4's CCSD(T)'s SCF via deriv(0)",Egy[0],scf_corr_egy)
        NewWfn,Egy=MyMod.energy(wfn)
        tester.test_double("Psi4's CCSD(T) via energy()",Egy,correct_energy)
        NewWfn,Egy=MyMod.energy(wfn)
        tester.test_double("Psi4's CCSD(T)'s MP2 via energy()",Egy,mp2_corr_egy)
        NewWfn,Egy=MyMod.energy(wfn)
        tester.test_double("Psi4's CCSD(T)'s SCF via energy()",Egy,scf_corr_egy)
        NewWfn,Egy=MyMod.deriv(1,wfn)
        tester.test_double("Psi4's CCSD(T) via deriv(1)",
            sum([abs(i-j) for i,j in zip(Egy,correct_grad)]),0.0)
        NewWfn,Egy=MyMod.gradient(wfn)
        tester.test_double("Psi4's CCSD(T) via gradient()",
            sum([abs(i-j) for i,j in zip(Egy,correct_grad)]),0.0)
        
        tester.print_results()
        return tester.nfailed()

def run_test():
    with psr.ModuleAdministrator() as mm:
        return Run(mm)

