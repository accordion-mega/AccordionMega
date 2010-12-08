/***************************************************************************
 *   Copyright (C) 2006 by Patrick Stinson                                 *
 *   patrickkidd@gmail.com                                                 *
 *                                                                         *
 *   Permission is hereby granted, free of charge, to any person obtaining *
 *   a copy of this software and associated documentation files (the       *
 *   "Software"), to deal in the Software without restriction, including   *
 *   without limitation the rights to use, copy, modify, merge, publish,   *
 *   distribute, sublicense, and/or sell copies of the Software, and to    *
 *   permit persons to whom the Software is furnished to do so, subject to *
 *   the following conditions:                                             *
 *                                                                         *
 *   The above copyright notice and this permission notice shall be        *
 *   included in all copies or substantial portions of the Software.       *
 *                                                                         *
 *   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,       *
 *   EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF    *
 *   MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.*
 *   IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR     *
 *   OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, *
 *   ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR *
 *   OTHER DEALINGS IN THE SOFTWARE.                                       *
 ***************************************************************************/

#include <Python.h>
#include <numarray/numarray.h>
#include <numarray/libnumarray.h>
#include <sndfile.h>

#ifndef Py_RETURN_NONE
#define Py_RETURN_NONE Py_INCREF(Py_None); return Py_None;
#endif


static PyObject *SndFileError;


static PyObject *get_sf_error(int err)
{
  return NULL;
}


typedef struct {
  PyObject_HEAD;
  SNDFILE *sndfile;
  SF_INFO sfinfo;
} SndFile;


static void
SndFile_dealloc(SndFile *self)
{
  if(self->sndfile)
    sf_close(self->sndfile);
  self->ob_type->tp_free((PyObject *) self);
}


static PyObject *
SndFile_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
  SndFile *self = (SndFile *) type->tp_alloc(type, 0);
  self->sndfile = NULL;
  return (PyObject *) self;
}


static int SndFile_init(SndFile *self, PyObject *args, PyObject *kwds)
{
  return 0;
}


static PyObject *
SndFile_open(SndFile *self, PyObject *args)
{
  char *fname;
  int samplerate = 44100;
  int channels = 2;

  if(self->sndfile)
    {
      PyErr_Format(SndFileError, "sndfile already open");
      return NULL;
    }

  if(!PyArg_ParseTuple(args, "s|ii", &fname, &samplerate, &channels))
      return NULL;

  self->sfinfo.channels = channels;
  self->sfinfo.samplerate = samplerate;

  self->sndfile = sf_open(fname, SFM_READ, &self->sfinfo);
  if(self->sndfile == NULL)
    {
      PyErr_Format(SndFileError, "sf_open failed.");
      return NULL;
    }

  Py_RETURN_NONE;
}



static PyObject *
SndFile_close(SndFile *self, PyObject *args)
{
  int err;
  
  if(self->sndfile == NULL)
    {
      PyErr_Format(SndFileError, "sndfile already open");
      return NULL;
    }
  
  err = sf_close(self->sndfile);
  if(err != 0)
    return get_sf_error(err);
  self->sndfile = NULL;

  Py_RETURN_NONE;
}
static PyObject *
SndFile_info(SndFile *self, PyObject *args)
{
  PyObject *frames = NULL;
  PyObject *samplerate = NULL;
  PyObject *channels = NULL;
  PyObject *format = NULL;
  PyObject *sections = NULL;
  PyObject *seekable = NULL;
  PyObject *info = NULL;

  if(!self->sndfile)
    {
      PyErr_Format(SndFileError, "sndfile not open yet");
      return NULL;
    }

  frames = PyInt_FromLong(self->sfinfo.frames);
  if(frames == NULL) goto fail;

  samplerate = PyInt_FromLong(self->sfinfo.samplerate);
  if(samplerate == NULL) goto fail;

  channels = PyInt_FromLong(self->sfinfo.channels);
  if(channels == NULL) goto fail;

  format = PyInt_FromLong(self->sfinfo.format);
  if(format == NULL) goto fail;

  sections = PyInt_FromLong(self->sfinfo.sections);
  if(sections == NULL) goto fail;

  seekable = PyInt_FromLong(self->sfinfo.seekable);
  if(seekable == NULL) goto fail;

  info = PyDict_New();
  if(info == NULL) goto fail;

  if(PyDict_SetItemString(info, "frames", frames))
    goto fail;
  if(PyDict_SetItemString(info, "samplerate", samplerate))
    goto fail;
  if(PyDict_SetItemString(info, "channels", channels))
    goto fail;
  if(PyDict_SetItemString(info, "format", format))
    goto fail;
  if(PyDict_SetItemString(info, "sections", sections))
    goto fail;
  if(PyDict_SetItemString(info, "seekable", seekable))
    goto fail;
  
  return info;

 fail:
  Py_XDECREF(frames);
  Py_XDECREF(samplerate);
  Py_XDECREF(channels);
  Py_XDECREF(format);
  Py_XDECREF(sections);
  Py_XDECREF(seekable);
  Py_XDECREF(info);
  return NULL;
}


