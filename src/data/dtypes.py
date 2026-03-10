import pandas as pd
from typing import Dict


def cast_datasets(datasets: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:

    basket = datasets.get("basket_charged")
    if basket is not None:
        basket["MAT_CODE"] = basket["MAT_CODE"].astype("string")
        basket["CHARGED_AMOUNT"] = pd.to_numeric(basket["CHARGED_AMOUNT"], errors="coerce")

    added = datasets.get("eaf_added")
    if added is not None:
        added["MAT_CODE"] = added["MAT_CODE"].astype("string")
        added["CHARGE_AMOUNT"] = pd.to_numeric(added["CHARGE_AMOUNT"], errors="coerce")

    chemistry = datasets.get("eaf_final_chemical")
    if chemistry is not None:
        chemistry["POSITIONROW"] = chemistry["POSITIONROW"].astype("string")
        for col in chemistry.columns:
            if col.startswith("VAL"):
                chemistry[col] = pd.to_numeric(
                    chemistry[col].astype(str).str.replace(",", ".", regex=False), errors="coerce"
                )

    gas = datasets.get("eaf_gaslance")
    if gas is not None:
        for col in ["O2_AMOUNT", "O2_FLOW", "GAS_AMOUNT", "GAS_FLOW"]:
            if col in gas.columns:
                gas[col] = pd.to_numeric(
                    gas[col].astype(str).str.replace(",", ".", regex=False), errors="coerce"
                )

    transformer = datasets.get("eaf_transformer")
    if transformer is not None:
        transformer["DURATION"] = pd.to_timedelta(
            "00:" + transformer["DURATION"].astype(str).str.replace(" ", "", regex=False), errors="coerce"
        ).dt.total_seconds()
        transformer["MW"] = pd.to_numeric(
            transformer["MW"].astype(str).str.replace(",", ".", regex=False), errors="coerce"
        )

    inj = datasets.get("inj_mat")
    if inj is not None:
        for col in ["INJ_AMOUNT_CARBON", "INJ_FLOW_CARBON"]:
            if col in inj.columns:
                inj[col] = pd.to_numeric(
                    inj[col].astype(str).str.replace(",", ".", regex=False), errors="coerce"
                )

    return datasets