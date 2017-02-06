import pulsar as psr
import pulsar_psi4 as psr4


correct_energy={"MP2":-231.5384495068172,"HF":-230.72770624141242}
correct_grad=[0.006137035827856574, 0.0035173274613208502, -2.942711926490877e-06,
              0.006032365704163989, -0.003591617404611433, 1.7006549651828846e-05,
              8.308936283627335e-05, 0.007081783050386731, 3.7892862739588302e-06,
              3.4111743043508096e-05, -0.007047081488336257, -2.2646721919903712e-05,
              -0.006130238983989775, 0.003715006126424475, -2.467054965467428e-06,
              -0.006218344896395278, -0.003599559510897715, 4.632438014260271e-06,
              0.005027029643231741, 0.0028636716682285956, -1.854673220716207e-06,
              0.004994176019386391, -0.002934959973087372, -1.6137435877982482e-06,
              3.851219290886443e-05, 0.005744800745805793, -2.4843230250415453e-06,
              -5.363831770738883e-05, -0.00581875373104173, 5.078416334660975e-06,
              -0.0049421707533421205, 0.002906108710732949, 2.266812173503999e-06,
              -0.005001927540838891, -0.0028367256571535555, 1.2357261964571526e-06]



def Run(mm):
        tester = psr.PyTester("Testing Pulsar/Psi4 MP2 Interface")
        mm.load_module("pulsar_psi4","DF-SCF","PSI4_SCF")
        mm.load_module("pulsar_psi4","DF-MP2","PSI4_MP2")
        mm.change_option("PSI4_MP2","PRINT",1)#Set to 1+ to see all the output
        mol=psr.make_system("""
        0 1
        C -1.2131 -0.6884 0.0000
        C -1.2028 0.7064 0.0001
        C -0.0103 -1.3948 0.0000
        C 0.0104 1.3948 -0.0001
        C 1.2028 -0.7063 0.0000
        C 1.2131 0.6884 0.0000
        H -2.1577 -1.2244 0.0000
        H -2.1393 1.2564 0.0001
        H -0.0184 -2.4809 -0.0001
        H 0.0184 2.4808 0.0000
        H 2.1394 -1.2563 0.0001
        H 2.1577 1.2245 0.0000
        """)
    
        wfn=psr.Wavefunction()
        wfn.system=psr.apply_single_basis("PRIMARY","aug-cc-pvdz",mol)

        MyMod=mm.get_module("PSI4_MP2",0)
        MySCFMod=mm.get_module("PSI4_SCF",0)
    
        NewWfn,Egy=MyMod.deriv(0,wfn)
        tester.test_double("Psi4's MP2 via deriv(0)",Egy[0],correct_energy["MP2"])
        SCFWfn,SCFEgy=MySCFMod.deriv(0,wfn)
        tester.test_double("Psi4's HF via deriv(0)",SCFEgy[0],correct_energy["HF"])
        NewWfn,Egy=MyMod.energy(wfn)
        tester.test_double("Psi4's MP2 via energy()",Egy,correct_energy["MP2"])
        SCFWfn,SCFEgy=MySCFMod.energy(wfn)
        tester.test_double("Psi4's HF via energy()",SCFEgy,correct_energy["HF"])
        NewWfn,Egy=MyMod.deriv(1,wfn)
        tester.test_double("Psi4's MP2 via deriv(1)",
            sum([abs(i-j) for i,j in zip(Egy,correct_grad)]),0.0)
        NewWfn,Egy=MyMod.gradient(wfn)
        tester.test_double("Psi4's MP2 via gradient()",
            sum([abs(i-j) for i,j in zip(Egy,correct_grad)]),0.0)
        
        tester.print_results()
        return tester.nfailed()

def run_test():
    with psr.ModuleAdministrator() as mm:
        return Run(mm)
