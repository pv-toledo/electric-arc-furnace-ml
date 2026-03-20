import matplotlib.pyplot as plt
import pandas as pd

def plot_heat_profile(heat_id: str, eaf_transformer: pd.DataFrame, eaf_gaslance: pd.DataFrame, inj_mat: pd.DataFrame, eaf_temp: pd.DataFrame) -> None:
    
    fig, axes = plt.subplots(4, 1, figsize=(13,12), sharex=False)
    fig.suptitle(f"Heat: {heat_id}", fontsize=13, y=1.01)

    tr = (
        eaf_transformer[eaf_transformer["HEATID"] == heat_id]
        .sort_values("STARTTIME")
        .copy()
    )

    tr["min"] = (tr["STARTTIME"] - tr["STARTTIME"].iloc[0]).dt.total_seconds() / 60

    axes[0].step(tr["min"], tr["MW"], where="post", linewidth=1.2, color="steelblue")
    axes[0].set(ylabel="Power (MW)", title="Transformer Power")
    axes[0].fill_between(tr["min"], tr["MW"], step="post", alpha=0.15, color="steelblue")

    gl = (
        eaf_gaslance[eaf_gaslance["HEATID"] == heat_id]
        .sort_values("REVTIME")
        .copy()
    )

    gl["min"] = (gl["REVTIME"] - gl["REVTIME"].iloc[0]).dt.total_seconds() / 60
    axes[1].plot(gl["min"], gl["O2_AMOUNT"].cumsum(), linewidth=1.2, color="tomato")
    axes[1].set(ylabel="Cumulative O2 (Nm³)", title="O2 Lance")

    inj = (
    inj_mat[inj_mat["HEATID"] == heat_id]
    .sort_values("REVTIME")
    .copy()
    )

    inj["min"] = (inj["REVTIME"] - inj["REVTIME"].iloc[0]).dt.total_seconds() / 60

    axes[2].plot(inj["min"], inj["INJ_AMOUNT_CARBON"].cumsum(), linewidth=1.2, color="goldenrod")
    axes[2].set(ylabel="Cumulative carbon (kg)", title="Carbon injection") 

    
    temp = eaf_temp[eaf_temp["HEATID"] == heat_id].sort_values("DATETIME").copy()
    t0 = tr["STARTTIME"].iloc[0]  
    temp["min"] = (temp["DATETIME"] - t0).dt.total_seconds() / 60

    axes[3].scatter(temp["min"], temp["TEMP"], s=60, zorder=5, color="darkgreen")
    axes[3].plot(temp["min"], temp["TEMP"], linewidth=0.8, linestyle="--", color="darkgreen", alpha=0.5)
    axes[3].scatter(temp["min"].iloc[-1], temp["TEMP"].iloc[-1], s=120, color="red", zorder=6, label="Tapping")
    axes[3].set(ylabel="Temperature (°C)", title="Temperature Measurements", xlabel="Time (min)")
    axes[3].legend(fontsize=9)

    for ax in axes:
        ax.grid(True, alpha=0.4)

    plt.tight_layout()
    plt.show()