cmake_minimum_required(VERSION 2.8.3)

include(cmake/base.cmake)
include(cmake/python.cmake)
include(cmake-modules/xacro.cmake)

SET(PROJECT_NAME "hpp_tiago")
SET(PROJECT_DESCRIPTION "Additionnal files to use tiago in HPP")
SET(PROJECT_URL "")

SETUP_PROJECT()

ADD_REQUIRED_DEPENDENCY(tiago_data)
FINDPYTHON(REQUIRED)

foreach(dir robots urdf srdf)
    install(DIRECTORY ${dir}/
      DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/${PROJECT_NAME}/${dir})
endforeach(dir)

INSTALL(DIRECTORY src/hpp DESTINATION ${PYTHON_SITELIB})

# Generate URDFs
#SET(TYPES steel)

MAKE_DIRECTORY(${PROJECT_BINARY_DIR}/robots)
FOREACH(type ${TYPES})
  GENERATE_URDF_FILE(${TIAGO_DATA_DATAROOTDIR}/${PROJECT_NAME}/robots/tiago_${type}.urdf
    ${PROJECT_BINARY_DIR}/robots/tiago_${type} "urdf")
  INSTALL(FILES
    ${PROJECT_BINARY_DIR}/robots/tiago_${type}.urdf
    DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/${PROJECT_NAME}/urdf)
ENDFOREACH(type ${TYPES})

INSTALL(FILES package.xml DESTINATION
  ${CMAKE_INSTALL_DATAROOTDIR}/${PROJECT_NAME})


SETUP_PROJECT_FINALIZE()
