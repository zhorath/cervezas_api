# Cervezas API

## Usage

All responses will have the form

```json
{
    "is_success": "Bool state [true, false].",
    "status": "Simple status description",
    "error_message": "In case to error, describe what happened"
}
```

### Login

**Definition**

`GET /login`

**Response**

- `200 OK` on success

```json
{
    "status": "Login successfully",
    "is_sucess": true
}
```

Save the header property called "token_api", is goona be required for futures endpoints.

### Get All Beers

**Definition**

`GET /get_all_beers`

**Response**

- `200 OK` on success

```json
{
    "status": "Success",
    "is_successful": true,
    "data": [
        {
            "beer_id": 1,
            "beer_name": "Imperial Light",
            "alcohol_percentage": 3.7,
            "brand_name": "FIFCO",
            "type_name": "IPAs"
        }
    ]
}
```

`POST /get_all_beers`

**Response**

- `405 NOT_ALLOWED` on error

```json
{
    "message": "The method is not allowed for the requested URL."
}
```

### Get Specific Beer By User

**Definition**

`POST /get_beer`

**Arguments**

- `"beer_id":int` beer identificator

**Headers**

- `"token_api":str` session token identificator

**Response**

- `200 Created` on success

```json
{
    "status": "Success",
    "is_successful": true,
    "data": [
        {
            "beer_id": 3,
            "beer_name": "Imperial",
            "alcohol_percentage": 4.5,
            "brand_id": 1,
            "brand_name": "FIFCO",
            "type_id": 4,
            "type_name": "Lagers",
            "Cumulative total By User": 2,
            "Last Beer": "2020-03-08T20:05:44"
        }
    ]
}
```

## Add new beer to User

`GET /add_beer`

**Response**

- `200 OK` on success

```json
{
    "status": "Update successfully",
    "is_sucess": true
}
```

## Add new user

**Definition**

`POST /new_user`

**Arguments**

- `"beer_id":int` beer identificator

**Headers**

- `"token_api":str` session token identificator

**Response**

- `201 Created` on success

```json
{
    "status": "New user created",
    "is_sucess": true
}
```