#include "microops.h"
PyObject* micro_type(PyObject* a) { return PyUnicode_FromString(Py_TYPE(a)->tp_name); }
