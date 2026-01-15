#include "microops.h"
PyObject* micro_dict_update(PyObject* dict, PyObject* other) {
    if (!PyDict_Check(dict)) Py_RETURN_NONE;
    PyDict_Update(dict, other);
    Py_RETURN_NONE;
}
