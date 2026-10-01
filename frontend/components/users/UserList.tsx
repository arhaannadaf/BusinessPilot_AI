"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import {
  Search,
  SlidersHorizontal,
  UserPlus,
  Users,
  MoreHorizontal,
} from "lucide-react";

type UserStatus = "Active" | "Inactive" | "Pending";

type User = {
  id: string;
  name: string;
  email: string;
  role: string;
  status: UserStatus;
  lastActive: string;
};

const users: User[] = [];

const tabs = [
  "All Users",
  "Active",
  "Inactive",
  "Pending",
  "Invited",
];

export default function UserList() {
  const [activeTab, setActiveTab] = useState("All Users");
  const [search, setSearch] = useState("");

  const filteredUsers = useMemo(() => {
    let result = users;

    if (activeTab !== "All Users" && activeTab !== "Invited") {
      result = result.filter((user) => user.status === activeTab);
    }

    if (search.trim()) {
      const searchValue = search.toLowerCase();

      result = result.filter(
        (user) =>
          user.name.toLowerCase().includes(searchValue) ||
          user.email.toLowerCase().includes(searchValue) ||
          user.role.toLowerCase().includes(searchValue)
      );
    }

    return result;
  }, [activeTab, search]);

  return (
    <div className="min-h-screen bg-[#f7f9fc] px-4 py-6 sm:px-6 lg:px-8">
      <div className="mx-auto w-full max-w-[1600px]">

        {/* Page Header */}
        <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h1 className="text-2xl font-bold text-[#172033] sm:text-3xl">
              Users
            </h1>

            <p className="mt-1 text-sm text-[#667085] sm:text-base">
              Manage users and their access to BusinessPilot.
            </p>
          </div>

          <Link
            href="/users/invite"
            className="inline-flex w-fit items-center justify-center gap-2 rounded-lg bg-[#126df5] px-5 py-3 text-sm font-semibold text-white transition hover:bg-[#0d5ed7]"
          >
            <UserPlus size={18} />
            Invite User
          </Link>
        </div>

        {/* Main Card */}
        <div className="overflow-hidden rounded-2xl border border-[#e5eaf1] bg-white shadow-sm">

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

          {/* Toolbar */}
          <div className="flex flex-col gap-4 border-b border-[#edf0f4] p-5 sm:p-6 lg:flex-row lg:items-center lg:justify-between">

            {/* Search */}
            <div className="relative w-full lg:max-w-md">
              <Search
                size={19}
                className="absolute left-4 top-1/2 -translate-y-1/2 text-[#98a2b3]"
              />

              <input
                type="text"
                placeholder="Search users..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="h-11 w-full rounded-lg border border-[#dce2ea] bg-white pl-11 pr-4 text-sm text-[#344054] outline-none transition placeholder:text-[#98a2b3] focus:border-[#126df5] focus:ring-2 focus:ring-[#126df5]/10"
              />
            </div>

            {/* Actions */}
            <div className="flex w-full gap-3 sm:w-auto">
              <button
                onClick={() =>
                  alert("Advanced filters will be connected later.")
                }
                className="inline-flex h-11 flex-1 items-center justify-center gap-2 rounded-lg border border-[#dce2ea] bg-white px-4 text-sm font-semibold text-[#344054] transition hover:bg-[#f7f9fc] sm:flex-none"
              >
                <SlidersHorizontal size={17} />
                Filter
              </button>

              <Link
                href="/users/invite"
                className="inline-flex h-11 flex-1 items-center justify-center gap-2 rounded-lg bg-[#126df5] px-4 text-sm font-semibold text-white transition hover:bg-[#0d5ed7] sm:flex-none"
              >
                <UserPlus size={17} />
                Invite User
              </Link>
            </div>
          </div>

          {/* User Table */}
          {filteredUsers.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="w-full min-w-[900px]">
                <thead>
                  <tr className="border-b border-[#edf0f4] bg-[#fafbfc] text-left">
                    <th className="px-6 py-4 text-xs font-semibold uppercase tracking-wide text-[#667085]">
                      Name
                    </th>

                    <th className="px-6 py-4 text-xs font-semibold uppercase tracking-wide text-[#667085]">
                      Email
                    </th>

                    <th className="px-6 py-4 text-xs font-semibold uppercase tracking-wide text-[#667085]">
                      Role
                    </th>

                    <th className="px-6 py-4 text-xs font-semibold uppercase tracking-wide text-[#667085]">
                      Status
                    </th>

                    <th className="px-6 py-4 text-xs font-semibold uppercase tracking-wide text-[#667085]">
                      Last Active
                    </th>

                    <th className="px-6 py-4 text-right text-xs font-semibold uppercase tracking-wide text-[#667085]">
                      Actions
                    </th>
                  </tr>
                </thead>

                <tbody>
                  {filteredUsers.map((user) => (
                    <tr
                      key={user.id}
                      className="border-b border-[#edf0f4] transition hover:bg-[#fafbfc]"
                    >
                      <td className="px-6 py-5">
                        <Link
                          href={`/users/${user.id}`}
                          className="font-semibold text-[#172033] hover:text-[#126df5]"
                        >
                          {user.name}
                        </Link>
                      </td>

                      <td className="px-6 py-5 text-sm text-[#667085]">
                        {user.email}
                      </td>

                      <td className="px-6 py-5 text-sm font-medium text-[#344054]">
                        {user.role}
                      </td>

                      <td className="px-6 py-5">
                        <span
                          className={`inline-flex rounded-full px-3 py-1 text-xs font-semibold ${
                            user.status === "Active"
                              ? "bg-[#e8f8ef] text-[#16834b]"
                              : user.status === "Inactive"
                              ? "bg-[#fdecec] text-[#c93636]"
                              : "bg-[#fff5dc] text-[#a56a00]"
                          }`}
                        >
                          {user.status}
                        </span>
                      </td>

                      <td className="px-6 py-5 text-sm text-[#667085]">
                        {user.lastActive}
                      </td>

                      <td className="px-6 py-5 text-right">
                        <button
                          onClick={() =>
                            alert(`Actions for ${user.name}`)
                          }
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
            /* Empty State */
            <div className="flex min-h-[420px] flex-col items-center justify-center px-6 py-16 text-center">

              <div className="flex h-20 w-20 items-center justify-center rounded-full bg-[#eef5ff] text-[#126df5]">
                <Users size={36} />
              </div>

              <h2 className="mt-6 text-xl font-bold text-[#172033]">
                No users found
              </h2>

              <p className="mt-2 max-w-md text-sm leading-6 text-[#667085]">
                {search
                  ? "No users match your search. Try a different name, email, or role."
                  : "There are currently no users in your organization. Invite your first user to get started."}
              </p>

              {!search && (
                <Link
                  href="/users/invite"
                  className="mt-6 inline-flex items-center gap-2 rounded-lg bg-[#126df5] px-5 py-3 text-sm font-semibold text-white transition hover:bg-[#0d5ed7]"
                >
                  <UserPlus size={18} />
                  Invite Your First User
                </Link>
              )}
            </div>
          )}

          {/* Pagination */}
          <div className="flex flex-col gap-3 border-t border-[#edf0f4] px-5 py-5 sm:flex-row sm:items-center sm:justify-between sm:px-6">
            <p className="text-sm text-[#667085]">
              {filteredUsers.length === 0
                ? "Showing 0 users"
                : `Showing ${filteredUsers.length} users`}
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
    </div>
  );
}