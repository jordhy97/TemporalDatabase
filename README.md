# TemporalDatabase
 Temporal Database Assignment for IF4040 Advanced Data Modelling

# Endpoints
- **`GET`** `/table`
    - Parameters:
        - `table`: Table name
    - Response: Entire table in JSON
    - Example:
        ```
        GET /table?table=emp
        ```
        ```
        [
            {
                "instance": "Engineering",
                "name": "Claudine Summerside",
                "valid_from": "1981-11-21",
                "valid_to": "2018-03-22"
            },
            {
                "instance": "Services",
                "name": "Garvy Domke",
                "valid_from": "1992-04-02",
                "valid_to": "2018-08-14"
            },
            ...
        ]
        ```
- **`POST`** `/allen`
    - Parameters: JSON
        - `data`: Two element list. Each member must contain a `valid_from` field and a `valid_to` field
        - `op`: One of the following:
            - `before`
            - `after`
            - `equals`
            - `meets`
            - `met_by`
            - `overlaps`
            - `overlapped_by`
            - `during`
            - `contains`
            - `starts`
            - `started_by`
            - `finishes`
            - `finished_by`
    - Response: `True` or `False` string
    - Example:
        ```
        POST /allen

        {
            "data": [
                {
                    "instance": "Engineering",
                    "name": "Claudine Summerside",
                    "valid_from": "1981-11-21",
                    "valid_to": "2018-03-22"
                },
                {
                    "instance": "Services",
                    "name": "Garvy Domke",
                    "valid_from": "1992-04-02",
                    "valid_to": "2018-08-14"
                }
            ],
            "op": "overlapped_by"
        }
        ```
        ```
        True
        ```

## Temporal Algebra
- **`POST`** `/select`
    - Parameters: JSON
        ```
        {
            "data": [
                {
                    "col": column name,
                    "op": binary operator ("=", "<", ...),
                    "val": value to compare,
                },
                ...
            ],
            "table": table name
        }
        ```
    - Response: Query result as JSON list
    - Example:
        ```json
        POST /select

        {
            "data": [
                {
                    "col": "instance",
                    "op": "=",
                    "val": "Marketing"
                },
                {
                    "col": "name",
                    "op": "LIKE",
                    "val": "F%"
                }
            ],
            "table": "emp"
        }
        ```
        ```json
        [
            {
                "name": "Fannie Porson",
                "instance": "Marketing",
                "valid_from": "1985-05-09",
                "valid_to": "1987-11-11"
            }
        ]
        ```
- **`POST`** `/project`
    - Parameters: JSON
        ```
        {
            "table": table name,
            "col": column to project
        }
        ```
    - Response: Query result as JSON list
    - Example:
        ```json
        POST /project

        {
            "table": "emp",
            "col": "instance"
        }
        ```
        ```json
        [
            {
                "instance": "Training",
                "valid_from": "1978-12-22",
                "valid_to": "1984-06-23"
            },
            {
                "instance": "Training",
                "valid_from": "2014-01-09",
                "valid_to": "2035-02-21"
            },
            {
                "instance": "Marketing",
                "valid_from": "1981-01-15",
                "valid_to": "1989-04-22"
            },
            {
                "instance": "Support",
                "valid_from": "1998-05-27",
                "valid_to": "2012-01-31"
            }
        ]
        ```
- **`POST`** `/union`
    - Parameters: JSON
        ```
        {
            "tables": [list of table names]
        }
        ```
    - Response: Query result as JSON list
    - Example:
        ```json
        POST /union

        {
            "tables": ["dept", "mgr"]
        }
        ```
        ```json
        [
            {
                "employee": "Aindrea Turrell",
                "department": "Support",
                "valid_from": "1972-01-28",
                "valid_to": "2017-09-17"
            },
            {
                "employee": "Arley McGeraghty",
                "department": "Marketing",
                "valid_from": "1992-01-01",
                "valid_to": "2008-03-24"
            },
            {
                "employee": "Ianthe Imlen",
                "department": "Support",
                "valid_from": "2007-08-23",
                "valid_to": "2029-09-06"
            },
            {
                "employee": "Louis Plail",
                "department": "Marketing",
                "valid_from": "1997-08-07",
                "valid_to": "2000-08-26"
            },
            {
                "employee": "Cyrus Hymers",
                "department": "Support",
                "valid_from": "1993-01-19",
                "valid_to": "2008-08-11"
            },
            {
                "employee": "Paulie Toulmin",
                "department": "Training",
                "valid_from": "1974-06-22",
                "valid_to": "1991-03-21"
            },
            {
                "employee": "Paulie Toulmin",
                "department": "Training",
                "valid_from": "1994-11-25",
                "valid_to": "2012-02-29"
            },
            {
                "employee": "Fannie Porson",
                "department": "Marketing",
                "valid_from": "1997-04-13",
                "valid_to": "2007-06-09"
            },
            {
                "employee": "Kore Skelcher",
                "department": "Marketing",
                "valid_from": "2012-07-31",
                "valid_to": "2033-10-16"
            }
        ]
        ```
