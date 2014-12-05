from .models import UserNotification
def my_notifications(request):
	if request.user.is_authenticated():
		notifications = UserNotification.objects.filter(user=request.user).order_by('-created')[0:5]
		notifications_not_viewed = UserNotification.objects.filter(id__in=notifications,viewed=False).count()
	else:
		notifications = None
		notifications_not_viewed = 0
	return {"NOTIFICATIONS": notifications,"NOTIFICATIONS_NOT_VIEWED":notifications_not_viewed}

