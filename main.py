import mysql.connector
from fastapi import FastAPI
import statistics as stats
from pydantic import BaseModel
import config

temp_db = mysql.connector.connect(
    host=config.DATABASE_CONFIG["host"],
    user=config.DATABASE_CONFIG["user"],
    password=config.DATABASE_CONFIG["password"],
    database=config.DATABASE_CONFIG["database"],
)
cursor = temp_db.cursor()


class Temperature(BaseModel):
    timestamp: int
    timezone: str
    measurement: float
    unit: str
    location: str


def median(arr):
    arr = sorted(arr)
    if len(arr) % 2:
        return arr[len(arr) // 2]
    else:
        return (arr[len(arr) // 2] + arr[len(arr) // 2 - 1]) / 2


app = FastAPI()


@app.get("/")
def list_all():
    cursor.execute("SELECT * FROM temp_table")
    return cursor.fetchall()


@app.post("/temperature")
def submit_temperature(item: Temperature):
    cursor.execute("""INSERT INTO temp_table ( timestamp, timezone, measurement, unit, location ) VALUES (%s, %s, %s, %s, %s)""",
                   (item.timestamp, item.timezone, item.measurement, item.unit, item.location))
    temp_db.commit()
    return item


@app.get("/stats/{since}/{until}/{location}/{unit}/")
def get_stats(since: str, until: str, location: str, unit: str):
    cursor.execute("""SELECT measurement FROM temp_table WHERE location = %s AND unit = %s AND timestamp >= %s AND timestamp <= %s""",
                   (location, unit, since, until))
    result = list(map(lambda x: x[0], cursor.fetchall()))
    print(result)

    return {
        "average": stats.mean(result),
        "median": stats.median(result),
        "count": len(result),
    }
