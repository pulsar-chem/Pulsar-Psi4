#!/usr/bin/env python3
import os
import sys

thispath = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(thispath),"helper"))

from MiscFxns import *
from StandardModules import *
import pulsar_psi4

correct_energy=-76.26853406893483
correct_grad=[0.0002402802000335972, 0.0004993106264440486, 0.009092481746614771,
              0.005425219448594002, 0.0008833958284405264, -0.0047545452679508835,
              -0.005665499648627583, -0.0013827064548850101, -0.004337936478663376]



def Run(mm):
    try:
        tester = psr.testing.Tester("Testing Pulsar/Psi4 CCSD Interface")
        tester.print_header()
        pulsar_psi4.pulsar_psi4_setup(mm)
        LoadDefaultModules(mm)
        mm.change_option("PSI4_CCSD","BASIS_SET","aug-cc-pvdz")
        mm.change_option("PSI4_CCSD","PRINT",0)#Set to 1+ to see all the output
        mol=psr.system.make_system("""
        0 1
        O    1.2361419   1.0137761  -0.0612424
        H    0.5104418   0.8944555   0.5514190
        H    1.9926927   1.1973129   0.4956931
        """)
    
        wfn=psr.datastore.Wavefunction()
        wfn.system=mol
        MyMod=mm.get_module("PSI4_CCSD",0)
    
        NewWfn,Egy=MyMod.deriv(0,wfn)
        tester.test_value("Psi4's CCSD via deriv(0)",Egy[0],correct_energy)
        NewWfn,Egy=MyMod.energy(wfn)
        tester.test_value("Psi4's CCSD via energy()",Egy,correct_energy)
        NewWfn,Egy=MyMod.deriv(1,wfn)
        tester.test_value("Psi4's CCSD via deriv(1)",
            sum([abs(i-j) for i,j in zip(Egy,correct_grad)]),0.0)
        NewWfn,Egy=MyMod.gradient(wfn)
        tester.test_value("Psi4's CCSD via gradient()",
            sum([abs(i-j) for i,j in zip(Egy,correct_grad)]),0.0)
        
        tester.print_results()
        
    except Exception as e:
      psr.output.print_global_output("Caught exception in main handler\n")
      traceback.print_exc()

with psr.ModuleAdministrator() as mm:
    Run(mm)

psr.finalize()
