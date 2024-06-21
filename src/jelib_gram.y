// **************************************************************************
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
//  (Last Emacs Update:Thu Jun 20, 2024  9:22 pm by Gary Delp v-0.1.2)
//
// Thu Jun 20, 2024  4:38 pm by Gary Delp v-0.1.0:
//      Header template expanded
// *start of: SRC/jelib_gram.y

%code top {
#define _GNU_SOURCE
#include "config.h"
 }

%code requires {
#include "jelib_defs.h"
    int yylex (void);
    void yyerror (char const *);
}
%header
%union {
    long int   n;
    cell_p     c;
    char    *str;
    pair_t  pair;
    mod_t mod_st;
}
%token NUM

%% /* Grammar rules and actions follow.  */





// Local Variables:
// mode: C++
// End:

/// end of: SRC/jelib_gram.y
