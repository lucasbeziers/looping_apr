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
    
    col_params, col_results = st.columns(2)
    with col_params:
        # Section 1: Global Parameters
        with st.container(border=True):
            col_titles = st.columns(2)
            with col_titles[0]:
                asset_A_name = st.text_input("Name 1", placeholder="Asset A")
                price_A = st.number_input(
                    f"Price of {asset_A_name if asset_A_name else 'A'}", min_value=0.0, value=1.0, step=0.01,
                    help=f"Unit price of {asset_A_name if asset_A_name else 'A'} in dollars"
                )
            with col_titles[1]:
                asset_B_name = st.text_input("Name 2", placeholder="Asset B")
                price_B = st.number_input(
                    f"Price of {asset_B_name if asset_B_name else 'B'}", min_value=0.0, value=1.0, step=0.01,
                    help=f"Unit price of {asset_B_name if asset_B_name else 'B'} in dollars"
                )

            asset_A_name = asset_A_name if asset_A_name else "A"
            asset_B_name = asset_B_name if asset_B_name else "B"
    
        # Section 2: Protocol Parameters
        with st.container(border=True):
            
            col_A, col_B = st.columns(2)
            col_A.subheader(f"{asset_A_name} parameters")
            col_B.subheader(f"{asset_B_name} parameters")
            with col_A:
                supply_apr_pct = st.number_input(
                    f"Supply APR (%) for {asset_A_name}", min_value=0.0, value=5.0, step=0.1,
                    help=f"Annual lending rate paid for {asset_A_name}"
                )
                
            with col_B:
                borrow_apr_pct = st.number_input(
                    f"Borrow APR (%) for {asset_B_name}", value=3.0, step=0.1,
                    help=f"Annual borrowing rate for {asset_B_name}"
                )
            
            col1, col2, col3 = st.columns([2, 1, 1])

            with col1:
                initial_amount = st.number_input(
                    f"Initial Amount in {asset_A_name}", min_value=0.0, value=1.0, step=1.0,
                    help=f"Starting amount you deposit in {asset_A_name}"
                )
            with col2:
                max_ltv_pct = st.number_input(
                    "Max LTV (%)", min_value=0.0, max_value=100.0, value=75.0, step=0.1,
                    help="Maximum borrowing value allowed relative to collateral"
                )
            with col3:
                lltv_pct = st.number_input(
                    "LLTV (%)", min_value=0.0, max_value=100.0, value=80.0, step=0.1,
                    help="Protocol liquidation threshold"
                )
                if max_ltv_pct > lltv_pct:
                    lltv_pct = max_ltv_pct  
                
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

    with col_results:
        with st.container(border=True):
            st.subheader("Resulting APR Calculation")
            
            col_apr, col_hr = st.columns(2)
            
            with col_apr:
                # Calculate the resulting APR based on the leverage
                if leverage > 1:
                    effective_supply_apr = supply_apr_pct / 100.0
                    effective_borrow_apr = borrow_apr_pct / 100.0

                    # Net APR = (Supply APR * Leverage) - (Borrow APR * (Leverage - 1))
                    resulting_apr = (effective_supply_apr * leverage) - (effective_borrow_apr * (leverage - 1))
                    resulting_apr_pct = resulting_apr * 100
                else:
                    resulting_apr_pct = supply_apr_pct

                st.metric("Resulting APR (%)", f"{resulting_apr_pct:.2f}")

            with col_hr:
                # Calculate and display the Health Ratio
                if health_ratio > 0:
                    health_ratio = round(health_ratio, 2)
                else:
                    health_ratio = float("inf")

                st.metric("Health Ratio", f"{health_ratio}")

            # Calculate Liquidation Price
            if leverage > 1:
                R = (leverage - 1) / (leverage * lltv)
                st.text(f"Liquidated if 1 {asset_A_name} = {(price_A/price_B)*R:.6f} {asset_B_name} or 1 {asset_B_name} = {(price_B/price_A)/R:.6f} {asset_A_name}")
                # st.text(f"Liquidated if 1 {asset_A_name} = ${price_A*R:.6f} or 1 {asset_B_name} = ${price_B/R:.6f}")
        

if __name__ == "__main__":
    main()