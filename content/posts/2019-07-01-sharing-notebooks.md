---
title: Sharing Jupyter Notebooks
date: 2019-07-02
draft: true
---

"Who is my audience?" is a good question to begin with. We could refine that to,
"How far will this code go? How many people will use it? And for how long will
they rely on it to work?" 

For example, if you are the only user and you only need the code for a day, you might use the
notebook document as a messy scratch pad with out-of-order execution and no
clear record of the software dependencies (what libraries, what versions, etc.).
But if the notebook is meant to be used for a long time by many people, you might
clean up the code a bit, ensure it executes top-to-button,
[move any large code chunks out of the notebook and into traditional Python modules](https://nsls-ii.github.io/scientific-python-cookiecutter/),
put the notebook in version control using
[nbdime](https://nbdime.readthedocs.io/en/latest/),
and specify the software-dependencies in a
[Binder](https://mybinder.readthedocs.io/en/latest/)-compatible repository.
The appropriate level of effort and ceremony depends on how far the code will go.
We can vizualize the space of how "far" code goes in space (people) and in time.

![phase space of how far code goes](/static/images/how-far-phase-space.svg)

[A recent talk on this question](https://www.youtube.com/watch?v=PcJeHNWOoWk)
asked the audience to answer for themselves at what point in this space they add
software best practices like version control, an issue tracker, tests, continuous
integration, a README, API documentation, usage examples, and so on. Where in
this space are those tools worth the trouble?

Considering sharing Jupyter notebooks in particular, we could further ask, how
much effort does the *sender* invest to share it and how much effort does the
*recipient* invest to get it working for them?

![phase space of how far code goes](/static/images/effort-status-quo.svg)

The most obvious way for beginners to send and receive notebooks is to
email them. Consider where that fits in this space. If the recipient happens to
have all the right libraries and other resources already available, this might
*just work™*. But more often the recipient needs to sort out the right
environment to run the notebook in. In this sense, sharing notebooks on
[nbviewer](nbviewer.org) fits in about the same space&mdash; one gets a better
user experience in exchange for learning about nbviewer, but the notebook does
not encode anything about the environment it should be run in. To provide the
recipient with this information, the sender can provide a
[Reproducible Execution Environment Specification](https://repo2docker.readthedocs.io/en/latest/specification.html) (REES),
which may be as simple as a ``requirements.txt`` file or as custom as a
``Dockerfile``. It is a significant step up in effort or expertise required from
the sender.

What new tools can we imagine filling this space? Some quetsions to consider:

* Are the sender and recipient on the same JupyterHub?
* Is the notebook being "published" for long-term reuse by many people (the
  nbviewer use case) or quickly transferred between a small number of people
  for short-term collaboration (the email use case)?
* Is the unit being shared one notebook or a set of notebooks and associated
  data files?
* Does the notebook have specific or specialized resource requirements?

For low-effort sharing between two users on the same JupyterHub, I propose
[JupyterHub Share Link](https://github.com/danielballan/jupyterhub-share-link),
which provides functionality similar to Google Docs'
"Anyone with link can read (and make a copy)." By assuming that the users are
on the same Hub and that the sharing is short-term, the tool can automatically
open the recipient's notebook in the right environment. See link for details.

![JupyterHub Share Link Demo GIF](https://github.com/danielballan/jupyterhub-share-link/raw/master/demo.gif?raw=true)

For sharing that is longer-term or between Hubs, we need a more explicit list of
requirements from the sender. How can move that to the left on our diagram? We
can look for ways for make it easier for the sender to define a REES by adding a
UI and other tooling.

As an aside, it is tempting to aim for a tool that can detect all the software
dependencies automatically with no effort by the sender. My personal view is
that fully automating this is not worthwhile because the result will always be
brittle. Maybe a tool that can that can provide a *guess* as a starting point to
be reviewed and refined by the sender could be viable.

We can also make the tools behind Binder applicable in other contexts. For
example, we could imagine:

* a JupyterHub Service that builds a container from a REES without requiring Kubernetes
* an alternate builder that turns a REES into conda environment, for the subset
  of REES where this is possible (i.e. no ``Dockerfile`` support of course)
* a gallery of REES containers published by other users with options to spawn
  in a container that mounts the user's local storage

We intend to prototype these ideas in
[Jupyter REES Service](https://github.com/danielballan/jupyter-rees-service).
