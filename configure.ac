# -------------------------------------------------------------------------------
#  S R C / c o n f i g u r e . a c
#  created Thu Jun 20, 2024 11:40 am by: Gary Delp
# -------------------------------------------------------------------------------
#   Copyright (c) 2024 by Gary Delp. All Rights Reserved Worldwide.
#    Licensed under the Apache License, Version 2.0
# -------------------------------------------------------------------------------
# -Commentary:
#  (Last Emacs Update:  Wed Jun 26, 2024  3:24 pm by Gary Delp v-0.1.18)
#
# Wed Jun 26, 2024  3:24 pm by Gary Delp v-0.1.18:
#     Modified YACC test to remove bison flag -y
# -start of: SRC/configure.ac
#-O outline from  https://www.gnu.org/savannah-checkouts/gnu/autoconf/
#   manual/autoconf-2.72/html_node/Autoconf-Input-Layout.html
#-O Autoconf requirements 
AC_PREREQ([2.71])

#-O AC_INIT([package],[version],[bug-report-address])
AC_INIT([elec2xic],
	[0.1],
	[elec2xic-bugs@graceandcharm.info],
	[dist/elec2xic-dist],
	[https://github.com/ElderDelp/elec2xic])

AM_INIT_AUTOMAKE([foreign -Wall -Werror])

#-O information on the package
# Make sure that this specific file exists in the src directory
#AC_CONFIG_SRCDIR([jelib_gram.y])

#-O checks for programs
AC_PROG_CC
AC_PROG_LEX([noyywrap])
if test "x$LEX" != xflex; then
   LEX="$SHELL $missing_dir/missing flex"
   AC_SUBST([LEX_OUTPUT_ROOT], [lex.yy])
   AC_SUBST([LEXLIB], [''])
fi
AC_PROG_YACC
if test "x$YACC" == "xbison -y"; then
   YACC="bison"
   echo " tested for bison... using without the -y flag"
fi
   
AC_PROG_INSTALL
#-O checks for libraries
#-O checks for header files
AC_CHECK_HEADER([stdio.h],
                [AC_DEFINE([HAVE_STDIO_H], 1,
                   [Define to 1 if you have <stdio.h>.])],
                [AC_MSG_ERROR([sorry, can't do anything for you])])
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
AC_OUTPUT
