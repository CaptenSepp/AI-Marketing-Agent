# Multi-tier LLM fallback wrapper.
# Junior-level note: Tries each configured model until one succeeds.
class FallbackChatModel:
    """Tries models in sequential order until one succeeds."""

    def __init__(self, primary, *backups):
        self.models = [primary, *backups]

    @property
    def primary(self):
        return self.models[0]

    @property
    def backup(self):
        return self.models[1] if len(self.models) > 1 else self.models[0]

    def bind_tools(self, tools):
        return FallbackChatModel(*(model.bind_tools(tools) for model in self.models))

    def with_structured_output(self, schema):
        return FallbackChatModel(
            *(model.with_structured_output(schema) for model in self.models)
        )

    def invoke(self, messages):
        last_exception = None
        for model in self.models:
            try:
                return model.invoke(messages)
            except Exception as exc:  # noqa: BLE001
                last_exception = exc
        if last_exception is not None:
            raise last_exception
        raise RuntimeError("No models configured in FallbackChatModel")
