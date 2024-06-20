# -------------------------------------------------------------------------------
#  S R C / c o n f i g u r e . a c
#  created Thu Jun 20, 2024 11:40 am by: Gary Delp
# -------------------------------------------------------------------------------
#   Copyright (c) 2024 by Gary Delp. All Rights Reserved Worldwide.
#    Licensed under the Apache License, Version 2.0
# -------------------------------------------------------------------------------
# -Commentary:
#  (Last Emacs Update:  Thu Jun 20, 2024  1:57 pm by Gary Delp v-0.1.2)
#
# Thu Jun 20, 2024  1:57 pm by Gary Delp v-0.1.2:
#      Initialize
# -start of: SRC/configure.ac
#-O outline from  https://www.gnu.org/savannah-checkouts/gnu/autoconf/
#   manual/autoconf-2.72/html_node/Autoconf-Input-Layout.html
#-O Autoconf requirements 
AC_PREREQ([2.68])
#-O AC_INIT(package, version, bug-report-address)
m4_define([elec2xic_VERSION], [0.1])
AC_INIT([elec2xic],
	m4_defn([elec2xic_VERSION]),
	[elec2xic-bugs@graceandcharm.info],
	[dist/elec2xic-dist],
	[https://github.com/ElderDelp/elec2xic])

#-O information on the package
AC_CONFIG_SRCDIR ([jelib_gram.y)
#-O checks for programs
AM_INIT_AUTOMAKE([-Wall -Werror foreign])
AC_PROG_CC
AC_PROG_LEX
AC_PROG_YACC
AC_PROG_INSTALL
AC_PROG_MKDIR_P 
#-O checks for libraries
#-O checks for header files
AC_CHECK_HEADER([stdio.h],
                [AC_DEFINE([HAVE_STDIO_H], 1,
                   [Define to 1 if you have <stdio.h>.])],
                [AC_MSG_ERROR([sorry, can't do anything for you])])
AC_INCLUDE_DEFAULTS()
#-O checks for types
#-O checks for structures
#-O checks for compiler characteristics
#-O checks for library functions
#-O checks for system services
#-O AC_CONFIG_FILES([file])
AC_CONFIG_HEADERS([config.h])
AC_CONFIG_FILES([
 Makefile
 src/Makefile
])
#-O AC_OUTPUT
