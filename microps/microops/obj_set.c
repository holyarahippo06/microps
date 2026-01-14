#include "microops.h"
PyObject* micro_obj_set(PyObject* o, PyObject* k, PyObject* v) { PyObject_SetItem(o,k,v); Py_RETURN_NONE; }
