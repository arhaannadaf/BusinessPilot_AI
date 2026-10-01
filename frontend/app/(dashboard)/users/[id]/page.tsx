"use client";

import Link from "next/link";
import {
  ArrowLeft,
  Mail,
  Phone,
  Building2,
  BriefcaseBusiness,
  ShieldCheck,
  CalendarDays,
  Clock3,
  MoreHorizontal,
  Pencil,
  UserRound,
  KeyRound,
  Activity,
} from "lucide-react";
import { useParams } from "next/navigation";

export default function UserProfilePage() {
  const params = useParams();
  const userId = params.id as string;

  return (
    <div className="min-h-screen bg-[#f7f9fc] px-4 py-6 sm:px-6 lg:px-8">
      <div className="mx-auto w-full max-w-[1500px]">

        {/* Back */}
        <Link
          href="/users"
          className="mb-6 inline-flex items-center gap-2 text-sm font-semibold text-[#667085] transition hover:text-[#126df5]"
        >
          <ArrowLeft size={18} />
          Back to Users
        </Link>

        {/* Profile Header */}
        <div className="overflow-hidden rounded-2xl border border-[#e5eaf1] bg-white shadow-sm">
          <div className="h-32 bg-gradient-to-r from-[#0f1d2e] to-[#126df5] sm:h-40" />

          <div className="px-5 pb-6 sm:px-8">
            <div className="-mt-12 flex flex-col gap-5 sm:-mt-14 sm:flex-row sm:items-end sm:justify-between">

              <div className="flex flex-col gap-4 sm:flex-row sm:items-end">
                <div className="flex h-24 w-24 items-center justify-center rounded-2xl border-4 border-white bg-[#eef5ff] text-[#126df5] shadow-md sm:h-28 sm:w-28">
                  <UserRound size={46} />
                </div>

                <div className="pb-1">
                  <div className="flex flex-wrap items-center gap-3">
                    <h1 className="text-2xl font-bold text-[#172033] sm:text-3xl">
                      User Profile
                    </h1>

                    <span className="rounded-full bg-[#f2f4f7] px-3 py-1 text-xs font-semibold text-[#667085]">
                      User ID: {userId}
                    </span>
                  </div>

                  <p className="mt-1 text-sm text-[#667085]">
                    User details and account information
                  </p>
                </div>
              </div>

              <div className="flex items-center gap-2">
                <button
                  onClick={() =>
                    alert("Edit user will be connected to the backend later.")
                  }
                  className="inline-flex items-center gap-2 rounded-lg border border-[#dce2ea] bg-white px-4 py-2.5 text-sm font-semibold text-[#344054] transition hover:bg-[#f7f9fc]"
                >
                  <Pencil size={17} />
                  Edit User
                </button>

                <button
                  onClick={() =>
                    alert("More user actions will be connected later.")
                  }
                  className="inline-flex h-10 w-10 items-center justify-center rounded-lg border border-[#dce2ea] text-[#667085] transition hover:bg-[#f7f9fc] hover:text-[#344054]"
                >
                  <MoreHorizontal size={19} />
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="mt-6 grid grid-cols-1 gap-6 xl:grid-cols-3">

          {/* Personal Information */}
          <div className="xl:col-span-2">
            <div className="rounded-2xl border border-[#e5eaf1] bg-white p-6 shadow-sm">
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-[#eef5ff] text-[#126df5]">
                  <UserRound size={20} />
                </div>

                <div>
                  <h2 className="text-lg font-bold text-[#172033]">
                    Personal Information
                  </h2>

                  <p className="mt-1 text-sm text-[#667085]">
                    Basic information about this user.
                  </p>
                </div>
              </div>

              <div className="mt-6 grid grid-cols-1 gap-5 sm:grid-cols-2">

                <InfoItem
                  icon={<Mail size={18} />}
                  label="Email Address"
                  value="Not available"
                />

                <InfoItem
                  icon={<Phone size={18} />}
                  label="Phone Number"
                  value="Not available"
                />

                <InfoItem
                  icon={<Building2 size={18} />}
                  label="Department"
                  value="Not available"
                />

                <InfoItem
                  icon={<BriefcaseBusiness size={18} />}
                  label="Job Title"
                  value="Not available"
                />
              </div>
            </div>

            {/* Account Information */}
            <div className="mt-6 rounded-2xl border border-[#e5eaf1] bg-white p-6 shadow-sm">
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-[#eef5ff] text-[#126df5]">
                  <ShieldCheck size={20} />
                </div>

                <div>
                  <h2 className="text-lg font-bold text-[#172033]">
                    Account Information
                  </h2>

                  <p className="mt-1 text-sm text-[#667085]">
                    Account status and access details.
                  </p>
                </div>
              </div>

              <div className="mt-6 grid grid-cols-1 gap-5 sm:grid-cols-2">

                <InfoItem
                  icon={<ShieldCheck size={18} />}
                  label="Role"
                  value="Not available"
                />

                <InfoItem
                  icon={<Activity size={18} />}
                  label="Account Status"
                  value="Not available"
                />

                <InfoItem
                  icon={<CalendarDays size={18} />}
                  label="Joined"
                  value="Not available"
                />

                <InfoItem
                  icon={<Clock3 size={18} />}
                  label="Last Active"
                  value="Not available"
                />
              </div>
            </div>

            {/* Permissions */}
            <div className="mt-6 rounded-2xl border border-[#e5eaf1] bg-white p-6 shadow-sm">
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-[#eef5ff] text-[#126df5]">
                  <KeyRound size={20} />
                </div>

                <div>
                  <h2 className="text-lg font-bold text-[#172033]">
                    Permissions
                  </h2>

                  <p className="mt-1 text-sm text-[#667085]">
                    Access permissions assigned to this user.
                  </p>
                </div>
              </div>

              <div className="mt-6 rounded-xl border border-dashed border-[#dce2ea] bg-[#fafbfc] px-6 py-10 text-center">
                <KeyRound
                  size={28}
                  className="mx-auto text-[#98a2b3]"
                />

                <h3 className="mt-4 text-sm font-semibold text-[#344054]">
                  Permissions not available
                </h3>

                <p className="mx-auto mt-1 max-w-md text-sm leading-6 text-[#98a2b3]">
                  Permissions will be loaded from the backend when this
                  user&apos;s role and access configuration are available.
                </p>
              </div>
            </div>
          </div>

          {/* Right Column */}
          <div>

            {/* User Status */}
            <div className="rounded-2xl border border-[#e5eaf1] bg-white p-6 shadow-sm">
              <h2 className="text-lg font-bold text-[#172033]">
                User Status
              </h2>

              <div className="mt-5 rounded-xl bg-[#fafbfc] p-5">
                <div className="flex items-center gap-3">
                  <span className="h-3 w-3 rounded-full bg-[#98a2b3]" />

                  <span className="text-sm font-semibold text-[#344054]">
                    Status unavailable
                  </span>
                </div>

                <p className="mt-3 text-sm leading-6 text-[#667085]">
                  The current status will be displayed after connecting this
                  page to the user API.
                </p>
              </div>
            </div>

            {/* Recent Activity */}
            <div className="mt-6 rounded-2xl border border-[#e5eaf1] bg-white p-6 shadow-sm">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-lg font-bold text-[#172033]">
                    Recent Activity
                  </h2>

                  <p className="mt-1 text-sm text-[#667085]">
                    Latest activity from this user.
                  </p>
                </div>

                <Activity
                  size={21}
                  className="text-[#126df5]"
                />
              </div>

              <div className="mt-6 rounded-xl border border-dashed border-[#dce2ea] bg-[#fafbfc] px-5 py-10 text-center">
                <Clock3
                  size={27}
                  className="mx-auto text-[#98a2b3]"
                />

                <h3 className="mt-4 text-sm font-semibold text-[#344054]">
                  No activity available
                </h3>

                <p className="mt-1 text-sm leading-6 text-[#98a2b3]">
                  User activity will appear here after the backend is
                  connected.
                </p>
              </div>
            </div>

            {/* Backend Note */}
            <div className="mt-6 rounded-2xl border border-[#cfe0ff] bg-[#f5f9ff] p-5">
              <div className="flex gap-3">
                <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-[#126df5] text-white">
                  <Activity size={18} />
                </div>

                <div>
                  <h3 className="text-sm font-bold text-[#172033]">
                    Backend Ready
                  </h3>

                  <p className="mt-1 text-sm leading-6 text-[#667085]">
                    This page uses the URL user ID and is ready to load real
                    user information from the backend API.
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

function InfoItem({
  icon,
  label,
  value,
}: {
  icon: React.ReactNode;
  label: string;
  value: string;
}) {
  return (
    <div className="rounded-xl border border-[#edf0f4] bg-[#fafbfc] p-4">
      <div className="flex items-center gap-3">
        <div className="text-[#126df5]">
          {icon}
        </div>

        <div className="min-w-0">
          <p className="text-xs font-semibold uppercase tracking-wide text-[#98a2b3]">
            {label}
          </p>

          <p className="mt-1 truncate text-sm font-semibold text-[#344054]">
            {value}
          </p>
        </div>
      </div>
    </div>
  );
}