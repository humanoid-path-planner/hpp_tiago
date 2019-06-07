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

INSTALL(FILES package.xml DESTINATION
  ${CMAKE_INSTALL_DATAROOTDIR}/${PROJECT_NAME})

# Make symbolic link to tiago_steel.urdf installed by tiago_data
INSTALL(CODE "execute_process( \
    COMMAND ${CMAKE_COMMAND} -E create_symlink \
    ${TIAGO_DATA_DATAROOTDIR}/tiago_data/robots/tiago_steel.urdf \
    ${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_DATAROOTDIR}/${PROJECT_NAME}/urdf/tiago_steel.urdf   \
    )"
  )

SETUP_PROJECT_FINALIZE()
