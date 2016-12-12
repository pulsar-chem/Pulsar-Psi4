import psi4.core as psi4
import pulsar as psr

def psr_2_psi4_mol(PsrMol):
    """Converts the pulsar molecule into a Psi4 molecule
       TODO: Add symmetry
    """
    mol_string="no_com\nno_reorient\nunits bohr\nsymmetry c1\n"\
       +str(int(PsrMol.charge))+" "+str(int(PsrMol.multiplicity))\
       +"\n"
    for atom in PsrMol:
        mol_string+=psr.atomic_symbol_from_z(atom.Z)+" "+\
           str(atom[0])+" "+str(atom[1])+" "+str(atom[2])+"\n"

    return psi4.Molecule.create_molecule_from_string(mol_string)
