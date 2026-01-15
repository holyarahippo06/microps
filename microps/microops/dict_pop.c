#include "microops.h"
PyObject* micro_dict_pop(PyObject* dict, PyObject* key, PyObject* default_val) {
    if (!PyDict_Check(dict)) {
        Py_INCREF(default_val);
        return default_val;
    }
    PyObject* value = PyDict_GetItem(dict, key);
    if (value) {
        Py_INCREF(value);
        PyDict_DelItem(dict, key);
        return value;
    }
    Py_INCREF(default_val);
    return default_val;
}
