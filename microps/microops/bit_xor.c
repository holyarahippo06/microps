#include "microops.h"
PyObject* micro_bit_xor(PyObject* a, PyObject* b) { 
    return PyNumber_Xor(a, b); 
}
