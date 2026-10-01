"use client";

import Link from "next/link";
import { Mail, ArrowLeft, Send, CheckCircle2 } from "lucide-react";
import { useState } from "react";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();

    setSubmitted(true);
  };

  return (
    <main className="min-h-screen bg-[#eef4fc]">

      {/* =========================================
          HEADER
      ========================================= */}

      <header className="flex w-full items-center px-6 py-5 sm:px-10 lg:px-16">

        <Link
          href="/login"
          className="flex items-center gap-3"
        >

          {/* Logo */}

          <div className="relative flex h-11 w-11 items-center justify-center">

            <Send
              size={40}
              strokeWidth={2.5}
              className="rotate-[-35deg] text-blue-600"
              fill="currentColor"
            />

          </div>


          {/* Brand */}

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
          MAIN CONTENT
      ========================================= */}

      <section className="flex min-h-[calc(100vh-90px)] items-center justify-center px-5 pb-12 sm:px-8">

        <div className="w-full max-w-[1050px] overflow-hidden rounded-2xl bg-white shadow-sm">


          {/* =====================================
              CONTENT
          ===================================== */}

          <div className="grid min-h-[580px] lg:grid-cols-2">


            {/* =================================
                LEFT INFORMATION PANEL
            ================================= */}

            <div className="relative hidden overflow-hidden bg-[#142844] px-10 py-12 text-white lg:flex lg:flex-col">

              {/* Decorative circles */}

              <div className="absolute -bottom-32 -left-10 h-64 w-64 rounded-full bg-blue-500/20" />

              <div className="absolute -bottom-24 right-[-80px] h-64 w-64 rounded-full bg-blue-400/20" />


              {/* Heading */}

              <div className="relative z-10 mt-10">

                <div className="mb-6 h-[3px] w-10 rounded-full bg-blue-400" />

                <h2 className="max-w-[390px] text-4xl font-bold leading-tight xl:text-5xl">
                  Secure Your
                  <br />
                  <span className="text-blue-400">
                    BusinessPilot
                  </span>
                  <br />
                  Account
                </h2>

                <p className="mt-6 max-w-[390px] text-base leading-7 text-slate-200">
                  Don't worry. It happens to everyone.
                  We'll help you get back into your
                  account securely.
                </p>

              </div>


              {/* Security information */}

              <div className="relative z-10 mt-12 space-y-6">

                <div className="flex items-start gap-4">

                  <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-blue-500/20">

                    <CheckCircle2
                      size={20}
                      className="text-blue-300"
                    />

                  </div>

                  <div>

                    <h3 className="text-sm font-semibold">
                      Secure Reset
                    </h3>

                    <p className="mt-1 text-xs leading-5 text-slate-300">
                      We'll send a secure password
                      reset link to your email.
                    </p>

                  </div>

                </div>


                <div className="flex items-start gap-4">

                  <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-blue-500/20">

                    <CheckCircle2
                      size={20}
                      className="text-blue-300"
                    />

                  </div>

                  <div>

                    <h3 className="text-sm font-semibold">
                      Protected Account
                    </h3>

                    <p className="mt-1 text-xs leading-5 text-slate-300">
                      Your account and business data
                      remain protected.
                    </p>

                  </div>

                </div>

              </div>


              {/* Quote */}

              <div className="relative z-10 mt-auto">

                <div className="mb-4 h-[3px] w-8 rounded-full bg-blue-400" />

                <p className="max-w-[330px] text-lg italic leading-7 text-slate-200">
                  "Your data deserves
                  <br />
                  to stay secure."
                </p>

              </div>

            </div>


            {/* =================================
                RIGHT FORM
            ================================= */}

            <div className="flex items-center justify-center px-6 py-14 sm:px-12 lg:px-16">

              <div className="w-full max-w-[420px]">


                {!submitted ? (

                  <>
                    {/* Heading */}

                    <div className="mb-9">

                      <h2 className="text-3xl font-bold tracking-tight text-[#101b30] sm:text-4xl">
                        Forgot Password?
                      </h2>

                      <p className="mt-3 text-sm leading-6 text-slate-500">
                        Enter your email address and we'll
                        send you a link to reset your password.
                      </p>

                    </div>


                    {/* Form */}

                    <form
                      onSubmit={handleSubmit}
                      className="space-y-6"
                    >

                      {/* Email */}

                      <div>

                        <label
                          htmlFor="email"
                          className="mb-2 block text-sm font-semibold text-slate-700"
                        >
                          Email Address
                        </label>

                        <div className="flex h-12 items-center rounded-md border border-slate-300 bg-white px-3 transition focus-within:border-blue-500 focus-within:ring-4 focus-within:ring-blue-500/10">

                          <Mail
                            size={19}
                            className="mr-3 shrink-0 text-slate-400"
                          />

                          <input
                            id="email"
                            type="email"
                            value={email}
                            onChange={(event) =>
                              setEmail(event.target.value)
                            }
                            placeholder="you@company.com"
                            required
                            className="h-full w-full bg-transparent text-sm text-slate-700 outline-none placeholder:text-slate-400"
                          />

                        </div>

                      </div>


                      {/* Send Button */}

                      <button
                        type="submit"
                        className="flex h-12 w-full items-center justify-center gap-2 rounded-md bg-blue-600 text-sm font-semibold text-white shadow-sm transition hover:bg-blue-700 active:scale-[0.99]"
                      >
                        <Send size={17} />
                        Send Reset Link
                      </button>

                    </form>


                    {/* Back to login */}

                    <div className="mt-8 text-center">

                      <Link
                        href="/login"
                        className="inline-flex items-center gap-2 text-sm font-semibold text-blue-600 hover:text-blue-700"
                      >
                        <ArrowLeft size={16} />
                        Back to Sign In
                      </Link>

                    </div>

                  </>

                ) : (

                  /* =================================
                     SUCCESS MESSAGE
                  ================================= */

                  <div className="text-center">

                    <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-green-100">

                      <CheckCircle2
                        size={32}
                        className="text-green-600"
                      />

                    </div>


                    <h2 className="mt-6 text-3xl font-bold tracking-tight text-[#101b30]">
                      Check Your Email
                    </h2>


                    <p className="mt-4 text-sm leading-6 text-slate-500">
                      If an account exists for
                    </p>

                    <p className="mt-1 font-semibold text-slate-700">
                      {email}
                    </p>

                    <p className="mt-1 text-sm leading-6 text-slate-500">
                      we've sent instructions to reset
                      your password.
                    </p>


                    {/* Back */}

                    <Link
                      href="/login"
                      className="mt-8 inline-flex h-12 items-center justify-center gap-2 rounded-md bg-blue-600 px-6 text-sm font-semibold text-white transition hover:bg-blue-700"
                    >
                      <ArrowLeft size={16} />
                      Back to Sign In
                    </Link>

                  </div>

                )}

              </div>

            </div>

          </div>

        </div>

      </section>

    </main>
  );
}