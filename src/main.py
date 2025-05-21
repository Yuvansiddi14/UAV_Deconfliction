from deconfliction import check_deconfliction
from visualization import visualize_2d, visualize_4d

def main():
    ###############
    # 2D Scenario #
    ###############
    # Sample primary mission (2D)
    primary_mission_2d = {
        "waypoints": [
            {"x": 0, "y": 0, "time": 0},
            {"x": 10, "y": 10, "time": 5},
            {"x": 20, "y": 0, "time": 10}
        ],
        "mission_window": {"start": 0, "end": 10}
    }

    # Sample simulated flights (2D)
    simulated_flights_2d = [
        {
            "id": "drone_1",
            "waypoints": [
                {"x": 10, "y": 10, "time": 5},
                {"x": 15, "y": 5, "time": 7}
            ]
        },
        {
            "id": "drone_2",
            "waypoints": [
                {"x": 5, "y": 5, "time": 2},
                {"x": 25, "y": 5, "time": 9}
            ]
        }
    ]

    safety_buffer = 3  # minimum allowed distance

    # Run deconfliction check for 2D mission
    result_2d = check_deconfliction(primary_mission_2d, simulated_flights_2d, safety_buffer)
    print("2D Deconfliction Status:", result_2d["status"])
    if result_2d["status"] == "conflict":
        print("2D Conflict Details:")
        for conflict in result_2d["details"]:
            print(conflict)

    # Visualize 2D mission & conflicts
    visualize_2d(primary_mission_2d, simulated_flights_2d, safety_buffer, conflicts=result_2d.get("details"))

    ###############
    # 4D Scenario #
    ###############
    # Sample primary mission (4D - with altitude)
    primary_mission_4d = {
        "waypoints": [
            {"x": 0, "y": 0, "z": 0, "time": 0},
            {"x": 10, "y": 10, "z": 5, "time": 5},
            {"x": 20, "y": 0, "z": 10, "time": 10}
        ],
        "mission_window": {"start": 0, "end": 10}
    }

    # Sample simulated flights (4D)
    simulated_flights_4d = [
        {
            "id": "drone_A",
            "waypoints": [
                {"x": 10, "y": 10, "z": 5, "time": 5},
                {"x": 15, "y": 5, "z": 6, "time": 7}
            ]
        },
        {
            "id": "drone_B",
            "waypoints": [
                {"x": 5, "y": 5, "z": 2, "time": 2},
                {"x": 25, "y": 5, "z": 8, "time": 9}
            ]
        }
    ]

    # Run deconfliction check for 4D mission
    result_4d = check_deconfliction(primary_mission_4d, simulated_flights_4d, safety_buffer)
    print("4D Deconfliction Status:", result_4d["status"])
    if result_4d["status"] == "conflict":
        print("4D Conflict Details:")
        for conflict in result_4d["details"]:
            print(conflict)

    # Visualize 4D mission & conflicts
    visualize_4d(primary_mission_4d, simulated_flights_4d, safety_buffer, conflicts=result_4d.get("details"))

if __name__ == "__main__":
    main()

