from rest_framework_mongoengine import routers as mongorouters
from apps.appname.views import *
 
mongorouter = mongorouters.DefaultRouter()
mongorouter.register(r'page', PageViewSet)
mongorouter.register(r'element', ElementViewSet)
mongorouter.register(r'elementtype', ElementTypeViewSet)
mongorouter.register(r'locator', LocatorViewSet)
mongorouter.register(r'action', ActionViewSet)
mongorouter.register(r'testcase', TestCaseViewSet)
mongorouter.register(r'component', ComponentViewSet)
mongorouter.register(r'step', StepViewSet)

urlpatterns = [
 
]
 
urlpatterns += mongorouter.urls