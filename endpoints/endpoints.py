from typing import Optional

from fastapi import APIRouter, File, Query
from pydantic import BaseModel

from ..utils import file_parser

router = APIRouter()


class Individual(BaseModel):
    individual_id: str


db_handler = None # Initialize to None

def set_db_handler(db):
    global db_handler
    db_handler = db


@router.get("/individuals")
def read_all_users():
    """GET /individuals: returns a list of individual IDs"""
    return db_handler.get_all_users()


@router.get("/individuals/{individual}/genetic-data")
def read_individual(
    individual: str, variants: Optional[str] = Query(None, alias="variants")
):
    """
    GET /individuals/<individual_id>/genetic-data?variants=rs123,rs456:
    returns all the genetic data for a single individual, optionally filtered by variant IDs
    """
    return db_handler.get_individual_data(individual, variants)


@router.post("/individuals")
def create_individual(new_individual: Individual):
    """POST /individuals: creates a new individual given an ID"""
    db_handler.insert_new_individual(new_individual.individual_id)
    return "Succesfully added new individual"


@router.post("/individuals/{individual_id}/genetic_data")
def insert_individual_data(individual_id: str, file: bytes = File(...)):
    """
    POST /individuals/<individual_id>/genetic-data:
    takes a sano file and stores the genetic data for that individual to be queried later
    """
    content = file.decode("utf-8")
    lines = content.split("\n")
    file_parser.batch_insert_genetic_data_to_db(lines, individual_id, db_handler)
    return "Successfully uploaded data"
