import { useCallback, useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { ArrowLeft, Download, FileText, Loader2, Mail, RefreshCw } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { api } from "@/lib/api";

interface Sections {
  summary: string;
  skills: string[];
  experience: { title: string; company: string; duration: string; bullets: string[] }[];
  projects: { name: string; bullets: string[]; technologies: string[] }[];
  education: { degree: string; institution: string; year: string }[];
}

interface OptimizeResult {
  document_id: string;
  original_ats_score: number | null;
  new_ats_score: number;
  sections: Sections;
  ats_improvements: string[];
}

interface CoverLetterResult {
  document_id: string;
  cover_letter: string;
  tone: string;
}

interface OriginalProfile {
  full_name: string;
  skills: string[];
  experience: { title: string; company: string; duration: string; description: string }[];
  projects: { name: string; description: string; technologies: string[] }[];
  education: { degree: string; institution: string; year: string }[];
}

async function downloadDoc(docId: string, filename: string) {
  const res = await api.get(`/documents/${docId}/download`, { responseType: "blob" });
  const url = URL.createObjectURL(res.data);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

export default function ResumeStudio() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [original, setOriginal] = useState<OriginalProfile | null>(null);
  const [result, setResult] = useState<OptimizeResult | null>(null);
  const [letter, setLetter] = useState<CoverLetterResult | null>(null);
  const [optimizing, setOptimizing] = useState(true);
  const [writingLetter, setWritingLetter] = useState(false);
  const [error, setError] = useState("");

  const optimize = useCallback(
    async (refresh = false) => {
      setError("");
      setOptimizing(true);
      try {
        const [prof, opt] = await Promise.all([
          api.get("/profile"),
          api.post(`/jobs/${id}/optimize-resume${refresh ? "?refresh=1" : ""}`),
        ]);
        setOriginal(prof.data);
        setResult(opt.data);
      } catch {
        setError("Our AI is busy, please retry in a moment.");
      } finally {
        setOptimizing(false);
      }
    },
    [id]
  );

  useEffect(() => {
    optimize();
  }, [optimize]);

  async function generateLetter(refresh = false) {
    setError("");
    setWritingLetter(true);
    try {
      const res = await api.post(`/jobs/${id}/cover-letter${refresh ? "?refresh=1" : ""}`);
      setLetter(res.data);
    } catch {
      setError("Our AI is busy, please retry in a moment.");
    } finally {
      setWritingLetter(false);
    }
  }

  return (
    <div className="mx-auto max-w-6xl px-4 py-10">
      <Button variant="ghost" size="sm" onClick={() => navigate(`/jobs/${id}`)}>
        <ArrowLeft className="h-4 w-4" /> Back to job
      </Button>
      <h1 className="mt-2 text-2xl font-bold">Resume Studio</h1>
      {error && <p className="mt-2 text-sm text-destructive">{error}</p>}

      {optimizing ? (
        <div className="flex h-64 flex-col items-center justify-center gap-3 text-muted-foreground">
          <Loader2 className="h-8 w-8 animate-spin" />
          <p>Resume Agent is tailoring your resume for this job…</p>
        </div>
      ) : result ? (
        <>
          <Card className="mt-6">
            <CardContent className="flex flex-wrap items-center justify-between gap-6 p-6">
              <div className="flex items-center gap-6">
                <div className="text-center">
                  <p className="text-3xl font-bold text-muted-foreground">
                    {result.original_ats_score ?? "—"}
                  </p>
                  <p className="text-xs text-muted-foreground">ATS before</p>
                </div>
                <span className="text-2xl text-muted-foreground">→</span>
                <div className="text-center">
                  <p className="text-3xl font-bold text-green-600">{result.new_ats_score}</p>
                  <p className="text-xs text-muted-foreground">ATS after</p>
                </div>
                <ul className="ml-4 hidden max-w-md list-disc pl-4 text-xs text-muted-foreground md:block">
                  {result.ats_improvements.slice(0, 3).map((tip) => (
                    <li key={tip}>{tip}</li>
                  ))}
                </ul>
              </div>
              <div className="flex gap-2">
                <Button variant="outline" size="sm" onClick={() => optimize(true)}>
                  <RefreshCw className="h-3.5 w-3.5" /> Regenerate
                </Button>
                <Button size="sm" onClick={() => downloadDoc(result.document_id, "tailored_resume.pdf")}>
                  <Download className="h-3.5 w-3.5" /> Download PDF
                </Button>
              </div>
            </CardContent>
          </Card>

          <div className="mt-6 grid gap-6 lg:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-base">
                  <FileText className="h-4 w-4" /> Original profile
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4 text-sm">
                {original && (
                  <>
                    <div className="flex flex-wrap gap-1">
                      {original.skills.map((s) => (
                        <span key={s} className="rounded-full border border-border px-2 py-0.5 text-xs">
                          {s}
                        </span>
                      ))}
                    </div>
                    {original.experience.map((e, i) => (
                      <div key={i}>
                        <p className="font-medium">
                          {e.title} — {e.company}{" "}
                          <span className="font-normal text-muted-foreground">{e.duration}</span>
                        </p>
                        <p className="text-muted-foreground">{e.description}</p>
                      </div>
                    ))}
                    {original.projects.map((p, i) => (
                      <div key={i}>
                        <p className="font-medium">{p.name}</p>
                        <p className="text-muted-foreground">{p.description}</p>
                      </div>
                    ))}
                  </>
                )}
              </CardContent>
            </Card>

            <Card className="border-green-600/40">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-base">
                  <FileText className="h-4 w-4 text-green-600" /> Tailored for this job
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4 text-sm">
                <p className="italic text-muted-foreground">{result.sections.summary}</p>
                <div className="flex flex-wrap gap-1">
                  {result.sections.skills.map((s) => (
                    <span
                      key={s}
                      className="rounded-full bg-green-600/10 px-2 py-0.5 text-xs text-green-700 dark:text-green-400"
                    >
                      {s}
                    </span>
                  ))}
                </div>
                {result.sections.experience.map((e, i) => (
                  <div key={i}>
                    <p className="font-medium">
                      {e.title} — {e.company}{" "}
                      <span className="font-normal text-muted-foreground">{e.duration}</span>
                    </p>
                    <ul className="list-disc pl-5 text-muted-foreground">
                      {e.bullets.map((b) => (
                        <li key={b}>{b}</li>
                      ))}
                    </ul>
                  </div>
                ))}
                {result.sections.projects.map((p, i) => (
                  <div key={i}>
                    <p className="font-medium">{p.name}</p>
                    <ul className="list-disc pl-5 text-muted-foreground">
                      {p.bullets.map((b) => (
                        <li key={b}>{b}</li>
                      ))}
                    </ul>
                  </div>
                ))}
              </CardContent>
            </Card>
          </div>
        </>
      ) : null}

      <Card className="mt-6">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-base">
            <Mail className="h-4 w-4" /> Cover letter
          </CardTitle>
        </CardHeader>
        <CardContent>
          {letter ? (
            <>
              <p className="mb-3 text-xs text-muted-foreground">Tone: {letter.tone}</p>
              <p className="whitespace-pre-line text-sm leading-relaxed">{letter.cover_letter}</p>
              <div className="mt-4 flex gap-2">
                <Button variant="outline" size="sm" onClick={() => generateLetter(true)} disabled={writingLetter}>
                  <RefreshCw className="h-3.5 w-3.5" /> Regenerate
                </Button>
                <Button size="sm" onClick={() => downloadDoc(letter.document_id, "cover_letter.pdf")}>
                  <Download className="h-3.5 w-3.5" /> Download PDF
                </Button>
              </div>
            </>
          ) : (
            <Button onClick={() => generateLetter()} disabled={writingLetter}>
              {writingLetter ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" /> Cover Letter Agent writing…
                </>
              ) : (
                "Generate cover letter"
              )}
            </Button>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
