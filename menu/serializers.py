from .models import MenuItem
from rest_framework import serializers

class MenuSerializers(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = "__all__"