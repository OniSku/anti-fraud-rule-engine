from typing import Dict, Any
from src.database import db
from src.schemas import CheckResultSchema


class RuleEngineService:
    """
    Ядро бизнес-логики.
    Здесь я реализовал механизм проверки входящих объектов по динамическим правилам.
    """

    async def check_object(self, target_type: str, obj_data: Dict[str, Any]) -> CheckResultSchema:
        """
        Прогоняет объект через все активные правила для его типа.
        target_type: 'Transaction', 'Account' или 'Device'
        """
        # 1. Получаю абсолютно все правила из БД
        all_rules = await db.get_all_rules()

        # 2. Оставляю только те, которые относятся к текущему объекту
        applicable_rules = [r for r in all_rules if r.get("target") == target_type]

        errors = []

        # 3. Применяю каждое правило
        for rule in applicable_rules:
            field = rule.get("field")
            operator = rule.get("operator")
            rule_value = rule.get("value")

            # Если в присланном объекте вообще нет такого поля — пропускаем
            if field not in obj_data:
                continue

            obj_value = obj_data[field]

            # Если условие правила ВЫПОЛНЯЕТСЯ (например, сумма реально > 10000),
            # значит это нарушение (сработал триггер блокировки)
            if self._apply_operator(obj_value, operator, rule_value):
                errors.append(
                    f"Нарушено правило #{rule['id']}: Поле '{field}' ({obj_value}) заблокировано по условию '{operator} {rule_value}'"
                )

        # 4. Формирую ответ
        if errors:
            return CheckResultSchema(status="rejected", errors=errors)

        # Если ошибок нет, сохраняю успешный объект в "базу"
        await db.save_object({"type": target_type, "data": obj_data})
        return CheckResultSchema(status="approved", errors=[])

    def _apply_operator(self, obj_value: Any, operator: str, rule_value: Any) -> bool:
        """
        Вспомогательный метод для безопасного вычисления условий.
        Я вынес это в отдельный метод, чтобы изолировать логику сравнения и ловить ошибки типов.
        """
        try:
            if operator == ">":
                return obj_value > rule_value
            elif operator == "<":
                return obj_value < rule_value
            elif operator == "==":
                return obj_value == rule_value
            elif operator == "!=":
                return obj_value != rule_value
            elif operator == "in":
                # Например: проверка, находится ли страна в списке заблокированных
                return obj_value in rule_value
        except TypeError:
            # Защита от падения, если попытаются сравнить строку с числом (например, "RU" > 1000)
            return False

        return False


# Создаю единственный экземпляр сервиса для импорта в другие файлы
rule_engine = RuleEngineService()