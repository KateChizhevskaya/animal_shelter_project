from django.urls import path
from animal_rent_api.apps.user.views import UpdateUser, UserListView, ChangeUserBlockedStatusView

urlpatterns = [
	path('', UserListView.as_view(), name='user_list'),
	path('change_blocked_status/<int:id>/', ChangeUserBlockedStatusView.as_view(), name='change_blocked_status'),
	path('update/', UpdateUser.as_view(), name='update_user'),
]
