# This file defines the serializers for all event-related entities.
from rest_framework import serializers
from .models import Event, Venue, Speaker, Sponsor, Event_Speaker, Event_Sponsor, Registration, Category, Tag

class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = '__all__'

class SpeakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speaker
        fields = '__all__'

class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = '__all__'

class EventSpeakerSerializer(serializers.ModelSerializer):
    speaker = serializers.StringRelatedField()
    class Meta:
        model = Event_Speaker
        fields = ['speaker', 'presentation_topic', 'presentation_start_time', 'presentation_end_time']

class EventSponsorSerializer(serializers.ModelSerializer):
    sponsor = serializers.StringRelatedField()
    class Meta:
        model = Event_Sponsor
        fields = ['sponsor', 'sponsorship_level', 'sponsorship_amount']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['slug']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ['slug']

class RegistrationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    event_name = serializers.CharField(source='event.name', read_only=True)
    
    class Meta:
        model = Registration
        fields = ['id', 'user', 'event', 'event_name', 'status', 'registration_date']
        read_only_fields = ['id', 'user', 'registration_date']

class EventSerializer(serializers.ModelSerializer):
    organizer = serializers.StringRelatedField(read_only=True)
    venue = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Venue.objects.all(),
        required=False,
        allow_null=True
    )
    categories = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Category.objects.all()
    )
    tags = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Tag.objects.all()
    )
    speakers = EventSpeakerSerializer(source='event_speakers', many=True, read_only=True)
    sponsors = EventSponsorSerializer(source='event_sponsors', many=True, read_only=True)
    
    class Meta:
        model = Event
        fields = [
            'id', 'organizer', 'name', 'slug', 'description', 'start_date', 'end_date',
            'start_time', 'end_time', 'venue', 'location_details', 'status',
            'max_attendees', 'ticket_price', 'speakers', 'sponsors',
            'categories', 'tags'
        ]
        read_only_fields = ['id', 'organizer', 'status', 'slug']