#include "microops.h"
PyObject* micro_truthy(PyObject* a) { return PyBool_FromLong(PyObject_IsTrue(a)); }
