import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

### Model with simplification

## Time
dt = 0.01
T = 25
t = np.linspace(0, T, int(T / dt))
tn = len(t)

## Tool induction time
TA1 = int(2 / dt)
TC1 = int(30 / dt)

## Parameters
# Doubling time td = ln(2)/r
rR = np.log(2)/0.5
print(rR)
rRc = np.log(2)/0.5
rS = np.log(2)/0.3
rSc = np.log(2)/0.3
print(rS)
K = 10**9  # cells
nu = np.log(2)/1.5  # h^-1
print(nu)
alpha_ = 0.8
beta_ = 0.52
lambda_ = 0.3
kA = np.log(2)/6
print(kA)
M = 0.2
n_ = 2
k_ = 10
theta_ = 3

## Functions
def theta(A):
    return k_*A**n_/(theta_**n_+A**n_)

## Initialization
R = np.zeros(tn)
Rc = np.zeros(tn)
C = np.zeros(tn)
S = np.zeros(tn)
Sc = np.zeros(tn)
A = np.zeros(tn)
ASR = np.zeros(tn)
ARS = np.zeros(tn)

R[0] = 5
A[0] = 0
Rc[0] = 0
S[0] = 5
Sc[0] = 0
C[0] = 10
ASR[0] = (S[0]+Sc[0]+C[0])/(R[0]+Rc[0]+S[0]+Sc[0]+C[0])
ARS[0] = 1-ASR[0]

## Model
for k in tqdm(range(0, tn - 1)):
    R_k = R[k]
    C_k = C[k]
    Rc_k = Rc[k]
    S_k = S[k]
    Sc_k = Sc[k]
    A_k = A[k]
    ASR_k = ASR[k]
    ARS_k = ARS[k]
    R[k+1] = R_k + dt*(rR*R_k*((ARS_k-M)/K)*(1-(R_k/K))- beta_*R_k*C_k + alpha_*R_k*S_k*((ARS_k-M)/K) + lambda_*Rc_k)
    Rc[k+1] = Rc_k + dt*(rRc*Rc_k*((ARS_k-M)/K)*(1-(Rc_k/K)) + beta_*R_k*C_k - theta(A_k)*Rc_k + alpha_*Sc_k*Rc_k*((ARS_k-M)/K)-lambda_*Rc_k)
    S[k+1] = S_k + dt*(rS*S_k*(1-(S_k/K)) - beta_*S_k*C_k + theta(A_k)*(Rc_k+C_k+Sc_k) - alpha_*R_k*S_k+lambda_*Sc_k)
    Sc[k+1] = Sc_k + dt*(rSc*Sc_k*(1-(Sc_k/K)) + beta_*S_k*C_k - theta(A_k)*Sc_k - alpha_*Sc_k*Rc_k-lambda_*Sc_k)
    if k != TC1:
        C[k+1] = C_k + dt*(-nu*C_k - theta(A_k)*C_k)
    else:
        C[k + 1] = C[0]
    if k != TA1:
        A[k + 1] = A_k + dt * (-kA*A_k)
    else:
        A[k+1] = 10
    if R[k+1] + Rc[k+1] + S[k+1] + Sc[k+1] + C[k+1] != 0:
        ASR[k+1] = (S[k+1] + Sc[k+1] + C[k+1]) / (R[k+1] + Rc[k+1] + S[k+1] + Sc[k+1] + C[k+1])
        ARS[k+1] = 1 - ASR[k+1]
    else:
        ASR[k+1] = 0
        ARS[k+1] = 0

# Create a figure with custom size
fig, axs = plt.subplots(2, 4, figsize=(20, 10))

# List of data and labels
data = [Rc, R, Sc, S, C, A, ASR, ARS]
labels = ["Rc", "R", "Sc", "S", "C", "A", "ASR", "ARS"]  # Y-axis labels

# Custom color
line_color = '#9FA4D5'

# Customize the plots
for i, ax in enumerate(axs.flat):
    ax.plot(t, data[i], color=line_color, linewidth=2)
    ax.set_xlabel('t in hours', fontsize=12)
    ax.set_ylabel(f"{labels[i]}(t)", fontsize=12)  # Use labels instead of titles
    ax.set_title(f"Evolution of {labels[i]}", fontsize=14, fontweight='bold')  # Bold titles
    ax.grid(True)

    if labels[i] == "A":
        # Add an arrow and legend on the A plot at t=2
        ax.annotate("Induction", xy=(2, A[2]), xytext=(4, A[2] + 0.2),
                    arrowprops=dict(arrowstyle='->', color='black'), fontsize=12, fontweight='bold')

# Automatically adjust spacing between subplots
plt.tight_layout()

# Adjust the spacing of y-axes
plt.subplots_adjust(wspace=0.3, hspace=0.5)

# Show the figure
plt.show()

