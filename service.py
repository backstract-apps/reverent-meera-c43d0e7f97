from sqlalchemy.orm import Session, aliased
from database import SessionLocal
from sqlalchemy import and_, or_
from typing import *
from fastapi import Request, UploadFile, HTTPException
import models, schemas
import boto3
import jwt
from datetime import datetime
import requests
import math
import random
import asyncio
from pathlib import Path


def convert_to_datetime(date_string):
    if date_string is None:
        return None
    from fastapi import HTTPException

    if "T" in date_string:
        try:
            return datetime.fromisoformat(date_string.replace("Z", "+00:00"))
        except ValueError:
            date_part = date_string.split("T")[0]
            try:
                return datetime.strptime(date_part, "%Y-%m-%d")
            except ValueError:
                raise HTTPException(
                    status_code=422,
                    detail=f"Improper format in datetime: {date_string}",
                )
    else:
        try:
            return datetime.strptime(date_string, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(
                status_code=422, detail=f"Improper format in datetime: {date_string}"
            )


async def get_foods_id(db: Session, id: int):

    query = db.query(models.Foods)
    query = query.filter(and_(models.Foods.id == id))

    foods_one = query.first()

    foods_one = (
        (foods_one.to_dict() if hasattr(foods_one, "to_dict") else vars(foods_one))
        if foods_one
        else foods_one
    )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"foods_one": foods_one},
    }
    return res


async def get_meallogs_id(db: Session, id: int):

    query = db.query(models.Meallogs)
    query = query.filter(and_(models.Meallogs.id == id))

    meallogs_one = query.first()

    meallogs_one = (
        (
            meallogs_one.to_dict()
            if hasattr(meallogs_one, "to_dict")
            else vars(meallogs_one)
        )
        if meallogs_one
        else meallogs_one
    )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"meallogs_one": meallogs_one},
    }
    return res


async def get_foods(db: Session):

    query = db.query(models.Foods)

    foods_all = query.all()
    foods_all = (
        [new_data.to_dict() for new_data in foods_all] if foods_all else foods_all
    )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"foods_all": foods_all},
    }
    return res


async def post_foods(db: Session, raw_data: schemas.PostFoods):
    name: str = raw_data.name
    serving_size_g: float = raw_data.serving_size_g
    calories: int = raw_data.calories
    macros: str = raw_data.macros
    is_verified: int = raw_data.is_verified

    record_to_be_added = {
        "name": name,
        "macros": macros,
        "calories": calories,
        "is_verified": is_verified,
        "serving_size_g": serving_size_g,
    }
    new_foods = models.Foods(**record_to_be_added)
    db.add(new_foods)
    db.commit()
    db.refresh(new_foods)
    foods_inserted_record = new_foods.to_dict()

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"foods_inserted_record": foods_inserted_record},
    }
    return res


async def put_foods_id(db: Session, raw_data: schemas.PutFoodsId):
    id: int = raw_data.id
    name: str = raw_data.name
    serving_size_g: float = raw_data.serving_size_g
    calories: int = raw_data.calories
    macros: str = raw_data.macros
    is_verified: int = raw_data.is_verified

    query = db.query(models.Foods)
    query = query.filter(and_(models.Foods.id == id))
    foods_edited_record = query.first()

    if foods_edited_record:
        for key, value in {
            "id": id,
            "name": name,
            "macros": macros,
            "calories": calories,
            "is_verified": is_verified,
            "serving_size_g": serving_size_g,
        }.items():
            setattr(foods_edited_record, key, value)

        db.commit()
        db.refresh(foods_edited_record)

        foods_edited_record = (
            foods_edited_record.to_dict()
            if hasattr(foods_edited_record, "to_dict")
            else vars(foods_edited_record)
        )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"foods_edited_record": foods_edited_record},
    }
    return res


async def delete_foods_id(db: Session, id: int):

    query = db.query(models.Foods)
    query = query.filter(and_(models.Foods.id == id))

    record_to_delete = query.first()
    if record_to_delete:
        db.delete(record_to_delete)
        db.commit()
        foods_deleted = record_to_delete.to_dict()
    else:
        foods_deleted = record_to_delete

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"foods_deleted": foods_deleted},
    }
    return res


