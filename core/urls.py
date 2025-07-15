from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('simple_mark/', views.simple_mark, name='simple_mark'),
    path('', views.group_list, name='group_list'),
    path('group/create/', views.group_create, name='group_create'),
    path('group/<int:group_id>/', views.group_detail, name='group_detail'),
    path('group/<int:group_id>/add-member/', views.add_member, name='add_member'),
    path('group/<int:group_id>/assess/<int:assessor_id>/<int:question_id>/', views.assessment_page, name='assessment_page'),
    path('add-question/', views.add_question, name='add_question'),
    path('group/<int:group_id>/results/', views.group_results, name='group_results'),
    path('group/<int:group_id>/member/<int:member_id>/edit/', views.edit_member, name='edit_member'),
    path('group/<int:group_id>/member/<int:member_id>/delete/', views.delete_member, name='delete_member'),
    path('group/<int:group_id>/delete/', views.delete_group, name='delete_group'),
    path('group/<int:group_id>/edit/', views.edit_group, name="edit_group"),

]