static PyObject *
SndFile_read(SndFile *self, PyObject *args)
{
  int items;
  PyObject *osound;
  PyArrayObject *sound;
  PyObject *typeObject;
  int type;

  if(!self->sndfile)
    {
      PyErr_Format(SndFileError, "sndfile not open yet");
      return NULL;
    }

  if(!PyArg_ParseTuple(args, "O", &osound)) {
    return NULL;
  }
  Py_INCREF(osound);

  if(!NA_NumArrayCheck(osound))
    {
      PyErr_Format(SndFileError, "argument not a numarray.NumArray");
      return NULL;
    }

  typeObject = PyObject_CallMethod(osound, "type", NULL);
  type = NA_typeObjectToTypeNo(typeObject);
  Py_DECREF(typeObject);

  sound = (PyArrayObject *) NA_InputArray(osound, type, NUM_C_ARRAY);

  if(sound == NULL)
    {
      PyErr_SetString(SndFileError, 
                      "couldn't convert array to PyArrayObject.");
      return NULL;
    }
  else if(sound->nd != 1)
    {
      Py_DECREF(sound);
      PyErr_Format(SndFileError,
                   "sound arrays must have 1 dimension, not (%d)",
                   sound->nd);
      return NULL;
    }

  items = sound->dimensions[0];
  switch(type)
    {
    case tFloat32:
      items = sf_read_float(self->sndfile, NA_OFFSETDATA(sound), items);
      break;
      
    case tFloat64:
      items = sf_read_double(self->sndfile, NA_OFFSETDATA(sound), items);
      break;
      
    case tInt16:
      items = sf_read_short(self->sndfile, NA_OFFSETDATA(sound), items);
      break;

    case tInt32:
      items = sf_read_int(self->sndfile, NA_OFFSETDATA(sound), items);
      break;

    case tBool:
    case tInt8:
    case tUInt8:
    case tInt64:
    case tUInt64:
    case tComplex32:
    case tComplex64:
      PyErr_Format(SndFileError, "invalid numarray type");
      return NULL;
    };

  return Py_BuildValue("i", items);
}


static PyObject *
SndFile_readf(SndFile *self, PyObject *args)
{
  int items;
  PyObject *osound;
  PyArrayObject *sound;
  PyObject *typeObject;
  int type;

  if(!self->sndfile)
    {
      PyErr_Format(SndFileError, "sndfile not open yet");
      return NULL;
    }

  if(!PyArg_ParseTuple(args, "O", &osound)) {
    return NULL;
  }
  Py_INCREF(osound);

  if(!NA_NumArrayCheck(osound))
    {
      PyErr_Format(SndFileError, "argument not a numarray.NumArray");
      return NULL;
    }

  typeObject = PyObject_CallMethod(osound, "type", NULL);
  type = NA_typeObjectToTypeNo(typeObject);
  Py_DECREF(typeObject);

  sound = (PyArrayObject *) NA_InputArray(osound, type, NUM_C_ARRAY);

  if(sound == NULL)
    {
      PyErr_SetString(SndFileError, 
                      "couldn't convert array to PyArrayObject.");
      return NULL;
    }
  else if(sound->nd != 1)
    {
      Py_DECREF(sound);
      PyErr_Format(SndFileError,
                   "sound arrays must have 1 dimension, not (%d)",
                   sound->nd);
      return NULL;
    }

  items = sound->dimensions[0] / self->sfinfo.channels;
  switch(type)
    {
    case tFloat32:
      items = sf_readf_float(self->sndfile, NA_OFFSETDATA(sound), items);
      break;
      
    case tFloat64:
      items = sf_readf_double(self->sndfile, NA_OFFSETDATA(sound), items);
      break;
      
    case tInt16:
      items = sf_readf_short(self->sndfile, NA_OFFSETDATA(sound), items);
      break;

    case tInt32:
      items = sf_readf_int(self->sndfile, NA_OFFSETDATA(sound), items);
      break;

    case tBool:
    case tInt8:
    case tUInt8:
    case tInt64:
    case tUInt64:
    case tComplex32:
    case tComplex64:
      PyErr_Format(SndFileError, "invalid numarray type");
      return NULL;
    };

  return Py_BuildValue("i", items);
}


static PyObject *
SndFile_seek(SndFile *self, PyObject *args)
{
  int whence;
  int frames;
  sf_count_t ret;

  if(!PyArg_ParseTuple(args, "ii", &frames, &whence))
    return NULL;

  ret = sf_seek(self->sndfile, frames, whence);

  if(ret == -1)
    {
      PyErr_SetString(SndFileError, "sf_seek failed");
      return NULL;
    }

  return Py_BuildValue("i", ret);
}


