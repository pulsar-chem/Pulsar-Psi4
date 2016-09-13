from .SCF import SCF
from .MP2 import MP2
from .CC import CCSD
from .CC import CCSD_T_

from pulsar.modulemanager import ModuleCreationFuncs

def insert_supermodule():
    cf = ModuleCreationFuncs()
    cf.add_py_creator("DF-SCF", SCF.SCF)
    cf.add_py_creator("DF-MP2",MP2.MP2)
    cf.add_py_creator("FNO-DF-CCSD",CCSD.DF_CCSD)
    cf.add_py_creator("FNO-DF-CCSD(T)",CCSD_T_.DF_CCSD_T_)
    return cf
