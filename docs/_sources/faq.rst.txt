.. _faq:

Frequently asked questions
==========================

1. Do I need to use Pyleoclim with PaleoTS? Can I use other toolboxes?

The short answer to this is yes. You can use any toolboxes and in any languages that your heart desires and write the component code. However, there are two caveats to take into consideration:

* You may need to create and store a Docker container for that specific library if you are planning to use our servers. Otherwise you just need to ensure that the library is available on your server along WINGS.

* The data output need to be of similar type as what is needed by the abstract workflow (in most cases a JSON file). If you are planning to replace only certain components in workflow, make sure that the properties in the JSON file are filled out appropriately.

You can learn more about creating your own components :ref:`here <Creating new components>`.

2. Do I need to use Docker containers?

If you are planning to use PaleoTS through our server, you do. If you are `installing your own version on your servers <installing>`, you can make sure that all the packages you need are also on the server. You may need to rewrite existing code to work with packages installed on a server.

3. Can I work offline?

When using our server, not at the moment. You can be offline while the runs execute but you will need an internet connection to interact with PaleoTS. If installing on your own machine, you may need an internet connection when pulling Docker containers.
