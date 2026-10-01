"use client";

import { useState } from "react";
import {
  Building2,
  ShieldCheck,
  Bell,
  User,
  Save,
  Lock,
  Mail,
  AlertTriangle,
  CheckCircle2,
} from "lucide-react";

const settingsTabs = [
  {
    id: "general",
    label: "General",
    icon: Building2,
  },
  {
    id: "security",
    label: "Security",
    icon: ShieldCheck,
  },
  {
    id: "notifications",
    label: "Notifications",
    icon: Bell,
  },
  {
    id: "profile",
    label: "Profile",
    icon: User,
  },
];

export default function SettingsPage() {
  const [activeTab, setActiveTab] = useState("general");

  const [organizationName, setOrganizationName] =
    useState("BusinessPilot Organization");

  const [organizationEmail, setOrganizationEmail] =
    useState("admin@businesspilot.ai");

  const [timezone, setTimezone] =
    useState("Asia/Kolkata");

  const [language, setLanguage] =
    useState("English");

  const [emailNotifications, setEmailNotifications] =
    useState(true);

  const [securityAlerts, setSecurityAlerts] =
    useState(true);

  const [productUpdates, setProductUpdates] =
    useState(false);

  const [saved, setSaved] = useState(false);

  const handleSave = () => {
    // Backend API will be connected here later.
    setSaved(true);

    setTimeout(() => {
      setSaved(false);
    }, 3000);
  };

  return (
    <div className="min-h-screen bg-[#f7f9fc] px-4 py-6 sm:px-6 lg:px-8">
      <div className="mx-auto w-full max-w-[1500px]">

        {/* Header */}
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-[#172033] sm:text-3xl">
            Settings
          </h1>

          <p className="mt-1 text-sm text-[#667085] sm:text-base">
            Manage your organization, security and account preferences.
          </p>
        </div>

        {/* Main Layout */}
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-[250px_minmax(0,1fr)]">

          {/* Sidebar */}
          <div className="h-fit rounded-2xl border border-[#e5eaf1] bg-white p-3 shadow-sm">

            {settingsTabs.map((tab) => {
              const Icon = tab.icon;
              const active = activeTab === tab.id;

              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`mb-1 flex w-full items-center gap-3 rounded-lg px-4 py-3 text-left text-sm font-semibold transition ${
                    active
                      ? "bg-[#eef5ff] text-[#126df5]"
                      : "text-[#667085] hover:bg-[#f7f9fc] hover:text-[#344054]"
                  }`}
                >
                  <Icon size={18} />
                  {tab.label}
                </button>
              );
            })}

          </div>

          {/* Content */}
          <div className="min-w-0">

            {/* =====================================
                GENERAL
            ====================================== */}
            {activeTab === "general" && (
              <div className="rounded-2xl border border-[#e5eaf1] bg-white shadow-sm">

                <div className="border-b border-[#edf0f4] px-6 py-6 sm:px-8">
                  <h2 className="text-lg font-bold text-[#172033]">
                    General Settings
                  </h2>

                  <p className="mt-1 text-sm text-[#667085]">
                    Manage basic information about your organization.
                  </p>
                </div>

                <div className="space-y-6 p-6 sm:p-8">

                  {/* Organization Name */}
                  <div>
                    <label
                      htmlFor="organizationName"
                      className="mb-2 block text-sm font-semibold text-[#344054]"
                    >
                      Organization Name
                    </label>

                    <div className="relative">
                      <Building2
                        size={18}
                        className="absolute left-3.5 top-1/2 -translate-y-1/2 text-[#98a2b3]"
                      />

                      <input
                        id="organizationName"
                        type="text"
                        value={organizationName}
                        onChange={(e) =>
                          setOrganizationName(e.target.value)
                        }
                        className="h-11 w-full rounded-lg border border-[#dce2ea] pl-11 pr-4 text-sm text-[#344054] outline-none transition focus:border-[#126df5] focus:ring-2 focus:ring-[#126df5]/10"
                      />
                    </div>
                  </div>

                  {/* Organization Email */}
                  <div>
                    <label
                      htmlFor="organizationEmail"
                      className="mb-2 block text-sm font-semibold text-[#344054]"
                    >
                      Organization Email
                    </label>

                    <div className="relative">
                      <Mail
                        size={18}
                        className="absolute left-3.5 top-1/2 -translate-y-1/2 text-[#98a2b3]"
                      />

                      <input
                        id="organizationEmail"
                        type="email"
                        value={organizationEmail}
                        onChange={(e) =>
                          setOrganizationEmail(e.target.value)
                        }
                        className="h-11 w-full rounded-lg border border-[#dce2ea] pl-11 pr-4 text-sm text-[#344054] outline-none transition focus:border-[#126df5] focus:ring-2 focus:ring-[#126df5]/10"
                      />
                    </div>
                  </div>

                  {/* Timezone and Language */}
                  <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">

                    <div>
                      <label
                        htmlFor="timezone"
                        className="mb-2 block text-sm font-semibold text-[#344054]"
                      >
                        Timezone
                      </label>

                      <select
                        id="timezone"
                        value={timezone}
                        onChange={(e) =>
                          setTimezone(e.target.value)
                        }
                        className="h-11 w-full rounded-lg border border-[#dce2ea] bg-white px-4 text-sm text-[#344054] outline-none focus:border-[#126df5] focus:ring-2 focus:ring-[#126df5]/10"
                      >
                        <option value="Asia/Kolkata">
                          India Standard Time
                        </option>

                        <option value="UTC">
                          UTC
                        </option>

                        <option value="America/New_York">
                          Eastern Time
                        </option>

                        <option value="America/Los_Angeles">
                          Pacific Time
                        </option>

                        <option value="Europe/London">
                          London
                        </option>
                      </select>
                    </div>

                    <div>
                      <label
                        htmlFor="language"
                        className="mb-2 block text-sm font-semibold text-[#344054]"
                      >
                        Language
                      </label>

                      <select
                        id="language"
                        value={language}
                        onChange={(e) =>
                          setLanguage(e.target.value)
                        }
                        className="h-11 w-full rounded-lg border border-[#dce2ea] bg-white px-4 text-sm text-[#344054] outline-none focus:border-[#126df5] focus:ring-2 focus:ring-[#126df5]/10"
                      >
                        <option value="English">
                          English
                        </option>

                        <option value="Hindi">
                          Hindi
                        </option>
                      </select>
                    </div>

                  </div>

                </div>

                <SaveButton
                  saved={saved}
                  onClick={handleSave}
                />

              </div>
            )}

            {/* =====================================
                SECURITY
            ====================================== */}
            {activeTab === "security" && (
              <div className="space-y-6">

                <div className="rounded-2xl border border-[#e5eaf1] bg-white shadow-sm">

                  <div className="border-b border-[#edf0f4] px-6 py-6 sm:px-8">
                    <h2 className="text-lg font-bold text-[#172033]">
                      Security Settings
                    </h2>

                    <p className="mt-1 text-sm text-[#667085]">
                      Manage authentication and account security.
                    </p>
                  </div>

                  <div className="divide-y divide-[#edf0f4]">

                    <SecuritySetting
                      icon={<Lock size={19} />}
                      title="Password Policy"
                      description="Configure password requirements for organization users."
                      button="Configure"
                    />

                    <SecuritySetting
                      icon={<ShieldCheck size={19} />}
                      title="Two-Factor Authentication"
                      description="Require users to verify their identity with an additional security step."
                      button="Configure"
                    />

                    <SecuritySetting
                      icon={<User size={19} />}
                      title="Session Management"
                      description="Manage active sessions and session expiration settings."
                      button="Manage"
                    />

                  </div>
                </div>

                {/* Change Password */}
                <div className="rounded-2xl border border-[#e5eaf1] bg-white shadow-sm">

                  <div className="border-b border-[#edf0f4] px-6 py-6 sm:px-8">
                    <h2 className="text-lg font-bold text-[#172033]">
                      Change Password
                    </h2>

                    <p className="mt-1 text-sm text-[#667085]">
                      Update your account password.
                    </p>
                  </div>

                  <div className="grid grid-cols-1 gap-5 p-6 sm:grid-cols-2 sm:p-8">

                    <PasswordField
                      label="Current Password"
                    />

                    <PasswordField
                      label="New Password"
                    />

                    <PasswordField
                      label="Confirm New Password"
                    />

                  </div>

                  <div className="flex justify-end border-t border-[#edf0f4] px-6 py-5 sm:px-8">
                    <button
                      onClick={() =>
                        alert(
                          "Password change will be connected to the backend later."
                        )
                      }
                      className="rounded-lg bg-[#126df5] px-5 py-3 text-sm font-semibold text-white transition hover:bg-[#0d5ed7]"
                    >
                      Update Password
                    </button>
                  </div>

                </div>

              </div>
            )}

            {/* =====================================
                NOTIFICATIONS
            ====================================== */}
            {activeTab === "notifications" && (
              <div className="rounded-2xl border border-[#e5eaf1] bg-white shadow-sm">

                <div className="border-b border-[#edf0f4] px-6 py-6 sm:px-8">
                  <h2 className="text-lg font-bold text-[#172033]">
                    Notification Settings
                  </h2>

                  <p className="mt-1 text-sm text-[#667085]">
                    Choose which notifications you want to receive.
                  </p>
                </div>

                <div className="divide-y divide-[#edf0f4]">

                  <NotificationSetting
                    title="Email Notifications"
                    description="Receive important organization updates by email."
                    enabled={emailNotifications}
                    onChange={setEmailNotifications}
                  />

                  <NotificationSetting
                    title="Security Alerts"
                    description="Receive notifications about security-related events."
                    enabled={securityAlerts}
                    onChange={setSecurityAlerts}
                  />

                  <NotificationSetting
                    title="Product Updates"
                    description="Receive information about new BusinessPilot features."
                    enabled={productUpdates}
                    onChange={setProductUpdates}
                  />

                </div>

                <SaveButton
                  saved={saved}
                  onClick={handleSave}
                />

              </div>
            )}

            {/* =====================================
                PROFILE
            ====================================== */}
            {activeTab === "profile" && (
              <div className="rounded-2xl border border-[#e5eaf1] bg-white shadow-sm">

                <div className="border-b border-[#edf0f4] px-6 py-6 sm:px-8">
                  <h2 className="text-lg font-bold text-[#172033]">
                    Profile Settings
                  </h2>

                  <p className="mt-1 text-sm text-[#667085]">
                    Manage your personal account information.
                  </p>
                </div>

                <div className="p-6 sm:p-8">

                  <div className="flex flex-col items-start gap-5 sm:flex-row sm:items-center">

                    <div className="flex h-20 w-20 items-center justify-center rounded-full bg-[#126df5] text-2xl font-bold text-white">
                      JD
                    </div>

                    <div>
                      <h3 className="text-xl font-bold text-[#172033]">
                        John Doe
                      </h3>

                      <p className="mt-1 text-sm text-[#667085]">
                        Administrator
                      </p>

                      <p className="mt-1 text-sm text-[#667085]">
                        admin@businesspilot.ai
                      </p>
                    </div>

                  </div>

                  <div className="mt-8 grid grid-cols-1 gap-6 sm:grid-cols-2">

                    <div>
                      <label className="mb-2 block text-sm font-semibold text-[#344054]">
                        First Name
                      </label>

                      <input
                        type="text"
                        defaultValue="John"
                        className="h-11 w-full rounded-lg border border-[#dce2ea] px-4 text-sm text-[#344054] outline-none focus:border-[#126df5] focus:ring-2 focus:ring-[#126df5]/10"
                      />
                    </div>

                    <div>
                      <label className="mb-2 block text-sm font-semibold text-[#344054]">
                        Last Name
                      </label>

                      <input
                        type="text"
                        defaultValue="Doe"
                        className="h-11 w-full rounded-lg border border-[#dce2ea] px-4 text-sm text-[#344054] outline-none focus:border-[#126df5] focus:ring-2 focus:ring-[#126df5]/10"
                      />
                    </div>

                    <div className="sm:col-span-2">
                      <label className="mb-2 block text-sm font-semibold text-[#344054]">
                        Email Address
                      </label>

                      <input
                        type="email"
                        defaultValue="admin@businesspilot.ai"
                        className="h-11 w-full rounded-lg border border-[#dce2ea] px-4 text-sm text-[#344054] outline-none focus:border-[#126df5] focus:ring-2 focus:ring-[#126df5]/10"
                      />
                    </div>

                  </div>

                </div>

                <SaveButton
                  saved={saved}
                  onClick={handleSave}
                />

              </div>
            )}

            {/* Danger Zone */}
            <div className="mt-6 rounded-2xl border border-[#f0caca] bg-white shadow-sm">

              <div className="p-6 sm:p-8">

                <div className="flex items-start gap-4">

                  <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-[#fff5f5] text-[#c93636]">
                    <AlertTriangle size={21} />
                  </div>

                  <div>
                    <h2 className="text-lg font-bold text-[#c93636]">
                      Danger Zone
                    </h2>

                    <p className="mt-1 text-sm leading-6 text-[#667085]">
                      These actions can affect your organization and should
                      only be performed when necessary.
                    </p>
                  </div>

                </div>

                <div className="mt-6 flex flex-col gap-4 rounded-xl border border-[#f0caca] p-5 sm:flex-row sm:items-center sm:justify-between">

                  <div>
                    <h3 className="text-sm font-bold text-[#344054]">
                      Delete Organization
                    </h3>

                    <p className="mt-1 text-xs leading-5 text-[#667085]">
                      Permanently delete the organization and its data.
                    </p>
                  </div>

                  <button
                    onClick={() =>
                      alert(
                        "Organization deletion will be connected to the backend later."
                      )
                    }
                    className="shrink-0 rounded-lg border border-[#e06b6b] px-4 py-2.5 text-sm font-semibold text-[#c93636] transition hover:bg-[#fff5f5]"
                  >
                    Delete Organization
                  </button>

                </div>

              </div>
            </div>

          </div>
        </div>
      </div>
    </div>
  );
}

