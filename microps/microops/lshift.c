#include "microops.h"
PyObject* micro_lshift(PyObject* a, PyObject* b) { 
    return PyNumber_Lshift(a, b); 
}
