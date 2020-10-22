from animal_rent_api.apps.user.models import RentUser


def get_admins():
	return RentUser.objects.raw(
		f'''
					SELECT * FROM "apps_rentuser" WHERE 
					("apps_rentuser"."is_staff" = true AND "apps_rentuser"."is_deleted" = False)
				'''
	)
