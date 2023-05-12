from blogapp.models import Post, User, Comment, CommentReply, Category
from rest_framework import serializers
import datetime


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    post = PostSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class CommentRepliesSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    comment = CommentSerializer(read_only=True)

    class Meta:
        model = CommentReply
        fields = '__all__'


class WeatherRealtimeSerializer(serializers.Serializer):
    name = serializers.CharField(source='location.name')
    region = serializers.CharField(source='location.region')
    country = serializers.CharField(source='location.country')
    localtime = serializers.DateTimeField(source='location.localtime')
    temp_c = serializers.FloatField(source='current.temp_c')
    is_day = serializers.IntegerField(source='current.is_day')
    condition = serializers.DictField(source='current.condition')


class WeatherForecastSerializer(serializers.Serializer):
    name = serializers.CharField(source='location.name')
    region = serializers.CharField(source='location.region')
    country = serializers.CharField(source='location.country')
    localtime = serializers.DateTimeField(source='location.localtime')
    date = serializers.DateField('date')
    max_temp = serializers.DecimalField(source='day.maxtemp_c', max_digits=5, decimal_places=2)
    min_temp = serializers.DecimalField(source='day.mintemp_c', max_digits=5, decimal_places=2)
    avg_temp = serializers.DecimalField(source='day.avgtemp_c', max_digits=5, decimal_places=2)
    condition = serializers.DictField(source='day.condition')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['localtime'].format = '%Y-%m-%d %H:%M:%S'

    def to_representation(self, instance):
        forecast_data = instance.get('forecast', {})
        forecast_day = forecast_data.get('forecastday', [])[0]
        date = datetime.strptime(self.context['date'], '%Y-%m-%d').date()
        day_data = forecast_day.get('day', {})
        return {
            'name': instance.get('location', {}).get('name'),
            'region': instance.get('location', {}).get('region'),
            'country': instance.get('location', {}).get('country'),
            'localtime': instance.get('location', {}).get('localtime'),
            'date': date,
            'max_temp': day_data.get('maxtemp_c'),
            'min_temp': day_data.get('mintemp_c'),
            'avg_temp': day_data.get('avgtemp_c'),
            'condition': day_data.get('condition', {})
        }
