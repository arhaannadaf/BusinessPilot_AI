import Sidebar from "@/components/layout/Sidebar";
import TopHeader from "@/components/layout/TopHeader";

export default function DashboardLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <div className="app-shell">
      <Sidebar />

      <div className="app-main">
        <TopHeader />

        <main className="page-content">
          {children}
        </main>
      </div>
    </div>
  );
}