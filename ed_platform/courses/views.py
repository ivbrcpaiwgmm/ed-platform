from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .models import Product, Lesson
from .utils.access_checker import has_access


def product_list(request):
    products = Product.objects.annotate(lesson_count=Count('lesson'))
    data = [
        {
            'id': product.id,
            'name': product.name,
            'start_datetime': product.start_datetime,
            'price': product.price,
            'lesson_count': product.lesson_count
        }
        for product in products
    ]
    return JsonResponse(data, safe=False)


def lessons_by_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if not has_access(request.user, product):
        return JsonResponse({"error": "Access denied"}, status=403)

    lessons = Lesson.objects.filter(product=product)

    lessons_data = []
    for lesson in lessons:
        lesson_data = {
            'id': lesson.id,
            'name': lesson.name,
            'video_url': lesson.video_url,
        }
        lessons_data.append(lesson_data)
    return JsonResponse(lessons_data, safe=False)
