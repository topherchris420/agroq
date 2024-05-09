import streamlit as st
from groq import GroqError, Environment
import numpy as np
import pandas as pd

st.title("GroqGen: Autogen and Crew AI Agent Generator")

agent_templates = {
    "Autogen": {
        "parameters": ["environment", "sensors", "actuators"],
        "behaviors": ["navigation", "obstacle avoidance"],
        "goals": ["reach destination", "avoid collisions"]
    },
    "Crew AI": {
        "parameters": ["team size", "roles", "communication protocols"],
        "behaviors": ["coordinated navigation", "task allocation"],
        "goals": ["complete mission", "minimize team risk"]
    }
}

agent_type = st.selectbox("Select Agent Type", list(agent_templates.keys()))

with st.form("agent_config"):
    st.header("Configure Agent Parameters")
    parameters = agent_templates[agent_type]["parameters"]
    config_params = {param: st.text_input(param, value="") for param in parameters}
    config_goals = st.text_input("Goals", value=", ".join(agent_templates[agent_type]["goals"]))
    submit_button = st.form_submit_button("Generate Agent")

    if submit_button:
        generate_agent(agent_type, config_params, config_goals)

def generate_agent(agent_type, config_params, config_goals):
    try:
        config_params = {k: v.strip() for k, v in config_params.items()}
        config_goals = [goal.strip() for goal in config_goals.split(",")]

        groq_model = f"""
        def generate_agent(params: dict, goals: list) -> dict:
            behavior = 'navigate' if 'indoor' in params.get('environment', '') else 'avoid obstacles'
            return {{
                'Agent Type': '{agent_type}',
                'Parameters': params,
                'Behavior': behavior,
                'Goals': goals
            }}
        """

        groq_env = Environment()  # Ensure this matches the actual setup
        agent = groq_env.execute_code(groq_model, params=config_params, goals=config_goals)

        st.header("Generated Agent")
        st.write(agent)
    except GroqError as e:
        st.error(f"Error generating agent: {e}")
    except Exception as e:
        st.error(f"Unexpected error: {e}")
