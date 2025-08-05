"""
Service functions for working with database.
"""
from django.shortcuts import get_object_or_404
from household_chemicals.models import ChemicalProduct


def get_product_by_id(product_id: int) -> ChemicalProduct:
    """
    Get product by its ID.

    Args:
        product_id: ID of the product.
    Returns:
        ChemicalProduct: ChemicalProduct object with specified ID.
    """
    return get_object_or_404(ChemicalProduct, id=product_id)
