---
layout: post
date: 2012-11-28
title: Turkey Time
excerpt: Estimating turkey cooking times with science.
image: 2012-11-24-20.20.54.jpg
wordpress_id: 2785
wordpress_url: http://www.danallan.com/?p=2785
categories:
- notes
comments: true
tags: []
---
Ways to estimate turkey cooking times:

* USDA guidelines
* the simple rule "18 minutes per pound"
* $$\text{time} = \frac{\text{weight}^{2/3}}{1.5}$$ (using weight in pounds)

The "18 minutes" rule works for some weights, but it doesn't scale right for large turkeys. A wider range of accuracy is achieved by the simple formula, [suggested](http://www.symmetrymagazine.org/breaking/2008/11/26/the-panofsky-turkey-constant) by the late physicist and SLAC director [Pief Panofsky](http://en.wikipedia.org/wiki/Wolfgang_K._H._Panofsky). All of these assume the oven is set to 325 F.

<embed class="svg-image" src="{% asset_path turkey-comparison-of-methods.svg %}" style="display: block; margin: auto; margin-top: 1em; margin-bottom: 1em;" />

The exponent in Panofsky's formula comes from the ratio of the turkey's surface area, through which heat flows, to its volume. The 1.5 is empirical, fitting the mathematical curve to data from actual cooked turkeys.

![Just spraying a turkey is all.]({% asset_path spraying-turkey.jpg %})

With a little more trouble, we can solve the problem without referring to actual cooking times, using only the basic material properties of turkey. We can use our solution to estimate cooking times at other temperatures, such as smoking a turkey on a 225 F grill.

What if we imagine that the turkey is a round ball of cold meat sitting in hot air? Simplifying its shape and ignoring the details of the cooking process, we have a straightforward physics problem. The properties we need (density $$\rho$$, conductivity $$\kappa$$, and diffusivity $$\alpha$$) were measured and [published](http://www.nt.ntnu.no/users/skoge/prost/proceedings/aiche-2005/topical/pdffiles/T9/papers/554a.pdf) by the Canadian Food Research and Development Center.

How big should this imagined ball of turkey be? We could try mashing the turkey's whole mass into one solid ball. But since that approach ignores the bones, which conduct heat faster than meat, we should expect it to overestimate the cooking time. (And it does.) Instead, we can try including only the meat, which comprises roughly half the mass. For a 6- to 22-pound turkey, we'll be modeling a 13- to 21-cm meat ball. In comparison to a turkey breast, the thickest part of the meat, that seems about right.

Our turkey ball will start at 50 F, surrounded by 325 F air in the oven. I will solve the heat equation to compute when the center of the ball reaches 170 F, safe to eat.

<embed src="{% asset_path turkey-methods-with-heat-equation.svg %}" width="80%" style="display: block; margin: auto; margin-top: 1em; margin-bottom: 1em;" />

A fine fit like that seems too good to be true. Perhaps our approximations balanced each other by chance. Now, extend the model to learn something new: If we set the surrounding air to 225 F, as on charcoal grill, the equation predicts longer cooking times that agree with experience.

<embed src="{% asset_path turkey-oven-vs-grill.svg %}" width="80%" style="display: block; margin: auto; margin-top: 1em; margin-bottom: 1em;" />

The real physics of turkey cooking is explained in a nonmathematical post by [Modernist Cuisine](http://modernistcuisine.com/2012/11/turkey-tips/).

## Mathematical Appendix

Parameters:

* raw turkey temperature $$T_{\text{raw}} = 50 \text{ F}$$
* oven temperature $$T_{\text{oven}} = 325 \text{ F}$$
* thermal diffusivity $$\alpha = 1.4\times10^{-7} \text{ m}^2\text{/s}$$
* thermal conductivity $$\kappa = 0.45 \text{ W/mK}$$
* heat transfer coefficient of free air $$h = 10 \text{ W/m}^2\text{s}$$
* density $$\rho = 1070 \text{ Kg/m}^3$$

The temperature at the center of the turkey ball after time $$t$$ in the oven measured a distance $$r$$ from the center is given by

$$T(t,r / R) = T_{\text{oven}}\ -\ (T_{\text{oven}}-T_{\text{raw}})\displaystyle\sum\limits_{n=1}^\infty \frac{4(\sin\zeta_n - \zeta_n \cos \zeta_n)}{2 \zeta_n - sin(2 \zeta_n)}\frac{\sin(\zeta_n r/R)}{\zeta_n r/R}e^{-\zeta_n^2 \alpha t/R^2} $$

where $$\zeta_n$$ are given by the roots of the equation $$f(x) = 1 - \zeta \cot(\zeta) - \frac{h R}{\kappa}$$ and must be computed numerically.

We are mainly interested in the temperature at the center, the last part to cook. This is a slightly simpler expression.

$$T(t, 0) = T_{\text{oven}}\ -\ (T_{\text{oven}}-T_{\text{raw}})\displaystyle\sum\limits_{n=1}^\infty \frac{4(\sin\zeta_n - \zeta_n \cos \zeta_n)}{2 \zeta_n - sin(2 \zeta_n)}e^{-\zeta_n^2 \alpha t/R^2} $$

When $$T(t, 0) = 170 \text{ F}$$, the turkey is done.
