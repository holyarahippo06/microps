#include "microops.h"
PyObject* micro_ne(PyObject* a, PyObject* b) { 
    return PyObject_RichCompare(a, b, Py_NE); 
}
