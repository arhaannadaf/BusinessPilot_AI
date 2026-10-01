"use client";

import { Search, Bell, ChevronDown } from "lucide-react";

export default function TopHeader() {
  return (
    <header className="sticky top-0 z-30 flex h-[76px] w-full items-center border-b border-[#e5eaf1] bg-white px-4 sm:px-6 lg:px-8">
      <div className="flex w-full items-center justify-between gap-3">

        {/* Search */}
        <div className="relative min-w-0 flex-1 max-w-[560px]">
          <Search
            size={20}
            className="absolute left-3.5 top-1/2 -translate-y-1/2 text-[#667085] sm:left-4"
          />

          <input
            type="text"
            placeholder="Search anything..."
            className="h-11 w-full rounded-xl border border-[#dce2ea] bg-[#f8fafc] pl-10 pr-3 text-sm text-[#344054] outline-none transition placeholder:text-[#98a2b3] focus:border-[#126df5] focus:bg-white focus:ring-2 focus:ring-[#126df5]/10 sm:pl-11 sm:pr-4"
          />
        </div>

        {/* Right Side */}
        <div className="flex shrink-0 items-center gap-1 sm:gap-3">

          {/* Notifications */}
          <button
            onClick={() => alert("Notifications will be connected later.")}
            className="relative flex h-10 w-10 items-center justify-center rounded-full text-[#667085] transition hover:bg-[#f2f4f7] hover:text-[#126df5]"
            aria-label="Notifications"
          >
            <Bell size={20} />

            <span className="absolute right-2 top-1.5 h-2.5 w-2.5 rounded-full border-2 border-white bg-[#ef4444]" />
          </button>

          {/* Divider */}
          <div className="hidden h-8 w-px bg-[#e5eaf1] sm:block" />

          {/* User */}
          <button
            onClick={() => alert("Profile menu will be connected later.")}
            className="flex items-center gap-2 rounded-xl p-1.5 transition hover:bg-[#f7f9fc] sm:gap-3 sm:px-2"
          >
            {/* Avatar */}
            <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-[#126df5] text-xs font-bold text-white sm:h-10 sm:w-10 sm:text-sm">
              JD
            </div>

            {/* User Information */}
            <div className="hidden text-left md:block">
              <p className="text-sm font-semibold text-[#172033]">
                John Doe
              </p>

              <p className="text-xs text-[#667085]">
                Admin
              </p>
            </div>

            <ChevronDown
              size={17}
              className="hidden text-[#667085] md:block"
            />
          </button>
        </div>
      </div>
    </header>
  );
}