import yaml

# создание yaml-файла
yaml_data = """
task_name: energy
energy_sources:
  - name: nuclear
    cost_per_unit: 0.6
    capacity: 300
    schedule:
      - interval: "00:00-06:00"
        demand: 300
      - interval: "06:00-12:00"
        demand: 300
      - interval: "12:00-18:00"
        demand: 300
      - interval: "18:00-00:00"
        demand: 300
  - name: hydro
    cost_per_unit: 0.4
    capacity: 150
    schedule:
      - interval: "00:00-06:00"
        demand: 100
      - interval: "06:00-12:00"
        demand: 100
      - interval: "12:00-18:00"
        demand: 100
      - interval: "18:00-00:00"
        demand: 100
  - name: solar Plant
    cost_per_unit: 0.1
    capacity: 80
    schedule:
      - interval: "00:00-06:00"
        demand: 0
      - interval: "06:00-12:00"
        demand: 50
      - interval: "12:00-18:00"
        demand: 80
      - interval: "18:00-00:00"
        demand: 10
demand_schedule:
  - interval: "00:00-06:00"
    demand: 100
  - interval: "06:00-12:00"
    demand: 200
  - interval: "12:00-18:00"
    demand: 500
  - interval: "18:00-00:00"
    demand: 400
"""
with open('task.yaml', 'w') as f:
    f.write(yaml_data)

# считывание и вывод данных для проверки
with open('task.yaml', 'r') as f:
    data = yaml.safe_load(f)
    print(data)