async def get_mealplans_id(db: Session, id: int):

    query = db.query(models.Mealplans)
    query = query.filter(and_(models.Mealplans.id == id))

    mealplans_one = query.first()

    mealplans_one = (
        (
            mealplans_one.to_dict()
            if hasattr(mealplans_one, "to_dict")
            else vars(mealplans_one)
        )
        if mealplans_one
        else mealplans_one
    )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"mealplans_one": mealplans_one},
    }
    return res


async def post_mealplans(db: Session, raw_data: schemas.PostMealplans):
    user_id: int = raw_data.user_id
    start_date_dt: datetime.date = convert_to_datetime(raw_data.start_date_dt)
    plan_data: str = raw_data.plan_data
    is_active: int = raw_data.is_active
    created_at_dt: str = convert_to_datetime(raw_data.created_at_dt)

    record_to_be_added = {
        "user_id": user_id,
        "is_active": is_active,
        "plan_data": plan_data,
        "created_at_dt": created_at_dt,
        "start_date_dt": start_date_dt,
    }
    new_mealplans = models.Mealplans(**record_to_be_added)
    db.add(new_mealplans)
    db.commit()
    db.refresh(new_mealplans)
    mealplans_inserted_record = new_mealplans.to_dict()

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"mealplans_inserted_record": mealplans_inserted_record},
    }
    return res


async def put_mealplans_id(db: Session, raw_data: schemas.PutMealplansId):
    id: int = raw_data.id
    user_id: int = raw_data.user_id
    start_date_dt: datetime.date = convert_to_datetime(raw_data.start_date_dt)
    plan_data: str = raw_data.plan_data
    is_active: int = raw_data.is_active
    created_at_dt: str = convert_to_datetime(raw_data.created_at_dt)

    query = db.query(models.Mealplans)
    query = query.filter(and_(models.Mealplans.id == id))
    mealplans_edited_record = query.first()

    if mealplans_edited_record:
        for key, value in {
            "id": id,
            "user_id": user_id,
            "is_active": is_active,
            "plan_data": plan_data,
            "created_at_dt": created_at_dt,
            "start_date_dt": start_date_dt,
        }.items():
            setattr(mealplans_edited_record, key, value)

        db.commit()
        db.refresh(mealplans_edited_record)

        mealplans_edited_record = (
            mealplans_edited_record.to_dict()
            if hasattr(mealplans_edited_record, "to_dict")
            else vars(mealplans_edited_record)
        )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"mealplans_edited_record": mealplans_edited_record},
    }
    return res


async def delete_mealplans_id(db: Session, id: int):

    query = db.query(models.Mealplans)
    query = query.filter(and_(models.Mealplans.id == id))

    record_to_delete = query.first()
    if record_to_delete:
        db.delete(record_to_delete)
        db.commit()
        mealplans_deleted = record_to_delete.to_dict()
    else:
        mealplans_deleted = record_to_delete

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"mealplans_deleted": mealplans_deleted},
    }
    return res


async def get_recipes(db: Session):

    query = db.query(models.Recipes)

    recipes_all = query.all()
    recipes_all = (
        [new_data.to_dict() for new_data in recipes_all] if recipes_all else recipes_all
    )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"recipes_all": recipes_all},
    }
    return res


async def get_mealplans(db: Session):

    query = db.query(models.Mealplans)

    mealplans_all = query.all()
    mealplans_all = (
        [new_data.to_dict() for new_data in mealplans_all]
        if mealplans_all
        else mealplans_all
    )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"mealplans_all": mealplans_all},
    }
    return res


