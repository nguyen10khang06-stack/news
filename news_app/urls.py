from django.urls import path
from . import views

urlpatterns = [
    # 1. Trang chủ và Contact
    path("", views.index, name="index"),
    path("contact/", views.contact, name="contact"),

    # --- CHỨC NĂNG THÊM & SỬA (Nên đặt trước chi tiết tin) ---
    # Thêm tin tức mới (URL cố định)
    path("news/add/", views.add_news, name="add_news"),

    # Chỉnh sửa tin tức (URL động)
    path("news/<int:news_id>/edit/", views.edit_news, name="edit_news"),

    # 2. Chi tiết tin (URL động, phải đặt sau các URL cụ thể hơn)
    # Loại bỏ URL trùng lặp: path('news/<int:news_id>/', views.news_detail, name='news_detail'),
    path("news/<int:news_id>/", views.news_detail, name="news_detail"),

    # 3. Các Category cố định (Đặt trước category động)
    path("sports/", lambda request: views.category_page(request, "sports"), name="sports"),
    path("tech/", lambda request: views.category_page(request, "tech"), name="tech"),
    path("fashion/", lambda request: views.category_page(request, "fashion"), name="fashion"),

    # 4. Category chung (URL bắt bất kỳ chuỗi nào)
    path('<str:category_name>/', views.category_page, name='category_page'),
]