Hartree-Fock                                                               {#hf}
============

The main gotcha in using the Pulsar API to Psi4's HF code is the difference in
the option keys.  Below you will find a description of the keys used by Pulsar,
which are the keys to use with this interface *i.e.* don't use the Psi4 keys.

## Options

### Common

These are the options all flavors of Hartree-Fock have:

- PRINT : Printing level for HF in Psi4
- MAX_ITER : Maximum number of iterations (default:100)
- JK_BUILD_KEY : Used for controlling what Psi4 calls the SCF type
  (default: density fitting *i.e.* "df")
- EGY_TOLERANCE : Criteria for declaring the energy converged (default: 1e-6)
- DENS_TOLERANCE : Criteria for declaring the density converged (default: 1e-6)
- KEY_INITIAL_GUESS : The key of the module used for the initial guess (at the
  moment it is just the Psi4 option for guess, defaulting to SAD) 
- DAMPING_FACTOR : How much of the previuos density should be mixed in? This is
  an option in Psi4, but should not be used because it does not work

### Expert / Control

These are options that you probably shouldn't touch:

- MAX_DERIV : The level of analytic derivatives available (default: 2).  Change
  to use FDiff code.
- DRY_RUN : Set to true if the HF module is being "called" from a post-HF method

## Submodules

At the moment HF calls no submodules.
