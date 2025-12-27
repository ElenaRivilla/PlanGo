from django.db import models
from apps.itineraries.models.destination import Destination

class Activity(models.Model):
    place_id = models.CharField(max_length=255, primary_key=True)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='activities')
    name = models.CharField(max_length=255)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    address = models.TextField()
    ACTIVITY_TYPES = [
        ('adventure_sports_center', 'Adventure Sports Center'),
        ('amphitheatre', 'Amphitheatre'),
        ('amusement_center', 'Amusement Center'),
        ('amusement_park', 'Amusement Park'),
        ('aquarium', 'Aquarium'),
        ('banquet_hall', 'Banquet Hall'),
        ('barbecue_area', 'Barbecue Area'),
        ('botanical_garden', 'Botanical Garden'),
        ('bowling_alley', 'Bowling Alley'),
        ('casino', 'Casino'),
        ('childrens_camp', 'Children\'s Camp'),
        ('comedy_club', 'Comedy Club'),
        ('community_center', 'Community Center'),
        ('concert_hall', 'Concert Hall'),
        ('convention_center', 'Convention Center'),
        ('cultural_center', 'Cultural Center'),
        ('cycling_park', 'Cycling Park'),
        ('dance_hall', 'Dance Hall'),
        ('dog_park', 'Dog Park'),
        ('event_venue', 'Event Venue'),
        ('ferris_wheel', 'Ferris Wheel'),
        ('garden', 'Garden'),
        ('hiking_area', 'Hiking Area'),
        ('historical_landmark', 'Historical Landmark'),
        ('internet_cafe', 'Internet Cafe'),
        ('karaoke', 'Karaoke'),
        ('marina', 'Marina'),
        ('movie_rental', 'Movie Rental'),
        ('movie_theater', 'Movie Theater'),
        ('national_park', 'National Park'),
        ('night_club', 'Night Club'),
        ('observation_deck', 'Observation Deck'),
        ('off_roading_area', 'Off-Roading Area'),
        ('opera_house', 'Opera House'),
        ('park', 'Park'),
        ('farm', 'Farm'),
        ('philharmonic_hall', 'Philharmonic Hall'),
        ('picnic_ground', 'Picnic Ground'),
        ('planetarium', 'Planetarium'),
        ('plaza', 'Plaza'),
        ('roller_coaster', 'Roller Coaster'),
        ('skateboard_park', 'Skateboard Park'),
        ('state_park', 'State Park'),
        ('tourist_attraction', 'Tourist Attraction'),
        ('video_arcade', 'Video Arcade'),
        ('visitor_center', 'Visitor Center'),
        ('water_park', 'Water Park'),
        ('wedding_venue', 'Wedding Venue'),
        ('wildlife_park', 'Wildlife Park'),
        ('wildlife_refuge', 'Wildlife Refuge'),
        ('zoo', 'Zoo'),
        ('art_gallery', 'Art Gallery'),
        ('art_studio', 'Art Studio'),
        ('church', 'Church'),
        ('hindu_temple', 'Hindu Temple'),
        ('mosque', 'Mosque'),
        ('synagogue', 'Synagogue'),
        ('auditorium', 'Auditorium'),
        ('cultural_landmark', 'Cultural Landmark'),
        ('historical_place', 'Historical Place'),
        ('monument', 'Monument'),
        ('museum', 'Museum'),
        ('performing_arts_theater', 'Performing Arts Theater'),
        ('sculpture', 'Sculpture'),
    ]
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPES)
    latitude = models.DecimalField(max_digits=30, decimal_places=20)
    longitude = models.DecimalField(max_digits=30, decimal_places=20)
    isSave = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Activity'
        verbose_name_plural = 'Activity'
        
    def __str__(self):
        return self.name