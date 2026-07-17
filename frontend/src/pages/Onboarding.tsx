import { useEffect, useState, type ChangeEvent } from "react";
import { useNavigate } from "react-router-dom";
import { isAxiosError } from "axios";
import { Bot, FileUp, Loader2, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { api } from "@/lib/api";

interface EducationItem {
  degree: string;
  institution: string;
  year: string;
}
interface ExperienceItem {
  title: string;
  company: string;
  duration: string;
  description: string;
}
interface ProjectItem {
  name: string;
  description: string;
  technologies: string[];
}

const selectClass =
  "flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring";

export default function Onboarding() {
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  const [atsScore, setAtsScore] = useState<number | null>(null);
  const [atsFeedback, setAtsFeedback] = useState<string[]>([]);
  const [fullName, setFullName] = useState("");
  const [phone, setPhone] = useState("");
  const [location, setLocation] = useState("");
  const [skills, setSkills] = useState("");
  const [education, setEducation] = useState<EducationItem[]>([]);
  const [experience, setExperience] = useState<ExperienceItem[]>([]);
  const [projects, setProjects] = useState<ProjectItem[]>([]);

  const [role, setRole] = useState("");
  const [prefLocations, setPrefLocations] = useState("");
  const [workMode, setWorkMode] = useState("any");
  const [expLevel, setExpLevel] = useState("fresher");

  // Pre-fill from an existing profile so revisiting the wizard keeps edits
  useEffect(() => {
    api.get("/profile").then((res) => {
      const p = res.data;
      setFullName(p.full_name ?? "");
      setPhone(p.phone ?? "");
      setLocation(p.location ?? "");
      setSkills((p.skills ?? []).join(", "));
      setEducation(p.education ?? []);
      setExperience(p.experience ?? []);
      setProjects(p.projects ?? []);
      const prefs = p.preferences ?? {};
      setRole(prefs.role ?? "");
      setPrefLocations((prefs.locations ?? []).join(", "));
      setWorkMode(prefs.mode ?? "any");
      setExpLevel(prefs.exp_level ?? "fresher");
    });
  }, []);

  function onFileChange(e: ChangeEvent<HTMLInputElement>) {
    setError("");
    setFile(e.target.files?.[0] ?? null);
  }

  async function handleUpload() {
    if (!file) return;
    setError("");
    setUploading(true);
    try {
      const form = new FormData();
      form.append("file", file);
      const res = await api.post("/resumes/upload", form);
      const { profile, resume, ats_feedback } = res.data;
      setAtsScore(resume.ats_score);
      setAtsFeedback(ats_feedback ?? []);
      setFullName(profile.full_name ?? "");
      setPhone(profile.phone ?? "");
      setLocation(profile.location ?? "");
      setSkills((profile.skills ?? []).join(", "));
      setEducation(profile.education ?? []);
      setExperience(profile.experience ?? []);
      setProjects(profile.projects ?? []);
      setStep(2);
    } catch (err) {
      if (isAxiosError(err) && err.response?.data?.error?.message) {
        setError(err.response.data.error.message);
      } else {
        setError("Upload failed. Please try again.");
      }
    } finally {
      setUploading(false);
    }
  }

  async function handleFinish() {
    setError("");
    setSaving(true);
    try {
      await api.put("/profile", {
        full_name: fullName,
        phone,
        location,
        skills: skills.split(",").map((s) => s.trim()).filter(Boolean),
        education,
        experience,
        projects,
        preferences: {
          role,
          locations: prefLocations.split(",").map((s) => s.trim()).filter(Boolean),
          mode: workMode,
          exp_level: expLevel,
        },
      });
      navigate("/dashboard");
    } catch {
      setError("Couldn't save your profile. Please try again.");
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="mx-auto max-w-3xl px-4 py-10">
      <div className="mb-8 flex items-center gap-3">
        {[1, 2, 3].map((s) => (
          <div key={s} className="flex items-center gap-3">
            <div
              className={`flex h-8 w-8 items-center justify-center rounded-full text-sm font-medium ${
                s <= step ? "bg-primary text-primary-foreground" : "bg-muted text-muted-foreground"
              }`}
            >
              {s}
            </div>
            {s < 3 && <div className="h-px w-10 bg-border" />}
          </div>
        ))}
        <span className="ml-2 text-sm text-muted-foreground">
          {step === 1 ? "Upload resume" : step === 2 ? "Review your AI-filled profile" : "Job preferences"}
        </span>
      </div>

      {step === 1 && (
        <Card>
          <CardHeader>
            <CardTitle>Upload your resume</CardTitle>
            <CardDescription>
              PDF, max 5 MB. The Profile Agent will extract your skills, education,
              experience, and projects — you review everything before it's saved.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <label
              htmlFor="resume-file"
              className="flex cursor-pointer flex-col items-center gap-2 rounded-lg border-2 border-dashed border-border p-10 text-center hover:bg-muted"
            >
              <FileUp className="h-8 w-8 text-muted-foreground" />
              <span className="text-sm">
                {file ? file.name : "Click to choose a PDF resume"}
              </span>
              <input
                id="resume-file"
                type="file"
                accept="application/pdf,.pdf"
                className="hidden"
                onChange={onFileChange}
              />
            </label>
            {error && <p className="text-sm text-destructive">{error}</p>}
            <div className="flex items-center justify-between">
              <Button variant="ghost" onClick={() => navigate("/dashboard")}>
                I'll do this later
              </Button>
              <Button onClick={handleUpload} disabled={!file || uploading}>
                {uploading ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Profile Agent is reading your resume…
                  </>
                ) : (
                  <>
                    <Bot className="h-4 w-4" /> Analyze with AI
                  </>
                )}
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {step === 2 && (
        <div className="space-y-6">
          {atsScore !== null && (
            <Card>
              <CardContent className="flex items-center gap-6 p-6">
                <div className="flex h-20 w-20 shrink-0 flex-col items-center justify-center rounded-full border-4 border-primary">
                  <span className="text-2xl font-bold">{atsScore}</span>
                  <span className="text-[10px] text-muted-foreground">ATS</span>
                </div>
                <div>
                  <p className="font-medium">ATS compatibility score</p>
                  <ul className="mt-1 list-disc pl-4 text-sm text-muted-foreground">
                    {atsFeedback.map((tip) => (
                      <li key={tip}>{tip}</li>
                    ))}
                  </ul>
                </div>
              </CardContent>
            </Card>
          )}

          <Card>
            <CardHeader>
              <CardTitle>Your details</CardTitle>
              <CardDescription>Extracted by AI — fix anything that's off.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid gap-4 sm:grid-cols-3">
                <div className="space-y-2">
                  <Label htmlFor="ob-name">Full name</Label>
                  <Input id="ob-name" value={fullName} onChange={(e) => setFullName(e.target.value)} />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="ob-phone">Phone</Label>
                  <Input id="ob-phone" value={phone} onChange={(e) => setPhone(e.target.value)} />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="ob-location">Location</Label>
                  <Input id="ob-location" value={location} onChange={(e) => setLocation(e.target.value)} />
                </div>
              </div>
              <div className="space-y-2">
                <Label htmlFor="ob-skills">Skills (comma-separated)</Label>
                <Input id="ob-skills" value={skills} onChange={(e) => setSkills(e.target.value)} />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Experience</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {experience.length === 0 && (
                <p className="text-sm text-muted-foreground">Nothing extracted.</p>
              )}
              {experience.map((exp, i) => (
                <div key={i} className="space-y-2 rounded-lg border border-border p-4">
                  <div className="grid gap-2 sm:grid-cols-3">
                    <Input
                      placeholder="Title"
                      value={exp.title}
                      onChange={(e) =>
                        setExperience(experience.map((x, j) => (j === i ? { ...x, title: e.target.value } : x)))
                      }
                    />
                    <Input
                      placeholder="Company"
                      value={exp.company}
                      onChange={(e) =>
                        setExperience(experience.map((x, j) => (j === i ? { ...x, company: e.target.value } : x)))
                      }
                    />
                    <Input
                      placeholder="Duration"
                      value={exp.duration}
                      onChange={(e) =>
                        setExperience(experience.map((x, j) => (j === i ? { ...x, duration: e.target.value } : x)))
                      }
                    />
                  </div>
                  <textarea
                    className="w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm"
                    rows={2}
                    value={exp.description}
                    onChange={(e) =>
                      setExperience(experience.map((x, j) => (j === i ? { ...x, description: e.target.value } : x)))
                    }
                  />
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setExperience(experience.filter((_, j) => j !== i))}
                  >
                    <Trash2 className="h-3.5 w-3.5" /> Remove
                  </Button>
                </div>
              ))}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Education</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {education.map((edu, i) => (
                <div key={i} className="grid gap-2 sm:grid-cols-[2fr_2fr_1fr_auto]">
                  <Input
                    placeholder="Degree"
                    value={edu.degree}
                    onChange={(e) =>
                      setEducation(education.map((x, j) => (j === i ? { ...x, degree: e.target.value } : x)))
                    }
                  />
                  <Input
                    placeholder="Institution"
                    value={edu.institution}
                    onChange={(e) =>
                      setEducation(education.map((x, j) => (j === i ? { ...x, institution: e.target.value } : x)))
                    }
                  />
                  <Input
                    placeholder="Year"
                    value={edu.year}
                    onChange={(e) =>
                      setEducation(education.map((x, j) => (j === i ? { ...x, year: e.target.value } : x)))
                    }
                  />
                  <Button variant="ghost" size="sm" onClick={() => setEducation(education.filter((_, j) => j !== i))}>
                    <Trash2 className="h-3.5 w-3.5" />
                  </Button>
                </div>
              ))}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Projects</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {projects.map((proj, i) => (
                <div key={i} className="space-y-2 rounded-lg border border-border p-4">
                  <Input
                    placeholder="Project name"
                    value={proj.name}
                    onChange={(e) =>
                      setProjects(projects.map((x, j) => (j === i ? { ...x, name: e.target.value } : x)))
                    }
                  />
                  <textarea
                    className="w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm"
                    rows={2}
                    value={proj.description}
                    onChange={(e) =>
                      setProjects(projects.map((x, j) => (j === i ? { ...x, description: e.target.value } : x)))
                    }
                  />
                  <Button variant="ghost" size="sm" onClick={() => setProjects(projects.filter((_, j) => j !== i))}>
                    <Trash2 className="h-3.5 w-3.5" /> Remove
                  </Button>
                </div>
              ))}
            </CardContent>
          </Card>

          <div className="flex justify-between">
            <Button variant="outline" onClick={() => setStep(1)}>
              Back
            </Button>
            <Button onClick={() => setStep(3)}>Looks good — set preferences</Button>
          </div>
        </div>
      )}

      {step === 3 && (
        <Card>
          <CardHeader>
            <CardTitle>What are you looking for?</CardTitle>
            <CardDescription>The Job Discovery Agent uses this to find matching roles.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="ob-role">Desired role</Label>
              <Input
                id="ob-role"
                placeholder="e.g. Backend Developer"
                value={role}
                onChange={(e) => setRole(e.target.value)}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="ob-pref-loc">Preferred locations (comma-separated)</Label>
              <Input
                id="ob-pref-loc"
                placeholder="e.g. Hyderabad, Bangalore, Remote"
                value={prefLocations}
                onChange={(e) => setPrefLocations(e.target.value)}
              />
            </div>
            <div className="grid gap-4 sm:grid-cols-2">
              <div className="space-y-2">
                <Label htmlFor="ob-mode">Work mode</Label>
                <select id="ob-mode" className={selectClass} value={workMode} onChange={(e) => setWorkMode(e.target.value)}>
                  <option value="any">Any</option>
                  <option value="remote">Remote</option>
                  <option value="hybrid">Hybrid</option>
                  <option value="onsite">On-site</option>
                </select>
              </div>
              <div className="space-y-2">
                <Label htmlFor="ob-level">Experience level</Label>
                <select id="ob-level" className={selectClass} value={expLevel} onChange={(e) => setExpLevel(e.target.value)}>
                  <option value="fresher">Fresher / New grad</option>
                  <option value="junior">Junior (1-2 yrs)</option>
                  <option value="mid">Mid (3-5 yrs)</option>
                  <option value="senior">Senior (5+ yrs)</option>
                </select>
              </div>
            </div>
            {error && <p className="text-sm text-destructive">{error}</p>}
            <div className="flex justify-between">
              <Button variant="outline" onClick={() => setStep(2)}>
                Back
              </Button>
              <Button onClick={handleFinish} disabled={saving}>
                {saving ? "Saving…" : "Finish setup"}
              </Button>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
