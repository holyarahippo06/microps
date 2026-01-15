#include "microops.h"
PyObject* micro_insert(PyObject* list, PyObject* index, PyObject* item) {
    if (PyList_Check(list)) {
        Py_ssize_t idx = PyLong_AsSsize_t(index);
        PyList_Insert(list, idx, item);
    }
    Py_RETURN_NONE;
}
