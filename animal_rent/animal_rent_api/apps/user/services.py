from animal_rent_api.apps.user.models import RentUser


def get_admins():
	return RentUser.objects.filter(is_staff=True, is_deleted=False)