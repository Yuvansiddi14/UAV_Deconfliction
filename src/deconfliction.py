import math

def calculate_distance(p1, p2):
    """
    Calculate Euclidean distance between two points.
    Supports 2D and 3D:
      - If both points have 'z', use 3D distance.
      - Otherwise, assume 2D.
    """
    if "z" in p1 and "z" in p2:
        return math.sqrt((p1["x"] - p2["x"]) ** 2 +
                         (p1["y"] - p2["y"]) ** 2 +
                         (p1["z"] - p2["z"]) ** 2)
    else:
        return math.sqrt((p1["x"] - p2["x"]) ** 2 +
                         (p1["y"] - p2["y"]) ** 2)

def time_overlap(t1_start, t1_end, t2, tolerance=0):
    """
    Check if a single time instant (t2) falls within the interval [t1_start, t1_end].
    A tolerance parameter adds slack if needed.
    """
    return (t1_start - tolerance) <= t2 <= (t1_end + tolerance)

def check_deconfliction(primary_mission, simulated_flights, safety_buffer, time_tolerance=0):
    """
    Check conflicts between the primary mission and a list of simulated flights.

    Parameters:
      - primary_mission (dict): with keys "waypoints" (list of waypoints) and "mission_window".
        Each waypoint should be a dict with keys 'x', 'y', optional 'z', and 'time'.
      - simulated_flights (list): each element is a dict with an "id" and "waypoints".
      - safety_buffer (float): minimum allowed distance between drones.
      - time_tolerance (float): allowable slack in overlap.

    Returns:
      dict: {"status": "clear"} if no conflict,
            {"status": "conflict", "details": [ ... conflict details ... ]}
    """
    conflicts = []
    p_waypoints = primary_mission["waypoints"]

    # Iterate over primary mission segments (between consecutive waypoints)
    for i in range(len(p_waypoints) - 1):
        p_start = p_waypoints[i]
        p_end = p_waypoints[i + 1]
        # For each segment, consider the corresponding time window
        for sim in simulated_flights:
            for sim_point in sim["waypoints"]:
                # Check if the simulated point exists in the time window of the segment.
                if time_overlap(p_start["time"], p_end["time"], sim_point["time"], tolerance=time_tolerance):
                    # Use the starting point (for simplicity) to compute distance.
                    dist = calculate_distance(p_start, sim_point)
                    if dist < safety_buffer:
                        conflicts.append({
                            "primary_segment": (p_start, p_end),
                            "conflict_at": sim_point,
                            "sim_drone": sim["id"],
                            "distance": dist,
                            "conflict_time": sim_point["time"]
                        })
    if conflicts:
        return {"status": "conflict", "details": conflicts}
    else:
        return {"status": "clear"}

