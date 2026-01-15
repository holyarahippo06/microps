#include "microops.h"
PyObject* micro_lt(PyObject* a, PyObject* b) { 
    return PyObject_RichCompare(a, b, Py_LT); 
}
