from django.db import models
from apps.itineraries.models.destination import Destination

class Restaurant(models.Model):
    place_id = models.CharField(max_length=255, primary_key=True)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='restaurants')
    name = models.CharField(max_length=255)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    address = models.TextField()
    RESTAURANT_TYPES = [
        ('acai_shop', 'Acai Shop'),
        ('afghani_restaurant', 'Afghani Restaurant'),
        ('african_restaurant', 'African Restaurant'),
        ('american_restaurant', 'American Restaurant'),
        ('asian_restaurant', 'Asian Restaurant'),
        ('bagel_shop', 'Bagel Shop'),
        ('bakery', 'Bakery'),
        ('bar', 'Bar'),
        ('bar_and_grill', 'Bar and Grill'),
        ('barbecue_restaurant', 'Barbecue Restaurant'),
        ('brazilian_restaurant', 'Brazilian Restaurant'),
        ('breakfast_restaurant', 'Breakfast Restaurant'),
        ('brunch_restaurant', 'Brunch Restaurant'),
        ('buffet_restaurant', 'Buffet Restaurant'),
        ('cafe', 'Cafe'),
        ('cafeteria', 'Cafeteria'),
        ('candy_store', 'Candy Store'),
        ('cat_cafe', 'Cat Cafe'),
        ('chinese_restaurant', 'Chinese Restaurant'),
        ('chocolate_factory', 'Chocolate Factory'),
        ('chocolate_shop', 'Chocolate Shop'),
        ('coffee_shop', 'Coffee Shop'),
        ('confectionery', 'Confectionery'),
        ('deli', 'Deli'),
        ('dessert_restaurant', 'Dessert Restaurant'),
        ('dessert_shop', 'Dessert Shop'),
        ('diner', 'Diner'),
        ('dog_cafe', 'Dog Cafe'),
        ('donut_shop', 'Donut Shop'),
        ('fast_food_restaurant', 'Fast Food Restaurant'),
        ('fine_dining_restaurant', 'Fine Dining Restaurant'),
        ('food_court', 'Food Court'),
        ('french_restaurant', 'French Restaurant'),
        ('greek_restaurant', 'Greek Restaurant'),
        ('hamburger_restaurant', 'Hamburger Restaurant'),
        ('ice_cream_shop', 'Ice Cream Shop'),
        ('indian_restaurant', 'Indian Restaurant'),
        ('indonesian_restaurant', 'Indonesian Restaurant'),
        ('italian_restaurant', 'Italian Restaurant'),
        ('japanese_restaurant', 'Japanese Restaurant'),
        ('juice_shop', 'Juice Shop'),
        ('korean_restaurant', 'Korean Restaurant'),
        ('lebanese_restaurant', 'Lebanese Restaurant'),
        ('meal_delivery', 'Meal Delivery'),
        ('meal_takeaway', 'Meal Takeaway'),
        ('mediterranean_restaurant', 'Mediterranean Restaurant'),
        ('mexican_restaurant', 'Mexican Restaurant'),
        ('middle_eastern_restaurant', 'Middle Eastern Restaurant'),
        ('pizza_restaurant', 'Pizza Restaurant'),
        ('pub', 'Pub'),
        ('ramen_restaurant', 'Ramen Restaurant'),
        ('restaurant', 'Restaurant'),
        ('sandwich_shop', 'Sandwich Shop'),
        ('seafood_restaurant', 'Seafood Restaurant'),
        ('spanish_restaurant', 'Spanish Restaurant'),
        ('steak_house', 'Steak House'),
        ('sushi_restaurant', 'Sushi Restaurant'),
        ('tea_house', 'Tea House'),
        ('thai_restaurant', 'Thai Restaurant'),
        ('turkish_restaurant', 'Turkish Restaurant'),
        ('vegan_restaurant', 'Vegan Restaurant'),
        ('vegetarian_restaurant', 'Vegetarian Restaurant'),
        ('vietnamese_restaurant', 'Vietnamese Restaurant'),
        ('wine_bar', 'Wine Bar'),
    ]
    restaurant_type = models.CharField(max_length=50, choices=RESTAURANT_TYPES)
    latitude = models.DecimalField(max_digits=30, decimal_places=20)
    longitude = models.DecimalField(max_digits=30, decimal_places=20)
    isSave = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Restaurant'
        verbose_name_plural = 'Restaurant'
    
    def __str__(self):
        return self.name
    