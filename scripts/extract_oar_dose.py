import os
import pandas as pd
import numpy as np

data_dir = "data/raw/openkbp/provided-data/train-pats"

structures = [
    "Brainstem",
    "SpinalCord",
    "Parotid_L",
    "Parotid_R"
]

results = []

for patient in os.listdir(data_dir):

    patient_path = os.path.join(data_dir, patient)

    dose_path = os.path.join(patient_path, "dose.csv")

    if not os.path.exists(dose_path):
        continue

    dose = pd.read_csv(dose_path, header=None).astype(float).values.flatten()

    for structure in structures:

        structure_path = os.path.join(patient_path, f"{structure}.csv")

        if not os.path.exists(structure_path):
            continue

        mask = pd.read_csv(structure_path, header=None).astype(float).values.flatten()

        organ_voxels = dose[mask > 0]

        if len(organ_voxels) == 0:
            continue

        mean_dose = organ_voxels.mean()

        results.append({
            "patient": patient,
            "structure": structure,
            "mean_dose": mean_dose
        })

df = pd.DataFrame(results)

df.to_csv("data/processed/oar_dose_summary.csv", index=False)

print("Dataset creado:", df.shape)