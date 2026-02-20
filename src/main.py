import asyncio
import json
from src.database import db
from src.service import rule_engine
from src.schemas import TransactionSchema, AccountSchema, RuleSchema


async def main():
    """
    Главная функция для демонстрации работы Anti-Fraud системы.
    Я написал её так, чтобы она имитировала реальные HTTP-запросы и ответы.
    """
    print("=== Запуск Business Rule Engine (Anti-Fraud API Mock) ===\n")

    # 1. Загрузка активных правил
    rules = await db.get_all_rules()
    print(f"[*] Активные правила в базе ({len(rules)} шт.):")
    for r in rules:
        print(f"    - [{r['target']}] Если '{r['field']}' {r['operator']} {r['value']} -> Блокировать")

    print("\n=== ИМИТАЦИЯ ВХОДЯЩИХ ЗАПРОСОВ (API POST) ===")

    # СЦЕНАРИЙ А: Успешная транзакция
    print("\n[Запрос 1] Проверка Транзакции (Сумма: 5000)")
    tx1_data = {"amount": 5000, "currency": "USD", "user_id": 101}
    # Прогоняю данные через Pydantic для имитации валидации DRF/FastAPI
    tx1_validated = TransactionSchema(**tx1_data).model_dump()
    result1 = await rule_engine.check_object("Transaction", tx1_validated)
    print(f"Ответ API: {result1.model_dump_json(indent=2)}")

    # СЦЕНАРИЙ Б: Отклоненная транзакция (Срабатывает Правило #1)
    print("\n[Запрос 2] Проверка Транзакции (Сумма: 15000)")
    tx2_data = {"amount": 15000, "currency": "USD", "user_id": 102}
    tx2_validated = TransactionSchema(**tx2_data).model_dump()
    result2 = await rule_engine.check_object("Transaction", tx2_validated)
    print(f"Ответ API: {result2.model_dump_json(indent=2)}")

    # СЦЕНАРИЙ В: Отклоненный аккаунт (Срабатывает Правило #2)
    print("\n[Запрос 3] Проверка Аккаунта (Страна: North Korea)")
    acc1_data = {"country": "North Korea", "age": 25, "is_active": True}
    acc1_validated = AccountSchema(**acc1_data).model_dump()
    result3 = await rule_engine.check_object("Account", acc1_validated)
    print(f"Ответ API: {result3.model_dump_json(indent=2)}")

    print("\n=== ИМИТАЦИЯ ДЕЙСТВИЙ АДМИНИСТРАТОРА ===")

    # СЦЕНАРИЙ Г: Админ "на горячую" добавляет новое правило
    print("\n[АДМИН] Добавляет правило: Блокировать пользователей младше 18 лет")
    new_rule_data = {"target": "Account", "field": "age", "operator": "<", "value": 18}
    new_rule_validated = RuleSchema(**new_rule_data).model_dump()
    await db.add_rule(new_rule_validated)
    print("[-] Правило успешно добавлено в базу.")

    # СЦЕНАРИЙ Д: Проверка нового правила
    print("\n[Запрос 4] Проверка Аккаунта (Страна: USA, Возраст: 16)")
    acc2_data = {"country": "USA", "age": 16, "is_active": True}
    acc2_validated = AccountSchema(**acc2_data).model_dump()
    result4 = await rule_engine.check_object("Account", acc2_validated)
    print(f"Ответ API: {result4.model_dump_json(indent=2)}")

    # ИТОГ: Проверка базы данных
    print("\n=== Итоговое состояние БД (Одобренные объекты) ===")
    saved_objects = await db.get_all_objects()
    print(json.dumps(saved_objects, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    # Я использую asyncio.run для запуска асинхронного Event Loop
    asyncio.run(main())