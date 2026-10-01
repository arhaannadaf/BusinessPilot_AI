"use client";

import Link from "next/link";
import {
  Mail,
  Lock,
  Eye,
  EyeOff,
  User,
  CheckCircle2,
  Send,
} from "lucide-react";
import { useState } from "react";

export default function SignupPage() {
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  return (
    <main className="min-h-screen bg-[#eef4fc]">

      {/* =========================================
          HEADER
      ========================================= */}

      <header className="flex w-full items-center justify-between px-6 py-5 sm:px-10 lg:px-16">

        {/* BusinessPilot Logo */}

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


        {/* Sign in */}

        <p className="hidden text-sm text-slate-500 sm:block">
          Already have an account?{" "}
          <Link
            href="/login"
            className="font-semibold text-blue-600 hover:text-blue-700"
          >
            Sign in
          </Link>
        </p>

      </header>


      {/* =========================================
          SIGNUP CONTAINER
      ========================================= */}

      <section className="mx-auto flex w-full max-w-[1250px] px-5 pb-10 sm:px-8 lg:px-10">

        <div className="grid w-full overflow-hidden rounded-2xl shadow-sm lg:grid-cols-2">


          {/* =====================================
              LEFT INFORMATION PANEL
          ===================================== */}

          <div className="relative hidden min-h-[720px] overflow-hidden bg-[#eef5ff] px-10 py-12 lg:flex lg:flex-col">

            {/* Decorative circles */}

            <div className="absolute -bottom-28 -left-20 h-72 w-72 rounded-full bg-blue-200/40" />

            <div className="absolute bottom-[-80px] right-[-100px] h-72 w-72 rounded-full bg-blue-300/30" />


            {/* Heading */}

            <div className="relative z-10 mt-8">

              <h2 className="max-w-[370px] text-4xl font-bold leading-tight text-[#101b30] xl:text-5xl">
                Join{" "}
                <span className="text-blue-600">
                  BusinessPilot
                </span>
              </h2>

              <p className="mt-4 max-w-[390px] text-lg leading-7 text-slate-500">
                Start your journey towards smarter
                business decisions.
              </p>

            </div>


            {/* Illustration */}

            <div className="relative z-10 mt-16 flex flex-1 items-center justify-center">

              <div className="relative h-[300px] w-[390px]">

                {/* Chart window */}

                <div className="absolute left-1/2 top-1/2 h-[180px] w-[250px] -translate-x-1/2 -translate-y-1/2 rounded-xl border border-blue-100 bg-white p-5 shadow-xl">

                  {/* Window dots */}

                  <div className="mb-5 flex gap-1.5">

                    <span className="h-2 w-2 rounded-full bg-slate-300" />
                    <span className="h-2 w-2 rounded-full bg-slate-300" />
                    <span className="h-2 w-2 rounded-full bg-slate-300" />

                  </div>


                  {/* Bars */}

                  <div className="flex h-[105px] items-end justify-center gap-4">

                    <div className="h-[40px] w-7 rounded-t bg-blue-200" />
                    <div className="h-[65px] w-7 rounded-t bg-blue-300" />
                    <div className="h-[50px] w-7 rounded-t bg-blue-400" />
                    <div className="h-[85px] w-7 rounded-t bg-blue-500" />

                  </div>

                </div>


                {/* Analyze card */}

                <div className="absolute left-0 top-5 flex items-center gap-3 rounded-xl bg-white px-4 py-3 shadow-lg">

                  <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-blue-100">

                    <CheckCircle2
                      size={20}
                      className="text-blue-600"
                    />

                  </div>

                  <span className="text-sm font-semibold text-slate-700">
                    Analyze
                  </span>

                </div>


                {/* Simulate card */}

                <div className="absolute right-0 top-16 flex items-center gap-3 rounded-xl bg-white px-4 py-3 shadow-lg">

                  <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-emerald-100">

                    <CheckCircle2
                      size={20}
                      className="text-emerald-500"
                    />

                  </div>

                  <span className="text-sm font-semibold text-slate-700">
                    Simulate
                  </span>

                </div>


                {/* Decide card */}

                <div className="absolute bottom-10 left-5 flex items-center gap-3 rounded-xl bg-white px-4 py-3 shadow-lg">

                  <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-purple-100">

                    <CheckCircle2
                      size={20}
                      className="text-purple-500"
                    />

                  </div>

                  <span className="text-sm font-semibold text-slate-700">
                    Decide
                  </span>

                </div>


                {/* Grow card */}

                <div className="absolute bottom-0 right-3 flex items-center gap-3 rounded-xl bg-white px-4 py-3 shadow-lg">

                  <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-amber-100">

                    <CheckCircle2
                      size={20}
                      className="text-amber-500"
                    />

                  </div>

                  <span className="text-sm font-semibold text-slate-700">
                    Grow
                  </span>

                </div>

              </div>

            </div>


            {/* Quote */}

            <div className="relative z-10 mt-auto">

              <div className="mb-4 h-[3px] w-9 rounded-full bg-blue-500" />

              <p className="text-lg italic leading-7 text-slate-600">
                "Empowering teams
                <br />
                with data-driven decisions."
              </p>

            </div>

          </div>


          {/* =====================================
              RIGHT SIGNUP FORM
          ===================================== */}

          <div className="flex min-h-[720px] items-center justify-center bg-white px-6 py-10 sm:px-12 lg:px-14">

            <div className="w-full max-w-[440px]">

              {/* Heading */}

              <div className="mb-7">

                <h2 className="text-3xl font-bold tracking-tight text-[#101b30] sm:text-4xl">
                  Create Your Account
                </h2>

                <p className="mt-2 text-sm leading-6 text-slate-500">
                  Join BusinessPilot and start making
                  better decisions today.
                </p>

              </div>


              {/* Form */}

              <form
                onSubmit={(event) => {
                  event.preventDefault();
                  alert(
                    "Account creation will be connected to the backend later."
                  );
                }}
                className="space-y-5"
              >

                {/* FULL NAME */}

                <div>

                  <label
                    htmlFor="fullName"
                    className="mb-2 block text-sm font-semibold text-slate-700"
                  >
                    Full Name
                  </label>

                  <div className="flex h-12 items-center rounded-md border border-slate-300 bg-white px-3 transition focus-within:border-blue-500 focus-within:ring-4 focus-within:ring-blue-500/10">

                    <User
                      size={19}
                      className="mr-3 shrink-0 text-slate-400"
                    />

                    <input
                      id="fullName"
                      type="text"
                      placeholder="Enter your full name"
                      className="h-full w-full bg-transparent text-sm text-slate-700 outline-none placeholder:text-slate-400"
                      required
                    />

                  </div>

                </div>


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
                      placeholder="Create a password"
                      className="h-full w-full bg-transparent text-sm text-slate-700 outline-none placeholder:text-slate-400"
                      required
                    />

                    <button
                      type="button"
                      onClick={() =>
                        setShowPassword(!showPassword)
                      }
                      className="ml-2 flex h-8 w-8 shrink-0 items-center justify-center text-slate-400 hover:text-slate-600"
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


                  {/* Password requirements */}

                  <div className="mt-2 space-y-1">

                    <p className="flex items-center gap-2 text-xs text-slate-400">
                      <span className="h-2.5 w-2.5 rounded-full border border-slate-300" />
                      At least 8 characters
                    </p>

                    <p className="flex items-center gap-2 text-xs text-slate-400">
                      <span className="h-2.5 w-2.5 rounded-full border border-slate-300" />
                      Includes a number
                    </p>

                    <p className="flex items-center gap-2 text-xs text-slate-400">
                      <span className="h-2.5 w-2.5 rounded-full border border-slate-300" />
                      Includes a special character
                    </p>

                  </div>

                </div>


                {/* CONFIRM PASSWORD */}

                <div>

                  <label
                    htmlFor="confirmPassword"
                    className="mb-2 block text-sm font-semibold text-slate-700"
                  >
                    Confirm Password
                  </label>

                  <div className="flex h-12 items-center rounded-md border border-slate-300 bg-white px-3 transition focus-within:border-blue-500 focus-within:ring-4 focus-within:ring-blue-500/10">

                    <Lock
                      size={19}
                      className="mr-3 shrink-0 text-slate-400"
                    />

                    <input
                      id="confirmPassword"
                      type={
                        showConfirmPassword
                          ? "text"
                          : "password"
                      }
                      placeholder="Confirm your password"
                      className="h-full w-full bg-transparent text-sm text-slate-700 outline-none placeholder:text-slate-400"
                      required
                    />

                    <button
                      type="button"
                      onClick={() =>
                        setShowConfirmPassword(
                          !showConfirmPassword
                        )
                      }
                      className="ml-2 flex h-8 w-8 shrink-0 items-center justify-center text-slate-400 hover:text-slate-600"
                      aria-label={
                        showConfirmPassword
                          ? "Hide password"
                          : "Show password"
                      }
                    >
                      {showConfirmPassword ? (
                        <EyeOff size={18} />
                      ) : (
                        <Eye size={18} />
                      )}
                    </button>

                  </div>

                </div>


                {/* TERMS */}

                <label className="flex items-start gap-3 text-xs leading-5 text-slate-500">

                  <input
                    type="checkbox"
                    required
                    className="mt-1 h-4 w-4 shrink-0 accent-blue-600"
                  />

                  <span>
                    I agree to the{" "}
                    <a
                      href="#"
                      className="font-medium text-blue-600 hover:text-blue-700"
                    >
                      Terms of Service
                    </a>{" "}
                    and{" "}
                    <a
                      href="#"
                      className="font-medium text-blue-600 hover:text-blue-700"
                    >
                      Privacy Policy
                    </a>
                  </span>

                </label>


                {/* CREATE ACCOUNT */}

                <button
                  type="submit"
                  className="flex h-12 w-full items-center justify-center rounded-md bg-blue-600 text-sm font-semibold text-white shadow-sm transition hover:bg-blue-700 active:scale-[0.99]"
                >
                  Create Account
                </button>

              </form>


              {/* OR */}

              <div className="my-6 flex items-center gap-4">

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
                  alert(
                    "Google signup will be connected later."
                  )
                }
                className="flex h-12 w-full items-center justify-center gap-3 rounded-md border border-slate-300 bg-white text-sm font-semibold text-slate-700 transition hover:bg-slate-50"
              >

                <span className="text-lg font-bold text-blue-500">
                  G
                </span>

                Continue with Google

              </button>


              {/* MOBILE SIGN IN */}

              <p className="mt-7 text-center text-sm text-slate-500 sm:hidden">

                Already have an account?{" "}

                <Link
                  href="/login"
                  className="font-semibold text-blue-600 hover:text-blue-700"
                >
                  Sign in
                </Link>

              </p>

            </div>

          </div>

        </div>

      </section>

    </main>
  );
}