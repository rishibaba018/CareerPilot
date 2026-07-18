import { useNavigate } from "react-router-dom";
import { Bot, FileText, Target } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const steps = [
  {
    icon: FileText,
    title: "1. Upload once",
    text: "Upload your resume one time. AI builds your master profile automatically.",
    tone: "border-sky-200 bg-sky-50/60 [&_svg]:text-sky-600 dark:border-sky-900 dark:bg-sky-950/40",
    iconBg: "bg-sky-500/15",
  },
  {
    icon: Target,
    title: "2. Match instantly",
    text: "AI finds real jobs and scores your fit — with reasons, not just a number.",
    tone: "border-violet-200 bg-violet-50/60 [&_svg]:text-violet-600 dark:border-violet-900 dark:bg-violet-950/40",
    iconBg: "bg-violet-500/15",
  },
  {
    icon: Bot,
    title: "3. Apply smarter",
    text: "Tailored resume, cover letter, and interview prep generated per job.",
    tone: "border-emerald-200 bg-emerald-50/60 [&_svg]:text-emerald-600 dark:border-emerald-900 dark:bg-emerald-950/40",
    iconBg: "bg-emerald-500/15",
  },
];

export default function Landing() {
  const navigate = useNavigate();

  return (
    <div className="relative mx-auto max-w-6xl overflow-hidden px-4">
      <div
        aria-hidden
        className="pointer-events-none absolute left-1/2 top-0 h-[420px] w-[720px] -translate-x-1/2 rounded-full bg-primary/15 blur-3xl"
      />
      <section className="relative py-24 text-center">
        <p className="mx-auto mb-4 w-fit rounded-full border border-primary/30 bg-primary/5 px-3 py-1 text-xs font-medium text-primary">
          9 AI agents · 1 profile · 0 blank pages
        </p>
        <h1 className="mx-auto max-w-3xl bg-gradient-to-r from-primary via-purple-500 to-primary bg-clip-text text-4xl font-bold tracking-tight text-transparent sm:text-6xl">
          Stop applying. Start landing.
        </h1>
        <p className="mx-auto mt-4 max-w-2xl text-lg text-muted-foreground">
          CareerPilot's team of 9 AI agents finds jobs, scores your fit, tailors
          your resume, and writes your cover letters — from one profile you
          create once.
        </p>
        <div className="mt-8 flex justify-center gap-3">
          <Button size="lg" onClick={() => navigate("/register")}>
            Get started free
          </Button>
          <Button size="lg" variant="outline" onClick={() => navigate("/login")}>
            Log in
          </Button>
        </div>
      </section>

      <section className="grid gap-6 pb-24 sm:grid-cols-3">
        {steps.map(({ icon: Icon, title, text, tone, iconBg }) => (
          <Card key={title} className={`transition-all hover:-translate-y-1 hover:shadow-lg ${tone}`}>
            <CardHeader>
              <div className={`mb-2 flex h-11 w-11 items-center justify-center rounded-xl ${iconBg}`}>
                <Icon className="h-6 w-6" />
              </div>
              <CardTitle>{title}</CardTitle>
            </CardHeader>
            <CardContent className="text-sm text-muted-foreground">{text}</CardContent>
          </Card>
        ))}
      </section>
    </div>
  );
}
