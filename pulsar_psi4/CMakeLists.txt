cmake_minimum_required(VERSION 3.1)
find_package(pulsar REQUIRED)
find_package(psi4 REQUIRED)
get_target_property(PSI4_CORE psi4 INTERFACE_LINK_LIBRARIES)
get_filename_component(PSI4_LIBRARY_DIR ${PSI4_CORE} DIRECTORY)
get_filename_component(PSI4_LIBRARY_DIR ${PSI4_LIBRARY_DIR} DIRECTORY)
message(STATUS ${PSI4_LIBRARY_DIR})
configure_file("__init__.py.in" "__init__.py" @ONLY)

install(FILES ${CMAKE_BINARY_DIR}/__init__.py 
        DESTINATION ${CMAKE_INSTALL_PREFIX}/modules/pulsar_psi4
)

install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/
        DESTINATION ${CMAKE_INSTALL_PREFIX}/modules/pulsar_psi4
        PATTERN "*.py"
        PATTERN tests EXCLUDE
        PATTERN "*.in" EXCLUDE
)
