#include "microops.h"
PyObject* micro_to_bool(PyObject* a) { 
    return PyBool_FromLong(PyObject_IsTrue(a)); 
}
