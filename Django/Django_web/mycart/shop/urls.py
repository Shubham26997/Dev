from django.urls import path
from shop.views import index, about, contact, prodview, search, tracker
urlpatterns = [
    path ("", view=index, name="ShopHome"),
    path ("about/", view=about, name="ShopAbout"),
    path ("contact/<str:details>", view=contact, name="ShopContact"), #this is str path convertor which is giving only str data type to the url else not found 404
    path ("prodview/", view=prodview, name="ShopView"),
    path ("search/", view=search, name="ShopSearch"),
    path ("tracker/", view=tracker, name="ShopTracker"),
]