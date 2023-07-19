from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database import (
    add_quote,
    delete_quote,
    retrieve_quote,
    retrieve_quotes,
    update_quote,
    get_random_quote
)

from server.models.quote import (
    ResponseModel,
    ErrorResponseModel,
    QuoteSchema,
    UpdateQuoteModel,
)

router = APIRouter()

@router.get("/random", response_description="Random quote retrieved")  # Add the new route
async def get_random_quote_data():
    ''' Get a random quote '''
    quote = await get_random_quote()
    if quote:
        return ResponseModel(quote, "Random quote retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "No quotes found.")

@router.post("/", response_description="create a quote")
async def add_quote_data(quote: QuoteSchema = Body(...)):
    ''' Create a new quote '''
    quote = jsonable_encoder(quote)
    new_quote = await add_quote(quote)
    return ResponseModel(new_quote, "quote added successfully")

@router.get("/", response_description="quotes retrieved")
async def get_quotes():
    ''' Get all quotes '''
    quotes = await retrieve_quotes()
    if quotes:
        return ResponseModel(quotes, "quotes data retrieved successfully")
    return ResponseModel(quotes, "Empty list returned")


@router.get("/{id}", response_description="quote data retrieved")
async def get_quote_data(id):
    ''' Get single quote by id '''
    quote = await retrieve_quote(id)
    if quote:
        return ResponseModel(quote, "quote data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "quote doesn't exist.")


@router.put("/{id}")
async def update_quote_data(id: str, req: UpdateQuoteModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_quote = await update_quote(id, req)
    if updated_quote:
        return ResponseModel(
            "Quote with ID: {} name update is successful".format(id),
            "Quote name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the qoute data.",
    )

@router.delete("/{id}", response_description="Quote data deleted from the database")
async def delete_quote_data(id: str):
    delete_quote = await delete_quote(id)
    if delete_quote:
        return ResponseModel(
            "Quote with ID: {} removed".format(id), "Quote deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Quote with id {0} doesn't exist".format(id)
    )