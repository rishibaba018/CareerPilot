import { useNavigate } from "react-router-dom";
import { Bot, FileText, Target } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const steps = [
  {
    icon: FileText,
    title: "1. Upload once",
    text: "Upload your resume one time. AI builds your master profile automatically.",
  },
  {
    icon: Target,
    title: "2. Match instantly",
    text: "AI finds real jobs and scores your fit — with reasons, not just a number.",
  },
  {
    icon: Bot,
    title: "3. Apply smarter",
    text: "Tailored resume, cover letter, and interview prep generated per job.",
  },
];

export default function Landing() {
  const navigate = useNavigate();

  return (
    <div className="mx-auto max-w-6xl px-4">
      <section className="py-24 text-center">
        <h1 className="mx-auto max-w-3xl text-4xl font-bold tracking-tight sm:text-5xl">
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
        {steps.map(({ icon: Icon, title, text }) => (
          <Card key={title}>
            <CardHeader>
              <Icon className="mb-2 h-8 w-8" />
              <CardTitle>{title}</CardTitle>
            </CardHeader>
            <CardContent className="text-sm text-muted-foreground">{text}</CardContent>
          </Card>
        ))}
      </section>
    </div>
  );
}
