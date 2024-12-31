from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import garage_router, car_router, maintenance_router
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(garage_router.router, prefix="/garages", tags=["Garages"])
app.include_router(car_router.router,prefix="/cars",tags=["Cars"])
app.include_router(maintenance_router.router,prefix="/maintenance",tags=["Maintenances"])

uvicorn.run(app,host="127.0.0.1",port=8088)



