from fastapi import APIRouter
from fastapi.responses import JSONResponse
from internal.service.health_service import HealthService

router = APIRouter(tags=["Health"])

@router.get("/health")
@router.get("/api/v1/health")
async def health_check():
    result = await HealthService.get_health_status()
    status_code = 200 if result["db"] == "up" else 503
    return JSONResponse(status_code=status_code, content=result)