import pulsar as psr
import pulsar_psi4 as psr4

correct_energy={"CCSD":-76.268636061439,
                "MP2":-76.260764521668,
                "HF":-76.041427954977}
                
correct_grad=[0.0002402802000335972, 0.0004993106264440486, 0.009092481746614771,
              0.005425219448594002, 0.0008833958284405264, -0.0047545452679508835,
              -0.005665499648627583, -0.0013827064548850101, -0.004337936478663376]



def Run(mm):
        tester = psr.PyTester("Testing Pulsar/Psi4 CCSD Interface")
        mm.load_module("pulsar_psi4","DF-SCF","PSI4_SCF")
        mm.load_module("pulsar_psi4","DF-MP2","PSI4_MP2")
        mm.load_module("pulsar_psi4","FNO-DF-CCSD","PSI4_CCSD")
        mm.change_option("PSI4_CCSD","PRINT",1)#Set to 1+ to see all the output
        mol=psr.make_system("""
        0 1
        O    1.2361419   1.0137761  -0.0612424
        H    0.5104418   0.8944555   0.5514190
        H    1.9926927   1.1973129   0.4956931
        """)
    
        wfn=psr.Wavefunction()
        wfn.system=psr.apply_single_basis("PRIMARY","aug-cc-pvdz",mol)
        MyMod=mm.get_module("PSI4_CCSD",0)
        MyHFMod=mm.get_module("PSI4_SCF",0)
        MyMP2Mod=mm.get_module("PSI4_MP2",0)
        
        NewWfn,Egy=MyMod.deriv(0,wfn)
        tester.test_double("Psi4's CCSD via deriv(0)",Egy[0],correct_energy["CCSD"])
        NewWfn,Egy=MyMP2Mod.deriv(0,wfn)
        tester.test_double("Psi4's MP2 via deriv(0)",Egy[0],correct_energy["MP2"])
        NewWfn,Egy=MyHFMod.deriv(0,wfn)
        tester.test_double("Psi4's HF via deriv(0)",Egy[0],correct_energy["HF"])
        
        NewWfn,Egy=MyMod.energy(wfn)
        tester.test_double("Psi4's CCSD via energy()",Egy,correct_energy["CCSD"])
        NewWfn,Egy=MyMP2Mod.energy(wfn)
        tester.test_double("Psi4's MP2 via energy()",Egy,correct_energy["MP2"])
        NewWfn,Egy=MyHFMod.energy(wfn)
        tester.test_double("Psi4's HF via energy()",Egy,correct_energy["HF"])
        
        NewWfn,Egy=MyMod.deriv(1,wfn)
        tester.test_double("Psi4's CCSD via deriv(1)",
            sum([abs(i-j) for i,j in zip(Egy,correct_grad)]),0.0)
        NewWfn,Egy=MyMod.gradient(wfn)
        tester.test_double("Psi4's CCSD via gradient()",
            sum([abs(i-j) for i,j in zip(Egy,correct_grad)]),0.0)
        
        tester.print_results()
        return tester.nfailed()

def run_test():
    with psr.ModuleAdministrator() as mm:
        return Run(mm)
