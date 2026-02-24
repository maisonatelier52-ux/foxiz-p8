import type { Metadata } from 'next';
import { Inter, Playfair_Display } from 'next/font/google';
import './globals.css';

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
});

const playfair = Playfair_Display({
  subsets: ['latin'],
  variable: '--font-playfair',
  display: 'swap',
});

export const metadata: Metadata = {
  title: {
    default: 'Nexus News | Global Perspective & Premium Insights',
    template: '%s | Nexus News'
  },
  description: 'Unrivaled news coverage and expert analysis for the discerning reader.',
  keywords: ['news', 'finance', 'tech', 'lifestyle', 'premium insights'],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${inter.variable} ${playfair.variable}`} suppressHydrationWarning>
      <body className="antialiased font-sans">
        {children}
      </body>
    </html>
  );
}
