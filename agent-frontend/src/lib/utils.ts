import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatCitationLabel(articleLabel?: string | null, pageNumber?: number | null) {
  const articlePart = articleLabel || "Constitution reference";
  const pagePart = typeof pageNumber === "number" ? ` • Page ${pageNumber}` : "";
  return `${articlePart}${pagePart}`;
}

export function generateMessageId() {
  return crypto.randomUUID();
}
