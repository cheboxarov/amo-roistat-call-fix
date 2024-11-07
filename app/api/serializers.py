from rest_framework import serializers


class AuthParamsSerializer(serializers.Serializer):

    code = serializers.CharField()
    client_id = serializers.CharField()
    referer = serializers.CharField()
    