"use client";

import { FormEvent, useState } from "react";
import Link from "next/link";
import {
  ArrowLeft,
  UserPlus,
  Mail,
  Phone,
  Building2,
  Briefcase,
  ShieldCheck,
  CheckCircle2,
} from "lucide-react";

export default function InviteUserPage() {
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [department, setDepartment] = useState("");
  const [jobTitle, setJobTitle] = useState("");
  const [role, setRole] = useState("");
  const [sendEmail, setSendEmail] = useState(true);

  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    // Backend API will be connected here later.
    setSubmitted(true);
  };

  if (submitted) {
    return (
      <div className="min-h-screen bg-[#f7f9fc] px-4 py-8 sm:px-6 lg:px-8">
        <div className="mx-auto flex min-h-[80vh] w-full max-w-[700px] items-center justify-center">
          <div className="w-full rounded-2xl border border-[#e5eaf1] bg-white p-8 text-center shadow-sm sm:p-12">
            <div className="mx-auto flex h-20 w-20 items-center justify-center rounded-full bg-[#e8f8ef] text-[#16834b]">
              <CheckCircle2 size={42} />
            </div>

            <h1 className="mt-6 text-2xl font-bold text-[#172033]">
              Invitation Ready
            </h1>

            <p className="mx-auto mt-3 max-w-md text-sm leading-6 text-[#667085]">
              The user invitation has been prepared successfully. The backend
              will send the invitation when the API is connected.
            </p>

            <div className="mt-6 rounded-xl bg-[#f7f9fc] p-4 text-left">
              <p className="text-xs font-semibold uppercase tracking-wide text-[#98a2b3]">
                User
              </p>

              <p className="mt-1 text-sm font-semibold text-[#344054]">
                {fullName}
              </p>

              <p className="mt-1 text-sm text-[#667085]">
                {email}
              </p>
            </div>

            <div className="mt-8 flex flex-col gap-3 sm:flex-row sm:justify-center">
              <Link
                href="/users"
                className="inline-flex items-center justify-center gap-2 rounded-lg bg-[#126df5] px-5 py-3 text-sm font-semibold text-white transition hover:bg-[#0d5ed7]"
              >
                <ArrowLeft size={17} />
                Back to Users
              </Link>

              <button
                onClick={() => setSubmitted(false)}
                className="rounded-lg border border-[#dce2ea] bg-white px-5 py-3 text-sm font-semibold text-[#344054] transition hover:bg-[#f7f9fc]"
              >
                Invite Another User
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#f7f9fc] px-4 py-6 sm:px-6 lg:px-8">
      <div className="mx-auto w-full max-w-[1100px]">

        {/* Back */}
        <Link
          href="/users"
          className="mb-5 inline-flex items-center gap-2 text-sm font-medium text-[#667085] transition hover:text-[#126df5]"
        >
          <ArrowLeft size={18} />
          Back to Users
        </Link>

        {/* Header */}
        <div className="mb-6">
          <div className="flex items-center gap-3">
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-[#eef5ff] text-[#126df5]">
              <UserPlus size={24} />
            </div>

            <div>
              <h1 className="text-2xl font-bold text-[#172033] sm:text-3xl">
                Invite User
              </h1>

              <p className="mt-1 text-sm text-[#667085]">
                Add a new user to your BusinessPilot organization.
              </p>
            </div>
          </div>
        </div>

        {/* Form Card */}
        <form onSubmit={handleSubmit}>
          <div className="rounded-2xl border border-[#e5eaf1] bg-white shadow-sm">

            {/* Personal Information */}
            <div className="border-b border-[#edf0f4] px-6 py-6 sm:px-8">
              <h2 className="text-lg font-bold text-[#172033]">
                Personal Information
              </h2>

              <p className="mt-1 text-sm text-[#667085]">
                Enter the basic information of the person you want to invite.
              </p>

              <div className="mt-6 grid grid-cols-1 gap-6 sm:grid-cols-2">

                {/* Full Name */}
                <div>
                  <label
                    htmlFor="fullName"
                    className="mb-2 block text-sm font-semibold text-[#344054]"
                  >
                    Full Name
                  </label>

                  <div className="relative">
                    <UserPlus
                      size={18}
                      className="absolute left-3.5 top-1/2 -translate-y-1/2 text-[#98a2b3]"
                    />

                    <input
                      id="fullName"
                      type="text"
                      required
                      value={fullName}
                      onChange={(e) => setFullName(e.target.value)}
                      placeholder="Enter full name"
                      className="h-11 w-full rounded-lg border border-[#dce2ea] bg-white pl-11 pr-4 text-sm text-[#344054] outline-none transition placeholder:text-[#98a2b3] focus:border-[#126df5] focus:ring-2 focus:ring-[#126df5]/10"
                    />
                  </div>
                </div>

                {/* Email */}
                <div>
                  <label
                    htmlFor="email"
                    className="mb-2 block text-sm font-semibold text-[#344054]"
                  >
                    Email Address
                  </label>

                  <div className="relative">
                    <Mail
                      size={18}
                      className="absolute left-3.5 top-1/2 -translate-y-1/2 text-[#98a2b3]"
                    />

                    <input
                      id="email"
                      type="email"
                      required
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      placeholder="name@example.com"
                      className="h-11 w-full rounded-lg border border-[#dce2ea] bg-white pl-11 pr-4 text-sm text-[#344054] outline-none transition placeholder:text-[#98a2b3] focus:border-[#126df5] focus:ring-2 focus:ring-[#126df5]/10"
                    />
                  </div>
                </div>

                {/* Phone */}
                <div>
                  <label
                    htmlFor="phone"
                    className="mb-2 block text-sm font-semibold text-[#344054]"
                  >
                    Phone Number
                  </label>

                  <div className="relative">
                    <Phone
                      size={18}
                      className="absolute left-3.5 top-1/2 -translate-y-1/2 text-[#98a2b3]"
                    />

                    <input
                      id="phone"
                      type="tel"
                      value={phone}
                      onChange={(e) => setPhone(e.target.value)}
                      placeholder="+91 98765 43210"
                      className="h-11 w-full rounded-lg border border-[#dce2ea] bg-white pl-11 pr-4 text-sm text-[#344054] outline-none transition placeholder:text-[#98a2b3] focus:border-[#126df5] focus:ring-2 focus:ring-[#126df5]/10"
                    />
                  </div>
                </div>

                {/* Department */}
                <div>
                  <label
                    htmlFor="department"
                    className="mb-2 block text-sm font-semibold text-[#344054]"
                  >
                    Department
                  </label>

                  <div className="relative">
                    <Building2
                      size={18}
                      className="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 text-[#98a2b3]"
                    />

                    <select
                      id="department"
                      required
                      value={department}
                      onChange={(e) => setDepartment(e.target.value)}
                      className="h-11 w-full appearance-none rounded-lg border border-[#dce2ea] bg-white pl-11 pr-4 text-sm text-[#344054] outline-none transition focus:border-[#126df5] focus:ring-2 focus:ring-[#126df5]/10"
                    >
                      <option value="">Select department</option>
                      <option value="Management">Management</option>
                      <option value="Finance">Finance</option>
                      <option value="Marketing">Marketing</option>
                      <option value="Sales">Sales</option>
                      <option value="Human Resources">Human Resources</option>
                      <option value="Operations">Operations</option>
                      <option value="Technology">Technology</option>
                    </select>
                  </div>
                </div>

                {/* Job Title */}
                <div>
                  <label
                    htmlFor="jobTitle"
                    className="mb-2 block text-sm font-semibold text-[#344054]"
                  >
                    Job Title
                  </label>

                  <div className="relative">
                    <Briefcase
                      size={18}
                      className="absolute left-3.5 top-1/2 -translate-y-1/2 text-[#98a2b3]"
                    />

                    <input
                      id="jobTitle"
                      type="text"
                      value={jobTitle}
                      onChange={(e) => setJobTitle(e.target.value)}
                      placeholder="e.g. Business Analyst"
                      className="h-11 w-full rounded-lg border border-[#dce2ea] bg-white pl-11 pr-4 text-sm text-[#344054] outline-none transition placeholder:text-[#98a2b3] focus:border-[#126df5] focus:ring-2 focus:ring-[#126df5]/10"
                    />
                  </div>
                </div>

                {/* Role */}
                <div>
                  <label
                    htmlFor="role"
                    className="mb-2 block text-sm font-semibold text-[#344054]"
                  >
                    Role
                  </label>

                  <div className="relative">
                    <ShieldCheck
                      size={18}
                      className="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 text-[#98a2b3]"
                    />

                    <select
                      id="role"
                      required
                      value={role}
                      onChange={(e) => setRole(e.target.value)}
                      className="h-11 w-full appearance-none rounded-lg border border-[#dce2ea] bg-white pl-11 pr-4 text-sm text-[#344054] outline-none transition focus:border-[#126df5] focus:ring-2 focus:ring-[#126df5]/10"
                    >
                      <option value="">Select role</option>
                      <option value="Administrator">Administrator</option>
                      <option value="Manager">Manager</option>
                      <option value="Business Analyst">
                        Business Analyst
                      </option>
                      <option value="Viewer">Viewer</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>

            {/* Invitation Settings */}
            <div className="px-6 py-6 sm:px-8">
              <h2 className="text-lg font-bold text-[#172033]">
                Invitation Settings
              </h2>

              <p className="mt-1 text-sm text-[#667085]">
                Choose how the user should receive their invitation.
              </p>

              <label className="mt-6 flex cursor-pointer items-start gap-3 rounded-xl border border-[#e5eaf1] bg-[#fafbfc] p-4 transition hover:bg-[#f7f9fc]">
                <input
                  type="checkbox"
                  checked={sendEmail}
                  onChange={(e) => setSendEmail(e.target.checked)}
                  className="mt-0.5 h-4 w-4 rounded border-[#cbd5e1] text-[#126df5] focus:ring-[#126df5]"
                />

                <span>
                  <span className="block text-sm font-semibold text-[#344054]">
                    Send invitation email
                  </span>

                  <span className="mt-1 block text-xs leading-5 text-[#667085]">
                    The user will receive an email with instructions to access
                    BusinessPilot.
                  </span>
                </span>
              </label>
            </div>

            {/* Buttons */}
            <div className="flex flex-col-reverse gap-3 border-t border-[#edf0f4] px-6 py-5 sm:flex-row sm:justify-end sm:px-8">
              <Link
                href="/users"
                className="inline-flex h-11 items-center justify-center rounded-lg border border-[#dce2ea] bg-white px-5 text-sm font-semibold text-[#344054] transition hover:bg-[#f7f9fc]"
              >
                Cancel
              </Link>

              <button
                type="submit"
                className="inline-flex h-11 items-center justify-center gap-2 rounded-lg bg-[#126df5] px-5 text-sm font-semibold text-white transition hover:bg-[#0d5ed7]"
              >
                <UserPlus size={17} />
                Send Invitation
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}