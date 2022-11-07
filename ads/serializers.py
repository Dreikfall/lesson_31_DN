from rest_framework import serializers

from ads.models import Ad, Selection, Category
from users.models import User


# Валидатор
def is_published_validator(value):
    if value:
        raise serializers.ValidationError('is published cannot be True')
    return value


class AdSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        #read_only=True,
        queryset=Category.objects.all(),
        slug_field='name'
    )
    author = serializers.SlugRelatedField(
        #read_only=True,
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        model = Ad
        fields = '__all__'


class AdCreateSerializer(serializers.ModelSerializer):
    is_published = serializers.BooleanField(validators=[is_published_validator],
                                            required=False)

    class Meta:
        model = Ad
        fields = '__all__'


class SelectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = ['id', 'name']


class SelectionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = '__all__'

    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    items = serializers.SlugRelatedField(
        read_only=True,
        many=True,
        slug_field='name'
    )


class SelectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = '__all__'
        optional_fields = ['owner']







