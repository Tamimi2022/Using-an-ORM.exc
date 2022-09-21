import datetime
from unicodedata import name
from models import *
import models
from peewee import *
from typing import List

__winc_id__ = "286787689e9849969c326ee41d8c53c4"
__human_name__ = "Peewee ORM"


def cheapest_dish() -> models.Dish:
    """You want ot get food on a budget

    Query the database to retrieve the cheapest dish available
    """
    for dish in Dish.select().order_by(Dish.price_in_cents.asc()):
        return (dish)


def vegetarian_dishes() -> List[models.Dish]:
    """You'd like to know what vegetarian dishes are available

    Query the database to return a list of dishes that contain only
    vegetarian ingredients.
    """
    list_dishes = []
    for dish in models.Dish.select():
        print(dish.name)
        vegetarian_ingredients = True
        for ingerdient in dish.ingredients:
            if ingerdient.is_vegetarian is False:
                vegetarian_ingredients = False
        if vegetarian_ingredients is True:
            list_dishes.append(dish)
    return list_dishes


def best_average_rating() -> models.Restaurant:
    """You want to know what restaurant is best

    Query the database to retrieve the restaurant that has the highest
    rating on average
    """
    highest_resto = (
        models.Restaurant.select(
            models.Restaurant, fn.AVG(models.Rating.rating).alias('avg_rating')
        )
    )
    return highest_resto


def add_rating_to_restaurant() -> None:
    """After visiting a restaurant, you want to leave a rating

    Select the first restaurant in the dataset and add a rating
    """
    query = Restaurant.select().where(Restaurant.id ==1)
    for r in query:
        resto =r
    Rating.create(restaurant = resto, rating =5)


def dinner_date_possible() -> List[models.Restaurant]:
    """You have asked someone out on a dinner date, but where to go?

    You want to eat at around 19:00 and your date is vegan.
    Query a list of restaurants that account for these constraints.
    """
    list_dishes = []
    for dish in models.Dish.select():
        vegetarian_ingredients = True
        for ingredient in dish.ingredients:
            if ingredient.is_vegan is False:
                vegetarian_ingredients = False
        if vegetarian_ingredients is True:
            list_dishes.append(dish.name)
    print("list_dishes: ", list_dishes)

    # the resto is open between 19:00 and 22:00
    open_since = datetime.time(19, 00, 00)
    close_since = datetime.time(22, 00, 00)

    # The resto that has at least one dish that has only vegan ingredients
    query = (
        models.Restaurant.select(models.Restaurant)
        .join(models.Dish, on=(models.Dish.served_at == models.Restaurant.id))
        .where(
            (
                models.Dish.name.in_(list_dishes)
                & (models.Restaurant.opening_time <= open_since)
                & (models.Restaurant.closing_time >= close_since)
            )
        )
    )
    restaurant_options = [restaurant for restaurant in query]
    return restaurant_options


def add_dish_to_menu() -> models.Dish:
    """You have created a new dish for your restaurant and want to add it to the menu

    The dish you create must at the very least contain 'cheese'.
    You do not know which ingredients are in the database, but you must not
    create ingredients that already exist in the database. You may create
    new ingredients however.
    Return your newly created dish
    """
    create_new_dish = ('cheese', 5, 2000)
    vegetarian_ingredients_new = (
        ("cheese", (False, True, True)),
    )
    models.Dish.create(name=create_new_dish[0], served_at=create_new_dish[1], price_in_cents=create_new_dish[2])
    
    for name, i in vegetarian_ingredients_new:
        ing, created = models.Ingredient.get_or_create(
            name=name, is_vegan=i[0], is_vegetarian=i[1], is_glutenfree=i[2]
        )
        if created is True:
            print('add ', ing.name)
        else:
            print(ing.name, ' already in Database')
            
            # Add ingredient_data to new dish data
    dish = models.Dish.get(models.Dish.name == create_new_dish[0])
    for ingredient in vegetarian_ingredients_new:
        ing = models.Ingredient.get(models.Ingredient.name == ingredient[0])
        dish.ingredients.add(ing)
    return models.Dish.get(models.Dish.name == create_new_dish[0])