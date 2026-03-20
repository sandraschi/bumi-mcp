const base = "";

async function parseErr(r: Response): Promise<string> {
  try {
    const j = await r.json();
    if (j && typeof j.detail === "string") return j.detail;
    return JSON.stringify(j);
  } catch {
    return await r.text();
  }
}

export async function apiGet<T>(path: string): Promise<T> {
  const r = await fetch(`${base}${path}`);
  if (!r.ok) throw new Error(await parseErr(r));
  return r.json() as Promise<T>;
}