/* =========================================
   SAVE BUTTON
========================================= */

function SaveButton({
  saved,
  onClick,
}: {
  saved: boolean;
  onClick: () => void;
}) {
  return (
    <div className="flex items-center justify-end gap-3 border-t border-[#edf0f4] px-6 py-5 sm:px-8">

      {saved && (
        <span className="inline-flex items-center gap-2 text-sm font-medium text-[#16834b]">
          <CheckCircle2 size={17} />
          Changes saved
        </span>
      )}

      <button
        onClick={onClick}
        className="inline-flex items-center gap-2 rounded-lg bg-[#126df5] px-5 py-3 text-sm font-semibold text-white transition hover:bg-[#0d5ed7]"
      >
        <Save size={17} />
        Save Changes
      </button>

    </div>
  );
}

/* =========================================
   SECURITY SETTING
========================================= */

function SecuritySetting({
  icon,
  title,
  description,
  button,
}: {
  icon: React.ReactNode;
  title: string;
  description: string;
  button: string;
}) {
  return (
    <div className="flex flex-col gap-4 p-6 sm:flex-row sm:items-center sm:justify-between sm:px-8">

      <div className="flex items-start gap-4">

        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-[#eef5ff] text-[#126df5]">
          {icon}
        </div>

        <div>
          <h3 className="text-sm font-bold text-[#344054]">
            {title}
          </h3>

          <p className="mt-1 max-w-xl text-xs leading-5 text-[#667085]">
            {description}
          </p>
        </div>

      </div>

      <button
        onClick={() =>
          alert(`${title} will be connected to the backend later.`)
        }
        className="w-fit rounded-lg border border-[#dce2ea] px-4 py-2.5 text-sm font-semibold text-[#344054] hover:bg-[#f7f9fc]"
      >
        {button}
      </button>

    </div>
  );
}

/* =========================================
   PASSWORD FIELD
========================================= */

function PasswordField({
  label,
}: {
  label: string;
}) {
  return (
    <div>
      <label className="mb-2 block text-sm font-semibold text-[#344054]">
        {label}
      </label>

      <input
        type="password"
        placeholder="••••••••"
        className="h-11 w-full rounded-lg border border-[#dce2ea] px-4 text-sm text-[#344054] outline-none placeholder:text-[#98a2b3] focus:border-[#126df5] focus:ring-2 focus:ring-[#126df5]/10"
      />
    </div>
  );
}

/* =========================================
   NOTIFICATION SETTING
========================================= */

function NotificationSetting({
  title,
  description,
  enabled,
  onChange,
}: {
  title: string;
  description: string;
  enabled: boolean;
  onChange: (value: boolean) => void;
}) {
  return (
    <div className="flex items-center justify-between gap-5 p-6 sm:px-8">

      <div>
        <h3 className="text-sm font-bold text-[#344054]">
          {title}
        </h3>

        <p className="mt-1 text-xs leading-5 text-[#667085]">
          {description}
        </p>
      </div>

      <button
        type="button"
        onClick={() => onChange(!enabled)}
        className={`relative h-6 w-11 shrink-0 rounded-full transition ${
          enabled ? "bg-[#126df5]" : "bg-[#cbd5e1]"
        }`}
        aria-label={`Toggle ${title}`}
      >
        <span
          className={`absolute top-1 h-4 w-4 rounded-full bg-white shadow-sm transition ${
            enabled ? "left-6" : "left-1"
          }`}
        />
      </button>

    </div>
  );
}