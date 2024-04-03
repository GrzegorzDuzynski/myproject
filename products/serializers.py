from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from products.models import (
    Type,
    NewUser,
    Section,
    Status,
    Product
)


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = "__all__"


class NewUserDetailSerializer(serializers.ModelSerializer):
    serializer_related_field = serializers.PrimaryKeyRelatedField

    class Meta:
        model = NewUser
        fields = ["id", "type"]
        depth = 2


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = "__all__"


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        depth = 2


class JWTSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["user"] = {
            "id": user.id,
            "type": user.type

        }

        return token