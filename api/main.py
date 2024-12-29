from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from routers import garage_router, car_router, maintenance_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"detail": "Bad request"},
    )

app.include_router(garage_router.router, prefix="/garages", tags=["Garages"])

app.include_router(car_router.router,prefix="/cars",tags=["Cars"])

app.include_router(maintenance_router.router,prefix="/maintenance",tags=["Maintenances"])




