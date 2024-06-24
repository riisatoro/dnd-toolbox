from fastapi import APIRouter

from views.main import router as main_router
from views.auth import router as auth_router
from views.sheets import router as sheets_router


router = APIRouter()

router.include_router(main_router)
router.include_router(auth_router)
router.include_router(sheets_router)
