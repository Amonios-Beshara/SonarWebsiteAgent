export async function createSession(company: string) {
  const res = await fetch("http://localhost:8000/create-session", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ company }),
  });
  if (!res.ok) throw new Error("Failed to create session");
  return res.json();
}

export async function generateFAQ(transcript: string) {
  const res = await fetch("http://localhost:8000/generate-faq", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ transcript }),
  });
  if (!res.ok) throw new Error("Failed to generate FAQ");
  return res.json();
}
