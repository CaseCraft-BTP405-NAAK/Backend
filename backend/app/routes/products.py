from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.product import Product
from app.models.user import User
from app.schemas.product import Product as ProductSchema, ProductCreate, ProductUpdate
from app.auth.jwt import get_current_active_user

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=List[ProductSchema])
def get_products(
    skip: int = 0, 
    limit: int = 100,
    category: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: Optional[str] = "id",
    sort_order: Optional[str] = "asc",
    db: Session = Depends(get_db)
) -> Any:
    """
    Retrieve products with filtering, searching, and sorting options.
    
    Args:
        skip: Number of records to skip for pagination
        limit: Maximum number of records to return
        category: Filter products by category
        search: Search term to filter products by name or description
        sort_by: Field to sort results by (id, name, price)
        sort_order: Sort order (asc or desc)
        db: Database session dependency
        
    Returns:
        List of products matching the criteria
    """
    query = db.query(Product)
    
    # Apply category filter if provided
    if category:
        query = query.filter(Product.category == category)
    
    # Apply search filter if provided
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Product.name.ilike(search_term)) | 
            (Product.description.ilike(search_term))
        )
    
    # Apply sorting
    if sort_by not in ["id", "name", "price", "created_at"]:
        sort_by = "id"  # Default sort field
    
    sort_field = getattr(Product, sort_by)
    if sort_order.lower() == "desc":
        sort_field = sort_field.desc()
    else:
        sort_field = sort_field.asc()
    
    query = query.order_by(sort_field)
    
    # Apply pagination
    products = query.offset(skip).limit(limit).all()
    return products

@router.post("/", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
def create_product(
    product_in: ProductCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Create new product. Only admin users can create products.
    
    Args:
        product_in: Product data to create
        db: Database session dependency
        current_user: Current authenticated user
        
    Returns:
        The newly created product
        
    Raises:
        HTTPException: If user doesn't have admin privileges
    """
    # Check if user is admin
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can perform this action",
            headers={"X-Error": "ADMIN_REQUIRED"}
        )
    
    product = Product(
        name=product_in.name,
        description=product_in.description,
        price=product_in.price,
        stock=product_in.stock,
        image_url=product_in.image_url,
        category=product_in.category,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.get("/{product_id}", response_model=ProductSchema)
def get_product(product_id: int, db: Session = Depends(get_db)) -> Any:
    """
    Get product by ID.
    
    Args:
        product_id: ID of the product to retrieve
        db: Database session dependency
        
    Returns:
        Product with the specified ID
        
    Raises:
        HTTPException: If product with given ID is not found
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product

@router.put("/{product_id}", response_model=ProductSchema)
def update_product(
    product_id: int,
    product_in: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Update a product.
    
    Args:
        product_id: ID of the product to update
        product_in: Product data to update
        db: Database session dependency
        current_user: Current authenticated user
        
    Returns:
        The updated product
        
    Raises:
        HTTPException: If user doesn't have admin privileges or product not found
    """
    # Check if user is admin
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can perform this action",
            headers={"X-Error": "ADMIN_REQUIRED"}
        )
    
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    update_data = product_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.delete("/{product_id}", response_model=ProductSchema)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Delete a product.
    
    Args:
        product_id: ID of the product to delete
        db: Database session dependency
        current_user: Current authenticated user
        
    Returns:
        The deleted product
        
    Raises:
        HTTPException: If user doesn't have admin privileges or product not found
    """
    # Check if user is admin
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can perform this action",
            headers={"X-Error": "ADMIN_REQUIRED"}
        )
    
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    db.delete(product)
    db.commit()
    return product 