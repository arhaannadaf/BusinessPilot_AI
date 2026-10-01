"use client";

import { useState } from "react";
import {
  ShieldCheck,
  Lock,
  KeyRound,
  Smartphone,
  Monitor,
  CheckCircle2,
  XCircle,
  Clock3,
  MoreHorizontal,
} from "lucide-react";

type LoginActivity = {
  id: number;
  user: string;
  email: string;
  device: string;
  location: string;
  time: string;
  status: "Successful" | "Failed";
};

const loginActivity: LoginActivity[] = [
  {
    id: 1,
    user: "No login activity",
    email: "No authentication records yet",
    device: "—",
    location: "—",
    time: "—",
    status: "Successful",
  },
];

export default function AuthenticationPage() {
  const [activeTab, setActiveTab] = useState("Overview");

  const tabs = [
    "Overview",
    "Login Activity",
    "Authentication Methods",
    "Sessions",
  ];

  return (
    <div className="min-h-screen bg-[#f7f9fc] px-4 py-6 sm:px-6 lg:px-8">
      <div className="mx-auto w-full max-w-[1600px]">

        {/* Page Header */}
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-[#172033] sm:text-3xl">
            Authentication
          </h1>

          <p className="mt-1 text-sm text-[#667085] sm:text-base">
            Monitor authentication activity and manage account security.
          </p>
        </div>

        {/* Security Overview Cards */}
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 xl:grid-cols-4">

          {/* Authentication Status */}
          <div className="rounded-2xl border border-[#e5eaf1] bg-white p-5 shadow-sm">
            <div className="flex items-center justify-between">
              <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-[#e8f8ef] text-[#16834b]">
                <ShieldCheck size={22} />
              </div>

              <span className="rounded-full bg-[#e8f8ef] px-3 py-1 text-xs font-semibold text-[#16834b]">
                Secure
              </span>
            </div>

            <p className="mt-5 text-sm text-[#667085]">
              Authentication Status
            </p>

            <h2 className="mt-1 text-xl font-bold text-[#172033]">
              Protected
            </h2>
          </div>

          {/* Password */}
          <div className="rounded-2xl border border-[#e5eaf1] bg-white p-5 shadow-sm">
            <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-[#eef5ff] text-[#126df5]">
              <Lock size={22} />
            </div>

            <p className="mt-5 text-sm text-[#667085]">
              Password Authentication
            </p>

            <h2 className="mt-1 text-xl font-bold text-[#172033]">
              Enabled
            </h2>
          </div>

          {/* Two Factor */}
          <div className="rounded-2xl border border-[#e5eaf1] bg-white p-5 shadow-sm">
            <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-[#fff5dc] text-[#a56a00]">
              <Smartphone size={22} />
            </div>

            <p className="mt-5 text-sm text-[#667085]">
              Two-Factor Authentication
            </p>

            <h2 className="mt-1 text-xl font-bold text-[#172033]">
              Available
            </h2>
          </div>

          {/* Active Sessions */}
          <div className="rounded-2xl border border-[#e5eaf1] bg-white p-5 shadow-sm">
            <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-[#f1edff] text-[#6842d9]">
              <Monitor size={22} />
            </div>

            <p className="mt-5 text-sm text-[#667085]">
              Active Sessions
            </p>

            <h2 className="mt-1 text-xl font-bold text-[#172033]">
              0
            </h2>
          </div>
        </div>

        {/* Main Card */}
        <div className="mt-6 overflow-hidden rounded-2xl border border-[#e5eaf1] bg-white shadow-sm">

          {/* Tabs */}
          <div className="overflow-x-auto border-b border-[#edf0f4]">
            <div className="flex min-w-max px-4 sm:px-6">
              {tabs.map((tab) => {
                const isActive = activeTab === tab;

                return (
                  <button
                    key={tab}
                    onClick={() => setActiveTab(tab)}
                    className={`relative px-5 py-5 text-sm font-semibold transition ${
                      isActive
                        ? "text-[#126df5]"
                        : "text-[#667085] hover:text-[#344054]"
                    }`}
                  >
                    {tab}

                    {isActive && (
                      <span className="absolute bottom-0 left-0 h-0.5 w-full bg-[#126df5]" />
                    )}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Overview */}
          {activeTab === "Overview" && (
            <div className="p-5 sm:p-6">

              <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">

                {/* Security Settings */}
                <div className="rounded-xl border border-[#e5eaf1] p-5">
                  <div className="flex items-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-[#eef5ff] text-[#126df5]">
                      <KeyRound size={20} />
                    </div>

                    <div>
                      <h3 className="font-bold text-[#172033]">
                        Security Settings
                      </h3>

                      <p className="mt-1 text-xs text-[#667085]">
                        Authentication security configuration.
                      </p>
                    </div>
                  </div>

                  <div className="mt-5 space-y-3">

                    <SecurityRow
                      title="Password Authentication"
                      description="Users can sign in with email and password."
                      enabled
                    />

                    <SecurityRow
                      title="Two-Factor Authentication"
                      description="Additional verification for account security."
                      enabled={false}
                    />

                    <SecurityRow
                      title="Google Sign-In"
                      description="Allow users to authenticate using Google."
                      enabled={false}
                    />

                  </div>
                </div>

                {/* Authentication Information */}
                <div className="rounded-xl border border-[#e5eaf1] p-5">

                  <div className="flex items-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-[#eef5ff] text-[#126df5]">
                      <ShieldCheck size={20} />
                    </div>

                    <div>
                      <h3 className="font-bold text-[#172033]">
                        Authentication Protection
                      </h3>

                      <p className="mt-1 text-xs text-[#667085]">
                        Current account protection status.
                      </p>
                    </div>
                  </div>

                  <div className="mt-5 space-y-4">

                    <ProtectionRow
                      title="Secure Password Policy"
                      status="Configured"
                    />

                    <ProtectionRow
                      title="Session Protection"
                      status="Configured"
                    />

                    <ProtectionRow
                      title="Login Monitoring"
                      status="Available"
                    />

                    <ProtectionRow
                      title="Two-Factor Authentication"
                      status="Available"
                    />

                  </div>
                </div>
              </div>

            </div>
          )}

          {/* Login Activity */}
          {activeTab === "Login Activity" && (
            <div>

              <div className="border-b border-[#edf0f4] p-5 sm:p-6">
                <h2 className="text-lg font-bold text-[#172033]">
                  Login Activity
                </h2>

                <p className="mt-1 text-sm text-[#667085]">
                  Review successful and failed authentication attempts.
                </p>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full min-w-[900px]">

                  <thead>
                    <tr className="border-b border-[#edf0f4] bg-[#fafbfc] text-left">
                      <th className="px-6 py-4 text-xs font-semibold uppercase tracking-wide text-[#667085]">
                        User
                      </th>

                      <th className="px-6 py-4 text-xs font-semibold uppercase tracking-wide text-[#667085]">
                        Device
                      </th>

                      <th className="px-6 py-4 text-xs font-semibold uppercase tracking-wide text-[#667085]">
                        Location
                      </th>

                      <th className="px-6 py-4 text-xs font-semibold uppercase tracking-wide text-[#667085]">
                        Time
                      </th>

                      <th className="px-6 py-4 text-xs font-semibold uppercase tracking-wide text-[#667085]">
                        Status
                      </th>

                      <th className="px-6 py-4 text-right text-xs font-semibold uppercase tracking-wide text-[#667085]">
                        Actions
                      </th>
                    </tr>
                  </thead>

                  <tbody>
                    {loginActivity.map((activity) => (
                      <tr
                        key={activity.id}
                        className="border-b border-[#edf0f4]"
                      >
                        <td className="px-6 py-5">
                          <p className="text-sm font-semibold text-[#344054]">
                            {activity.user}
                          </p>

                          <p className="mt-1 text-xs text-[#98a2b3]">
                            {activity.email}
                          </p>
                        </td>

                        <td className="px-6 py-5 text-sm text-[#667085]">
                          {activity.device}
                        </td>

                        <td className="px-6 py-5 text-sm text-[#667085]">
                          {activity.location}
                        </td>

                        <td className="px-6 py-5 text-sm text-[#667085]">
                          {activity.time}
                        </td>

                        <td className="px-6 py-5">
                          <span className="inline-flex items-center gap-1.5 rounded-full bg-[#f2f4f7] px-3 py-1 text-xs font-semibold text-[#667085]">
                            <Clock3 size={13} />
                            No activity
                          </span>
                        </td>

                        <td className="px-6 py-5 text-right">
                          <button
                            disabled
                            className="inline-flex h-9 w-9 items-center justify-center rounded-lg text-[#98a2b3]"
                          >
                            <MoreHorizontal size={18} />
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>

                </table>
              </div>
            </div>
          )}

          {/* Authentication Methods */}
          {activeTab === "Authentication Methods" && (
            <div className="p-5 sm:p-6">

              <div className="grid grid-cols-1 gap-4 md:grid-cols-2">

                <AuthMethodCard
                  icon={<Lock size={22} />}
                  title="Email & Password"
                  description="Standard email and password authentication."
                  enabled
                />

                <AuthMethodCard
                  icon={<Smartphone size={22} />}
                  title="Two-Factor Authentication"
                  description="Use an additional verification step during login."
                  enabled={false}
                />

                <AuthMethodCard
                  icon={<ShieldCheck size={22} />}
                  title="Google Authentication"
                  description="Allow users to sign in using their Google account."
                  enabled={false}
                />

                <AuthMethodCard
                  icon={<KeyRound size={22} />}
                  title="Single Sign-On"
                  description="Enterprise authentication using an identity provider."
                  enabled={false}
                />

              </div>
            </div>
          )}

          {/* Sessions */}
          {activeTab === "Sessions" && (
            <div className="p-5 sm:p-6">

              <div className="flex min-h-[300px] flex-col items-center justify-center text-center">

                <div className="flex h-20 w-20 items-center justify-center rounded-full bg-[#eef5ff] text-[#126df5]">
                  <Monitor size={36} />
                </div>

                <h2 className="mt-6 text-xl font-bold text-[#172033]">
                  No Active Sessions
                </h2>

                <p className="mt-2 max-w-md text-sm leading-6 text-[#667085]">
                  Active user sessions will appear here after authentication
                  data is connected to the backend.
                </p>

              </div>
            </div>
          )}

        </div>
      </div>
    </div>
  );
}

/* =========================================
   SECURITY ROW
========================================= */

function SecurityRow({
  title,
  description,
  enabled,
}: {
  title: string;
  description: string;
  enabled: boolean;
}) {
  return (
    <div className="flex items-center justify-between gap-4 rounded-lg bg-[#f7f9fc] p-4">

      <div>
        <p className="text-sm font-semibold text-[#344054]">
          {title}
        </p>

        <p className="mt-1 text-xs leading-5 text-[#667085]">
          {description}
        </p>
      </div>

      <span
        className={`shrink-0 rounded-full px-3 py-1 text-xs font-semibold ${
          enabled
            ? "bg-[#e8f8ef] text-[#16834b]"
            : "bg-[#f2f4f7] text-[#667085]"
        }`}
      >
        {enabled ? "Enabled" : "Available"}
      </span>
    </div>
  );
}

/* =========================================
   PROTECTION ROW
========================================= */

function ProtectionRow({
  title,
  status,
}: {
  title: string;
  status: string;
}) {
  return (
    <div className="flex items-center justify-between border-b border-[#edf0f4] pb-3 last:border-0 last:pb-0">

      <div className="flex items-center gap-3">
        <CheckCircle2 size={18} className="text-[#16834b]" />

        <span className="text-sm font-medium text-[#344054]">
          {title}
        </span>
      </div>

      <span className="text-xs font-semibold text-[#667085]">
        {status}
      </span>
    </div>
  );
}

/* =========================================
   AUTHENTICATION METHOD CARD
========================================= */

function AuthMethodCard({
  icon,
  title,
  description,
  enabled,
}: {
  icon: React.ReactNode;
  title: string;
  description: string;
  enabled: boolean;
}) {
  return (
    <div className="rounded-xl border border-[#e5eaf1] p-5">

      <div className="flex items-start justify-between gap-4">

        <div className="flex items-center gap-3">

          <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-[#eef5ff] text-[#126df5]">
            {icon}
          </div>

          <div>
            <h3 className="font-bold text-[#172033]">
              {title}
            </h3>

            <p className="mt-1 text-xs leading-5 text-[#667085]">
              {description}
            </p>
          </div>

        </div>

        {enabled ? (
          <CheckCircle2
            size={20}
            className="shrink-0 text-[#16834b]"
          />
        ) : (
          <XCircle
            size={20}
            className="shrink-0 text-[#98a2b3]"
          />
        )}

      </div>

      <div className="mt-5">
        <span
          className={`rounded-full px-3 py-1 text-xs font-semibold ${
            enabled
              ? "bg-[#e8f8ef] text-[#16834b]"
              : "bg-[#f2f4f7] text-[#667085]"
          }`}
        >
          {enabled ? "Enabled" : "Not Configured"}
        </span>
      </div>
    </div>
  );
}