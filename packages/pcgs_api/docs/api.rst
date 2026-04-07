API Reference
=============

Client
------

.. autoclass:: pcgs_api.client.PCGSClient
   :members:
   :member-order: bysource
   :special-members: __init__

.. autoexception:: pcgs_api.client.RateLimitExceeded

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
