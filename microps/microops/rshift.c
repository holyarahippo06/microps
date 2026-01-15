#include "microops.h"
PyObject* micro_rshift(PyObject* a, PyObject* b) { 
    return PyNumber_Rshift(a, b); 
}
