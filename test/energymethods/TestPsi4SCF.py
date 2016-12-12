import pulsar as psr
import pulsar_psi4 as psr4

def pulsar_psi4_setup(mm):
    """Function that loads all modules within the Psi4 supermodule
    
       The super module's name is pulsar_psi4.  All modules are then loaded
       with key PSI4_<MODULE_TYPE>.  
       
       mm (psr.modulemanager.ModuleManger) : The modulemanager we are using
    """
    mm.load_module("pulsar_psi4","DF-SCF","PSI4_SCF")
    #mm.load_module("pulsar_psi4","DF-MP2","PSI4_MP2")
    #mm.load_module("pulsar_psi4","FNO-DF-CCSD","PSI4_CCSD")
    #mm.load_module("pulsar_psi4","FNO-DF-CCSD(T)","PSI4_CCSD(T)")
correct_energy=-230.72770623626
correct_grad=[-0.001551851884294686, -0.0008507155553763301, -1.2103725748197612e-05,
              -0.00160052369435415, 0.0008928151067878476, 3.250842858604653e-05,
              1.8857531201788014e-05, -0.0017668996536486792, 1.1742224714811236e-05,
              0.00010696538521742793, 0.001797739463200998, -4.033540974242907e-05,
              0.001499137572185394, -0.0007578088475287958, -1.0294059953128718e-05,
              0.0014718360942774927, 0.0007590369820973386, 1.4457208175570478e-05,
              -0.003479951552353172, -0.00196218134373749, -1.2294200426815296e-06,
              -0.003439478023433723, 0.002018016384940924, -3.521715873901698e-06,
              -3.541990919766688e-05, -0.0040351377970400115, -4.8298425531479415e-06,
              1.6087623835401438e-05, 0.003960592135823449, 8.433356415287494e-06,
              0.003491166484349273, -0.0020466635537632616, 4.811180603295413e-06,
              0.0035031743724702746, 0.0019912066781190563, 3.617754188626023e-07]



def Run(mm):
        tester = psr.PyTester("Testing Pulsar/Psi4 SCF Interface")
        pulsar_psi4_setup(mm)
        mm.change_option("PSI4_SCF","BASIS_SET","aug-cc-pvdz")
        mm.change_option("PSI4_SCF","PRINT",0)#Set to 1+ to see all the output

        wfn=psr.Wavefunction()
        wfn.system=psr.make_system("""
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
        MyMod=mm.get_module("PSI4_SCF",0)

        NewWfn,Egy=MyMod.deriv(0,wfn)
        tester.test_double("Psi4's SCF via deriv(0)",Egy[0],correct_energy)
        NewWfn,Egy=MyMod.energy(wfn)

        tester.test_double("Psi4's SCF via energy()",Egy,correct_energy)
        NewWfn,Egy=MyMod.deriv(1,wfn)
        tester.test_double("Psi4's SCF via deriv(1)",
            sum([abs(i-j) for i,j in zip(Egy,correct_grad)]),0.0)
        NewWfn,Egy=MyMod.gradient(wfn)
        tester.test_double("Psi4's SCF via gradient()",
            sum([abs(i-j) for i,j in zip(Egy,correct_grad)]),0.0)
        
        
        tester.print_results()
        return tester.nfailed()

def run_test():
    with psr.ModuleAdministrator() as mm:
        return Run(mm)
