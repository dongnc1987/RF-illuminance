# import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from matplotlib.gridspec import GridSpec
import random
from scipy.optimize import minimize
from calculation_saved_withLENS import *

# Set the Streamlit page configuration
st.set_page_config(page_title="Distribution of illuminance by LEDs", layout="wide")

# Calculation option for users
cal_option = st.sidebar.selectbox("Distribution of illuminance by LEDs", options=["Please choose", "Mannual calculation", "Optimization"])

# Use the selected value to control behavior
if cal_option == 'Please choose':
    st.subheader("Please select a measurement type from the dropdown...")
elif cal_option == 'Mannual calculation':
    # Header
    st.markdown("<h1 class='header'>Distribution of illuminance by LEDs</h1>", unsafe_allow_html=True)
  

    # Inputs for interactive parameters
    power_mW, theta_led = st.columns(2)
    with power_mW:
        power_mW = st.number_input('Typical LED power in mW', min_value=1.0, max_value=1500.0, value=880.0)
    with theta_led:
        theta_led = st.number_input('Semi-angle at half power (theta_led) without a LENS', min_value=1.0, max_value=90.0, value=70.0)

    theta_lens, efficacy, lx, ly = st.columns(4)
    with theta_lens:
        theta_lens = st.number_input('Semi-angle at half power (theta_lens)', min_value=0.0, max_value=90.0, value=45.0)
    with efficacy:
        efficacy_lm_per_W = st.number_input('Luminous efficacy of LED (lm/W)', min_value=200.0, max_value=1000.0, value=683.0)  # in lumens per watt
    with lx:
        lx = st.number_input('Width of the receiver plane (cm)', min_value=1.0, max_value=10.0, value=2.5)
    with ly:
        ly = st.number_input('Lengh of the receiver plane (cm)', min_value=1.0, max_value=10.0, value=2.5)


    h, beta, num_LEDs, R1 = st.columns(4)
    with h:
        h = st.number_input('Height of LEDs from the receiver plane (cm)', min_value=1.0, max_value=100.0, value=10.0)
    with R1:
        R1 = st.number_input('Radius of the circle plane inclusive LEDs (cm)', min_value=1.0, max_value=50.0, value=10.0)
    with beta:
        beta = st.number_input('Tilt angle (beta) of LEDs toward center (degrees)', min_value=0.0, max_value=90.0, value=0.0)
    with num_LEDs:
        num_LEDs = st.number_input('Number of LEDs on the circle', min_value=1, max_value=50, value=1)

    # Calculate I_0 using the function
    I_0 = calculate_I_0(power_mW, efficacy_lm_per_W, theta_lens, theta_led)

    # Calculate E_lux_total using the function
    XR, YR, E_lux_total = calculate_E_lux_total(I_0, theta_lens, h, beta, R1, lx, ly, num_LEDs)

    # Calculation option for users
    fig_option = st.selectbox("Displayed figure options for visualization", options=["Please choose", "3D view", "Full-size 2D view", "3D and 2D views", "Zoom-out 2D"])
    if fig_option == "Please choose":
        st.subheader("Please select a measurement type from the dropdown...")
    elif fig_option == "3D view":
        # Plotting
        fig = plt.figure(figsize=(18, 4.5))

        # 3D subplot
        ax1 = fig.add_subplot(131, projection='3d')
        surf = ax1.plot_surface(XR, YR, E_lux_total, cmap='viridis')
        fig.colorbar(surf, ax=ax1, fraction=0.037, pad=0.08)
        ax1.set_xlabel('X (cm)')
        ax1.set_ylabel('Y (cm)')
        ax1.set_title('Distribution of illuminance (lx) in 3D view')
        # Set scale according to lx and ly
        ax1.set_xlim([-lx / 2, lx / 2])
        ax1.set_ylim([-ly / 2, ly / 2])
        # Show the plots in Streamlit
        st.pyplot(fig)
    elif fig_option == "Full-size 2D view":
        # Plotting
        fig = plt.figure(figsize=(18, 4.5))

        # 2D subplot
        ax2 = fig.add_subplot(133)
        contour = ax2.contourf(XR, YR, E_lux_total, 50, cmap='viridis')
        fig.colorbar(contour, ax=ax2, fraction=0.046, pad=0.04)
        ax2.set_xlabel('X (cm)')
        ax2.set_ylabel('Y (cm)')
        ax2.set_title('Distribution of illuminance (lx) in 2D view')
        ax2.set_aspect('equal')
        # Set scale according to lx and ly
        # ax2.set_xlim([-2.5, 2.5])
        # ax2.set_ylim([-2.5, 2.5])
        ax2.set_aspect('equal')  # Maintain equal aspect ratio

        # Show the plots in Streamlit
        st.pyplot(fig)
    elif fig_option == "3D and 2D views":
        # Plotting
        fig = plt.figure(figsize=(18, 4.5))

        # 3D subplot
        ax1 = fig.add_subplot(131, projection='3d')
        surf = ax1.plot_surface(XR, YR, E_lux_total, cmap='viridis')
        fig.colorbar(surf, ax=ax1, fraction=0.046, pad=0.07)
        ax1.set_xlabel('X (cm)')
        ax1.set_ylabel('Y (cm)')
        ax1.set_title('Distribution of illuminance (lx) in 3D view')
        # Set scale according to lx and ly
        ax1.set_xlim([-lx / 2, lx / 2])
        ax1.set_ylim([-ly / 2, ly / 2])


        # 2D subplot
        ax2 = fig.add_subplot(132)
        contour = ax2.contourf(XR, YR, E_lux_total, 50, cmap='viridis')
        fig.colorbar(contour, ax=ax2, fraction=0.046, pad=0.04)
        ax2.set_xlabel('X (cm)')
        ax2.set_ylabel('Y (cm)')
        ax2.set_title('Distribution of illuminance (lx) in 2D view')
        ax2.set_aspect('equal')
        # Set scale according to lx and ly
        ax2.set_xlim([-lx / 2, lx / 2])
        ax2.set_ylim([-ly / 2, ly / 2])
        ax2.set_aspect('equal')  # Maintain equal aspect ratio

        # 2D subplot
        ax2 = fig.add_subplot(133)
        contour = ax2.contourf(XR, YR, E_lux_total, 50, cmap='viridis')
        fig.colorbar(contour, ax=ax2, fraction=0.046, pad=0.04)
        ax2.set_xlabel('X (cm)')
        ax2.set_ylabel('Y (cm)')
        ax2.set_title('Distribution of illuminance (lx) in 2D view')
        ax2.set_aspect('equal')
        # Set scale according to lx and ly
        ax2.set_xlim([-2.5, 2.5])
        ax2.set_ylim([-2.5, 2.5])
        ax2.set_aspect('equal')  # Maintain equal aspect ratio

        # Show the plots in Streamlit
        st.pyplot(fig)
    else:
        # Extract the center row and column for the line scan
        center_row = E_lux_total[E_lux_total.shape[0] // 2, :]
        center_column = E_lux_total[:, E_lux_total.shape[1] // 2]

        # Create a plot layout with contour plot and line scans
        fig = plt.figure(figsize=(10, 6))  # Adjusted figure size
        gs = GridSpec(3, 3, height_ratios=[3, 1, 1], width_ratios=[1, 4, 0.1])

        # Main contour plot
        ax_main = fig.add_subplot(gs[0, 1])
        contour = ax_main.contourf(XR, YR, E_lux_total, levels=50, cmap='viridis')
        ax_main.set_xlabel("X-axis")
        ax_main.set_ylabel("Y-axis")
        ax_main.set_xlim([-2.5, 2.5])  # Set the limits for X-axis
        ax_main.set_ylim([-2.5, 2.5])  # Set the limits for Y-axis

        # Remove x-ticks for the main contour plot to avoid overlap with the x-scan
        ax_main.tick_params(labelbottom=False)

        # Line scan along the X-axis (below the main plot)
        ax_xscan = fig.add_subplot(gs[1, 1], sharex=ax_main)
        ax_xscan.plot(XR[0, :], center_row, color='blue')
        ax_xscan.set_xlabel("X-axis")
        ax_xscan.set_ylabel("Intensity")
        ax_xscan.set_xlim([-2.5, 2.5])  # Set the same X-axis limits as the main plot

        # Line scan along the Y-axis (to the left of the main plot)
        ax_yscan = fig.add_subplot(gs[0, 0], sharey=ax_main)
        ax_yscan.plot(center_column, YR[:, 0], color='green')
        ax_yscan.set_xlabel("Intensity")
        ax_yscan.set_ylabel("Y-axis")
        ax_yscan.set_ylim([-2.5, 2.5])  # Set the same Y-axis limits as the main plot
        ax_yscan.invert_xaxis()  # Flip to align with the main plot

        # Add a color bar for the contour plot
        cbar_ax = fig.add_subplot(gs[0, 2])  # Color bar positioned to the right of the contour plot
        fig.colorbar(contour, cax=cbar_ax, orientation='vertical')

        plt.tight_layout()

        # Show the plot in Streamlit
        st.pyplot(fig)
else:
    # Header
    st.markdown("<h1 class='header'>Optimized distribution of illuminance by LEDs</h1>", unsafe_allow_html=True)
    
    # Inputs for interactive parameters
    power_mW, theta_led = st.columns(2)
    with power_mW:
        power_mW = st.number_input('Typical LED power in mW', min_value=1.0, max_value=1500.0, value=880.0)
    with theta_led:
        theta_led = st.number_input('Semi-angle at half power (theta_led) without a LENS', min_value=1.0, max_value=90.0, value=70.0)

    theta_lens, efficacy, lx, ly = st.columns(4)
    with theta_lens:
        theta_lens = st.number_input('Semi-angle at half power (theta_lens)', min_value=0.0, max_value=90.0, value=45.0)
    with efficacy:
        efficacy_lm_per_W = st.number_input('Luminous efficacy of LED (lm/W)', min_value=200.0, max_value=1000.0, value=683.0)  # in lumens per watt
    with lx:
        lx = st.number_input('Width of the receiver plane (cm)', min_value=1.0, max_value=10.0, value=2.5)
    with ly:
        ly = st.number_input('Lengh of the receiver plane (cm)', min_value=1.0, max_value=10.0, value=2.5)
    # Calculate I_0 using the function
    I_0 = calculate_I_0(power_mW, efficacy_lm_per_W, theta_lens, theta_led)

    # Random initial guesses for the optimization parameters
    h_init = random.uniform(5, 50)  # Random height between 5 and 50 cm
    R1_init = random.uniform(5, 30)  # Random radius between 5 and 30 cm
    num_LEDs_init = random.randint(1, 50)  # Random number of LEDs between 1 and 50
    beta_init = random.uniform(0, 45)  # Random tilt angle between 0° and 45°

    initial_guess = [h_init, R1_init, num_LEDs_init, beta_init]  # Start with random initial values

    # Set bounds for the parameters
    bounds = [(1.0, 20.0),  # h in cm
            (2.0, 10.0),  # R1 in cm
            (1.0, 6.0),  # num_LEDs
            (0.0, 60.0)]  # beta in degrees

    # Optimize the parameters using the minimize function
    result = minimize(objective_function, initial_guess, args=(I_0, theta_lens, lx, ly), bounds=bounds, method='L-BFGS-B')

    # Extract the optimized parameters
    h_opt, R1_opt, num_LEDs_opt, beta_opt = result.x

    # Recalculate the illuminance with the optimized parameters
    XR_opt, YR_opt, E_lux_total_opt = calculate_E_lux_total(I_0, theta_lens, h_opt, beta_opt, R1_opt, lx, ly, int(num_LEDs_opt))
    
    # Display the optimized parameters
    st.write(f"Optimized Height (h): {h_opt:.2f} cm")
    st.write(f"Optimized Tilt angle (beta): {beta_opt:.2f} degrees")
    st.write(f"Optimized Number of LEDs: {int(num_LEDs_opt)}")
    st.write(f"Optimized Radius of LED circle (R1): {R1_opt:.2f} cm")

    # Extract the center row and column for the line scan (optimized)
    center_row_opt = E_lux_total_opt[E_lux_total_opt.shape[0] // 2, :]
    center_column_opt = E_lux_total_opt[:, E_lux_total_opt.shape[1] // 2]

    # Create a plot layout with contour plot and line scans (optimized)
    fig_opt = plt.figure(figsize=(10, 6))
    gs_opt = GridSpec(3, 3, height_ratios=[3, 1, 1], width_ratios=[1, 4, 0.1])

    # Main contour plot for optimized case
    ax_main_opt = fig_opt.add_subplot(gs_opt[0, 1])
    contour_opt = ax_main_opt.contourf(XR_opt, YR_opt, E_lux_total_opt, levels=50, cmap='viridis')
    ax_main_opt.set_xlabel("X-axis")
    ax_main_opt.set_ylabel("Y-axis")
    # ax_main_opt.set_xlim([-1.25, 1.25])
    # ax_main_opt.set_ylim([-1.25, 1.25])
    ax_main_opt.tick_params(labelbottom=False)

    # Line scan along the X-axis (below the main plot)
    ax_xscan_opt = fig_opt.add_subplot(gs_opt[1, 1], sharex=ax_main_opt)
    ax_xscan_opt.plot(XR_opt[0, :], center_row_opt, color='blue')
    ax_xscan_opt.set_xlabel("X-axis")
    ax_xscan_opt.set_ylabel("Intensity")
    # ax_main_opt.set_xlim([-1.25, 1.25])

    # Line scan along the Y-axis (to the left of the main plot)
    ax_yscan_opt = fig_opt.add_subplot(gs_opt[0, 0], sharey=ax_main_opt)
    ax_yscan_opt.plot(center_column_opt, YR_opt[:, 0], color='green')
    ax_yscan_opt.set_xlabel("Intensity")
    ax_yscan_opt.set_ylabel("Y-axis")
    # ax_main_opt.set_ylim([-1.25, 1.25])
    ax_yscan_opt.invert_xaxis()

    # Add a color bar for the contour plot
    cbar_ax_opt = fig_opt.add_subplot(gs_opt[0, 2])
    fig_opt.colorbar(contour_opt, cax=cbar_ax_opt, orientation='vertical')

    plt.tight_layout()

    # Show the optimized plot in Streamlit
    st.pyplot(fig_opt)





