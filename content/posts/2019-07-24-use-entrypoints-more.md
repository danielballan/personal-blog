---
title: The SciPy Ecosystem Should Use Custom Entrypoints More
summary: Python library developers can declare custom ``entry_points`` in their packages. This language feature is a good fit for "plugin discovery", and it should be more widely used.
date: 2019-07-25
tags:
- SciPy
- entrypoints
---


Think of a Python library that has some programmatic interface, some protocol,
intended to be "pluggable" by other libraries. Sometimes it is useful to search
the set of installed Python packages to discover plugins that extend that
interface. I recently learned of a nice way to do this that I think should be
more widely known and used.

## Entrypoints are commonly used for "console scripts"

The most familiar use of the ``entry_points`` parameter is defining
executables in a Python package. A minimal example of that looks like:

{{< highlight python "hl_lines=7 8 9" >}}
# setup.py
from setuptools import setup

setup(
    name='stuff',
    pymodules=['stuff'],
    entry_points={
        'console_scripts': [
            'my_custom_executable = stuff:main',
            ]
        }
    )
{{< / highlight >}}

```python
# stuff.py
def main():
    print("Hello world")
```


```bash
$ my_custom_executable
Hello world
```

## Entrypoints can also be used to advertise custom extension points

The Python library [intake](https://intake.readthedocs.io) defines a protocol
for "drivers" that can read from some file format or database and return a
Python data structure. Intake comes with some drivers included, and external
libraries can define their own. Intake compiles a registry of the drivers it can
find installed on the system. External libraries can advertise their drivers to
intake by including an ``'intake.drivers'`` entrypoint. For example, the library
``intake_xarray`` includes a driver for reading zarr files.

{{< highlight python "hl_lines=3 4 5" >}}
setup(
    ...
    entry_points={
        'intake.drivers': [
            'zarr = intake_xarray.xzarr:ZarrSource',
            ...
            ]
        }
    )
{{< / highlight >}}

To discover this driver, intake uses the small library
[entrypoints](https://entrypoints.readthedocs.io), which provides a simple
high-level API for searching all the installed Python packages for a given
entrypoint.


```python
>>> import entrypoints
>>> entrypoints.get_group_all('intake.drivers')
[EntryPoint('zarr', 'intake_xarray.xzarr', 'ZarrSource', None), ...]
```

The same approach is used by
[nbconvert](https://nbconvert.readthedocs.io/en/latest/) to discover plugins for
exporting Jupyter notebooks to other formats.

```python
setup(
    ...
    entry_points={
        "nbconvert.exporters" : [
            'custom=nbconvert.exporters:TemplateExporter',
            'html=nbconvert.exporters:HTMLExporter',
            'slides=nbconvert.exporters:SlidesExporter',
            'latex=nbconvert.exporters:LatexExporter',
            'pdf=nbconvert.exporters:PDFExporter',
            'markdown=nbconvert.exporters:MarkdownExporter',
            'python=nbconvert.exporters:PythonExporter',
            'rst=nbconvert.exporters:RSTExporter',
            'notebook=nbconvert.exporters:NotebookExporter',
            'asciidoc=nbconvert.exporters:ASCIIDocExporter',
            'script=nbconvert.exporters:ScriptExporter']
        }
    )
```

## Alternatives

### Package Naming Convention

In earlier releases, intake used a different approach for driver discovery. It
searched the set of all installed packages for ones whose names began with
``'intake_'``. It imported each one and searched its top-level namespace for
classes that inherited from a certain base class. This had several
disadvantages:

* Drivers had to be packaged in packages named ``intake_*`` to be discoverable.
  This excluded libraries that pre-dated intake from adding discoverable intake
  drivers.
* Drivers had to *subclass* an object from ``intake`` as opposed to duck-typing
  like one.
* The discovery process was slow because it required importing every package
  named ``intake_*`` order to search its contents for subclasses.

### Namespace Packages

A data export tool called
[suitcase](https://blueskyproject.io/suitcase) uses
[Python namespace packages](https://packaging.python.org/guides/packaging-namespace-packages/).
Each participating package is expected to define a namespace package
``suitcase.X`` (for some ``X``) and that package is expected to contain callable
objects with certain names and signatures. Like the naming convention approach,
this excludes pre-existing packages from participating in suitcase's plugin
mechanism.  Additionally, namespace packages are fragile: if any package fails
to implement namespace packaging correctly, it can break all the other installed
``suitcase.*`` packages.

## Name Collisions

What if two different protocols happen to use the same entrypoint name?
If package authors prefix their entrypoint with their package name, as in
``intake.drivers`` and ``nbconvert.exporters``, we'll avoid this problem.

There is also potential for name collisions within entrypoints. Suppose that in
addition to ``intake_xarray``'s zarr reader

{{< highlight python "hl_lines=5" >}}
setup(
    ...
    entry_points={
        'intake.drivers': [
            'zarr = intake_xarray.xzarr:ZarrSource',
            ...
            ]
        }
    )
{{< / highlight >}}

I have installed an alternative zarr reader

{{< highlight python "hl_lines=5" >}}
setup(
    ...
    entry_points={
        'intake.drivers': [
            'zarr = my_alternative_reader:ZarrSource',
            ...
            ]
        }
    )
{{< / highlight >}}

The function ``entrypoints.get_group_all('intake.drivers')`` returns a list with both
``Entrypoint``s. It's up to the library author to decide how what to do from
there. Intake resolves this with a configuration file and some command line
tools for reviewing the options and specifying priority.

## Where else should we use this?

Entrypoints are a good language feature for advertising objects in a library
that participate in a plugin mechanism. I have applied it to intake, and I
propose applying it to suitcase. There is also
[discussion](https://github.com/jupyter/notebook/issues/2894) about using in
more places in the Jupyter ecosystem. Let's keep an eye out for situations where
a custom entrypoint is the best tool for the job.

*Thanks to Min RK and Matthias Bussonnier for bringing this feature to my
attention in their review of
[intake#236](https://github.com/intake/intake/pull/236). Thanks also to Thomas
Kluyver for the excellent ``entrypoints``
library and to Martin Durant for his work on ``intake``.*
