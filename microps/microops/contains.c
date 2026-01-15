#include "microops.h"
PyObject* micro_contains(PyObject* container, PyObject* item) { 
    int result = PySequence_Contains(container, item);
    if (result < 0) { PyErr_Clear(); return PyBool_FromLong(0); }
    return PyBool_FromLong(result);
}
