# Pulsar-Psi4
The Psi4 supermodule for use with the Pulsar framework.

##Supported Methods
At the moment the following methods from Psi4 work with Pulsar:
- DF-SCF
- DF-MP2
- FNO-DF-CCSD
- FNO-DF-CCSD(T)

##Compatibility Level
All Psi4 modules interact with Pulsar very simply.  Specifically they only work
as EnergyMethods.  This means attempting to change the keys, for say the Fock
builder, will not lead to any difference.  Furthermore, we cheat a bit on
setting Psi4 options.  Specifically, instead of using the basis set key to get
the basis from Pulsar, we just push the basis key to Psi4.  This means your key
should be something like: "sto-3g","aug-cc-pVDZ", etc.

