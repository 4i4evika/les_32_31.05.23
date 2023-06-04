### Создайте приложение для эмуляции работы пиццерии. Приложение должно иметь следующую функциональность:
# 1.Пользователь может выбрать из пяти стандартных рецептов пиццы или создать свой рецепт
# 2.Пользователь может выбирать, добавлять топпинги(сладкий лук, халапеньо, чили, соленый огурец, оливки и т.п.)
# 3.Информацию о заказанной пицце нужно отображать на экран и сохранять в файл.
# 4.Расчет может производиться как наличными, так и картой.
# 5.Необходимо иметь возможность просмотреть количество проданных пицц, выручку, прибыль
# 6.Классы должны должны быть построены с учетом принципов SOLID и паттернов проектирования.


from abc import ABC, abstractmethod


class PizzaBase:
    minimal_size = 25

    def __init__(self):
        self.size = ''.join(char for char in self.__class__.__name__ if char.isdigit())
        if int(self.size) < self.minimal_size:
            raise Exception('Слишком маленькая пицца!')

    @property
    def cost(self):
        return (int(self.size) - self.minimal_size)**2

    def __str__(self):
        return f'Основа для пиццы {self.size} см'


class PizzaBase25cm(PizzaBase):
    pass


class Kitchen:
    current_toppings = {}

    @classmethod
    def start(cls):
        for topping in Topping.__subclasses__():
            cls.add_topping(topping)

    @classmethod
    def add_topping(cls, topping):
        if topping.__name__ not in cls.current_toppings:
            cls.current_toppings[topping.__name__] = topping

    @classmethod
    def remove_topping(cls, topping):
        if topping.__name__ in cls.current_toppings:
            del cls.current_toppings[topping.__name__]

    class DontHaveTopping(Exception):
        pass


class Topping(ABC):

    def __init__(self):
        self.name = self.__class__.__name__
        if self.name not in Kitchen.current_toppings:
            raise Kitchen.DontHaveTopping

    @abstractmethod
    def cost(self):
        pass

    def __str__(self):
        return self.name


class Pepperoni(Topping):
    @property
    def cost(self):
        return 20


class Tomatoes(Topping):
    @property
    def cost(self):
        return 20


class Cheese(Topping):
    @property
    def cost(self):
        return 25


class Bacon(Topping):
    @property
    def cost(self):
        return 23


class Mushrooms(Topping):
    @property
    def cost(self):
        return 18


class Pizza:
    def __init__(self, base, *toppings):
        self.base = base
        self.toppings = toppings

    @property
    def cost(self):
        return sum((top.cost for top in self.toppings)) * self.base.cost


class PizzaTemplates:
    @staticmethod
    def Margarita(base=PizzaBase25cm()):
        return Pizza(base,
                     Kitchen.current_toppings['Cheese'](),
                     Kitchen.current_toppings['Tomatoes']())

    @staticmethod
    def Pepperoni(base=PizzaBase25cm()):
        return Pizza(base,
                     Kitchen.current_toppings['Cheese'](),
                     Kitchen.current_toppings['Pepperoni']())

    @staticmethod
    def BaconAndMushrooms(base=PizzaBase25cm()):
        return Pizza(base,
                     Kitchen.current_toppings['Cheese'](),
                     Kitchen.current_toppings['Bacon'](),
                     Kitchen.current_toppings['Mushrooms'](),
                     Kitchen.current_toppings['Tomatoes']())


class CashRegister:
    def __init__(self):
        self.basket = []

    def start(self):
        query = None
        self.make_an_order()
        while query != '5':
            print('-'*30)
            query = input('Введите команду:\n'
                          '1. Добавить пиццу в корзину\n'
                          '2. Удалить пиццу из корзины\n'
                          '3. Просмотреть ваш заказ\n'
                          '4. Очистить корзину\n'
                          '5. Выход:\n')
            if query == '1':
                self.add_pizza()
            elif query == '2':
                self.delete_pizza()
            elif query == '3':
                print(self.view_pizza())
            elif query == '4':
                self.clear_pizza()
                print('Корзина очищена')

    def make_an_order(self):
        self.basket = []

    def add_pizza(self):
        query = input('Выберите опцию:\n'
                      '1. Выбрать одну из готовых пицц\n'
                      '2. Собрать пиццу самому!\n')
        if query == '1':
            base = 'Введите номер пиццы, которую вы бы хотели заказать:\n'
            templates = list(PizzaTemplates.__dict__.items())
            for i, pizza in enumerate(templates):
                if isinstance(pizza[1], staticmethod):
                    base += f'{i}. {pizza[0]} - {", ".join(map(str, pizza[1]().toppings)).lower()}\n'
            choice = int(input(base))

            pizza_maker = templates[choice][0]

            self.basket.append(pizza_maker)
        else:
            component = input('Укажите ингредиенты через запятую (сыр, бекон, помидоры, пепперони):\n')
            pizza = {'Индивидуальная': component.split(', ')}
            print(f'Вы добавили {pizza}')
            self.basket.append('Individual')

    def delete_pizza(self):
        pizza = input('Введите наименование пиццы для удаления: ')
        self.basket.remove(pizza)
        print(f'Пицца {pizza} удалена из корзины')


    def view_pizza(self):
        if len(self.basket) == 0:
            return 'Корзина пуста'
        else:
            return self.basket

    def clear_pizza(self):
        self.basket.clear()


class Pizzeria:
    def __init__(self):
        self.sold_pizzas = 0
        self.revenue = 0
        self.profit = 0
        self.cash_register = CashRegister()

    def run(self):
        Kitchen.start()
        self.cash_register.start()


def main():
    app = Pizzeria()
    app.run()


if __name__ == '__main__':
    main()
