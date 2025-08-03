"""
Service functions for working with database.
"""

from household_chemicals.models import ChemicalProduct


def get_product_by_id(product_id: int) -> ChemicalProduct:
    """
    Get product by its ID.

    Args:
        product_id: ID of the product.
    Returns:
        ChemicalProduct: ChemicalProduct object with specified ID.
    """
    return ChemicalProduct.objects.get(id=product_id)
