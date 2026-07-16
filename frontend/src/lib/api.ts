import { API_BASE_URL, API_PREFIX } from "@/lib/constants";
import type { ApiErrorBody, QueryRequest, QueryResponse } from "@/types";

/**
 * A user-facing API failure. `code` is the backend's machine code
 * (e.g. `engine_error`, `engine_timeout`, `validation_error`) or a synthetic
 * `network_error` when the request never reached the server.
 */
export class ApiError extends Error {
  readonly code: string;
  readonly status: number;
  readonly requestId?: string;

  constructor(
    code: string,
    message: string,
    status: number,
    requestId?: string,
  ) {
    super(message);
    this.name = "ApiError";
    this.code = code;
    this.status = status;
    this.requestId = requestId;
  }
}

function isApiErrorBody(value: unknown): value is ApiErrorBody {
  if (typeof value !== "object" || value === null) return false;
  const error = (value as { error?: unknown }).error;
  return (
    typeof error === "object" &&
    error !== null &&
    typeof (error as { message?: unknown }).message === "string"
  );
}

/**
 * POST a farmer query to the engine. Resolves with the structured answer or
 * throws an {@link ApiError} carrying a user-safe message and the backend
 * error code (never a raw status or stack trace — PRD RULE 501).
 */
export async function postQuery(
  body: QueryRequest,
  signal?: AbortSignal,
): Promise<QueryResponse> {
  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}${API_PREFIX}/query`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
      signal,
    });
  } catch (cause) {
    if (cause instanceof DOMException && cause.name === "AbortError") {
      throw cause;
    }
    throw new ApiError(
      "network_error",
      "Couldn't reach Krishiva. Check your connection and try again.",
      0,
    );
  }

  if (!response.ok) {
    const payload: unknown = await response.json().catch(() => null);
    if (isApiErrorBody(payload)) {
      throw new ApiError(
        payload.error.code,
        payload.error.message,
        response.status,
        payload.error.request_id,
      );
    }
    throw new ApiError(
      "unknown_error",
      "Krishiva couldn't process your question right now. Please try again.",
      response.status,
    );
  }

  return (await response.json()) as QueryResponse;
}
