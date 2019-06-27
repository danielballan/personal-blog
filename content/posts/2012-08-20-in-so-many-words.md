---
layout: post
title: In So Many Words
image: words-300x239.jpg
wordpress_id: 2052
wordpress_url: http://www.danallan.com/?p=2052
categories:
- projects
- computing
comments: true
tags:
- title: computational linguistics
  slug: computational-linguistics
  autoslug: computational-linguistics
- title: Gmail
  slug: gmail
  autoslug: gmail
- title: lexical analysis
  slug: lexical-analysis
  autoslug: lexical-analysis
---
In [a book chapter](http://norvig.com/ngrams/) from 2008, Peter Norvig cracked coded, historical German telegrams using a simple computer program. He included the program so you can try it yourself. On my computer, it cracked the code in less than a minute.

His program relies on a database of every English word, how often it is used, and how often it is found near any other word in context. Two researchers at Google derived [this database](http://www.ldc.upenn.edu/Catalog/CatalogEntry.jsp?catalogId=LDC2006T13) from the corpus of English on the public Web.

Inspired and curious, I made a similar database from all the email messages that I sent or received since 2007. What can be learned from a person's aggregated correspondence?

My emails contained 17,400,000 _tokens_ — words, misspellings, and one-off expressions like "aaargh" — drawn from a vocabulary of 265,000 distinct _types_. I discarded types that occurred less than five times, paring down the vocabulary to 62,000 common types.

The most common types are generic.

    the
    to
    a
    and
    i
    com
    http

But the most common _long_ types reveal more.

    rochester
    facebook
    delivery
    message
    university
    students
    physics
    baltimore
    subject
    hopkins

The database doesn't just count words; it remembers their order. So we can ask questions like, "What word usually follows 'ridiculously'?"

    ridiculously loud
    ridiculously cheap
    ridiculously awesome
    ridiculously ridiculous
    ridiculously hot

It's like Google auto-suggest, but completely derived from my writing and the writing of my email correspondents. Ridiculously ridiculous!

Another question: "Fill in 'love the ____'."

    love the zappos
    love the passion
    love the idea
    love the lamb
    love the pictures
    love the sideburns

The database knows, with confidence, how I use the word "swing" in context.

    swing dance    (394)
    swing dancing  (385)
    swing by       (149)
    swing in        (74)

## Under the hood.

Update: Downloading a copy of your Gmail messages is now [much easier](http://gmailblog.blogspot.com/2013/12/download-copy-of-your-gmail-and-google.html).

I downloaded my Gmail messages onto my local machine with ``getmail``. (I followed [these instructions](http://datalinkcontrol.net/dlc/content/gmail-backup-getmail).) A Python script extracted the body text from each email as a lowercase string. The script split the text into words with the blunt regular expression ``[a-z]+``. It inserted all of these words into one giant SQL table, identified by which email message they came from (``msg_id``) and their position in the message (``pos``)

SQL is a convenient language for the questions I asked. For example, it's easy to group occurrences of the same word and tally them.

    insert into Types (token, tally)
    select token, count(*) from Tokens
    group by token

To list the most common types, as I did above:

    select type
    from Types
    order by tally desc

    the
    to
    a
    and
    i
    com
    http

To restrict the search to longer words:

    select type
    from Types
    where length(type) &gt; 6
    order by tally desc

    rochester
    facebook
    delivery
    message
    university 
    students
    physics
    baltimore
    subject
    hopkins

For queries about words in context, I created the table ``Bigrams``, which takes the words from ``Tokens`` by pairs in sequence, groups recurrences, and tallies them.

    insert into Bigrams (type1, type2, tally)
    select a.token, b.token, count(*)
    from Tokens a join Tokens b
    where a.msg_id=b.msg_id
    and b.pos=1+a.pos
    group by a.token, b.token

Now I can ask, if Word 1 is "ridiculously," what is Word 2?

    select type1, type2
    from Bigrams
    where type1=&#039;ridiculously&#039;
    order by tally desc

    ridiculously loud
    ridiculously on
    ridiculously awesome
    ridiculously ridiculous
    ridiculously hot

With this large data set in hand, I might also try [topic detection](http://en.wikipedia.org/wiki/Latent_Dirichlet_allocation) (see this [cool application](http://blog.echen.me/2011/06/27/topic-modeling-the-sarah-palin-emails/)), though I doubt it would tell me anything that I don't already know. I could also use the date and time information in the emails, as Stephen Wolfram did when he [analyzed his own emailing habits](http://blog.stephenwolfram.com/2012/03/the-personal-analytics-of-my-life/). Combining that with lexical analysis would be cool, but I might need a few years' more data....

Thanks to [David Lu](http://www.probablydavid.com) and Jim, respectively, for the links.
