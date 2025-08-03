from household_chemicals.models import ChemicalProduct

def get_product_by_id(product_id: int) -> ChemicalProduct:
    return ChemicalProduct.objects.get(id=product_id)
