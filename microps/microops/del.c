#include "microops.h"
PyObject* micro_del(PyObject* o, PyObject* k) { if(PyObject_DelItem(o,k)<0)PyErr_Clear(); Py_RETURN_NONE; }
