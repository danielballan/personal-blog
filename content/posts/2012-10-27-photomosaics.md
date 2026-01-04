---
layout: post
date: 2012-10-27
title: Photomosaics
summary: Demonstrating open source software for generating irregular photomosaics
image: matt-kilroy.jpg
wordpress_id: 2553
wordpress_url: http://www.danallan.com/?p=2553
comments: true
tags:
- photomosaic
---
![](/static/images/neil-armstrong.jpg)
I wrote a program that builds photomosaics.

I was impressed by a magazine cover by [Charis Tsevis](http://www.flickr.com/photos/tsevis/), an artist in Athens who specializes in these. Tsevis uses a combination of professional software and custom scripts, and his mosaics are subtler than regular photomosaics. He mixes tiles of different sizes, using smaller tiles to capture the detail of a face or to trace along a curved edge. In [some mosaics](http://www.flickr.com/photos/tsevis/7985477322/in/set-72157622661792616), he spaces tiles irregularly, evoking an unfinished jigsaw puzzle. He adapts the color palette of his subject to the colors in his collection of tiles. I wrote a script (in Python and SQL) that builds mosiacs in the same style, mining collections of 2000–10,000 pictures. Tsevis's high-quality work is probably impossible to automate, but I can make passable imitations.

I assembled the photo of Neil Armstrong from NASA's [Astronomy Picture of the Day](http://apod.nasa.gov/apod/) archives. Here is the original photo with three styles of photomosaic from my script: traditional regular tiles, multi-scale tiles, and irregularly spaced tiles.

{:.gallery}
![]](/static/images/neil-armstrong-original1.jpg)
![]](/static/images/neil-regular.jpg)
![]](/static/images/neil-armstrong.jpg)
![]](/static/images/neil-irregular1.jpg)


The [Library of Congress](http://www.loc.gov/pictures/) is another good source for free images in bulk. Below: Ella Fitzgerald from vintage performing arts posters and Baltimore Oriole Matt Kilroy (1866-1940) from baseball cards of his time.

![Ella Fitzgerald](/static/images/ella-fitzgerald.jpg)
![Matt Kilroy](/static/images/matt-kilroy.jpg)

My script is in an open-source [GitHub repository](https://github.com/danielballan/photomosaic/), on which page you can read more about how it actually works. Probably the most interesting section for a quick read is [how matching images are chosen](https://github.com/danielballan/photomosaic/#tile-matching-and-repetition).

Incidentally, the original computer-generated photomosaic was invented in 1993 by Joseph Francis, who still works on digital art and [writes about it](http://www.digitalartform.com/). If you want to make some mosaics but you don't want to mess around with my Python script, install [AndreaMosaic](http://www.andreaplanet.com/andreamosaic/download/) for Windows and Mac. It doesn't have these Tsevis-inspired features (yet, anyway) but it makes good regular mosaics.
