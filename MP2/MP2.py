import os
import sys
import pulsar as psr
thispath = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,os.path.dirname(thispath))
sys.path.insert(0,os.path.dirname(os.path.dirname(thispath)))
import PulsarPsi4Common as psr24

class MP2(psr.modulebase.EnergyMethod):
    def __init__(self, myid):
        super(MP2, self).__init__(myid)

    def deriv_(self,order,wfn):
        return psr24.psi4_call('mp2',order,wfn,self.options(),self.cache(),
            self.get_hash(order,wfn)
        )

    def get_hash(self,order,wfn):
        return psr24.make_hash(self.options(),order,wfn,
            ['BASIS_SET','FROZEN_CORE']
        )
      