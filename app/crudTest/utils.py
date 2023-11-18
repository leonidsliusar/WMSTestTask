from typing import Protocol
from crudTest.data_models import T, CategoryBase, ProductBase, models_mapping
from crudTest.dal import add_multiple, get_many, get_all
from crudTest.models import M, Category, Product


class Parser(Protocol):
    ...


class StringParser(Parser):

    def __init__(self, data_set: list, map_key: list, model: T):
        self.data_set = data_set
        self.base_model = model
        self.map_key = map_key

    @property
    def map_from_str(self) -> list[dict]:
        obj_map_set = []
        for item in self.data_set[1:]:
            if item.strip():
                value = [x.strip() for x in item.split(':')]
                obj_map = self.parse_value(value)
                obj_map_set.append(obj_map)
        return obj_map_set

    def parse_value(self, value: list[str]) -> dict:
        for i in range(len(value)):
            value[i] = value[i].strip('')
        obj_map = dict(zip(self.map_key, value))
        serialized_model = self.base_model(**obj_map)
        return serialized_model.model_dump()

    @property
    def model(self) -> T:
        return self.base_model


class ParserFactory(Protocol):

    def prepare(self) -> Parser:
        ...


class StringParserFactory(ParserFactory):

    def __init__(self, data: str):
        self.data_string = data

    @property
    def prepare(self) -> StringParser:
        data_set = self.data_string.split('\n')
        map_key = data_set[0].split(':')
        map_key = [x.strip(' ') for x in map_key]
        key_length = len(map_key)
        model = None
        if key_length == 3:
            model = CategoryBase
        elif key_length == 5:
            model = ProductBase
        return StringParser(data_set, map_key, model)


def get_obj_set(obj_map_set: list[dict], db_model: M) -> list[M]:
    if db_model == Category:
        obj_ids_map = {}
        self_parent_map = {}
        obj_set = []
        for item in obj_map_set:
            parent = item.get('parent')
            item['parent'] = None
            item_id = item.get('id')
            obj_ids_map.update({item_id: db_model(**item)})
            if parent:
                self_parent_map[item_id] = parent
        for item in obj_map_set:
            obj_set.append(db_model(**item))
        for item in obj_set:
            parent_id = self_parent_map.get(item.id)
            item.parent = obj_ids_map.get(parent_id)
        return obj_set
    else:
        category_ids = []
        for item in obj_map_set:
            category_ids.append(item.get('category_id'))
        category_obj_set = get_many(Category, category_ids)
        category_map = {}
        for item in category_obj_set:
            category_map[item.id] = item
        obj_set = []
        for product in obj_map_set:
            product['category_id'] = category_map.get(product['category_id'])
            obj_set.append(db_model(**product))
        return obj_set


def insert_from_string(data: str, parser_factory: Parser = StringParserFactory) -> None:
    """Insert from string interface"""
    parser = parser_factory(data).prepare
    db_model = models_mapping.get(parser.model)
    obj_map_set = parser.map_from_str
    obj_set = get_obj_set(obj_map_set, db_model)
    add_multiple(db_model, obj_set)


def fetch_all(model: M = Product) -> list[M]:
    return get_all(model)
