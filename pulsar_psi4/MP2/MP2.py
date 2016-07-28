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
        scf=self.create_child(self.options().get('SCF_KEY'))
        return scf.deriv_(order,wfn)

class MP2(psr.modulebase.EnergyMethod,MP2_Guts):
    def __init__(self, myid):
        super(MP2, self).__init__(myid)

    def deriv_(self,order,wfn):
        self.run_sub_calls(order,wfn)
        FinalWfn,Egy=psr24.psi4_call('mp2',order,wfn,self.options(),
           self.cache(),self.get_hash(order,wfn))
        self.run_sub_calls(order,wfn)
        return FinalWfn,Egy

class MP2_Dry(psr.modulebase.EnergyMethod,MP2_Guts):
    def __init__(self,myid):
        super(MP2_Dry,self).__init__(myid)
    
    def deriv_(self,order,wfn):
        self.run_sub_calls(order,wfn)
        return psr24.psi4_dryrun(wfn,self.options(),self.cache(),
           self.get_hash(order,wfn),"MP2 TOTAL ENERGY")