#include <stdlib.h>

#include <Python.h>


PyObject* cjson_loads(PyObject* self, PyObject* args) {
    const char *input_json;

    if (!PyArg_ParseTuple(args, "s", &input_json)) {
        PyErr_SetString(PyExc_TypeError, "Expected a string");
        return NULL;
    }

    PyObject *dict = PyDict_New();
    if (!dict) {
        PyErr_SetString(PyExc_MemoryError, "Failed to create dictionary");
        return NULL;
    }

    int part_memory = 40;
    char* key_buf = calloc(part_memory, sizeof(char));
    char* val_buf = calloc(part_memory, sizeof(int));
    int size_key = 0, size_val = 0;
    int flag_key = 0, flag_val = 0, in_val = 0, flag_num = 0;
    int key_index = 0, val_index = 0;

    for (const char *ptr = input_json; *ptr; ++ptr) {

        if (*ptr != '{') {
            if (*ptr == '"' && !flag_val) { // start of key
                flag_key = 1;
            }
            if (*ptr == ':') { // end of key
                flag_val = 1;
                flag_key = 0;
            }
            if (flag_val && !in_val && (*ptr == '"' || (*ptr <= '9' && *ptr >= '0'))) { // type of val
                flag_num = (*ptr == '"') ? 0 : 1;
                in_val = 1;
            }
            if (*ptr == ',' || *ptr == '}') { // end of pair (key, val)
                flag_val = 0;
                in_val = 0;
            }

            if (flag_key && *ptr != '"') { // add key symbol
                key_buf[key_index++] = *ptr;
                if (key_index == size_key) {
                    size_key += part_memory;
                    key_buf = realloc(key_buf, size_key);
                }
            }
            if (in_val) { // add val symbol
                if (*ptr == '"') continue;
                val_buf[val_index++] = *ptr;
                if (val_index == size_val) {
                    size_val += part_memory;
                    val_buf = realloc(val_buf, size_val);
                }
            }
            if ((!flag_key && key_index > 0) && (!flag_val && val_index > 0)) { // add pair to dict
                key_buf[key_index] = '\0';
                val_buf[val_index] = '\0';

                PyObject *py_key = Py_BuildValue("s", key_buf);
                PyObject *py_val = (flag_num) ? Py_BuildValue("i", atoi(val_buf)) : Py_BuildValue("s", val_buf);
                PyDict_SetItem(dict, py_key, py_val);

                key_index = 0, val_index = 0, flag_num = 0;
                flag_key = 0, flag_val = 0, in_val = 0;
                free(key_buf);
                free(val_buf);
                key_buf = calloc(part_memory, sizeof(char));
                val_buf = calloc(part_memory, sizeof(int));
                size_key = part_memory, size_val = part_memory;
            }
        }
    }
    if (key_buf) free(key_buf);
    if (val_buf) free(val_buf);

    return dict;
}
