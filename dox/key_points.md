Things to Keep in Mind                  {#key_points}
======================

Despite embodying many of the same concepts as Pulsar, internally Psi4 operates
quite differently.  For this reason there are a couple of things to know before
using the Pulsar interface to Psi4.  For the most part the Pulsar API to Psi4 is
written in a manner to ensure that Pulsar practices map as best as possible to
Psi4's practices.

Option Parsing
--------------

Psi4 has some support for options on a per module basis; however, it is not at
the same level as Pulsar's support.  Consequentially, there needs to be a
mapping from Pulsar's less specific options to Psi4's more specific options. At
the moment this mapping is kept in `Pulsar2Psi4Options.py`.

Basis Set Parsing
-----------------

To my knowledge, Psi4 intrinsically assumes you are reading your basis set from
a `*.gbs` file.  Although, parsing through the Psi4 source you may be tempted to
think that you can manually specify the coeficients and exponents, but it
appears that much of that machinery is not hooked up.  Rather than dumping the
Pulsar basis set out to a file just to have Psi4 read it back in again we do a
little cheat.  When you call `psr.apply_single_basis` the description of the
basis set is saved onto the atom *e.g.* `6-31G*`.  When we are setting Psi4's
options we use the `BASIS_SET` key to pull the description off of an atom and
tell Psi4 to use that.  Consequentially, at the moment you may only use
pre-defined basis sets.

Cacheing / Checkpointing
------------------------

At the moment, Psi4 has no support for cacheing and checkpointing.  Furthermore,
the Pulsar CacheData class is not going to be introduced into the the main
Psi4 source code.  Hence, we have to be a little creative in cacheing the
results.  Getting the results is easy, Psi4 returns their wavefunction object,
which has all of the info we need for the Pulsar Wavefunction class.  The
energies and derivatives are available via the Psi variables.  The complication
comes in when you realize that Psi4's internal structure does not mirror the
recursive nature of Pulsar, *e.g.* Psi4's MP2 code doesn't call the SCF code,
but rather the driver takes care of passing the information.  In order to make
it appear as if Psi4 was recursively calling modules we introduce the idea of a
"dry run".  What this means is when you ask Pulsar to run Psi4's CCSD(T) code
it lets Psi4 run CCSD(T) and then calls what conceptually we think of as the
submodules (CCSD,MP2,SCF) in a "dry" state.  When called in a dry state all the
module does is read information from the psi variables and then call its
submodules (also in a dry run).  This allows all of the submodules to cache the
results they normally would.

The biggest consequence of this is that you should run your biggest computation,
say CCSD(T) first, and then get the correlation energy by running SCF and
subtracting the two energies.  If you run them in the other order the SCF will
be run twice.

