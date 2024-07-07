---
layout: post
title: 'Considering Some New APIs.json Types'
image: https://apisjson.org/images/types.png
---
I am evaluating all of the enums for APIs.json before I plan for the next version. One of the enumerators that haven’t been updated in a while, but has some interesting changes on the table is the type property. To date the APIs.json type property has the following three values.

- **Index** - The index of an API, you decide the scope.
- **Template** - A template of an API you can reuse.
- **Example** - Just an example API for demonstration.

However, with recent work on APIs.io and API Commons I am considering adding the following values to the list of enumerators, adding to the different types of APIs you can describe with APIs.json.

- **Blueprint** - A blueprint of APIs.json for an API producer.
- **Contract** - A contract governing the operation of API.
- **Network** - A network of many APIs within a single domain.
- **Search** - Multiple APIs included in a single search node.

I am just adding these as an issue. I haven’t locked them in yet. I haven’t added to any of the APIs I’ve published recently. I want to do more exploration and soul searching. Why do I need them? I will be filtering automation and the application of rules based upon these types, but what else will they be doing? And are there other ways we can slice and dice an APIs.json definition to accomplish the same thing? We will see.

