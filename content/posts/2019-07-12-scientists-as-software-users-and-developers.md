---
title: Scientists as Software Users and Developers
date: 2019-07-12
draft: true
---

The scientific Python ecosystem is built by and for people who fall along a
continuum between _software user_ and _software developer_, and this motivates
technology choices.

In many industries, software developers and users are clustered into distinct
roles, producer and consumer. The developer's mandate is to provide an
end-product that meets the users' needs. Software in science is different: the
roles are more smoothed out. At the extremes, there are scientists who use
software as is, never needing to open the hood or form a clear mental model of
how it works internally, and there are Research Software Engineers who spend
100% of their time writing code for scientific applications.  But there are many
scientists situated along a continuum between these two.

The choice of technologies reflects that continuum. In many industries, a
developer writing a web application might choose a popular backend framework
like Flask or Django and a popular frontend like React or Vue. There is a large
community behind those projects, and it is comparatively easy to hire developers
who can work on them.

Within the SciPy community, a scientist/developer might choose to implement
their web application as a Jupyter notebook rendered as a web application using
Voila. This might strike an outsider to that community as an odd choice, as it
adds some layers of complexity and relies on tools that are, in the wider world,
less established. Why do scientists do this?

An often-invoked applause line at the SciPy conference is, "And you can have
this web app without writing any JavaScript!" Among scientists, Python and C++
are much more common competencies than JavaScript, and there are several
frameworks designed to enable scientists to generate front-end code from Python
([Bokeh](https://bokeh.pydata.org/en/latest/),
[Plotly.py](https://plot.ly/python/),
[ipywidgets](https://ipywidgets.readthedocs.io/en/latest/)) or C++
([xwidgets](https://xwidgets.readthedocs.io/en/latest/)).
They empower scientists to build or modify the tools they need by reapplying a
skill they might already have, or feel motivated to learn, without obtaining a
competency in web development.

The same tool may be picked up by a scientist who never looks under the hood of
the software they use; by another scientists who enjoys writing detector drivers
in C on the weekend; and by a graduate student who starts at one extreme and
evolves over time toward the other. These tools can satisfy the needs of all
those scientists&mdash;with the same codebase.
