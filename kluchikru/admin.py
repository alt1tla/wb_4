from django.contrib import admin
from .models import User, PropertyType, Location, Category, Advertisement, Photo, Review, FavoriteAdvertisement, Notification, Statistics, Agency, Agent

# Настройка для модели User
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'email', 'is_active', 'is_staff', 'is_agent', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'is_agent')
    search_fields = ('name', 'surname', 'email')
    list_display_links = ('name', 'surname')
    readonly_fields = ('date_joined',)
    date_hierarchy = 'date_joined'

# Настройка для модели Agency
@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'agent_count', 'advertisement_count')
    search_fields = ('name',)
    list_filter = ('created_at',)
    ordering = ('created_at',)

# Настройка для модели Agent
@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('user', 'agency')
    search_fields = ('user__email', 'user__name', 'user__surname')
    list_filter = ('agency',)
    ordering = ('agency',)

# Настройка для модели PropertyType
@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

# Настройка для модели Location
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('city', 'district', 'street', 'house')
    list_filter = ('city', 'district')
    search_fields = ('city', 'district', 'street', 'house')

# Настройка для модели Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name',)

# Настройка для модели Advertisement
@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'formatted_price', 'status', 'date_posted')
    list_filter = ('status', 'property_type', 'category')
    search_fields = ('title', 'description')
    list_display_links = ('title',)
    date_hierarchy = 'date_posted'
    raw_id_fields = ('user',)  

    @admin.display(description='Цена')
    def formatted_price(self, obj):
        return obj.formatted_price()

# Настройка для модели Photo
@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('advertisement', 'image_url', 'display_order')
    list_filter = ('advertisement',)
    search_fields = ('advertisement__title',)

# Настройка для модели Review
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('advertisement', 'user', 'rating', 'comment')
    list_filter = ('rating',)
    search_fields = ('advertisement__title', 'user__name')
    readonly_fields = ('advertisement', 'user')

# Настройка для модели FavoriteAdvertisement
@admin.register(FavoriteAdvertisement)
class FavoriteAdvertisementAdmin(admin.ModelAdmin):
    list_display = ('user', 'advertisement')
    list_filter = ('user',)
    search_fields = ('user__name', 'advertisement__title')

# Настройка для модели Notification
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'created_at', 'status')
    list_filter = ('notification_type', 'status')
    search_fields = ('user__name', 'message')

# Настройка для модели Statistics
@admin.register(Statistics)
class StatisticsAdmin(admin.ModelAdmin):
    list_display = ('date', 'user_count', 'advertisement_count')
    list_filter = ('date',)
    date_hierarchy = 'date'
