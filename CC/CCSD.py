import os
import sys
import pulsar as psr
thispath = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,os.path.dirname(thispath))
sys.path.insert(0,os.path.dirname(os.path.dirname(thispath)))
import psi4
import PulsarPsi4Common as psr24

class DF_CCSD(psr.modulebase.EnergyMethod):
    def __init__(self, myid):
        super(DF_CCSD, self).__init__(myid)

    def deriv_(self,order,wfn):
        return psr24.psi4_call('fno-ccsd',order,wfn,self.options(),self.cache(),
            self.get_hash(order,wfn)
        )

    def get_hash(self,order,wfn):
        return psr24.make_hash(self.options(),order,wfn,
            ['BASIS_SET','FROZEN_CORE']
        )
