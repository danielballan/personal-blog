---
title: A Reader Protocol for the SciPy Ecosystem
date: 2020-03-07
---

*Summary: The SciPy ecosystem would benefit from a file-like protocol that
returns (potentially lazy) SciPy/PyData data structures when read. This can be
achieved in a distributed way without adopting any particular library.*

Real scientific data analysis typically involves combining data from multiple
instruments, research groups, or techniques, each with their own storage formats
(e.g. CSV vs TIFF) or layouts and metdata conventions within a given format
(e.g. NeXuS HDF5 vs NetCDF HDF5).

Established libraries provide a succinct enough way to load many formats into
appropriate data structures, such as ``pandas.read_csv`` or
``dask.dataframe.read_csv`` and ``tifffile.imread`` or ``dask_image.imread``.

Can we make it easier to discover the available readers for a given format
and make handling multiple formats more seamless?

## A Reader API that rhymes with Python's file API

If we draw inspiration Python's API for opening files

```python
file = open(...)
file.read()
...
file.close()
```

we could imagine a "Scientific Python Reader API" that rhymes well with this API
but returns appropriate SciPy/PyData data structure instead of strings or bytes.

```python
from some_library import SomeReader
reader = SomeReader(...)
reader.read()
...
reader.close()
```

Before the widespread adoption of dask for deferred I/O and computation, this
pattern would have had limited scope because pulling up large array data in one
step is not viable for many real datasets. But if ``reader.read()`` may return a
`dask.array.Array` or a `dask.dataframe.DataFrame` or an `xarray` data structure
backed by dask, `reader` can inexpensively and promptly return one of these
objects with reasonably-sized internal chunks and leave it to downstream code to
decide if and when to materialize them, in whole or in part.

## Use Entrypoints to Make Readers Discoverable

Libraries that implement this Reader API can use
[entrypoints](https://packaging.python.org/specifications/entry-points/) to
declare them, using a standard entrypoint group agreed on by the community
(TBD).

```python
# setup.py

setup(
    ...
    entry_points = {'TBD.readers' ['FORMAT = some_package:SomeReader']}
)
```

For the ``FORMAT`` it would be natural to specify a MIME type string.
IANA maintains an official registry of formats (e.g. ``'image/png'``), and it
also defines a standard for adding application-specific formats outside of the
official standard (e.g. ``'application/x-hdf'``).
(Although MIME types are not as well known to the scientific user--programmers
that in the SciPy ecosystem, MIME types do already have foothold in SciPy via
IPython rich display's
[`_repr_mimebundle_`](https://ipython.readthedocs.io/en/stable/config/integrating.html#MyObject._repr_mimebundle_)
and the
[Jupyter data explorer](https://github.com/jupyterlab/jupyterlab-data-explorer).)

New libraries may be created to implement this interface on top of existing I/O
libraries. For example, a `pandas_reader` library could be published that wraps
`pandas.read_csv` and/or `dask.dataframe.read_csv` in the Reader API. In time,
if that works well, established libraries like tifffile and pandas could add
such objects and an associated `entry_points` declaration. Importantly, they
could do so without adding a new dependency on or connection to any
particular library.

## Build Tools Dispatch to a Compatible Reader

On a parallel track, other libraries that focus on generalizing I/O and
abstracting over file formats, such as
[intake](https://intake.readthedocs.io/) and
[pims](http://soft-matter.github.io/pims), could develop tooling that uses this
protocol. Using Thomas Kluyver's slim library
[entrypoints](https://packaging.python.org/specifications/entry-points/),
they could search the Python packages in a user's environment to discover their
``'TBD.readers'`` and their respective designated ``FORMAT``. (The magic of
entrypoints is that this search can be performed inexpensively, without
importing the packages.)

In many scenarios, it would be possible to automatically detect a file's type
based on its file extension or
[signature](https://en.wikipedia.org/wiki/List_of_file_signatures) using the
standard library module
[mimetypes](https://docs.python.org/3/library/mimetypes.html) or one the
external libraries [puremagic](https://pypi.org/project/puremagic/),
[python-magic](https://pypi.org/project/python-magic/), or
[filetype](https://pypi.org/project/filetype/). This would enable to dispatch
MIME type to a compatible Reader, enable the succinct usage

```python
from some_library import open

open('table.csv').read()  # dask.dataframe.DataFrame
open('array.npz').read()  # numpy.ndarray
open('image_stack.tiff').read()  # xarray.DataArray
open('image_series/*.tiff').read()  # xarray.DataArray
open('video.mov').read()  # xarray.DataArray
```

where an implementation of `open` may be

```python
import entrypoints
groups = entrypoints.get_groups_all('TBD.readers')

def open(file, *args, **kwargs):
    mimetype = guess_mime_type(file)
    # Import just the Reader classes of interest.
    compatible_reader_classes = [ep.load() for ep in groups[mimetype]]
    # Choose among the compatible readers....see discussion below.
    return reader_class(file, *args, **kwargs)
```

Within a given MIME type there can be significant variety of internal structure
or metadata conventions. (HDF5 is a common example.) For this, nested dispatch
may be the right idea: after the initial dispatch based on MIME type, the reader
registered for that MIME type may inspect the file further and do a second layer
of dispatch based on its contents/layout.

## Managing a Variety of Return Types

Is it possible to standardize one return type for `read()`? It seems that
the Reader protocol would need to support at least tabular and non-tabular data:
certain operations make sense on DataFrames but not on N-D structures. Also,
while dask is a core part of the story for large data sets, in certain domains
Readers that return an in-memory data structures may be appealing, either to
avoid a dask dependency or for plain simplicity. Therefore it seems unlikely
we can agree on less than two or perhaps four data structures. Having more than
1, we may as well support N.

When multiple readers for a given MIME type are discovered, some heuristic could
be used to choose between them. Different libraries can make different choices
here; we don't need to pick one "correct" priority. For example, perhaps the
richest representation would be chosen, with ``xarray.DataArray`` taking
precedence over ``numpy.ndarray`` if available; and/or perhaps the laziest
representation would win, with ``dask.dataframe.DataFrame`` taking precedence
over ``pandas.DataFrame``. To facilitate this, we might specify one more
required attribute on ``Reader``. Borrowing an idea from intake, we could
require Readers to carry a ``container`` attribute, with the string of the
fully-qualified name of the type returned by `read()`, as in

```py
reader.container == 'dask.dataframe.core.DataFrame'
```

This diverges from the neat simplicity of the original analogy---"Readers are
just like files that return SciPy data structures when you read them."---but
it's a reasonable mitigation of the return instability of ``read()``. The
complete Reader API would still be quite succinct and could be implemented in
less than 100 LOC in most cases.

```py
class SomeReader:
    container = '...'

    def __init__(self, ...):
        ...

    def read(self):
        ...

    def close(self)
        ...
```

Alternatively, we could consider using type annotations, but it may be wiser to
wait until they have more a foothold in the SciPy ecosytem.
