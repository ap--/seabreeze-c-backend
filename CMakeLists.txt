cmake_minimum_required(VERSION 3.26)

project(
  seabreeze_c_backend
  DESCRIPTION "Seabreeze C Backend python extension module"
  LANGUAGES C CXX
)

option(SEABREEZE_C_BACKEND_USE_SYSTEM_LIBSEABREEZE
       "Link against a libseabreeze installation instead of the vendored sources" OFF)
option(SEABREEZE_C_BACKEND_LIMITED_API
       "Compile the extension module against the python stable ABI (>=3.11)" ON)

option(SEABREEZE_C_BACKEND_DISABLE_FH4
       "Disable the MSVC FH4 exception handling implementation (avoids requiring VCRUNTIME140_1.dll)" OFF)

set(SEABREEZE_C_BACKEND_LIMITED_API_VERSION "3.11" CACHE STRING
    "Minimum python version of the stable ABI the extension module is compiled against")

if(MSVC AND SEABREEZE_C_BACKEND_DISABLE_FH4)
  # see: https://devblogs.microsoft.com/cppblog/making-cpp-exception-handling-smaller-x64/
  add_compile_options(/d2FH4-)
endif()

# --- python ------------------------------------------------------------------
find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)

if(Python_VERSION VERSION_LESS SEABREEZE_C_BACKEND_LIMITED_API_VERSION)
  # the buffer protocol is only part of the stable ABI since python 3.11
  set(SEABREEZE_C_BACKEND_LIMITED_API OFF)
endif()
if(SEABREEZE_C_BACKEND_LIMITED_API)
  find_package(Python REQUIRED COMPONENTS Interpreter Development.SABIModule)
endif()

# --- libseabreeze ------------------------------------------------------------
if(SEABREEZE_C_BACKEND_USE_SYSTEM_LIBSEABREEZE)
  # link dynamically against an existing libseabreeze installation. This is
  # used for the wheel builds (the shared library is vendored into the wheel by
  # auditwheel/delocate/delvewheel) and for conda-forge, where libseabreeze is
  # packaged in its own feedstock and must not be vendored.
  find_package(seabreeze REQUIRED)
else()
  # build the vendored libseabreeze sources as a shared library, link the
  # extension module against it and ship it inside the python package
  set(BUILD_SHARED_LIBS ON)
  set(SEABREEZE_INSTALL OFF)
  add_subdirectory(src/libseabreeze)
  # the library is loaded from next to the extension module, so the version
  # suffixes (and the symlinks they require) are not needed
  set_property(TARGET seabreeze PROPERTY VERSION)
  set_property(TARGET seabreeze PROPERTY SOVERSION)
  install(
    TARGETS seabreeze
    RUNTIME DESTINATION seabreeze_c_backend
    LIBRARY DESTINATION seabreeze_c_backend
  )
endif()

# the extension module loads libseabreeze from next to itself when it is
# vendored into the wheel. CMAKE_INSTALL_RPATH_USE_LINK_PATH additionally keeps
# the location of a system libseabreeze in the rpath, which allows the wheel
# repair tools to resolve and vendor it.
if(APPLE)
  list(APPEND CMAKE_INSTALL_RPATH "@loader_path")
else()
  list(APPEND CMAKE_INSTALL_RPATH "$ORIGIN")
endif()
set(CMAKE_INSTALL_RPATH_USE_LINK_PATH ON)

# --- cythonize ---------------------------------------------------------------
set(_pyx "${CMAKE_CURRENT_SOURCE_DIR}/src/seabreeze_c_backend/_libseabreeze_wrapper.pyx")
set(_cpp "${CMAKE_CURRENT_BINARY_DIR}/_libseabreeze_wrapper.cpp")

add_custom_command(
  OUTPUT "${_cpp}"
  COMMAND
    "${Python_EXECUTABLE}" -m cython --cplus
    -I "${CMAKE_CURRENT_SOURCE_DIR}/src"
    -X language_level=3str
    -X embedsignature=True
    --module-name seabreeze_c_backend._libseabreeze_wrapper
    --output-file "${_cpp}"
    "${_pyx}"
  DEPENDS
    "${_pyx}"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/seabreeze_c_backend/_libseabreeze.pxd"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/seabreeze_c_backend/__init__.pxd"
  VERBATIM
  COMMENT "Cythonizing _libseabreeze_wrapper.pyx"
)

# --- extension module --------------------------------------------------------
if(SEABREEZE_C_BACKEND_LIMITED_API)
  python_add_library(
    _libseabreeze_wrapper MODULE "${_cpp}"
    USE_SABI "${SEABREEZE_C_BACKEND_LIMITED_API_VERSION}" WITH_SOABI
  )
  target_compile_definitions(_libseabreeze_wrapper PRIVATE CYTHON_LIMITED_API=1)
else()
  python_add_library(_libseabreeze_wrapper MODULE "${_cpp}" WITH_SOABI)
endif()

target_link_libraries(_libseabreeze_wrapper PRIVATE seabreeze::seabreeze)

install(TARGETS _libseabreeze_wrapper DESTINATION seabreeze_c_backend)
