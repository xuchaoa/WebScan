from rest_framework_mongoengine import serializers
from apps.appname.models import *


class PageSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Page
        fields = '__all__'


class ElementSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Element
        fields = '__all__'


class ElementTypeSerializer(serializers.DocumentSerializer):
    class Meta:
        model = ElementType
        fields = '__all__'


class LocatorSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Locator
        fields = '__all__'


class ActionSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Action
        fields = '__all__'


class TestCaseSerializer(serializers.DocumentSerializer):
    class Meta:
        model = TestCase
        fields = '__all__'


class ComponentSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Component
        fields = '__all__'


class StepSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Step
        fields = '__all__'