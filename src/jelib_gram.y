/* **************************************************************************
//  S R C / j e l i b _ g r a m . y
//  created Thu Jun 20, 2024  1:28 pm by: Gary Delp
// **************************************************************************
//   Copyright (c) 2024 by Gary Delp. All Rights Reserved Worldwide.
//    Licensed under the Apache License, Version 2.0
// **************************************************************************
// *Commentary:
//    The Electric CAD tool saves cells in .jelib format
//      This is a parser that pulls a file or files into a form that can
//        be manipulated.
//  (Last Emacs Update:Wed Jun 26, 2024  2:46 pm by Gary Delp v-0.1.4)
//
// Wed Jun 26, 2024  2:46 pm by Gary Delp v-0.1.4:
//
// Fri Jun 21, 2024 10:22 pm by Gary Delp v-0.1.4:
//
// Thu Jun 20, 2024  4:38 pm by Gary Delp v-0.1.0:
//      Header template expanded
// *start of: SRC/jelib_gram.y
*/

%code top {
#define _GNU_SOURCE
#include "config.h"
 }

%code requires {
#include "jelib_defs.h"
    int yylex (void);
    void yyerror (char const *);
#define YYLTYPE YYLTYPE
    typedef struct YYLTYPE {
        int first_line;
        int first_column;
        int last_line;
        int last_column;
        char *filename;
    } YYLTYPE;
}

%header jelib_gram.tab.h

%union {
    long int     n;
    cell_p    cell;
    char      *str;
    pair_t    pair;
    mod_st mod_str;
    tree_p   treep;
}

%code {
    static void print_token (yytoken_kind_t token, YYSTYPE val);
    static void trace_token (yytoken_kind_t token, YYLTYPE loc);
 }
%token NUM

%% /* Grammar rules and actions follow.  */

file: {headers} cells {




// Local Variables:
// mode: C++
// End:

/// end of: SRC/jelib_gram.y
