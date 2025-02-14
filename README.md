// Start of Selection
# 🛡️ Secure Data Analysis System

Welcome to the Secure Data Analysis System – a robust, Python-based solution for analyzing data files using advanced Language Models (LLMs) in a fully isolated environment. By combining the power of OpenAI's language models with the enhanced security of Docker containerization, this system offers both cutting‐edge data insights and top-notch protection.

## ✨ Features

- **🔒 Secure File Access & Code Execution:** Executes code within isolated Docker containers, ensuring a safe and controlled environment for data analysis.
- **🤖 Intelligent Agents:** Utilizes OpenAI's language models to deliver sophisticated data understanding and processing.
- **🛠️ Extensible Tool System:** Easily extend functionality through a modular tool interface.
- **📊 Built-in Data Analysis Support:** Comes pre-equipped with libraries like `pandas`, `numpy`, `matplotlib`, and `seaborn` for comprehensive data exploration.
- **🔍 Detailed Logging & Error Tracking:** Provides in-depth logging to facilitate efficient debugging and monitoring.
- **🏗️ Clean, Object-Oriented Architecture:** Designed with a clear separation of concerns, aiding in scalability and maintainability.

## 🏛️ Architecture

### Core Components

1. **Agent System** (`resources/registry/agents/`):  
   - **BaseAgent:** The abstract base class for all agents.
   - **FileAccessAgent:** Manages secure file operations.
   - **PythonExecAgent:** Oversees code generation and execution within Docker containers.

2. **Services** (`resources/object_oriented_agents/services/`):  
   - **LanguageModelInterface:** An abstract interface for interacting with language models.
   - **OpenAILanguageModel:** A concrete implementation that leverages the OpenAI API.
   - **OpenAIClientFactory:** Handles the creation and management of OpenAI API clients.

3. **Utils** (`resources/object_oriented_agents/utils/`):  
   - **logger.py:** Provides a centralized logging system.
   - **openai_util.py:** Offers utility functions for interacting with the OpenAI API.

### Component InteractionssequenceDiagram
    participant User
    participant CLI
    participant FileAgent
    participant CodeAgent
    participant LLM
    participant Docker

    User->>CLI: Run analysis
    CLI->>Docker: Start container
    CLI->>FileAgent: Read file
    FileAgent->>CLI: File content
    CLI->>CodeAgent: Generate & run code
    CodeAgent->>LLM: Request code
    LLM-->>CodeAgent: Return code
    CodeAgent->>Docker: Execute code
    Docker-->>CodeAgent: Results
    CodeAgent->>CLI: Analysis results
    CLI->>User: Display results
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Docker
- An active OpenAI API key

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/secure-data-analysis.git
   cd secure-data-analysis
   ```

2. **Install Dependencies:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure the OpenAI API:**

   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```

### Basic Usage

Run the analyzer with a CSV file and your question:

```bash
python secure_analyzer.py --file your_data.csv --question "What are the monthly trends?"
```

## 🔒 Security Features

### 1. Docker Isolation

- Executes all code in isolated Docker containers.
- Runs with a non-root user.
- Enforces strict resource limits and network isolation.

### 2. File Access Security

```python
# Example from FileAccessAgent
def safe_file_access(self, filename: str) -> str:
    if not self._is_safe_path(filename):
        return "Error: Invalid file path"
    return self._read_file_safely(filename)
```

### 3. Language Model Security

```python
# From OpenAILanguageModel
def generate_completion(
    self,
    model: str,
    messages: List[Dict[str, str]],
    tools: Optional[List[Dict[str, Any]]] = None,
    reasoning_effort: Optional[str] = None
) -> Dict[str, Any]:
    try:
        response = self.openai_client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools
        )
        return response
    except Exception as e:
        self.logger.error(f"OpenAI call failed: {str(e)}", exc_info=True)
        raise
```

## 📖 Example Workflows

### 1. Basic Data Analysis

```bash
python secure_analyzer.py \
    --file sales_data.csv \
    --question "Show me the average sales by quarter"
```

### 2. Advanced Analysis with Visualization

```bash
python secure_analyzer.py \
    --file traffic_data.csv \
    --question "Create a line plot showing accidents over time_of_day"
```

## 🛠️ Development Guide

### Creating a New Tool

Implement the `ToolInterface` to add custom capabilities:

```python
from ...object_oriented_agents.core_classes.tool_interface import ToolInterface

class CustomAnalysisTool(ToolInterface):
    def get_definition(self) -> Dict[str, Any]:
        return {
            "function": {
                "name": "custom_analysis",
                "description": "Performs custom data analysis",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "analysis_type": {"type": "string"},
                        "columns": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["analysis_type", "columns"]
                }
            }
        }

    def run(self, arguments: Dict[str, Any]) -> str:
        # Implementation
        pass
```

### Creating a New Agent

Extend the base agent to create custom agents:

```python
from ...object_oriented_agents.core_classes.base_agent import BaseAgent

class CustomAnalysisAgent(BaseAgent):
    def __init__(
        self,
        developer_prompt: str = "Your custom prompt here",
        model_name: str = "gpt-4",
        logger=None,
        language_model_interface=None
    ):
        super().__init__(
            developer_prompt=developer_prompt,
            model_name=model_name,
            logger=logger,
            language_model_interface=language_model_interface
        )
        self.setup_tools()

    def setup_tools(self) -> None:
        self.tool_manager.register_tool(CustomAnalysisTool())
```

## 📝 Logging System

Our project utilizes a hierarchical logging system to streamline monitoring and debugging:

```python
from ...object_oriented_agents.utils.logger import get_logger

logger = get_logger(__name__)

# Usage examples
logger.info("Starting analysis...")
logger.debug("Processing file: %s", filename)
logger.error("Error in analysis", exc_info=True)
```

**Log Configuration:**

- **Log Level:** Configurable (DEBUG, INFO, ERROR)
- **Output:** Both console and file (`logs.log`)
- **Format:** `%(asctime)s - %(name)s - %(levelname)s - %(message)s`

## 🤝 Contributing

We welcome contributions! To get started:

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/NewFeature`).
3. Commit your changes (`git commit -m 'Add NewFeature'`).
4. Push to your branch (`git push origin feature/NewFeature`).
5. Open a Pull Request.

### Development Guidelines

- Adhere to the PEP 8 style guide.
- Include unit tests for new features.
- Update the documentation as needed.
- Maintain type hints and clear commit messages.

## 📄 License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for their groundbreaking language models.
- Docker for delivering robust containerization.
- All contributors and users who help improve this project.

## 📞 Contact

Sharad Jain – [@seekingtroooth](https://x.com/seekingtroooth) – sharadsfo@gmail.com

Project Link: [https://github.com/Imsharad/openai-code-interpreter](https://github.com/Imsharad/openai-code-interpreter)

## 📚 Additional Resources

- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)
- [Docker Documentation](https://docs.docker.com/)
- [Python Packaging Documentation](https://packaging.python.org/)
