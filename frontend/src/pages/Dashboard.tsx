import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useAuth } from "@/context/AuthContext";

export default function Dashboard() {
  const { user } = useAuth();

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
            <CardDescription>Sprint 2</CardDescription>
          </CardHeader>
          <CardContent className="text-sm text-muted-foreground">
            Upload your resume and let the Profile Agent build your master profile.
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
