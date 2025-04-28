# AI TASK GENERATOR

## Fork of Claude AI Task Master by [@eyaltoledano]([https://github.com/eyaltoledano/claude-ai-task-master](https://github.com/eyaltoledano/claude-task-master)). 
Github address: [AI Task Generator]([https://github.com/asimsinan/ai-task-generator](https://github.com/asimsinan/ai-task-generator))
* Added support for OPENAI


A task management system for AI-driven development with Claude and OpenAI, designed to work seamlessly with Cursor AI.

## To-Do
- Make it work with all other AI providers


## Requirements

- Node.js 14.0.0 or higher
- Anthropic API key (Claude API) and/or OpenAI API key
- Anthropic SDK version 0.39.0 or higher
- OpenAI SDK version 4.0.0 or higher

## Configuration

The script can be configured through environment variables in a `.env` file at the root of the project:

### Required Configuration (at least one of the following)

- `ANTHROPIC_API_KEY`: Your Anthropic API key for Claude
- `OPENAI_API_KEY`: Your OpenAI API key (alternative to Anthropic)

### Optional Configuration

- `MODEL`: Specify which Claude model to use (default: "claude-3-7-sonnet-20250219")
- `MAX_TOKENS`: Maximum tokens for model responses (default: 4000)
- `TEMPERATURE`: Temperature for model responses (default: 0.7)
- `OPENAI_MODEL`: Specify which OpenAI model to use (default: "gpt-4o")
- `OPENAI_MAX_TOKENS`: Maximum tokens for OpenAI responses (default: 4096)
- `OPENAI_TEMPERATURE`: Temperature for OpenAI responses (default: 0.2)
- `PREFER_OPENAI`: Whether to prefer OpenAI over Claude (default: false)
- `PERPLEXITY_API_KEY`: Your Perplexity API key for research-backed subtask generation
- `PERPLEXITY_MODEL`: Specify which Perplexity model to use (default: "sonar-medium-online")
- `DEBUG`: Enable debug logging (default: false)
- `LOG_LEVEL`: Log level - debug, info, warn, error (default: info)
- `DEFAULT_SUBTASKS`: Default number of subtasks when expanding (default: 3)
- `DEFAULT_PRIORITY`: Default priority for generated tasks (default: medium)
- `PROJECT_NAME`: Override default project name in tasks.json
- `PROJECT_VERSION`: Override default version in tasks.json

## Installation

```bash
# Install globally
npm install -g ai-task-generator

# OR install locally within your project
npm install ai-task-generator
```

### Initialize a new project

```bash
# If installed globally
ai-task-generator init

# If installed locally
npx ai-task-generator-init
```

This will prompt you for project details and set up a new project with the necessary files and structure.

### Handling Deprecation Warnings

If you encounter punycode module deprecation warnings when running the CLI, you have several options:

```bash
# Option 1: Use the no-warnings version of the command
ai-task-generator-no-warnings <command>

# Option 2: Use the npm start script (which suppresses warnings)
npm start -- <command>

# Option 3: Run with the Node.js --no-deprecation flag
node --no-deprecation bin/ai-task-generator.js <command>
```

These solutions will suppress the Node.js deprecation warnings related to the punycode module.

## AI Model Support

AI Task Generator now supports both Claude (Anthropic) and GPT (OpenAI) models for task generation, analysis, and other AI operations. You can configure your preferred model using:

- Environment variables: Set `ANTHROPIC_API_KEY` and/or `OPENAI_API_KEY` in your `.env` file
- Command-line flags: Use `--prefer-openai` with commands like `ai-task-generator parse-prd`
- Configuration: Set `PREFER_OPENAI=true` in your `.env` file to default to OpenAI

The system will automatically fall back to an alternative model if your preferred one is unavailable or overloaded.

### Important Notes

1. **ES Modules Configuration:**

   - This project uses ES Modules (ESM) instead of CommonJS.
   - This is set via `"type": "module"` in your package.json.
   - Use `import/export` syntax instead of `require()`.
   - Files should use `.js` or `.mjs` extensions.
   - To use a CommonJS module, either:
     - Rename it with `.cjs` extension
     - Use `await import()` for dynamic imports
   - If you need CommonJS throughout your project, remove `"type": "module"` from package.json, but AI Task Generator scripts expect ESM.

2. The Anthropic SDK version should be 0.39.0 or higher.

## Quick Start with Global Commands

After installing the package globally, you can use these CLI commands from any directory:

```bash
# Initialize a new project
ai-task-generator init

# Parse a PRD and generate tasks
ai-task-generator parse-prd your-prd.txt

# List all tasks
ai-task-generator list

# Show the next task to work on
ai-task-generator next

# Generate task files
ai-task-generator generate
```

## Troubleshooting

### If `ai-task-generator init` doesn't respond:

Try running it with Node directly:

```bash
node node_modules/claude-ai-task-generator/scripts/init.js
```

Or clone the repository and run:

```bash
git clone https://github.com/eyaltoledano/claude-ai-task-generator.git
cd claude-ai-task-generator
node scripts/init.js
```

## Task Structure

Tasks in tasks.json have the following structure:

- `id`: Unique identifier for the task (Example: `1`)
- `title`: Brief, descriptive title of the task (Example: `"Initialize Repo"`)
- `description`: Concise description of what the task involves (Example: `"Create a new repository, set up initial structure."`)
- `status`: Current state of the task (Example: `"pending"`, `"done"`, `"deferred"`)
- `dependencies`: IDs of tasks that must be completed before this task (Example: `[1, 2]`)
  - Dependencies are displayed with status indicators (✅ for completed, ⏱️ for pending)
  - This helps quickly identify which prerequisite tasks are blocking work
- `priority`: Importance level of the task (Example: `"high"`, `"medium"`, `"low"`)
- `details`: In-depth implementation instructions (Example: `"Use GitHub client ID/secret, handle callback, set session token."`)
- `testStrategy`: Verification approach (Example: `"Deploy and call endpoint to confirm 'Hello World' response."`)
- `subtasks`: List of smaller, more specific tasks that make up the main task (Example: `[{"id": 1, "title": "Configure OAuth", ...}]`)

## Integrating with Cursor AI

Claude AI Task Generator is designed to work seamlessly with [Cursor AI](https://www.cursor.so/), providing a structured workflow for AI-driven development.

### Setup with Cursor

1. After initializing your project, open it in Cursor
2. The `.cursor/rules/dev_workflow.mdc` file is automatically loaded by Cursor, providing the AI with knowledge about the task management system
3. Place your PRD document in the `scripts/` directory (e.g., `scripts/prd.txt`)
4. Open Cursor's AI chat and switch to Agent mode

### Setting up MCP in Cursor

To enable enhanced task management capabilities directly within Cursor using the Model Control Protocol (MCP):

1. Go to Cursor settings
2. Navigate to the MCP section
3. Click on "Add New MCP Server"
4. Configure with the following details:
   - Name: "AI Task Generator"
   - Type: "Command"
   - Command: "npx -y ai-task-generator-mcp"
5. Save the settings

Once configured, you can interact with AI Task Generator's task management commands directly through Cursor's interface, providing a more integrated experience.

### Initial Task Generation

In Cursor's AI chat, instruct the agent to generate tasks from your PRD:

```
Please use the ai-task-generator parse-prd command to generate tasks from my PRD. The PRD is located at scripts/prd.txt.
```

The agent will execute:

```bash
ai-task-generator parse-prd scripts/prd.txt
```

This will:

- Parse your PRD document
- Generate a structured `tasks.json` file with tasks, dependencies, priorities, and test strategies
- The agent will understand this process due to the Cursor rules

### Generate Individual Task Files

Next, ask the agent to generate individual task files:

```
Please generate individual task files from tasks.json
```

The agent will execute:

```bash
ai-task-generator generate
```

This creates individual task files in the `tasks/` directory (e.g., `task_001.txt`, `task_002.txt`), making it easier to reference specific tasks.

## AI-Driven Development Workflow

The Cursor agent is pre-configured (via the rules file) to follow this workflow:

### 1. Task Discovery and Selection

Ask the agent to list available tasks:

```
What tasks are available to work on next?
```

The agent will:

- Run `ai-task-generator list` to see all tasks
- Run `ai-task-generator next` to determine the next task to work on
- Analyze dependencies to determine which tasks are ready to be worked on
- Prioritize tasks based on priority level and ID order
- Suggest the next task(s) to implement

### 2. Task Implementation

When implementing a task, the agent will:

- Reference the task's details section for implementation specifics
- Consider dependencies on previous tasks
- Follow the project's coding standards
- Create appropriate tests based on the task's testStrategy

You can ask:

```
Let's implement task 3. What does it involve?
```

### 3. Task Verification

Before marking a task as complete, verify it according to:

- The task's specified testStrategy
- Any automated tests in the codebase
- Manual verification if required

### 4. Task Completion

When a task is completed, tell the agent:

```
Task 3 is now complete. Please update its status.
```

The agent will execute:

```bash
ai-task-generator set-status --id=3 --status=done
```

### 5. Handling Implementation Drift

If during implementation, you discover that:

- The current approach differs significantly from what was planned
- Future tasks need to be modified due to current implementation choices
- New dependencies or requirements have emerged

Tell the agent:

```
We've changed our approach. We're now using Express instead of Fastify. Please update all future tasks to reflect this change.
```

The agent will execute:

```bash
ai-task-generator update --from=4 --prompt="Now we are using Express instead of Fastify."
```

This will rewrite or re-scope subsequent tasks in tasks.json while preserving completed work.

### 6. Breaking Down Complex Tasks

For complex tasks that need more granularity:

```
Task 5 seems complex. Can you break it down into subtasks?
```

The agent will execute:

```bash
ai-task-generator expand --id=5 --num=3
```

You can provide additional context:

```
Please break down task 5 with a focus on security considerations.
```

The agent will execute:

```bash
ai-task-generator expand --id=5 --prompt="Focus on security aspects"
```

You can also expand all pending tasks:

```
Please break down all pending tasks into subtasks.
```

The agent will execute:

```bash
ai-task-generator expand --all
```

For research-backed subtask generation using Perplexity AI:

```
Please break down task 5 using research-backed generation.
```

The agent will execute:

```bash
ai-task-generator expand --id=5 --research
```

## Command Reference

Here's a comprehensive reference of all available commands:

### Parse PRD

```bash
# Parse a PRD file and generate tasks
ai-task-generator parse-prd <prd-file.txt>

# Limit the number of tasks generated
ai-task-generator parse-prd <prd-file.txt> --num-tasks=10
```

### List Tasks

```bash
# List all tasks
ai-task-generator list

# List tasks with a specific status
ai-task-generator list --status=<status>

# List tasks with subtasks
ai-task-generator list --with-subtasks

# List tasks with a specific status and include subtasks
ai-task-generator list --status=<status> --with-subtasks
```

### Show Next Task

```bash
# Show the next task to work on based on dependencies and status
ai-task-generator next
```

### Show Specific Task

```bash
# Show details of a specific task
ai-task-generator show <id>
# or
ai-task-generator show --id=<id>

# View a specific subtask (e.g., subtask 2 of task 1)
ai-task-generator show 1.2
```

### Update Tasks

```bash
# Update tasks from a specific ID and provide context
ai-task-generator update --from=<id> --prompt="<prompt>"
```

### Generate Task Files

```bash
# Generate individual task files from tasks.json
ai-task-generator generate
```

### Set Task Status

```bash
# Set status of a single task
ai-task-generator set-status --id=<id> --status=<status>

# Set status for multiple tasks
ai-task-generator set-status --id=1,2,3 --status=<status>

# Set status for subtasks
ai-task-generator set-status --id=1.1,1.2 --status=<status>
```

When marking a task as "done", all of its subtasks will automatically be marked as "done" as well.

### Expand Tasks

```bash
# Expand a specific task with subtasks
ai-task-generator expand --id=<id> --num=<number>

# Expand with additional context
ai-task-generator expand --id=<id> --prompt="<context>"

# Expand all pending tasks
ai-task-generator expand --all

# Force regeneration of subtasks for tasks that already have them
ai-task-generator expand --all --force

# Research-backed subtask generation for a specific task
ai-task-generator expand --id=<id> --research

# Research-backed generation for all tasks
ai-task-generator expand --all --research
```

### Clear Subtasks

```bash
# Clear subtasks from a specific task
ai-task-generator clear-subtasks --id=<id>

# Clear subtasks from multiple tasks
ai-task-generator clear-subtasks --id=1,2,3

# Clear subtasks from all tasks
ai-task-generator clear-subtasks --all
```

### Analyze Task Complexity

```bash
# Analyze complexity of all tasks
ai-task-generator analyze-complexity

# Save report to a custom location
ai-task-generator analyze-complexity --output=my-report.json

# Use a specific LLM model
ai-task-generator analyze-complexity --model=claude-3-opus-20240229

# Set a custom complexity threshold (1-10)
ai-task-generator analyze-complexity --threshold=6

# Use an alternative tasks file
ai-task-generator analyze-complexity --file=custom-tasks.json

# Use Perplexity AI for research-backed complexity analysis
ai-task-generator analyze-complexity --research
```

### View Complexity Report

```bash
# Display the task complexity analysis report
ai-task-generator complexity-report

# View a report at a custom location
ai-task-generator complexity-report --file=my-report.json
```

### Managing Task Dependencies

```bash
# Add a dependency to a task
ai-task-generator add-dependency --id=<id> --depends-on=<id>

# Remove a dependency from a task
ai-task-generator remove-dependency --id=<id> --depends-on=<id>

# Validate dependencies without fixing them
ai-task-generator validate-dependencies

# Find and fix invalid dependencies automatically
ai-task-generator fix-dependencies
```

### Add a New Task

```bash
# Add a new task using AI
ai-task-generator add-task --prompt="Description of the new task"

# Add a task with dependencies
ai-task-generator add-task --prompt="Description" --dependencies=1,2,3

# Add a task with priority
ai-task-generator add-task --prompt="Description" --priority=high
```

## Feature Details

### Analyzing Task Complexity

The `analyze-complexity` command:

- Analyzes each task using AI to assess its complexity on a scale of 1-10
- Recommends optimal number of subtasks based on configured DEFAULT_SUBTASKS
- Generates tailored prompts for expanding each task
- Creates a comprehensive JSON report with ready-to-use commands
- Saves the report to scripts/task-complexity-report.json by default

The generated report contains:

- Complexity analysis for each task (scored 1-10)
- Recommended number of subtasks based on complexity
- AI-generated expansion prompts customized for each task
- Ready-to-run expansion commands directly within each task analysis

### Viewing Complexity Report

The `complexity-report` command:

- Displays a formatted, easy-to-read version of the complexity analysis report
- Shows tasks organized by complexity score (highest to lowest)
- Provides complexity distribution statistics (low, medium, high)
- Highlights tasks recommended for expansion based on threshold score
- Includes ready-to-use expansion commands for each complex task
- If no report exists, offers to generate one on the spot

### Smart Task Expansion

The `expand` command automatically checks for and uses the complexity report:

When a complexity report exists:

- Tasks are automatically expanded using the recommended subtask count and prompts
- When expanding all tasks, they're processed in order of complexity (highest first)
- Research-backed generation is preserved from the complexity analysis
- You can still override recommendations with explicit command-line options

Example workflow:

```bash
# Generate the complexity analysis report with research capabilities
ai-task-generator analyze-complexity --research

# Review the report in a readable format
ai-task-generator complexity-report

# Expand tasks using the optimized recommendations
ai-task-generator expand --id=8
# or expand all tasks
ai-task-generator expand --all
```

### Finding the Next Task

The `next` command:

- Identifies tasks that are pending/in-progress and have all dependencies satisfied
- Prioritizes tasks by priority level, dependency count, and task ID
- Displays comprehensive information about the selected task:
  - Basic task details (ID, title, priority, dependencies)
  - Implementation details
  - Subtasks (if they exist)
- Provides contextual suggested actions:
  - Command to mark the task as in-progress
  - Command to mark the task as done
  - Commands for working with subtasks

### Viewing Specific Task Details

The `show` command:

- Displays comprehensive details about a specific task or subtask
- Shows task status, priority, dependencies, and detailed implementation notes
- For parent tasks, displays all subtasks and their status
- For subtasks, shows parent task relationship
- Provides contextual action suggestions based on the task's state
- Works with both regular tasks and subtasks (using the format taskId.subtaskId)

## Best Practices for AI-Driven Development

1. **Start with a detailed PRD**: The more detailed your PRD, the better the generated tasks will be.

2. **Review generated tasks**: After parsing the PRD, review the tasks to ensure they make sense and have appropriate dependencies.

3. **Analyze task complexity**: Use the complexity analysis feature to identify which tasks should be broken down further.

4. **Follow the dependency chain**: Always respect task dependencies - the Cursor agent will help with this.

5. **Update as you go**: If your implementation diverges from the plan, use the update command to keep future tasks aligned with your current approach.

6. **Break down complex tasks**: Use the expand command to break down complex tasks into manageable subtasks.

7. **Regenerate task files**: After any updates to tasks.json, regenerate the task files to keep them in sync.

8. **Communicate context to the agent**: When asking the Cursor agent to help with a task, provide context about what you're trying to achieve.

9. **Validate dependencies**: Periodically run the validate-dependencies command to check for invalid or circular dependencies.

## Example Cursor AI Interactions

### Starting a new project

```
I've just initialized a new project with Claude AI Task Generator. I have a PRD at scripts/prd.txt.
Can you help me parse it and set up the initial tasks?
```

### Working on tasks

```
What's the next task I should work on? Please consider dependencies and priorities.
```

### Implementing a specific task

```
I'd like to implement task 4. Can you help me understand what needs to be done and how to approach it?
```

### Managing subtasks

```
I need to regenerate the subtasks for task 3 with a different approach. Can you help me clear and regenerate them?
```

### Handling changes

```
We've decided to use MongoDB instead of PostgreSQL. Can you update all future tasks to reflect this change?
```

### Completing work

```
I've finished implementing the authentication system described in task 2. All tests are passing.
Please mark it as complete and tell me what I should work on next.
```

### Analyzing complexity

```
Can you analyze the complexity of our tasks to help me understand which ones need to be broken down further?
```

### Viewing complexity report

```
Can you show me the complexity report in a more readable format?
```
