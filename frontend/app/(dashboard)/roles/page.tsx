"use client";

import { useState } from "react";
import {
  Search,
  Plus,
  ShieldCheck,
  Users,
  MoreHorizontal,
  X,
  Check,
} from "lucide-react";

type Role = {
  id: number;
  name: string;
  description: string;
  users: number;
  permissions: string[];
};

const roles: Role[] = [
  {
    id: 1,
    name: "Administrator",
    description: "Full access to BusinessPilot and organization settings.",
    users: 0,
    permissions: [
      "Manage Users",
      "Manage Roles",
      "Manage Organizations",
      "View Analytics",
      "Manage Teams",
      "View Audit Logs",
      "Manage Settings",
    ],
  },
  {
    id: 2,
    name: "Manager",
    description: "Manage teams, users and business information.",
    users: 0,
    permissions: [
      "Manage Users",
      "View Analytics",
      "Manage Teams",
      "View Audit Logs",
    ],
  },
  {
    id: 3,
    name: "Business Analyst",
    description: "Analyze business data and generate insights.",
    users: 0,
    permissions: [
      "View Analytics",
      "Create Scenarios",
      "View Business Data",
    ],
  },
  {
    id: 4,
    name: "Viewer",
    description: "Read-only access to available business information.",
    users: 0,
    permissions: [
      "View Analytics",
      "View Business Data",
    ],
  },
];

const allPermissions = [
  "Manage Users",
  "Manage Roles",
  "Manage Organizations",
  "View Analytics",
  "Manage Teams",
  "View Audit Logs",
  "Manage Settings",
  "Create Scenarios",
  "View Business Data",
];

