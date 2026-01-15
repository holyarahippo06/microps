#include "microops.h"
// Change the name here:
PyObject* micro_del_op(PyObject* o, PyObject* k) { 
    if(PyObject_DelItem(o,k)<0) PyErr_Clear(); 
    Py_RETURN_NONE; 
}
