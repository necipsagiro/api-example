from fastapi import FastAPI
from pydantic import BaseModel


class Temperature(BaseModel):
    timestamp: str
    timezone: str
    measurement: int
    unit: str
    location: str


temps = [
    Temperature(
        timestamp="1681895166",
        timezone="UTC",
        measurement=1,
        unit="F",
        location="Germany"
    ),
    Temperature(
        timestamp="1681895168",
        timezone="UTC",
        measurement=2,
        unit="F",
        location="France"
    ),
]

app = FastAPI()


@app.post("/temperature")
def submit_temperature(item: Temperature):
    temps.append(item)
    print(temps)
    return item


@app.get("/temperature/{since}/{until}/{location}/{unit}/")
def get_temperature(since: str, until: str, location: str, unit: str):
    result = []
    for temp in temps:
        if temp.location == location and temp.unit == unit and temp.timestamp >= since and temp.timestamp <= until:
            result.append(temp)
    return result


@app.get("/stats/{since}/{until}/{location}/{unit}/")
def get_stats(since: str, until: str, location: str, unit: str):
    result = []
    for temp in temps:
        if temp.location == location and temp.unit == unit and temp.timestamp >= since and temp.timestamp <= until:
            result.append(temp)
    return
