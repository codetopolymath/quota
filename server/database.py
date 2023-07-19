from bson.objectid import ObjectId

import random
from datetime import datetime
import pytz

import motor.motor_asyncio 

MONGOURI = "mongodb+srv://rohit:12345@cluster0.dypvdcc.mongodb.net/?retryWrites=true&w=majority"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGOURI)

database = client.quotes

quote_collection = database.get_collection("quotes_collection")


# helpers : used to parse data from database to user
def quote_helper(quote) -> dict:
    current_time = datetime.now(pytz.timezone("Asia/Kolkata"))
    formatted_time = current_time.strftime("%Y-%m-%d")
    return {
        "id": quote["_id"],
        "content": quote["content"],
        "auther": quote["auther"],
        "category": quote["category"],
        "tags": quote["tags"],
        "created_at": str(formatted_time),
        "updated_at": str(formatted_time)   
    }


# get a random quote from the database
async def get_random_quote() -> dict:
    count = await quote_collection.count_documents({})
    if count == 0:
        return {"message": "No quotes found"}

    random_index = random.randint(0, count - 1)
    quote = await quote_collection.find().skip(random_index).limit(1).to_list(1)
    if quote:
        return quote_helper(quote[0])
    else:
        return {"message": "Failed to retrieve random quote"}

# get all quotes from database
async def retrieve_quotes():
    quotes = []
    async for quote in quote_collection.find():
        quotes.append(quote_helper(quote))
    return quotes

# add a quote into database
async def add_quote(quote_data: dict) -> dict:
    current_time = datetime.now(pytz.timezone("Asia/Kolkata"))
    formatted_time = current_time.strftime("%Y-%m-%d")
    quote_data["created_at"] = formatted_time
    quote_data["updated_at"] = formatted_time
    quote = await quote_collection.insert_one(quote_data)
    new_quote = await quote_collection.find_one({"_id": quote.inserted_id})
    return quote_helper(new_quote)

# retrieve a quote based in ObjectId
async def retrieve_quote(id: str) -> dict:
    quote = await quote_collection.find_one({"_id": id})
    if quote:
        return quote_helper(quote)
    else:
        return {"message": "quote not found"}
    
# update a quote based on ObjectId and provided data
async def update_quote(id: str, data: dict) -> str:
    # return false if empty request body is send
    if len(data) < 1:
        return {"message": "no data provided to update"}
    quote = await quote_collection.find_one({"_id": ObjectId(id)})
    if quote:
        updated_quote = await quote_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_quote:
            return quote_helper(await quote_collection.find_one({"_id": ObjectId(id)}))
        else:
            return {"message": "quote not found or update failed"}
    else:
        return {"message": "quote not found"}


# delete a quote based on ObjectId
async def delete_quote(id: str) -> str:
    quote = await quote_collection.find_one({"_id": ObjectId(id)})
    if quote:
        deleted_quote = await quote_collection.delete_one({"_id": ObjectId(id)})
        if deleted_quote:
            return {"message": "quote deleted"}
        else:
            return {"message": "quote not found or delete failed"}
    else:
        return {"message": "quote not found"}
