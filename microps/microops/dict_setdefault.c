#include "microops.h"
PyObject* micro_dict_setdefault(PyObject* dict, PyObject* key, PyObject* default_val) {
    if (!PyDict_Check(dict)) {
        Py_INCREF(default_val);
        return default_val;
    }
    PyObject* value = PyDict_GetItem(dict, key);
    if (value) {
        Py_INCREF(value);
        return value;
    }
    PyDict_SetItem(dict, key, default_val);
    Py_INCREF(default_val);
    return default_val;
}
