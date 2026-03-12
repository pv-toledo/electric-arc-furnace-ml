import pandas as pd
from typing import Dict


def cast_datasets(datasets: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:

    temperature = datasets.get("eaf_temp")
    if temperature is not None:
        temperature["TEMP"] = pd.to_numeric(temperature["TEMP"], errors="coerce")
        temperature["VALO2_PPM"] = pd.to_numeric(temperature["VALO2_PPM"], errors="coerce")
        temperature["DATETIME"] = pd.to_datetime(temperature["DATETIME"], format="%Y-%m-%d %H:%M:%S", errors="coerce")

    basket = datasets.get("basket_charged")
    if basket is not None:
        basket["CHARGED_AMOUNT"] = pd.to_numeric(basket["CHARGED_AMOUNT"], errors="coerce")
        basket["DATETIME"] = pd.to_datetime(basket["DATETIME"], format="%Y-%m-%d %H:%M:%S", errors="coerce")


    added = datasets.get("eaf_added")
    if added is not None:
        added["CHARGE_AMOUNT"] = pd.to_numeric(added["CHARGE_AMOUNT"], errors="coerce")
        added["DATETIME"] = pd.to_datetime(added["DATETIME"], format="%Y-%m-%d %H:%M:%S", errors="coerce")


    chemistry = datasets.get("eaf_final_chemical")
    if chemistry is not None:
        chemistry["DATETIME"] = pd.to_datetime(chemistry["DATETIME"], format="%Y-%m-%d %H:%M:%S", errors="coerce")

        for col in chemistry.columns:
            if col.startswith("VAL"):
                chemistry[col] = pd.to_numeric(
                    chemistry[col].astype("string").str.replace(",", ".", regex=False), errors="coerce"
                )

    gas = datasets.get("eaf_gaslance")
    if gas is not None:
        gas["REVTIME"] = pd.to_datetime(gas["REVTIME"], format="%Y-%m-%d %H:%M:%S,%f", errors="coerce")

        for col in ["O2_AMOUNT", "O2_FLOW", "GAS_AMOUNT", "GAS_FLOW"]:
            if col in gas.columns:
                gas[col] = pd.to_numeric(
                    gas[col].astype("string").str.replace(",", ".", regex=False), errors="coerce"
                )

    transformer = datasets.get("eaf_transformer")
    if transformer is not None:
        transformer["STARTTIME"] = pd.to_datetime(transformer["STARTTIME"], format="%Y-%m-%d %H:%M:%S", errors="coerce")
        transformer["DURATION"] = pd.to_timedelta(
            "00:" + transformer["DURATION"].astype("string").str.replace(" ", "", regex=False), errors="coerce"
        ).dt.total_seconds()
        transformer["MW"] = pd.to_numeric(
            transformer["MW"].astype("string").str.replace(",", ".", regex=False), errors="coerce"
        )

    inj = datasets.get("inj_mat")
    if inj is not None:
        for col in ["INJ_AMOUNT_CARBON", "INJ_FLOW_CARBON"]:
            if col in inj.columns:
                inj[col] = pd.to_numeric(
                    inj[col].astype("string").str.replace(",", ".", regex=False), errors="coerce"
                )

    ferro = datasets.get("ferro")
    if ferro is not None:
        for col in ferro.columns:
            if col != "Description" and col != "MAT_CODE":
                ferro[col] = pd.to_numeric(
                    ferro[col].astype("string").str.replace(",", ".", regex=False), errors="coerce"
                )

    return datasets