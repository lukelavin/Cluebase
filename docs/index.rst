.. Cluebase documentation master file, created by
   sphinx-quickstart on Sat Aug 10 18:49:37 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

What is Cluebase?
====================================

Cluebase is an API of all recorded *Jeopardy!* games. Over 5,000 games,
10,000 contestants, and 350,000 clues are available through Cluebase.

All information was scraped from J-Archive_, which is a fan-operated archive of
*Jeopardy!* information. The data in Cluebase is only as good as the data in
J-Archive. If you notice any bad data that you believe should be removed from
the database, you can contact me at llavin@purdue.edu.

Cluebase was originally intended to be the backend for a personal project that
allowed you to practice for the *Jeopardy!* online exam using previously aired
clues. If I ever get around to doing that, I'll leave a link here.

.. _J-Archive: https://www.j=archive.com

General Info
===============

**All of Cluebase's endpoints return simple JSON representations.**

Here's an example of how Cluebase may respond to a successful API call::

   {
     status: "success",
     data: [
       {
         id: 2,
         game_id: 1,
         value: 200,
         daily_double: false,
         round: "J!",
         category: "2 VERBS IN ONE",
         clue: "To travel by taking rides from passing cars",
         response: "hitchhike"
       }
     ]
   }


The ``status`` key will hold either ``"success"`` or ``"failure"``.
 - If the JSON object returned has a status of ``"failure"``, there will
   be no data in the object. **It is your responsibility to check the status
   of each response before attempting to access the data.**
 - On failure, instead of returning an object with a ``data`` value,
   an object with an ``error`` value will be returned, giving the name
   and message for the error that occurred.

Here's an example of a failed call to the API::

  {
    status: "failure",
    error: "LimitNotANumberError(): Limit parameter must be a valid number"
  }

As mentioned, this JSON object returned has no value for ``data``,
and instead holds error information in ``error``.


Endpoints
=========


Clues
-----

Info about /clues endpoints


Categories
----------

Info about /categories endpoints


Games
-----

**Game Model**

+-------------+---------+-------------------------------------------------------------------------------------------------------+
| Field       | Type    | Notes                                                                                                 |
+=============+=========+=======================================================================================================+
| id          | integer |                                                                                                       |
+-------------+---------+-------------------------------------------------------------------------------------------------------+
| episode_num | integer | The episode number (more descriptive than the id)                                                     |
+-------------+---------+-------------------------------------------------------------------------------------------------------+
| season_id   | integer | The **id** for the season in which this game aired                                                    |
+-------------+---------+-------------------------------------------------------------------------------------------------------+
| air_date    | String  | Air date of this episode, in the format of "YYYY-MM-DD"                                               |
+-------------+---------+-------------------------------------------------------------------------------------------------------+
| notes       | String  | Special notes about the episode. Includes notable players, tournament details, and other fun tidbits. |
+-------------+---------+-------------------------------------------------------------------------------------------------------+
| contestant1 | integer | The **id** of the first contestant                                                                    |
+-------------+---------+-------------------------------------------------------------------------------------------------------+
| contestant2 | integer | The **id** of the second contestant                                                                   |
+-------------+---------+-------------------------------------------------------------------------------------------------------+
| contestant3 | integer | The **id** of the third contestant                                                                    |
+-------------+---------+-------------------------------------------------------------------------------------------------------+
| winner      | integer | The **id** of the winner of the game                                                                  |
+-------------+---------+-------------------------------------------------------------------------------------------------------+
| score1      | integer | The final score of the first contestant                                                               |
+-------------+---------+-------------------------------------------------------------------------------------------------------+
| score2      | integer | The final score of the second contestant                                                              |
+-------------+---------+-------------------------------------------------------------------------------------------------------+
| score3      | integer | The final score of the third contestant                                                               |
+-------------+---------+-------------------------------------------------------------------------------------------------------+


Contestants
-----------

**Contestant Model**

All JSON objects found in the ``data`` array for contestant calls will follow this model.

