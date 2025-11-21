from django.contrib import admin
from .models import News, Category

# ---------------------------
# Category admin
# ---------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")   # cột hiển thị
    search_fields = ("name",)               # tìm kiếm
    prepopulated_fields = {"slug": ("name",)}  # tự động tạo slug từ name
    list_per_page = 20                       # phân trang


# ---------------------------
# News admin
# ---------------------------
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    # ĐÃ THÊM "image" VÀO list_display
    list_display = ("id", "title", "category", "image", "created_at", "views", "is_published")
    list_filter = ("category", "created_at", "is_published")  # lọc bên phải
    search_fields = ("title", "content")                      # tìm kiếm
    prepopulated_fields = {"slug": ("title",)}               # tự tạo slug
    list_editable = ("is_published",)                        # chỉnh trực tiếp trong danh sách
    ordering = ("-created_at",)                              # sắp xếp theo ngày mới nhất
    list_per_page = 20