export default function RolesPage() {
  const [search, setSearch] = useState("");
  const [selectedRole, setSelectedRole] = useState<Role | null>(null);
  const [showCreateRole, setShowCreateRole] = useState(false);

  const filteredRoles = roles.filter(
    (role) =>
      role.name.toLowerCase().includes(search.toLowerCase()) ||
      role.description.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-[#f7f9fc] px-4 py-6 sm:px-6 lg:px-8">
      <div className="mx-auto w-full max-w-[1600px]">

        {/* Page Header */}
        <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h1 className="text-2xl font-bold text-[#172033] sm:text-3xl">
              Roles & Permissions
            </h1>

            <p className="mt-1 text-sm text-[#667085] sm:text-base">
              Manage roles and control what users can access.
            </p>
          </div>

          <button
            onClick={() => setShowCreateRole(true)}
            className="inline-flex w-fit items-center gap-2 rounded-lg bg-[#126df5] px-5 py-3 text-sm font-semibold text-white transition hover:bg-[#0d5ed7]"
          >
            <Plus size={18} />
            Create Role
          </button>
        </div>

        {/* Main Card */}
        <div className="rounded-2xl border border-[#e5eaf1] bg-white shadow-sm">

          {/* Toolbar */}
          <div className="flex flex-col gap-4 border-b border-[#edf0f4] p-5 sm:p-6 lg:flex-row lg:items-center lg:justify-between">
            <div>
              <h2 className="text-lg font-bold text-[#172033]">
                Organization Roles
              </h2>

              <p className="mt-1 text-sm text-[#667085]">
                Roles determine the permissions available to each user.
              </p>
            </div>

            <div className="relative w-full lg:max-w-sm">
              <Search
                size={18}
                className="absolute left-3.5 top-1/2 -translate-y-1/2 text-[#98a2b3]"
              />

              <input
                type="text"
                placeholder="Search roles..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="h-11 w-full rounded-lg border border-[#dce2ea] bg-white pl-10 pr-4 text-sm text-[#344054] outline-none transition placeholder:text-[#98a2b3] focus:border-[#126df5] focus:ring-2 focus:ring-[#126df5]/10"
              />
            </div>
          </div>

          {/* Roles */}
          <div className="grid grid-cols-1 gap-5 p-5 sm:p-6 lg:grid-cols-2 xl:grid-cols-3">

            {filteredRoles.map((role) => (
              <div
                key={role.id}
                className="rounded-xl border border-[#e5eaf1] bg-white p-5 transition hover:border-[#cbd8ed] hover:shadow-sm"
              >
                {/* Role Header */}
                <div className="flex items-start justify-between gap-4">

                  <div className="flex items-center gap-3">
                    <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-[#eef5ff] text-[#126df5]">
                      <ShieldCheck size={22} />
                    </div>

                    <div>
                      <h3 className="font-bold text-[#172033]">
                        {role.name}
                      </h3>

                      <div className="mt-1 flex items-center gap-1.5 text-xs text-[#667085]">
                        <Users size={14} />
                        {role.users} users
                      </div>
                    </div>
                  </div>

                  <button
                    onClick={() => setSelectedRole(role)}
                    className="flex h-9 w-9 items-center justify-center rounded-lg text-[#667085] transition hover:bg-[#f2f4f7] hover:text-[#344054]"
                  >
                    <MoreHorizontal size={18} />
                  </button>
                </div>

                {/* Description */}
                <p className="mt-5 min-h-[48px] text-sm leading-6 text-[#667085]">
                  {role.description}
                </p>

                {/* Permissions */}
                <div className="mt-5">
                  <p className="text-xs font-semibold uppercase tracking-wide text-[#98a2b3]">
                    Permissions
                  </p>

                  <div className="mt-3 flex flex-wrap gap-2">
                    {role.permissions.slice(0, 3).map((permission) => (
                      <span
                        key={permission}
                        className="rounded-full bg-[#f2f6fc] px-3 py-1.5 text-xs font-medium text-[#475467]"
                      >
                        {permission}
                      </span>
                    ))}

                    {role.permissions.length > 3 && (
                      <span className="rounded-full bg-[#f2f6fc] px-3 py-1.5 text-xs font-medium text-[#667085]">
                        +{role.permissions.length - 3} more
                      </span>
                    )}
                  </div>
                </div>

                {/* View Permissions */}
                <button
                  onClick={() => setSelectedRole(role)}
                  className="mt-5 w-full rounded-lg border border-[#dce2ea] px-4 py-2.5 text-sm font-semibold text-[#344054] transition hover:bg-[#f7f9fc]"
                >
                  View Permissions
                </button>
              </div>
            ))}

          </div>

          {/* Empty Search State */}
          {filteredRoles.length === 0 && (
            <div className="px-6 py-16 text-center">
              <ShieldCheck
                size={42}
                className="mx-auto text-[#98a2b3]"
              />

              <h3 className="mt-4 text-lg font-bold text-[#172033]">
                No roles found
              </h3>

              <p className="mt-2 text-sm text-[#667085]">
                Try searching with a different role name.
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Role Details Modal */}
      {selectedRole && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4">
          <div className="max-h-[90vh] w-full max-w-lg overflow-y-auto rounded-2xl bg-white shadow-xl">

            {/* Modal Header */}
            <div className="flex items-start justify-between border-b border-[#edf0f4] p-6">
              <div className="flex items-center gap-3">
                <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-[#eef5ff] text-[#126df5]">
                  <ShieldCheck size={22} />
                </div>

                <div>
                  <h2 className="text-lg font-bold text-[#172033]">
                    {selectedRole.name}
                  </h2>

                  <p className="mt-1 text-sm text-[#667085]">
                    {selectedRole.users} users assigned
                  </p>
                </div>
              </div>

              <button
                onClick={() => setSelectedRole(null)}
                className="flex h-9 w-9 items-center justify-center rounded-lg text-[#667085] hover:bg-[#f2f4f7]"
              >
                <X size={19} />
              </button>
            </div>

            {/* Permissions */}
            <div className="p-6">
              <p className="text-sm font-semibold text-[#344054]">
                Available Permissions
              </p>

              <div className="mt-4 space-y-2">
                {allPermissions.map((permission) => {
                  const hasPermission =
                    selectedRole.permissions.includes(permission);

                  return (
                    <div
                      key={permission}
                      className={`flex items-center justify-between rounded-lg px-4 py-3 ${
                        hasPermission
                          ? "bg-[#f2faf5]"
                          : "bg-[#f7f9fc]"
                      }`}
                    >
                      <span className="text-sm font-medium text-[#344054]">
                        {permission}
                      </span>

                      {hasPermission && (
                        <Check
                          size={18}
                          className="text-[#16834b]"
                        />
                      )}
                    </div>
                  );
                })}
              </div>

              <button
                onClick={() =>
                  alert(
                    "Role editing will be connected to the backend later."
                  )
                }
                className="mt-6 w-full rounded-lg bg-[#126df5] px-5 py-3 text-sm font-semibold text-white transition hover:bg-[#0d5ed7]"
              >
                Edit Role
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Create Role Modal */}
      {showCreateRole && (
        <CreateRoleModal
          onClose={() => setShowCreateRole(false)}
        />
      )}
    </div>
  );
}

/* ------------------------------------------
   CREATE ROLE MODAL
------------------------------------------ */

function CreateRoleModal({
  onClose,
}: {
  onClose: () => void;
}) {
  const [roleName, setRoleName] = useState("");
  const [description, setDescription] = useState("");

  const [selectedPermissions, setSelectedPermissions] = useState<string[]>(
    []
  );

  const togglePermission = (permission: string) => {
    setSelectedPermissions((current) =>
      current.includes(permission)
        ? current.filter((item) => item !== permission)
        : [...current, permission]
    );
  };

  const handleCreate = () => {
    if (!roleName.trim()) {
      alert("Please enter a role name.");
      return;
    }

    alert(
      "Role creation will be connected to the backend later."
    );

    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4">
      <div className="max-h-[90vh] w-full max-w-xl overflow-y-auto rounded-2xl bg-white shadow-xl">

        {/* Header */}
        <div className="flex items-center justify-between border-b border-[#edf0f4] p-6">
          <div>
            <h2 className="text-xl font-bold text-[#172033]">
              Create New Role
            </h2>

            <p className="mt-1 text-sm text-[#667085]">
              Create a custom role with specific permissions.
            </p>
          </div>

          <button
            onClick={onClose}
            className="flex h-9 w-9 items-center justify-center rounded-lg text-[#667085] hover:bg-[#f2f4f7]"
          >
            <X size={19} />
          </button>
        </div>

        {/* Form */}
        <div className="space-y-5 p-6">

          {/* Role Name */}
          <div>
            <label className="mb-2 block text-sm font-semibold text-[#344054]">
              Role Name
            </label>

            <input
              type="text"
              value={roleName}
              onChange={(e) => setRoleName(e.target.value)}
              placeholder="e.g. Sales Manager"
              className="h-11 w-full rounded-lg border border-[#dce2ea] px-4 text-sm text-[#344054] outline-none placeholder:text-[#98a2b3] focus:border-[#126df5] focus:ring-2 focus:ring-[#126df5]/10"
            />
          </div>

          {/* Description */}
          <div>
            <label className="mb-2 block text-sm font-semibold text-[#344054]">
              Description
            </label>

            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Describe what this role is used for..."
              rows={3}
              className="w-full resize-none rounded-lg border border-[#dce2ea] px-4 py-3 text-sm text-[#344054] outline-none placeholder:text-[#98a2b3] focus:border-[#126df5] focus:ring-2 focus:ring-[#126df5]/10"
            />
          </div>

          {/* Permissions */}
          <div>
            <label className="mb-3 block text-sm font-semibold text-[#344054]">
              Permissions
            </label>

            <div className="space-y-2">
              {allPermissions.map((permission) => {
                const selected = selectedPermissions.includes(permission);

                return (
                  <label
                    key={permission}
                    className={`flex cursor-pointer items-center gap-3 rounded-lg border p-3 transition ${
                      selected
                        ? "border-[#126df5] bg-[#eef5ff]"
                        : "border-[#e5eaf1] hover:bg-[#f7f9fc]"
                    }`}
                  >
                    <input
                      type="checkbox"
                      checked={selected}
                      onChange={() => togglePermission(permission)}
                      className="h-4 w-4 rounded border-[#cbd5e1] text-[#126df5] focus:ring-[#126df5]"
                    />

                    <span className="text-sm font-medium text-[#344054]">
                      {permission}
                    </span>
                  </label>
                );
              })}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="flex flex-col-reverse gap-3 border-t border-[#edf0f4] p-6 sm:flex-row sm:justify-end">
          <button
            onClick={onClose}
            className="rounded-lg border border-[#dce2ea] px-5 py-3 text-sm font-semibold text-[#344054] hover:bg-[#f7f9fc]"
          >
            Cancel
          </button>

          <button
            onClick={handleCreate}
            className="rounded-lg bg-[#126df5] px-5 py-3 text-sm font-semibold text-white hover:bg-[#0d5ed7]"
          >
            Create Role
          </button>
        </div>
      </div>
    </div>
  );
}