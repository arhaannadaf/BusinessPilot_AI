"use client";

import { useMemo, useState } from "react";
import {
  Search,
  Filter,
  FileText,
  UserPlus,
  ShieldCheck,
  Users,
  Settings,
  KeyRound,
  MoreHorizontal,
  X,
  Clock,
} from "lucide-react";

type AuditLog = {
  id: number;
  action: string;
  user: string;
  description: string;
  time: string;
  ipAddress: string;
  category: string;
  status: "Success" | "Failed";
};

const auditLogs: AuditLog[] = [
  {
    id: 1,
    action: "User Invited",
    user: "Administrator",
    description: "A new user invitation was created.",
    time: "—",
    ipAddress: "—",
    category: "Users",
    status: "Success",
  },
  {
    id: 2,
    action: "Role Updated",
    user: "Administrator",
    description: "A user role was updated.",
    time: "—",
    ipAddress: "—",
    category: "Roles",
    status: "Success",
  },
  {
    id: 3,
    action: "Team Created",
    user: "Administrator",
    description: "A new organization team was created.",
    time: "—",
    ipAddress: "—",
    category: "Teams",
    status: "Success",
  },
  {
    id: 4,
    action: "Password Changed",
    user: "Administrator",
    description: "An account password was changed.",
    time: "—",
    ipAddress: "—",
    category: "Security",
    status: "Success",
  },
];

const categories = [
  "All Categories",
  "Users",
  "Roles",
  "Teams",
  "Security",
  "Settings",
];

