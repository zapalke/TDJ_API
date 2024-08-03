from rest_framework import serializers


class StrictCharField(serializers.CharField):
    """
    Custom char field serializer that positively validates only data that is 
    already type string instead of validating all data that can be saved as string.
    """
    def to_internal_value(self, data):
        if not isinstance(data, str):
            raise serializers.ValidationError("This field must be a string.")
        return super().to_internal_value(data)
    
class InputDataSerializer(serializers.Serializer):
    num = serializers.IntegerField()
    text = StrictCharField()