- **`POST`** `/set_difference`
    - Parameters: JSON
        ```
        {
            "tables": [list of table names. First table name is the table subtracted from]
        }
        ```
    - Response: Query result as JSON list
    - Example:
        ```json
        POST /set_difference

        {
            "tables": ["dept", "emp"]
        }
        ```
        ```json
        [
            {
                "employee": "Aindrea Turrell",
                "department": "Support",
                "valid_from": "1972-01-28",
                "valid_to": "2017-09-17"
            },
            {
                "employee": "Ianthe Imlen",
                "department": "Support",
                "valid_from": "2025-05-31",
                "valid_to": "2029-09-06"
            },
            {
                "employee": "Louis Plail",
                "department": "Marketing",
                "valid_from": "1997-08-07",
                "valid_to": "2000-08-26"
            },
            {
                "employee": "Paulie Toulmin",
                "department": "Training",
                "valid_from": "1974-06-22",
                "valid_to": "1991-03-21"
            },
            {
                "employee": "Kore Skelcher",
                "department": "Marketing",
                "valid_from": "2012-07-31",
                "valid_to": "2033-10-16"
            }
        ]
        ```
- **`POST`** `/join`
    - Parameters: JSON
        ```
        {
            "tables": [list of table names]
        }
        ```
    - Response: Query result as JSON list
    - Example:
        ```json
        POST /join

        {
            "tables": ["dept", "mgr"]
        }
        ```
        ```json
        [
            {
                "name": "Arley McGeraghty",
                "department": "Marketing",
                "employee": "Louis Plail",
                "valid_from": "1997-08-07",
                "valid_to": "2000-08-26"
            },
            {
                "name": "Cyrus Hymers",
                "department": "Support",
                "employee": "Aindrea Turrell",
                "valid_from": "1993-01-19",
                "valid_to": "2008-08-11"
            },
            {
                "name": "Fannie Porson",
                "department": "Marketing",
                "employee": "Louis Plail",
                "valid_from": "1997-08-07",
                "valid_to": "2000-08-26"
            },
            {
                "name": "Ianthe Imlen",
                "department": "Support",
                "employee": "Aindrea Turrell",
                "valid_from": "2007-08-23",
                "valid_to": "2017-09-17"
            },
            {
                "name": "Ianthe Imlen",
                "department": "Support",
                "employee": "Ianthe Imlen",
                "valid_from": "2014-08-20",
                "valid_to": "2025-05-31"
            }
        ]
        ```
- **`POST`** `/timeslice`
    - Parameters: JSON
        ```
        {
            "table": table name,
            "time": valid time to slice
        }
        ```
    - Response: Query result as JSON list
    - Example:
        ```json
        POST /timeslice

        {
            "table": "dept",
            "time": "2000-01-01"
        }
        ```
        ```json
        [
            {
                "employee": "Aindrea Turrell",
                "department": "Support"
            },
            {
                "employee": "Louis Plail",
                "department": "Marketing"
            }
        ]
        ```

## Data Modification
- **`POST`** `/insert`
    - Parameters: JSON
        ```
        {
            "data": data to insert,
            "table": table to insert to
        }
        ```
    - Response: Number of rows affected
    - Example:
        ```json
        POST /insert

        {
            "table": "mgr",
            "data": {
                "name": "Paulie Toulmin",
                "department": "Training",
                "valid_from": "2000-01-01",
                "valid_to": "2030-01-01"
            }
        }
        ```
        ```
        1
        ```
- **`POST`** `/delete`
    - Parameters: JSON
        ```
        {
            "data": data to delete,
            "table": table to delete from
        }
        ```
    - Response: Number of rows affected
    - Example:
        ```json
        POST /delete

        {
            "table": "mgr",
            "data": {
                "name": "Paulie Toulmin",
                "department": "Training",
                "valid_from": "2000-01-01",
                "valid_to": "2030-01-01"
            }
        }
        ```
        ```
        1
        ```