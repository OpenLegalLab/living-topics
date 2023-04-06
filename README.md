# Living Topics (Proto Alpha)

TL;DR: In this hackathon experiment, we examine data describing Swiss government functions, comparing results with Wikipedia and media sources. Some notebooks with initial set-up for machine learning, along with results of crawl, can be found in this repository.

See also:

- [Challenge page](https://hack.opendata.ch/project/946)
- [TERMDAT API](https://www.i14y.admin.ch/de/catalog/dataservices/ff0c37eb-2f7c-4ff6-996e-d22b77bf52fc)
- [Mediawiki API](https://www.mediawiki.org/wiki/API:Search)

## Hackathon journey

This code project is based on the "[Living Topics](https://hack.opendata.ch/project/946)" challenge, proposed at [#GovTechHack23](https://www.bk.admin.ch/govtech-hackathon) on March 23, 2023. Here is the gist of it:

> The goal of this challenge is to harness the expressivity and freshness of the terminologies provided by TermDat to create a high-quality map of what topics the Swiss Government is currently working on.

Looking at this problem statement, we first have to take a step back: what is the structure of the Swiss government, what is the scope of 'topics', where would you start - in other words, what would be the high-level 1:1000000 map of the administrations?

![](https://prod-swishop-s3.s3.eu-central-1.amazonaws.com/styles/swt_9_2_1200x267/s3/2023-01/header-lk1000.png)
_1:1 Million [Map of Switzerland](https://shop.swisstopo.admin.ch/en/maps/national-maps/national-map-million) (swisstopo shop)_

After some discussion, we came up with a slightly more accessible version of the Living Topics challenge: instead of bottom up - at the current topic levels as originally stated - let us begin at the top level of government, obtain definitions of the functions and responsibilities of government departments. The more detail we have, the better we would be able to classify a topic as belonging to one or another office. From here, step by step we would be able to identify specific current affairs.

![](https://www.ch-info.swiss/img/containers/1-img/buku_2020_de_44-45-organigramm.jpg/81daf884ace3f577a6118a83a5644515.jpg) _Organigram from the [2020 edition](https://www.ch-info.swiss/edition-2020/bundesverwaltung/bundesverwaltung), see also [2023 update](https://www.ch-info.swiss/edition-2023/die-bundesverwaltung/organigramm)._

We begin at the top. Helpfully, the Federal Chancellery produces an illustrated [guide to the political and administrative system](https://www.ch-info.swiss/edition-2023/edition-2023/deckblatt-ausgabe-2023) (ch-info.swiss) in Switzerland, available in print, online and in an app. This gives a brief overview to the departments, with some detail of their function. We could unfortunately not find the source code or any way to bulk-download from this website. We keep searching.

![](https://i.imgur.com/r3YmGl8.jpg)
_[172.010.1 Government and Administrative Organization Ordinance](https://www.fedlex.admin.ch/eli/cc/1999/170/de#annex_1/lvl_u1)_

The [FEDLEX](https://www.fedlex.admin.ch/) service provides us the legal documents that serve as the mandated basis for the administrations. We find the interface clumsy, and the document layouts not machine-readable. Even when we export the XML version, we get impractical HTML tables inside. A better way to access it is through the Linked Data service:

![Screenshot from 2023-04-06 22-38-32](https://user-images.githubusercontent.com/31819/230489263-1b617d49-db51-40db-a7bc-4c4caf257f1d.png)
_[Screenshot of LINDAS term browser](https://ld.admin.ch/dimension/office)_

Our discussion further leads us to explore the [State Calendar](https://staatskalender.admin.ch/) as an alternative source of hierarchical structure, which leads us to quickly updating a long overdue [public bodies](https://github.com/OpendataCH/public_bodies_of_the_swiss_federation/issues/1) open data source.

What does 'the Internet' have to say about all this?

![](https://i.imgur.com/D2u4cQq.png)
_Screenshot of ChatGPT by OpenAI._

Hmm, wonder where 'the Internet' gets this data from...?

![Wikipedia](https://i.imgur.com/f0bwVOK.jpg) _Screenshot of four language editions (EN-IT-FR-DE) of a [Wikipedia article](https://en.wikipedia.org/wiki/Federal_administration_of_Switzerland)._

The Wikipedia page [Federal administration of Switzerland](https://en.wikipedia.org/wiki/Federal_administration_of_Switzerland) provides a similar overview. We found that the very complete content in the German edition to be somewhat out of date, the English language nearly as complete, the French significantly shorter, and Italian practically empty. Using the [Mediawiki API](https://www.mediawiki.org/wiki/API:Search) - also via handy [Python wrapper](https://github.com/goldsmith/Wikipedia) - it is possible to quickly get the contents of Wikipedia pages. And in an [Edit-a-thon](https://en.wikipedia.org/wiki/Wikipedia:How_to_run_an_edit-a-thon), we could update them and improve the translations.


![](https://i.imgur.com/NI3wK0Z.jpg)
_Screenshot of successive [Linguee.com](https://www.linguee.com/) searches._

What else could we try? A series of searches on [Linguee](https://www.linguee.com/) (a dictionary service that is part of DeepL) provided some clues about various government websites and media repositories describing responsibilites of the federal, cantonal and municipal government. 

![](https://i.imgur.com/GSF4jb6.png)
_Screenshot of [Nicht Sache der Kantone](https://www.nzz.ch/nicht_sache_der_kantone-ld.926167?reduced=true) (NZZ 2009)._

Finally, we explore the media landscape. At other hackathons like the recent [Rethink Journalism](https://opendata.ch/events/rejoha22/) event, we had a chance to work with press databases - some of which would be excellent resources to understand expectations and questions about the function of government from the outside in. We leave this avenue for a future foray, though we trust that the web services of the Confederation would be the best starting point. 

Which brings us to the point of departure of the hackathon - the [I14Y Interoperability Platform](https://www.i14y.admin.ch/de/catalog/all?publisher=e76faf06-72d0-4ac0-ae1b-5d0db67041a5&statuses=Recorded&access_right=PUBLIC). We decide to use the API of TERMDAT to in sequence understand the main levels and units of government, though all three of the available endpoints, like [News Service API](https://www.i14y.admin.ch/de/catalog/dataservices/52b7f97d-df95-45d2-8533-d2a2fa43641a), are interesting:

![](https://i.imgur.com/ZVOSl1M.jpg)
_Screenshot of [I14Y Interoperability Platform](https://www.i14y.admin.ch/)_

Continuing with the questions we explored above, we first explore the relatively straightforward web interface, punching in some test searches, that seemed to give promising even if limited results:

![](https://i.imgur.com/gL2oTbL.jpg)
_Screenshot of [TERMDAT](https://www.termdat.ch/search)_

It becomes clear that we would need to be very precise, and correct, in our queries. First, we create a simple folder structure: `bund` (Federal), `kantone` (Cantonal) and `gemeinde` (Municipal) for the three levels of government. Then `bk`, `uvek`, `edi` ... for the main government departments. In these folders we can put text files (`termdat.txt`, `wikipedia.txt`, ..) that help us to create a classifier for topics related to these departments. 

![](https://i.imgur.com/jLWeNnz.png)

We write a simple aggregator to repeatedly query the [TERMDAT API](https://api.termdat.ch/swagger/index.html) and save the descriptions (or any available notes) about the departments into these folders. One of the issues we experienced were minor inconsistencies in the data schema (missing `description` fields), which our code works around.

![](https://bucketeer-036aa605-c047-4623-8610-f1764b90cf98.s3.amazonaws.com/public/163/QCEKJ08Q6O3VHDOT2IZYP46V/Screenshot_from_20230324_142849.jpg)
_Screenshot of API docs, Jupyter notebook, search results._

At this point, we look into the question of how to best classify these texts. Using a Sentence Similarity model like [gBERT-large-sts-v2](https://huggingface.co/aari1995/German_Semantic_STS_V2), which has a fine-tuned version by [Deutsche Telekom](https://huggingface.co/deutsche-telekom/gbert-large-paraphrase-euclidean), we can utilise a cloud-based API - or run our own inference service to work out the appropriate department. We have some initial code, but could not get results until a few hours after the deadline. 

![](https://i.imgur.com/eWzUuBD.png)
_Screenshot of [sentence-transformers](https://github.com/we-art-o-nauts/living-topics/blob/main/sentence-transformers.ipynb) notebook_

We are motivated to continue on this idea, and would be happy to hear feedback & suggestions via [GitHub Discussions](https://github.com/we-art-o-nauts/living-topics/discussions).

## License

MIT
