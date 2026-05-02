import gradio as gr
import pandas as pd

# Dummy data (to avoid crash)
n_days = 31
baseline_end = 21
theta = 0.35
collapse_days = [23, 24]

pmes_df = pd.DataFrame({
    'merchant': ['M1','M2','M3'],
    'PMES': [0.82, 0.65, 0.48],
    'V_m': [120, 80, 45],
    'R_m': [0.1, 0.3, 0.6]
})

def analyze_transaction(txn_type, step, amount,
                         old_bal_orig, new_bal_orig,
                         old_bal_dest, new_bal_dest):

    balance_drain  = old_bal_orig - new_bal_orig
    amount_ratio   = amount / (old_bal_orig + 1)
    zero_orig      = new_bal_orig == 0

    risk_score = 0.0
    flags      = []

    if txn_type in ['TRANSFER', 'CASH_OUT']:
        risk_score += 0.3
        flags.append("High-risk transaction type")
    if zero_orig:
        risk_score += 0.4
        flags.append("Account fully drained")
    if amount_ratio > 0.9:
        risk_score += 0.2
        flags.append("Amount is >90% of balance")

    risk_score = min(risk_score, 1.0)
    verdict = "🚨 FRAUD DETECTED" if risk_score > 0.5 else "✅ NORMAL"

    return f"{verdict}\nRisk Score: {risk_score:.2f}"

def get_collapse_summary():
    return f"Collapse Days: {collapse_days}"

def get_pmes_summary():
    return str(pmes_df.head())

with gr.Blocks(title="FraudShield") as demo:

    gr.Markdown("# FraudShield — Fraud Detection System")

    with gr.Tab("Transaction Checker"):
        txn_type = gr.Dropdown(['TRANSFER','PAYMENT','CASH_OUT'])
        step = gr.Slider(1, 744)
        amount = gr.Number()
        old_orig = gr.Number()
        new_orig = gr.Number()
        old_dest = gr.Number()
        new_dest = gr.Number()

        btn = gr.Button("Analyze")
        out = gr.Textbox()

        btn.click(
            analyze_transaction,
            inputs=[txn_type, step, amount,
                    old_orig, new_orig, old_dest, new_dest],
            outputs=out
        )

    with gr.Tab("Topology"):
        btn2 = gr.Button("Check Collapse")
        out2 = gr.Textbox()
        btn2.click(get_collapse_summary, outputs=out2)

    with gr.Tab("PMES"):
        btn3 = gr.Button("Show PMES")
        out3 = gr.Textbox()
        btn3.click(get_pmes_summary, outputs=out3)

demo.launch()
