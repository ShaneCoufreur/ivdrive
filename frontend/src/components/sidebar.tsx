"use client";

import Link from "next/link";
import Image from "next/image";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Settings,
  LogOut,
  ChevronLeft,
  ChevronRight,
  Sun,
  Moon,
} from "lucide-react";
import { useState, useEffect } from "react";
import { useTheme } from "next-themes";
import { useAuth } from "@/lib/auth-context";

const navItems = [
  { href: "/", icon: LayoutDashboard, label: "Dashboard" },
  { href: "/settings", icon: Settings, label: "Settings" },
];

export function Sidebar() {
  const pathname = usePathname();
  const { user, logout } = useAuth();
  const [collapsed, setCollapsed] = useState(false);
  const { theme, setTheme, resolvedTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => setMounted(true), []);

  const isDark = mounted && resolvedTheme === "dark";

  return (
    <aside
      className={`fixed left-0 top-0 h-screen bg-iv-charcoal/80 backdrop-blur-xl border-r border-iv-border flex flex-col z-50 transition-all duration-300 ${
        collapsed ? "w-[72px]" : "w-[240px]"
      }`}
    >
      <div className="flex items-center gap-3 p-4 border-b border-iv-border">
        <Image
          src="/logo.png"
          alt="iVDrive"
          width={40}
          height={40}
          className="rounded-lg flex-shrink-0"
        />
        {!collapsed && (
          <div className="flex flex-col">
            <span className="text-lg font-bold leading-none">
              <span className="gradient-text">iV</span>
              <span className="text-iv-glow">Drive</span>
            </span>
            <span className="text-[10px] font-semibold text-iv-warning tracking-widest uppercase mt-0.5">
              Beta
            </span>
          </div>
        )}
      </div>

      <nav className="flex-1 py-4 space-y-1 px-2">
        {navItems.map((item) => {
          const isActive =
            item.href === "/"
              ? pathname === "/" || pathname.startsWith("/vehicles")
              : pathname.startsWith(item.href);
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all ${
                isActive
                  ? "bg-iv-green/15 text-iv-green"
                  : "text-iv-muted hover:text-iv-text hover:bg-iv-surface"
              }`}
            >
              <item.icon size={20} className="flex-shrink-0" />
              {!collapsed && <span className="text-sm font-medium">{item.label}</span>}
            </Link>
          );
        })}
      </nav>

      <div className="border-t border-iv-border p-3 space-y-2">
        {!collapsed && user && (
          <div className="px-2 py-1">
            <p className="text-xs text-iv-muted truncate">{user.email}</p>
          </div>
        )}

        <button
          onClick={() => setTheme(isDark ? "light" : "dark")}
          className="flex items-center gap-3 px-3 py-2 rounded-lg text-iv-muted hover:text-iv-text hover:bg-iv-surface transition-all w-full"
          title={isDark ? "Switch to light mode" : "Switch to dark mode"}
        >
          {mounted ? (
            isDark ? <Sun size={18} className="flex-shrink-0" /> : <Moon size={18} className="flex-shrink-0" />
          ) : (
            <Sun size={18} className="flex-shrink-0" />
          )}
          {!collapsed && <span className="text-sm">{mounted ? (isDark ? "Light Mode" : "Dark Mode") : "Theme"}</span>}
        </button>

        <button
          onClick={logout}
          className="flex items-center gap-3 px-3 py-2 rounded-lg text-iv-muted hover:text-iv-danger hover:bg-iv-danger/10 transition-all w-full"
        >
          <LogOut size={18} className="flex-shrink-0" />
          {!collapsed && <span className="text-sm">Logout</span>}
        </button>
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="flex items-center justify-center w-full py-1 text-iv-muted hover:text-iv-text transition-colors"
        >
          {collapsed ? <ChevronRight size={16} /> : <ChevronLeft size={16} />}
        </button>
      </div>
    </aside>
  );
}
