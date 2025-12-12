from pydantic import BaseModel,Field,field_validator

import datetime

import uuid

from typing import Any, Dict, List,Optional,Tuple

import re

class Users(BaseModel):
    email: Optional[str]=None
    password_hash: Optional[str]=None
    target_calories: Optional[int]=None
    dietary_restrictions: Optional[str]=None
    created_at_dt: Optional[Any]=None


class ReadUsers(BaseModel):
    email: Optional[str]=None
    password_hash: Optional[str]=None
    target_calories: Optional[int]=None
    dietary_restrictions: Optional[str]=None
    created_at_dt: Optional[Any]=None
    class Config:
        from_attributes = True


class Recipes(BaseModel):
    user_id: Optional[int]=None
    title: Optional[str]=None
    instructions: Optional[str]=None
    nutritional_data: Optional[str]=None
    created_at_dt: Optional[Any]=None


class ReadRecipes(BaseModel):
    user_id: Optional[int]=None
    title: Optional[str]=None
    instructions: Optional[str]=None
    nutritional_data: Optional[str]=None
    created_at_dt: Optional[Any]=None
    class Config:
        from_attributes = True


class Foods(BaseModel):
    name: Optional[str]=None
    serving_size_g: Optional[float]=None
    calories: Optional[int]=None
    macros: Optional[str]=None
    is_verified: Optional[int]=None


class ReadFoods(BaseModel):
    name: Optional[str]=None
    serving_size_g: Optional[float]=None
    calories: Optional[int]=None
    macros: Optional[str]=None
    is_verified: Optional[int]=None
    class Config:
        from_attributes = True


class Meallogs(BaseModel):
    user_id: Optional[int]=None
    log_date_dt: Optional[datetime.date]=None
    meal_type: Optional[str]=None
    logged_details: Optional[str]=None
    total_calories: Optional[int]=None


class ReadMeallogs(BaseModel):
    user_id: Optional[int]=None
    log_date_dt: Optional[datetime.date]=None
    meal_type: Optional[str]=None
    logged_details: Optional[str]=None
    total_calories: Optional[int]=None
    class Config:
        from_attributes = True


class Mealplans(BaseModel):
    user_id: Optional[int]=None
    start_date_dt: Optional[datetime.date]=None
    plan_data: Optional[str]=None
    is_active: Optional[int]=None
    created_at_dt: Optional[Any]=None


class ReadMealplans(BaseModel):
    user_id: Optional[int]=None
    start_date_dt: Optional[datetime.date]=None
    plan_data: Optional[str]=None
    is_active: Optional[int]=None
    created_at_dt: Optional[Any]=None
    class Config:
        from_attributes = True




class PostFoods(BaseModel):
    name: Optional[str]=None
    serving_size_g: Optional[Any]=None
    calories: Optional[int]=None
    macros: Optional[str]=None
    is_verified: Optional[int]=None

    class Config:
        from_attributes = True



class PutFoodsId(BaseModel):
    id: int = Field(...)
    name: Optional[str]=None
    serving_size_g: Optional[Any]=None
    calories: Optional[int]=None
    macros: Optional[str]=None
    is_verified: Optional[int]=None

    class Config:
        from_attributes = True



class PostMealplans(BaseModel):
    user_id: Optional[int]=None
    start_date_dt: Optional[Any]=None
    plan_data: Optional[str]=None
    is_active: Optional[int]=None
    created_at_dt: Optional[str]=None

    class Config:
        from_attributes = True



class PutMealplansId(BaseModel):
    id: int = Field(...)
    user_id: Optional[int]=None
    start_date_dt: Optional[Any]=None
    plan_data: Optional[str]=None
    is_active: Optional[int]=None
    created_at_dt: Optional[str]=None

    class Config:
        from_attributes = True



class PutMeallogsId(BaseModel):
    id: int = Field(...)
    user_id: Optional[int]=None
    log_date_dt: Optional[Any]=None
    meal_type: Optional[str]=None
    logged_details: Optional[str]=None
    total_calories: Optional[int]=None

    class Config:
        from_attributes = True



class PostRecipes(BaseModel):
    user_id: Optional[int]=None
    title: Optional[str]=None
    instructions: Optional[str]=None
    nutritional_data: Optional[str]=None
    created_at_dt: Optional[str]=None

    class Config:
        from_attributes = True



class PutRecipesId(BaseModel):
    id: int = Field(...)
    user_id: Optional[int]=None
    title: Optional[str]=None
    instructions: Optional[str]=None
    nutritional_data: Optional[str]=None
    created_at_dt: Optional[str]=None

    class Config:
        from_attributes = True



class PostUsers(BaseModel):
    email: Optional[str]=None
    password_hash: Optional[str]=None
    target_calories: Optional[int]=None
    dietary_restrictions: Optional[str]=None
    created_at_dt: Optional[str]=None

    class Config:
        from_attributes = True



class PutUsersId(BaseModel):
    id: int = Field(...)
    email: Optional[str]=None
    password_hash: Optional[str]=None
    target_calories: Optional[int]=None
    dietary_restrictions: Optional[str]=None
    created_at_dt: Optional[str]=None

    class Config:
        from_attributes = True



class PostMeallogs(BaseModel):
    user_id: Optional[int]=None
    log_date_dt: Optional[Any]=None
    meal_type: Optional[str]=None
    logged_details: Optional[str]=None
    total_calories: Optional[int]=None

    class Config:
        from_attributes = True



# Query Parameter Validation Schemas

class GetFoodsIdQueryParams(BaseModel):
    """Query parameter validation for get_foods_id"""
    id: int = Field(..., ge=1, description="Id")

    class Config:
        populate_by_name = True


class GetMeallogsIdQueryParams(BaseModel):
    """Query parameter validation for get_meallogs_id"""
    id: int = Field(..., ge=1, description="Id")

    class Config:
        populate_by_name = True


class DeleteFoodsIdQueryParams(BaseModel):
    """Query parameter validation for delete_foods_id"""
    id: int = Field(..., ge=1, description="Id")

    class Config:
        populate_by_name = True


class GetMealplansIdQueryParams(BaseModel):
    """Query parameter validation for get_mealplans_id"""
    id: int = Field(..., ge=1, description="Id")

    class Config:
        populate_by_name = True


class DeleteMealplansIdQueryParams(BaseModel):
    """Query parameter validation for delete_mealplans_id"""
    id: int = Field(..., ge=1, description="Id")

    class Config:
        populate_by_name = True


class DeleteMeallogsIdQueryParams(BaseModel):
    """Query parameter validation for delete_meallogs_id"""
    id: int = Field(..., ge=1, description="Id")

    class Config:
        populate_by_name = True


class GetRecipesIdQueryParams(BaseModel):
    """Query parameter validation for get_recipes_id"""
    id: int = Field(..., ge=1, description="Id")

    class Config:
        populate_by_name = True


class DeleteRecipesIdQueryParams(BaseModel):
    """Query parameter validation for delete_recipes_id"""
    id: int = Field(..., ge=1, description="Id")

    class Config:
        populate_by_name = True


class GetUsersIdQueryParams(BaseModel):
    """Query parameter validation for get_users_id"""
    id: int = Field(..., ge=1, description="Id")

    class Config:
        populate_by_name = True


class DeleteUsersIdQueryParams(BaseModel):
    """Query parameter validation for delete_users_id"""
    id: int = Field(..., ge=1, description="Id")

    class Config:
        populate_by_name = True
