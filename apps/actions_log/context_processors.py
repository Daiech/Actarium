from .models import UserNotification
from actarium_apps.task_manager.models import UserTasks
from django.utils.translation import ugettext as _

def my_notifications(request):
	summary_list=list()
	summary_quantity = 0
	if request.user.is_authenticated():
		notifications = UserNotification.objects.filter(user=request.user).order_by('-created')[0:5]
		notifications_not_viewed = UserNotification.objects.filter(id__in=notifications,viewed=False).count()
		usertasks = UserTasks.objects.get_pending_tasks_by_user(request.user)
		summary_list.append({
			"glyphicon":"glyphicon glyphicon-edit",
			"title":_(u"Tareas pendientes"),
			"quantity":usertasks.count() 
		})
		summary_quantity += usertasks.count()
	else:
		notifications = None
		notifications_not_viewed = 0

	response = {
		"NOTIFICATIONS": notifications,
		"NOTIFICATIONS_NOT_VIEWED":notifications_not_viewed,
		"SUMMARY_QUANTITY":summary_quantity,
		"SUMMARY_LIST":summary_list
	}

	return response

