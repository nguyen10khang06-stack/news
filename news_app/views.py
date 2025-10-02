from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import News, Category
from .forms import NewsForm
from django.utils.text import slugify  # <--- ĐÃ THÊM DÒNG NÀY


# ---------------------------
# Trang chủ
# ---------------------------
def index(request):
    top_news = News.objects.order_by("-created_at")[:2]  # 2 tin nổi bật
    latest_news = News.objects.order_by("-created_at")[:6]  # 6 tin mới
    popular_news = News.objects.order_by("-views")[:6]  # 6 tin nhiều view
    categories = Category.objects.all()

    context = {
        "top_news": top_news,
        "latest_news": latest_news,
        "popular_news": popular_news,
        "categories": categories,
    }
    return render(request, "news_app/index.html", context)


# ---------------------------
# Chi tiết tin
# ---------------------------
def news_detail(request, news_id):
    news = get_object_or_404(News, id=news_id)
    news.views += 1  # tăng lượt xem
    news.save()
    return render(request, "news_app/news_detail.html", {"news": news})


# ---------------------------
# Trang category (sports, tech, fashion)
# ---------------------------
def category_page(request, category_name):
    category = Category.objects.filter(name=category_name).first()

    top_item = None
    quick_items = []
    other_items = []

    if category:
        top_item = News.objects.filter(category=category).order_by('-created_at').first()
        if top_item:  # chỉ lấy news khác nếu top_item tồn tại
            quick_items = News.objects.filter(category=category).exclude(id=top_item.id).order_by('-created_at')[:3]
            other_items = News.objects.filter(category=category).exclude(
                id__in=[top_item.id] + [n.id for n in quick_items]).order_by('-created_at')

    # Map biến theo category để template khớp
    context = {'category_name': category_name}
    if category_name == 'tech':
        context['top_tech'] = top_item
        context['quick_tech'] = quick_items
        context['other_tech'] = other_items
    elif category_name == 'sports':
        context['top_sport'] = top_item
        context['quick_sports'] = quick_items
        context['other_sports'] = other_items
    elif category_name == 'fashion':
        context['top_fashion'] = top_item
        context['quick_fashion'] = quick_items
        context['other_fashion'] = other_items

    template_map = {
        'sports': 'news_app/sports.html',
        'tech': 'news_app/tech.html',
        'fashion': 'news_app/fashion.html'
    }

    return render(request, template_map.get(category_name, "news_app/index.html"), context)


# ---------------------------
# Chức năng chỉnh sửa tin tức (ĐÃ SỬA SLUG)
# ---------------------------
def edit_news(request, news_id):
    news = get_object_or_404(News, id=news_id)

    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            # Lấy đối tượng nhưng CHƯA LƯU
            news_instance = form.save(commit=False)

            # TỰ ĐỘNG CẬP NHẬT SLUG khi tiêu đề thay đổi
            news_instance.slug = slugify(news_instance.title)

            # Lưu vào database
            news_instance.save()

            return redirect('news_detail', news_id=news_instance.id)
    else:
        form = NewsForm(instance=news)

    return render(request, 'news_app/edit_news.html', {'form': form, 'news': news})


# ---------------------------
# Chức năng Thêm tin tức mới (ĐÃ SỬA SLUG)
# ---------------------------
def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            # Lấy đối tượng nhưng CHƯA LƯU
            news_instance = form.save(commit=False)

            # TỰ ĐỘNG TẠO SLUG
            news_instance.slug = slugify(news_instance.title)

            # Lưu vào database
            news_instance.save()

            return redirect('news_detail', news_id=news_instance.id)
    else:
        form = NewsForm()

    return render(request, 'news_app/add_news.html', {'form': form})


# ---------------------------
# Trang Contact
# ---------------------------
def contact(request):
    success_message = None

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        try:
            send_mail(
                subject=f"{subject} từ {name}",
                message=message,
                from_email=email,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            success_message = "Cảm ơn bạn! Tin nhắn của bạn đã được gửi."
        except Exception as e:
            success_message = f"Đã xảy ra lỗi: {e}"

    return render(request, "news_app/contact.html", {"success_message": success_message})