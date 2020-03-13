---
title: A Reader Protocol for the SciPy Ecosystem
date: 2020-03-07
draft: true
---

*Summary: To make handling data across multiple file formats more seamless, the
SciPy ecosystem would benefit from a file-like protocol that returns
(potentially lazy) SciPy/PyData data structures when read. This can be achieved
in a distributed way without a dependency on or reference to any particular
library.*

Real scientific data analysis typically involves combining data from multiple
instruments, research groups, or techniques, each with their own storage formats
(e.g. CSV vs. TIFF) or layouts and metadata conventions within a given format
(e.g. NeXuS HDF5 vs. NetCDF HDF5).

Established libraries provide a succinct enough way to load many formats into
appropriate data structures, such as ``pandas.read_csv`` or
``dask.dataframe.read_csv`` and ``tifffile.imread`` or ``dask_image.imread``,
but can we make it easier to discover the available readers for a given format
and make handling multiple formats more seamless?

## A Reader API that rhymes with Python's file API

If we draw inspiration from Python's API for opening files

```python
file = open(...)
file.read()
...
file.close()
```

we could imagine a Scientific Python Reader API that "rhymes" with Python's
builtin API but returns a suitable SciPy/PyData data structure instead of
strings or bytes.

```python
from some_library import SomeReader
reader = SomeReader(...)
reader.read()
...
reader.close()
```

Before the widespread adoption of dask for deferred I/O and computation, this
pattern would have had limited scope because pulling up large array data all at
once is not viable for many real datasets. But if ``reader.read()`` may return a
`dask.array.Array`, a `dask.dataframe.DataFrame`, or an `xarray` data structure
backed by dask, `reader` can inexpensively and promptly construct one of these
objects with internal chunks and leave it to downstream code to
decide if and when to materialize them, in whole or in part.

## Use Entrypoints to make Readers discoverable