static PyMethodDef SndFile_methods[] = {

  {"open", (PyCFunction) SndFile_open, METH_VARARGS,
   "On success, the sf_open function returns a non NULL pointer which\n"
   "should be passed as the first parameter to all subsequent libsndfile\n"
   "calls dealing with that audio file. On fail, the sf_open function\n"
   "returns a NULL pointer.\n"
   "\n"
   "open(fpath, samplerate, channels)\n"},

  {"close", (PyCFunction) SndFile_close, METH_NOARGS,
   "The close function closes the file, deallocates its internal buffers."},

  {"info", (PyCFunction) SndFile_info, METH_NOARGS,
   "Return a dict containing the attributes if struct SF_INFO."},

  {"read", (PyCFunction) SndFile_read, METH_VARARGS,
   "Read a number of items into a passed numarray. The function will try "
   "to read using the item type of the numarrya. Return the number of "
   "items actually read. "},

  {"readf", (PyCFunction) SndFile_readf, METH_VARARGS,
   "Read a number of items into a passed numarray. The function will try "
   "to read using the item type of the numarrya. Return the number of "
   "items actually read. "},

  {"seek", (PyCFunction) SndFile_seek, METH_VARARGS,
   "seek to a place in the file.\n"
   "seek(frames, whence), where whence is one of "
   "SEEK_SET, SEEK_CUR, SEEK_END"},

  {NULL},
};


static PyTypeObject SndFileType = {
  PyObject_HEAD_INIT(NULL)
  0,                         /*ob_size*/
  "sndfile.SndFile",   /*tp_name*/
  sizeof(SndFile),      /*tp_basicsize*/
  0,                         /*tp_itemsize*/
  (destructor) SndFile_dealloc,                         /*tp_dealloc*/
  0,                         /*tp_print*/
  0,                         /*tp_getattr*/
  0,                         /*tp_setattr*/
  0,                         /*tp_compare*/
  0,                         /*tp_repr*/
  0,                         /*tp_as_number*/
  0,                         /*tp_as_sequence*/
  0,                         /*tp_as_mapping*/
  0,                         /*tp_hash */
  0,                         /*tp_call*/
  0,                         /*tp_str*/
  0,                         /*tp_getattro*/
  0,                         /*tp_setattro*/
  0,                         /*tp_as_buffer*/
  Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,        /*tp_flags*/
  "Libsndfile is a library designed to allow the reading and writing of\n"
"many different sampled sound file formats (such as MS Windows WAV and\n"
"the Apple/SGI AIFF format) through one standard library interface.\n"
"\n"
"During read and write operations, formats are seamlessly converted\n"
"between the format the application program has requested or supplied\n"
"and the file's data format. The application programmer can remain\n"
"blissfully unaware of issues such as file endian-ness and data\n"
"format. See Note 1 and Note 2.\n"
"\n"
"Every effort is made to keep these documents up-to-date, error free\n"
"and unambiguous. However, since maintaining the documentation is the\n"
"least fun part of working on libsndfile, these docs can and do fall\n"
"behind the behaviour of library. If any errors omissions or\n"
"ambiguities are found, please notify Erik de Castro Lopo.\n"
"\n"
"Finally, if you think there is some feature missing from libsndfile,\n"
"check that it isn't already implemented (and documented) here.\n"
"\n"
"Module attributes:\n"
"\n"
"class SndFile()\n"
"SEEK_SET\n"
"SEEK_CUR\n"
"SEEK_END",        /* tp_doc */
  0,                         /* tp_traverse */
  0,                         /* tp_clear */
  0,                         /* tp_richcompare */
  0,                         /* tp_weaklistoffset */
  0,                         /* tp_iter */
  0,                         /* tp_iternext */
  SndFile_methods,        /* tp_methods */
  0,        /* tp_members */
  0,                         /* tp_getset */
  0,                         /* tp_base */
  0,                         /* tp_dict */
  0,                         /* tp_descr_get */
  0,                         /* tp_descr_set */
  0,                         /* tp_dictoffset */
  (initproc)SndFile_init, /* tp_init */
  0,                         /* tp_alloc */
  SndFile_new,              /* tp_new */
};


static PyMethodDef sndfile_methods[] = {

  {NULL}

};


PyMODINIT_FUNC initsndfile(void)
{
  PyObject *module;

  if(PyType_Ready(&SndFileType) < 0)
    return;

  module = Py_InitModule3("sndfile", sndfile_methods,
                          "libsndfile wrapper");
  
  Py_INCREF(&SndFileType);
  PyModule_AddObject(module, "SndFile", 
                     (PyObject *)&SndFileType);

  SndFileError = PyErr_NewException("sndfile.error", NULL, NULL);
  Py_INCREF(SndFileError);
  PyModule_AddObject(module, "error", SndFileError);

  if(PyModule_AddIntConstant(module, "SEEK_SET", SEEK_SET) == -1)
    return;
  if(PyModule_AddIntConstant(module, "SEEK_CUR", SEEK_CUR) == -1)
    return;
  if(PyModule_AddIntConstant(module, "SEEK_END", SEEK_END) == -1)
    return;

  import_libnumarray();
}
