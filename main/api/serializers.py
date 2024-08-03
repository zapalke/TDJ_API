from rest_framework import serializers

class InputDataSerializer(serializers.Serializer):
    num = serializers.IntegerField()
    text = serializers.CharField()