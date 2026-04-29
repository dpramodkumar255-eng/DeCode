import React from "react";
import { useQuery } from "@tanstack/react-query";
import { base44 } from "@/api/base44Client";
import { Link } from "react-router-dom";
import { User, Search, BarChart3, TrendingUp, Target, BookOpen, Zap } from "lucide-react";
import { Button } from "@/components/ui/button";
import StatsCard from "@/components/dashboard/StatsCard";
import ReadinessGauge from "@/components/dashboard/ReadinessGauge";
import SkillGapChart from "@/components/dashboard/SkillGapChart";
import ImprovementChecklist from "@/components/dashboard/ImprovementChecklist";
import ScoreBreakdown from "@/components/dashboard/ScoreBreakdown";

export default function Dashboard() {
  const { data: profiles = [] } = useQuery({
    queryKey: ["profiles"],
    queryFn: () => base44.entities.StudentProfile.list("-created_date", 10),
  });

  const { data: results = [] } = useQuery({
    queryKey: ["results"],
    queryFn: () => base44.entities.AnalysisResult.list("-created_date", 20),
  });

  const latestResult = results[0];
  const avgMatch = results.length > 0
    ? Math.round(results.reduce((sum, r) => sum + (r.match_percentage || 0), 0) / results.length)
    : 0;

  const hasData = results.length > 0;

  return (
    <div className="space-y-8">
      {/* Hero header */}
      <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-foreground">Placement Readiness</h1>
          <p className="text-muted-foreground mt-1">Track your market fit and improve your placement chances</p>
        </div>
        <div className="flex gap-2">
          <Link to="/profile">
            <Button variant="outline" className="rounded-xl gap-2 text-sm">
              <User className="w-4 h-4" /> Profile
            </Button>
          </Link>
          <Link to="/analyze">
            <Button className="rounded-xl gap-2 text-sm">
              <Search className="w-4 h-4" /> New Analysis
            </Button>
          </Link>
        </div>
      </div>

      {/* Stats row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatsCard title="Profiles Created" value={profiles.length} icon={User} subtitle="Student profiles" />
        <StatsCard title="Analyses Run" value={results.length} icon={BarChart3} subtitle="Job comparisons" />
        <StatsCard title="Avg. Match" value={`${avgMatch}%`} icon={TrendingUp} subtitle="Across all jobs" />
        <StatsCard
          title="Skills Tracked"
          value={profiles.reduce((sum, p) => sum + (p.skills?.length || 0), 0)}
          icon={Zap}
          subtitle="Total skills"
        />
      </div>

      {hasData ? (
        <>
          {/* Main dashboard grid */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <ReadinessGauge score={latestResult.match_percentage || 0} />
            <div className="lg:col-span-2">
              <SkillGapChart
                matchedSkills={latestResult.matched_skills || []}
                missingSkills={latestResult.missing_skills || []}
              />
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <ScoreBreakdown
              skillScore={latestResult.skill_match_score || 0}
              experienceScore={latestResult.experience_score || 0}
              educationScore={latestResult.education_score || 0}
            />
            <ImprovementChecklist improvements={latestResult.improvements || []} />
          </div>

          {/* Summary card */}
          {latestResult.summary && (
            <div className="rounded-2xl bg-card border border-border p-6">
              <div className="flex items-center gap-2 mb-3">
                <BookOpen className="w-4 h-4 text-primary" />
                <h3 className="text-sm font-medium text-muted-foreground">Latest Analysis Summary</h3>
              </div>
              <p className="text-sm text-foreground leading-relaxed">{latestResult.summary}</p>
              <div className="mt-3 flex items-center gap-2 text-xs text-muted-foreground">
                <Target className="w-3.5 h-3.5" />
                <span>Target: {latestResult.job_title}</span>
              </div>
            </div>
          )}
        </>
      ) : (
        <div className="rounded-2xl bg-card border border-border p-12 text-center">
          <div className="w-16 h-16 rounded-2xl bg-primary/10 flex items-center justify-center mx-auto mb-4">
            <Sparkles className="w-8 h-8 text-primary" />
          </div>
          <h2 className="text-xl font-semibold text-foreground mb-2">Get Started</h2>
          <p className="text-muted-foreground max-w-md mx-auto mb-6">
            Create a student profile and run your first job analysis to see your placement readiness score and personalized recommendations.
          </p>
          <div className="flex justify-center gap-3">
            <Link to="/profile">
              <Button variant="outline" className="rounded-xl">Create Profile</Button>
            </Link>
            <Link to="/analyze">
              <Button className="rounded-xl">Run Analysis</Button>
            </Link>
          </div>
        </div>
      )}
    </div>
  );
}

  {/* Stats row */}
  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
    <StatsCard title="Profiles Created" value={profiles.length} icon={User} subtitle="Student profiles" />
    <StatsCard title="Analyses Run" value={results.length} icon={BarChart3} subtitle="Job comparisons" />
    <StatsCard title="Avg. Match" value={`${avgMatch}%`} icon={TrendingUp} subtitle="Across all jobs" />
    <StatsCard
      title="Skills Tracked"
      value={profiles.reduce((sum, p) => sum + (p.skills?.length || 0), 0)}
      icon={Zap}
      subtitle="Total skills"
    />
  </div>

  {hasData ? (
    <>
      {/* Main dashboard grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <ReadinessGauge score={latestResult.match_percentage || 0} />
        <div className="lg:col-span-2">
          <SkillGapChart
            matchedSkills={latestResult.matched_skills || []}
            missingSkills={latestResult.missing_skills || []}
          />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ScoreBreakdown
          skillScore={latestResult.skill_match_score || 0}
          experienceScore={latestResult.experience_score || 0}
          educationScore={latestResult.education_score || 0}
        />
        <ImprovementChecklist improvements={latestResult.improvements || []} />
      </div>

      {/* Summary card */}
      {latestResult.summary && (
        <div className="rounded-2xl bg-card border border-border p-6">
          <div className="flex items-center gap-2 mb-3">
            <BookOpen className="w-4 h-4 text-primary" />
            <h3 className="text-sm font-medium text-muted-foreground">Latest Analysis Summary</h3>
          </div>
          <p className="text-sm text-foreground leading-relaxed">{latestResult.summary}</p>
          <div className="mt-3 flex items-center gap-2 text-xs text-muted-foreground">
            <Target className="w-3.5 h-3.5" />
            <span>Target: {latestResult.job_title}</span>
          </div>
        </div>
      )}
    </>
  ) : (
    <div className="rounded-2xl bg-card border border-border p-12 text-center">
      <div className="w-16 h-16 rounded-2xl bg-primary/10 flex items-center justify-center mx-auto mb-4">
        <Sparkles className="w-8 h-8 text-primary" />
      </div>
      <h2 className="text-xl font-semibold text-foreground mb-2">Get Started</h2>
      <p className="text-muted-foreground max-w-md mx-auto mb-6">
        Create a student profile and run your first job analysis to see your placement readiness score and personalized recommendations.
      </p>
      <div className="flex justify-center gap-3">
        <Link to="/profile">
          <Button variant="outline" className="rounded-xl">Create Profile</Button>
        </Link>
        <Link to="/analyze">
          <Button className="rounded-xl">Run Analysis</Button>
        </Link>
      </div>
    </div>
  )}
</div>
  );
}
