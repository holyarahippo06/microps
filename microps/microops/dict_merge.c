#include "microops.h"
PyObject* micro_dict_merge(PyObject* dict1, PyObject* dict2) {
    if (!PyDict_Check(dict1) || !PyDict_Check(dict2)) Py_RETURN_NONE;
    PyDict_Merge(dict1, dict2, 1);
    Py_RETURN_NONE;
}
