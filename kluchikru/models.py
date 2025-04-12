from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager, PermissionsMixin

# Менеджер для модели User, который управляет созданием пользователей
class UserManager(BaseUserManager):
  def create_user(self, email, password=None, **extra_fields):
    if not email:
        raise ValueError('Email is required')
    email = self.normalize_email(email)
    user = self.model(email=email, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_superuser(self, email, password=None, **extra_fields):
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)
    return self.create_user(email, password, **extra_fields)

# Модель пользователя, которая используется для аутентификации
class User(AbstractBaseUser , PermissionsMixin):
  name = models.CharField(max_length=100, verbose_name='Имя')
  surname = models.CharField(max_length=100, verbose_name='Фамилия')
  patronymic = models.CharField(max_length=100, verbose_name='Отчество')
  phone_number = models.CharField(max_length=15, verbose_name='Номер телефона')
  email = models.EmailField(unique=True, verbose_name='Электронная почта')
  date_joined = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
  is_active = models.BooleanField(default=True, verbose_name='Активен')
  is_staff = models.BooleanField(default=False, verbose_name='Сотрудник')
  is_agent = models.BooleanField(default=False, verbose_name='Агент')

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []
  
  objects = UserManager()

  class Meta:
        verbose_name = "Пользователь"  
        verbose_name_plural = "Пользователи"  

  def __str__(self):
    return f"{self.name} {self.surname}"

# Модель агенства, которая описывает агенство
class Agency(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    name = models.CharField(max_length=255, verbose_name='Название')
    agent_count = models.PositiveIntegerField(default=0, verbose_name='Количество агентов')
    advertisement_count = models.PositiveIntegerField(default=0, verbose_name='Количество объявлений')

    class Meta:
        verbose_name = "Агентство"
        verbose_name_plural = "Агентства"

    def __str__(self):
        return self.name

# Модель агентов, связывающая агенство и агента
class Agent(models.Model):
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name='agents', verbose_name='Агентство')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')

    class Meta:
        verbose_name = "Агент"
        verbose_name_plural = "Агенты"

    def __str__(self):
        return f"{self.user.name} {self.user.surname} - {self.agency.name}"

# Модель типа недвижимости, которая описывает различные типы недвижимости
class PropertyType(models.Model):
  name = models.CharField(max_length=100, verbose_name='Название типа недвижимости')
  description = models.TextField(verbose_name='Описание типа недвижимости')

  class Meta:
        verbose_name = "Тип недвижимости"  
        verbose_name_plural = "Типы недвижимости" 

  def __str__(self):
    return self.name

# Модель локации, которая описывает географическое местоположение недвижимости
class Location(models.Model):
  city = models.CharField(max_length=100, verbose_name='Город')
  district = models.CharField(max_length=150, verbose_name='Район')
  street = models.CharField(max_length=150, verbose_name='Улица')
  house = models.CharField(max_length=15, verbose_name='Дом')

  class Meta:
        verbose_name = "Адрес"  
        verbose_name_plural = "Адреса" 

  def __str__(self):
    return f"{self.city}, {self.district}, {self.street}, {self.house}"

# Модель категории, которая описывает различные категории недвижимости
class Category(models.Model):
  name = models.CharField(max_length=100, verbose_name='Название категории недвижимости')
  description = models.TextField(verbose_name='Описание категории недвижимости')
  created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

  class Meta:
        verbose_name = "Категория"  
        verbose_name_plural = "Категории" 

  def __str__(self):
    return self.name

# Модель объявления, которая содержит информацию о недвижимости, выставленной на продажу или аренду
class Advertisement(models.Model):
  STATUS_CHOICES = [
      ('draft', 'Черновик'),
      ('active', 'Актуально'),
      ('sold', 'Продано'),
      ('rented', 'Арендовано'),
  ]
  title = models.CharField(max_length=200, verbose_name='Заголовок')
  description = models.TextField(verbose_name='Описание')
  price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Цена')
  user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
  property_type = models.ForeignKey(PropertyType, on_delete=models.CASCADE, verbose_name='Тип недвижимости')
  location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name='Локация')
  category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
  date_posted = models.DateTimeField(auto_now_add=True, verbose_name='Дата размещения')
  status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name='Статус')

  def formatted_price(self):
    if self.price >= 1_000_000:
        return f"{self.price / 1_000_000:.2f} млн"
    elif self.price >= 1_000:
        return f"{self.price / 1_000:.2f} тыс"
    else:
        return f"{self.price:.2f} руб."

  class Meta:
        verbose_name = "Объявление"  
        verbose_name_plural = "Объявления" 

  def __str__(self):
    return f"{self.title} - {self.formatted_price()}"

# Модель фотографии, которая хранит изображения, связанные с объявлениями
class Photo(models.Model):
  advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='photos', verbose_name='Объявление')
  image_url = models.URLField(verbose_name='URL изображения')
  display_order = models.IntegerField(verbose_name='Порядок отображения')

  class Meta:
        verbose_name = "Фотография"  
        verbose_name_plural = "Фотографии" 

  def __str__(self):
      return f"Фото для объявления: {self.advertisement.title} - Порядок отображения: {self.display_order}"

# Модель отзыва, которая позволяет пользователям оставлять отзывы о объявлениях
class Review(models.Model):
  advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, verbose_name='Объявление')
  user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
  rating = models.IntegerField(
      validators=[
          MinValueValidator(0),  
          MaxValueValidator(5)   
      ], verbose_name='Оценка'
  )
  comment = models.TextField(verbose_name='Комментарий')

  class Meta:
        verbose_name = "Отзыв"  
        verbose_name_plural = "Отзывы" 

  def __str__(self):
    return f"Отзыв для {self.advertisement.title} от {self.user.name} - Рейтинг: {self.rating}"

# Модель избранных объявлений, которая позволяет пользователям сохранять объявления в избранное
class FavoriteAdvertisement(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
  advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, verbose_name='Объявление')

  class Meta:
        verbose_name = "Избранное"  
        verbose_name_plural = "Избранные" 

  def __str__(self):
      return f"Избранное: {self.user.name} - {self.advertisement.title}"

# Модель уведомлений, которая хранит уведомления для пользователей о событиях, связанных с объявлениями
class Notification(models.Model):
  NOTIFICATION_TYPE_CHOICES = [
        ('new_ad', 'Новое объявление'),
        ('ad_update', 'Объявление обновлено'),
        ('ad_sold', 'Недвижимость продана'),
        ('ad_rented', 'Недвижимость арендована'),
  ]
  user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
  advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, verbose_name='Объявление')
  notification_type = models.CharField(max_length=50, verbose_name='Тип уведомления')
  created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
  status = models.CharField(max_length=50, verbose_name='Статус')
  message = models.TextField(verbose_name='Сообщение')

  class Meta:
        verbose_name = "Уведомление"  
        verbose_name_plural = "Уведомления" 

  def __str__(self):
    return f"Уведомление для {self.user.name}: {self.notification_type}"

# Модель статистики, которая хранит данные о количестве пользователей и объявлений на определенную дату
class Statistics(models.Model):
  date = models.DateField(verbose_name='Дата')
  user_count = models.IntegerField(verbose_name='Пользователи')
  advertisement_count = models.IntegerField(verbose_name='Объявления')

  class Meta:
        verbose_name = "Статистика"  
        verbose_name_plural = "Статистика" 

  def __str__(self):
      return f"Статистика на {self.date}: Пользователи - {self.user_count}, Объявления - {self.advertisement_count}"
