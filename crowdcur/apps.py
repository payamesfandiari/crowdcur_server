from django.apps import AppConfig


class CrowdcurConfig(AppConfig):
    name = 'crowdcur'

    def ready(self):
        import crowdcur.signals
