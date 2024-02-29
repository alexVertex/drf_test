import io

from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .models import Car, Country, Manufacture, Commentary


class CountrySerializer(serializers.ModelSerializer):
    manufactures = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Country
        fields = ('name', 'manufactures')


class ManufactureCarSerializer(serializers.ModelSerializer):
    commentsCount = serializers.IntegerField(source='commentarys.count')

    class Meta:
        model = Car
        fields = ('name', 'commentsCount')


class ManufactureSerializer(serializers.ModelSerializer):
    countryName = serializers.StringRelatedField(source='country')
    cars = ManufactureCarSerializer(many=True, read_only=True)

    class Meta:
        model = Manufacture
        fields = ('name', 'country', 'countryName', 'cars')


class CommentarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentary
        fields = ('email', 'car', 'date', 'commentaryData')


class CarCommentarySerializer(serializers.ModelSerializer):
    car = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Commentary
        fields = ('email', 'car', 'date', 'commentaryData')


class CarSerializer(serializers.ModelSerializer):
    manufactureName = serializers.StringRelatedField(source='manufacture')
    commentarys = CarCommentarySerializer(many=True, read_only=True)
    commentsCount = serializers.IntegerField(source='commentarys.count', read_only=True)

    class Meta:
        model = Car
        fields = ('name', 'manufacture', 'manufactureName', "dateStartProduce", "dateStopProduce", 'commentsCount',
                  'commentarys')

    def validate(self, data):
        if data['dateStartProduce'] > data['dateStopProduce']:
            raise serializers.ValidationError("Конец производства до его начала")
        return data

# name = serializers.CharField(max_length=100)
# manufacture = serializers.CharField(max_length=100)
# dateStartProduce = serializers.DateField()
# dateStopProduce = serializers.DateField()
#
# def create(self, validated_data):
#    return Car.objects.create(**validated_data)
#
# def update(self, instance, validated_data):
#    instance.name = validated_data.get('name', instance.name)
#    instance.manufacture = validated_data.get('manufacture', instance.manufacture)
#    instance.dateStartProduce = validated_data.get('dateStartProduce', instance.dateStartProduce)
#    instance.dateStopProduce = validated_data.get('dateStopProduce', instance.dateStopProduce)
#    instance.save()
#    return instance
