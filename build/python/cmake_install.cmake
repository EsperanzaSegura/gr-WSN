# Install script for directory: /home/miguel/gr-WSN/python

# Set the install prefix
IF(NOT DEFINED CMAKE_INSTALL_PREFIX)
  SET(CMAKE_INSTALL_PREFIX "/usr/local")
ENDIF(NOT DEFINED CMAKE_INSTALL_PREFIX)
STRING(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
IF(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  IF(BUILD_TYPE)
    STRING(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  ELSE(BUILD_TYPE)
    SET(CMAKE_INSTALL_CONFIG_NAME "Release")
  ENDIF(BUILD_TYPE)
  MESSAGE(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
ENDIF(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)

# Set the component getting installed.
IF(NOT CMAKE_INSTALL_COMPONENT)
  IF(COMPONENT)
    MESSAGE(STATUS "Install component: \"${COMPONENT}\"")
    SET(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  ELSE(COMPONENT)
    SET(CMAKE_INSTALL_COMPONENT)
  ENDIF(COMPONENT)
ENDIF(NOT CMAKE_INSTALL_COMPONENT)

# Install shared libraries without execute permission?
IF(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  SET(CMAKE_INSTALL_SO_NO_EXE "1")
ENDIF(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python2.7/dist-packages/WSN" TYPE FILE FILES
    "/home/miguel/gr-WSN/python/__init__.py"
    "/home/miguel/gr-WSN/python/tx_app_xbee.py"
    "/home/miguel/gr-WSN/python/tx_nwk_zigbee.py"
    "/home/miguel/gr-WSN/python/tx_mac_802_15_4.py"
    "/home/miguel/gr-WSN/python/rx_mac_802_15_4.py"
    "/home/miguel/gr-WSN/python/rx_nwk_zigbee.py"
    "/home/miguel/gr-WSN/python/rx_app_xbee.py"
    )
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python2.7/dist-packages/WSN" TYPE FILE FILES
    "/home/miguel/gr-WSN/build/python/__init__.pyc"
    "/home/miguel/gr-WSN/build/python/tx_app_xbee.pyc"
    "/home/miguel/gr-WSN/build/python/tx_nwk_zigbee.pyc"
    "/home/miguel/gr-WSN/build/python/tx_mac_802_15_4.pyc"
    "/home/miguel/gr-WSN/build/python/rx_mac_802_15_4.pyc"
    "/home/miguel/gr-WSN/build/python/rx_nwk_zigbee.pyc"
    "/home/miguel/gr-WSN/build/python/rx_app_xbee.pyc"
    "/home/miguel/gr-WSN/build/python/__init__.pyo"
    "/home/miguel/gr-WSN/build/python/tx_app_xbee.pyo"
    "/home/miguel/gr-WSN/build/python/tx_nwk_zigbee.pyo"
    "/home/miguel/gr-WSN/build/python/tx_mac_802_15_4.pyo"
    "/home/miguel/gr-WSN/build/python/rx_mac_802_15_4.pyo"
    "/home/miguel/gr-WSN/build/python/rx_nwk_zigbee.pyo"
    "/home/miguel/gr-WSN/build/python/rx_app_xbee.pyo"
    )
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

