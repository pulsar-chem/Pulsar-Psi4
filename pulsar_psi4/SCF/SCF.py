import os
import sys
import pulsar as psr
thispath = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,os.path.dirname(thispath))
sys.path.insert(0,os.path.dirname(os.path.dirname(thispath)))
import PulsarPsi4Common as psr24

class SCF_Guts:
    IsDry_=False
    def get_hash(self,order,wfn):
        return psr24.make_hash(self.options(),order,wfn,['BASIS_SET'])

class SCF(psr.modulebase.EnergyMethod,SCF_Guts):
  def __init__(self, myid):
    super(SCF, self).__init__(myid)

  def deriv_(self,order,wfn):
     if self.options().get("IS_DRY"):
        return psr24.psi4_dryrun(wfn,self.options(),self.cache(),
                              self.get_hash(order,wfn),"HF TOTAL ENERGY") 
     dawfn,egy=psr24.psi4_call('scf',order,wfn,self.options(),self.cache(),
        self.get_hash(order,wfn))
     psr24.psi4_clean()
     return dawfn,egy    
      

