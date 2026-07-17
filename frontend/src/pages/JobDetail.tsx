import { useCallback, useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { ArrowLeft, Check, Loader2, Sparkles, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { api } from "@/lib/api";
import type { Job } from "@/pages/Jobs";

function scoreRing(score: number) {
  if (score >= 75) return "border-green-600 text-green-600";
  if (score >= 50) return "border-yellow-600 text-yellow-600";
  return "border-red-600 text-red-600";
}

export default function JobDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [job, setJob] = useState<Job | null>(null);
  const [matching, setMatching] = useState(false);
  const [error, setError] = useState("");

  const fetchJob = useCallback(async () => {
    const res = await api.get(`/jobs/${id}`);
    setJob(res.data);
  }, [id]);

  useEffect(() => {
    fetchJob();
  }, [fetchJob]);

  async function analyze() {
    setError("");
    setMatching(true);
    try {
      await api.post(`/jobs/${id}/match`);
      await fetchJob();
    } catch {
      setError("Our AI is busy, please retry in a moment.");
    } finally {
      setMatching(false);
    }
  }

  if (!job) {
    return (
      <div className="flex h-64 items-center justify-center text-muted-foreground">
        <Loader2 className="mr-2 h-5 w-5 animate-spin" /> Loading…
      </div>
    );
  }

  const match = job.my_match;

  return (
    <div className="mx-auto max-w-4xl px-4 py-10">
      <Button variant="ghost" size="sm" onClick={() => navigate("/jobs")}>
        <ArrowLeft className="h-4 w-4" /> Back to jobs
      </Button>

      <div className="mt-4 flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold">{job.title}</h1>
          <p className="text-muted-foreground">
            {job.company} · {job.location}
            {job.work_mode && ` · ${job.work_mode}`}
            {job.salary_range && ` · ${job.salary_range}`}
          </p>
        </div>
        <div className="flex gap-2">
          {!match && (
            <Button onClick={analyze} disabled={matching}>
              {matching ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" /> Matching Agent thinking…
                </>
              ) : (
                <>
                  <Sparkles className="h-4 w-4" /> Analyze my fit
                </>
              )}
            </Button>
          )}
          <Button variant={match ? "default" : "outline"} onClick={() => navigate(`/jobs/${id}/studio`)}>
            Optimize resume &amp; cover letter
          </Button>
        </div>
      </div>
      {error && <p className="mt-2 text-sm text-destructive">{error}</p>}

      {match && (
        <Card className="mt-6">
          <CardContent className="flex flex-col gap-6 p-6 sm:flex-row">
            <div
              className={`flex h-24 w-24 shrink-0 flex-col items-center justify-center rounded-full border-4 ${scoreRing(match.fit_score)}`}
            >
              <span className="text-3xl font-bold">{match.fit_score}</span>
              <span className="text-[10px] uppercase text-muted-foreground">fit score</span>
            </div>
            <div className="space-y-3">
              <p className="text-sm leading-relaxed">{match.reasoning}</p>
              <div className="flex flex-wrap gap-1.5">
                {match.matched_skills.map((s) => (
                  <span
                    key={s}
                    className="inline-flex items-center gap-1 rounded-full bg-green-600/10 px-2 py-0.5 text-xs text-green-700 dark:text-green-400"
                  >
                    <Check className="h-3 w-3" /> {s}
                  </span>
                ))}
                {match.missing_skills.map((s) => (
                  <span
                    key={s}
                    className="inline-flex items-center gap-1 rounded-full bg-red-600/10 px-2 py-0.5 text-xs text-red-700 dark:text-red-400"
                  >
                    <X className="h-3 w-3" /> {s}
                  </span>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      <Card className="mt-6">
        <CardHeader>
          <CardTitle>Job description</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="whitespace-pre-line text-sm leading-relaxed text-muted-foreground">
            {job.description}
          </p>
          <div className="mt-4 flex flex-wrap gap-1.5">
            {job.skills_required.map((s) => (
              <span key={s} className="rounded-full border border-border px-2 py-0.5 text-xs">
                {s}
              </span>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
