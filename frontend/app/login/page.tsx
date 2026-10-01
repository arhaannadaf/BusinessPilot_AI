"use client";

import Link from "next/link";
import {
  Mail,
  Lock,
  Eye,
  EyeOff,
  BarChart3,
  Lightbulb,
  SlidersHorizontal,
  Target,
  Send,
} from "lucide-react";
import { useState } from "react";

export default function LoginPage() {
  const [showPassword, setShowPassword] = useState(false);

  return (
    <main className="min-h-screen bg-[#eef4fc]">

      {/* =========================================
          HEADER
      ========================================= */}

      <header className="flex w-full items-center justify-between px-6 py-5 sm:px-10 lg:px-16">

        {/* Logo */}

        <Link href="/login" className="flex items-center gap-3">

          <div className="relative flex h-11 w-11 items-center justify-center">

            <Send
              size={40}
              strokeWidth={2.5}
              className="rotate-[-35deg] text-blue-600"
              fill="currentColor"
            />

          </div>

          <div className="-ml-1">
            <h1 className="text-2xl font-extrabold tracking-tight text-[#101b30] sm:text-3xl">
              Business<span className="text-blue-600">Pilot</span>
            </h1>

            <p className="text-[10px] font-medium tracking-wide text-slate-500 sm:text-xs">
              Data to Decisions. Faster.
            </p>
          </div>

        </Link>

      </header>


      {/* =========================================
          LOGIN CONTAINER
      ========================================= */}

      <section className="mx-auto flex w-full max-w-[1250px] px-5 pb-10 sm:px-8 lg:px-10">

        <div className="grid w-full overflow-hidden rounded-2xl shadow-sm lg:grid-cols-2">


          {/* =====================================
              LEFT INFORMATION PANEL
          ===================================== */}

          <div className="relative hidden min-h-[650px] overflow-hidden bg-[#142844] px-10 py-12 text-white lg:flex lg:flex-col">

            {/* Decorative background */}

            <div className="absolute -bottom-32 -left-10 h-64 w-64 rounded-full bg-blue-500/20" />

            <div className="absolute -bottom-24 right-[-80px] h-64 w-64 rounded-full bg-blue-400/20" />


            {/* Small line */}

            <div className="mb-6 h-[3px] w-10 rounded-full bg-blue-400" />


            {/* Main heading */}

            <h2 className="max-w-[390px] text-4xl font-bold leading-[1.2] xl:text-5xl">

              Turn Business Data
              <br />

              into{" "}

              <span className="text-blue-400">
                Better
              </span>

              <br />

              <span className="text-blue-400">
                Decisions
              </span>

            </h2>


            {/* Description */}

            <p className="mt-6 max-w-[410px] text-base leading-7 text-slate-200">
              BusinessPilot helps organizations analyze,
              simulate and make data-driven decisions with
              confidence.
            </p>


            {/* Features */}

            <div className="mt-9 flex flex-col gap-6">

              {/* Feature 1 */}

              <div className="flex items-center gap-4">

                <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-blue-500/20">

                  <BarChart3
                    size={22}
                    className="text-blue-300"
                  />

                </div>

                <div>

                  <h3 className="text-sm font-semibold">
                    Unified Business Data
                  </h3>

                  <p className="mt-1 text-xs text-slate-300">
                    Bring your data together
                  </p>

                </div>

              </div>


              {/* Feature 2 */}

              <div className="flex items-center gap-4">

                <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-blue-500/20">

                  <Lightbulb
                    size={22}
                    className="text-blue-300"
                  />

                </div>

                <div>

                  <h3 className="text-sm font-semibold">
                    Intelligent Insights
                  </h3>

                  <p className="mt-1 text-xs text-slate-300">
                    Find opportunities
                  </p>

                </div>

              </div>


              {/* Feature 3 */}

              <div className="flex items-center gap-4">

                <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-blue-500/20">

                  <SlidersHorizontal
                    size={22}
                    className="text-blue-300"
                  />

                </div>

                <div>

                  <h3 className="text-sm font-semibold">
                    What-if Scenarios
                  </h3>

                  <p className="mt-1 text-xs text-slate-300">
                    Explore different options
                  </p>

                </div>

              </div>


              {/* Feature 4 */}

              <div className="flex items-center gap-4">

                <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-blue-500/20">

                  <Target
                    size={22}
                    className="text-blue-300"
                  />

                </div>

                <div>

                  <h3 className="text-sm font-semibold">
                    Better Outcomes
                  </h3>

                  <p className="mt-1 text-xs text-slate-300">
                    Make confident decisions
                  </p>

                </div>

              </div>

            </div>


            {/* Bottom quote */}

            <div className="relative mt-auto pt-10">

              <div className="mb-4 h-[3px] w-8 rounded-full bg-blue-400" />

              <p className="max-w-[330px] text-lg italic leading-7 text-slate-200">
                "A smarter tomorrow
                <br />
                for every decision today."
              </p>

            </div>

          </div>


          {/* =====================================
              RIGHT LOGIN PANEL
          ===================================== */}

          <div className="flex min-h-[650px] items-center justify-center bg-white px-6 py-12 sm:px-12 lg:px-14">

            <div className="w-full max-w-[430px]">


              {/* Heading */}

              <div className="mb-9">

                <h2 className="text-3xl font-bold tracking-tight text-[#101b30] sm:text-4xl">
                  Welcome Back
                </h2>

                <p className="mt-2 text-sm text-slate-500">
                  Sign in to your BusinessPilot account
                </p>

              </div>


              {/* Form */}

              <form
                onSubmit={(event) => {
                  event.preventDefault();
                  alert("Login will be connected to the backend later.");
                }}
                className="space-y-6"
              >

                {/* EMAIL */}

                <div>

                  <label
                    htmlFor="email"
                    className="mb-2 block text-sm font-semibold text-slate-700"
                  >
                    Email
                  </label>

                  <div className="flex h-12 items-center rounded-md border border-slate-300 bg-white px-3 transition focus-within:border-blue-500 focus-within:ring-4 focus-within:ring-blue-500/10">

                    <Mail
                      size={19}
                      className="mr-3 shrink-0 text-slate-400"
                    />

                    <input
                      id="email"
                      type="email"
                      placeholder="you@company.com"
                      className="h-full w-full bg-transparent text-sm text-slate-700 outline-none placeholder:text-slate-400"
                      required
                    />

                  </div>

                </div>


                {/* PASSWORD */}

                <div>

                  <label
                    htmlFor="password"
                    className="mb-2 block text-sm font-semibold text-slate-700"
                  >
                    Password
                  </label>

                  <div className="flex h-12 items-center rounded-md border border-slate-300 bg-white px-3 transition focus-within:border-blue-500 focus-within:ring-4 focus-within:ring-blue-500/10">

                    <Lock
                      size={19}
                      className="mr-3 shrink-0 text-slate-400"
                    />

                    <input
                      id="password"
                      type={showPassword ? "text" : "password"}
                      placeholder="Enter your password"
                      className="h-full w-full bg-transparent text-sm text-slate-700 outline-none placeholder:text-slate-400"
                      required
                    />

                    <button
                      type="button"
                      onClick={() =>
                        setShowPassword(!showPassword)
                      }
                      className="ml-2 flex h-8 w-8 shrink-0 items-center justify-center text-slate-400 transition hover:text-slate-600"
                      aria-label={
                        showPassword
                          ? "Hide password"
                          : "Show password"
                      }
                    >
                      {showPassword ? (
                        <EyeOff size={18} />
                      ) : (
                        <Eye size={18} />
                      )}
                    </button>

                  </div>


                  {/* Forgot password */}

                  <div className="mt-2 flex justify-end">

                    <Link
                      href="/forgot-password"
                      className="text-xs font-medium text-blue-600 hover:text-blue-700"
                    >
                      Forgot password?
                    </Link>

                  </div>

                </div>


                {/* SIGN IN */}

                <button
                  type="submit"
                  className="flex h-12 w-full items-center justify-center rounded-md bg-blue-600 text-sm font-semibold text-white shadow-sm transition hover:bg-blue-700 active:scale-[0.99]"
                >
                  Sign In
                </button>

              </form>


              {/* OR */}

              <div className="my-7 flex items-center gap-4">

                <div className="h-px flex-1 bg-slate-200" />

                <span className="text-xs font-medium text-slate-400">
                  OR
                </span>

                <div className="h-px flex-1 bg-slate-200" />

              </div>


              {/* GOOGLE */}

              <button
                type="button"
                onClick={() =>
                  alert("Google login will be connected later.")
                }
                className="flex h-12 w-full items-center justify-center gap-3 rounded-md border border-slate-300 bg-white text-sm font-semibold text-slate-700 transition hover:bg-slate-50"
              >

                {/* Google G */}

                <span className="text-lg font-bold text-blue-500">
                  G
                </span>

                Continue with Google

              </button>


              {/* SIGN UP */}

              <p className="mt-8 text-center text-sm text-slate-500">

                Don't have an account?{" "}

                <Link
                  href="/signup"
                  className="font-semibold text-blue-600 hover:text-blue-700"
                >
                  Sign up
                </Link>

              </p>

            </div>

          </div>

        </div>

      </section>

    </main>
  );
}