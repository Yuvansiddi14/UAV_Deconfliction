import matplotlib.pyplot as plt
import plotly.graph_objects as go

def visualize_2d(primary_mission, simulated_flights, safety_buffer, conflicts=None):
    """
    Create a 2D matplotlib plot showing the primary mission and simulated flights.
    Conflict points are highlighted.
    """
    plt.figure(figsize=(10, 8))

    # Plot the primary mission route
    p_x = [wp["x"] for wp in primary_mission["waypoints"]]
    p_y = [wp["y"] for wp in primary_mission["waypoints"]]
    plt.plot(p_x, p_y, "bo-", label="Primary Mission")

    # Plot simulated flights
    for sim in simulated_flights:
        sim_x = [wp["x"] for wp in sim["waypoints"]]
        sim_y = [wp["y"] for wp in sim["waypoints"]]
        plt.plot(sim_x, sim_y, "r.-", label=f"Simulated Drone {sim['id']}")

    # Highlight conflict points
    if conflicts:
        for conflict in conflicts:
            cp = conflict["conflict_at"]
            plt.plot(cp["x"], cp["y"], "kx", markersize=12)
            plt.text(cp["x"], cp["y"], f"Conflict: {conflict['sim_drone']}", fontsize=9)

    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.title("2D Drone Mission & Simulated Flight Paths")
    plt.legend()
    plt.grid(True)
    plt.show()

def visualize_4d(primary_mission, simulated_flights, safety_buffer, conflicts=None):
    """
    Create a 3D Plotly visualization (extra credit) that shows a 4D view
    (3D spatial coordinates with time represented via color).
    """
    # Ensure primary mission has altitude data
    p_x, p_y, p_z, p_time = [], [], [], []
    for wp in primary_mission["waypoints"]:
        if "z" not in wp:
            print("Primary mission is missing altitude data. 4D visualization cannot be rendered.")
            return
        p_x.append(wp["x"])
        p_y.append(wp["y"])
        p_z.append(wp["z"])
        p_time.append(wp["time"])

    fig = go.Figure()

    # Add primary mission trace
    fig.add_trace(go.Scatter3d(
        x=p_x,
        y=p_y,
        z=p_z,
        mode="lines+markers",
        marker=dict(size=6, color=p_time, colorscale="Viridis", colorbar=dict(title="Time")),
        line=dict(color="blue", width=4),
        name="Primary Mission"
    ))

    # Add simulated flights
    for sim in simulated_flights:
        sim_x, sim_y, sim_z, sim_time = [], [], [], []
        valid = True
        for wp in sim["waypoints"]:
            if "z" not in wp:
                valid = False
                break
            sim_x.append(wp["x"])
            sim_y.append(wp["y"])
            sim_z.append(wp["z"])
            sim_time.append(wp["time"])
        if not valid:
            continue
        fig.add_trace(go.Scatter3d(
            x=sim_x,
            y=sim_y,
            z=sim_z,
            mode="lines+markers",
            marker=dict(size=4, color=sim_time, colorscale="Jet"),
            line=dict(width=2),
            name=f"Simulated Drone {sim['id']}"
        ))

    # Highlight conflict points if available
    if conflicts:
        conflict_x, conflict_y, conflict_z, conflict_labels = [], [], [], []
        for conflict in conflicts:
            cp = conflict["conflict_at"]
            if "z" in cp:
                conflict_x.append(cp["x"])
                conflict_y.append(cp["y"])
                conflict_z.append(cp["z"])
                conflict_labels.append(f"{conflict['sim_drone']} at t={cp['time']}")
        if conflict_x:
            fig.add_trace(go.Scatter3d(
                x=conflict_x,
                y=conflict_y,
                z=conflict_z,
                mode="markers+text",
                marker=dict(size=8, color="red"),
                text=conflict_labels,
                name="Conflicts"
            ))

    fig.update_layout(
        scene=dict(
            xaxis_title="X Coordinate",
            yaxis_title="Y Coordinate",
            zaxis_title="Altitude"
        ),
        title="4D (3D + Time) Drone Mission Visualization",
        margin=dict(l=0, r=0, b=0, t=30)
    )
    fig.show()


