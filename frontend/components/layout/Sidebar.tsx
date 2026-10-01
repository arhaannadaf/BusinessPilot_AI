"use client";

import Image from "next/image";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Building2,
  Users,
  ShieldCheck,
  UsersRound,
  LockKeyhole,
  FileText,
  Settings,
  ArrowUpRight,
  X,
  Menu,
} from "lucide-react";
import { useState } from "react";

const menuItems = [
  {
    label: "Dashboard",
    href: "/dashboard",
    icon: LayoutDashboard,
  },
  {
    label: "Organizations",
    href: "/organizations",
    icon: Building2,
  },
  {
    label: "Users",
    href: "/users",
    icon: Users,
  },
  {
    label: "Roles & Permissions",
    href: "/roles",
    icon: ShieldCheck,
  },
  {
    label: "Teams",
    href: "/teams",
    icon: UsersRound,
  },
  {
    label: "Authentication",
    href: "/authentication",
    icon: LockKeyhole,
  },
  {
    label: "Audit Logs",
    href: "/audit-logs",
    icon: FileText,
  },
  {
    label: "Settings",
    href: "/settings",
    icon: Settings,
  },
];

export default function Sidebar() {
  const pathname = usePathname();
  const [isOpen, setIsOpen] = useState(false);

  const closeSidebar = () => {
    setIsOpen(false);
  };

  return (
    <>
      {/* Mobile Menu Button */}
      <button
        onClick={() => setIsOpen(true)}
        className="fixed left-4 top-4 z-50 flex h-11 w-11 items-center justify-center rounded-xl border border-[#e5eaf1] bg-white text-[#344054] shadow-sm transition hover:bg-[#f7f9fc] lg:hidden"
        aria-label="Open navigation menu"
      >
        <Menu size={22} />
      </button>

      {/* Mobile Overlay */}
      {isOpen && (
        <button
          onClick={closeSidebar}
          aria-label="Close navigation menu"
          className="fixed inset-0 z-40 bg-[#172033]/50 lg:hidden"
        />
      )}

      {/* Sidebar */}
      <aside
        className={`fixed left-0 top-0 z-50 flex h-screen w-[280px] shrink-0 flex-col border-r border-[#e5eaf1] bg-white transition-transform duration-300 lg:static lg:z-auto lg:translate-x-0 ${
          isOpen ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        {/* Logo */}
        <div className="flex h-[96px] items-center justify-between border-b border-[#edf0f4] px-6">
          <Link
            href="/dashboard"
            onClick={closeSidebar}
            className="block transition-opacity hover:opacity-90"
          >
            <Image
              src="/images/businesspilot-logo.png"
              alt="BusinessPilot AI"
              width={225}
              height={85}
              priority
              className="h-auto w-[205px] object-contain"
            />
          </Link>

          {/* Mobile Close Button */}
          <button
            onClick={closeSidebar}
            className="flex h-9 w-9 items-center justify-center rounded-lg text-[#667085] transition hover:bg-[#f2f4f7] hover:text-[#344054] lg:hidden"
            aria-label="Close navigation menu"
          >
            <X size={21} />
          </button>
        </div>

        {/* Navigation */}
        <nav className="flex-1 overflow-y-auto px-4 py-6">
          <div className="space-y-1.5">
            {menuItems.map((item) => {
              const Icon = item.icon;

              const isActive =
                pathname === item.href ||
                (item.href !== "/dashboard" &&
                  pathname.startsWith(`${item.href}/`));

              return (
                <Link
                  key={item.href}
                  href={item.href}
                  onClick={closeSidebar}
                  className={`group flex min-h-[48px] items-center gap-3 rounded-lg px-4 text-sm font-semibold transition ${
                    isActive
                      ? "bg-[#eef5ff] text-[#126df5]"
                      : "text-[#344054] hover:bg-[#f7f9fc] hover:text-[#126df5]"
                  }`}
                >
                  <Icon
                    size={21}
                    strokeWidth={isActive ? 2.3 : 2}
                    className={`shrink-0 ${
                      isActive
                        ? "text-[#126df5]"
                        : "text-[#667085] group-hover:text-[#126df5]"
                    }`}
                  />

                  <span>{item.label}</span>
                </Link>
              );
            })}
          </div>
        </nav>

        {/* Bottom Branding */}
        <div className="px-5 pb-6">
          <div className="relative overflow-hidden rounded-2xl bg-[#f5f9ff] px-5 py-6">
            <div className="relative z-10">
              <p className="text-sm font-bold leading-5 text-[#126df5]">
                Better decisions.
                <br />
                Stronger businesses.
              </p>

              <Link
                href="/dashboard"
                onClick={closeSidebar}
                className="mt-4 inline-flex items-center gap-1.5 text-xs font-semibold text-[#667085] transition hover:text-[#126df5]"
              >
                Explore BusinessPilot
                <ArrowUpRight size={14} />
              </Link>
            </div>

            {/* Decorative Shape */}
            <div className="absolute -bottom-10 -right-8 h-28 w-28 rotate-12 rounded-3xl border-[14px] border-[#dceaff] opacity-70" />
          </div>
        </div>
      </aside>
    </>
  );
}