import psi4.core as psi4
import pulsar as psr

def psr_2_psi4_bs(wfn,psi4_mol,bs_key):
    """Converts the pulsar basis into a vector of shells needed to make Psi4
       basis
       
       So the real trick here is figuring out how to build a Psi4 basis that
       doesn't go through all of their file parsing machinery.  The ultimate
       class we need to build is psi4::BasisSet.  this can be built in three
       ways:
           1. BasisSet(type(string),mol,
              shell_map(map<string,vector<ShellInfo>)
           2. build(mol,vector<ShellInfo>)
           3. construct_from_pydict(mol,dict(pybind11::dict),puream(bool))
              - W/o reverse engineering the code I have no idea what's in
                the dictionary
       in all of these ways mol is a psi4::Molecule instance, which we know
       how to make from our psr_2_psi4_mol function.  Ignoring 3 for the
       moment, the task is to figure out how to make a ShellInfo instance.
       This class is relatively straightforward, we need:
           1. angular momentum (int)
           2. contraction coeficients (vector<double>)
           3. exponents (vector<double>)
           4. pure or cartesian (psi4::GaussianType)
           5. atom center (int)
           6. position of center (psi4::Vector3)
           7. starting position (int)
           8. is shell normalized (psi4::PrimitiveType)

       Nevermind...somehow the static member build maps to pybuild_basis,
       which in turn has a completely different signature.


       wfn : the pulsar wavefunction to convert
       bs_key : the key for the pulsar basis to use
    """
    PsrBS=wfn.system.get_basis_set(bs_key)
    p4_pure,p4_cart=psi4.GaussianType.Pure, \
                    psi4.GaussianType.Cartesian
    psr_pure=psr.ShellType.SphericalGaussian
    pt_unorm=psi4.PrimitiveType.Unnormalized
    nbf=0
    shells=[]
    for counter,bf in enumerate(PsrBS):
        psi4_type=p4_pure if bf.get_type()==psr_pure else p4_cart
        psr_c,psr_e=bf.get_coefs(0),bf.get_alphas()
        vec3=psi4.Vector3(bf.get_coords()[0],bf.get_coords()[1],bf.get_coords()[2])
        shells.append(psi4.ShellInfo(bf.am(),psr_c,psr_e,psi4_type,counter,
                      vec3,nbf,pt_unorm))
        nbf+=bf.n_functions()
    return psi4.BasisSet.build(psi4_mol,shells)
