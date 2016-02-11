INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_WSN WSN)

FIND_PATH(
    WSN_INCLUDE_DIRS
    NAMES WSN/api.h
    HINTS $ENV{WSN_DIR}/include
        ${PC_WSN_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    WSN_LIBRARIES
    NAMES gnuradio-WSN
    HINTS $ENV{WSN_DIR}/lib
        ${PC_WSN_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(WSN DEFAULT_MSG WSN_LIBRARIES WSN_INCLUDE_DIRS)
MARK_AS_ADVANCED(WSN_LIBRARIES WSN_INCLUDE_DIRS)

