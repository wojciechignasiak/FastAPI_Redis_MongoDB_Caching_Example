from starlette.requests import Request

async def get_mongo_client(request: Request):
    try:
        return request.app.state.mongo_client
    except Exception as e:
        print({"get_mongo_client": f"Error: {e}"})