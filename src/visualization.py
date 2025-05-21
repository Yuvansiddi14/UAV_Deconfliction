import matplotlib.pyplot as plt
import matplotlib.animation as animation
import plotly.graph_objects as go

def get_position_at_time(waypoints, t):
    """Interpolates drone position at time t."""
    if t <= waypoints[0]["time"]:
        return waypoints[0]
    if t >= waypoints[-1]["time"]:
        return waypoints[-1]
    for i in range(len(waypoints) - 1):
        w1, w2 = waypoints[i], waypoints[i + 1]
        if w1["time"] <= t <= w2["time"]:
            ratio = (t - w1["time"]) / (w2["time"] - w1["time"])
            pos = {
                "x": w1["x"] + ratio * (w2["x"] - w1["x"]),
                "y": w1["y"] + ratio * (w2["y"] - w1["y"]),
                "time": t
            }
            if "z" in w1 and "z" in w2:
                pos["z"] = w1["z"] + ratio * (w2["z"] - w1["z"])
            return pos
    return waypoints[-1]

def visualize_combined(primary_mission, simulated_flights, conflicts):
    """Automatically selects 2D or enhanced 4D visualization based on altitude presence."""
    
    # Detect if altitude ('z') is included in data
    has_altitude = any("z" in wp for wp in primary_mission["waypoints"])

    if not has_altitude:
        #### 👉 Animated 2D Visualization ####
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.set_xlim(-5, 25)
        ax.set_ylim(-5, 15)
        ax.set_xlabel("X Coordinate")
        ax.set_ylabel("Y Coordinate")
        ax.set_title("Animated 2D Drone Mission")
        ax.grid(True)

        p_x = [wp["x"] for wp in primary_mission["waypoints"]]
        p_y = [wp["y"] for wp in primary_mission["waypoints"]]
        ax.plot(p_x, p_y, "b--", alpha=0.3, label="Primary Path")

        for sim in simulated_flights:
            sim_x = [wp["x"] for wp in sim["waypoints"]]
            sim_y = [wp["y"] for wp in sim["waypoints"]]
            ax.plot(sim_x, sim_y, "r--", alpha=0.3, label=f"Drone {sim['id']}")

        primary_marker, = ax.plot([], [], "bo", markersize=8, label="Primary Drone")
        sim_markers = {sim["id"]: ax.plot([], [], "ro", markersize=6)[0] for sim in simulated_flights}
        conflict_markers, = ax.plot([], [], "rx", markersize=10, label="Conflict Points")
        time_text = ax.text(0.02, 0.95, "", transform=ax.transAxes)

        ani = animation.FuncAnimation(fig, lambda frame: update_2d(frame, primary_marker, sim_markers, conflict_markers, time_text, primary_mission, simulated_flights, conflicts), frames=100, interval=100, blit=True)
        plt.legend()
        plt.show()

    else:
        #### 👉 Enhanced 4D Visualization ####
        fig = go.Figure()

        for sim in simulated_flights:
            fig.add_trace(go.Scatter3d(
                x=[wp["x"] for wp in sim["waypoints"]],
                y=[wp["y"] for wp in sim["waypoints"]],
                z=[wp["z"] for wp in sim["waypoints"]],
                mode="lines+markers",
                marker=dict(size=4, color="red"),
                name=f"Drone {sim['id']}"
            ))

        fig.add_trace(go.Scatter3d(
            x=[wp["x"] for wp in primary_mission["waypoints"]],
            y=[wp["y"] for wp in primary_mission["waypoints"]],
            z=[wp["z"] for wp in primary_mission["waypoints"]],
            mode="lines+markers",
            marker=dict(size=6, color="blue"),
            name="Primary Drone"
        ))

        fig.update_layout(
            title="4D Drone Mission Animation",
            scene=dict(xaxis_title="X", yaxis_title="Y", zaxis_title="Altitude"),
            updatemenus=[dict(
                type="buttons",
                showactive=False,
                buttons=[dict(label="Play", method="animate",
                              args=[None, {"frame": {"duration": 100, "redraw": True},
                                           "fromcurrent": True}])])]
        )

        fig.show()

