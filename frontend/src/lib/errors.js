export function isLockedError(error) {
  const status = error?.response?.status;
  return status === 402 || status === 403;
}

export function lockedMessage(error) {
  const detail = error?.response?.data?.detail;
  if (typeof detail === "string" && detail.trim()) return detail;
  if (detail && typeof detail === "object") return JSON.stringify(detail);
  if (error?.response?.status === 402) return "Subscription inactive. Please renew to continue.";
  if (error?.response?.status === 403) return "You do not have access to this workspace.";
  return "Access is locked for this action.";
}
