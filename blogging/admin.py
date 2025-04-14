# from django.contrib import admin

# Register your models here.
from blogging.models import Post, Category

# and a new admin registration
# admin.site.register(Post)
# admin.site.register(Category)


from django.contrib import admin
from .models import Post, Category


class CategoryInline(admin.TabularInline):
    model = Post.categories.through


class PostAdmin(admin.ModelAdmin):
    inlines = [
        CategoryInline,
    ]
    exclude = ("categories",)


class CategoryAdmin(admin.ModelAdmin):
    exclude = ("posts",)


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
