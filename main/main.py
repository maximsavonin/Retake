import yaml
from pyomo.environ import *

def load_data_from_yaml(file_path):
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)
    return data

def optimize_energy(data):
    # Создание модели
    model = ConcreteModel()

    name = data['task_name']
    energy_sources = data['energy_sources']
    source_names = [source['name'] for source in energy_sources]
    cost_per_unit = {source['name']: source['cost_per_unit'] for source in energy_sources}
    capacity = {source['name']: source['capacity'] for source in energy_sources}
    demand_schedule = {interval['interval']: interval['demand'] for interval in data['demand_schedule']}

    # Определение переменных
    model.production = Var(source_names, demand_schedule.keys(), within=NonNegativeReals)

    # Целевая функция: минимизировать общую стоимость производства
    model.total_cost = Objective(expr=sum(
        cost_per_unit[source] * model.production[source, interval] for source in source_names
        for interval in demand_schedule.keys()), sense=minimize)

    # Ограничение на максимальную генерацию для каждого источника
    def max_capacity_rule(model, source, interval):
        return model.production[source, interval] <= capacity[source]

    model.max_capacity_constraint = Constraint(source_names, demand_schedule.keys(),
                                               rule=max_capacity_rule)

    # Ограничение на совпадение спроса и предложения в каждый интервал времени
    def demand_supply_balance_rule(model, interval):
        return sum(model.production[source, interval] for source in source_names) == demand_schedule[interval]

    model.demand_supply_balance_constraint = Constraint(demand_schedule.keys(), rule=demand_supply_balance_rule)

    # Решение
    solver = SolverFactory('glpk')
    results = solver.solve(model)
    results.problem.name = name

    print("="*60)
    print("РЕЗУЛЬТАТЫ ЗАДАЧИ")
    print("="*60)
    print("-"*60)
    print("Информация о задаче")
    print("-"*60)
    print("Название задачи:", name)
    print("-"*60)
    print("Информация о решении")
    print("-"*60)
    print("Статус решателя:", results.solver.status)
    print("Условие завершения решателя:", results.solver.termination_condition)
    print("Время выполнения решения:", results.solver.time)
    print("="*60)
    print("\n")
    print("="*60)
    print("ОПТИМАЛЬНОЕ РЕШЕНИЕ:")
    if results.solver.termination_condition == TerminationCondition.optimal:
        print("Оптимальное расписание генерации электроэнергии:")
        for source in source_names:
            for interval in demand_schedule.keys():
                print(
                    f"Источник: {source}, Интервал: {interval}, Генерация: {model.production[source, interval].value}")
    else:
        print("Не удалось найти оптимальное решение.")
    print("="*60)

if __name__ == "__main__":
    data = load_data_from_yaml("task.yaml")
    optimize_energy(data)
