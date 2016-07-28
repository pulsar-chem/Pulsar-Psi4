get_filename_component(PSI4_LIBRARY_DIR ${PSI4_LIBRARY} DIRECTORY)
configure_file("__init__.py.in" "__init__.py" @ONLY)
add_subdirectory(tests)

install(FILES ${CMAKE_BINARY_DIR}/pulsar_psi4/__init__.py 
        DESTINATION ${CMAKE_INSTALL_PREFIX}/modules/pulsar_psi4
)

install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/
        DESTINATION ${CMAKE_INSTALL_PREFIX}/modules/pulsar_psi4
        PATTERN "*.py"
        PATTERN tests EXCLUDE
        PATTERN "*.in" EXCLUDE
)
