"use client";

import {
  Building2,
  Plus,
  Search,
  MoreHorizontal,
  Users,
  Settings,
  ArrowUpRight,
  CheckCircle2,
} from "lucide-react";
import { useState } from "react";

type Organization = {
  id: string;
  name: string;
  description: string;
  members: number;
  status: "Active" | "Inactive";
};

const organizations: Organization[] = [];

export default function OrganizationsPage() {
  const [search, setSearch] = useState("");
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [organizationName, setOrganizationName] = useState("");
  const [organizationDescription, setOrganizationDescription] =
    useState("");
  const [created, setCreated] = useState(false);

  const filteredOrganizations = organizations.filter((organization) => {
    const value = search.toLowerCase();

    return (
      organization.name.toLowerCase().includes(value) ||
      organization.description.toLowerCase().includes(value)
    );
  });

  const handleCreateOrganization = () => {
    if (!organizationName.trim()) {
      alert("Please enter an organization name.");
      return;
    }

    setCreated(true);
  };

  const closeModal = () => {
    setShowCreateModal(false);
    setOrganizationName("");
    setOrganizationDescription("");
    setCreated(false);
  };

  return (
    <div className="min-h-screen bg-[#f7f9fc] px-4 py-6 sm:px-6 lg:px-8">
      <div className="mx-auto w-full max-w-[1600px]">

        {/* Page Header */}
        <div className="mb-8 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-[#172033] sm:text-4xl">
              Organizations
            </h1>

            <p className="mt-2 text-sm text-[#667085] sm:text-base">
              Manage organizations and their BusinessPilot workspaces.
            </p>
          </div>

          <button
            onClick={() => setShowCreateModal(true)}
            className="inline-flex w-fit items-center gap-2 rounded-lg bg-[#126df5] px-5 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-[#0d5ed7]"
          >
            <Plus size={18} />
            Create Organization
          </button>
        </div>

        {/* Overview Cards */}
        <div className="mb-6 grid grid-cols-1 gap-5 sm:grid-cols-3">
          <div className="rounded-2xl border border-[#e5eaf1] bg-white p-6 shadow-sm">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-[#667085]">
                  Total Organizations
                </p>

                <h2 className="mt-3 text-3xl font-bold text-[#172033]">
                  {organizations.length}
                </h2>
              </div>

              <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-[#eef5ff] text-[#126df5]">
                <Building2 size={24} />
              </div>
            </div>
          </div>

          <div className="rounded-2xl border border-[#e5eaf1] bg-white p-6 shadow-sm">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-[#667085]">
                  Active Organizations
                </p>

                <h2 className="mt-3 text-3xl font-bold text-[#172033]">
                  {organizations.filter(
                    (organization) => organization.status === "Active"
                  ).length}
                </h2>
              </div>

              <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-[#eaf8f0] text-[#16834b]">
                <CheckCircle2 size={24} />
              </div>
            </div>
          </div>

          <div className="rounded-2xl border border-[#e5eaf1] bg-white p-6 shadow-sm">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-[#667085]">
                  Total Members
                </p>

                <h2 className="mt-3 text-3xl font-bold text-[#172033]">
                  {organizations.reduce(
                    (total, organization) =>
                      total + organization.members,
                    0
                  )}
                </h2>
              </div>

              <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-[#f3edff] text-[#7a4dd8]">
                <Users size={24} />
              </div>
            </div>
          </div>
        </div>

        {/* Main Card */}
        <div className="overflow-hidden rounded-2xl border border-[#e5eaf1] bg-white shadow-sm">

          {/* Toolbar */}
          <div className="flex flex-col gap-4 border-b border-[#edf0f4] p-5 sm:p-6 lg:flex-row lg:items-center lg:justify-between">
            <div>
              <h2 className="text-xl font-bold text-[#172033]">
                Your Organizations
              </h2>

              <p className="mt-1 text-sm text-[#667085]">
                Organizations available in your BusinessPilot workspace.
              </p>
            </div>

            <div className="relative w-full lg:max-w-md">
              <Search
                size={19}
                className="absolute left-4 top-1/2 -translate-y-1/2 text-[#98a2b3]"
              />

              <input
                type="text"
                placeholder="Search organizations..."
                value={search}
                onChange={(event) => setSearch(event.target.value)}
                className="h-11 w-full rounded-lg border border-[#dce2ea] bg-white pl-11 pr-4 text-sm text-[#344054] outline-none transition placeholder:text-[#98a2b3] focus:border-[#126df5] focus:ring-2 focus:ring-[#126df5]/10"
              />
            </div>
          </div>

          {/* Organization List */}
          {filteredOrganizations.length > 0 ? (
            <div className="divide-y divide-[#edf0f4]">
              {filteredOrganizations.map((organization) => (
                <div
                  key={organization.id}
                  className="flex flex-col gap-5 p-6 transition hover:bg-[#fafbfc] lg:flex-row lg:items-center lg:justify-between"
                >
                  <div className="flex items-start gap-4">
                    <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-xl bg-[#eef5ff] text-[#126df5]">
                      <Building2 size={27} />
                    </div>

                    <div>
                      <h3 className="text-lg font-bold text-[#172033]">
                        {organization.name}
                      </h3>

                      <p className="mt-1 text-sm text-[#667085]">
                        {organization.description}
                      </p>

                      <div className="mt-3 flex flex-wrap items-center gap-3">
                        <span className="inline-flex items-center gap-1.5 text-sm text-[#667085]">
                          <Users size={15} />
                          {organization.members} members
                        </span>

                        <span
                          className={`inline-flex rounded-full px-3 py-1 text-xs font-semibold ${
                            organization.status === "Active"
                              ? "bg-[#e8f8ef] text-[#16834b]"
                              : "bg-[#fdecec] text-[#c93636]"
                          }`}
                        >
                          {organization.status}
                        </span>
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    <button
                      onClick={() =>
                        alert(
                          `Opening ${organization.name} settings.`
                        )
                      }
                      className="inline-flex h-10 items-center gap-2 rounded-lg border border-[#dce2ea] px-4 text-sm font-semibold text-[#344054] transition hover:bg-[#f7f9fc]"
                    >
                      <Settings size={16} />
                      Settings
                    </button>

                    <button
                      onClick={() =>
                        alert(
                          `Opening ${organization.name}.`
                        )
                      }
                      className="inline-flex h-10 items-center gap-2 rounded-lg bg-[#126df5] px-4 text-sm font-semibold text-white transition hover:bg-[#0d5ed7]"
                    >
                      Open
                      <ArrowUpRight size={16} />
                    </button>

                    <button
                      onClick={() =>
                        alert(
                          `More actions for ${organization.name}`
                        )
                      }
                      className="inline-flex h-10 w-10 items-center justify-center rounded-lg text-[#667085] transition hover:bg-[#f2f4f7] hover:text-[#344054]"
                    >
                      <MoreHorizontal size={19} />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            /* Empty State */
            <div className="flex min-h-[430px] flex-col items-center justify-center px-6 py-16 text-center">
              <div className="flex h-20 w-20 items-center justify-center rounded-full bg-[#eef5ff] text-[#126df5]">
                <Building2 size={36} />
              </div>

              <h2 className="mt-6 text-xl font-bold text-[#172033]">
                {search
                  ? "No organizations found"
                  : "No organizations yet"}
              </h2>

              <p className="mt-2 max-w-md text-sm leading-6 text-[#667085]">
                {search
                  ? "No organizations match your search. Try a different organization name."
                  : "Create your first organization to start managing users, teams, roles, and business decisions."}
              </p>

              {!search && (
                <button
                  onClick={() => setShowCreateModal(true)}
                  className="mt-6 inline-flex items-center gap-2 rounded-lg bg-[#126df5] px-5 py-3 text-sm font-semibold text-white transition hover:bg-[#0d5ed7]"
                >
                  <Plus size={18} />
                  Create Your First Organization
                </button>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Create Organization Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-[#172033]/50 px-4 py-6">
          <div className="w-full max-w-lg rounded-2xl bg-white shadow-2xl">

            {!created ? (
              <>
                {/* Modal Header */}
                <div className="border-b border-[#edf0f4] px-6 py-5">
                  <div className="flex items-center justify-between">
                    <div>
                      <h2 className="text-xl font-bold text-[#172033]">
                        Create Organization
                      </h2>

                      <p className="mt-1 text-sm text-[#667085]">
                        Set up a new BusinessPilot workspace.
                      </p>
                    </div>

                    <button
                      onClick={closeModal}
                      className="text-2xl text-[#98a2b3] hover:text-[#344054]"
                    >
                      ×
                    </button>
                  </div>
                </div>

                {/* Form */}
                <div className="space-y-5 p-6">
                  <div>
                    <label className="mb-2 block text-sm font-semibold text-[#344054]">
                      Organization Name
                    </label>

                    <input
                      type="text"
                      value={organizationName}
                      onChange={(event) =>
                        setOrganizationName(event.target.value)
                      }
                      placeholder="Enter organization name"
                      className="h-11 w-full rounded-lg border border-[#dce2ea] px-4 text-sm text-[#344054] outline-none placeholder:text-[#98a2b3] focus:border-[#126df5] focus:ring-2 focus:ring-[#126df5]/10"
                    />
                  </div>

                  <div>
                    <label className="mb-2 block text-sm font-semibold text-[#344054]">
                      Description
                    </label>

                    <textarea
                      value={organizationDescription}
                      onChange={(event) =>
                        setOrganizationDescription(
                          event.target.value
                        )
                      }
                      placeholder="Describe your organization"
                      rows={4}
                      className="w-full resize-none rounded-lg border border-[#dce2ea] px-4 py-3 text-sm text-[#344054] outline-none placeholder:text-[#98a2b3] focus:border-[#126df5] focus:ring-2 focus:ring-[#126df5]/10"
                    />
                  </div>

                  <div className="flex justify-end gap-3 pt-2">
                    <button
                      onClick={closeModal}
                      className="rounded-lg border border-[#dce2ea] px-5 py-2.5 text-sm font-semibold text-[#344054] transition hover:bg-[#f7f9fc]"
                    >
                      Cancel
                    </button>

                    <button
                      onClick={handleCreateOrganization}
                      className="rounded-lg bg-[#126df5] px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-[#0d5ed7]"
                    >
                      Create Organization
                    </button>
                  </div>
                </div>
              </>
            ) : (
              /* Success State */
              <div className="px-6 py-12 text-center">
                <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-[#e8f8ef] text-[#16834b]">
                  <CheckCircle2 size={32} />
                </div>

                <h2 className="mt-5 text-xl font-bold text-[#172033]">
                  Organization Ready
                </h2>

                <p className="mx-auto mt-2 max-w-md text-sm leading-6 text-[#667085]">
                  The organization form has been completed. The actual
                  organization will be created when the backend API is
                  connected.
                </p>

                <button
                  onClick={closeModal}
                  className="mt-6 rounded-lg bg-[#126df5] px-6 py-3 text-sm font-semibold text-white transition hover:bg-[#0d5ed7]"
                >
                  Done
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}