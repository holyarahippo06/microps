#include "microops.h"
PyObject* micro_not(PyObject* a) { return PyBool_FromLong(!PyObject_IsTrue(a)); }
