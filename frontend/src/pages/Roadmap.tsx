import { useState } from "react";
import { Compass, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { api } from "@/lib/api";

interface Phase {
  phase: string;
  focus: string;
  skills: string[];
  certifications: string[];
  target_roles: string[];
}

export default function Roadmap() {
  const [phases, setPhases] = useState<Phase[] | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function generate() {
    setLoading(true);
    setError("");
    try {
      const res = await api.get("/career/roadmap");
      setPhases(res.data.roadmap);
    } catch {
      setError("Our AI is busy, please retry in a moment.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="mx-auto max-w-3xl px-4 py-10">
      <h1 className="flex items-center gap-2 text-2xl font-bold">
        <Compass className="h-6 w-6" /> Career roadmap
      </h1>
      <p className="mt-1 text-sm text-muted-foreground">
        The Mentor Agent builds a 2-year plan from your real profile and goals.
      </p>
      {error && <p className="mt-2 text-sm text-destructive">{error}</p>}

      {!phases ? (
        <Button className="mt-6" onClick={generate} disabled={loading}>
          {loading ? (
            <>
              <Loader2 className="h-4 w-4 animate-spin" /> Mentor Agent planning…
            </>
          ) : (
            "Generate my roadmap"
          )}
        </Button>
      ) : (
        <div className="mt-8 space-y-0">
          {phases.map((p, i) => (
            <div key={p.phase} className="relative pl-8 pb-8">
              {i < phases.length - 1 && (
                <span className="absolute left-[11px] top-8 h-full w-px bg-border" />
              )}
              <span className="absolute left-0 top-1.5 flex h-6 w-6 items-center justify-center rounded-full bg-primary text-xs font-bold text-primary-foreground">
                {i + 1}
              </span>
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-base">
                    {p.phase} — <span className="font-normal">{p.focus}</span>
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-2 text-sm">
                  <div className="flex flex-wrap gap-1">
                    {p.skills.map((s) => (
                      <span key={s} className="rounded-full border border-border px-2 py-0.5 text-xs">
                        {s}
                      </span>
                    ))}
                  </div>
                  {p.certifications.length > 0 && (
                    <p className="text-muted-foreground">🎓 {p.certifications.join(", ")}</p>
                  )}
                  {p.target_roles.length > 0 && (
                    <p className="text-muted-foreground">🎯 Target roles: {p.target_roles.join(", ")}</p>
                  )}
                </CardContent>
              </Card>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
