from django.contrib import admin
from apps.board.models import Category, Subcategory, Post, Comment, Shout


class SubcategoryInline(admin.TabularInline):
    model = Subcategory
    ordering = ('order', )


class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        SubcategoryInline,
    ]
    list_display = ('name', 'order', )
    ordering = ('order', )


class CommentInline(admin.TabularInline):
    model = Comment
    ordering = ('created', )


class PostAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline
    ]
    list_display = ('title', 'category', 'user')
    ordering = ('title', )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Shout)
