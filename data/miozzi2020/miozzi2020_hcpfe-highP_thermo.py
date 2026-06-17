'''
Script that transforms the raw thermo data
"miozzi2020_hcpfe-and-mgo_thermo_raw.dat"
into the database format file
"miozzi2020_hcpfe-highP_thermo.dat"
'''

import os
import sys
import pandas as pd

FOLDER = os.path.dirname("./data/miozzi2020/")
INPUT_FILE = os.path.join(FOLDER, "miozzi2020_hcpfe-and-mgo_thermo_raw.dat")
OUTPUT_FILE = os.path.join(FOLDER, "miozzi2020_hcpfe-highP_thermo.dat")

# Constants
NA = 6.02214076e23          # Avogadro number, mol^-1
M_Fe = 55.845e-3            # Iron molar mass, kg/mol
m_Fe = M_Fe / NA            # Atomic mass, kg per atom
n_atoms = 2                 # number of atoms per crystal lattice, iron hcp
mass_cell_kg = n_atoms * M_Fe / NA  # mass of crystal lattice kg

if __name__ == "__main__":
    input_path = INPUT_FILE
    output_path = OUTPUT_FILE

    # Input dataframe
    df = pd.read_csv(input_path, sep="\t", engine="python", comment="#")
    # Output dataframe
    df2 = pd.DataFrame()

    # Convert lattice volume in Angstrom^3 to density in SI, and propagate uncertainty
    df2["rho[kg/m^3]"] = mass_cell_kg / (df["V(A^3)"] * 1e-30)
    df2["drho[kg/m^3]"] = df2["rho[kg/m^3]"] * df["dV"] / df["V(A^3)"]
    # Convert pressure from GPa to Pa
    df2["P[Pa]"] = df["P(Gpa)"] * 1e9
    df2["dP[Pa]"] = df["dP"] * 1e9
    # Nothing to do with temperature
    df2["T[K]"] = df["T"]
    df2["dT[K]"] = df["dT"]

    # Export density and pressure in scientific notation
    list_columns_to_scientific = ["rho[kg/m^3]", 
                                  "drho[kg/m^3]", 
                                  "P[Pa]", 
                                  "dP[Pa]"]
    for col in list_columns_to_scientific:
        df2[col] = df2[col].map(lambda x: f"{x:.6e}")

    # Export to final file
    df2.to_csv(output_path, sep="\t", index=False)
