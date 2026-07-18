import { useEffect, useState } from "react";
import { Bot, Check, Loader2 } from "lucide-react";

/** Animated "agents at work" strip shown during long AI calls (master-plan §18.1).
 *  Steps advance on a timer and the last step pulses until the real call resolves. */
export default function AgentVisualizer({ steps }: { steps: string[] }) {
  const [active, setActive] = useState(0);

  useEffect(() => {
    const t = setInterval(
      () => setActive((a) => Math.min(a + 1, steps.length - 1)),
      2200
    );
    return () => clearInterval(t);
  }, [steps.length]);

  return (
    <div className="mx-auto w-full max-w-md space-y-3 rounded-xl border border-primary/30 bg-primary/5 p-5">
      <p className="flex items-center gap-2 text-sm font-semibold text-primary">
        <Bot className="h-4 w-4 animate-pulse" /> Agents at work
      </p>
      <ul className="space-y-2">
        {steps.map((label, i) => (
          <li key={label} className="flex items-center gap-2 text-sm">
            {i < active ? (
              <Check className="h-4 w-4 shrink-0 text-green-600" />
            ) : i === active ? (
              <Loader2 className="h-4 w-4 shrink-0 animate-spin text-primary" />
            ) : (
              <span className="h-4 w-4 shrink-0 rounded-full border border-border" />
            )}
            <span className={i <= active ? "" : "text-muted-foreground"}>{label}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
