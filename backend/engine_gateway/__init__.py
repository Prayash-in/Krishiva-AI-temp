"""The boundary between the backend and the AI engine.

The backend depends only on the :class:`QueryEngine` protocol defined in
``contract``. The real engine (retrieval + rule engine + LLM) plugs in later by
satisfying that protocol; :class:`StubQueryEngine` keeps the API runnable today.
"""
