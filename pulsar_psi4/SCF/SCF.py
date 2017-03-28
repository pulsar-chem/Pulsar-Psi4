import os
import sys
thispath = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,os.path.dirname(thispath))
sys.path.insert(0,os.path.dirname(os.path.dirname(thispath)))
import PulsarPsi4Common as psr24
import pulsar as psr

class SCF_Guts:
    IsDry_=False
    def get_hash(self,order,wfn):
        return psr24.make_hash(self.options(),order,wfn,['BASIS_SET'])

class SCF(psr.EnergyMethod,SCF_Guts):
  def dry_run(self,order,wfn):
      my_hash=self.get_hash(order,wfn)
      return psr24.psi4_dryrun(wfn,self.options(),self.cache(),
                               my_hash,"HF TOTAL ENERGY")

  def __init__(self, myid):
    super(SCF, self).__init__(myid)

  def deriv_(self,order,wfn):
     psr24.psi4_set_options(self.options(),"DF-SCF",wfn)
     if self.options().get("IS_DRY"):
         return self.dry_run(order,wfn)
     dawfn,egy=psr24.psi4_call('scf',order,wfn,self.options(),self.cache(),
        self.get_hash(order,wfn))
     if order==1: #Save the energy
        self.dry_run(order,wfn)
     psr24.psi4_clean()
     return dawfn,egy    
      

