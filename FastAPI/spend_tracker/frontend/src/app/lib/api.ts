const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

export async function sendChatMessage(
  message: string,
  history: ChatMessage[],
  month?: number,
  year?: number,
): Promise<string> {
  const res = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, history, month, year }),
  });
  if (!res.ok) throw new Error("Chat request failed");
  const data = await res.json();
  return data.reply as string;
}

export interface ZoneResponse {
  zone: "SAFE" | "WARNING" | "DANGER";
  saving_score: number | null;
  spend_score: number | null;
  zone_score: number | null;
  narrative: string | null;
  action_pills: string[] | null;
  category_data: Record<string, { spent: number; budget: number }> | null;
  month: number;
  year: number;
}

export interface SavingsPlan {
  id: string;
  month: number;
  year: number;
  salary_amount: number;
  target_save_pct: number;
  allocations: Array<{ instrument: string; amount: number; rationale?: string; reason?: string }>;
  total_to_save: number;
  gemini_narrative: string | null;
  created_at: string;
}

export interface Expense {
  id: string;
  amount: number;
  description: string;
  category: string;
  source: string;
  created_at: string;
  expense_date: string;
  confirmed: boolean;
  bank_id: string | null;
  bank_name: string | null;
}

export interface Bank {
  id: string;
  name: string;
}

async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...init,
    cache: "no-store",
  });
  if (!res.ok) throw new Error(`API ${path} → ${res.status}`);
  return res.json() as Promise<T>;
}

export async function fetchZone(): Promise<ZoneResponse> {
  return apiFetch<ZoneResponse>("/zone");
}

export async function fetchSavingsPlan(month: number, year: number): Promise<SavingsPlan | null> {
  try {
    return await apiFetch<SavingsPlan>(`/savings-plan?month=${month}&year=${year}`);
  } catch {
    return null;
  }
}

export async function fetchExpenses(
  month?: number,
  year?: number,
  dateFrom?: string,
  dateTo?: string,
): Promise<Expense[]> {
  try {
    const params = new URLSearchParams();
    if (dateFrom) params.set("date_from", dateFrom);
    if (dateTo) params.set("date_to", dateTo);
    if (!dateFrom && !dateTo && month !== undefined && year !== undefined) {
      params.set("month", month.toString());
      params.set("year", year.toString());
    }
    const query = params.toString() ? `?${params.toString()}` : "";
    return await apiFetch<Expense[]>(`/expenses${query}`);
  } catch {
    return [];
  }
}

export async function postExpense(rawText: string): Promise<unknown> {
  return apiFetch("/expense", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ raw_text: rawText, source: "web" }),
  });
}

export async function confirmExpense(expenseId: string): Promise<void> {
  await apiFetch(`/expense/${expenseId}/confirm`, { method: "POST" });
}

export async function deleteExpense(expenseId: string): Promise<void> {
  await apiFetch(`/expense/${expenseId}`, { method: "DELETE" });
}

export async function updateExpense(
  expenseId: string,
  fields: { amount?: number; description?: string; category?: string; bank_id?: string | null },
): Promise<Expense> {
  return apiFetch<Expense>(`/expense/${expenseId}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(fields),
  });
}

export async function fetchBanks(): Promise<Bank[]> {
  try {
    return await apiFetch<Bank[]>("/settings/banks");
  } catch {
    return [];
  }
}

export async function createBank(name: string): Promise<Bank> {
  return apiFetch<Bank>("/settings/banks", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name }),
  });
}

export async function deleteBank(bankId: string): Promise<void> {
  await apiFetch(`/settings/banks/${bankId}`, { method: "DELETE" });
}

export async function refreshInsights(): Promise<ZoneResponse> {
  return apiFetch<ZoneResponse>("/insights/refresh", { method: "POST" });
}

export interface MonthSettingsOut {
  salary: number | null;
  save_pct: number | null;
  month: number;
  year: number;
  locked: boolean;
}

export interface MonthlySummary {
  month: number;
  year: number;
  month_label: string;
  total_spent: number;
  salary: number;
  total_saved: number;
  zone: string | null;
  saving_score: number | null;
  spend_score: number | null;
}

export async function fetchSettings(month: number, year: number): Promise<MonthSettingsOut> {
  return apiFetch<MonthSettingsOut>(`/settings?month=${month}&year=${year}`);
}

export async function saveSettings(salary: number, save_pct: number, month: number, year: number): Promise<MonthSettingsOut> {
  return apiFetch<MonthSettingsOut>("/settings", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ salary, save_pct, month, year }),
  });
}

export async function updateSettings(salary: number, save_pct: number, month: number, year: number): Promise<MonthSettingsOut> {
  return apiFetch<MonthSettingsOut>("/settings", {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ salary, save_pct, month, year }),
  });
}

export async function restartMonth(month: number, year: number): Promise<void> {
  await apiFetch(`/settings/restart?month=${month}&year=${year}`, { method: "DELETE" });
}

export interface InvestmentInsight {
  assessment: "GOOD" | "MODERATE" | "NEEDS_ATTENTION";
  summary: string;
  allocation_review: string;
  action_items: string[];
  priority_action: string;
}

export async function fetchInvestmentInsight(month: number, year: number): Promise<InvestmentInsight> {
  return apiFetch<InvestmentInsight>(`/insights/investment-review?month=${month}&year=${year}`, {
    method: "POST",
  });
}

export async function fetchMonthlyHistory(): Promise<MonthlySummary[]> {
  try {
    return await apiFetch<MonthlySummary[]>("/insights/monthly-history");
  } catch {
    return [];
  }
}
