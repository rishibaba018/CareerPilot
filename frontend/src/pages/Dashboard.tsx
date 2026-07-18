import { useCallback, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { ArrowLeft, ArrowRight, Bot, Loader2, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useAuth } from "@/context/AuthContext";
import { api } from "@/lib/api";

interface AppCard {
  id: string;
  status: string;
  applied_at: string | null;
  job: {
    id: string;
    title: string;
    company: string;
    location: string;
    fit_score: number | null;
  };
}

type Board = Record<string, AppCard[]>;

const COLUMNS = ["saved", "applied", "interview", "offer"] as const;
const COLUMN_LABELS: Record<string, string> = {
  saved: "Saved",
  applied: "Applied (simulated)",
  interview: "Interview",
  offer: "Offer",
};
const FLOW = ["saved", "applied", "interview", "offer"];

export default function Dashboard() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [board, setBoard] = useState<Board | null>(null);
  const [movingId, setMovingId] = useState<string | null>(null);
  const [insights, setInsights] = useState<{ insights: string[]; suggestions: string[] } | null>(null);
  const [coaching, setCoaching] = useState(false);

  async function loadInsights() {
    setCoaching(true);
    try {
      const res = await api.get("/applications/insights");
      setInsights(res.data);
    } finally {
      setCoaching(false);
    }
  }

  const fetchBoard = useCallback(async () => {
    const res = await api.get("/applications");
    setBoard(res.data);
  }, []);

  useEffect(() => {
    fetchBoard();
  }, [fetchBoard]);

  async function move(app: AppCard, direction: 1 | -1) {
    const idx = FLOW.indexOf(app.status);
    const next = FLOW[idx + direction];
    if (!next) return;
    setMovingId(app.id);
    try {
      await api.patch(`/applications/${app.id}`, { status: next });
      await fetchBoard();
    } finally {
      setMovingId(null);
    }
  }

  async function reject(app: AppCard) {
    setMovingId(app.id);
    try {
      await api.patch(`/applications/${app.id}`, { status: "rejected" });
      await fetchBoard();
    } finally {
      setMovingId(null);
    }
  }

  const isEmpty =
    board && COLUMNS.every((c) => board[c].length === 0) && board.rejected.length === 0;

  return (
    <div className="mx-auto max-w-6xl px-4 py-10">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 className="text-2xl font-bold">
            {user?.full_name ? `${user.full_name}'s` : "Your"} pipeline
          </h1>
          <p className="text-sm text-muted-foreground">
            Track every application from Saved to Offer. Submission is simulated for the demo.
          </p>
        </div>
        <Button onClick={() => navigate("/jobs")}>
          <Sparkles className="h-4 w-4" /> Find more jobs
        </Button>
      </div>

      <Card className="mt-6 border-primary/30">
        <CardHeader className="pb-2">
          <CardTitle className="flex items-center gap-2 text-base">
            <Bot className="h-4 w-4 text-primary" /> Tracking Agent insights
          </CardTitle>
        </CardHeader>
        <CardContent>
          {insights ? (
            <div className="grid gap-4 sm:grid-cols-2">
              <div>
                <p className="mb-1 text-xs font-semibold uppercase text-muted-foreground">What I see</p>
                <ul className="list-disc space-y-1 pl-4 text-sm">
                  {insights.insights.map((s) => (
                    <li key={s}>{s}</li>
                  ))}
                </ul>
              </div>
              <div>
                <p className="mb-1 text-xs font-semibold uppercase text-muted-foreground">Do this week</p>
                <ul className="list-disc space-y-1 pl-4 text-sm">
                  {insights.suggestions.map((s) => (
                    <li key={s}>{s}</li>
                  ))}
                </ul>
              </div>
            </div>
          ) : (
            <Button variant="outline" size="sm" onClick={loadInsights} disabled={coaching}>
              {coaching ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" /> Tracking Agent reviewing your pipeline…
                </>
              ) : (
                "Coach me on my pipeline"
              )}
            </Button>
          )}
        </CardContent>
      </Card>

      {!board ? (
        <div className="flex h-48 items-center justify-center text-muted-foreground">
          <Loader2 className="mr-2 h-5 w-5 animate-spin" /> Loading pipeline…
        </div>
      ) : isEmpty ? (
        <div className="mt-16 text-center">
          <p className="text-muted-foreground">
            Nothing here yet. Save a job from the feed, or generate a tailored resume — it
            lands here automatically.
          </p>
          <Button className="mt-4" onClick={() => navigate("/jobs")}>
            Browse jobs
          </Button>
        </div>
      ) : (
        <>
          <div className="mt-8 grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            {COLUMNS.map((col) => (
              <div key={col} className="rounded-lg bg-muted/50 p-3">
                <p className="mb-3 flex items-center justify-between px-1 text-sm font-semibold">
                  {COLUMN_LABELS[col]}
                  <span className="rounded-full bg-muted px-2 text-xs text-muted-foreground">
                    {board[col].length}
                  </span>
                </p>
                <div className="space-y-2">
                  {board[col].map((app) => (
                    <Card key={app.id} className="shadow-sm">
                      <CardContent className="space-y-2 p-3">
                        <button
                          className="text-left text-sm font-medium hover:underline"
                          onClick={() => navigate(`/jobs/${app.job.id}`)}
                        >
                          {app.job.title}
                        </button>
                        <p className="text-xs text-muted-foreground">
                          {app.job.company}
                          {app.job.fit_score !== null && (
                            <span className="ml-2 rounded-full bg-primary/10 px-1.5 py-0.5 font-semibold">
                              {app.job.fit_score}%
                            </span>
                          )}
                        </p>
                        <div className="flex items-center justify-between pt-1">
                          <div className="flex gap-1">
                            <Button
                              variant="ghost"
                              size="sm"
                              className="h-7 px-2"
                              disabled={col === "saved" || movingId === app.id}
                              onClick={() => move(app, -1)}
                            >
                              <ArrowLeft className="h-3.5 w-3.5" />
                            </Button>
                            <Button
                              variant="ghost"
                              size="sm"
                              className="h-7 px-2"
                              disabled={col === "offer" || movingId === app.id}
                              onClick={() => move(app, 1)}
                            >
                              <ArrowRight className="h-3.5 w-3.5" />
                            </Button>
                          </div>
                          <button
                            className="text-xs text-muted-foreground hover:text-destructive"
                            onClick={() => reject(app)}
                          >
                            reject
                          </button>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </div>
            ))}
          </div>
          {board.rejected.length > 0 && (
            <p className="mt-4 text-xs text-muted-foreground">
              Rejected: {board.rejected.map((a) => `${a.job.title} (${a.job.company})`).join(", ")}
            </p>
          )}
        </>
      )}
    </div>
  );
}
