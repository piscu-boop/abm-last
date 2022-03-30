from sys import api_version
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_company_name():
    return {"Company name": "Example company, LLC"}


@router.get("/employees")
async def get_employees_number():
    return 165