# Weather Peru API

Weather Peru API is an app designed to showcase how [gpt-3.5-turbo](https://platform.openai.com/docs/guides/chat/introduction) can be used to interact with data in natural language. The API uses weather records from various meteorological stations across Peru to respond to natural language queries. Please note that the project does not come with data preloaded, and you will need to download the necessary data from the official website of [SENAMHI](https://www.senamhi.gob.pe/mapas/descarga-datos/pdf/tutorial-para-la-descarga-de-datos.pdf) before uploading it for use in the app.

## Set up

1. Clone this repository: `git clone https://github.com/IvanHerreraCasas/weather_peru_api.git`
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install the required packages: `pip install -r requirements.txt`
5. In the root directory create a new file `.env` with the following lines
```
SQLALCHEMY_DATABASE_URI=<YOUR_DATABASE_URI>
OPENAI_API_KEY=<YOUR_KEY>
```
5. Run the app: `flask run`
6. Upload your data (more details in usage section)

## Usage examples

### `/stations`

#### `POST`

Create a new or save a station.

##### Request Body

```json
{
  "name": "San Miguel",
  "region": "Piura",
  "province": "Piura",
  "district": "Castilla"
}
```

#### `GET`

Returns a list of all available stations in the specified region, province, district.

##### Paramaters

```json
{
  "region": "Piura"
}
```

##### Response

```json
[
    {
        "district": "Piura",
        "id": 5,
        "name": "Miraflores",
        "province": "Piura",
        "region": "Piura"
    },
    {
        "district": "Marvelica",
        "id": 6,
        "name": "Mallares",
        "province": "Sullana",
        "region": "Piura"
    },
    {
        "district": "Catacaos",
        "id": 7,
        "name": "San Miguel",
        "province": "Piura",
        "region": "Piura"
    }
]
```

### `/records`

#### `POST`

Upload and save a new records file.

##### Parameters

```json
{
  "station_name": "Catacaos"
}
```

##### Files

```json
{
  "file": "path/catacaos.txt"
}
```

#### `GET`

Returns a list of records that meet the specified conditions: date range, location, and station name.

##### Parameters

```json
{
  "start_date": "1998-03-22",
  "end_date": "1998-03-22",
  "region": "Piura",
  "province": "Piura"
}
```

##### Response

```json
[
    {
        "date": "1998-03-22",
        "id": 41082,
        "max_temp": 35.0,
        "min_temp": 25.2,
        "precipitation": 75.0,
        "station_name": "Miraflores"
    },
    {
        "date": "1998-03-22",
        "id": 95135,
        "max_temp": 34.5,
        "min_temp": 23.2,
        "precipitation": 34.0,
        "station_name": "San Miguel"
    }
]
```

### `/ask`

This is the main endpoint of this API. It receives natural language questions related to weather records from Peru and responds with the relevant information. The questions can be related to specific weather records, statistical information, or averages.

`GET`

#### Example 1

##### Parameters

```json
{
  "question": "What was the day with highest precipitation in Sullana."
}
```

##### Response

```json
{
  "answer": "The highest precipitation in Sullana was recorded on March 22, 1998, with 201mm. The temperature was between 24.5°C and 35.2°C. The station named \"Mallares\" registered this weather record.",
  "function_result": {
        "id": 60440,
        "date": "1998-03-22",
        "precipitation": 201.0,
        "max_temp": 35.2,
        "min_temp": 24.5,
        "station_name": "Mallares"
    } 
}
```

#### Example 2

##### Parameters

```json
{
  "question": "What was the average max temperature in Piura, Piura from 2000 to 2015?"
}
```

##### Response

```json
{
    "answer": "The average max temperature in Piura, Piura from 2000 to 2015 was 30.8 degrees Celsius.",
    "function_result": 30.837992986989494
}
```

### `/statistics/records`

#### `GET`

This endpoint returns the weather record with the highest or lowest value of a specified parameter in the specified conditions.

##### Parameters

```json
{
  "stat_type": "max",
  "parameter": "precipitation",
  "region": "Piura",
  "province": "Sullana"
}
```

##### Response

```json
{
    "record": {
        "date": "2011-03-11",
        "id": 84716,
        "max_temp": 38.6,
        "min_temp": 19.9,
        "precipitation": 0.0,
        "station_name": "Mallares"
    }
}
```

### `/statistic/value`

#### `GET`

Return a statistical value (average, ...) in the specified conditions.

##### Parameters

```json
{
  "stat_type": "average",
  "parameter": "max_temp",
  "region": "Piura",
  "province": "Piura"
}
```

##### Response

```json
{
    "value": 30.614071868307963
}
```

## Conclusion

The Weather Peru API project demonstrates how natural language processing and machine learning can be used to make data more accessible to non-technical users. This API provides an intuitive and user-friendly interface for querying weather records in Peru. Users can interact with the data using conversational language, making the data more accessible to people who may not have the technical expertise required to use traditional data analysis tools. This API can be easily extended to include data from other regions or weather parameters, providing a powerful tool for exploring and understanding weather patterns in Peru.