async def put_meallogs_id(db: Session, raw_data: schemas.PutMeallogsId):
    id: int = raw_data.id
    user_id: int = raw_data.user_id
    log_date_dt: datetime.date = convert_to_datetime(raw_data.log_date_dt)
    meal_type: str = raw_data.meal_type
    logged_details: str = raw_data.logged_details
    total_calories: int = raw_data.total_calories

    query = db.query(models.Meallogs)
    query = query.filter(and_(models.Meallogs.id == id))
    meallogs_edited_record = query.first()

    if meallogs_edited_record:
        for key, value in {
            "id": id,
            "user_id": user_id,
            "meal_type": meal_type,
            "log_date_dt": log_date_dt,
            "logged_details": logged_details,
            "total_calories": total_calories,
        }.items():
            setattr(meallogs_edited_record, key, value)

        db.commit()
        db.refresh(meallogs_edited_record)

        meallogs_edited_record = (
            meallogs_edited_record.to_dict()
            if hasattr(meallogs_edited_record, "to_dict")
            else vars(meallogs_edited_record)
        )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"meallogs_edited_record": meallogs_edited_record},
    }
    return res


async def delete_meallogs_id(db: Session, id: int):

    query = db.query(models.Meallogs)
    query = query.filter(and_(models.Meallogs.id == id))

    record_to_delete = query.first()
    if record_to_delete:
        db.delete(record_to_delete)
        db.commit()
        meallogs_deleted = record_to_delete.to_dict()
    else:
        meallogs_deleted = record_to_delete

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"meallogs_deleted": meallogs_deleted},
    }
    return res


async def get_recipes_id(db: Session, id: int):

    query = db.query(models.Recipes)
    query = query.filter(and_(models.Recipes.id == id))

    recipes_one = query.first()

    recipes_one = (
        (
            recipes_one.to_dict()
            if hasattr(recipes_one, "to_dict")
            else vars(recipes_one)
        )
        if recipes_one
        else recipes_one
    )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"recipes_one": recipes_one},
    }
    return res


async def post_recipes(db: Session, raw_data: schemas.PostRecipes):
    user_id: int = raw_data.user_id
    title: str = raw_data.title
    instructions: str = raw_data.instructions
    nutritional_data: str = raw_data.nutritional_data
    created_at_dt: str = convert_to_datetime(raw_data.created_at_dt)

    record_to_be_added = {
        "title": title,
        "user_id": user_id,
        "instructions": instructions,
        "created_at_dt": created_at_dt,
        "nutritional_data": nutritional_data,
    }
    new_recipes = models.Recipes(**record_to_be_added)
    db.add(new_recipes)
    db.commit()
    db.refresh(new_recipes)
    recipes_inserted_record = new_recipes.to_dict()

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"recipes_inserted_record": recipes_inserted_record},
    }
    return res


async def put_recipes_id(db: Session, raw_data: schemas.PutRecipesId):
    id: int = raw_data.id
    user_id: int = raw_data.user_id
    title: str = raw_data.title
    instructions: str = raw_data.instructions
    nutritional_data: str = raw_data.nutritional_data
    created_at_dt: str = convert_to_datetime(raw_data.created_at_dt)

    query = db.query(models.Recipes)
    query = query.filter(and_(models.Recipes.id == id))
    recipes_edited_record = query.first()

    if recipes_edited_record:
        for key, value in {
            "id": id,
            "title": title,
            "user_id": user_id,
            "instructions": instructions,
            "created_at_dt": created_at_dt,
            "nutritional_data": nutritional_data,
        }.items():
            setattr(recipes_edited_record, key, value)

        db.commit()
        db.refresh(recipes_edited_record)

        recipes_edited_record = (
            recipes_edited_record.to_dict()
            if hasattr(recipes_edited_record, "to_dict")
            else vars(recipes_edited_record)
        )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"recipes_edited_record": recipes_edited_record},
    }
    return res


async def delete_recipes_id(db: Session, id: int):

    query = db.query(models.Recipes)
    query = query.filter(and_(models.Recipes.id == id))

    record_to_delete = query.first()
    if record_to_delete:
        db.delete(record_to_delete)
        db.commit()
        recipes_deleted = record_to_delete.to_dict()
    else:
        recipes_deleted = record_to_delete

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"recipes_deleted": recipes_deleted},
    }
    return res


