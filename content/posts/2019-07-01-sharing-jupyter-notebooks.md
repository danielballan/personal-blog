---
title: Sharing Jupyter Notebooks
summary: A survey of approaches for sharing Jupyter notebooks
date: 2019-07-03
---

How can we expand and improve the tools for sharing Jupyter notebooks?

"Who is my audience?" is a good question to begin with. Sometimes we want to
share notebooks within teams, and sometimes we want to publish them to the world.
If you are the sole user and you only need the code for a day, you
might use a Jupyter notebook as a messy scratch pad, executing cells out of
order and not bothering to leave a record of the software dependencies (what
libraries, what versions, etc.).  But if the notebook is meant to be used for a
long time by many people, you might clean up the code a bit, ensure the cells
execute top-to-bottom,
[move any large code chunks out of the notebook and into traditional Python modules](https://nsls-ii.github.io/scientific-python-cookiecutter/),
put the notebook in version control using
[nbdime](https://nbdime.readthedocs.io/en/latest/),
and specify the software-dependencies in a
[Binder](https://mybinder.readthedocs.io/en/latest/)-compatible repository.
The appropriate level of effort and ceremony depends on how far the code will go.
We can visualize the space of how "far" code goes in space (people) and in time.

![phase space of how far code goes](/static/images/how-far-phase-space.svg)

[A recent talk on this question](https://www.youtube.com/watch?v=PcJeHNWOoWk)
asked the audience to answer for themselves where in this space they impose
version control, an issue tracker like GitHub, tests, continuous
integration, a README, API documentation, usage examples, and so on. Where in
this space does the benefit justify the effort?

Considering sharing Jupyter notebooks in particular, we could further ask, how
much effort does the *sender* invest to share it and how much effort does the
*recipient* invest to get that notebook working for them?

![current tools placed in the space of sender and recipient effort](/static/images/effort-status-quo.svg)

The most obvious way for beginners to send and receive notebooks is to
email them. Consider where that fits in this space. If the recipient happens to
have all the right libraries and other resources already available, this might
*just work™*. But more often the recipient needs to sort out the right
environment to run the notebook in. In this sense, sharing notebooks on
[nbviewer](nbviewer.org) or
[bookstore](https://bookstore.readthedocs.io/en/latest/) or my own
[nbexamples](http://github.com/danielballan/nbexamples)
lands in about the same place as email&mdash; one gets
a better user experience in exchange for learning about a more specific tool,
but the notebook still does not encode anything about the environment it should
be run in.

[Binder](https://mybinder.readthedocs.io/en/latest/) enables senders to
share a custom computing environment, bundling up multiple notebooks,
associated support files, and specified software requirements. With one click,
recipients are dropped into a Jupyter server with some free computational
resources and temporary storage, and they can start working immediately.
With the new
[Voilà](https://blog.jupyter.org/and-voil%C3%A0-f6a2c08a4a93), nontechnical users
can be directed to a standardalone web application / dashboard built from a
notebook. [PyViz Panel](http://panel.pyviz.org/) is doing interesting work in
in an overlapping space, capturing software dependencies, tests, and more, and
presenting recipients with a static or interactive view.

Enabling this requires the sender to write down what their requirements are, which may be
as simple as a ``requirements.txt`` file or as custom as a ``Dockerfile``. The
Binder team calls this a [Reproducible Execution Environment Specification](https://repo2docker.readthedocs.io/en/latest/specification.html)
(REES). Composing a REES is a modest but significant step up in effort or
expertise required from the sender in exchange for a stronger guarantee that
the recipient will be able to run the notebook without a lot of trial and error.

What regions in the space of sender and recipient effort and "how far code goes"
are important? How else can we extend or recombine the components of Jupyter to
create well-matched solutions?

Some questions to consider:

* Are the sender and recipient on the same JupyterHub?
* Is the notebook being "published" for long-term reuse by many people (the
  Binder use case) or quickly transferred between a small number of people
  for short-term collaboration (the email use case)?
* Is the unit being shared just *one* notebook or a collection of notebooks? Are
  there additional files necessary to run them?
* Does the notebook have specific or specialized resource requirements?

For low-effort, short-term sharing between two users on the same JupyterHub, we
have prototyped
[danielballan/jupyterhub-share-link](https://github.com/danielballan/jupyterhub-share-link),
which provides functionality similar to Google Docs' feature:
"Anyone with link can read" (and make a copy). By assuming that the users are
on the same Hub and that the sharing is short-term, the tool can automatically
open the recipient's notebook in the right environment. See link for details.

![JupyterHub Share Link Demo GIF](https://github.com/danielballan/jupyterhub-share-link/raw/master/demo.gif?raw=true)

For sharing that is longer-term or between users who are not logged into the same
Hub, we need a more explicit list of requirements from the sender to enable the
recipient to reconstruct a working environment. Currently, the best option there
is to define a REES. That could potentially be made easier by adding UI or other
tooling.

![new ideas placed in the space of sender and recipient effort](/static/images/effort-new-ideas.svg)

We can also make the tools behind Binder directly applicable in more contexts.
For example, we could imagine:

* a JupyterHub Service that builds a container from a REES without requiring Kubernetes
* an alternate builder that builds a conda environment instead of a container,
  for the subset of REES where this is possible (i.e. no ``Dockerfile`` support
  of course)
* a gallery of REES containers published by other users with options to spawn
  in a container that mounts the recipient's local storage to provide
  persistence

We plan to prototype these ideas in the repository
[danielballan/jupyter-rees-service](https://github.com/danielballan/jupyter-rees-service).

These ideas grew out of conversations at the
[Jupyter Community Workshop for Scientific User Facilities and HPC](https://blog.jupyter.org/jupyter-community-workshop-jupyter-for-scientific-user-facilities-and-high-performance-computing-3afa4a990086).
