#include "microops.h"
PyObject* micro_gt(PyObject* a, PyObject* b) { 
    return PyObject_RichCompare(a, b, Py_GT); 
}
