---
layout: post
title: Olympics in Boulder
image: swimmer.jpg
wordpress_id: 1859
wordpress_url: http://www.danallan.com/?p=1859
categories: projects science-demos
comments: true
tags: []
---
On the last day [Boulder School for Condensed Matter Physics](http://boulder.research.yale.edu/Boulder-2012/index.html), a month-long program for young researchers, we formed teams for competitions. Here's one of our entries in Physics Charades: "a swimmer at low Reynolds number."

![a swimmer at low Reynolds number]({% asset_path swimmer.jpg %})

Next, we erupted Diet Coke with Mentos, competing to make the highest fountain. A paper in the _American Journal of Physics_ found that [there are many important factors]({% asset_path Coffey-Diet-Coke-and-Mentos-What-is-really-behind-this-physical-reaction-2008.pdf %}). For us, the key tricks were warming the soda beforehand and forcing the geyser through a small hole. We won that challenge handily.

![our geyser]({% asset_path mentos1.jpg %})

Finally, each team invented a competition for the others. These are the rules of our invention, written for fellow physicists.

## Our challenge: Human Spin Glass

Sixteen team members stand in a 4x4 array. Each person may stand ("spin up") or sit ("spin down") at will.

![human spin glass]({% asset_path spin_glass.jpg %})

We will give each person a card with four small integers. These represent "couplings" to neighbors in the array. For example, a +2 at the top of the card means that if I am in the same state the person in front of me, I earn 2 points for my team. I lose 2 points if we are in different states. Likewise, a -1 on the right of the card means I earn 1 point if I'm in the opposite state from the neighbor to my right, and I lose 1 point if we are the same.

The system will be frustrated. Your challenge is to react to your neighbors in a way that optimizes your score, prioritizing couplings that offer the most points. You will have 30 seconds to "fluctuate" between sitting and standing and to "anneal" into a low-energy (high-scoring) state. When the time is up, each person will compute and report their score. Your aim is to maximize the team's score.

We'll assume periodic boundary conditions, so people on the edges must peer down the line. In other words, the sign convention is: 

$$ H = - \sum\limits_{\langle ij\rangle} J_{ij}\ S_i \cdot S_j \\ \text{Score} = -H $$ 

 ...so a more positive score is a better score.

## Appendix: Simulation and Experiment

If each person acts simply to maximize their personal score, with no oversight or communication, this game is well modeled by a [Metropolis algorithm](http://en.wikipedia.org/wiki/Metropolis%E2%80%93Hastings_algorithm) at zero temperature. With a simple simulation, I learned that this process usually finds the ground state (highest possible score). It only takes about 10–20 moves, depending on the couplings.

I worried that the game would be too easy, that each team would find the ground state and tie. But, in reality, the crowd is confusing enough to be challenging, even with only 16 players. Notably, players optimized bonds along rows much better than they optimized bonds along columns. Conversations are easier along rows.
