#include "microops.h"
PyObject* micro_reverse(PyObject* list) { 
    if (PyList_Check(list)) {
        PyList_Reverse(list);
    }
    Py_RETURN_NONE;
}
