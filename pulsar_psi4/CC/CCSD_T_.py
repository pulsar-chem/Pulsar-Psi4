import os
import sys
import pulsar as psr
thispath = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,os.path.dirname(thispath))
sys.path.insert(0,os.path.dirname(os.path.dirname(thispath)))
import PulsarPsi4Common as psr24

class DF_CCSD_T_Guts:
    def get_hash(self,order,wfn):
        return psr24.make_hash(self.options(),order,wfn,
            ['BASIS_SET','FROZEN_CORE','CCSD_KEY']
        )
        
    def run_sub_calls(self,order,wfn):
        CCSD=self.create_child_from_option('CCSD_KEY')
        CCSD.options().change("IS_DRY",True)
        return CCSD.deriv(order,wfn)

class DF_CCSD_T_(psr.EnergyMethod,DF_CCSD_T_Guts):
    def __init__(self, myid):
        super(DF_CCSD_T_, self).__init__(myid)

    def deriv_(self,order,wfn):
        self.run_sub_calls(order,wfn)
        FinalWfn,Egy=psr24.psi4_call('fno-ccsd(t)',order,wfn,self.options(),
           self.cache(),self.get_hash(order,wfn))
        self.run_sub_calls(order,wfn)
        psr24.psi4_clean()
        return FinalWfn,Egy

