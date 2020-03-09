# Import Json Lib
from datetime import datetime

# Import Sqlite3 Lib
import sqlite3


def getDBConnection():
    conn = sqlite3.connect('database/database.db')
    conn.row_factory = sqlite3.Row
    return conn


def newUser(username: str, password: str):
    """
        Query to add a new beer to user
    """

    _conn = getDBConnection()

    with _conn:
        cursor = _conn.cursor()
        update_ts = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        cursor.execute(
            """
                insert into tb_users
                (
                    username, password, is_active, created_date
                )
                values
                (
                    ?, ?, true, ?
                );
            """, (username, password, update_ts)
        )
        cursor.execute(
            """
                select last_insert_rowid() as "user_id"
            """
        )

        rows = cursor.fetchall()

    return ([dict(row) for row in rows])


def checkUser(username: str, password: str):
    """
        Query to add a new beer to user
    """

    _conn = getDBConnection()

    with _conn:
        cursor = _conn.cursor()
        update_ts = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        cursor.execute(
            """
                select  *
                from    tb_users
                where   username = ?
                        and
                        password = ?
                        and
                        is_active is true;
            """, (username, password)
        )

        rows = cursor.fetchall()
        response = [dict(row) for row in rows]

    if len(response) == 1:
        return response[0]
    else:
        return None


def getAllBeers():
    """
        Query to get all available beers from Sqlite
    """

    _conn = getDBConnection()

    with _conn:
        cursor = _conn.cursor()
        cursor.execute(
            """
                Select  b.id as "beer_id",
                        b.name as "beer_name",
                        b.alcohol_percentage,
                        bb.name as "brand_name",
                        bt.name as "type_name"
                from    tb_beers as b
                    inner join tb_beer_types as bt
                        on  b.type_id = bt.id
                            and
                            b.is_active is true
                    inner join tb_beer_brands as bb
                        on b.brand_id = bb.id;
            """
        )

        rows = cursor.fetchall()

    return ([dict(row) for row in rows])


def getBeerByUser(beer_id: int, user_id: int):
    """
        Query to get a specific beer by user
    """

    _conn = getDBConnection()

    with _conn:
        cursor = _conn.cursor()
        cursor.execute(
            """
                Select  b.id as "beer_id",
                        b.name as "beer_name",
                        b.alcohol_percentage,
                        b.brand_id,
                        bb.name as "brand_name",
                        b.type_id,
                        bt.name as "type_name",
                        ifnull(bbu.count, 0) as "Cumulative total By User",
                        bbu.last_modified_date as "Last Beer"
                from    tb_beers as b
                    inner join tb_beer_types as bt
                        on  b.type_id = bt.id
                            and
                            b.id = ?
                            and
                            b.is_active is true
                    inner join tb_beer_brands as bb
                        on  b.brand_id = bb.id
                    left join tb_beers_by_user as bbu
                        on  b.id = bbu.beer_id
                            and
                            bbu.user_id = ?;
            """, (beer_id, user_id))

        rows = cursor.fetchall()

    return ([dict(row) for row in rows])


def newBeerToUser(beer_id: int, user_id: int):
    """
        Query to add a new beer to user
    """

    _conn = getDBConnection()

    with _conn:
        cursor = _conn.cursor()
        update_ts = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        cursor.execute(
            """
                insert into tb_beers_by_user
                (
                    user_id, beer_id, count, last_modified_date
                )
                values
                (
                    :user_id, :beer_id, 1, :last_modified_date
                )
                on conflict(user_id, beer_id) do update
                set count = count + 1,
                    last_modified_date = :last_modified_date
                WHERE   user_id = :user_id
                        and
                        beer_id = :beer_id;
            """, {"beer_id": beer_id, "user_id": user_id, "last_modified_date": update_ts}
        )

        rows = cursor.fetchall()

    return ([dict(row) for row in rows])
