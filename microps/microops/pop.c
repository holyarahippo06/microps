#include "microops.h"
PyObject* micro_pop(PyObject* list, PyObject* index) { 
    if (PyList_Check(list)) {
        Py_ssize_t idx = PyLong_AsSsize_t(index);
        if (idx < 0 || idx >= PyList_Size(list)) {
            Py_RETURN_NONE;
        }
        PyObject* item = PyList_GetItem(list, idx);
        Py_INCREF(item);
        PySequence_DelItem(list, idx);
        return item;
    }
    Py_RETURN_NONE;
}
