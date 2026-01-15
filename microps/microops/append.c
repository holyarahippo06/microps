#include "microops.h"
PyObject* micro_append(PyObject* list, PyObject* item) { 
    if (PyList_Check(list)) {
        PyList_Append(list, item);
    }
    Py_RETURN_NONE;
}
