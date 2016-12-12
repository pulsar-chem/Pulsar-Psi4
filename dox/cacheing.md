Hooking Psi4 Up to Pulsar's Cache                                    {#cacheing}
=================================

The interface to Psi4 is initially non-invasive.  What this means is we can't go
propegating Pulsar's classes through Psi4.  In order to work with Pulsar, Psi4
needs to use the cache or else we're going to be repeating computations many,
many times.  This page details how we do this while avoiding leaking our classes
into Psi4.

## Dry Runs

We distinguish between two types of runs to a Psi4 module, the normal run and a
dry run.  The normal run, is well, normal.  It calls the module exactly like you
expect.  The dry run is a thin wrapper that circumvents the actual call.  This
wrapper is used to set data for submodules that in theory were called.  For
example a call to Psi4's MP2 code automatically calls Psi4's HF code in a dry
state so that it can cache HF's values.  A dry run is signaled via the option:

DRY_RUN : Set to True to use a module's dry run path

All psi4 energy methods should have in their Deriv_ function an if statement
that calls psi4_dryrun if this option is true.  The psi4_dryrun command is of
the signature:
~~~{.py}
(psr.wavefunction,[]) psi4_dryrun(psr.Wavefunction,
                                  psr.OptionMap,
                                  psr.CacheData,
                                  string,
                                  string
)
~~~
Basically you pass in the wavefunction to cache, a list of options for the
module, that module's cache, the hash to cache under, and the Psi variable for
the energy you are caching (Psi4 does not provide higher-order derivatives
piece-wise).   If the hash is already in the cache this function simply returns
the deriv and wavefunction, otherwise the wavefunction you passed in and the
energy Psi associates with the Psi variable you passed in are cached and the
result is cached.  If you don't provide a psi variable or no value is found, 
only the options are set and None is returned.  The latter is hacky, but it 
allows us to call Psi4 in a Pulsar-like manner.  Basically, Pulsar wants us to
set options per module, whereas Psi4 does not.  By letting the dry run set the
options it emulates Pulsar behavior.
