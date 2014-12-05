#encoding:utf-8
from django.utils.translation import ugettext_lazy as _

CHOICE_TYPE_NOTIFICATION = (
    (_(u'Tareas'),(
            ('NEW_TASK',_(u'Nueva tarea')),
        )
    ),
    (_(u'Actas'),(
            ('NEW_MINUTES',_(u'Nueva acta creada')),
            ('APPROVAL_NEED',_(u'Esta acta necesita tu aprobacion'))
        )
    )
)