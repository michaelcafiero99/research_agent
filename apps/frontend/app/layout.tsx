import "./globals.css";
import { Public_Sans, Source_Serif_4, JetBrains_Mono } from "next/font/google";
import { Toaster } from "@/components/ui/sonner";

const publicSans = Public_Sans({ subsets: ["latin"] });

const sourceSerif = Source_Serif_4({
  subsets: ["latin"],
  weight: ["400", "600"],
  variable: "--font-serif",
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  weight: ["400", "500"],
  variable: "--font-mono",
});

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <title>Morning Paper</title>
        <link rel="shortcut icon" href="/images/favicon.ico" />
        <meta name="description" content="Morning Paper — AI-powered research scout" />
      </head>
      <body
        className={`${publicSans.className} ${sourceSerif.variable} ${jetbrainsMono.variable}`}
      >
          <div className="bg-zinc-100 grid grid-rows-[auto,1fr] h-[100dvh]">
            <div className="px-6 py-4">
              <a href="/" className="font-serif-display text-xl tracking-tight text-zinc-900">
                Morning Paper
              </a>
            </div>
            <div className="bg-white mx-4 relative grid rounded-t-2xl border border-zinc-200 border-b-0 shadow-[0_-4px_24px_rgba(0,0,0,0.04)]">
              <div className="absolute inset-0">{children}</div>
            </div>
          </div>
          <Toaster />
      </body>
    </html>
  );
}
