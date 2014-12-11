from .models import UserNotification
from actarium_apps.task_manager.models import UserTasks
from apps.groups_app.models import rel_user_minutes_signed
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

def my_notifications(request):
	summary_list=list()
	summary_quantity = 0
	if request.user.is_authenticated():
		notifications = UserNotification.objects.filter(user=request.user).order_by('-created')[0:5]
		notifications_not_viewed = UserNotification.objects.filter(id__in=notifications,viewed=False).count()

		# TASKS
		usertasks = UserTasks.objects.get_pending_tasks_by_user(request.user)
		summary_list.append({
			"glyphicon":"glyphicon glyphicon-edit",
			"title":_(u"Tareas pendientes"),
			"quantity":usertasks.count(),
			"url":reverse('list_pending_tasks'),
			"id": 'list_pending_tasks'
		})
		summary_quantity += usertasks.count()

		# APPROVAL OF MINUTES
		rel_user_minutes = rel_user_minutes_signed.objects.filter(id_user = request.user, is_signed_approved=0).order_by('-date_joined')
		summary_list.append({
			"glyphicon":"glyphicon glyphicon-ok-sign",
			"title":_(u"Actas por aprobar"),
			"quantity":rel_user_minutes.count(),
			"url":reverse('list_pending_approval_of_minutes'),
			"id": 'list_pending_approval_of_minutes'
		})
		summary_quantity += rel_user_minutes.count()


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