export default function AuditLogsPage() {
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("All Categories");
  const [selectedLog, setSelectedLog] = useState<AuditLog | null>(null);

  const filteredLogs = useMemo(() => {
    return auditLogs.filter((log) => {
      const matchesSearch =
        log.action.toLowerCase().includes(search.toLowerCase()) ||
        log.user.toLowerCase().includes(search.toLowerCase()) ||
        log.description.toLowerCase().includes(search.toLowerCase());

      const matchesCategory =
        category === "All Categories" ||
        log.category === category;

      return matchesSearch && matchesCategory;
    });
  }, [search, category]);

  return (
    <div className="min-h-screen bg-[#f7f9fc] px-4 py-6 sm:px-6 lg:px-8">
      <div className="mx-auto w-full max-w-[1600px]">

        {/* Page Header */}
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-[#172033] sm:text-3xl">
            Audit Logs
          </h1>

          <p className="mt-1 text-sm text-[#667085] sm:text-base">
            Track important activities and changes made within your organization.
          </p>
        </div>

        {/* Summary Cards */}
        <div className="mb-6 grid grid-cols-1 gap-5 sm:grid-cols-2 xl:grid-cols-4">

          <SummaryCard
            icon={<FileText size={22} />}
            title="Total Events"
            value={String(auditLogs.length)}
            description="Recorded events"
          />

          <SummaryCard
            icon={<UserPlus size={22} />}
            title="User Events"
            value={String(
              auditLogs.filter((log) => log.category === "Users").length
            )}
            description="User-related actions"
          />

          <SummaryCard
            icon={<ShieldCheck size={22} />}
            title="Security Events"
            value={String(
              auditLogs.filter((log) => log.category === "Security").length
            )}
            description="Security-related actions"
          />

          <SummaryCard
            icon={<Settings size={22} />}
            title="System Events"
            value={String(
              auditLogs.filter(
                (log) =>
                  log.category === "Settings" ||
                  log.category === "Roles" ||
                  log.category === "Teams"
              ).length
            )}
            description="Configuration changes"
          />
        </div>

        {/* Main Card */}
        <div className="overflow-hidden rounded-2xl border border-[#e5eaf1] bg-white shadow-sm">

          {/* Toolbar */}
          <div className="border-b border-[#edf0f4] p-5 sm:p-6">

            <div className="flex flex-col gap-4 xl:flex-row xl:items-center xl:justify-between">

              <div>
                <h2 className="text-lg font-bold text-[#172033]">
                  Activity History
                </h2>

                <p className="mt-1 text-sm text-[#667085]">
                  Review actions performed by users and administrators.
                </p>
              </div>

              <div className="flex w-full flex-col gap-3 sm:flex-row xl:w-auto">

                {/* Search */}
                <div className="relative flex-1 sm:min-w-[280px]">
                  <Search
                    size={18}
                    className="absolute left-3.5 top-1/2 -translate-y-1/2 text-[#98a2b3]"
                  />

                  <input
                    type="text"
                    placeholder="Search audit logs..."
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                    className="h-11 w-full rounded-lg border border-[#dce2ea] bg-white pl-10 pr-4 text-sm text-[#344054] outline-none transition placeholder:text-[#98a2b3] focus:border-[#126df5] focus:ring-2 focus:ring-[#126df5]/10"
                  />
                </div>

                {/* Category Filter */}
                <div className="relative">
                  <Filter
                    size={17}
                    className="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 text-[#667085]"
                  />

                  <select
                    value={category}
                    onChange={(e) => setCategory(e.target.value)}
                    className="h-11 w-full appearance-none rounded-lg border border-[#dce2ea] bg-white pl-10 pr-9 text-sm font-medium text-[#344054] outline-none focus:border-[#126df5] focus:ring-2 focus:ring-[#126df5]/10 sm:w-[190px]"
                  >
                    {categories.map((item) => (
                      <option key={item} value={item}>
                        {item}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
            </div>
          </div>

          {/* Table */}
          {filteredLogs.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="w-full min-w-[1000px]">

                <thead>
                  <tr className="border-b border-[#edf0f4] bg-[#fafbfc] text-left">

                    <th className="px-6 py-4 text-xs font-semibold uppercase tracking-wide text-[#667085]">
                      Action
                    </th>

                    <th className="px-6 py-4 text-xs font-semibold uppercase tracking-wide text-[#667085]">
                      User
                    </th>

                    <th className="px-6 py-4 text-xs font-semibold uppercase tracking-wide text-[#667085]">
                      Description
                    </th>

                    <th className="px-6 py-4 text-xs font-semibold uppercase tracking-wide text-[#667085]">
                      Time
                    </th>

                    <th className="px-6 py-4 text-xs font-semibold uppercase tracking-wide text-[#667085]">
                      IP Address
                    </th>

                    <th className="px-6 py-4 text-xs font-semibold uppercase tracking-wide text-[#667085]">
                      Status
                    </th>

                    <th className="px-6 py-4 text-right text-xs font-semibold uppercase tracking-wide text-[#667085]">
                      Details
                    </th>

                  </tr>
                </thead>

                <tbody>
                  {filteredLogs.map((log) => (
                    <tr
                      key={log.id}
                      className="border-b border-[#edf0f4] transition hover:bg-[#fafbfc]"
                    >

                      {/* Action */}
                      <td className="px-6 py-5">
                        <div className="flex items-center gap-3">

                          <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-[#eef5ff] text-[#126df5]">
                            {getActionIcon(log.category)}
                          </div>

                          <span className="text-sm font-semibold text-[#344054]">
                            {log.action}
                          </span>
                        </div>
                      </td>

                      {/* User */}
                      <td className="px-6 py-5">
                        <span className="text-sm font-medium text-[#344054]">
                          {log.user}
                        </span>
                      </td>

                      {/* Description */}
                      <td className="max-w-[300px] px-6 py-5">
                        <span className="text-sm text-[#667085]">
                          {log.description}
                        </span>
                      </td>

                      {/* Time */}
                      <td className="px-6 py-5">
                        <div className="flex items-center gap-2 text-sm text-[#667085]">
                          <Clock size={15} />
                          {log.time}
                        </div>
                      </td>

                      {/* IP */}
                      <td className="px-6 py-5">
                        <span className="font-mono text-sm text-[#667085]">
                          {log.ipAddress}
                        </span>
                      </td>

                      {/* Status */}
                      <td className="px-6 py-5">
                        <span
                          className={`inline-flex rounded-full px-3 py-1 text-xs font-semibold ${
                            log.status === "Success"
                              ? "bg-[#e8f8ef] text-[#16834b]"
                              : "bg-[#fdecec] text-[#c93636]"
                          }`}
                        >
                          {log.status}
                        </span>
                      </td>

                      {/* Details */}
                      <td className="px-6 py-5 text-right">
                        <button
                          onClick={() => setSelectedLog(log)}
                          className="inline-flex h-9 w-9 items-center justify-center rounded-lg text-[#667085] transition hover:bg-[#f2f4f7] hover:text-[#344054]"
                        >
                          <MoreHorizontal size={19} />
                        </button>
                      </td>

                    </tr>
                  ))}
                </tbody>

              </table>
            </div>
          ) : (
            <div className="flex min-h-[400px] flex-col items-center justify-center px-6 py-16 text-center">

              <div className="flex h-20 w-20 items-center justify-center rounded-full bg-[#eef5ff] text-[#126df5]">
                <FileText size={36} />
              </div>

              <h2 className="mt-6 text-xl font-bold text-[#172033]">
                No audit logs found
              </h2>

              <p className="mt-2 max-w-md text-sm leading-6 text-[#667085]">
                Try changing your search or category filter.
              </p>

            </div>
          )}

          {/* Footer */}
          <div className="flex flex-col gap-3 border-t border-[#edf0f4] px-5 py-5 sm:flex-row sm:items-center sm:justify-between sm:px-6">

            <p className="text-sm text-[#667085]">
              Showing {filteredLogs.length}{" "}
              {filteredLogs.length === 1 ? "event" : "events"}
            </p>

            <div className="flex gap-2">

              <button
                disabled
                className="rounded-lg border border-[#dce2ea] px-4 py-2 text-sm font-medium text-[#98a2b3] disabled:cursor-not-allowed"
              >
                Previous
              </button>

              <button
                disabled
                className="rounded-lg border border-[#dce2ea] px-4 py-2 text-sm font-medium text-[#98a2b3] disabled:cursor-not-allowed"
              >
                Next
              </button>

            </div>
          </div>
        </div>
      </div>

      {/* Details Modal */}
      {selectedLog && (
        <AuditLogDetails
          log={selectedLog}
          onClose={() => setSelectedLog(null)}
        />
      )}
    </div>
  );
}

/* =========================================
   SUMMARY CARD
========================================= */

function SummaryCard({
  icon,
  title,
  value,
  description,
}: {
  icon: React.ReactNode;
  title: string;
  value: string;
  description: string;
}) {
  return (
    <div className="rounded-2xl border border-[#e5eaf1] bg-white p-5 shadow-sm">

      <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-[#eef5ff] text-[#126df5]">
        {icon}
      </div>

      <p className="mt-5 text-sm text-[#667085]">
        {title}
      </p>

      <div className="mt-1 flex items-end gap-2">
        <h2 className="text-2xl font-bold text-[#172033]">
          {value}
        </h2>
      </div>

      <p className="mt-1 text-xs text-[#98a2b3]">
        {description}
      </p>
    </div>
  );
}

/* =========================================
   ACTION ICON
========================================= */

function getActionIcon(category: string) {
  switch (category) {
    case "Users":
      return <UserPlus size={18} />;

    case "Roles":
      return <ShieldCheck size={18} />;

    case "Teams":
      return <Users size={18} />;

    case "Security":
      return <KeyRound size={18} />;

    case "Settings":
      return <Settings size={18} />;

    default:
      return <FileText size={18} />;
  }
}

/* =========================================
   AUDIT LOG DETAILS
========================================= */

function AuditLogDetails({
  log,
  onClose,
}: {
  log: AuditLog;
  onClose: () => void;
}) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4">

      <div className="w-full max-w-lg rounded-2xl bg-white shadow-xl">

        {/* Header */}
        <div className="flex items-start justify-between border-b border-[#edf0f4] p-6">

          <div>
            <div className="flex items-center gap-3">

              <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-[#eef5ff] text-[#126df5]">
                {getActionIcon(log.category)}
              </div>

              <div>
                <h2 className="text-xl font-bold text-[#172033]">
                  {log.action}
                </h2>

                <p className="mt-1 text-sm text-[#667085]">
                  Audit event details
                </p>
              </div>

            </div>
          </div>

          <button
            onClick={onClose}
            className="flex h-9 w-9 items-center justify-center rounded-lg text-[#667085] hover:bg-[#f2f4f7]"
          >
            <X size={19} />
          </button>

        </div>

        {/* Content */}
        <div className="space-y-5 p-6">

          <DetailRow
            label="Performed By"
            value={log.user}
          />

          <DetailRow
            label="Description"
            value={log.description}
          />

          <DetailRow
            label="Category"
            value={log.category}
          />

          <DetailRow
            label="Time"
            value={log.time}
          />

          <DetailRow
            label="IP Address"
            value={log.ipAddress}
          />

          <div>
            <p className="text-xs font-semibold uppercase tracking-wide text-[#98a2b3]">
              Status
            </p>

            <span
              className={`mt-2 inline-flex rounded-full px-3 py-1 text-xs font-semibold ${
                log.status === "Success"
                  ? "bg-[#e8f8ef] text-[#16834b]"
                  : "bg-[#fdecec] text-[#c93636]"
              }`}
            >
              {log.status}
            </span>
          </div>

        </div>

        {/* Footer */}
        <div className="border-t border-[#edf0f4] p-6">
          <button
            onClick={onClose}
            className="w-full rounded-lg bg-[#126df5] px-5 py-3 text-sm font-semibold text-white transition hover:bg-[#0d5ed7]"
          >
            Close
          </button>
        </div>

      </div>
    </div>
  );
}

/* =========================================
   DETAIL ROW
========================================= */

function DetailRow({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div>
      <p className="text-xs font-semibold uppercase tracking-wide text-[#98a2b3]">
        {label}
      </p>

      <p className="mt-1 text-sm font-medium text-[#344054]">
        {value}
      </p>
    </div>
  );
}