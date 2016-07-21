cmake_minimum_required(VERSION 3.1)

# Find the pulsar core and psi4
list(APPEND CMAKE_PREFIX_PATH "${PULSAR_PATH}")
find_package(pulsar REQUIRED)
find_package(psi4 REQUIRED)
add_subdirectory(tests)

install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/
        DESTINATION ${CMAKE_INSTALL_PREFIX}/modules/pulsar_psi4
        PATTERN "*.py"
        PATTERN tests EXCLUDE
)

