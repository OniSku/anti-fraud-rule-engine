import asyncio
from typing import List, Dict, Any

# Имитация таблицы "Правила" (Rules)
# Я добавил несколько стартовых правил, чтобы API сразу было с чем работать при запуске.
MOCK_RULES_DB: List[Dict[str, Any]] = [
    {"id": 1, "target": "Transaction", "field": "amount", "operator": ">", "value": 10000},
    {"id": 2, "target": "Account", "field": "country", "operator": "==", "value": "North Korea"},
    {"id": 3, "target": "Device", "field": "is_trusted", "operator": "==", "value": False},
]

# Имитация таблицы успешных объектов (прошедших проверку)
MOCK_OBJECTS_DB: List[Dict[str, Any]] = []


class MockDatabase:
    """
    Асинхронный слой доступа к данным (Data Access Layer).
    Я реализовал его с имитацией задержки ввода-вывода (asyncio.sleep),
    чтобы поведение системы максимально соответствовало реальной работе с СУБД.
    """

    async def get_all_rules(self) -> List[Dict[str, Any]]:
        """Получение всех активных правил"""
        await asyncio.sleep(0.1)  # Имитация сетевой задержки к БД
        return MOCK_RULES_DB

    async def add_rule(self, rule_data: Dict[str, Any]) -> Dict[str, Any]:
        """Добавление нового правила с автогенерацией ID"""
        await asyncio.sleep(0.1)
        new_id = max([r.get("id", 0) for r in MOCK_RULES_DB] + [0]) + 1
        rule_data["id"] = new_id
        MOCK_RULES_DB.append(rule_data)
        return rule_data

    async def delete_rule(self, rule_id: int) -> bool:
        """Удаление правила по ID"""
        await asyncio.sleep(0.1)
        initial_len = len(MOCK_RULES_DB)
        # Оставляем только те правила, ID которых не совпадает с удаляемым
        MOCK_RULES_DB[:] = [r for r in MOCK_RULES_DB if r.get("id") != rule_id]
        return len(MOCK_RULES_DB) < initial_len

    async def save_object(self, obj_data: Dict[str, Any]) -> None:
        """Сохранение бизнес-объекта, успешно прошедшего проверку"""
        await asyncio.sleep(0.1)
        MOCK_OBJECTS_DB.append(obj_data)

    async def get_all_objects(self) -> List[Dict[str, Any]]:
        """Получение истории проверенных объектов"""
        await asyncio.sleep(0.1)
        return MOCK_OBJECTS_DB


# Создаю единственный экземпляр подключения к нашей "БД" (паттерн Singleton для слоя данных)
db = MockDatabase()