from .models import News, Category
from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = News
        fields = '__all__'

class NewsAdmin(admin.ModelAdmin):
    form = PostAdminForm
    description = '-empty-'
    list_display = ('id', 'title', 'category', 'created_at', 'update_at', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('pk', 'title')
    list_editable = ('is_published',)
    save_as = True
    list_filter = ('is_published', 'category')

class CategoryAdmin(admin.ModelAdmin):
    description = '-empty-'
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('pk', 'title')


admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)
