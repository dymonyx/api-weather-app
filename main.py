from fastapi import FastAPI
import uvicorn

from api.weather_routes import weather_router
from config import PORT

app = FastAPI()
app.include_router(weather_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
