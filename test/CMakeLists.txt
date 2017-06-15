cmake_minimum_required(VERSION 3.0)

#This sets PULSAR_RUNTEST variable
find_package(pulsar REQUIRED)

########################
# Core pulsar module tests
########################
function(pulsar_psi4_py_test dir test_name)
  pulsar_py_test(${dir} ${test_name} ${PULSAR_PSI4_PREFIX})
endfunction()

foreach(dir energymethods)
  add_subdirectory(${dir})
  install(FILES ${CMAKE_BINARY_DIR}/${dir}/CTestTestfile.cmake DESTINATION ${dir})
endforeach()

# This file was created from the various add_test commands
install(FILES ${CMAKE_BINARY_DIR}/CTestTestfile.cmake DESTINATION .)
