from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from app.models import db, Question, Category
from app.schemas.category import CategoryResponse, CategoryCreate


categories_bp = Blueprint('categories', __name__)


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=20)


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )


@categories_bp.route('/', methods=['GET'])
def get_categories():
    """Получение списка всех категорий."""

    # Шаг 1: получить список объектов из Базы Данных
    categories = db.session.query(Category).all()  # -> [<Category obj 1>, <Category obj 2>, ... <Category obj 100500>]

    # Шаг 2: преобразовать список сложных объектов в список словарей python (простые объекты)
    categories_data = [
        CategoryResponse.model_validate(cat).model_dump()
        for cat in categories
    ]  # -> [{"id": 1, "name": "Category 1"}, {"id": 2, "name": "Category 2"}, ..., {"id": 13, "name": "Category 13"}]

    # Шаг 3: вернуть упрощённые данные как ответ со статус годом
    return jsonify(categories_data), 200


@categories_bp.route('/', methods=['POST'])
def create_category():
    """Создание новой категории."""
    try:
        category_data = CategoryCreate.model_validate_json(request.data)
    except ValidationError as e:
        return jsonify(e.errors()), 400

    category_data = category_data.model_dump()

    category = Category(**category_data)
    db.session.add(category)
    db.session.commit()

    return jsonify(CategoryResponse.model_validate(category).model_dump()), 201


@categories_bp.route('/<int:pk>', methods=['PUT'])
def update_category(pk):
    # pk == Primary Key
    """Обновление конкретной категории по ее ID."""
    print(pk)

    # category = db.session.query(Category).filter(Category.id == pk).one()
    category = db.session.query(Category).filter(Category.id == pk).one_or_none()
    # if category is None:
    if not category:  # category=None => False => not False => => True
        return jsonify({'message': "Категория с таким ID не найдена"}), 404

    try:
        data = CategoryCreate.model_validate_json(request.data)
    except ValidationError as err:
        return jsonify(err.errors()), 400

    data: dict = data.model_dump()

    for column, value in data.items():
        setattr(category, column, value)

    db.session.commit()
    return jsonify({'message': f"Категория обновлена: {category.name}"}), 200


@categories_bp.route('/<int:pk>', methods=['DELETE'])
def delete_category(pk):
    """Удаление конкретной категории по ее ID."""
    category = db.session.query(Category).filter(Category.id == pk).one_or_none()
    if category is None:
        return jsonify({'message': "Категория с таким ID не найдена"}), 404

    db.session.delete(category)
    db.session.commit()
    # return jsonify({'message': f"Категория с ID {pk} удалена"}), 200
    return jsonify({'message': f"Категория с ID {pk} удалена"}), 204

    # 200 -> OK
    # 204 -> (OK) NO CONTENT
