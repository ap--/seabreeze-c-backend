cmake_minimum_required(VERSION 3.20)

project(
  libseabreeze
  VERSION 3.0.11.11
  DESCRIPTION "Ocean Optics SeaBreeze spectrometer library"
  LANGUAGES C CXX
)

include(GNUInstallDirs)
include(CMakePackageConfigHelpers)

set(CMAKE_CXX_STANDARD 11 CACHE STRING "C++ standard used to compile libseabreeze")
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# --- platform specific sources -----------------------------------------------
# the vendored sources provide one implementation per platform. Only the
# implementation matching the current platform must be compiled.
if(WIN32)
  set(_seabreeze_excluded_dirs "linux" "osx" "posix")
elseif(APPLE)
  set(_seabreeze_excluded_dirs "linux" "winusb" "windows")
else()
  set(_seabreeze_excluded_dirs "osx" "winusb" "windows")
endif()

file(GLOB_RECURSE _seabreeze_sources CONFIGURE_DEPENDS
  "${CMAKE_CURRENT_SOURCE_DIR}/src/*.c"
  "${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp"
)
foreach(_dir IN LISTS _seabreeze_excluded_dirs)
  list(FILTER _seabreeze_sources EXCLUDE REGEX "/src/.*/${_dir}/")
endforeach()

if(NOT _seabreeze_sources)
  message(FATAL_ERROR "No libseabreeze sources found in ${CMAKE_CURRENT_SOURCE_DIR}/src")
endif()

add_library(seabreeze ${_seabreeze_sources})
add_library(seabreeze::seabreeze ALIAS seabreeze)

target_include_directories(seabreeze
  PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}/libseabreeze>
)

set_target_properties(seabreeze PROPERTIES
  VERSION ${PROJECT_VERSION}
  SOVERSION ${PROJECT_VERSION_MAJOR}
  POSITION_INDEPENDENT_CODE ON
  # libseabreeze does not annotate its symbols with __declspec(dllexport)
  WINDOWS_EXPORT_ALL_SYMBOLS ON
)

# --- platform specific dependencies ------------------------------------------
if(WIN32)
  target_compile_definitions(seabreeze PRIVATE _WINDOWS)
  target_link_libraries(seabreeze PRIVATE winusb ws2_32 setupapi)

elseif(APPLE)
  find_library(CARBON_LIBRARY Carbon REQUIRED)
  find_library(CORE_FOUNDATION_LIBRARY CoreFoundation REQUIRED)
  find_library(IOKIT_LIBRARY IOKit REQUIRED)
  target_link_libraries(seabreeze PRIVATE
    ${CARBON_LIBRARY} ${CORE_FOUNDATION_LIBRARY} ${IOKIT_LIBRARY}
  )

else()
  # the linux usb implementation uses the libusb-0.1 api, which is provided
  # by libusb-compat on top of libusb-1.0
  find_package(PkgConfig QUIET)
  if(PkgConfig_FOUND)
    # depending on the distribution the compat layer ships libusb.pc or libusb-0.1.pc
    pkg_check_modules(LIBUSB IMPORTED_TARGET libusb)
    if(NOT LIBUSB_FOUND)
      pkg_check_modules(LIBUSB IMPORTED_TARGET libusb-0.1)
    endif()
  endif()
  if(TARGET PkgConfig::LIBUSB)
    target_link_libraries(seabreeze PRIVATE PkgConfig::LIBUSB)
  else()
    find_library(USB_LIBRARY NAMES usb REQUIRED)
    find_path(USB_INCLUDE_DIR NAMES usb.h REQUIRED)
    target_link_libraries(seabreeze PRIVATE ${USB_LIBRARY})
    target_include_directories(seabreeze PRIVATE ${USB_INCLUDE_DIR})
  endif()
endif()

# --- installation ------------------------------------------------------------
option(SEABREEZE_INSTALL "Generate install rules for libseabreeze" ON)

if(SEABREEZE_INSTALL)
  install(
    TARGETS seabreeze
    EXPORT seabreezeTargets
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
  )
  install(
    DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/include/"
    DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}/libseabreeze"
    FILES_MATCHING PATTERN "*.h"
  )
  install(
    EXPORT seabreezeTargets
    FILE seabreezeTargets.cmake
    NAMESPACE seabreeze::
    DESTINATION "${CMAKE_INSTALL_LIBDIR}/cmake/seabreeze"
  )

  configure_package_config_file(
    "${CMAKE_CURRENT_SOURCE_DIR}/cmake/seabreezeConfig.cmake.in"
    "${CMAKE_CURRENT_BINARY_DIR}/seabreezeConfig.cmake"
    INSTALL_DESTINATION "${CMAKE_INSTALL_LIBDIR}/cmake/seabreeze"
  )
  write_basic_package_version_file(
    "${CMAKE_CURRENT_BINARY_DIR}/seabreezeConfigVersion.cmake"
    COMPATIBILITY SameMajorVersion
  )
  install(
    FILES
      "${CMAKE_CURRENT_BINARY_DIR}/seabreezeConfig.cmake"
      "${CMAKE_CURRENT_BINARY_DIR}/seabreezeConfigVersion.cmake"
    DESTINATION "${CMAKE_INSTALL_LIBDIR}/cmake/seabreeze"
  )

  configure_file(
    "${CMAKE_CURRENT_SOURCE_DIR}/cmake/libseabreeze.pc.in"
    "${CMAKE_CURRENT_BINARY_DIR}/libseabreeze.pc"
    @ONLY
  )
  install(
    FILES "${CMAKE_CURRENT_BINARY_DIR}/libseabreeze.pc"
    DESTINATION "${CMAKE_INSTALL_LIBDIR}/pkgconfig"
  )
endif()
