from fastapi import FastAPI
from app.routes.route import router
from app.routes.operation import router as operation_router


app = FastAPI()

app.include_router(router=router, prefix="/api/todos", tags=["todos"])
app.include_router(router=operation_router, prefix="/api/operations", tags=["operations"])