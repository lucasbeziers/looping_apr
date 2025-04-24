# app.py
import streamlit as st

def main():
    st.set_page_config(page_title="Simplified APR Looping", layout="wide")
    st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 10%;
                    padding-right: 10%;
                }
        </style>
        """, unsafe_allow_html=True)
    st.title("Simplified APR Looping Simulation")
    
    # Section 1: Global Parameters
    with st.container(border=True):
        col_titles = st.columns(2)
        with col_titles[0]:
            asset_A_name = st.text_input("Name 1", placeholder="Asset A")
            price_A = st.number_input(
                f"Price of {asset_A_name if asset_A_name else 'Asset A'}", min_value=0.0, value=1.0, step=0.01,
                help=f"Unit price of {asset_A_name if asset_A_name else 'Asset A'} in dollars"
            )
        with col_titles[1]:
            asset_B_name = st.text_input("Name 2", placeholder="Asset B")
            price_B = st.number_input(
                f"Price of {asset_B_name if asset_B_name else 'Asset B'}", min_value=0.0, value=1.0, step=0.01,
                help=f"Unit price of {asset_B_name if asset_B_name else 'Asset B'} in dollars"
            )

        asset_A_name = asset_A_name if asset_A_name else "Asset A"
        asset_B_name = asset_B_name if asset_B_name else "Asset B"

    # Section 2: Protocol Parameters
    with st.container(border=True):
        col1, col2 = st.columns(2)

        with col1:
            st.subheader(f"Parameters for {asset_A_name}")
            initial_amount = st.number_input(
                f"Initial Amount in {asset_A_name}", min_value=0.0, value=100.0, step=1.0,
                help=f"Starting amount you deposit in {asset_A_name}"
            )
            supply_apr_pct = st.number_input(
                f"Supply APR (%) for {asset_A_name}", min_value=0.0, value=5.0, step=0.1,
                help=f"Annual lending rate paid for {asset_A_name}"
            )
        with col2:
            st.subheader(f"Parameters for {asset_B_name}")
            col3, col4 = st.columns(2)
            with col3:
                max_ltv_pct = st.number_input(
                    "Max LTV (%)", min_value=0.0, max_value=100.0, value=75.0, step=0.1,
                    help="Maximum borrowing value allowed relative to collateral"
                )
            with col4:
                lltv_pct = st.number_input(
                    "LLTV (%)", min_value=0.0, max_value=100.0, value=80.0, step=0.1,
                    help="Protocol liquidation threshold"
                )
                if max_ltv_pct > lltv_pct:
                    lltv_pct = max_ltv_pct
            borrow_apr_pct = st.number_input(
                f"Borrow APR (%) for {asset_B_name}", value=7.0, step=0.1,
                help=f"Annual borrowing rate for {asset_B_name}"
            )
        # Calculate max leverage from max LTV
        max_ltv = max_ltv_pct / 100.0
        lltv = lltv_pct / 100.0

        if max_ltv > 0 and max_ltv < 1:
            leverage_max = round(1 / (1 - max_ltv), 2)
        else:
            leverage_max = 1.0

        st.markdown(f"**Maximum Allowed Leverage: {leverage_max}x**")

        leverage = st.slider(
            "Desired Leverage", min_value=1.0, max_value=leverage_max, value=1.0, step=0.1,
            help="Total desired leverage (e.g., 1 = no looping, 2 = double exposure)"
        )

    # Automatically calculate target LTV from leverage
    if leverage > 0:
        ltv_target = (leverage - 1) / leverage
    else:
        ltv_target = 0

    # Calculate Health Ratio
    if ltv_target > 0:
        health_ratio = (1 * lltv) / (ltv_target)
    else:
        health_ratio = float("inf")

    if st.button("Run Simulation"):
        params = {
            f"initial_amount_{asset_A_name}": initial_amount,
            f"supply_apr_{asset_A_name}": supply_apr_pct / 100.0,
            f"borrow_apr_{asset_B_name}": borrow_apr_pct / 100.0,
            "max_ltv": max_ltv,
            "liquidation_threshold": lltv,
            "leverage": leverage,
            "ltv_target": round(ltv_target, 4),
            "health_ratio": round(health_ratio, 4),
            f"price_{asset_A_name}": price_A,
            f"price_{asset_B_name}": price_B
        }
        st.subheader("Input Parameters for Simulation")
        st.json(params)


if __name__ == "__main__":
    main()