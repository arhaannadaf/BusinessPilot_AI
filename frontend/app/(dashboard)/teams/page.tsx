"use client";

import { useState } from "react";
import {
  Search,
  Plus,
  Users,
  MoreHorizontal,
  X,
  UserPlus,
  Edit3,
  Trash2,
} from "lucide-react";

type Team = {
  id: number;
  name: string;
  description: string;
  members: number;
  department: string;
};

const teams: Team[] = [
  {
    id: 1,
    name: "Sales Team",
    description: "Responsible for sales activities and customer relationships.",
    members: 0,
    department: "Sales",
  },
  {
    id: 2,
    name: "Marketing Team",
    description: "Manages marketing campaigns and brand activities.",
    members: 0,
    department: "Marketing",
  },
  {
    id: 3,
    name: "Finance Team",
    description: "Handles financial planning, reporting and analysis.",
    members: 0,
    department: "Finance",
  },
  {
    id: 4,
    name: "Technology Team",
    description: "Responsible for technology and product development.",
    members: 0,
    department: "Technology",
  },
];

export default function TeamsPage() {
  const [search, setSearch] = useState("");
  const [selectedTeam, setSelectedTeam] = useState<Team | null>(null);
  const [showCreateTeam, setShowCreateTeam] = useState(false);

  const filteredTeams = teams.filter(
    (team) =>
      team.name.toLowerCase().includes(search.toLowerCase()) ||
      team.department.toLowerCase().includes(search.toLowerCase()) ||
      team.description.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-[#f7f9fc] px-4 py-6 sm:px-6 lg:px-8">
      <div className="mx-auto w-full max-w-[1600px]">

        {/* Page Header */}
        <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h1 className="text-2xl font-bold text-[#172033] sm:text-3xl">
              Teams
            </h1>

            <p className="mt-1 text-sm text-[#667085] sm:text-base">
              Organize users into teams and manage team access.
            </p>
          </div>

          <button
            onClick={() => setShowCreateTeam(true)}
            className="inline-flex w-fit items-center gap-2 rounded-lg bg-[#126df5] px-5 py-3 text-sm font-semibold text-white transition hover:bg-[#0d5ed7]"
          >
            <Plus size={18} />
            Create Team
          </button>
        </div>

        {/* Main Card */}
        <div className="rounded-2xl border border-[#e5eaf1] bg-white shadow-sm">

          {/* Toolbar */}
          <div className="flex flex-col gap-4 border-b border-[#edf0f4] p-5 sm:p-6 lg:flex-row lg:items-center lg:justify-between">

            <div>
              <h2 className="text-lg font-bold text-[#172033]">
                Organization Teams
              </h2>

              <p className="mt-1 text-sm text-[#667085]">
                Create and manage teams within your organization.
              </p>
            </div>

            <div className="relative w-full lg:max-w-sm">
              <Search
                size={18}
                className="absolute left-3.5 top-1/2 -translate-y-1/2 text-[#98a2b3]"
              />

              <input
                type="text"
                placeholder="Search teams..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="h-11 w-full rounded-lg border border-[#dce2ea] bg-white pl-10 pr-4 text-sm text-[#344054] outline-none transition placeholder:text-[#98a2b3] focus:border-[#126df5] focus:ring-2 focus:ring-[#126df5]/10"
              />
            </div>
          </div>

          {/* Team Cards */}
          {filteredTeams.length > 0 ? (
            <div className="grid grid-cols-1 gap-5 p-5 sm:p-6 lg:grid-cols-2 xl:grid-cols-3">

              {filteredTeams.map((team) => (
                <div
                  key={team.id}
                  className="rounded-xl border border-[#e5eaf1] bg-white p-5 transition hover:border-[#cbd8ed] hover:shadow-sm"
                >

                  {/* Team Header */}
                  <div className="flex items-start justify-between gap-4">

                    <div className="flex items-center gap-3">
                      <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-[#eef5ff] text-[#126df5]">
                        <Users size={22} />
                      </div>

                      <div>
                        <h3 className="font-bold text-[#172033]">
                          {team.name}
                        </h3>

                        <p className="mt-1 text-xs text-[#667085]">
                          {team.department}
                        </p>
                      </div>
                    </div>

                    <button
                      onClick={() => setSelectedTeam(team)}
                      className="flex h-9 w-9 items-center justify-center rounded-lg text-[#667085] transition hover:bg-[#f2f4f7] hover:text-[#344054]"
                    >
                      <MoreHorizontal size={18} />
                    </button>
                  </div>

                  {/* Description */}
                  <p className="mt-5 min-h-[48px] text-sm leading-6 text-[#667085]">
                    {team.description}
                  </p>

                  {/* Members */}
                  <div className="mt-5 flex items-center justify-between border-t border-[#edf0f4] pt-4">
                    <div className="flex items-center gap-2 text-sm text-[#667085]">
                      <Users size={17} />
                      <span>
                        {team.members}{" "}
                        {team.members === 1 ? "member" : "members"}
                      </span>
                    </div>

                    <button
                      onClick={() => setSelectedTeam(team)}
                      className="text-sm font-semibold text-[#126df5] hover:text-[#0d5ed7]"
                    >
                      View Team
                    </button>
                  </div>
                </div>
              ))}

            </div>
          ) : (
            <div className="flex min-h-[400px] flex-col items-center justify-center px-6 py-16 text-center">

              <div className="flex h-20 w-20 items-center justify-center rounded-full bg-[#eef5ff] text-[#126df5]">
                <Users size={36} />
              </div>

              <h2 className="mt-6 text-xl font-bold text-[#172033]">
                No teams found
              </h2>

              <p className="mt-2 max-w-md text-sm leading-6 text-[#667085]">
                No teams match your search. Try searching for another team.
              </p>
            </div>
          )}

          {/* Footer */}
          <div className="border-t border-[#edf0f4] px-5 py-5 sm:px-6">
            <p className="text-sm text-[#667085]">
              {filteredTeams.length}{" "}
              {filteredTeams.length === 1 ? "team" : "teams"} available
            </p>
          </div>
        </div>
      </div>

      {/* Team Details Modal */}
      {selectedTeam && (
        <TeamDetailsModal
          team={selectedTeam}
          onClose={() => setSelectedTeam(null)}
        />
      )}

      {/* Create Team Modal */}
      {showCreateTeam && (
        <CreateTeamModal
          onClose={() => setShowCreateTeam(false)}
        />
      )}
    </div>
  );
}

/* =========================================
   TEAM DETAILS MODAL
========================================= */

function TeamDetailsModal({
  team,
  onClose,
}: {
  team: Team;
  onClose: () => void;
}) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4">
      <div className="w-full max-w-lg rounded-2xl bg-white shadow-xl">

        {/* Header */}
        <div className="flex items-start justify-between border-b border-[#edf0f4] p-6">

          <div className="flex items-center gap-3">
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-[#eef5ff] text-[#126df5]">
              <Users size={23} />
            </div>

            <div>
              <h2 className="text-xl font-bold text-[#172033]">
                {team.name}
              </h2>

              <p className="mt-1 text-sm text-[#667085]">
                {team.department}
              </p>
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
        <div className="space-y-6 p-6">

          <div>
            <p className="text-xs font-semibold uppercase tracking-wide text-[#98a2b3]">
              Description
            </p>

            <p className="mt-2 text-sm leading-6 text-[#667085]">
              {team.description}
            </p>
          </div>

          <div>
            <p className="text-xs font-semibold uppercase tracking-wide text-[#98a2b3]">
              Team Members
            </p>

            <div className="mt-3 flex items-center gap-3 rounded-lg bg-[#f7f9fc] p-4">
              <Users size={20} className="text-[#126df5]" />

              <span className="text-sm font-semibold text-[#344054]">
                {team.members}{" "}
                {team.members === 1 ? "member" : "members"}
              </span>
            </div>
          </div>

          {/* Actions */}
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">

            <button
              onClick={() =>
                alert("Add member functionality will be connected later.")
              }
              className="inline-flex items-center justify-center gap-2 rounded-lg border border-[#dce2ea] px-4 py-3 text-sm font-semibold text-[#344054] hover:bg-[#f7f9fc]"
            >
              <UserPlus size={17} />
              Add Member
            </button>

            <button
              onClick={() =>
                alert("Edit team functionality will be connected later.")
              }
              className="inline-flex items-center justify-center gap-2 rounded-lg border border-[#dce2ea] px-4 py-3 text-sm font-semibold text-[#344054] hover:bg-[#f7f9fc]"
            >
              <Edit3 size={17} />
              Edit
            </button>

            <button
              onClick={() =>
                alert("Delete team functionality will be connected later.")
              }
              className="inline-flex items-center justify-center gap-2 rounded-lg border border-[#f0caca] px-4 py-3 text-sm font-semibold text-[#c93636] hover:bg-[#fff5f5]"
            >
              <Trash2 size={17} />
              Delete
            </button>

          </div>
        </div>

        {/* Footer */}
        <div className="border-t border-[#edf0f4] p-6">
          <button
            onClick={onClose}
            className="w-full rounded-lg bg-[#126df5] px-5 py-3 text-sm font-semibold text-white hover:bg-[#0d5ed7]"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}

/* =========================================
   CREATE TEAM MODAL
========================================= */

function CreateTeamModal({
  onClose,
}: {
  onClose: () => void;
}) {
  const [teamName, setTeamName] = useState("");
  const [department, setDepartment] = useState("");
  const [description, setDescription] = useState("");

  const handleCreate = () => {
    if (!teamName.trim()) {
      alert("Please enter a team name.");
      return;
    }

    if (!department) {
      alert("Please select a department.");
      return;
    }

    alert("Team creation will be connected to the backend later.");

    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4">
      <div className="w-full max-w-lg rounded-2xl bg-white shadow-xl">

        {/* Header */}
        <div className="flex items-center justify-between border-b border-[#edf0f4] p-6">

          <div>
            <h2 className="text-xl font-bold text-[#172033]">
              Create New Team
            </h2>

            <p className="mt-1 text-sm text-[#667085]">
              Create a team and organize your users.
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

          {/* Team Name */}
          <div>
            <label className="mb-2 block text-sm font-semibold text-[#344054]">
              Team Name
            </label>

            <input
              type="text"
              value={teamName}
              onChange={(e) => setTeamName(e.target.value)}
              placeholder="e.g. Product Team"
              className="h-11 w-full rounded-lg border border-[#dce2ea] px-4 text-sm text-[#344054] outline-none placeholder:text-[#98a2b3] focus:border-[#126df5] focus:ring-2 focus:ring-[#126df5]/10"
            />
          </div>

          {/* Department */}
          <div>
            <label className="mb-2 block text-sm font-semibold text-[#344054]">
              Department
            </label>

            <select
              value={department}
              onChange={(e) => setDepartment(e.target.value)}
              className="h-11 w-full rounded-lg border border-[#dce2ea] bg-white px-4 text-sm text-[#344054] outline-none focus:border-[#126df5] focus:ring-2 focus:ring-[#126df5]/10"
            >
              <option value="">Select department</option>
              <option value="Management">Management</option>
              <option value="Sales">Sales</option>
              <option value="Marketing">Marketing</option>
              <option value="Finance">Finance</option>
              <option value="Human Resources">Human Resources</option>
              <option value="Operations">Operations</option>
              <option value="Technology">Technology</option>
            </select>
          </div>

          {/* Description */}
          <div>
            <label className="mb-2 block text-sm font-semibold text-[#344054]">
              Description
            </label>

            <textarea
              rows={4}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Describe the purpose of this team..."
              className="w-full resize-none rounded-lg border border-[#dce2ea] px-4 py-3 text-sm text-[#344054] outline-none placeholder:text-[#98a2b3] focus:border-[#126df5] focus:ring-2 focus:ring-[#126df5]/10"
            />
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
            Create Team
          </button>

        </div>
      </div>
    </div>
  );
}