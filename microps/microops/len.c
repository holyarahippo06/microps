#include "microops.h"
PyObject* micro_len(PyObject* a) { return PyLong_FromSsize_t(PyObject_Size(a)); }
