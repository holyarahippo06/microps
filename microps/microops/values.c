#include "microops.h"
PyObject* micro_values(PyObject* dict) { 
    if (PyDict_Check(dict)) {
        return PyDict_Values(dict);
    }
    Py_RETURN_NONE;
}
