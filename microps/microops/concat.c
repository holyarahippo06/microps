#include "microops.h"
PyObject* micro_concat(PyObject* a, PyObject* b) { 
    return PySequence_Concat(a, b);
}