+----------------+---------+--------------------------------------------------------------------------------------+
| Field          | Type    | Notes                                                                                |
+================+=========+======================================================================================+
| id             | integer |                                                                                      |
+----------------+---------+--------------------------------------------------------------------------------------+
| name           | String  | Contestant's name                                                                    |
+----------------+---------+--------------------------------------------------------------------------------------+
| notes          | String  | Contestant's intro, including job and hometown                                       |
+----------------+---------+--------------------------------------------------------------------------------------+
| games_played   | integer | Total games played. May be inaccurate if the contestant has played tournament games. |
+----------------+---------+--------------------------------------------------------------------------------------+
| total_winnings | integer | Total winnings. May be inaccurate if the contestant has played tournament games.     |
+----------------+---------+--------------------------------------------------------------------------------------+

``/contestants``
~~~~~~~~~~~~~~~~

Lists all recorded contestants.

**Example output**::

  {
    status: "success",
    data: [
      {
        id: 208,
        name: "Ken Jennings",
        notes: "a software engineer from Salt Lake City, Utah",
        games_played: 94,
        total_winnings: 2522700
      }
    ]
  }

**Possible Query Parameters**

- ``?limit=<int>``
   - Limits the response to a maximum of <int> contestants.
   - **Set to 50 by default.**
   - **Maximum of 1000.**

- ``?offset=<int>``
   - Accesses the data starting from an offset of <int> places.
   - Especially useful in conjunction with limit to achieve
     pagination (Page 1 is limit 50 offset 0, Page 2 is limit
     50 offset 50, etc.).
   - **Set to 0 by default.**

- ``?order_by=<field>``
   - Orders the data by the given field.
   - For example, ``?order_by=name`` will alphabetically order the returned
     contestants by their names.
   - **Set to id by default.**

- ``?sort=asc`` or ``?sort=desc``
   - Used to change the direction of order_by results.
   - ``?sort=asc`` will order the results in ascending order, and ``?sort=desc``
     will order the results in descending order.
   - **Set to ``asc`` by default.**

Example Url

   https://cluebase.lukelav.in/contestants?limit=10&order_by=total_winnings&sort=desc

This call will return the top 10 contestants who won the most.

``/contestants/<id>``
~~~~~~~~~~~~~~~~~~~~~~

Information on a specific contestant.


Seasons
-------

**Season Model**

All JSON objects found in the ``data`` array for season calls will follow this model.

+-------------+---------+-----------------------------------------------------------------------------+
| Field       | Type    | Notes                                                                       |
+=============+=========+=============================================================================+
| id          | integer |                                                                             |
+-------------+---------+-----------------------------------------------------------------------------+
| season_name | String  | Name of the season (usually "Season [Number]")                              |
+-------------+---------+-----------------------------------------------------------------------------+
| start_date  | String  | Air date of the first episode in this season, in the format of "YYYY-MM-DD" |
+-------------+---------+-----------------------------------------------------------------------------+
| end_date    | String  | Air date of the first episode in this season, in the format of "YYYY-MM-DD" |
+-------------+---------+-----------------------------------------------------------------------------+
| total_games | integer | Total games documented in this season                                       |
+-------------+---------+-----------------------------------------------------------------------------+


Util
----

Cluebase also has some other miscellaneous endpoints.

``/uptime``
~~~~~~~~~~~

Returns how long the API has been running.

Example output::

   {
     status: "success",
     uptime: "4 days, 04:15:23.421409"
   }


Errors
======

In the result of a failure, Cluebase returns details about the error that
occurred.

LimitNotANumberError
--------------------

Results from an incorrectly formed query string. The limit parameter must
be a valid number.

**Bad example**::

   https://cluebase.lukelav.in/clues?limit=ThisIsAString

"ThisIsAString" is obviously not a number. Here's what it should look like.

**Good example**::

   https://cluebase.lukelav.in/clues?limit=30

This will properly use the "limit" parameter to return a maximum of 30 clues.
