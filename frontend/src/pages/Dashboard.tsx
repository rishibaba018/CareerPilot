import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useAuth } from "@/context/AuthContext";

export default function Dashboard() {
  const { user } = useAuth();
  const navigate = useNavigate();

  return (
    <div className="mx-auto max-w-6xl px-4 py-12">
      <h1 className="text-2xl font-bold">
        Welcome{user?.full_name ? `, ${user.full_name}` : ""} 👋
      </h1>
      <p className="mt-1 text-muted-foreground">
        You're logged in. Here's what's coming next.
      </p>
      <div className="mt-8 grid gap-6 sm:grid-cols-3">
        <Card>
          <CardHeader>
            <CardTitle>Resume &amp; Profile</CardTitle>
            <CardDescription>Ready now</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3 text-sm text-muted-foreground">
            <p>Upload your resume and let the Profile Agent build your master profile.</p>
            <Button size="sm" onClick={() => navigate("/onboarding")}>
              Set up profile
            </Button>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Job Feed</CardTitle>
            <CardDescription>Sprint 3</CardDescription>
          </CardHeader>
          <CardContent className="text-sm text-muted-foreground">
            Real jobs matched to your preferences with explained fit scores.
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Applications</CardTitle>
            <CardDescription>Sprint 5</CardDescription>
          </CardHeader>
          <CardContent className="text-sm text-muted-foreground">
            Track every application on a kanban board, from Saved to Offer.
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
