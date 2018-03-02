cmake_minimum_required(VERSION 2.8.3)

include(cmake/base.cmake)
include(cmake/python.cmake)
include(cmake-modules/xacro.cmake)

SET(PROJECT_NAME "hpp_tiago")
SET(PROJECT_DESCRIPTION "Additionnal files to use tiago in HPP")
SET(PROJECT_URL "")
SET(PROJECT_VERSION 0)

SETUP_PROJECT()

FINDPYTHON(REQUIRED)
ADD_REQUIRED_DEPENDENCY("tiago_description")

SET(TIAGO_DESCRIPTION_SHARE_DIR ${TIAGO_DESCRIPTION_PREFIX}/share/tiago_description)
FILE(RELATIVE_PATH TIAGO_DESCRIPTION_SHARE_REL_DIR ${CMAKE_CURRENT_BINARY_DIR} ${TIAGO_DESCRIPTION_SHARE_DIR})
SET(INSTALL_SHARE_DIR ${CMAKE_INSTALL_PREFIX}/share/${PROJECT_NAME})

foreach(dir robots urdf srdf)
    install(DIRECTORY ${dir}/
      DESTINATION ${INSTALL_SHARE_DIR}/${dir})
endforeach(dir)

INSTALL(DIRECTORY src/hpp DESTINATION ${PYTHON_SITELIB})

# Generate URDFs
#SET(TYPES iron steel)
SET(TYPES steel)

MAKE_DIRECTORY(${CMAKE_BINARY_DIR}/robots)
FOREACH(type ${TYPES})
  GENERATE_URDF_FILE(${TIAGO_DESCRIPTION_SHARE_REL_DIR}/robots/tiago_${type}.urdf robots/tiago_${type} "urdf")
  INSTALL(FILES
    ${CMAKE_BINARY_DIR}/robots/tiago_${type}.urdf
    DESTINATION ${INSTALL_SHARE_DIR}/urdf)
ENDFOREACH(type ${TYPES})

SET(XACRO_BASE "robots/tiago_airbus.urdf")
SET(FIND_HPP_TIAGO_COMMAND ${CMAKE_SOURCE_DIR})
CONFIGURE_FILE(${CMAKE_SOURCE_DIR}/${XACRO_BASE}.xacro.in ${CMAKE_BINARY_DIR}/${XACRO_BASE}.xacro @ONLY)
ADD_CUSTOM_COMMAND(
  OUTPUT ${CMAKE_BINARY_DIR}/${XACRO_BASE}
  COMMAND ${_xacro_py}
  ARGS --inorder -o ${CMAKE_BINARY_DIR}/${XACRO_BASE} ${CMAKE_BINARY_DIR}/${XACRO_BASE}.xacro additional_translation:=false
  MAIN_DEPENDENCY ${CMAKE_BINARY_DIR}/${XACRO_BASE}.xacro
  COMMENT "Generating URDF from ${XACRO_BASE}.xacro.in"
  )
  LIST(APPEND ALL_GENERATED_URDF ${CMAKE_BINARY_DIR}/${XACRO_BASE})

GENERATE_URDF_FILE(${CMAKE_SOURCE_DIR}/robots/tiago_airbus.urdf robots/tiago_airbus "urdf")
INSTALL(FILES
  ${CMAKE_BINARY_DIR}/robots/tiago_airbus.urdf
  DESTINATION ${INSTALL_SHARE_DIR}/urdf)

ADD_CUSTOM_TARGET (generate_urdf_file ALL DEPENDS ${ALL_GENERATED_URDF})

SETUP_PROJECT_FINALIZE()
