from django import template
from django.db.models import Count, F
from news.models import Category
register = template.Library()


# @register.simple_tag()
# def get_categories():
#     return Category.objects.raw("SELECT * FROM news_category")
#     # return Category.objects.all()





@register.inclusion_tag('news/list_category.html')
def show_category():
    # categories = Category.objects.all()
    # categories = Category.objects.annotate(count=Count('news', filter=F('news__is_published'))).filter(count__gt=0)
    categories = Category.objects.raw("SELECT news_category.id, news_category.title, COUNT(news_news.id) AS count "
                                      "FROM news_category "
                                      "LEFT JOIN news_news ON news_news.category_id = news_category.id "
                                      "WHERE is_published != false "
                                      "GROUP BY (news_category.id) "
                                      "HAVING COUNT(news_news.id) > 0 "
                                      "ORDER BY news_category.id DESC"
                                      )
    return {'categories': categories}
