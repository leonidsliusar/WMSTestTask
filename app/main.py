from crudTest.utils import insert_from_string
from django.db.utils import IntegrityError

products = """id:title:category_id:count:cost
1:Велосипед:1:100:100.50
2:Кастрюля 1,5л:2:50:1200
3:Тарелка 25см:3:1000:25
4:Кастрюля 3л:2:55:300.78"""

category = """id:title:parent
1:Велосипеды:None
3:Тарелки:4
2:Кастрюли:4
4:Посуда для кухни:5
5:Товары для дома:None"""

if __name__ == '__main__' or 'manage.py':
    for data in [category, products]:
        try:
            insert_from_string(data)
        except IntegrityError as e:
            print(f'Already exists\n{e.__str__()}')
