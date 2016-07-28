cmake_minimum_required(VERSION 3.1)

# Find the pulsar core and psi4
list(APPEND CMAKE_PREFIX_PATH "${PULSAR_PATH}")
find_package(pulsar REQUIRED)
find_package(psi4 REQUIRED)
add_subdirectory(pulsar_psi4)



