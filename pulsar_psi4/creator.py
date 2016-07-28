from .SCF import SCF
from .MP2 import MP2
from .CC import CCSD
from .CC import CCSD_T_

from pulsar.modulemanager import ModuleCreationFuncs

def insert_supermodule():
    cf = ModuleCreationFuncs()
    cf.add_py_creator("SCF", SCF.SCF)
    cf.add_py_creator("SCF_DRY",SCF.SCF_Dry)
    cf.add_py_creator("MP2",MP2.MP2)
    cf.add_py_creator("MP2_DRY",MP2.MP2_Dry)
    cf.add_py_creator("CCSD",CCSD.DF_CCSD)
    cf.add_py_creator("CCSD_DRY",CCSD.DF_CCSD_Dry)
    cf.add_py_creator("CCSD(T)",CCSD_T_.DF_CCSD_T_)
    return cf
