#include "microops.h"
PyObject* micro_div(PyObject* a, PyObject* b) { return PyNumber_TrueDivide(a, b); }
