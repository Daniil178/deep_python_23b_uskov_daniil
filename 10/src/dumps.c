#include <stdlib.h>
#include <stdio.h>

#include <Python.h>


PyObject* cjson_dumps(PyObject* self, PyObject* args) {
    PyObject *dict;

    if (!PyArg_ParseTuple(args, "O", &dict)) {
        PyErr_SetString(PyExc_TypeError, "Expected a PyObject");
        return NULL;
    }

    if (!PyDict_CheckExact(dict)) {
        PyErr_SetString(PyExc_TypeError, "Expected a dictionary");
        return NULL;
    }

    PyObject *result = PyUnicode_FromString("{");

    PyObject *key, *value;
    Py_ssize_t pos = 0;

    PyObject *comma = PyUnicode_FromString(", ");
    PyObject *closing_brace = PyUnicode_FromString("}");

    while (PyDict_Next(dict, &pos, &key, &value)) {
        const char *c_key = PyUnicode_AsUTF8(PyObject_Str(key));
        PyObject *str_value = PyObject_Str(value);
        const char *c_value = PyUnicode_AsUTF8(str_value);
        PyObject *temp;

        if (PyNumber_Check(value)) {
            temp = PyUnicode_FromFormat("\"%s\": %d", c_key, atoi(c_value));
        } else {
            temp = PyUnicode_FromFormat("\"%s\": \"%s\"", c_key, c_value);
        }

        Py_DECREF(str_value);
        PyObject *concat_result = PyUnicode_Concat(result, temp);
        if (PyDict_Size(dict) > 1 && pos < PyDict_Size(dict)) {
            PyUnicode_Append(&concat_result, comma);
        }

        if (concat_result == NULL) {
            PyErr_SetString(PyExc_RuntimeError, "Failed to concatenate strings");
            Py_DECREF(result);
            Py_DECREF(comma);
            Py_DECREF(closing_brace);
            return NULL;
        }

        Py_DECREF(result);
        result = concat_result;
    }

    PyObject *final_result = PyUnicode_Concat(result, closing_brace);

    Py_DECREF(comma);
    Py_DECREF(result);
    Py_DECREF(closing_brace);

    return final_result;
}
