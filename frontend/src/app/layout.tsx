import type { Metadata, Viewport } from "next";
import { Inter } from "next/font/google";

import { QueryProvider } from "@/providers/query-provider";
import { ThemeProvider } from "@/providers/theme-provider";

import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Krishiva AI — Your farming assistant",
  description:
    "Krishiva AI is the farmer's intelligent copilot — diagnose crop diseases, get treatment advice, and answers grounded in an agricultural knowledge base.",
  applicationName: "Krishiva AI",
};

export const viewport: Viewport = {
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#ffffff" },
    { media: "(prefers-color-scheme: dark)", color: "#0a0a0c" },
  ],
  width: "device-width",
  initialScale: 1,
};

// Set the theme class before first paint to avoid a flash (PRD §11.4).
const themeScript = `(function(){try{var t=JSON.parse(localStorage.getItem('krishiva.ui')||'{}').state?.theme||'system';var d=t==='dark'||(t==='system'&&matchMedia('(prefers-color-scheme: dark)').matches);document.documentElement.classList.toggle('dark',d);}catch(e){}})();`;

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <script dangerouslySetInnerHTML={{ __html: themeScript }} />
      </head>
      <body className={`${inter.variable} antialiased`}>
        <QueryProvider>
          <ThemeProvider>{children}</ThemeProvider>
        </QueryProvider>
      </body>
    </html>
  );
}
