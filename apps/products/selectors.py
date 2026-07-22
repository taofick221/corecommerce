from django.core.cache import cache

from .models import Brand, Category

CATEGORY_CACHE_KEY = "categories:list"


def get_categories():
    categories = cache.get(CATEGORY_CACHE_KEY)

    if categories is None:
        categories = list(Category.objects.select_related("parent").all())
        cache.set(
            CATEGORY_CACHE_KEY,
            categories,
            timeout=60 * 60,
        )

    return categories


BRAND_CACHE_KEY = "brands:list"


def get_brands():

    brands = cache.get(BRAND_CACHE_KEY)

    if brands is None:

        brands = list(Brand.objects.all())

        cache.set(
            BRAND_CACHE_KEY,
            brands,
            timeout=60 * 60,
        )

    return brands
