from database.models import Rating, Neighborhood
from database import db
from utils.formatters import get_row_dict
from utils.validators.rating import (
    validate_create_rating,
    validate_update_rating
)
from settings import logger


def create_rating(body, username, neighborhood_id):

    neighborhood = db.get_one(Neighborhood, neighborhood_id)

    if neighborhood[1] == 404:
        return 'Bairro não existe', 404

    errors = validate_create_rating(body)
    if errors:
        return errors, 400

    try:
        rating = Rating(
            user=username,
            id_neighborhood=neighborhood_id,
            rating_neighborhood=body['rating_neighborhood'],
            details=body['details'],
        )
        result, code = db.insert_one(rating)

        return result, code
    except Exception as error:
        logger.error(error)
        return str(error), 401


def get_all_ratings():
    result, code = db.get_all(Rating)
    if result:
        if code == 200:
            ratings_neighborhood = [get_row_dict(u) for u in result]
            return ratings_neighborhood, code
        return result, code
    return [], 200


def get_one_rating(id_rating):
    result, code = db.get_one(Rating, id_rating)

    if code == 200:
        rating = get_row_dict(result)
        return rating, 200
    return result, code


def delete_rating(id_rating):
    result, code = db.delete(Rating, id_rating)

    return result, code


def update_rating(id_rating, body):
    params = {}
    fields = ['rating_neighborhood', 'details']

    result, status = db.get_one(Rating, id_rating)
    rating_before_update = get_row_dict(result)

    if status == 404:
        return 'Avaliação não existe', 404

    for field in fields:
        if field in body:
            params[field] = body[field]
        else:
            params[field] = rating_before_update[field]

    logger.info(params)

    errors = validate_update_rating(params)
    if errors:
        return errors, 400

    result, code = db.update(Rating, id_rating, params)

    if code == 200:
        rating = get_row_dict(result)
        return rating, code

    return result, code
