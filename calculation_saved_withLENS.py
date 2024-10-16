import numpy as np

# Function to calculate I_0
def calculate_I_0(power_mW, efficacy_lm_per_W, theta_lens, theta_led):
    """Calculate the center luminous intensity I_0 in candela (cd)."""
    solid_angle_led = 2 * np.pi * (1 - np.cos(np.radians(theta_led)))  # Approximation for solid angle in steradians of a LED without a LENS
    solid_angle_lens = 2 * np.pi * (1 - np.cos(np.radians(theta_lens)))  # Approximation for solid angle in steradians of a LED with a LENS
    power_accepted = power_mW*solid_angle_lens/solid_angle_led
    luminous_flux_lm = (power_accepted / 1000) * efficacy_lm_per_W  # Convert radiant power to luminous flux (in lumens)    
    I_0 = luminous_flux_lm / solid_angle_lens  # center Luminous intensity formula
    return I_0

#  Function to calculate total illuminance E_lux_total
def calculate_E_lux_total(I_0, theta_lens, h, beta, R1, lx, ly, num_LEDs):
    """Calculate the total illuminance on the detector plane from multiple LEDs."""
    
    beta_rad = np.radians(beta)
    m = -np.log10(2) / np.log10(np.cos(np.radians(theta_lens)))  # Lambertian order of emission
    
    # Room grid
    Nx = lx * 25  # number of grid points along x-axis
    Ny = ly * 25  # number of grid points along y-axis
    x = np.linspace(-lx / 2, lx / 2, int(Nx))
    y = np.linspace(-ly / 2, ly / 2, int(Ny))
    XR, YR = np.meshgrid(x, y)  # receiver plane grid

    # Initialize total received power to zero
    E_lux_total = np.zeros_like(XR)

    # Calculate alpha angles for LEDs
    alphas = np.linspace(0, 360, num_LEDs, endpoint=False)
    alphas_rad = np.radians(alphas)

    for alpha_rad in alphas_rad:
        # LED position on a circle of radius R1
        x_led = R1 * np.cos(alpha_rad)
        y_led = R1 * np.sin(alpha_rad)

        # Distance from LED to each point on the detector plane
        tran_distanc_rec = np.sqrt((XR - x_led)**2 + (YR - y_led)**2 + h**2)

        # Direction from LED to center of detector (0,0)
        dir_to_center_x = -x_led / np.sqrt(x_led**2 + y_led**2)
        dir_to_center_y = -y_led / np.sqrt(x_led**2 + y_led**2)

        # Cosine of irradiance angle
        cos_phi = ((h / tran_distanc_rec) * np.cos(beta_rad)) + (
                    (dir_to_center_x * (XR - x_led) + dir_to_center_y * (YR - y_led)) / tran_distanc_rec * np.sin(beta_rad))

        # Ensure cos_phi values are within [-1,1]
        cos_phi = np.clip(cos_phi, -1, 1)

        # Received power from this LED
        E_lux = (I_0 * cos_phi ** m) / (tran_distanc_rec ** 2)

        # Accumulate the received power
        E_lux_total += E_lux
    
    return XR, YR, E_lux_total


def objective_function(params, I_0, theta_lens, lx, ly):
    h_opt, R1_opt, num_LEDs_opt, beta_opt = params
    
    # Call the illuminance calculation with the optimized parameters
    _, _, E_lux_total = calculate_E_lux_total(I_0, theta_lens, h_opt, beta_opt, R1_opt, lx, ly, int(num_LEDs_opt))
    
    # Calculate the uniformity score (min/max ratio)
    uniformity_score = np.min(E_lux_total) / np.max(E_lux_total)
    
    # We want to maximize the uniformity, so minimize the inverse of uniformity
    return -uniformity_score  # Negative because minimize() minimizes the function

