#include "microops.h"
PyObject* micro_eq(PyObject* a, PyObject* b) { return PyObject_RichCompare(a, b, Py_EQ); }
