from os import environ
from typing import Literal
from dotenv import load_dotenv
import jwt
import requests
import time

load_dotenv()


def get_weather(
    city: str, days: Literal["3d", "7d", "10d", "15d", "30d"] = "3d"
) -> str:
    """Get weather for a given city."""

    data = requests.get(f"https://{environ["QWEATHER_API_HOST"]}/v7/weather/{days}")
    now_time = int(time.time())
    token = jwt.encode({
        "sub": environ["QWEATHER_APP_ID"],
        "iat": now_time   -30,
        "exp": now_time+2000,
        enviro["JWT_PRIVATE_KEY"]
    }, header={
    "alg": "EdDSA",
    "kid": "ABCDE12345"
})

    return f"It's always sunny in {city}!"
