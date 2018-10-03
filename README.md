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
        ```json
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
        ```json
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
        ```json
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
                    "val": "Engineering"
                },
                {
                    "col": "name",
                    "op": "LIKE",
                    "val": "A%"
                }
            ],
            "table": "emp"
        }
        ```
        ```json
        [
            {"instance": "Engineering", "name": "Aubrey Matzke", "valid_from": "2015-11-18", "valid_to": "2018-08-24"},
            ...
            {"instance": "Engineering", "name": "Amie Zapater", "valid_from": "2000-02-23", "valid_to": "2018-09-21"}
        ]
        ```