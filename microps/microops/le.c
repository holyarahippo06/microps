#include "microops.h"
PyObject* micro_le(PyObject* a, PyObject* b) { 
    return PyObject_RichCompare(a, b, Py_LE); 
}
