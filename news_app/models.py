from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    # Thêm slug nếu muốn dùng prepopulated_fields
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.name


class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    # ĐÃ THÊM: Trường hình ảnh, lưu vào thư mục 'news_images/' trong MEDIA_ROOT
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    # Thêm slug nếu muốn dùng prepopulated_fields
    slug = models.SlugField(unique=True, blank=True, null=True)
    # Thêm is_published nếu muốn bật tắt hiển thị
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title