async def get_users_id(db: Session, id: int):

    query = db.query(models.Users)
    query = query.filter(and_(models.Users.id == id))

    users_one = query.first()

    users_one = (
        (users_one.to_dict() if hasattr(users_one, "to_dict") else vars(users_one))
        if users_one
        else users_one
    )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"users_one": users_one},
    }
    return res


async def post_users(db: Session, raw_data: schemas.PostUsers):
    email: str = raw_data.email
    password_hash: str = raw_data.password_hash
    target_calories: int = raw_data.target_calories
    dietary_restrictions: str = raw_data.dietary_restrictions
    created_at_dt: str = convert_to_datetime(raw_data.created_at_dt)

    record_to_be_added = {
        "email": email,
        "created_at_dt": created_at_dt,
        "password_hash": password_hash,
        "target_calories": target_calories,
        "dietary_restrictions": dietary_restrictions,
    }
    new_users = models.Users(**record_to_be_added)
    db.add(new_users)
    db.commit()
    db.refresh(new_users)
    users_inserted_record = new_users.to_dict()

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"users_inserted_record": users_inserted_record},
    }
    return res


async def put_users_id(db: Session, raw_data: schemas.PutUsersId):
    id: int = raw_data.id
    email: str = raw_data.email
    password_hash: str = raw_data.password_hash
    target_calories: int = raw_data.target_calories
    dietary_restrictions: str = raw_data.dietary_restrictions
    created_at_dt: str = convert_to_datetime(raw_data.created_at_dt)

    query = db.query(models.Users)
    query = query.filter(and_(models.Users.id == id))
    users_edited_record = query.first()

    if users_edited_record:
        for key, value in {
            "id": id,
            "email": email,
            "created_at_dt": created_at_dt,
            "password_hash": password_hash,
            "target_calories": target_calories,
            "dietary_restrictions": dietary_restrictions,
        }.items():
            setattr(users_edited_record, key, value)

        db.commit()
        db.refresh(users_edited_record)

        users_edited_record = (
            users_edited_record.to_dict()
            if hasattr(users_edited_record, "to_dict")
            else vars(users_edited_record)
        )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"users_edited_record": users_edited_record},
    }
    return res


async def delete_users_id(db: Session, id: int):

    query = db.query(models.Users)
    query = query.filter(and_(models.Users.id == id))

    record_to_delete = query.first()
    if record_to_delete:
        db.delete(record_to_delete)
        db.commit()
        users_deleted = record_to_delete.to_dict()
    else:
        users_deleted = record_to_delete

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"users_deleted": users_deleted},
    }
    return res


async def get_meallogs(db: Session):

    query = db.query(models.Meallogs)

    meallogs_all = query.all()
    meallogs_all = (
        [new_data.to_dict() for new_data in meallogs_all]
        if meallogs_all
        else meallogs_all
    )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"meallogs_all": meallogs_all},
    }
    return res


async def get_users(db: Session):

    query = db.query(models.Users)

    users_all = query.all()
    users_all = (
        [new_data.to_dict() for new_data in users_all] if users_all else users_all
    )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"users_all": users_all},
    }
    return res


async def post_meallogs(db: Session, raw_data: schemas.PostMeallogs):
    user_id: int = raw_data.user_id
    log_date_dt: datetime.date = convert_to_datetime(raw_data.log_date_dt)
    meal_type: str = raw_data.meal_type
    logged_details: str = raw_data.logged_details
    total_calories: int = raw_data.total_calories

    record_to_be_added = {
        "user_id": user_id,
        "meal_type": meal_type,
        "log_date_dt": log_date_dt,
        "logged_details": logged_details,
        "total_calories": total_calories,
    }
    new_meallogs = models.Meallogs(**record_to_be_added)
    db.add(new_meallogs)
    db.commit()
    db.refresh(new_meallogs)
    meallogs_inserted_record = new_meallogs.to_dict()

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"meallogs_inserted_record": meallogs_inserted_record},
    }
    return res
