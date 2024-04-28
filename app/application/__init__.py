from functools import wraps

from di import DIContainer

from .unit_of_work import UnitOfWork
from .application_service_life_cycle import ApplicationServiceLifeCycle


def transactional(method, is_listening: bool = True):
    @wraps(method)
    def handle_transaction(*args, **kwargs):
        application_life_cycle = DIContainer.instance().resolve(
            ApplicationServiceLifeCycle
        )

        try:
            application_life_cycle.begin(is_listening)
            _return = method(*args, **kwargs)
            application_life_cycle.success()
            return _return
        except Exception as e:
            application_life_cycle.fail(e)

    return handle_transaction