Libraries can use
[entrypoints](https://packaging.python.org/specifications/entry-points/) to
declare any objects they define that satisfy the Reader API.
Entrypoints were *formerly* a feature/quirk of setuptools but are now officially
part of the PyPA specification, thanks to efforts by Thomas Kluyver. Here is an
example using `setup.py`:

```python
# setup.py

setup(
    ...
    entry_points = {
        'TBD.readers': [
            'FORMAT = some_package:SomeReader',
            'ANOTHER_FORMAT = some_package:AnotherReader'
        ]
    }
)
```

Entrypoints are also supported in tool-specific `pyproject.toml` sections by
[flit](https://flit.readthedocs.io/en/latest/pyproject_toml.html#entry-points-sections)
and
[poetry](https://python-poetry.org/docs/pyproject/#plugins).
A name for the entrypoint group (`'TBD.readers'` here) is considered further
below.

New libraries may be created to implement the Reader interface on top of
existing I/O libraries. For example, a new `pandas_reader` library could be
published that wraps `pandas.read_csv` in the Reader API. In time, if that works
well, pandas could adopt this object itself along with an associated
`entry_points` declaration.  Importantly, it could do so **without adding any
dependency on or connection to any particular library**.

For the ``FORMAT`` it would be natural to standardize on using MIME type.
IANA maintains an
[official registry](https://www.iana.org/assignments/media-types/media-types.xhtml)
of formats (e.g. `'text/csv'`, `'image/tiff'`), and it
provides a method for defining application-specific formats outside of the
official registry (e.g. `'application/x-hdf'`).
Although MIME types are not as widely known to the scientist user--programmers
in the SciPy ecosystem as they are to web developers, MIME types do already
have a foothold in SciPy via IPython rich display's
[`_repr_mimebundle_`](https://ipython.readthedocs.io/en/stable/config/integrating.html#MyObject._repr_mimebundle_)
and the
[Jupyter data explorer](https://github.com/jupyterlab/jupyterlab-data-explorer).

## Dispatch based on resource type to a compatible Reader

On a parallel track, other libraries that focus on generalizing I/O and
abstracting over file formats, such as
[intake](https://intake.readthedocs.io/) and
[pims](http://soft-matter.github.io/pims), could develop tooling on top of this
protocol. Using Thomas Kluyver's slim library
[entrypoints](https://entrypoints.readthedocs.io/),
they could search the Python packages in a user's environment to discover all
``'TBD.readers'`` and their respective designated ``FORMAT``s. (The magic of
entrypoints is that this search can be performed inexpensively, without
importing the packages.)

In many scenarios, it would be possible to automatically detect a file's type
based on its file extension or
[signature](https://en.wikipedia.org/wiki/List_of_file_signatures) using the
standard library module
[mimetypes](https://docs.python.org/3/library/mimetypes.html) or one the
external libraries [puremagic](https://pypi.org/project/puremagic/),
[python-magic](https://pypi.org/project/python-magic/), or
[filetype](https://pypi.org/project/filetype/). Then, dispatching on MIME type
to a suitable Reader enables a succinct usage like

```python
import some_library

some_library.open('table.csv').read()  # dask.dataframe.DataFrame
some_library.open('array.npz').read()  # dask.array.Array
some_library.open('image_stack.tiff').read()  # xarray.DataArray
some_library.open('image_series/*.tiff').read()  # xarray.DataArray
some_library.open('video.mp4').read()  # xarray.DataArray
```

where an implementation of `open` may be

```python
import entrypoints
groups = entrypoints.get_group_all('TBD.readers')

def open(file, *args, **kwargs):
    mimetype = guess_mime_type(file)
    # Import just the Reader classes of interest.
    compatible_reader_classes = [ep.load() for ep in groups[mimetype]]
    # Choose among the compatible readers....
    # See discussion in next section.
    ...
    return reader_class(file, *args, **kwargs)
```

Within a given MIME type there can be significant variety of internal structure
or metadata conventions. (HDF5 is a common example.) For this, nested dispatch
may be the right idea: after the initial dispatch based on MIME type, the reader
registered for that MIME type may inspect the file further and do a second layer
of dispatch based on its contents/layout. For example, a general `HDF5Reader`
registered for the `'application/x-hdf'` MIME type may distinguish the file
based on its content and then dispatch to a
`NetCDFReader` or a `NeXuSTomographyReader`. Automatic inference would be
possible is some cases, while in others guidance from the user would be
required.

There may be no globally "correct" approach for this kind of dispatch, but there
need not be. Just as libraries can declare Readers without adopting a new
dependency, libraries can separately experiment with file type detection and/or
dispatch in ways that make sense for their respective user communities.

## Support a variety of data structures

Is it possible to standardize on one return type for `read()`? It seems that
the Reader protocol would need to support at least tabular and non-tabular data:
certain operations make sense on DataFrames but not on N-dimensional structures.
Also, while dask is a core part of the story for large data sets, in domains
where data sets are generally small, Readers that return in-memory data
structures may be appealing, either to avoid a dask dependency or for plain
simplicity.  Therefore it seems unlikely we can agree on less than two or
perhaps four data structures. Having more than 1, we may as well support N.

This also leaves room for Readers that return more specialized data structures
not yet mentioned here, including a
[sparse.COO](https://sparse.pydata.org/en/latest/generated/sparse.COO.html#sparse.COO)
array or a
[Glue data object](http://docs.glueviz.org/en/stable/developer_guide/data.html).

When multiple readers for a given MIME type are discovered, such as one
``'text/csv'`` Reader declared by pandas and another declared by dask.dataframe,
a function like `some_library.open` could use a heuristic to choose between them or present
options to the user. Different libraries can make different choices here; we
don't need to pick one "correct" priority. For example, perhaps the laziest
representation would win, with ``dask.dataframe.DataFrame`` (if available)
taking precedence over ``pandas.DataFrame``.

To facilitate this, we need Readers to tell us which data structure they return
from `read()`. Adapting an idea from intake, we could require Readers to define
a `container` attribute with the fully-qualified name of the type returned by
`read()`, as in

```py
reader.container == 'dask.dataframe.core.DataFrame'
```

This adds one more thing to implement, but the complete Reader API would still
be succinct and could be implemented in less than 100 lines of code in most
cases (building on top of existing I/O code).

```py
class SomeReader:
    container = '...'

    def __init__(self, ...):
        # May accept a file buffer, filepath, or file glob pattern, plus any
        # specific required or optional parameters necessary.
        # Not all underlying I/O can accept all of these, so we must allow
        # Readers to vary here. How to *make* a Reader will vary, but the API of
        # an instance once you *have* one is very locked down.

        # This may open a file/files and in some cases inspect enough to
        # validate that it can probably read successfully, but it should not
        # read or cache any large data.
        ...

    def read(self):
        # Construct and return an object of type `SomeReader.container`.
        ...

    def close(self):
        # Clean up any system resources (network connections, file handles)
        # that were created in __init__.
        ...

    def __enter__(self):
        return self

    def __exit__(self, *exc_details):
        self.close()
```

Alternatively, we could consider conveying this using type annotations,
but it seems wiser to wait until type annotations become more established in the
SciPy ecosystem in general.

There is a strict one-to-one mapping between a given Reader class and its
container. There is no way to override the container at ``__init__`` time. This
locked-down simplicity is important if we hope to scale the protocol via
distributed, community-based effort. Of course, downstream of calling
`reader.read()`, library or user code may downcast to a simpler structure, e.g.
extract a simple `numpy.ndarray` from an
`xarray.DataArray`-of-`dask.array.Array`s.

## Designed for community-based scaling

No one has the resources to write Readers for every bespoke format in common
use in the SciPy ecosystem. Microscopy formats alone---my home turf---comprise a
wilderness of persnickety variation.

If members of the SciPy ecosystem's distributed contributor base also feel the
pain of managing multiple file formats and believe that Reader adds value, they
will be able to quickly grasp its small API and may begin adding support in the
codebases that their community already uses.

Prior similar work, including
[PIMS readers](https://soft-matter.github.io/pims/v0.4.1/custom_readers.html),
[intake DataSources](https://intake.readthedocs.io/en/latest/api_base.html#intake.source.base.DataSource),
and
[databroker handlers](https://blueskyproject.io/event-model/external.html#handlers),
have similar goals and some overlap in their approach, but none combine all of:

* A very small API that rhymes with the usage for opening and reading files in
  Python
* Declaring `entry_points` for zero-dependency coordination between libraries
* Declaring MIME types to facilitate dispatch by file type
* Leveraging dask (and other libraries in that space) to leave any sub-selection
  / slicing to downstream code rather than managing it internally

This is a good time to be building out I/O tools that return richer data
structures.  Matplotlib is funded to develop a more context-aware data model for
matplotlib 4.0, and other libraries like glue which have long had such data
models seem poised to benefit as well. Improvements in this space can help drive
practical compliance with the
[FAIR](https://www.nature.com/articles/sdata201618) (Findable, Accessible,
Interoperable, Reusable) guiding principles for data management and stewardship.

## First Prototypes

* A prototype of one Reader (wrapping `tifffile`) and a simple example of
  MIME type dispatch have been sketched in a
  [proposal for PIMS](https://github.com/danielballan/pims2-prototype).

  Excerpt from example:

  ```python
  In [1]: import my_tiff_package

  In [2]: reader = my_tiff_package.TIFFReader('example_data/lfw_subset_as_stack.tif')

  In [3]: reader.read()
  Out[3]: dask.array<stack, shape=(200, 25, 25), dtype=float64, chunksize=(1, 25, 25), chunktype=numpy.ndarray>

  In [4]: reader.read().compute()
  <numpy array output, snipped>

  In [5]: import pims

  In [6]: pims.open('example_data/lfw_subset_as_stack.tif').read()
  Out[7]: dask.array<stack, shape=(200, 25, 25), dtype=float64, chunksize=(1, 25, 25), chunktype=numpy.ndarray>
  ```

  Illustration of the role of `close()` and context methods:

  ```python
  with TIFFReader(...) as reader:
      da = reader.read()
      arr = da.compute()  # works
  da.compute()  # fails, because underlying file handles are closed

* Two Readers (fixed-width formatted text and TIFF again) and a mechanism for
  integrating with intake's `DataSource` abstraction have been sketched in
  [danielballan/reader_prototype](https://github.com/danielballan/reader_prototype).

## Related questions not in scope

This design leaves room for libraries that define Reader-compliant objects and
libraries that make use of them to address questions such as:

* When to load directly and when to load in a deferred fashion, "lazily"
* When and how to leverage parallelism
* How to handle deeply hierarchical or unstructured data using container types
  not specifically mentioned here
* When to detect types implicitly and when to mark up types explicitly
* How to handle remote data and cloud resorces. (Individual Readers might
  leverage [fsspec](https://filesystem-spec.readthedocs.io/) for this, for
  example.)

Work in these areas is compatible with the proposed standard and need not be
explicitly addressed by it.

This also does not address how to discover readers that are not installed, i.e.
how to search PyPI for packages that may contain a relevant reader. This is also
important, but it raises questions about security and gatekeeping. Discovering
readers within an installed environment is a useful step.

## Why not just a function?

In general I prefer simple functions to object-oriented structures. Why not
just declare functions that return the data directly in one step, instead of
`SomeReader(...).read()`?

* As with the built-in `open(...).read()`, it is useful to have a two-step
  process where the first step checks if the resource can even be found and
  accessed, and the second step does the reading.
* The `close()` method and context manager methods give control over when any
  system resources (file handles, network connections) will be released. A
  simple function would have to contain these resources in a closure, with no
  way of explicitly releasing them.
* We need some place to indicate our ``container``. Frameworks that can
  standardize on always returning the same type from ``read()`` do not need such
  a thing, but a share standard that can return a variety of types would, for
  the reasons described earlier. This could be implemented by putting a simple
  function *next* to its container, as in ``{'function': read, 'container':
  'dask.array.Array'}``, and pointing the entrypoint at that. But this is
  perhaps not any "cleaner" than a small class that implements an interface
  that is already established in the language.

## How should we organize?

If this idea gains buy-in from library maintainers, where should we document and
advertise this entrypoint and what can be done with it?  How should we spell the
entrypoint group name (`'TBD.readers'`)?

Entrypoints are generally scoped to a
package to avoid name collisions, as in `'nbconvert.exporters'` or
`'pandas_plotting_backends'`. We could center on an I/O-abstracting library such
as `'intake.readers'` or `'pims.readers'`. (To be clear, it is an open question
whether the `Reader` idea will be incorporated into either.) But that risks
giving the incorrect impression that the functionality is tied to a particular
library, when in fact these libraries could go away and the entrypoint would
still be useful.

With the necessary community support (perhaps a NEP process) we might claim a
more generic namespace like `'scikit.readers'`, `'scipy.readers'`, or
`'pydata.readers'` to clearly communicate that any project can declare such an
entrypoint and any project can perform Reader discovery without reference to or
dependency on a specific project.
