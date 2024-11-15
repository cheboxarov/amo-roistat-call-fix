from rest_framework import serializers


class AuthParamsSerializer(serializers.Serializer):

    code = serializers.CharField()
    client_id = serializers.CharField()
    referer = serializers.CharField()


class LeadEventSerializer(serializers.Serializer):

    subdomain = serializers.CharField(source="account[subdomain][0]")