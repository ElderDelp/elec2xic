// **************************************************************************
//  S R C / j e l i b _ d e f s . h
//  created Thu Jun 20, 2024  4:24 pm by: Gary Delp
// **************************************************************************
//   Copyright (c) 2024 by Gary Delp. All Rights Reserved Worldwide.
//    Licensed under the Apache License, Version 2.0
// **************************************************************************
// *Commentary:
//  (Last Emacs Update:  Fri Jun 21, 2024  5:13 pm by Gary Delp v-0.1.0)
//
// Fri Jun 21, 2024  5:13 pm by Gary Delp v-0.1.0:
//
// Thu Jun 20, 2024  4:37 pm by Gary Delp v-0.1.0:
//      Initial data types
// *start of: SRC/jelib_defs.h

#ifndef Def_INC_jelib_defs_h
#define Def_INC_jelib_defs_h
#include "config.h"

# define nil ((void *) 0)

/* For arbitrary lists, a cons cell */
typedef cons_t {
    void *car;
    cons_t *cdr;
} cons_t, *cons_p;

typedef enum cell_type_t {
    ct_ic, ct_lay, ct_sch
} cell_type_t, *cell_type_p;

/* All of the collected information about a cell */
typedef struct cell_t {
    char *name;
} cell_t, *cell_p;

/* balanced tree structure */
typedef struct tree_t {
    char *name;
    struct tree_t *left, *right, *up;
    void *el_p;                 // pointer to arbitrary element
} tree_t *tree_p;

/* JELIB Modifyier string */
typedef struct mod_str_t {
    char *modifyer;
} mod_str_t, *mod_str_p;


#endif /* Def__INC_jelib_defs_h */

// Local Variables:
// mode: C++
// End:

/// end of: SRC/jelib_defs.h
