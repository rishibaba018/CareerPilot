import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "@/context/AuthContext";

const CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID as string | undefined;
const GSI_SRC = "https://accounts.google.com/gsi/client";

declare global {
  interface Window {
    google?: {
      accounts: {
        id: {
          initialize: (config: object) => void;
          renderButton: (el: HTMLElement, options: object) => void;
        };
      };
    };
  }
}

/** "Sign in with Google" button. Renders nothing unless VITE_GOOGLE_CLIENT_ID is set. */
export default function GoogleSignIn({ onError }: { onError?: (msg: string) => void }) {
  const { loginWithGoogle } = useAuth();
  const navigate = useNavigate();
  const slot = useRef<HTMLDivElement>(null);
  const [failed, setFailed] = useState(false);

  useEffect(() => {
    if (!CLIENT_ID || !slot.current) return;

    const render = () => {
      if (!window.google || !slot.current) return;
      window.google.accounts.id.initialize({
        client_id: CLIENT_ID,
        callback: async (response: { credential: string }) => {
          try {
            await loginWithGoogle(response.credential);
            navigate("/dashboard");
          } catch {
            onError?.("Google sign-in failed. Please try again.");
          }
        },
      });
      window.google.accounts.id.renderButton(slot.current, {
        theme: "outline",
        size: "large",
        width: 320,
        text: "continue_with",
      });
    };

    if (window.google) {
      render();
      return;
    }
    const script = document.createElement("script");
    script.src = GSI_SRC;
    script.async = true;
    script.onload = render;
    script.onerror = () => setFailed(true);
    document.head.appendChild(script);
  }, [loginWithGoogle, navigate, onError]);

  if (!CLIENT_ID || failed) return null;

  return (
    <div className="space-y-3">
      <div className="flex items-center gap-3">
        <span className="h-px flex-1 bg-border" />
        <span className="text-xs text-muted-foreground">or</span>
        <span className="h-px flex-1 bg-border" />
      </div>
      <div ref={slot} className="flex justify-center" />
    </div>
  );
}
