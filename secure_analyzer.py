#!/usr/bin/env python3
"""
Secure Code Interpreter CLI
This script builds a Docker image/container, then uses two agents:
  - FileAccessAgent to ingest and copy the CSV file into the sandbox
  - PythonExecAgent to generate & execute a Python script for data analysis
Usage:
    python secure_analyzer.py --file <path/to/file.csv> --question "Your data question" [--verbose]
    python secure_analyzer.py -f resources/data/traffic_accidents.csv -q "What factors contribute to accident frequency?"
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path)

# Verify OpenAI API key is available
if not os.getenv("OPENAI_API_KEY"):
    print("Error: OPENAI_API_KEY not found in environment variables or .env file")
    sys.exit(1)

# Import the agents from your registry (ensure your PYTHONPATH is set accordingly)
from resources.registry.agents.file_access_agent import FileAccessAgent
from resources.registry.agents.python_code_exec_agent import PythonExecAgent

# --- Docker Management Functions ---

def build_docker_image():
    """Build the Docker image from the docker directory."""
    docker_dir = os.path.join(os.path.dirname(__file__), "resources", "docker")
    try:
        subprocess.run(
            ["docker", "build", "-t", "python_sandbox:latest", docker_dir],
            check=True, capture_output=True, text=True
        )
        logging.info("Docker image built successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Docker build failed: {e.stderr.strip()}")
        sys.exit(1)

def start_container(container_name="sandbox"):
    """Start the Docker container with restricted privileges."""
    try:
        subprocess.run([
            "docker", "run", "-d",
            "--name", container_name,
            "--network", "none",
            "--cap-drop", "all",
            "--pids-limit", "64",
            "--tmpfs", "/tmp:rw,size=64M",
            "python_sandbox:latest",
            "sleep", "infinity"
        ], check=True, capture_output=True, text=True)
        logging.info(f"Container '{container_name}' started successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Container start failed: {e.stderr.strip()}")
        sys.exit(1)

def cleanup_container(container_name="sandbox"):
    """Remove the Docker container."""
    try:
        subprocess.run(["docker", "rm", "-f", container_name], check=True, capture_output=True, text=True)
        logging.info(f"Container '{container_name}' cleaned up successfully.")
    except subprocess.CalledProcessError as e:
        logging.warning(f"Container cleanup failed: {e.stderr.strip()}")

# --- Main Application Flow ---

def main():
    # Set up CLI arguments
    parser = argparse.ArgumentParser(description="Secure Code Interpreter CLI")
    parser.add_argument("-f", "--file", required=True, help="Path to the CSV data file")
    parser.add_argument("-q", "--question", required=True, help="Data analysis question to answer")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Validate file exists
    if not Path(args.file).exists():
        logging.error(f"File not found: {args.file}")
        sys.exit(1)
    
    # --- Docker Setup ---
    build_docker_image()
    start_container()

    try:
        # --- Agent Initialization ---
        # FileAccessAgent uses a default prompt and the 'gpt-4o' model.
        file_agent = FileAccessAgent()  
        # PythonExecAgent is set up with o3-mini model and high reasoning effort.
        code_agent = PythonExecAgent(model_name="o3-mini", reasoning_effort="high")

        # Build a prompt that describes the context of the CSV file.
        file_prompt = f"""Use the file {os.path.basename(args.file)} for your analysis. 
The file data includes the following columns:
accidents, traffic_fine_amount, traffic_density, traffic_lights,
pavement_quality, urban_area, average_speed, rain_intensity,
vehicle_count, time_of_day."""
        logging.info("Setting up file context using FileAccessAgent.")
        # Get file context from the FileAccessAgent.
        file_context = file_agent.task(file_prompt)
        
        # Add context (both file prompt and file content) to the code execution agent.
        code_agent.add_context(file_prompt)
        code_agent.add_context(file_context)

        # --- Analysis Execution ---
        logging.info("Processing user question with PythonExecAgent.")
        analysis_result = code_agent.task(args.question)
        print("\n--- Analysis Result ---\n")
        print(analysis_result)
        print("\n-----------------------\n")
    except Exception as e:
        logging.error(f"Analysis failed: {str(e)}")
    finally:
        cleanup_container()

if __name__ == "__main__":
    main() 