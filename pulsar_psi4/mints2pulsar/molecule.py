import psi4.core as psi4
from psi4.driver.qmmm import *
import pulsar as psr

def psr_2_psi4_mol(PsrMol):
    """Converts the pulsar molecule into a Psi4 molecule
       TODO: Add symmetry
    """
    mol_string="no_com\nno_reorient\nunits bohr\nsymmetry c1\n"\
       +str(int(PsrMol.charge))+" "+str(int(PsrMol.multiplicity))\
       +"\n"
    charges = QMMM()
    has_charges = False
    for atom in PsrMol:
        if not psr.is_point_charge(atom):
            mol_string+=psr.atomic_symbol_from_z(atom.Z)+" "+\
                str(atom[0])+" "+str(atom[1])+" "+str(atom[2])+"\n"
        else:
           has_charges = True
           charges.extern.addCharge(atom.charge,atom[0],atom[1],atom[2])
    if has_charges:
        psi4.set_global_option_python('EXTERN',charges.extern)
    return psi4.Molecule.create_molecule_from_string(mol_string)
