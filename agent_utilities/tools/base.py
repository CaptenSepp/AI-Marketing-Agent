from collections.abc import Callable
from dataclasses import dataclass

from langchain_core.tools import BaseTool, StructuredTool
from pydantic import BaseModel

from agent_utilities.observability.console import print_console_section


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    description: str
    input_schema: type[BaseModel]
    execute: Callable[[BaseModel], BaseModel]
    result_schema: type[BaseModel]

    def as_langchain_tool(self, log_progress: bool = True) -> BaseTool:
        def run(**kwargs):
            if log_progress:
                print_console_section(
                    "TOOL STARTED",
                    f"The workflow is now running the {self.name} tool and waiting for its result.",
                    "started",
                )
            try:
                tool_input = self.input_schema.model_validate(kwargs)
                result = self.result_schema.model_validate(self.execute(tool_input))
                data = result.model_dump()
                if log_progress:
                    print_console_section(
                        "TOOL FINISHED",
                        f"The {self.name} tool returned a valid result to the workflow.",
                        "completed",
                    )
                return next(iter(data.values())) if len(data) == 1 else data
            except Exception as exc:
                print_console_section(
                    "TOOL FAILED",
                    f"The {self.name} tool stopped before returning a valid result.",
                    "failed",
                    f"{type(exc).__name__}: {exc}",
                )
                raise

        return StructuredTool.from_function(
            func=run,
            name=self.name,
            description=self.description,
            args_schema=self.input_schema,
        )
