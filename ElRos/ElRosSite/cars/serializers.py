from rest_framework import serializers

from cars.models import Car, Country, Manufacture, Commentary


class CountrySerializer(serializers.ModelSerializer):
    manufactures = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Country
        fields = ('name', 'manufactures')


class ManufactureCarSerializer(serializers.ModelSerializer):
    commentsCount = serializers.IntegerField(source='commentaries.count')

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
    commentaries = CarCommentarySerializer(many=True, read_only=True)
    commentsCount = serializers.IntegerField(source='commentaries.count', read_only=True)

    class Meta:
        model = Car
        fields = ('name', 'manufacture', 'manufactureName', 'dateStartProduce', 'dateStopProduce', 'commentsCount',
                  'commentaries')

    def validate(self, data):
        if data['dateStartProduce'] > data['dateStopProduce']:
            raise serializers.ValidationError('Конец производства до его начала')
        return data
