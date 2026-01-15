#include "microops.h"
PyObject* micro_ge(PyObject* a, PyObject* b) { 
    return PyObject_RichCompare(a, b, Py_GE); 
}
