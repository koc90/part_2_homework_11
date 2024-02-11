import uvicorn
from fastapi import FastAPI

from src.routes import contacts

app = FastAPI()

app.include_router(contacts.router, prefix="/api")


@app.get("/")
def read_root():
    dict_to_return = {
        "AppName": "Contacts",
        "Documentation": "/docs",
        "Display all contacts": "/contacts/all",
        "Display contact": "/contacts/?field=field_name&value=value",
        "field_name": ["id", "first_name", "last_name", "email"],
    }

    return dict_to_return


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
