"use client";

import {
  Users,
  UserCheck,
  UsersRound,
  BrainCircuit,
  ArrowUpRight,
  UserPlus,
  Plus,
  FileText,
  Activity,
  Clock,
  CheckCircle2,
} from "lucide-react";
import Link from "next/link";

const stats = [
  {
    title: "Total Users",
    value: "0",
    description: "Users in your organization",
    icon: Users,
  },
  {
    title: "Active Users",
    value: "0",
    description: "Currently active users",
    icon: UserCheck,
  },
  {
    title: "Teams",
    value: "0",
    description: "Teams in your organization",
    icon: UsersRound,
  },
  {
    title: "AI Insights",
    value: "0",
    description: "Insights generated",
    icon: BrainCircuit,
  },
];

const quickActions = [
  {
    title: "Invite User",
    description: "Add a new member to your organization",
    icon: UserPlus,
    href: "/users/invite",
  },
  {
    title: "Create Team",
    description: "Create a team and manage members",
    icon: UsersRound,
    href: "/teams",
  },
  {
    title: "Create Decision",
    description: "Start a new business decision analysis",
    icon: BrainCircuit,
    href: "/dashboard",
  },
];

export default function DashboardPage() {
  return (
    <div className="min-h-screen bg-[#f7f9fc] px-4 py-6 sm:px-6 lg:px-8">
      <div className="mx-auto w-full max-w-[1600px]">

        {/* Header */}
        <div className="mb-8">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h1 className="text-3xl font-bold tracking-tight text-[#172033] sm:text-4xl">
                Dashboard
              </h1>

              <p className="mt-2 text-sm text-[#667085] sm:text-base">
                Welcome to BusinessPilot. Here&apos;s an overview of your
                organization.
              </p>
            </div>

            <Link
              href="/users/invite"
              className="inline-flex w-fit items-center gap-2 rounded-lg bg-[#126df5] px-5 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-[#0d5ed7]"
            >
              <UserPlus size={18} />
              Invite User
            </Link>
          </div>
        </div>

        {/* Overview Cards */}
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 xl:grid-cols-4">
          {stats.map((stat) => {
            const Icon = stat.icon;

            return (
              <div
                key={stat.title}
                className="rounded-2xl border border-[#e5eaf1] bg-white p-6 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md"
              >
                <div className="flex items-start justify-between">
                  <div>
                    <p className="text-sm font-medium text-[#667085]">
                      {stat.title}
                    </p>

                    <h2 className="mt-3 text-3xl font-bold text-[#172033]">
                      {stat.value}
                    </h2>
                  </div>

                  <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-[#eef5ff] text-[#126df5]">
                    <Icon size={24} />
                  </div>
                </div>

                <p className="mt-4 text-sm text-[#98a2b3]">
                  {stat.description}
                </p>
              </div>
            );
          })}
        </div>

        {/* Main Grid */}
        <div className="mt-6 grid grid-cols-1 gap-6 xl:grid-cols-3">

          {/* Decision Intelligence */}
          <div className="xl:col-span-2">
            <div className="h-full rounded-2xl border border-[#e5eaf1] bg-white p-6 shadow-sm">
              <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <div className="flex items-center gap-3">
                    <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-[#eef5ff] text-[#126df5]">
                      <BrainCircuit size={23} />
                    </div>

                    <div>
                      <h2 className="text-xl font-bold text-[#172033]">
                        Decision Intelligence
                      </h2>

                      <p className="mt-1 text-sm text-[#667085]">
                        Analyze business decisions using multiple factors.
                      </p>
                    </div>
                  </div>
                </div>

                <Link
                  href="/dashboard"
                  className="inline-flex items-center gap-2 text-sm font-semibold text-[#126df5] hover:text-[#0d5ed7]"
                >
                  View decisions
                  <ArrowUpRight size={17} />
                </Link>
              </div>

              <div className="mt-8 rounded-xl border border-dashed border-[#dce2ea] bg-[#fafbfc] px-6 py-12 text-center">
                <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-white text-[#126df5] shadow-sm">
                  <BrainCircuit size={30} />
                </div>

                <h3 className="mt-5 text-lg font-bold text-[#172033]">
                  No decisions yet
                </h3>

                <p className="mx-auto mt-2 max-w-md text-sm leading-6 text-[#667085]">
                  Create your first business decision to compare options,
                  evaluate important factors, and generate structured insights.
                </p>

                <button
                  onClick={() =>
                    alert("Decision creation will be connected to the backend later.")
                  }
                  className="mt-6 inline-flex items-center gap-2 rounded-lg bg-[#126df5] px-5 py-3 text-sm font-semibold text-white transition hover:bg-[#0d5ed7]"
                >
                  <Plus size={18} />
                  Create Decision
                </button>
              </div>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="rounded-2xl border border-[#e5eaf1] bg-white p-6 shadow-sm">
            <div>
              <h2 className="text-xl font-bold text-[#172033]">
                Quick Actions
              </h2>

              <p className="mt-1 text-sm text-[#667085]">
                Common actions to manage BusinessPilot.
              </p>
            </div>

            <div className="mt-6 space-y-3">
              {quickActions.map((action) => {
                const Icon = action.icon;

                return (
                  <Link
                    key={action.title}
                    href={action.href}
                    className="group flex items-center gap-4 rounded-xl border border-[#edf0f4] p-4 transition hover:border-[#cfe0ff] hover:bg-[#f8fbff]"
                  >
                    <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-lg bg-[#eef5ff] text-[#126df5] transition group-hover:bg-[#126df5] group-hover:text-white">
                      <Icon size={21} />
                    </div>

                    <div className="min-w-0 flex-1">
                      <h3 className="text-sm font-semibold text-[#172033]">
                        {action.title}
                      </h3>

                      <p className="mt-1 text-xs leading-5 text-[#667085]">
                        {action.description}
                      </p>
                    </div>

                    <ArrowUpRight
                      size={17}
                      className="shrink-0 text-[#98a2b3] transition group-hover:text-[#126df5]"
                    />
                  </Link>
                );
              })}
            </div>
          </div>
        </div>

        {/* Bottom Section */}
        <div className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-2">

          {/* Recent Activity */}
          <div className="rounded-2xl border border-[#e5eaf1] bg-white p-6 shadow-sm">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-xl font-bold text-[#172033]">
                  Recent Activity
                </h2>

                <p className="mt-1 text-sm text-[#667085]">
                  Latest activity in your organization.
                </p>
              </div>

              <Activity
                size={22}
                className="text-[#126df5]"
              />
            </div>

            <div className="mt-6 rounded-xl border border-dashed border-[#dce2ea] bg-[#fafbfc] px-6 py-10 text-center">
              <Clock
                size={28}
                className="mx-auto text-[#98a2b3]"
              />

              <h3 className="mt-4 text-sm font-semibold text-[#344054]">
                No recent activity
              </h3>

              <p className="mt-1 text-sm text-[#98a2b3]">
                Activity will appear here when users start using the platform.
              </p>
            </div>
          </div>

          {/* Getting Started */}
          <div className="rounded-2xl border border-[#e5eaf1] bg-white p-6 shadow-sm">
            <div className="flex items-center gap-3">
              <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-[#eef5ff] text-[#126df5]">
                <FileText size={22} />
              </div>

              <div>
                <h2 className="text-xl font-bold text-[#172033]">
                  Getting Started
                </h2>

                <p className="mt-1 text-sm text-[#667085]">
                  Set up your BusinessPilot workspace.
                </p>
              </div>
            </div>

            <div className="mt-6 space-y-4">
              <div className="flex items-center gap-3 rounded-xl bg-[#fafbfc] p-4">
                <CheckCircle2
                  size={20}
                  className="text-[#98a2b3]"
                />

                <div>
                  <p className="text-sm font-semibold text-[#344054]">
                    Organization setup
                  </p>

                  <p className="mt-1 text-xs text-[#667085]">
                    Configure your organization information.
                  </p>
                </div>
              </div>

              <div className="flex items-center gap-3 rounded-xl bg-[#fafbfc] p-4">
                <CheckCircle2
                  size={20}
                  className="text-[#98a2b3]"
                />

                <div>
                  <p className="text-sm font-semibold text-[#344054]">
                    Invite your team
                  </p>

                  <p className="mt-1 text-xs text-[#667085]">
                    Add users who will work with your organization.
                  </p>
                </div>
              </div>

              <div className="flex items-center gap-3 rounded-xl bg-[#fafbfc] p-4">
                <CheckCircle2
                  size={20}
                  className="text-[#98a2b3]"
                />

                <div>
                  <p className="text-sm font-semibold text-[#344054]">
                    Create your first decision
                  </p>

                  <p className="mt-1 text-xs text-[#667085]">
                    Start analyzing a business decision with AI.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}