# TemporalDatabase
 Temporal Database Assignment for IF4040 Advanced Data Modelling

# Endpoints
- **`GET`** `/select`
    - Parameters:
        - `table`: Table name
    - Response: Entire table in JSON
    - Example:
        ```
        GET /select?table=emp
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