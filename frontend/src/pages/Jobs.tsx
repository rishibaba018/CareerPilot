import { useCallback, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Loader2, MapPin, Search, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { api } from "@/lib/api";

export interface JobMatch {
  fit_score: number;
  reasoning: string;
  matched_skills: string[];
  missing_skills: string[];
}

export interface Job {
  id: string;
  title: string;
  company: string;
  location: string;
  description: string;
  skills_required: string[];
  salary_range: string;
  work_mode: string;
  my_match: JobMatch | null;
}

function fitColor(score: number) {
  if (score >= 75) return "bg-green-600";
  if (score >= 50) return "bg-yellow-600";
  return "bg-red-600";
}

export default function Jobs() {
  const navigate = useNavigate();
  const [jobs, setJobs] = useState<Job[]>([]);
  const [count, setCount] = useState(0);
  const [page, setPage] = useState(1);
  const [q, setQ] = useState("");
  const [mode, setMode] = useState("");
  const [location, setLocation] = useState("");
  const [prefsApplied, setPrefsApplied] = useState(false);
  const [loading, setLoading] = useState(true);
  const [discovering, setDiscovering] = useState(false);

  // Auto-filter by the user's preferred location ("Remote" maps to work mode)
  useEffect(() => {
    api.get("/profile").then((res) => {
      const locs: string[] = res.data.preferences?.locations ?? [];
      const first = locs.find((l) => l.toLowerCase() !== "remote");
      if (first) setLocation(first.split(",")[0]);
      else if (locs.length > 0) setMode("remote");
      setPrefsApplied(true);
    }).catch(() => setPrefsApplied(true));
  }, []);

  const fetchJobs = useCallback(async () => {
    if (!prefsApplied) return;
    setLoading(true);
    try {
      const res = await api.get("/jobs", { params: { q, mode, location, page } });
      setJobs(res.data.results);
      setCount(res.data.count);
    } finally {
      setLoading(false);
    }
  }, [q, mode, location, page, prefsApplied]);

  useEffect(() => {
    fetchJobs();
  }, [fetchJobs]);

  async function discover() {
    setDiscovering(true);
    try {
      await api.post("/jobs/discover");
      setPage(1);
      await fetchJobs();
    } finally {
      setDiscovering(false);
    }
  }

  const totalPages = Math.max(1, Math.ceil(count / 12));

  return (
    <div className="mx-auto max-w-6xl px-4 py-10">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 className="text-2xl font-bold">Job Feed</h1>
          <p className="text-sm text-muted-foreground">{count} jobs in your pool</p>
        </div>
        <Button onClick={discover} disabled={discovering}>
          {discovering ? (
            <>
              <Loader2 className="h-4 w-4 animate-spin" /> Discovery Agent working…
            </>
          ) : (
            <>
              <Sparkles className="h-4 w-4" /> Find jobs for me
            </>
          )}
        </Button>
      </div>

      <div className="mt-6 flex flex-wrap gap-2">
        <div className="relative flex-1 min-w-52">
          <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input
            className="pl-8"
            placeholder="Search title, company, keywords…"
            value={q}
            onChange={(e) => {
              setQ(e.target.value);
              setPage(1);
            }}
          />
        </div>
        <div className="relative min-w-40">
          <MapPin className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input
            className="pl-8"
            placeholder="Location"
            value={location}
            onChange={(e) => {
              setLocation(e.target.value);
              setPage(1);
            }}
          />
        </div>
        {["", "remote", "hybrid", "onsite"].map((m) => (
          <Button
            key={m || "all"}
            variant={mode === m ? "default" : "outline"}
            size="sm"
            className="h-9"
            onClick={() => {
              setMode(m);
              setPage(1);
            }}
          >
            {m === "" ? "All modes" : m}
          </Button>
        ))}
      </div>

      {loading ? (
        <div className="flex h-48 items-center justify-center text-muted-foreground">
          <Loader2 className="mr-2 h-5 w-5 animate-spin" /> Loading jobs…
        </div>
      ) : jobs.length === 0 ? (
        <div className="mt-12 text-center text-muted-foreground">
          No jobs found. Try "Find jobs for me" or clear filters.
        </div>
      ) : (
        <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {jobs.map((job) => (
            <Card
              key={job.id}
              className="cursor-pointer transition-shadow hover:shadow-md"
              onClick={() => navigate(`/jobs/${job.id}`)}
            >
              <CardHeader className="pb-3">
                <div className="flex items-start justify-between gap-2">
                  <CardTitle className="text-base">{job.title}</CardTitle>
                  {job.my_match && (
                    <span
                      className={`shrink-0 rounded-full px-2 py-0.5 text-xs font-semibold text-white ${fitColor(job.my_match.fit_score)}`}
                    >
                      {job.my_match.fit_score}%
                    </span>
                  )}
                </div>
                <p className="text-sm text-muted-foreground">{job.company}</p>
              </CardHeader>
              <CardContent className="space-y-2 text-sm">
                <p className="flex items-center gap-1 text-muted-foreground">
                  <MapPin className="h-3.5 w-3.5" /> {job.location}
                  {job.work_mode && (
                    <span className="ml-1 rounded bg-muted px-1.5 py-0.5 text-xs">{job.work_mode}</span>
                  )}
                </p>
                {job.salary_range && <p className="text-muted-foreground">{job.salary_range}</p>}
                <div className="flex flex-wrap gap-1 pt-1">
                  {job.skills_required.slice(0, 4).map((s) => (
                    <span key={s} className="rounded-full border border-border px-2 py-0.5 text-xs">
                      {s}
                    </span>
                  ))}
                  {job.skills_required.length > 4 && (
                    <span className="text-xs text-muted-foreground">
                      +{job.skills_required.length - 4}
                    </span>
                  )}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {totalPages > 1 && (
        <div className="mt-8 flex items-center justify-center gap-3">
          <Button variant="outline" size="sm" disabled={page <= 1} onClick={() => setPage(page - 1)}>
            Previous
          </Button>
          <span className="text-sm text-muted-foreground">
            Page {page} of {totalPages}
          </span>
          <Button
            variant="outline"
            size="sm"
            disabled={page >= totalPages}
            onClick={() => setPage(page + 1)}
          >
            Next
          </Button>
        </div>
      )}
    </div>
  );
}
