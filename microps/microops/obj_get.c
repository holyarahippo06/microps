#include "microops.h"
PyObject* micro_obj_get(PyObject* o, PyObject* k) { PyObject* r=PyObject_GetItem(o,k); if(!r){PyErr_Clear(); Py_RETURN_NONE;} return r; }
