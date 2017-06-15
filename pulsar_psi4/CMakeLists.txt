cmake_minimum_required(VERSION 3.1)
find_package(pulsar REQUIRED)
find_package(psi4 REQUIRED)
get_filename_component(PSI4_CORE ${psi4_LIBRARY} DIRECTORY)
get_filename_component(PSI4_CORE ${PSI4_CORE} DIRECTORY)
configure_file("__init__.py.in" "__init__.py" @ONLY)

install(FILES ${CMAKE_BINARY_DIR}/__init__.py 
        DESTINATION ${CMAKE_INSTALL_PREFIX}/pulsar_psi4
)

install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/
        DESTINATION ${CMAKE_INSTALL_PREFIX}/pulsar_psi4
        PATTERN "*.py"
        PATTERN tests EXCLUDE
        PATTERN "*.in" EXCLUDE
)
