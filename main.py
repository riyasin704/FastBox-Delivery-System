import json
import math
import sys


def calculate_distance(point1, point2):
    """Return Euclidean distance between two points."""
    x1, y1 = point1
    x2, y2 = point2

    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def prepare_data(data):
    """
    Convert input into one common format.
    This allows the program to work with both the base case
    and the given test case files.
    """

    warehouses = data["warehouses"]
    agents = data["agents"]

    # base_case.json uses list format
    if isinstance(warehouses, list):
        warehouses = {
            item["id"]: item["location"]
            for item in warehouses
        }

    if isinstance(agents, list):
        agents = {
            item["id"]: item["location"]
            for item in agents
        }

    packages = []

    for package in data["packages"]:
        # Some files use "warehouse" and base case uses "warehouse_id"
        warehouse_id = package.get("warehouse")

        if warehouse_id is None:
            warehouse_id = package.get("warehouse_id")

        packages.append({
            "id": package["id"],
            "warehouse": warehouse_id,
            "destination": package["destination"]
        })

    return warehouses, agents, packages


def find_nearest_agent(warehouse_location, agents):
    """Find the agent nearest to a warehouse."""

    nearest_agent = None
    shortest_distance = float("inf")

    for agent_id, agent_location in agents.items():
        distance = calculate_distance(agent_location, warehouse_location)

        if distance < shortest_distance:
            shortest_distance = distance
            nearest_agent = agent_id

    return nearest_agent


def create_report(data):
    warehouses, agents, packages = prepare_data(data)

    report = {}

    # Initial report for every agent
    for agent_id in agents:
        report[agent_id] = {
            "packages_delivered": 0,
            "total_distance": 0.0,
            "efficiency": None
        }

    # Assign and deliver every package
    for package in packages:
        warehouse_id = package["warehouse"]
        warehouse_location = warehouses[warehouse_id]
        destination = package["destination"]

        agent_id = find_nearest_agent(warehouse_location, agents)
        agent_location = agents[agent_id]

        # Agent first reaches warehouse, then delivers the package
        pickup_distance = calculate_distance(
            agent_location,
            warehouse_location
        )

        delivery_distance = calculate_distance(
            warehouse_location,
            destination
        )

        total_trip_distance = pickup_distance + delivery_distance

        report[agent_id]["packages_delivered"] += 1
        report[agent_id]["total_distance"] += total_trip_distance

    # Calculate final values
    best_agent = None
    best_efficiency = float("inf")

    for agent_id in agents:
        delivered = report[agent_id]["packages_delivered"]
        total_distance = report[agent_id]["total_distance"]

        report[agent_id]["total_distance"] = round(total_distance, 2)

        if delivered > 0:
            efficiency = total_distance / delivered
            efficiency = round(efficiency, 2)

            report[agent_id]["efficiency"] = efficiency

            if efficiency < best_efficiency:
                best_efficiency = efficiency
                best_agent = agent_id

    report["best_agent"] = best_agent

    return report


def main():
    # Default file
    input_file = "data.json"

    # Optional: python main.py test_case_1.json
    if len(sys.argv) > 1:
        input_file = sys.argv[1]

    try:
        with open(input_file, "r") as file:
            data = json.load(file)

        report = create_report(data)

        with open("report.json", "w") as file:
            json.dump(report, file, indent=4)

        print("Delivery simulation completed.")
        print("Report saved in report.json")
        print()
        print(json.dumps(report, indent=4))

    except FileNotFoundError:
        print("Error: Input file not found.")

    except (KeyError, TypeError, json.JSONDecodeError) as error:
        print("Error in input data:", error)


if __name__ == "__main__":
    main()
