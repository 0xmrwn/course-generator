# Course Generator

This repository contains the codebase for a course generation module. The main purpose of this module is to generate and refine course content for a high school math course. The course content is generated using OpenAI's language model.

### Overview

The course generation module is built around the concept of multi-agent collaboration and advanced orchestration. It uses Language Learning Models (LLMs) to generate and refine course content. The module is designed to be flexible and scalable, allowing for the addition of new agents and the modification of existing ones.

### Key Components

### Agents

Agents are the core components of the system.They are responsible for generating and refining course content. Each agent has a specific role and communicates with other agents to complete tasks. The agents are built using the autogen library.

The agents are defined in the agents.py file. The build_course_generation_team function is used to create a team of agents. Each agent is given a specific role and a set of instructions, defined in the USER_PROXY_PROMPT, INSPECTOR_PROMPT, and WRITER_PROMPT variables.

### Orchestrator

The orchestrator manages the conversation between the agents.It ensures that the agents communicate effectively and complete their tasks in the correct order. The orchestrator is defined in the orchestrator.py file.

### Instruments

Instruments are tools, state, and functions that an agent can use across the lifecycle of conversations. They are defined in the `instruments.py` file. The `FileAgentInstruments` class is used to manage the state and functions of the agents.

### Main Function

The main function is the entry point of the program. It sets up the environment, generates the initial prompt, and starts the conversation between the agents. The main function is defined in the `main.py` file.

### How to Run

To run the course generation module, you need to have Python 3.11 or later installed. You also need to install the dependencies listed in the `pyproject.toml` file.

> If needed, first install poetry

```bash
pip install poetry
```

Once the dependencies are installed, you can run the main function to start the course generation process.

### Output

The output of the course generation module is a series of markdown files containing the generated course content. The files are saved in the agent_results directory, which is defined in the `instruments.py` file.