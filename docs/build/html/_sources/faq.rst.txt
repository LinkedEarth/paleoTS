.. _faq:

Frequently asked questions
==========================

1. Do I need to use Pyleoclim with PaleoTS? Can I use other toolboxes?

The short answer to this is yes. You can use any toolboxes and in any languages that your heart desire and write the component code. However, there are two caveats to take into consideration:

* You may need to create and store a Docker container for that specific library if you are planning to use our servers. Otherwise you just need to ensure that the library is available on your server along WINGS.

* The data output need to be of similar type as what is needed by the abstract workflow (in most cases a JSON file). If you are planning to replace only certain components in workflow, make sure that the properties in the JSON file are filled out appropriately. 
