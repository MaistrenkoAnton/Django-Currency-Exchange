=============================
currency-open-exchange
=============================

Currency conversion

Quickstart
----------

Install currency_open_exchange::

    pip install currency-open-exchange

Then use it in a project::

    import currency_open_exchange

In order to save exchange rates to your database, add `currency_open_exchange` to your INSTALLED_APPS in your project's settings::

    INSTALLED_APPS = (
        ...
        'currency_open_exchange',
        ...
    )

Setup the Open Exchange Rates backend
-------------------------------------

Open an account at https://openexchangerates.org/ if you don't have one already. Then, add this to your project's settings::


    'EXCHANGE_APP_ID': 'YOUR APP ID HERE',
    'EXCHANGE_BASE_CURRENCY': 'USD' (optional, only USD for free accounts)


For more information on the Open Exchange Rates API, see https://openexchangerates.org/

Pull the latest Exchange Rates
------------------------------

Once your backend is setup, get the latest exchange rates::

    $ ./manage.py update_rates

Convert from one currency to another
------------------------------------

Here's an example of converting 10 American Dollars to Chinese Renminbi:

.. code-block:: python

    from currency_open_exchange.utils import convert
    amount, currency = convert(10, "EUR", "BRL")
