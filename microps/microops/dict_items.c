#include "microops.h"
PyObject* micro_dict_items(PyObject* dict) {
    if (!PyDict_Check(dict)) Py_RETURN_NONE;
    return PyDict_Items(dict);
}
