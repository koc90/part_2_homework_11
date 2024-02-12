from typing import List

from fastapi import Query, Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.schemas import ContactBase, ContactResponse


import src.repository.contacts as contact_repo


router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/", response_model=List[ContactResponse])
async def display_choosen_contacts(
    field: str = Query(), value: str = Query(), db: Session = Depends(get_db)
):
    print("We are in routes.display_choosen_contacts function")

    contacts = await contact_repo.get_contacts_by(field, value, db)

    if bool(contacts) == False:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No contact found"
        )
    print(contacts[0].id)
    return contacts


@router.get("/all", response_model=List[ContactResponse])
async def display_all_contacts(db: Session = Depends(get_db)):
    print("We are in routes.display_all_contacts function")
    contacts = await contact_repo.get_contacts(db)
    print(contacts)
    return contacts


@router.get("/birthday", response_model=List[ContactResponse])
async def display_contacts_with_upcoming_birthay(db: Session = Depends(get_db)):
    print("We are in routes.display_contacts_with_upcoming_birthay function")
    contacts = await contact_repo.get_contact_with_upcoming_birtday(db)
    print(contacts)
    return contacts


@router.post("/", response_model=ContactResponse)
async def add_new_contact(body: ContactBase, db: Session = Depends(get_db)):
    print("We are in routes.add_new_contact function")
    new_contact = await contact_repo.create_new_contact(body, db)
    return new_contact


@router.put("/", response_model=ContactResponse)
async def update_choosen_contact(
    body: ContactBase,
    field: str = Query(),
    value: str = Query(),
    db: Session = Depends(get_db),
):
    print("We are in routes.update_choosen_contacts function")
    contacts = await contact_repo.get_contacts_by(field, value, db)

    if bool(contacts) == False:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No contact found"
        )

    contact_to_update = contacts[0]
    print(f"contact_to_update = {contact_to_update}")

    updated_contact = await contact_repo.update_contact(contact_to_update.id, body, db)
    return updated_contact


@router.delete("/", response_model=ContactResponse)
async def remove_choosen_contact(
    field: str = Query(),
    value: str = Query(),
    db: Session = Depends(get_db),
):
    print("We are in routes.remove_choosen_contact function")
    contacts = await contact_repo.get_contacts_by(field, value, db)

    if bool(contacts) == False:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No contact found"
        )

    contact_to_remove = contacts[0]

    removed_contact = await contact_repo.remove_contact(contact_to_remove.id, db)
    return removed_contact
