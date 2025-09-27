from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.cactegory import Category
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError


from ..schemas import category_schema

async def create_category(category: category_schema.CategoryCreate, db: AsyncSession):
    new_category = Category(
        name=category.name,
        description=category.description
    )
    db.add(new_category)
    try:
        await db.commit()
        await db.refresh(new_category)
        return new_category
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Category name already exists")


async def get_category_by_id(category_id: str, db: AsyncSession):
    res = await db.execute(select(Category).where(Category.id == category_id))
    category = res.scalars().first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category
# delete

async def delete_category(
    category_id: str,
    db: AsyncSession
):
   category = await get_category_by_id(category_id, db)
   
   await db.delete(category)
   await db.commit()
   return {"message": "Category deleted successfully"}

# update
async def patch_category(
    category_id: str,
    category: category_schema.CategoryUpdate,
    db: AsyncSession
):
    db_category = await get_category_by_id(category_id,db)

    update_data = category.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_category, key, value)
    
    await db.commit()
    await db.refresh(db_category)
    return db_category
    
async def get_categories(
    db: AsyncSession
):
    res = await db.execute(select(Category))
    
    categories = res.scalars().all()
    return categories