// FILE: microps/microops/bit_or.c
// ============================================
#include "microops.h"
PyObject* micro_bit_or(PyObject* a, PyObject* b) { 
    return PyNumber_Or(a, b); 
}
