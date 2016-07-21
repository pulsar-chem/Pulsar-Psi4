import os
import sys
import pulsar as psr
thispath = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,os.path.dirname(thispath))
sys.path.insert(0,os.path.dirname(os.path.dirname(thispath)))
import PulsarPsi4Common as psr24

class SCF(psr.modulebase.EnergyMethod):
  def __init__(self, myid):
    super(SCF, self).__init__(myid)

  def deriv_(self,order,wfn):
     return psr24.psi4_call('scf',order,wfn,self.options(),self.cache(),
        self.get_hash(order,wfn)
     )
     
  def get_hash(self,order,wfn):
     return psr24.make_hash(self.options(),order,wfn,['BASIS_SET'])
      

