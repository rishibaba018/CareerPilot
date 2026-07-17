import { Link, Outlet, useNavigate } from "react-router-dom";
import { Rocket } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/context/AuthContext";

export default function Layout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex flex-col">
      <header className="border-b border-border">
        <div className="mx-auto flex h-14 max-w-6xl items-center justify-between px-4">
          <Link to="/" className="flex items-center gap-2 font-semibold">
            <Rocket className="h-5 w-5" />
            CareerPilot
          </Link>
          <nav className="flex items-center gap-2">
            {user ? (
              <>
                <span className="mr-2 hidden text-sm text-muted-foreground sm:inline">
                  {user.full_name || user.email}
                </span>
                <Button variant="ghost" size="sm" onClick={() => navigate("/jobs")}>
                  Jobs
                </Button>
                <Button variant="outline" size="sm" onClick={() => navigate("/dashboard")}>
                  Dashboard
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => {
                    logout();
                    navigate("/");
                  }}
                >
                  Log out
                </Button>
              </>
            ) : (
              <>
                <Button variant="ghost" size="sm" onClick={() => navigate("/login")}>
                  Log in
                </Button>
                <Button size="sm" onClick={() => navigate("/register")}>
                  Get started
                </Button>
              </>
            )}
          </nav>
        </div>
      </header>
      <main className="flex-1">
        <Outlet />
      </main>
    </div>
  );
}
