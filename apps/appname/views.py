from rest_framework_mongoengine import viewsets as mongoviewsets
from apps.appname.serializers import *
from apps.appname.models import *


class PageViewSet(mongoviewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = Page.objects.all()
    serializer_class = PageSerializer


class ElementViewSet(mongoviewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = Element.objects.all()
    serializer_class = ElementSerializer


class ElementTypeViewSet(mongoviewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = ElementType.objects.all()
    serializer_class = ElementTypeSerializer


class LocatorViewSet(mongoviewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = Locator.objects.all()
    serializer_class = LocatorSerializer


class ActionViewSet(mongoviewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = Action.objects.all()
    serializer_class = ActionSerializer


class TestCaseViewSet(mongoviewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = TestCase.objects.all()
    serializer_class = TestCaseSerializer


class ComponentViewSet(mongoviewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer


class StepViewSet(mongoviewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = Step.objects.all()
    serializer_class = StepSerializer