---
layout: post
title: 'Pushing APIs.json V0.19'
image: https://apisjson.org/images/types.png
---
We have accumulated a number of additions to the spec lately based upon work on APIs.io APIs, but also profiling new APIs. You can find a list of all [the new features on Github as issues for v0.19](https://github.com/apis-json/api-json/issues?q=is%3Aissue+is%3Aclosed+label%3A0.19).

The most notable additions at the top level were:

- **Position** - Establishing the position of the APIs.json maintainer. (Producer / Consumer)
- **Access** - Defining what access levels exist for all APIs in APIs.json (Internal, 1st-Party, 3rd-Party)

Add the API level we added:

- **Created** - Extending created date to the API.
- **Modified** - Extending modified date to the API.

Then we added two things to properties:

- **Property Description** - The ability to add descriptions.
- **Property Tags** - The ability to tag with key words.

Then we added the following property types:

- ALPS
- JSON-LD
- Vocabulary
- Use Cases
- Plans
- JSON Forms
- Arazzo
- Compare
- RunInInsomnia
- API Evolution Property
- Data Contract
- Serverless Workflow
- Bruno Collection

After that there was some language added to allow for authoritative APIs.json as long as the URL for a GitHub profile matches the APIs Base URL. Probably not the most secure, but easily verified, and we are just determining simple ownership.

We have added [a v0.20 label and already adding new features to be considered](https://github.com/apis-json/api-json/labels/0.20), rapidly moving to support new features APIs.io, and other implementations. The goal is to get the spec reflecting the search index and something that can power reporting, analytics, and other interesting API discovery approaches.