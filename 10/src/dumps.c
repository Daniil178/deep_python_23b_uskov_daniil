#include <stdlib.h>
#include <stdio.h>

#include <Python.h>


PyObject* cjson_dumps(PyObject* self, PyObject* args) {
    PyObject *dict;

    if (!PyArg_ParseTuple(args, "O", &dict)) {
        PyErr_SetString(PyExc_TypeError, "Expected a dictionary");
        return NULL;
    }

    PyObject *result = PyUnicode_FromString("{");
    PyObject *items = PyDict_Items(dict);
    Py_ssize_t size = PyList_Size(items);

    for (Py_ssize_t i = 0; i < size; ++i) {
        PyObject *item = PyList_GetItem(items, i);
        PyObject *key = PyTuple_GetItem(item, 0);
        PyObject *value = PyTuple_GetItem(item, 1);

        PyObject *repr_key = PyObject_Repr(key);
        PyObject *repr_value = PyObject_Repr(value);

        PyObject *str_key = PyUnicode_AsUTF8String(repr_key);
        PyObject *str_value = PyUnicode_AsUTF8String(repr_value);

        const char *c_key = PyBytes_AS_STRING(str_key);
        const char *c_value = PyBytes_AS_STRING(str_value);

        size_t key_len = strlen(c_key) - 2;
        size_t value_len = strlen(c_value) - 2;

        PyObject *temp;
        if (PyNumber_Check(value)) {
            temp = PyUnicode_FromFormat("\"%.*s\": %d", (int)key_len, c_key + 1, atoi(c_value));
        } else {
            temp = PyUnicode_FromFormat("\"%.*s\": \"%.*s\"", (int)key_len, c_key + 1, (int)value_len, c_value + 1);
        }

        PyObject *comma = PyUnicode_FromString(", ");
        if (i == size - 1) {
            comma = PyUnicode_FromString("");
        }

        PyObject *concat_result = PyUnicode_Concat(result, temp);
        PyUnicode_Append(&concat_result, comma);

        Py_DECREF(repr_key);
        Py_DECREF(repr_value);
        Py_DECREF(str_key);
        Py_DECREF(str_value);
        Py_DECREF(temp);
        Py_DECREF(comma);

        if (concat_result == NULL) {
            PyErr_SetString(PyExc_RuntimeError, "Failed to concatenate strings");
            Py_DECREF(result);
            Py_DECREF(items);
            return NULL;
        }

        Py_DECREF(result);
        result = concat_result;
    }

    PyObject *closing_brace = PyUnicode_FromString("}");
    PyObject *final_result = PyUnicode_Concat(result, closing_brace);

    Py_DECREF(items);
    Py_DECREF(result);
    Py_DECREF(closing_brace);

    return final_result;
}
