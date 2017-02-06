import os
import sys
import pulsar as psr
thispath = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,os.path.dirname(thispath))
sys.path.insert(0,os.path.dirname(os.path.dirname(thispath)))
import PulsarPsi4Common as psr24

class MP2_Guts:
    def get_hash(self,order,wfn):
        return psr24.make_hash(self.options(),order,wfn,
            ['BASIS_SET','FROZEN_CORE','SCF_KEY']
        )

    def run_sub_calls(self,order,wfn):
        scf=self.create_child_from_option('SCF_KEY')
        scf.options().change("IS_DRY",True)
        return scf.deriv_(order,wfn)

class MP2(psr.EnergyMethod,MP2_Guts):
    def __init__(self, myid):
        super(MP2, self).__init__(myid)

    def deriv_(self,order,wfn):
        self.run_sub_calls(order,wfn)
        psr24.psi4_set_options(self.options(),"DF-MP2",wfn)
        if self.options().get("IS_DRY"):
            my_hash=self.get_hash(order,wfn)
            return psr24.psi4_dryrun(wfn,self.options(),self.cache(),
                                     my_hash,"MP2 TOTAL ENERGY")
        FinalWfn,Egy=psr24.psi4_call('mp2',order,wfn,self.options(),
           self.cache(),self.get_hash(order,wfn))
        self.run_sub_calls(order,wfn)
        psr24.psi4_clean()
        return FinalWfn,Egy
