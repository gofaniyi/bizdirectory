from django.urls import path

from . import views

urlpatterns = [
    path('view-listing/<int:id>/',
         views.view_listing, name='view-listing'),
    path('search/', views.search, name='search'),
    path('post-add-lisiting', views.post_add_listing, name='post-add-listing'),
    path('post-add-category', views.post_add_category, name='post-add-category'),
    path('listings/', views.all_listings, name='listings'),
    path('home/', views.home, name='home'),
    path('edit-listing/<int:id>/',
         views.edit_listing, name='edit-listing'),
    path('delete-listing/<int:id>/',
         views.delete_listing, name='delete-listing'),
    path('deactivate-listing/<int:id>/',
         views.deactivate_listing, name='deactivate-listing'),
    path('activate-listing/<int:id>/',
         views.activate_listing, name='activate-listing'),
    path('categories/', views.all_categories, name='categories'),
    path('add-listing/', views.add_listing, name='add-listing'),
    path('add-category/', views.add_category, name='add-category')
]
