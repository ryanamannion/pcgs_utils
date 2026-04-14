API Reference
=============

Authenticated Client (api.pcgs.com)
------------------------------------

The :class:`~pcgs_api.client.PCGSClient` wraps the official PCGS Public API at
``https://api.pcgs.com/publicapi``.  An API key is required — pass it as
``api_key`` or set the ``PCGS_ACCESS_TOKEN`` environment variable.

.. autoclass:: pcgs_api.client.PCGSClient
   :members:
   :member-order: bysource
   :special-members: __init__

.. autoexception:: pcgs_api.client.RateLimitExceeded

SpecSearch Client (collectorsuniverse.com)
------------------------------------------

The :class:`~pcgs_api.spec_search.SpecSearchClient` wraps the internal
autocomplete search endpoint on ``www.collectorsuniverse.com``.  No API key is
required.

.. autoclass:: pcgs_api.spec_search.SpecSearchClient
   :members:
   :member-order: bysource
   :special-members: __init__

.. autoclass:: pcgs_api.spec_search.SearchType
   :members:
   :undoc-members:

Schema — SpecSearch Results
----------------------------

.. autoclass:: pcgs_api.spec_search.PCGSCoinResult
   :members:

.. autoclass:: pcgs_api.spec_search.PCGSWorldCoinResult
   :members:

.. autoclass:: pcgs_api.spec_search.PSACardResult
   :members:

Schema — Coins
--------------

.. autoclass:: pcgs_api.schema.coin.CoinFacts
   :members:

.. autoclass:: pcgs_api.schema.coin.CoinFactsImage
   :members:

.. autoclass:: pcgs_api.schema.coin.AuctionItem
   :members:

.. autoclass:: pcgs_api.schema.coin.AuctionResponse
   :members:

.. autoclass:: pcgs_api.schema.coin.AuctionListResponse
   :members:

.. autoclass:: pcgs_api.schema.coin.ImageDetail
   :members:

.. autoclass:: pcgs_api.schema.coin.CoinImagesResponse
   :members:

Schema — Banknotes
------------------

.. autoclass:: pcgs_api.schema.banknote.Banknote
   :members:

.. autoclass:: pcgs_api.schema.banknote.BanknoteResponse
   :members:

.. autoclass:: pcgs_api.schema.banknote.BanknotesResponse
   :members:

.. autoclass:: pcgs_api.schema.banknote.BanknoteImagesResponse
   :members:

Schema — Orders
---------------

.. autoclass:: pcgs_api.schema.order.OrdersResponse
   :members:

.. autoclass:: pcgs_api.schema.order.OrderDetail
   :members:

.. autoclass:: pcgs_api.schema.order.GradingOrderLine
   :members:

Schema — Images
---------------

.. autoclass:: pcgs_api.schema.image.Image
   :members:

.. autoclass:: pcgs_api.schema.image.ImageSummary
   :members:
