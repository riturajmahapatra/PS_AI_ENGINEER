# AI Loop Platform

An autonomous, multi-agent engine and execution loop platform for AI engineering workflows.

## Project Structure

- **`agents/`**: Autonomous AI agent modules.
  - `base_agent.py`: Base abstract class for agents.
  - `planning_agent.py`: Task decomposition and plan generation.
  - `success_agent.py`: Goal verification and quality evaluation.
  - `execution_agent.py`: Code editing and tool execution.
  - `validation_agent.py`: Build, lint, and test validation.
- **`engine/`**: Core execution engine and state machine.
  - `graph_executor.py`: Dynamic agent node DAG executor.
  - `workflow_engine.py`: Agent execution loop orchestration.
  - `state.py`: Execution state models.
- **`runner/`**: Execution environment runners.
  - `repository.py`: Workspace filesystem manager.
  - `shell.py`: Subprocess & shell runner.
  - `git.py`: Git operations integration.
- **`validator/`**: Automated verification and quality gates.
  - `build.py`: Build system validator.
  - `tests.py`: Test suite execution validator.
  - `lint.py`: Code quality & linter validator.
  - `coverage.py`: Test coverage threshold validator.
- **`db/`**: Database models and data schemas.
  - `models.py`: ORM & data models.
  - `schemas.py`: Validation & API schemas.
- **`api/`**: Backend API endpoints.
- **`backend/`**: Core backend services.
- **`frontend/`**: Web canvas & visual interface components.
  - `canvas/`: Graph canvas workspace.
  - `nodes/`: Custom flow node components.
  - `console/`: Output terminal & execution logs interface.
  - `inspector/`: Node & agent property inspector.
  - `topbar/`: Navigation & toolbar controls.
  - `projects/`: Project list & workspace manager.
  - `settings/`: Platform & agent configuration panel.
- **`docker/`**: Container definitions & docker-compose configurations.
- **`logs/`**: Execution logs & audit records.
- **`artifacts/`**: Generated build artifacts & outputs.

