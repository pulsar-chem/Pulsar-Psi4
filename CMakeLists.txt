cmake_minimum_required(VERSION 3.1)
include(ExternalProject)

set(STAGE_DIR ${CMAKE_BINARY_DIR}/stage)
ExternalProject_Add(pulsar_psi4
   SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/pulsar_psi4
   CMAKE_ARGS -DCMAKE_INSTALL_PREFIX=${CMAKE_INSTALL_PREFIX}
              -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}
              -DPULSAR_PSI4_ROOT=${CMAKE_CURRENT_SOURCE_DIR}
   CMAKE_CACHE_ARGS -DCMAKE_PREFIX_PATH:STRING=${CMAKE_PREFIX_PATH}
   BUILD_COMMAND $(MAKE)
   BUILD_ALWAYS 1
   INSTALL_COMMAND $(MAKE) install DESTDIR=${STAGE_DIR}
)
set(PULSAR_PSI4_PREFIX ${STAGE_DIR}${CMAKE_INSTALL_PREFIX})
ExternalProject_Add(pulsar_psi4_test
   SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/test
   CMAKE_ARGS -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}
              -DCMAKE_INSTALL_PREFIX=${CMAKE_BINARY_DIR}/test_stage
              -DSTAGE_DIR=${STAGE_DIR}
              -DPULSAR_PSI4_PREFIX=${PULSAR_PSI4_PREFIX}
              -DCMAKE_CXX_COMPILER=${CMAKE_CXX_COMPILER}
              -DCMAKE_C_COMPILER=${CMAKE_C_COMPILER}
              -DCMAKE_CXX_FLAGS=${CMAKE_CXX_FLAGS}
              -DCMAKE_C_FLAGS=${CMAKE_C_FLAGS}
   CMAKE_CACHE_ARGS -DCMAKE_PREFIX_PATH:STRING=${CMAKE_PREFIX_PATH}
                    -DCMAKE_MODULE_PATH:STRING=${CMAKE_MODULE_PATH}
   BUILD_ALWAYS 1
)
add_dependencies(pulsar_psi4_test pulsar_psi4)
#This file will allow us to run ctest in the top-level build dir

#Basically it just defers to the actual top-level CTestTestfile.cmake in the
#build directory for this project
file(WRITE ${CMAKE_BINARY_DIR}/CTestTestfile.cmake "subdirs(test_stage)")

# Install the staging directory
install(DIRECTORY ${CMAKE_BINARY_DIR}/stage/${CMAKE_INSTALL_PREFIX}/ 
        DESTINATION ${CMAKE_INSTALL_PREFIX} USE_SOURCE_PERMISSIONS)
