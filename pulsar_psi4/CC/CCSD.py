import os
import sys
import pulsar as psr
thispath = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,os.path.dirname(thispath))
sys.path.insert(0,os.path.dirname(os.path.dirname(thispath)))
import psi4
import PulsarPsi4Common as psr24

class DF_CCSD_Guts:
    def get_hash(self,order,wfn):
        return psr24.make_hash(self.options(),order,wfn,
            ['BASIS_SET','FROZEN_CORE','MP2_KEY']
        )
        
    def run_sub_calls(self,order,wfn):
        MP2=self.create_child(self.options().get('MP2_KEY'))
        return MP2.deriv_(order,wfn)


class DF_CCSD(psr.modulebase.EnergyMethod,DF_CCSD_Guts):
    def __init__(self, myid):
        super(DF_CCSD, self).__init__(myid)

    def deriv_(self,order,wfn):
        self.run_sub_calls(order,wfn)
        FinalWfn,Egy=psr24.psi4_call('fno-ccsd',order,wfn,self.options(),self.cache(),
            self.get_hash(order,wfn)
        )
        self.run_sub_calls(order,wfn)
        return FinalWfn,Egy
        
class DF_CCSD_Dry(psr.modulebase.EnergyMethod,DF_CCSD_Guts):
    def __init__(self,myid):
       super(DF_CCSD_Dry,self).__init__(myid)
    
    def deriv_(self,order,wfn):
        self.run_sub_calls(order,wfn)
        return psr24.psi4_dryrun(wfn,self.options(),self.cache(),
           self.get_hash(order,wfn),"CCSD TOTAL ENERGY")
    